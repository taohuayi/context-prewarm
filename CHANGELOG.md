# GPTQuotaPrewarm v0.2.0 — Codex-first rebrand

**GPTQuotaPrewarm** is the new name for Context Prewarm. This release preserves the original idea: use spare Codex usage capacity to prepare future work, prioritizing independently useful artifacts and measuring cache benefits instead of assuming them.

## Changes

- Renamed the Agent Skill from `context-prewarm` to `gpt-quota-prewarm` (breaking installation path change).
- Updated the English and Chinese README, CLI help text, examples, validator and report template.
- Clarified the Codex-oriented use case and kept the project's explicit non-affiliation with OpenAI.
- Kept old `v0.1.0` release notes below for historical accuracy.
- GitHub repository renamed from `context-prewarm` to **`taohuayi/GPTQuotaPrewarm`**. Canonical URL: https://github.com/taohuayi/GPTQuotaPrewarm. GitHub's redirect normally preserves old repository URLs.

### Upgrade from v0.1.0

Remove the old `.agents/skills/context-prewarm` directory if installed and install `skills/gpt-quota-prewarm` as `.agents/skills/gpt-quota-prewarm`. Avoid loading both skill names simultaneously.

---

# Context Prewarm v0.1.0 — First public release

**Context Prewarm** is an experimental, open-source Agent Skill for turning otherwise-idle AI assistant capacity into useful preparation for likely future work, including *conditionally* reusable model context and durable, inspectable project artifacts.

## What's included

- Portable Agent Skill: `skills/context-prewarm/SKILL.md`
- Practical 5-step protocol: select, rank, bound, prepare, verify
- Lightweight Python candidate-scoring tool and *illustrative* cache cost estimator
- Example candidate table, sample prewarm plan and report template
- Technical model of prefix matching, cache uncertainty and quota-accounting limits
- English and Simplified Chinese documentation; MIT license and contribution/security notes
- Automated skill validation and unit tests through GitHub Actions

## Quick start

See [README.md](README.md) and [README.zh-CN.md](README.zh-CN.md). To install in a Codex project, copy `skills/context-prewarm` to your agent's project-local `.agents/skills/` directory.

```bash
python tools/prewarm.py rank examples/candidates.csv
python tools/prewarm.py estimate --prefix-tokens 40000 --future-reuses 3 --hit-probability 0.8 --cached-read-ratio 0.1 --write-ratio 1.0
python -m unittest discover -s tests -v
```

## Important limitations

- Not an official OpenAI project, subscription entitlement, automatic scheduler or quota bypass.
- Model cache is not persistent memory; future cache reuse is contingent on client and matching-input behavior.
- The estimator uses **hypothetical relative input units**, not measured subscription credits.
- Avoid unnecessary token use. Producing durable value is the first priority.
- Never prewarm credentials or publish private prompts, source code or proprietary project context.

We welcome redacted, reproducible benchmarks and user feedback.
