# Desktop inventory and comparison

Start here:

- [PROJECT_INDEX.md](PROJECT_INDEX.md) — the independent overview of 388 projects and resource collections.
- [COMPARISON_REPORT.md](COMPARISON_REPORT.md) — differences from AstraOrganized.
- [project-catalog-summary.json](project-catalog-summary.json) — compact data for filtering.
- [project-catalog.json](project-catalog.json) — full records, evidence, components, caveats, and IDs.

The independent inventory was completed before AstraOrganized was opened. Its original hashes are saved in independent-baseline.json and were verified after comparison. The original index is preserved in independent-snapshot; only navigation anchors were corrected in the displayed copy. Existing projects and the AstraOrganized folder were not modified.

Supporting JSON files preserve discovery, exclusions, validation, differences, and resumable state. Scripts document the analysis. No project was installed, built, tested, or run.

Source reference: [updateCase service](../src/services/caseService.ts) and [runtime regression](../tests/runtime-case-clearable-fields.test.mjs).
