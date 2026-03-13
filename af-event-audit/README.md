# AF Event Audit 使用说明

## 适用场景

- 需要校验 AppsFlyer in-app-events CSV 是否存在数据问题
- 需要生成“只包含问题与示例”的校验报告
- 需要按照既定规则输出比例指标与示例行

## 使用步骤

1. 阅读规则
   - 打开 `references/af_event_checks.md`，确认当前规则与术语
2. 运行脚本
   - 基本校验输出：
     ```bash
     python scripts/af_event_eval.py <csv-path>
     ```
   - 生成报告（默认输出到 `outputs/v1/`）：
     ```bash
     python scripts/af_event_eval.py <csv-path> --write-report
     ```
   - 指定输出目录：
     ```bash
     python scripts/af_event_eval.py <csv-path> --write-report --output-dir outputs/v2
     ```
3. 查看报告
   - 报告命名格式：`app - 日期 - organic/非organic 事件校验报告.md`
   - 报告仅包含：问题类型、比例指标、每类 1 条完整行示例（含行号与问题列）

## 输出版本管理

- 每次规则或逻辑变更，创建新的 `outputs/vN/` 目录
- 同步更新 `SKILL.md` 的 “Output Versions” 记录
- 默认输出目录在脚本参数 `--output-dir` 中体现

## Skill 迭代逻辑

- 规则更新：先更新 `references/af_event_checks.md`
- 逻辑更新：同步更新 `scripts/af_event_eval.py`
- 输出更新：创建新的 `outputs/vN/` 目录并写入报告样例
- 文档更新：同步更新 `SKILL.md` 的 Output Versions 与 README 说明

## 回答排查/解决方案的要求

- 用户询问排查或解决方案时，必须依据 `references/af_event_checks.md`
- 不得脱离该文件自行推断或扩展结论
