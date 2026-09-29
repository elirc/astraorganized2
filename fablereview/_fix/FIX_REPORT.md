# Fix report: applying the review to all 153 projects

Fable, 2026-09-18. Follows [PLAN.md](PLAN.md) and [FIX_BRIEF.md](FIX_BRIEF.md). One report per project is in [reports/](reports/) (153 files); the batch progress log is in [progress/](progress/).

## What was done

Every project that the review marked IMPROVE or REWORK, and every KEEP project with backlog items, received its "Improvements needed" list plus the cross-cutting P1-P4 items. Work was split by wave:

- **Wave 1 (75 template-generated JS courses).** One generator sweep (`wave1_sweep.py`: per-stack environment paragraphs, de-minified tests, README toolchain block, diff notes, clone banners) plus `sync_examples.py` (real "Executable examples" blocks in every 03 chapter, read from each project's own tests), then a per-project script under `scripts/` for the 54 non-clones (code fixes with new tests, project-specific exercises, review paragraphs, boundary traces, variations). The 21 clones got the sweep and banner only, as planned.
- **Wave 2 (78 bespoke courses).** 33 fixed by Opus agents in batches B09-B15 while agents were allowed; the remaining 45 fixed by Fable directly (per-project scripts under `scripts/`, plus `b15_docs.py`, `b16.py`, `b17.py`, `b18.py`). Off-stack reference projects (Java, Python) got a translation chapter, a glossary and the P1 items, per the brief; their code was left as delivered and the reports say so.
- **Phase 3.** Gate re-check with `verify.py`, a bulk pass (`phase3_bulk.py`) that filled empty 06/07 code-block gates from each project's own 03 examples and converted variations paragraphs to lists, then four Opus agents that hand-authored the remaining code blocks (56 projects, every block cited to a real file) and prerequisites-plus-glossary sections (32 projects, every term tied to a real symbol). Fable reviewed each agent's report and fixed two follow-ups (browser-only wording, list spacing).

Code changes were verified by running the project's own tests (and typecheck/build/lint where defined) after the change, using temporarily junctioned dependency trees or short-lived installs that were removed afterwards. No report was written before its test run passed; where a test could not be run, the report's Skipped section says so.

## Gates before and after

`verify.py` checks every project's course for the structural problems the review found. Counts are projects failing the gate (153 checked).

| gate | before | after | note |
|---|---:|---:|---|
| report written | 153 | 0 | one fix report per project |
| leaked names / wrong-stack claims (wave 1) | 68 | 1 | the remaining hit is `calendar-jobtrack` naming its own product, Questboard |
| agent-process language | 6 | 0 | |
| UTF-8 BOM in course files | 9 | 0 | |
| chapter set / titles | 1 | 0 | verifier now ignores the new `03b` break-it chapters when matching chapter 03 |
| code blocks in 03/04/06/07 | 145 | 0 | |
| glossary or prerequisites section (wave 2) | 77 | 0 | |
| variations section concrete (wave 1) | 75 | 0 | |
| identical review paragraphs (wave 1) | 75 | 21 | remaining are clones and near-clones sharing one generated paragraph |
| trace-lab boundaries generic (wave 1) | 25 | 9 | remaining are clones |
| shared paragraph share over 40% (wave 1) | 75 | 62 | median 73% before, 58.7% after; the generator's shared scaffolding is still the majority of a wave-1 course |

The last three rows are the honest limit of this pass: the wave-1 courses are less duplicated than before but still share most of their prose, because the generator's structure was kept and only the project-specific sections were rewritten. Making them fully bespoke is a rewrite, not a fix.

## Code changes worth knowing about

Every change is listed in the project's report; these are the ones that change behavior a learner will see.

- **Real defects fixed with tests:** subscription-billing whole-cent parsing; secure-notes session expiry; live-chat (JS1) oversize frame handling; newcodexJS 05 `isPublic` coercion, 11 datetime offsets, 12 message-id guard, 14 trigger cleanup, 16 bulk cap after dedupe; recipeview id canonicalization; bookmark-manager per-column ILIKE with escaped wildcards; org-explorer lock timeout to 503; pulse-analytics vocabulary-first parsing and refresh 409; kanban no-op drop guard; stock-catalog price floor; master4 per-SKU reservation aggregation and UUID ids (the delivered write loop double-created rows); master3 P2034 retry wrapper around every serializable transaction; master-6 narrowed P2002 catch; ww37 service validation derived from the Zod schemas; ww27 lifecycle vocabulary from one enum; job-track live chat `mark_read` range read moved inside the transaction (documented as the course's seventh defect); buildsmallplates boolean returns wired into the UI and a single-pass `updateSet`; andie error detail retained but redacted.
- **New runnable material:** buildCRMPYJS contacts CRUD module with 7 tests (the "house behind the gate"); astra4.2 `service/` HTTP+SQLite starter with a competing-PUT test; buildsql App.tsx split into `src/views/`; jstrain2.3 TypeScript starter; buildbusinesses Ticket 1 implemented end to end; grokbuildmultitenant direct middleware test; integration tests against a disposable PostgreSQL for master2, master3 (both executed and passing here) and ww17 (written, skip-gated, not executed: no migrated schema).
- **nethris:** the 194-line golfed dispatcher is now four readable files with identical behavior, verified by the 28 xUnit tests and the 28-check Python black-box suite before and after. The literal MapGroup conversion the review asked for was not done; the chapter already contrasts the two.

## Findings from the fix pass itself

- **Shopify token (P0).** The three literals in `astra-remaining-improvements/backups/cf8875344b43/scripts/populate-metaobjects.js` were replaced with a redaction marker, and andie's VERIFICATION now names that location for the follow-up owner. **The token still needs to be revoked in the Shopify admin**; a file edit does not do that, and other copies may exist.
- **e13** archived tests are excluded from Vitest (agent X11).
- Three projects (aiheartbeat, grokbuildppmproject, andie backups aside) were found already fixed on disk with no progress line; they were verified and reported rather than re-done.
- `fe.report` expects lists; 45 reports written with strings were rendered one character per bullet and repaired in place. Progress lines were unaffected.
- The verifier's chapter matching used a two-character prefix and was shadowed by the new `03b` files; fixed in `verify.py`.

## What remains

1. Revoke the Shopify token (owner action).
2. Wave-1 clones (21) still share their generated prose; a bespoke rewrite is the only way past the `shared>40` and `reviewpara` gates.
3. nethris MapGroup conversion (L); ww17 integration test needs a migrated database to run once; formforge's default Vitest pool times out on this laptop (use `--pool=threads`).
4. Off-stack Java items deliberately skipped (j1/j3 reformat and code changes) are listed in their reports.

## Index of tooling

`fable_edit.py` (safe chapter edits, reports), `family_express.py` (wave-1 Express family helpers), `wave1_sweep.py`, `sync_examples.py`, `phase3_bulk.py`, `verify.py` (`verify_before.json` / `verify_after.json`), `junction.py` (dependency junctions), `scripts/<slug>.py` and `scripts/b1{5,6,7,8}*.py` (per-project changes, each writing `<slug>.done.json`).
