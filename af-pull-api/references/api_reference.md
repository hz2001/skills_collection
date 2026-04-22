# AppsFlyer Pull API 完整参考

## Base URL
```
https://hq1.appsflyer.com/api/raw-data/export/app/
```

## Endpoints

### Non-Organic
| 报告类型 | Path |
|---------|------|
| In-App Events | `/{app-id}/in_app_events_report/v5` |
| Installs | `/{app-id}/installs_report/v5` |
| Uninstalls | `/{app-id}/uninstall_events_report/v5` |
| Reinstalls | `/{app-id}/reinstalls/v5` |

### Organic
| 报告类型 | Path |
|---------|------|
| In-App Events | `/{app-id}/organic_in_app_events_report/v5` |
| Installs | `/{app-id}/organic_installs_report/v5` |
| Uninstalls | `/{app-id}/organic_uninstall_events_report/v5` |
| Reinstalls | `/{app-id}/reinstalls_organic/v5` |

### Retargeting
| 报告类型 | Path |
|---------|------|
| Conversions | `/{app-id}/installs-retarget/v5` |
| In-App Events | `/{app-id}/in-app-events-retarget/v5` |

### Ad Revenue
| 报告类型 | Path |
|---------|------|
| Attributed | `/{app-id}/ad_revenue_raw/v5` |
| Organic | `/{app-id}/ad_revenue_organic_raw/v5` |
| Retargeting | `/{app-id}/ad-revenue-raw-retarget/v5` |

---

## Query Parameters

> 📌 参数来源：官方 OpenAPI Spec（[GitHub](https://github.com/AppsFlyerKnowledge/devhub-bidir-sync/blob/v0.1/reference/raw-data-pull-api-v2-token.json)），最后验证：2026-04-21

| 参数名 | 类型 | 必填 | 适用报告 | 说明 |
|-------|------|------|---------|------|
| `from` | string | ✅ | 全部 | 事件日期开始（`YYYY-MM-DD` 或 `YYYY-MM-DD HH:MM:SS`） |
| `to` | string | ✅ | 全部 | 事件日期结束 |
| `event_name` | array | ❌ | in-app events | **按事件名过滤**，多个用逗号分隔。例：`event_name=af_purchase,ftd` |
| `from_install_time` | string | ❌ | 全部 | 按 install 日期过滤-开始 |
| `to_install_time` | string | ❌ | 全部 | 按 install 日期过滤-结束 |
| `media_source` | string | ❌ | non-organic | 按媒体来源过滤（单值）。需与 `category` 配合使用 |
| `category` | string | ❌ | non-organic | 配合 `media_source`。Facebook 需同时设置两个参数 |
| `timezone` | string | ❌ | 全部 | 默认 UTC。支持 IANA 时区格式，如 `Asia/Shanghai` |
| `geo` | string | ❌ | 全部 | 按国家代码过滤（单值，每次 API 调用只能设一个） |
| `currency` | string | ❌ | 全部 | `preferred`=App 设置货币，`USD`=美元 |
| `agency` | array | ❌ | non-organic | 按代理商过滤，多个逗号分隔 |
| `maximum_rows` | integer | ❌ | 全部 | 返回最大行数限制（默认上限 200,000） |
| `additional_fields` | array | ❌ | 全部 | 额外字段，见 AF Raw Data Field Dictionary |

### event_name 用法示例

```bash
# 只拉 af_purchase 和 af_subscribe 事件
curl -L --proxy "socks5://127.0.0.1:7897" \
  -H "Authorization: Bearer $TOKEN" \
  "https://hq1.appsflyer.com/api/raw-data/export/app/{app-id}/organic_in_app_events_report/v5?from=2026-04-21&to=2026-04-21&event_name=af_purchase,af_subscribe"
```

> ⚠️ 注意：`event_name` 参数**支持服务端过滤**，无需下载全量数据后再本地筛选。建议在数据量大时使用，可大幅减少下载时间和文件大小。

---

## 鉴权

### V2 Token（推荐，账号级别）
- 获取位置：AF 控制台 → 右上角头像 → Security Center → API Token
- 一个 token 覆盖账号下所有 App
- 格式：JWT 三段式（长度约 200+ 字符）
- 使用方式：**HTTP Header**
  ```
  Authorization: Bearer <V2_TOKEN>
  ```

### V1 Token（旧版，per-app）
- 每个 App 单独获取，不可跨 App
- 使用方式：URL 参数 `?api_token=<V1_TOKEN>`

---

## 已知问题 & 注意事项

| 问题 | 原因 | 解决方法 |
|------|------|---------|
| `{"error": "Missing authorization header"}` | V2 Token 放 URL 参数 | 改用 Header |
| `schannel: failed to receive handshake` | 本机代理（127.0.0.1:7897）干扰 SSL | `curl.exe --noproxy "*"` |
| PowerShell Invoke-WebRequest 超时/卡死 | 数据量大，需等全量下载完才返回 | 改用 `curl.exe -o <file>` 直接写文件 |
| 302 重定向，数据在临时 URL | AF 服务器设计 | `curl.exe -L` 跟随重定向 |

---

## App ID 格式

| 平台 | 格式 | 示例 |
|------|------|------|
| iOS | `id` + Apple Store ID | `id6757069032` |
| Android | 包名 | `com.example.app` |

---

## 全字段列表（Pull API 固定返回，共 81 个）

```
Attributed Touch Type, Attributed Touch Time, Install Time, Event Time,
Event Name, Event Value, Event Revenue, Event Revenue Currency,
Event Revenue USD, Event Source, Is Receipt Validated, Partner,
Media Source, Channel, Keywords, Campaign, Campaign ID, Adset, Adset ID,
Ad, Ad ID, Ad Type, Site ID, Sub Site ID, Sub Param 1~5,
Cost Model, Cost Value, Cost Currency,
Contributor 1/2/3 Partner/Media Source/Campaign/Touch Type/Touch Time,
Region, Country Code, State, City, Postal Code, DMA, IP, WIFI,
Operator, Carrier, Language, AppsFlyer ID, Advertising ID, IDFA,
Android ID, Customer User ID, IMEI, IDFV, Platform, Device Type,
OS Version, App Version, SDK Version, App ID, App Name, Bundle ID,
Is Retargeting, Retargeting Conversion Type, Attribution Lookback,
Reengagement Window, Is Primary Attribution,
User Agent, HTTP Referrer, Original URL
```

> Pull API 不支持在请求中指定返回字段子集，字段由服务端固定返回。
> 下载后用 `scripts/filter_fields.py` 裁剪。
