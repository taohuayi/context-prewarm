# GPTQuotaPrewarm — repository naming and releases

The public project is branded **GPTQuotaPrewarm**; the desired GitHub repository name is `gpt-quota-prewarm` and the Agent Skill ID is `gpt-quota-prewarm`.

## Rename the GitHub repository

The repository owner must open the existing repository's **Settings → General → Repository name**, change `context-prewarm` to `gpt-quota-prewarm`, and save. The connected integration that authored the source cannot access GitHub's repository settings endpoint.

GitHub normally redirects old repository URLs to the new location. Verify CI badges and external links after rename; do not delete/recreate the existing repository or discard git history.

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
