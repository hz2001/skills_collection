---
name: af-pull-api
description: 使用 AppsFlyer Pull API 拉取原始数据报告（Raw Data）。当用户要求拉取 AF 数据、下载 in-app events、installs 报告，或需要查询某个 App 指定日期范围的 organic/non-organic 数据时使用。支持：切换报告类型（in-app events / installs）、调整日期范围、过滤 install 日期、选择返回字段。
---

# AppsFlyer Pull API Skill

## 配置文件

Token 存储路径：`memory/af_config.json`

```json
{
  "appsflyer": {
    "api_token": "<V2_TOKEN>"
  }
}
```

从文件读取 Token：
```powershell
$config = Get-Content "C:\Users\ZYB\.openclaw\workspace\memory\af_config.json" | ConvertFrom-Json
$token = $config.appsflyer.api_token
```

## 默认行为

用户未明确指定时，使用以下默认值：

| 参数 | 默认值 |
|------|--------|
| 报告类型 | `in_app_events`（organic + non-organic 各一份） |
| 日期范围 | 过去 3 天（`今天-3` 至 `今天`） |
| Install 日期限制 | 不限（不传 `from_install_time` / `to_install_time`） |
| 输出字段 | 见下方「默认字段列表」 |
| 输出目录 | `C:\Users\ZYB\Documents\af_raw_data\<今天日期>\` |

## 默认字段列表

> ⚠️ AF Pull API **不支持**在请求中指定返回字段，服务端固定返回全部 81 个字段。
> **每次下载完成后必须立即执行字段裁剪**，最终交付给用户的文件只保留以下 40 个字段。

**需要保留的字段（共 40 个）：**
```
Install Time, Event Time, Event Name, Event Value,
Event Revenue, Event Revenue Currency, Event Revenue USD,
Event Source, Media Source, Channel, Keywords,
Campaign, Campaign ID, Adset, Adset ID, Ad, Ad ID,
Country Code, State, City, Postal Code, DMA, IP,
AppsFlyer ID, Advertising ID, IDFA, Android ID,
Customer User ID, IMEI, IDFV, Platform, OS Version,
App Version, SDK Version, App ID, App Name,
Is Retargeting, User Agent, HTTP Referrer, Original URL
```

## 调用步骤

### 1. 构建 URL

```
Base URL: https://hq1.appsflyer.com/api/raw-data/export/app/

Non-Organic In-App Events:
  /{app-id}/in_app_events_report/v5?from=YYYY-MM-DD&to=YYYY-MM-DD

Organic In-App Events:
  /{app-id}/organic_in_app_events_report/v5?from=YYYY-MM-DD&to=YYYY-MM-DD

Non-Organic Installs:
  /{app-id}/installs_report/v5?from=YYYY-MM-DD&to=YYYY-MM-DD

Organic Installs:
  /{app-id}/organic_installs_report/v5?from=YYYY-MM-DD&to=YYYY-MM-DD
```

可选参数（按需追加）：
- `&from_install_time=YYYY-MM-DD&to_install_time=YYYY-MM-DD`：限制 install 日期范围
- `&attribution_lookback=7d`：更改归因回溯窗口

### 2. 执行下载（必须用 curl.exe）

下载到临时文件 `<名称>_raw.csv`：

```powershell
curl.exe -L --noproxy "*" --max-time 300 `
  -H "Authorization: Bearer $token" `
  -o "${outFile}_raw.csv" `
  -w "HTTP: %{http_code} | 大小: %{size_download} bytes | 耗时: %{time_total}s" `
  $url
```

> ⚠️ **必须使用 `curl.exe`**，不能用 PowerShell 的 `Invoke-WebRequest`
> ⚠️ **必须加 `--noproxy "*"`**，本机代理（127.0.0.1:7897）会导致 SSL 握手失败
> ⚠️ **必须加 `-L`**，AF 返回 302 重定向，真实数据在 `rawdata.appsflyer.com`

### 3. 裁剪字段（下载后必须立即执行，不可跳过）

```powershell
$scriptPath = "C:\Users\ZYB\AppData\Roaming\npm\node_modules\openclaw\skills\af-pull-api\scripts\filter_fields.py"
python $scriptPath "${outFile}_raw.csv" "$outFile"
Remove-Item "${outFile}_raw.csv"  # 删除原始全字段文件
```

裁剪后的文件即为最终交付文件，原始 `_raw.csv` 删除。

### 4. 输出文件命名规范

```
<AppAbbr>_<report_type>_<from>_<to>[_ios|_android].csv
例：CP_non_organic_installs_2026-03-24_ios.csv
    EQ_in_app_events_2026-03-22_2026-03-24_android.csv
```

## 参数变更场景

| 用户说 | 变更 |
|--------|------|
| 拉 installs 数据 | 切换 endpoint 为 `installs_report/v5` 和 `organic_installs_report/v5` |
| 限制 install 日期为 X~Y | 追加 `&from_install_time=X&to_install_time=Y` |
| 归因窗口改为 7 天 | 追加 `&attribution_lookback=7d` |
| 只拉 organic / 只拉 non-organic | 只调用对应的一个 endpoint |
| 更改日期范围 | 修改 `from` / `to` 参数 |

## App 名称识别

用户通常会用**简称（abbr）**、**slug** 或 **全名**来指定 App，如「EQ」「RealSpeak」「questionai」。

解析步骤：
1. 读取 `references/app_mapping.json`
2. 按以下顺序模糊匹配（不区分大小写）：`abbr` → `slug` → `full_name`
3. 确认匹配后，根据目标平台取对应的 `af_app_id`：
   - 默认优先 iOS（`af_app_id.ios`）
   - 用户明确说 Android 时取 `af_app_id.android`
   - 双平台 App 未指定时，分别拉两份（文件名加 `_ios` / `_android` 后缀）

映射文件字段说明：
- `abbr`：内部简称，如 `EQ`、`EL4`
- `slug`：英文短名，如 `questionai`、`realspeak`
- `full_name`：完整名称，如 `Question.AI`、`RealSpeak`
- `af_app_id.ios`：iOS AF App ID（格式 `id + 数字`）
- `af_app_id.android`：Android AF App ID（格式为包名）

> 若匹配到多个结果，列出候选让用户确认后再执行。

## 详细 API 参考

完整参数说明见：`references/api_reference.md`
App 映射表见：`references/app_mapping.json`
