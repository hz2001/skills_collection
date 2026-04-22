"""
filter_fields.py
裁剪 AF Pull API 下载的 CSV，只保留指定字段。
用法：python filter_fields.py <input.csv> <output.csv> [--fields "字段1,字段2,..."]
不传 --fields 时使用默认字段列表。
"""

import csv
import sys
import argparse

DEFAULT_FIELDS = [
    "Install Time",
    "Event Time",
    "Event Name",
    "Event Value",
    "Event Revenue",
    "Event Revenue Currency",
    "Event Revenue USD",
    "Event Source",
    "Media Source",
    "Channel",
    "Keywords",
    "Campaign",
    "Campaign ID",
    "Adset",
    "Adset ID",
    "Ad",
    "Ad ID",
    "Country Code",
    "State",
    "City",
    "Postal Code",
    "DMA",
    "IP",
    "AppsFlyer ID",
    "Advertising ID",
    "IDFA",
    "Android ID",
    "Customer User ID",
    "IMEI",
    "IDFV",
    "Platform",
    "OS Version",
    "App Version",
    "SDK Version",
    "App ID",
    "App Name",
    "Is Retargeting",
    "User Agent",
    "HTTP Referrer",
    "Original URL",
]


def filter_csv(input_path: str, output_path: str, fields: list[str]) -> None:
    with open(input_path, newline="", encoding="utf-8-sig") as fin:
        reader = csv.DictReader(fin)
        available = reader.fieldnames or []

        # 找出实际存在的字段，保持顺序
        keep = [f for f in fields if f in available]
        missing = [f for f in fields if f not in available]

        if missing:
            print(f"[WARN] Fields not found in source, skipped: {missing}")
        print(f"[OK] Keeping {len(keep)} fields")

        with open(output_path, "w", newline="", encoding="utf-8-sig") as fout:
            writer = csv.DictWriter(fout, fieldnames=keep, extrasaction="ignore")
            writer.writeheader()
            rows = 0
            for row in reader:
                writer.writerow({k: row[k] for k in keep})
                rows += 1

    print(f"[OK] Done! {rows} rows written to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="裁剪 AF CSV 字段")
    parser.add_argument("input", help="输入 CSV 文件路径")
    parser.add_argument("output", help="输出 CSV 文件路径")
    parser.add_argument(
        "--fields",
        help="自定义保留字段（逗号分隔），不传则使用默认字段列表",
        default=None,
    )
    args = parser.parse_args()

    fields = (
        [f.strip() for f in args.fields.split(",")]
        if args.fields
        else DEFAULT_FIELDS
    )

    filter_csv(args.input, args.output, fields)


if __name__ == "__main__":
    main()
