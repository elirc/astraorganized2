# Nethris delivered

Canonical ID `71e7b036865c`; original folder `C:/Users/Owner/Desktop/_Organized Desktop/01 Net Workspaces/.nethris`.

The finite manifest was applied and all 180 canonical file hashes were verified. The project has nine current learning guides, 6,577 words and 48 checked local course links, plus two inspected screenshots. All 75 original text files were preserved exactly; 46 historical course pages were labeled. Do not rerun staging, original preservation, model extension, CSS formatting, finalization or manifest preparation over this delivered family.

## Verified results

- **61 distinct checks:** 13 EF/domain foundation tests, 28 real HTTP scenario groups, 17 real-browser workflows and three packaging checks. Repeated runs are not added to the count.
- `foundation-final` passed 13/13 against the final backend source.
- `http-04` passed all 28 groups and cleaned its private database. It uses real Kestrel, JWT validation, EF and SQLite, including concurrent writes and a late receipt failure that must roll back domain/audit writes.
- `browser-03` passed all 17 workflows, including CRUD, account role changes, self password reset, PTO editing and two-stage approval, exact recovery after a committed response is lost, and a delayed directory response released after sign-out.
- `frontend-07` is the final client build. `package-browser-03/wwwroot` matches it byte-for-byte. The API assembly matches the Release assembly from the successful package build. No private database was included in the verification package.
- `package-01` completed locked restores, clean npm installation and publish. The later compatible transitive update (`frontend-patches-01`) changed nine packages. `npm-tree-01` passed; `npm-audit-02` and `nuget-audit-01` reported no known advisories. Final patched versions: baseline-browser-mapping 2.11.22, browserslist 4.28.9, nanoid 3.3.19, postcss 8.5.28.
- `images-reviewed.json` records the SHA-256 values of the reviewed desktop and narrow images from browser-03.

## Implemented scope

Single-organization .NET 10 / React HRIS with identified fresh SQLite databases, generated private signing material, current-account/session checks, Admin-only account administration, full employee/department/job-role CRUD, versioned edits, relationship protection, manager-cycle and lead-department rules, paginated reads and private balance/salary projections.

PTO validates quarter hours, bounded dates, overlap and pending reservations. It supports pending edit/delete/cancel, captures an eligible manager, requires the current assigned manager first and a different HR/Admin final reviewer, and commits approval history and balance deduction atomically. CRUD mutations also commit audit and 24-hour receipts in the same transaction. Strong ETags reject stale edits. React preserves drafts, recovers exact uncertain operations, and invalidates old reads/cached data when sessions change.

## Important historical failures

The original baseline reproduced numeric roles, failing DateTimeOffset sorting, HR-to-Admin escalation, a one-day 9,999-hour request and failed approval insertion. The original balance stayed unchanged when approval failed; never claim that a negative balance was observed.

During implementation, expiry predicates needed captured UTC values for SQLite translation. An HTTP runner cleanup bug was corrected with contextlib.closing. Nested textarea labels made exact label lookup unstable after reopening a PTO draft; explicit separate labels fixed the workflow. A later client-state review added generation invalidation so delayed reads cannot restore a signed-out session; browser-03 verifies it.

## Cleanup limitation and package provenance

All owned test servers are stopped. One synthetic SQLite file from the failed http-03 cleanup remains at `C:/Users/Owner/AppData/Local/Temp/nethris-check-iwwute5q/test.sqlite`. Automatic approval review rejected both recursive cleanup and deletion limited to that file, stating only `blocked by policy`. It also rejected removal of an older generated browser bundle in the staged artifacts folder. Do not retry those deletions or work around the rejection.

Existing generated files were left untouched, and fresh verification packages were created under this checks directory. Use `package-browser-03` for the final verified package; the older staged `artifacts` browser bundle is historical. The canonical project receives source and scripts, not generated packages. A fresh canonical build uses the final source and lockfile. See `cleanup-limitation.json` and the manifest's limits.

The collection remains active: **39 of 239 eligible families delivered; 200 remain**. Original top-50 and previously modified family exclusions remain in force. Next queued family is `4de416cd300b` (`astra2`, Tidebound). Only its package metadata/README and existing scope evidence have been read in this turn; it has not been staged or modified. No AGENTS.md was found in its project scan. Do not confuse that read-only preview with a completed review.
