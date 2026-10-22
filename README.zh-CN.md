# GPTQuotaPrewarm｜Codex / GPT 闲置额度预热

[![CI](https://github.com/taohuayi/GPTQuotaPrewarm/actions/workflows/ci.yml/badge.svg)](https://github.com/taohuayi/GPTQuotaPrewarm/actions/workflows/ci.yml) [![Release](https://img.shields.io/github/v/release/taohuayi/GPTQuotaPrewarm)](https://github.com/taohuayi/GPTQuotaPrewarm/releases/tag/v0.2.0)

[正式版本 v0.2.0](https://github.com/taohuayi/GPTQuotaPrewarm/releases/tag/v0.2.0) · [更新记录](CHANGELOG.md)

**把即将闲置的 AI 使用额度，转化成未来可复用的上下文和实际工作成果。**

[English](README.md) · [安装 Skill](skills/gpt-quota-prewarm/SKILL.md) · [示例方案](examples/warmup-plan.md)

> 这是独立开发、重点适配 Codex 的实验性开源 Agent Skill，并非 OpenAI 官方产品，也不承诺订阅额度一定减少。

## 最初的问题

> 现在没有特别重要的任务，但当前 Codex 额度快要重置了。我能否提前让 Astra 阅读我未来肯定需要的项目材料，在保留旧会话和可复用提示词前缀的前提下，减少未来真正做事时的重复输入成本？

**答案：有条件地可以。** 我们把这个策略叫作「闲置额度上下文预热」（Idle-capacity GPTQuotaPrewarming）。重要的是同时生产两份资产：

1. **上下文缓存资产（不保证）**：未来同一模型、同一线程、匹配的前缀可能命中缓存，从而降低重复输入成本。
2. **持久成果资产（更可靠）**：项目地图、架构分析、证据索引、检查清单、决策记录等保存到文件中；即使缓存未命中仍有价值。

该策略**不是**把今天没用完的 Token 存到未来，不等于永久记忆，也不支持跨模型共享底层计算缓存。永远不要为了凑 Token 而读取垃圾内容。

## 什么时候值得用？

| 场景 | 判断 | 理由 |
| --- | --- | --- |
| 明天要继续维护同一个仓库，今天额度富余 | 优先试验 | 文档稳定、复用概率高 |
| 未来几天会反复复审同一批 PR | 适合 | 可先读结构和验证规则，留下可审查产物 |
| 不知道未来要做什么，只想耗额度 | 不建议 | 无稳定复用目标，可能徒增消耗 |
| 材料每天剧烈变化或高度敏感 | 通常不建议 | 容易失效，有泄漏风险 |
| 需要在 Astra 和 Luna 间切换 | 不保证跨模型缓存 | 可以传递报告，但不能直接共享模型 KV 缓存 |

## 安装

将 `skills/gpt-quota-prewarm/` 复制到 Codex 项目里的 `.agents/skills/gpt-quota-prewarm/`；其他 Agent 使用其支持的 Agent Skills 目录。这个 Skill 只有说明文件，不要求 API Key，也不提供自动调度功能。

```bash
mkdir -p .agents/skills
cp -R /path/to/gpt-quota-prewarm/skills/gpt-quota-prewarm .agents/skills/
```

## 如何触发

第一次先让 Agent 评估，不要马上大规模读取：

> 请使用 gpt-quota-prewarm。今天额度有富余，明天我要继续处理当前 GitHub 仓库的代码审查。请评估最值得提前理解的稳定内容、预计复用频率、信息敏感性、实际工作产物和成本；提出一个有边界的小实验。执行之前先给我看方案。

批准后：

> 按方案只读检查稳定文档和关键代码，生成可追溯的项目地图与证据索引；不要改生产代码、不要读取机密文件。结束后告诉我下一次如何在原会话继续、如何验证缓存命中和真正的额度收益。

## 真实价值怎么验证？

**不要把 API 的缓存输入价格折扣直接套用到 Plus / Pro 的五小时或每周额度。** 真实节省须以客户端公开的用量字段或可比任务测试验证。比较以下指标：

- 今天预热消耗了多少额度、有没有产出有用文档；
- 后续任务是否沿用原有会话和模型，稳定前缀是否保留；
- 如果能取得 `cached_tokens`，缓存命中占比是多少；
- 与同类冷启动任务相比，未来消耗和结果质量有无改善。

已有的官方材料说明缓存和具体产品的计费可能不同。关于 Codex / Work 长期缓存的消息参见 [OpenAI 28 Days Day 16](https://community.openai.com/t/28-days-of-shipping-at-openai/1403897)；一般缓存机制见 [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)。

## 项目内容

- [`SKILL.md`](skills/gpt-quota-prewarm/SKILL.md)：Agent 实际执行的完整步骤和边界。
- [`references/MODEL.md`](skills/gpt-quota-prewarm/references/MODEL.md)：收益模型、缓存假设和失败条件。
- [`assets/WARMUP_REPORT_TEMPLATE.md`](skills/gpt-quota-prewarm/assets/WARMUP_REPORT_TEMPLATE.md)：每次预热必须交付的清单。
- [`tools/prewarm.py`](tools/prewarm.py)：无第三方依赖的候选任务排序和粗略经济性测算。
- [`examples/`](examples)：候选数据及完整示例。
- [`tests/`](tests)：工具测试。

## 三条底线

1. **先有未来任务，才有预热。** 不让缓存优化取代真正有价值的生产。
2. **隐私优先。** 绝不把个人资料、私有仓库内容、凭证等发布到公开仓库。
3. **可证伪。** 缓存未命中、未来任务改变、产物价值不够时，应直接停止或更改策略。

开源许可证：MIT。欢迎提交去敏感化的实测数据、改进方案和跨客户端实验。