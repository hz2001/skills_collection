---
name: af-event-audit
description: Audit AppsFlyer in-app-events CSV files using local validation rules. Use when asked to check an AF event report for data issues, explain why events are missing, or generate an issue-only audit report based on this skill's references/af_event_checks.md and scripts/af_event_eval.py.
---

# AF Event Audit

## Overview

Use this skill to read the local AF event validation rules and run the audit script against a target CSV, then report only the issues found (no \"not found\" items).

## Workflow

1. Read `references/af_event_checks.md` to align with the latest validation rules and terminology.
2. Run `scripts/af_event_eval.py <csv-path>` to generate the audit summary.
3. Create a report file named `(app - 日期 - organic/非organic 事件校验报告.md)` and include:
   - 问题类型列表（只写发现的问题）
   - Checklist（包含核对项与对号；若核对无问题则标记通过）
   - 关键比例指标（例如：有 IDFV 与 IP 且无 IDFA 的数量 / 无 IDFA 的总量）
   - 每类问题 1 条完整行示例，标注行号与具体问题列
4. Do not include solutions in the report.
5. If the user asks for排查/解决方案, read `references/af_event_checks.md` and answer based on it (do not re-analyze or invent).
6. Output management:
   - Store reports under `outputs/vN/` (e.g., `outputs/v1/`).
   - When the skill logic or rules change, create a new `outputs/vN/` folder for that version.
   - Update this SKILL.md to record the current output version and what changed.

## Usage

See `README.md`.

## Notes

- The audit script already implements required checks (Install Time, AF_id format, IP, currency rules, platform IDs, etc.).
- If the user updates rules in `references/af_event_checks.md`, sync the script before running audits.

## Temp Files

- **Never create temporary scripts or files outside this skill folder.**
- If analysis requires writing a temporary script (e.g., the CSV is not local and needs pre-processing), write it to `scripts/temp/` within this skill folder.
- Clean up files in `scripts/temp/` after the task is complete.

## Output Versions

- v1: Initial version using `references/af_event_checks.md` and `scripts/af_event_eval.py` with the current rule set.
