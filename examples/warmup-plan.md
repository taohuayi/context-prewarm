# Example: a productive prewarm pilot (fictional public repository)

**Context:** A contributor will review pull requests for a public package over the next week. Their assistant plan has unused quota before reset. No secret files will be opened.

**Goal:** Reduce repeated orientation effort while preparing a reusable, independently valuable architecture-and-tests map.

## Evaluate before running

| Dimension | Assessment |
| --- | --- |
| Expected reuse | 3+ PR reviews this week (hypothesis) |
| Stability | CONTRIBUTING, architecture guide, test runner, package manifests (relatively stable) |
| Deliverable | `docs/PROJECT_CONTEXT.md` with source paths and confidence labels |
| Risk | Low for a public repo; still exclude tokens, fixtures containing secrets, and private comments |
| Bound | One repository, the main docs and 3 critical entry points; at most 20 file reads |

## Execution prompt

> Use `gpt-quota-prewarm` to prepare for repeated PR reviews in this public repository. Read the README, architecture docs, contribution guide, package manifests, test configuration and up to three central modules. Do not modify source code or run deployments. Produce `docs/PROJECT_CONTEXT.md` with a module map, test entry points, important invariants, evidence paths, stale/unknown areas and a succinct handoff. Do not read credentials or secrets. End with a report explaining how to continue in the same session and how to compare cached usage to a cold-start PR review.

## Success criteria

- Future PR reviews can reference an accurate map with paths and evidence.
- At least one subsequent real task reuses the same session if appropriate.
- Cache metrics are recorded if available; otherwise savings remain **unverified**.
- The warm-up never becomes an excuse to read unrelated materials.

## Stop early when

- the user has urgent tasks needing their quota;
- the scoped sources are stale or unrelated to the planned future task;
- the agent encounters sensitive content or a permission boundary;
- no useful deliverable can be produced within the budget.
