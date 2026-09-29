# e2 final independent review — 2026-09-13

Decision: REJECTED / not applied. The source remains unchanged after the earlier review. `src/lib/cms/store.ts:198` still uses `rawValues[field.name] ?? field.defaultValue ?? null`, conflating explicit null with omission and defaults. `tests/cms-boundaries.test.ts` only tests `coerceFieldValue("not-json", "json")`; it does not exercise create/update or verify unchanged entry version, revisions, and audit log after invalid JSON or explicit null. Add mutation-boundary regressions and fix semantics before refreezing.
