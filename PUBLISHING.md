# GPTQuotaPrewarm — repository naming and releases

The public project is **[taohuayi/GPTQuotaPrewarm](https://github.com/taohuayi/GPTQuotaPrewarm)**. Its GitHub repository name is `GPTQuotaPrewarm`; the installable Agent Skill ID remains `gpt-quota-prewarm`.

## Repository rename status

The repository was renamed from `context-prewarm` to `GPTQuotaPrewarm` on GitHub. Use the canonical URL `https://github.com/taohuayi/GPTQuotaPrewarm` for new references.

GitHub normally redirects old repository URLs to the new location. Preserve the repository and its Git history, tags, and releases; avoid deleting and recreating it.

## About details

Description: `A Codex-focused Agent Skill that turns unused GPT quota into future-ready context and durable work.`

Suggested topics: `codex`, `agent-skills`, `prompt-caching`, `context-engineering`, `quota-optimization`, `ai-agents`.

## Publishing checklist

1. Check `skills/gpt-quota-prewarm/SKILL.md` and run `python tools/validate_skill.py`.
2. Run `python -m unittest discover -s tests -v`.
3. Confirm `main` CI succeeds.
4. Create a version tag/release on the validated commit, with release notes from `CHANGELOG.md`.
5. Check links, license, visibility, and that no personal/private project files are published.

This is an **independent community project**, not an OpenAI official product. Prompt-cache hits and subscription usage savings are not guaranteed.
