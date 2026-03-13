import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Any, Tuple


AF_ID_RE = re.compile(r"^\d+-\d+$")
MUST_USD_EVENTS = {"af_pay_new"}


def is_blank(value: Any) -> bool:
    return value is None or str(value).strip() == ""


def load_csv(path: Path) -> Tuple[List[Dict[str, str]], List[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        header = reader.fieldnames or []
        return rows, header


def add_issue(issues: Dict[str, List[int]], key: str, row_num: int) -> None:
    issues[key].append(row_num)


def check_rows(rows: List[Dict[str, str]]) -> Dict[str, Any]:
    issues: Dict[str, List[int]] = defaultdict(list)

    for idx, r in enumerate(rows, start=2):
        # Install Time empty
        if is_blank(r.get("Install Time")):
            add_issue(issues, "install_time_empty", idx)

        # Event Revenue Currency must be USD for must-USD events
        event_name = (r.get("Event Name") or "").strip()
        if event_name in MUST_USD_EVENTS:
            cur = (r.get("Event Revenue Currency") or "").strip().upper()
            if cur != "USD":
                add_issue(issues, "must_usd_currency", idx)

        # Event Revenue > 100 when currency is USD
        cur = (r.get("Event Revenue Currency") or "").strip().upper()
        if cur == "USD":
            val = (r.get("Event Revenue") or "").strip()
            if val:
                try:
                    if float(val) > 100:
                        add_issue(issues, "event_revenue_gt_100_usd", idx)
                except ValueError:
                    add_issue(issues, "event_revenue_parse_error", idx)

        # Media Source restricted
        if (r.get("Media Source") or "").strip().lower() == "restricted":
            add_issue(issues, "media_source_restricted", idx)

        # IP empty
        if is_blank(r.get("IP")):
            add_issue(issues, "ip_empty", idx)

        # AppsFlyer ID format
        afid = (r.get("AppsFlyer ID") or "").strip()
        if not afid:
            add_issue(issues, "af_id_empty", idx)
        elif not AF_ID_RE.match(afid):
            add_issue(issues, "af_id_bad_format", idx)

        # Advertising ID required for Android
        platform = (r.get("Platform") or "").strip().lower()
        adv_id = (r.get("Advertising ID") or "").strip()
        if platform == "android" and not adv_id:
            add_issue(issues, "android_advertising_id_empty", idx)

        # IDFV should not be empty for iOS
        idfv = (r.get("IDFV") or "").strip()
        if platform == "ios" and not idfv:
            add_issue(issues, "ios_idfv_empty", idx)

    # Metric: no IDFA but has IDFV and IP
    no_idfa_has_idfv_ip = 0
    no_idfa_total = 0
    for r in rows:
        idfa = (r.get("IDFA") or "").strip()
        idfv = (r.get("IDFV") or "").strip()
        ip = (r.get("IP") or "").strip()
        if not idfa:
            no_idfa_total += 1
            if idfv and ip:
                no_idfa_has_idfv_ip += 1

    return {
        "issues": issues,
        "metrics": {
            "no_idfa_has_idfv_ip": no_idfa_has_idfv_ip,
            "no_idfa_total": no_idfa_total,
        },
    }


def summarize(rows: List[Dict[str, str]], result: Dict[str, Any], max_examples: int) -> str:
    issues: Dict[str, List[int]] = result["issues"]

    lines: List[str] = []
    lines.append("问题汇总")

    def add_issue_summary(key: str, title: str) -> None:
        row_nums = issues.get(key, [])
        if not row_nums:
            return
        examples = ", ".join(str(n) for n in row_nums[:max_examples])
        more = "" if len(row_nums) <= max_examples else f"（另有 {len(row_nums) - max_examples} 行）"
        lines.append(f"- {title}：{len(row_nums)} 行，示例行号：{examples}{more}")

    add_issue_summary("install_time_empty", "Install Time 为空")
    add_issue_summary("must_usd_currency", "必须为 USD 的事件币种不为 USD")
    add_issue_summary("event_revenue_gt_100_usd", "USD 事件金额超过 100")
    add_issue_summary("event_revenue_parse_error", "Event Revenue 数值解析失败")
    add_issue_summary("media_source_restricted", "Media Source 为 restricted")
    add_issue_summary("ip_empty", "IP 为空")
    add_issue_summary("af_id_empty", "AppsFlyer ID 为空")
    add_issue_summary("af_id_bad_format", "AppsFlyer ID 格式不合规")
    add_issue_summary("android_advertising_id_empty", "Android 端 Advertising ID 为空")
    add_issue_summary("ios_idfv_empty", "iOS 端 IDFV 为空")

    # Metrics
    metric = result["metrics"]["no_idfa_has_idfv_ip"]
    lines.append("")
    lines.append("指标")
    lines.append(f"- 未上报 IDFA 但上报了 IDFV 且上报了 IP 的用户数：{metric}")

    return "\n".join(lines)


def parse_filename(csv_path: Path) -> Dict[str, str]:
    name = csv_path.name
    if name.lower().endswith(".csv"):
        name = name[:-4]
    parts = name.split("_")
    if len(parts) < 5:
        return {"app_id": "unknown", "report_group": "unknown", "start_date": "", "end_date": "", "timezone": ""}
    app_id = parts[0]
    report_group = parts[1]
    start_date = parts[2]
    end_date = parts[3]
    timezone = "_".join(parts[4:])
    return {
        "app_id": app_id,
        "report_group": report_group,
        "start_date": start_date,
        "end_date": end_date,
        "timezone": timezone,
    }


def find_examples(rows: List[Dict[str, str]]) -> Dict[str, Tuple[int, Dict[str, str]]]:
    examples: Dict[str, Tuple[int, Dict[str, str]]] = {}

    for idx, r in enumerate(rows, start=2):
        if "install_time_empty" not in examples and is_blank(r.get("Install Time")):
            examples["install_time_empty"] = (idx, r)
        if "must_usd_currency" not in examples:
            event_name = (r.get("Event Name") or "").strip()
            if event_name in MUST_USD_EVENTS:
                cur = (r.get("Event Revenue Currency") or "").strip().upper()
                if cur != "USD":
                    examples["must_usd_currency"] = (idx, r)
        if "event_revenue_gt_100_usd" not in examples:
            cur = (r.get("Event Revenue Currency") or "").strip().upper()
            if cur == "USD":
                val = (r.get("Event Revenue") or "").strip()
                if val:
                    try:
                        if float(val) > 100:
                            examples["event_revenue_gt_100_usd"] = (idx, r)
                    except ValueError:
                        pass
        if "event_revenue_parse_error" not in examples:
            cur = (r.get("Event Revenue Currency") or "").strip().upper()
            if cur == "USD":
                val = (r.get("Event Revenue") or "").strip()
                if val:
                    try:
                        float(val)
                    except ValueError:
                        examples["event_revenue_parse_error"] = (idx, r)
        if "media_source_restricted" not in examples and (r.get("Media Source") or "").strip().lower() == "restricted":
            examples["media_source_restricted"] = (idx, r)
        if "ip_empty" not in examples and is_blank(r.get("IP")):
            examples["ip_empty"] = (idx, r)
        afid = (r.get("AppsFlyer ID") or "").strip()
        if "af_id_empty" not in examples and not afid:
            examples["af_id_empty"] = (idx, r)
        if "af_id_bad_format" not in examples and afid and not AF_ID_RE.match(afid):
            examples["af_id_bad_format"] = (idx, r)
        platform = (r.get("Platform") or "").strip().lower()
        adv_id = (r.get("Advertising ID") or "").strip()
        if "android_advertising_id_empty" not in examples and platform == "android" and not adv_id:
            examples["android_advertising_id_empty"] = (idx, r)
        idfv = (r.get("IDFV") or "").strip()
        if "ios_idfv_empty" not in examples and platform == "ios" and not idfv:
            examples["ios_idfv_empty"] = (idx, r)

    return examples


def render_report(csv_path: Path, rows: List[Dict[str, str]], header: List[str], result: Dict[str, Any]) -> str:
    meta = parse_filename(csv_path)
    report_group = meta["report_group"]
    organic_label = "非organic" if "in-app-events" in report_group else "organic"
    issues = result["issues"]
    examples = find_examples(rows)

    def ratio(n: int, d: int) -> str:
        if d == 0:
            return "0/0（0.00%）"
        pct = n / d * 100
        return f"{n}/{d}（{pct:.2f}%）"

    lines: List[str] = []
    lines.append(f"# {meta['app_id']} - {meta['start_date']}_{meta['end_date']} - {organic_label}事件校验报告")
    lines.append("")
    lines.append("**数据范围**")
    lines.append(f"- 文件：`{csv_path.as_posix()}`")
    lines.append(f"- 行数：{len(rows)}")
    lines.append("")
    lines.append("**问题概览（仅列出发现的问题）**")

    total = len(rows)
    def add_issue_line(key: str, label: str) -> None:
        cnt = len(issues.get(key, []))
        if cnt == 0:
            return
        pct = (cnt / total * 100) if total else 0
        lines.append(f"- {label}：{cnt}/{total}（{pct:.2f}%）")

    add_issue_line("install_time_empty", "Install Time 为空")
    add_issue_line("must_usd_currency", "必须为 USD 的事件币种不为 USD")
    add_issue_line("event_revenue_gt_100_usd", "USD 事件金额超过 100")
    add_issue_line("event_revenue_parse_error", "Event Revenue 数值解析失败")
    add_issue_line("media_source_restricted", "Media Source 为 restricted")
    add_issue_line("ip_empty", "IP 为空")
    add_issue_line("af_id_empty", "AppsFlyer ID 为空")
    add_issue_line("af_id_bad_format", "AppsFlyer ID 格式不合规")
    add_issue_line("android_advertising_id_empty", "Android 端 Advertising ID 为空")
    add_issue_line("ios_idfv_empty", "iOS 端 IDFV 为空")

    lines.append("")
    lines.append("**比例指标**")
    no_idfa = result["metrics"]["no_idfa_total"]
    no_idfa_has_idfv_ip = result["metrics"]["no_idfa_has_idfv_ip"]
    lines.append(f"- 未上报 IDFA 但上报了 IDFV 且上报了 IP 的数据占“未上报 IDFA”数据的比例：{ratio(no_idfa_has_idfv_ip, no_idfa)}")

    lines.append("")
    lines.append("**问题示例（每类 1 条，包含完整行数据）**")

    def add_example(key: str, label: str, cols: str) -> None:
        if key not in examples:
            return
        row_num, row = examples[key]
        lines.append(f"- {label}（问题列：{cols}）")
        lines.append(f"- 行号：{row_num}")
        lines.append("```tsv")
        lines.append("\t".join(header))
        lines.append("\t".join(row.get(h, "") for h in header))
        lines.append("```")
        lines.append("")

    add_example("install_time_empty", "Install Time 为空", "`Install Time`")
    add_example("must_usd_currency", "必须为 USD 的事件币种不为 USD", "`Event Revenue Currency`")
    add_example("event_revenue_gt_100_usd", "USD 事件金额超过 100", "`Event Revenue` + `Event Revenue Currency`")
    add_example("event_revenue_parse_error", "Event Revenue 数值解析失败", "`Event Revenue`")
    add_example("media_source_restricted", "Media Source 为 restricted", "`Media Source`")
    add_example("ip_empty", "IP 为空", "`IP`")
    add_example("af_id_empty", "AppsFlyer ID 为空", "`AppsFlyer ID`")
    add_example("af_id_bad_format", "AppsFlyer ID 格式不合规", "`AppsFlyer ID`")
    add_example("android_advertising_id_empty", "Android 端 Advertising ID 为空", "`Advertising ID`")
    add_example("ios_idfv_empty", "iOS 端 IDFV 为空", "`IDFV`")

    lines.append("**说明**")
    lines.append("- 本报告仅列出检测到的问题类型与示例，不包含解决方案。")
    lines.append("- 如需排查/解决方案，请以 `references/af_event_checks.md` 中的说明为准。")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="AF 事件文件校验")
    parser.add_argument("csv", type=str, help="CSV 文件路径")
    parser.add_argument("--max-examples", type=int, default=10, help="每类问题最多展示的示例行号")
    parser.add_argument("--json", action="store_true", help="输出 JSON 结果")
    parser.add_argument("--write-report", action="store_true", help="写入报告到输出目录")
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(Path(__file__).resolve().parents[1] / "outputs" / "v1"),
        help="报告输出目录（默认：skill/outputs/v1）",
    )
    args = parser.parse_args()

    path = Path(args.csv)
    rows, header = load_csv(path)
    result = check_rows(rows)

    if args.json:
        # Convert defaultdict to normal dict with list
        issues = {k: v for k, v in result["issues"].items() if v}
        payload = {
            "total_rows": len(rows),
            "issues": issues,
            "metrics": result["metrics"],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(summarize(rows, result, args.max_examples))

    if args.write_report:
        report = render_report(path, rows, header, result)
        out_dir = Path(args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        meta = parse_filename(path)
        report_group = meta["report_group"]
        organic_label = "非organic" if "in-app-events" in report_group else "organic"
        out_name = f"{meta['app_id']} - {meta['start_date']}_{meta['end_date']} - {organic_label}事件校验报告.md"
        out_path = out_dir / out_name
        out_path.write_text(report, encoding="utf-8")
        print(f"报告已写入：{out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
