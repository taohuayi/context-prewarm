# Model, hypotheses, and decision rules

## Separate four layers

1. **User-visible transcript:** readable prior conversation, potentially truncated or compacted.
2. **Durable external work product:** files, PR comments, architecture notes or tests; transportable between models.
3. **Prompt cache:** implementation-specific reusable processing of a matching input prefix; may reduce later input cost.
4. **Plan limits / quota:** product-specific usage accounting; not equivalent to raw API token billing.

Do not confuse any two. A long-lived cache announcement does **not** make it a durable knowledge base. The strongest guarantee is the separately saved artifact.

## Reuse preconditions

- Relevant work resumes in a compatible environment and model.
- The cached prefix remains sufficiently unchanged; append-only conversational continuity often helps.
- Cache is eligible and retained under current service policies, and the server actually reports/achieves a hit.
- Future request actually needs the same material; stale or irrelevant context can make processing more expensive overall.

Changing tools, tool definitions, system instructions, model, request-level reasoning settings, summaries, or context compaction may affect eligibility. On supported GPT-6 API flows, use documented `configuration_update` for effort changes if the client offers it. Do not assume subscription UIs implement that feature.

## Two objectives; do not collapse them

**Future-window capacity:** if current quota expires, an approved warm-up today may help use fewer input-processing units when returning in a later window (if cache hits). It does not increase any hard subscription cap.

**Lifetime efficiency:** prep costs something now, even when current capacity is plentiful. Include warm-up input/write costs, reasoning/output/tool overhead, and the risk of never returning.

## Illustrative model

Let `L` be reusable prefix tokens, `N` expected future reuses, `p` probability of a hit, `r` cache-read / normal-input rate, `w` initial processing or cache-write / normal-input rate, `O` non-input overhead converted to normal-input units.

- Future gross reduction: `N * p * L * (1 - r)`.
- Lifetime difference against no warm-up: `N * p * L * (1 - r) - L * w - O`.
- The tool expresses **relative units**, not actual subscription credits or guaranteed monetary savings.
- A real artifact's usefulness (`V`) is separate and often more important than token savings.

For example `L=40,000`, `N=3`, `p=0.8`, `r=0.1`, `w=1`, `O=2,000`: future-window savings estimate is `86,400` equivalent uncached-input units; lifetime net is `44,400` under these *hypothetical* assumptions. Those numbers are not real Codex credit measurements.

### Break-even intuition

For zero overhead, expected reuses must exceed `w / [p * (1-r)]` for a positive theoretical lifetime input-cost balance. With `w=1`, `p=0.8`, `r=0.1`, this is `1.39`, so **two** future reuses are needed. More overhead or lower hit rate increases the threshold. This ignores deliverable value.

## Evidence levels

- **Observed:** provider/client exposes `cached_tokens` and comparable usage for a matched workload.
- **Supported inference:** current documentation says a behavior is possible, but the client's implementation was not verified.
- **Hypothesis:** the future task will reuse the prefix, or future quotas will be spared.

Label numbers accordingly. A claimed quota benefit without observable usage data stays a hypothesis.

## Official references (checked October 2026)

- https://developers.openai.com/api/docs/guides/prompt-caching
- https://developers.openai.com/api/docs/guides/reasoning
- https://community.openai.com/t/28-days-of-shipping-at-openai/1403897
- https://agentskills.io/specification
