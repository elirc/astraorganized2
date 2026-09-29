# ww5 independent final recheck

## Decision

REJECTED pending a small follow-up repair and regenerated delivery evidence.

## Findings

1. **Direct service authorization is incomplete (blocking).** `src/services/compensationService.ts:36-89` validates input, tenant employee, and approver identity, but never checks the caller against the `COMP_CHANGE_CREATE` role matrix. The API route applies that permission, but a caller of the exported service can pass an `EMPLOYEE` session and create a compensation draft plus approval and audit record. The plan explicitly calls for actual role enforcement on direct service list/write calls. Add the service-side check (preferably the shared permission assertion) and a regression test for an employee attempting draft creation. `listCompensationChanges` does have a role check, although it returns a bad-request error rather than the matrix's forbidden error.

2. **Planned course scope is still incomplete.** The staged `astraupskill` package has the required nine guide files and exact-original snapshots, but the measured total is 2,812 words. The plan requests approximately 4,000 words, and the prior follow-up review explicitly required expansion with source-grounded walkthroughs, matched fixtures/exercises, and links. This is not reflected as completed in the current manifest (`courseWords: 2812`). Expand the guides and rerun `prepare_delivery.py` so the manifest is regenerated from the final terminal records.

3. **Regression coverage remains narrower than the source plan.** The final record proves 7/7 tests pass, but `src/tests/state-transition.test.ts` covers only four state tests: one late submit, one happy approval/duplicate decision, invalid input, and submit rollback. It does not exercise the planned missing-link, invalid-decision, draft-decision, foreign-owner/tenant snapshot-preservation, approval late-audit rollback, or competing decision cases. Add meaningful tests for the highest-risk rejected paths and approval rollback/concurrency guard, or document a deliberate narrower scope in the plan.

## Verified evidence

- `ww5-tests-final-03.json` and log: `npm.cmd test -- --run`, 4 files / 7 tests passed, exit 0.
- `ww5-typecheck-final-07.json`: `npx.cmd tsc --noEmit`, exit 0.
- `ww5-build-final-03.json`: `npm.cmd run build`, exit 0.
- `withApiHandler.ts:29,62` uses the Next 15 `params: Promise<TParams>` contract and awaits it.
- `submitCompensationChange` wraps status, notification, and audit writes in `withStoreTransaction`; the existing rollback test confirms status and queue restoration after audit failure.
- Repository updates whitelist lifecycle timestamp fields and use expected-state guards; approval decisions validate tenant, link, submitted status, assigned approver, and pending state.
- No project-authored ambient fake dependency typings were found; `.gitignore` excludes runtime/dependency artifacts.

The rejection is based on source semantics and staged evidence only. No source, canonical copy, originals, or progress files were modified.
