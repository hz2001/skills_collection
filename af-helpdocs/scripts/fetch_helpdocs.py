"""
AppsFlyer Help Center 文档爬取脚本
目标: support.appsflyer.com (Zendesk Help Center API)
输出: memory/knowledge-base/af-helpdocs/ 下每个 section 一个 Markdown 文件

用法:
  python fetch_helpdocs.py                    # 爬取全部
  python fetch_helpdocs.py --filter SDK API   # 只爬包含关键词的 sections
  python fetch_helpdocs.py --dry-run          # 只显示 section 列表，不写文件

网络说明:
  使用 curl.exe --noproxy 直连（绕过系统代理），AF Help Center 无需代理可直达。
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from html.parser import HTMLParser

# ─── 配置 ────────────────────────────────────────────────────────────────────
BASE_API   = "https://support.appsflyer.com/api/v2/help_center/en-us"
OUTPUT_DIR = r"C:\Users\ZYB\.openclaw\workspace\memory\knowledge-base\af-helpdocs"
UA         = "Mozilla/5.0 (compatible; XiaoMo/1.0)"
DELAY_SEC  = 0.4   # 礼貌延迟，避免触发限速
PER_PAGE   = 100   # Zendesk 最大值


# ─── curl.exe 请求 ────────────────────────────────────────────────────────────
def curl_get(url: str) -> dict:
    """用 curl.exe --noproxy 直连，返回解析后的 JSON dict"""
    result = subprocess.run(
        ["curl.exe", "-s", "--noproxy", "*", "--max-time", "30",
         "-H", f"User-Agent: {UA}", url],
        capture_output=True, text=True, encoding="utf-8"
    )
    if result.returncode != 0:
        raise RuntimeError(f"curl failed: {result.stderr}")
    return json.loads(result.stdout)


def paginate(endpoint: str) -> list:
    """分页拉取所有数据"""
    results = []
    page = 1
    while True:
        sep = "&" if "?" in endpoint else "?"
        url = f"{BASE_API}/{endpoint}{sep}per_page={PER_PAGE}&page={page}"
        try:
            data = curl_get(url)
        except Exception as e:
            print(f"  [WARN] 请求失败: {url} → {e}", file=sys.stderr)
            break
        items = next((v for v in data.values() if isinstance(v, list)), None)
        if not items:
            break
        results.extend(items)
        if data.get("next_page"):
            page += 1
            time.sleep(DELAY_SEC)
        else:
            break
    return results


# ─── HTML → Markdown ──────────────────────────────────────────────────────────
class HtmlToMarkdown(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []
        self._skip_tags = {"script", "style", "noscript"}
        self._skip = 0
        self._list_stack = []
        self._list_counters = []
        self._in_pre = False
        self._pending_href = ""
        self._td_buf_start = 0
        self._td_buf = []
        self._tr_rows = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag in self._skip_tags:
            self._skip += 1; return
        if self._skip: return

        if tag == "pre":
            self._in_pre = True; self.result.append("\n```\n")
        elif tag == "code" and not self._in_pre:
            self.result.append("`")
        elif tag in ("h1","h2","h3","h4","h5","h6"):
            self.result.append("\n" + "#" * int(tag[1]) + " ")
        elif tag == "p":
            self.result.append("\n\n")
        elif tag == "br":
            self.result.append("  \n")
        elif tag in ("strong","b"):
            self.result.append("**")
        elif tag in ("em","i"):
            self.result.append("*")
        elif tag == "ul":
            self._list_stack.append("ul"); self._list_counters.append(0)
        elif tag == "ol":
            self._list_stack.append("ol"); self._list_counters.append(0)
        elif tag == "li":
            if self._list_stack:
                indent = "  " * (len(self._list_stack) - 1)
                if self._list_stack[-1] == "ol":
                    self._list_counters[-1] += 1
                    self.result.append(f"\n{indent}{self._list_counters[-1]}. ")
                else:
                    self.result.append(f"\n{indent}- ")
        elif tag == "a":
            self._pending_href = attrs_dict.get("href", "")
            self.result.append("[")
        elif tag == "img":
            alt = attrs_dict.get("alt", "image")
            src = attrs_dict.get("src", "")
            self.result.append(f"![{alt}]({src})")
        elif tag == "hr":
            self.result.append("\n\n---\n\n")
        elif tag == "blockquote":
            self.result.append("\n> ")
        elif tag == "table":
            self._tr_rows = []
        elif tag == "tr":
            self._td_buf = []
        elif tag in ("td","th"):
            self._td_buf_start = len(self.result)

    def handle_endtag(self, tag):
        if tag in self._skip_tags:
            self._skip = max(0, self._skip - 1); return
        if self._skip: return

        if tag == "pre":
            self._in_pre = False; self.result.append("\n```\n")
        elif tag == "code" and not self._in_pre:
            self.result.append("`")
        elif tag in ("h1","h2","h3","h4","h5","h6"):
            self.result.append("\n")
        elif tag in ("strong","b"):
            self.result.append("**")
        elif tag in ("em","i"):
            self.result.append("*")
        elif tag in ("ul","ol"):
            if self._list_stack:
                self._list_stack.pop(); self._list_counters.pop()
            self.result.append("\n")
        elif tag == "a":
            self.result.append(f"]({self._pending_href})")
            self._pending_href = ""
        elif tag in ("td","th"):
            cell = "".join(self.result[self._td_buf_start:]).strip().replace("\n"," ")
            del self.result[self._td_buf_start:]
            self._td_buf.append(cell)
        elif tag == "tr":
            self._tr_rows.append(list(self._td_buf))
            self._td_buf = []
        elif tag == "table":
            if self._tr_rows:
                header = self._tr_rows[0]; n = len(header)
                self.result.append("\n\n")
                self.result.append("| " + " | ".join(header) + " |\n")
                self.result.append("| " + " | ".join(["---"]*n) + " |\n")
                for row in self._tr_rows[1:]:
                    r = (row + [""]*n)[:n]
                    self.result.append("| " + " | ".join(r) + " |\n")
                self.result.append("\n")

    def handle_data(self, data):
        if not self._skip:
            self.result.append(data)

    def get_markdown(self):
        text = "".join(self.result)
        text = re.sub(r'\n{4,}', '\n\n\n', text)
        text = re.sub(r'[ \t]+\n', '\n', text)
        return text.strip()


def html_to_md(html: str) -> str:
    if not html:
        return ""
    p = HtmlToMarkdown()
    p.feed(html)
    return p.get_markdown()


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[\s_]+", "-", text.strip())
    return text[:60]


# ─── 主逻辑 ───────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="Fetch AF Help Center docs")
    ap.add_argument("--filter", nargs="*", default=[], metavar="KW",
                    help="只爬包含关键词的 sections（空=全部）")
    ap.add_argument("--dry-run", action="store_true",
                    help="只列出 sections，不写文件")
    args = ap.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    print("Step 1: 拉取分类和 sections...")
    categories = paginate("categories.json")
    cat_map = {c["id"]: c["name"] for c in categories}
    sections = paginate("sections.json")
    print(f"  分类: {len(categories)}, Sections: {len(sections)}")

    if args.filter:
        kws = [k.lower() for k in args.filter]
        sections = [s for s in sections if any(kw in s["name"].lower() for kw in kws)]
        print(f"  关键词过滤后: {len(sections)} sections")

    if args.dry_run:
        print("\n[Dry-run] Section 列表:")
        for s in sections:
            cat = cat_map.get(s.get("category_id"), "?")
            print(f"  [{cat}] {s['name']}")
        return

    print("\nStep 2: 拉取所有文章...")
    articles = paginate("articles.json")
    print(f"  文章总数: {len(articles)}")

    sec_articles: dict = {}
    for art in articles:
        sec_articles.setdefault(art.get("section_id"), []).append(art)

    print("\nStep 3: 写入 Markdown 文件...")
    index_lines = [
        "---",
        f"source: https://support.appsflyer.com/hc/en-us",
        f"updated_at: {now_str}",
        "---",
        "",
        "# AppsFlyer Help Center 文档索引",
        "",
        f"> 抓取时间：{now_str}  |  文章总数：{len(articles)}  |  Sections：{len(sections)}",
        "",
        "## 目录",
        "",
    ]

    written = 0
    for sec in sections:
        sid = sec["id"]
        sec_name = sec["name"]
        cat_name = cat_map.get(sec.get("category_id"), "Unknown")
        arts = sec_articles.get(sid, [])
        if not arts:
            continue

        filename = f"{slugify(sec_name)}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)

        lines = [
            "---",
            f"section: {sec_name}",
            f"category: {cat_name}",
            f"section_url: {sec.get('html_url','')}",
            f"updated_at: {now_str}",
            f"article_count: {len(arts)}",
            "---",
            "",
            f"# {sec_name}",
            f"> 分类: {cat_name} | 文章数: {len(arts)}",
            "",
        ]

        for art in sorted(arts, key=lambda x: x.get("position", 999)):
            title = art.get("title", "")
            url   = art.get("html_url", "")
            body  = art.get("body") or ""
            upd   = (art.get("updated_at") or "")[:10]
            md    = html_to_md(body) if body else "_（暂无内容）_"

            lines += [
                f"## {title}",
                f"> 链接: {url} | 更新: {upd}",
                "",
                md,
                "",
                "---",
                "",
            ]

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        size_kb = os.path.getsize(filepath) // 1024
        print(f"  [OK] {filename}  ({len(arts)} 篇, {size_kb}KB)")
        written += 1

        index_lines.append(f"- **[{sec_name}]({filename})** `{cat_name}` — {len(arts)} 篇")
        time.sleep(DELAY_SEC)

    # 写索引
    index_path = os.path.join(OUTPUT_DIR, "INDEX.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(index_lines))

    print(f"\n完成! 写入 {written} 个 sections → {OUTPUT_DIR}")
    print(f"索引: {index_path}")


if __name__ == "__main__":
    main()
