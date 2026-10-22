# GPTQuotaPrewarm — Codex Quota Prewarming & Prompt Cache Workflow

[![CI](https://github.com/taohuayi/context-prewarm/actions/workflows/ci.yml/badge.svg)](https://github.com/taohuayi/context-prewarm/actions/workflows/ci.yml) [![Release](https://img.shields.io/github/v/release/taohuayi/context-prewarm)](https://github.com/taohuayi/context-prewarm/releases/tag/v0.2.0)

[Latest release: v0.2.0](https://github.com/taohuayi/context-prewarm/releases/tag/v0.2.0) · [Changelog](CHANGELOG.md)

**Turn unused Codex quota into reusable GPT context and durable work.**

[简体中文](README.zh-CN.md) · [Skill](skills/gpt-quota-prewarm/SKILL.md) · [Example plan](examples/warmup-plan.md)

> **Status:** experimental Codex-focused Agent Skill, built independently. Not affiliated with OpenAI and not a guarantee of lower subscription usage.

## The idea

If an AI coding assistant's usage window is about to reset and useful capacity remains, you can spend that capacity on **likely future work**: reading stable documentation, mapping a project's architecture, identifying constraints, and producing reviewable artifacts. Later, continuing the **same model/thread with a preserved prompt prefix** may reuse cached input rather than processing the same context from scratch.

This creates *two independent assets*:

1. **Reusable context**, conditional on actual prompt-cache hits and product behavior.
2. **Durable artifacts** (architecture notes, evidence indexes, tests, decision records) that remain useful even if cache reuse fails.

**This does not bank unused subscription messages, store model intelligence permanently, or move a cache between different models.** Avoid work whose only purpose is increasing token count.

```text
Idle capacity today
      |
      v
Select stable, likely-to-be-reused, useful material
      |
      v
Read & understand --> produce an evidence-backed artifact
      |                            |
      v                            v
Keep reusable thread             Save files to repository
      |                            |
      +--------------+-------------+
                     v
          Continue real work later
                     |
            Measure actual value
```

## What the skill does

`gpt-quota-prewarm` is a portable [Agent Skill](https://agentskills.io/specification) that guides an agent to:

- decide **whether** prewarming makes sense (including a *do nothing* option);
- rank candidate future-work contexts by reuse, stability, deliverable value, cost, and sensitivity;
- prepare a **bounded, evidence-based** context-loading plan;
- perform read-only reconnaissance and create a useful handoff artifact when authorized;
- preserve thread continuity when practical, then **verify actual cache usage**, not assume it;
- stop before leaking secrets, burning the last reserve, or disturbing urgent work.

It is intentionally **instruction-first**, not a background scheduler, cache API, subscription-limit bypass, or secret collector.

## Quick start

Install the skill where your agent discovers project skills. For Codex, a common project-local location is `.agents/skills/`:

```bash
mkdir -p .agents/skills
cp -R /path/to/gpt-quota-prewarm/skills/gpt-quota-prewarm .agents/skills/
```

Or copy into your user-level agent skills directory if supported. Then ask your agent:

> Use `gpt-quota-prewarm`. I have some usage left before reset. Assess whether preparing my current project for tomorrow's PR review is worthwhile. Propose a small pilot first; do not perform an expensive warm-up without approval.

For an approved execution:

> Use `gpt-quota-prewarm` on this repository. Read the stable architecture and contribution docs, create an evidence-backed `docs/PROJECT_CONTEXT.md`, avoid secrets and production changes, and finish with a cache measurement plan.

### Optional no-dependency planning tools

```bash
python tools/prewarm.py rank examples/candidates.csv
python tools/prewarm.py estimate --prefix-tokens 40000 --future-reuses 3 --hit-probability 0.8 --cached-read-ratio 0.1 --write-ratio 1.0
python -m unittest discover -s tests -v
```

The estimator reports **relative input-processing units, not Codex subscription credits**. API write rates and subscription accounting differ. For subscription accounts, evaluate the future usable quota saved and artifact quality empirically.

## A five-step protocol

1. **Identify a future hinge.** A real project, recurring code review, onboarding task, exam preparation, or upcoming milestone—not an imagined reason to spend quota.
2. **Rank candidates.** Prefer stable documents likely to be used several times; reject sensitive or rapidly changing material.
3. **Set a bound.** Limit files, time, tool calls, and context; reserve capacity for any urgent work. Ask approval before execution.
4. **Prewarm productively.** Read only relevant sources, build an accurate evidence index, and save a portable work product. Retain the thread to improve chances of matching the prefix later.
5. **Verify and adapt.** Check cache tokens/hit rates and realized usage *if exposed by your client*, and assess artifact usefulness. If metrics are unavailable, label savings **unverified**.

See the [worked example](examples/warmup-plan.md) and the [technical assumptions](skills/gpt-quota-prewarm/references/MODEL.md).

## Important limitations

- A cache is **not** permanent project memory; a transcript or a local file is a distinct durable artifact.
- **Prefix matching matters.** Rewriting instructions, changing tools, trimming/compacting history, forking a thread, or changing model may invalidate reuse. Some systems support careful mid-thread reasoning-effort updates, but not every client implements them equivalently.
- OpenAI announced long-lived cached context for signed-in Codex / Work users in October 2026; this is **not** an unlimited guarantee for all clients, models, input changes, or future product versions.
- API cache-write charges are **not** the same as subscription-account costs. Depending on reuse, prewarming can increase *total* token use while reducing **later-window** consumption.
- Never upload private repository content, proprietary documents, API keys, credentials, or sensitive prompts into a public project. Always respect repository permissions and organizational policy.

## Measuring value

For a simplified single stable prefix, define:

- `L`: reusable input tokens; `N`: expected future uses; `p`: actual cache-hit probability;
- `r`: cached-input price divided by uncached-input price;
- `w`: initial write/processing cost in uncached-input units (depends on product);
- `O`: extra warm-up reasoning/output/tool overhead expressed in the same units.

Then an *illustrative* lifetime input-cost balance is:

`net = N × p × L × (1 − r) − L × w − O`

Later-window gross input savings are `N × p × L × (1 − r)`. **Neither formula predicts fixed Codex subscription credits.** If today's usage would otherwise expire, current- vs future-window value matters separately; additionally, a real artifact has independent value. Always use measured, comparable workloads.

## Sources and scope

- [OpenAI prompt caching guide](https://developers.openai.com/api/docs/guides/prompt-caching) — prefix matching, retention, cache usage fields, and API rates.
- [OpenAI reasoning models guide](https://developers.openai.com/api/docs/guides/reasoning) — configuration updates on supported models.
- [OpenAI developer community shipping log, Day 16](https://community.openai.com/t/28-days-of-shipping-at-openai/1403897) — Codex / Work long-lived cache announcement.
- [Agent Skills specification](https://agentskills.io/specification) — portable `SKILL.md` format.

This repository is independent, not affiliated with or endorsed by OpenAI. Product behavior and rates may change.

## Contributing

Experiments are welcome. Please share **redacted** benchmarks with `model`, `client`, `date`, `input tokens`, `cached tokens`, and comparable outcomes, without publishing prompts or confidential project material. See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md).

MIT licensed. See [LICENSE](LICENSE).