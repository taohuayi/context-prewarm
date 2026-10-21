# Contributing

Contributions should increase **real-world usefulness and measurability**, not token consumption.

Good contributions: reproducible (redacted) cache experiments, cross-client behavior observations, improved risk boundaries, tests, clearer installation instructions, and case studies with measurable deliverables.

For measurement issues or PRs, state the client, model, date, thread strategy, task, inputs/cached tokens when exposed, how the comparison workload was controlled, and what was not measured. Never publish prompts, user documents, personal identifiers, API keys, private repositories, or billing/account screenshots with sensitive information.

Before opening a PR, run:

```bash
python -m unittest discover -s tests -v
python tools/validate_skill.py
```

Keep the skill's instructions short and portable. Avoid vendor-specific assumptions outside the technical reference.