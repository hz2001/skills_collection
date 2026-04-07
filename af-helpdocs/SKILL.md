---
name: af-helpdocs
description: 查询、检索 AppsFlyer 官方帮助文档（support.appsflyer.com）。当用户询问 AppsFlyer 的功能说明、配置方法、归因概念、SDK 集成、In-App Events、Raw Data API、SKAN、Deep Linking、Audiences、隐私保护、广告网络配置（Meta/Google/TikTok 等）、Data Locker 等帮助中心内容时使用。也用于更新/重新爬取 AF 文档入库。
---

# AppsFlyer Help Center 文档查询 Skill

## 文档位置

已入库文档路径：`memory/knowledge-base/af-helpdocs/`

- **INDEX.md**：所有 sections 的索引，先读这个定位目标文件
- 每个 section 一个 `.md` 文件，文件名为 section 名称的 slug
- 共 90 个 sections，731 篇文章，约 6.8 MB

## 查询流程

1. **先读 INDEX.md**，根据用户问题找到最相关的 section 文件名
2. **用 `read` 工具加载对应 `.md` 文件**，搜索具体内容
3. **引用原文链接**：每篇文章都有 `> 链接: <url>` 标注，回答时附上

> 💡 文件较大（部分超过 200KB），用 `read` + `offset`/`limit` 分段读取，避免一次全量加载。

## 常用文件快速索引

| 主题 | 文件名 |
|------|--------|
| In-App Events | `in-app-events.md` |
| Attribution 概念 | `attribution-concepts.md` |
| Raw Data API | `raw-data-reportingapis.md` |
| SDK 集成规划 | `sdk-integration-planning.md` |
| SKAN / iOS 隐私 | `skan-solution.md`, `ios-platform.md` |
| Meta 广告集成 | `meta-ads.md` |
| Google Ads | `google-ads.md` |
| TikTok | `tiktok-for-business.md` |
| Deep Linking | `deep-linking-using-onelink.md` |
| Audiences | `audiences.md` |
| 归因场景 | `attribution-scenarios.md` |
| 数据保护/隐私 | `preserve-user-privacy.md` |
| Data Locker | `data-locker.md` |
| Protect Traffic (防作弊) | `protect-your-traffic.md` |
| 中国市场 | `china-market.md`, `china-domestic-market-ad-network-configuration.md` |
| 广告网络配置 A-F | `ad-network-configuration-guides-a-f.md` |
| 广告网络配置 G-Q | `ad-network-configuration-guides-g-q.md` |
| 广告网络配置 R-Z | `ad-network-configuration-guides-r-z.md` |

## 更新文档

当文档需要重新爬取时，运行：

```powershell
python scripts/fetch_helpdocs.py
```

可选参数：
- `--dry-run`：只列出 sections，不写文件
- `--filter SDK API`：只爬包含关键词的 sections

> ⚠️ 网络说明：脚本使用 `curl.exe --noproxy`，AF Help Center 无需代理可直连。不要给 Python 设置系统代理环境变量（`HTTPS_PROXY` 等），否则会导致 SSL 错误。
