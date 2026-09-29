# Disk cleanup proposal — modified upskilling projects

**Report only. Nothing has been deleted, moved, uninstalled, or cleaned. Your confirmation is required before any cleanup.**

Measured 2026-09-20T22:52:35.099531+00:00 to 2026-09-20T23:03:45.793549+00:00 (UTC). C: had **5.65 GiB free** at the end of the scan.

Scope: **182 previously modified project paths**, consolidated into **179 non-overlapping canonical scan roots**, plus AstraOrganized2 work areas and the shared caches listed below. This includes the earlier Fable-reviewed projects for inventory only; their code was not changed. The 132 unrelated queued project families were not added to the canonical-project scan.

The scope comes from the [153-project registry](../fablereview/registry.json) and completed entries in the [delivery ledger](../astra-remaining-improvements/progress.json). Nested entries covered by a parent scan are recorded in the JSON inventory. This is not a scan of every file on the device.

## Size summary and proposed approval groups

| Group | Measured logical size | Meaning |
|---|---:|---|
| A1: project/campaign dependencies and caches | **37.02 GiB** | Best first cleanup candidates for a source-only learning archive. |
| A2: shared user package/browser caches | **11.63 GiB** | Optional separate approval; affects other development projects too. |
| B: additional space after A1+A2 | **3.56 GiB** | Build/output folders and delivered staging copies; inspect contents before selecting. |
| A+B combined, paths counted once | **52.21 GiB** | Conditional logical-size ceiling, not guaranteed free-space gain. |

**These are logical file sizes, not measured reclaimable disk allocation.** NTFS compression, sparse files and package-store hard links can make actual freed space smaller. Symlinks/junctions were not followed. Nested candidates are not added twice in the totals above. In the CSV, `containedIn` identifies a parent candidate; do not sum all CSV rows.

## A1 — remove dependencies/caches while keeping the lessons

If you approve this group, the intended result is readable source, tests and learning documents without installed runtimes/dependencies/build caches. Reinstalling packages or tools and rebuilding would be necessary to run projects later. Keep package manifests, lockfiles, project/solution files, tool configuration, migrations and all source. This assumes you have not stored personal edits inside dependency/cache directories.

Largest measured A1 candidates (the CSV contains every path):

| ID | Size | Project/work area | Exact path |
|---|---:|---|---|
| D0003 | 2.13 GiB | AstraOrganized2 | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/npm-cache](../astra-remaining-improvements/npm-cache) |
| D0007 | 1.05 GiB | AstraOrganized2 | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/332058fd8671/node_modules](../astra-remaining-improvements/stage/332058fd8671/node_modules) |
| D0008 | 915.7 MiB | skillforgejs | [C:/Users/Owner/Desktop/skillforgejs/node_modules](../../skillforgejs/node_modules) |
| D0010 | 893.7 MiB | lucasrouter | [C:/Users/Owner/Desktop/lucasrouter/.next](../../lucasrouter/.next) |
| D0011 | 864.0 MiB | AstraOrganized2 | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/dependency-quarantine](../astra-remaining-improvements/dependency-quarantine) |
| D0014 | 832.5 MiB | AstraOrganized2 | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/80b4407b2971/node_modules](../astra-remaining-improvements/stage/80b4407b2971/node_modules) |
| D0015 | 806.3 MiB | AstraOrganized2 | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/5137a9c91d26/node_modules](../astra-remaining-improvements/stage/5137a9c91d26/node_modules) |
| D0017 | 803.3 MiB | AstraOrganized2 | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/9d3b119f40a0/node_modules](../astra-remaining-improvements/stage/9d3b119f40a0/node_modules) |
| D0020 | 776.4 MiB | AstraOrganized2 | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/38cbd0ab05af/node_modules](../astra-remaining-improvements/stage/38cbd0ab05af/node_modules) |
| D0029 | 749.4 MiB | AstraOrganized2 | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/7f871ce5e237/node_modules](../astra-remaining-improvements/stage/7f871ce5e237/node_modules) |
| D0031 | 739.1 MiB | AstraOrganized2 | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/f27db87d9d3a/node_modules](../astra-remaining-improvements/stage/f27db87d9d3a/node_modules) |
| D0032 | 736.9 MiB | AstraOrganized2 | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/27a8a1400c49/node_modules](../astra-remaining-improvements/stage/27a8a1400c49/node_modules) |
| D0034 | 714.5 MiB | AstraOrganized2 | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/4b702f01579b/node_modules](../astra-remaining-improvements/stage/4b702f01579b/node_modules) |
| D0035 | 714.0 MiB | AstraOrganized2 | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/toolchains](../astra-remaining-improvements/toolchains) |
| D0036 | 707.3 MiB | AstraOrganized2 | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/2c7ac2b52738/node_modules](../astra-remaining-improvements/stage/2c7ac2b52738/node_modules) |
| D0039 | 696.0 MiB | AstraOrganized2 | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/2d739127d551/node_modules](../astra-remaining-improvements/stage/2d739127d551/node_modules) |
| D0041 | 683.1 MiB | AstraOrganized2 | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/3e4e08e349a1/node_modules](../astra-remaining-improvements/stage/3e4e08e349a1/node_modules) |
| D0042 | 682.3 MiB | AstraOrganized2 | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/a80284ee08de/node_modules](../astra-remaining-improvements/stage/a80284ee08de/node_modules) |
| D0043 | 680.7 MiB | AstraOrganized2 | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/1c688787ace6/node_modules](../astra-remaining-improvements/stage/1c688787ace6/node_modules) |
| D0045 | 674.3 MiB | AstraOrganized2 | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/e5fa6d1a40be/node_modules](../astra-remaining-improvements/stage/e5fa6d1a40be/node_modules) |
| D0046 | 673.0 MiB | AstraOrganized2 | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/c178c034b3ed/node_modules](../astra-remaining-improvements/stage/c178c034b3ed/node_modules) |
| D0047 | 672.9 MiB | AstraOrganized2 | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/8c8b7f90a8d2/node_modules](../astra-remaining-improvements/stage/8c8b7f90a8d2/node_modules) |
| D0048 | 661.0 MiB | AstraOrganized2 | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/32d4e2fef457/node_modules](../astra-remaining-improvements/stage/32d4e2fef457/node_modules) |
| D0051 | 637.5 MiB | AstraOrganized2 | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/f9326daabc23/node_modules](../astra-remaining-improvements/stage/f9326daabc23/node_modules) |
| D0053 | 619.7 MiB | skillforgejs | [C:/Users/Owner/Desktop/skillforgejs/.next](../../skillforgejs/.next) |
| D0054 | 611.9 MiB | AstraOrganized2 | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/b7429e8bf71d/node_modules](../astra-remaining-improvements/stage/b7429e8bf71d/node_modules) |
| D0056 | 571.0 MiB | AstraOrganized2 | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/2f29156b71ed/node_modules](../astra-remaining-improvements/stage/2f29156b71ed/node_modules) |
| D0061 | 555.9 MiB | AstraOrganized2 | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/41315da7b7f9/node_modules](../astra-remaining-improvements/stage/41315da7b7f9/node_modules) |
| D0062 | 555.7 MiB | AstraOrganized2 | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/20574f0b81b4/node_modules](../astra-remaining-improvements/stage/20574f0b81b4/node_modules) |
| D0065 | 515.9 MiB | AstraOrganized2 | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/58c5c289a8ce/node_modules](../astra-remaining-improvements/stage/58c5c289a8ce/node_modules) |

## A2 — optional shared caches

These are outside the individual project folders. Removing them usually forces package/browser downloads later and can interrupt offline restore. They are not evidence that the corresponding software should be uninstalled.

| ID | Size | Exact path |
|---|---:|---|
| D0001 | 4.56 GiB | [C:/Users/Owner/.nuget/packages](../../../.nuget/packages) |
| D0002 | 4.29 GiB | [C:/Users/Owner/AppData/Local/pnpm/store](../../../AppData/Local/pnpm/store) |
| D0004 | 1.59 GiB | [C:/Users/Owner/AppData/Local/npm-cache](../../../AppData/Local/npm-cache) |
| D0005 | 1.19 GiB | [C:/Users/Owner/AppData/Local/ms-playwright](../../../AppData/Local/ms-playwright) |
| D0266 | 1.4 MiB | [C:/Users/Owner/AppData/Local/pip/Cache](../../../AppData/Local/pip/Cache) |

## B — larger optional deletions requiring a content check

A folder named `build`, `dist`, `bin`, `obj`, `vendor`, `artifacts` or `logs` is not automatically disposable. It can contain tracked files, custom scripts, database backups, useful screenshots or accepted evidence. These entries are candidates to inspect, not blanket deletion instructions. `.yarn` and IDE folders can contain configuration worth retaining.

Delivered staging copies under `astra-remaining-improvements/stage` have delivery manifests, but the size scan does not prove every staged file is duplicated. Before removing a whole copy, verify no later unique edits and retain the canonical project, guides, original snapshots and accepted check evidence. Smaller A candidates inside a staging copy are already counted in A.

| ID | Whole folder size | Additional after A | Type | Exact path |
|---|---:|---:|---|---|
| D0006 | 1.07 GiB | 818.8 KiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/332058fd8671](../astra-remaining-improvements/stage/332058fd8671) |
| D0009 | 911.6 MiB | 724.9 KiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/5137a9c91d26](../astra-remaining-improvements/stage/5137a9c91d26) |
| D0012 | 845.1 MiB | 714.2 KiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/80b4407b2971](../astra-remaining-improvements/stage/80b4407b2971) |
| D0013 | 835.4 MiB | 714.7 KiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/27a8a1400c49](../astra-remaining-improvements/stage/27a8a1400c49) |
| D0016 | 805.5 MiB | 2.2 MiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/9d3b119f40a0](../astra-remaining-improvements/stage/9d3b119f40a0) |
| D0018 | 787.4 MiB | 700.5 KiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/38cbd0ab05af](../astra-remaining-improvements/stage/38cbd0ab05af) |
| D0019 | 779.2 MiB | 581.0 KiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/2c7ac2b52738](../astra-remaining-improvements/stage/2c7ac2b52738) |
| D0021 | 770.9 MiB | 582.9 KiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/3e4e08e349a1](../astra-remaining-improvements/stage/3e4e08e349a1) |
| D0022 | 763.5 MiB | 1.9 MiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/7f871ce5e237](../astra-remaining-improvements/stage/7f871ce5e237) |
| D0023 | 761.0 MiB | 646.4 KiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/1c688787ace6](../astra-remaining-improvements/stage/1c688787ace6) |
| D0024 | 756.6 MiB | 485.9 KiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/e5fa6d1a40be](../astra-remaining-improvements/stage/e5fa6d1a40be) |
| D0025 | 756.1 MiB | 472.2 KiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/32d4e2fef457](../astra-remaining-improvements/stage/32d4e2fef457) |
| D0026 | 755.7 MiB | 633.2 KiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/8c8b7f90a8d2](../astra-remaining-improvements/stage/8c8b7f90a8d2) |
| D0027 | 749.9 MiB | 504.9 KiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/c178c034b3ed](../astra-remaining-improvements/stage/c178c034b3ed) |
| D0028 | 749.6 MiB | 720.7 KiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/f27db87d9d3a](../astra-remaining-improvements/stage/f27db87d9d3a) |
| D0030 | 739.7 MiB | 12.5 MiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/52d78d4a92a2](../astra-remaining-improvements/stage/52d78d4a92a2) |
| D0033 | 722.9 MiB | 684.4 KiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/4b702f01579b](../astra-remaining-improvements/stage/4b702f01579b) |
| D0037 | 706.2 MiB | 390.1 KiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/2d739127d551](../astra-remaining-improvements/stage/2d739127d551) |
| D0038 | 703.1 MiB | 1.0 MiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/f9326daabc23](../astra-remaining-improvements/stage/f9326daabc23) |
| D0040 | 691.6 MiB | 513.1 KiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/a80284ee08de](../astra-remaining-improvements/stage/a80284ee08de) |
| D0044 | 679.3 MiB | 620.9 KiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/b7429e8bf71d](../astra-remaining-improvements/stage/b7429e8bf71d) |
| D0049 | 658.9 MiB | 661.5 KiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/2f29156b71ed](../astra-remaining-improvements/stage/2f29156b71ed) |
| D0050 | 644.9 MiB | 644.9 MiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/b8fb41bd6255](../astra-remaining-improvements/stage/b8fb41bd6255) |
| D0052 | 628.1 MiB | 436.9 KiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/41315da7b7f9](../astra-remaining-improvements/stage/41315da7b7f9) |
| D0057 | 570.7 MiB | 1.3 MiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/58c5c289a8ce](../astra-remaining-improvements/stage/58c5c289a8ce) |
| D0058 | 565.2 MiB | 760.3 KiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/61d919e84af9](../astra-remaining-improvements/stage/61d919e84af9) |
| D0059 | 562.1 MiB | 446.3 KiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/20574f0b81b4](../astra-remaining-improvements/stage/20574f0b81b4) |
| D0060 | 559.4 MiB | 4.8 MiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/a8435f7ed53c](../astra-remaining-improvements/stage/a8435f7ed53c) |
| D0063 | 537.0 MiB | 1.7 MiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/077627a58eae](../astra-remaining-improvements/stage/077627a58eae) |
| D0064 | 516.7 MiB | 658.3 KiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/0bfafff7d45f](../astra-remaining-improvements/stage/0bfafff7d45f) |
| D0067 | 502.7 MiB | 1,021.6 KiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/9e1958f807df](../astra-remaining-improvements/stage/9e1958f807df) |
| D0068 | 494.9 MiB | 636.6 KiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/e7862246212d](../astra-remaining-improvements/stage/e7862246212d) |
| D0071 | 487.9 MiB | 575.9 KiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/3ecd02656197](../astra-remaining-improvements/stage/3ecd02656197) |
| D0074 | 469.1 MiB | 475.6 KiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/1c908de00eb7](../astra-remaining-improvements/stage/1c908de00eb7) |
| D0075 | 460.7 MiB | 686.0 KiB | Delivered staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/f98b34acf094](../astra-remaining-improvements/stage/f98b34acf094) |

## C — keep by default; only delete after a specific review

These are deliberately excluded from the proposed A+B total. Git history, backup/quarantine folders, unconfirmed staging areas, local databases and large archives may hold unique work or data. A remote repository does not prove uncommitted files or local branches are backed up. Database/VM files should not be removed as ordinary caches.

| ID | Size | Why retained | Exact path |
|---|---:|---|---|
| D0055 | 609.2 MiB | Unconfirmed staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/node_modules-z9-mismatch-20260913](../astra-remaining-improvements/stage/node_modules-z9-mismatch-20260913) |
| D0070 | 489.3 MiB | Git history — keep by default | [C:/Users/Owner/Desktop/netopen3/Umbraco-CMS/.git](../../netopen3/Umbraco-CMS/.git) |
| D0112 | 222.0 MiB | Unconfirmed staging copy | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/stage/node_modules-incomplete-80b4407b2971](../astra-remaining-improvements/stage/node_modules-incomplete-80b4407b2971) |
| D0120 | 165.3 MiB | Data/archive/large file — inspect | [C:/Users/Owner/Desktop/AstraOrganized2/documentation-audit/location-inventory.json](../documentation-audit/location-inventory.json) |
| D0144 | 92.4 MiB | Other work area / database fixture | [C:/Users/Owner/Desktop/AstraOrganized2/astrafinalplan/implementation/pg-test](../astrafinalplan/implementation/pg-test) |
| D0156 | 82.2 MiB | Git history — keep by default | [C:/Users/Owner/Desktop/netopen5/jellyfin/.git](../../netopen5/jellyfin/.git) |
| D0185 | 44.8 MiB | Git history — keep by default | [C:/Users/Owner/Desktop/buildsql/.git](../../buildsql/.git) |
| D0210 | 14.8 MiB | Git history — keep by default | [C:/Users/Owner/Desktop/JSProjectLearn/.git](../../JSProjectLearn/.git) |
| D0216 | 10.8 MiB | Other work area / database fixture | [C:/Users/Owner/Desktop/AstraOrganized2/astrafinalplan/implementation/batch04/stage](../astrafinalplan/implementation/batch04/stage) |
| D0221 | 8.9 MiB | Git history — keep by default | [C:/Users/Owner/Desktop/.netarchitectureproject/modular-monolith-with-ddd/.git](../../.netarchitectureproject/modular-monolith-with-ddd/.git) |
| D0222 | 8.9 MiB | Backups or quarantined originals | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/backups](../astra-remaining-improvements/backups) |
| D0224 | 8.6 MiB | Git history — keep by default | [C:/Users/Owner/Desktop/lucasrouter/.git](../../lucasrouter/.git) |
| D0231 | 6.4 MiB | Other work area / database fixture | [C:/Users/Owner/Desktop/AstraOrganized2/astrafinalplan/implementation/batch03/stage](../astrafinalplan/implementation/batch03/stage) |
| D0246 | 4.0 MiB | Git history — keep by default | [C:/Users/Owner/Desktop/gitjira-app/.git](../../gitjira-app/.git) |
| D0249 | 3.2 MiB | Other work area / database fixture | [C:/Users/Owner/Desktop/AstraOrganized2/astrafinalplan/implementation/stage](../astrafinalplan/implementation/stage) |
| D0258 | 1.9 MiB | Data/archive/large file — inspect | [C:/Users/Owner/Desktop/skillforgejs/data/skillforge.db](../../skillforgejs/data/skillforge.db) |
| D0261 | 1.7 MiB | Git history — keep by default | [C:/Users/Owner/Desktop/skillforgejs/.git](../../skillforgejs/.git) |
| D0264 | 1.4 MiB | Other work area / database fixture | [C:/Users/Owner/Desktop/AstraOrganized2/astrafinalplan/implementation/batch02/stage](../astrafinalplan/implementation/batch02/stage) |
| D0294 | 812.0 KiB | Data/archive/large file — inspect | [C:/Users/Owner/Desktop/astra4.2/interlude-extension.zip](../../astra4.2/interlude-extension.zip) |
| D0297 | 731.1 KiB | Git history — keep by default | [C:/Users/Owner/Desktop/formforge/.git](../../formforge/.git) |
| D0299 | 692.1 KiB | Git history — keep by default | [C:/Users/Owner/Desktop/buildsmallplates/.git](../../buildsmallplates/.git) |
| D0300 | 690.6 KiB | Backups or quarantined originals | [C:/Users/Owner/Desktop/AstraOrganized2/astrafinalplan/implementation/batch04/backups](../astrafinalplan/implementation/batch04/backups) |
| D0306 | 640.6 KiB | Backups or quarantined originals | [C:/Users/Owner/Desktop/AstraOrganized2/astra-remaining-improvements/snapshots](../astra-remaining-improvements/snapshots) |
| D0314 | 552.0 KiB | Data/archive/large file — inspect | [C:/Users/Owner/Desktop/_Organized Desktop/05 Numbered Experiments/e13/dev.db](../../_Organized%20Desktop/05%20Numbered%20Experiments/e13/dev.db) |
| D0320 | 522.4 KiB | Git history — keep by default | [C:/Users/Owner/Desktop/astra1/.git](../../astra1/.git) |

## Keep for upskilling

- Application source, tests, SQL/migrations, examples, fixtures and source assets.
- `astraupskill`, `upskilling`, `dfableandopus`, README files, project documentation, exercises and solutions.
- Canonical verification logs/screenshots and original-file snapshots used by those guides.
- Dependency manifests and lockfiles; `.csproj`/solution files; configuration and environment files needed to reconstruct the project.
- `.git` and backups unless you explicitly choose to give up their history/recovery value.
- Astra delivery manifests, baselines, progress ledgers and the cleanup inventory until the approved cleanup is checked.

The cleanup proposal does not remove whole canonical learning projects. Deleting installed dependencies does not normally reduce the usefulness of reading source or Markdown guides, but rendered apps, code execution, tests, and some editor tooling will stop working until restored.

## Full inventory and limitations

- [Every candidate path and size — CSV](disk-space-audit-2026-09-20/candidates.csv): 861 entries (A: 286, B: 285, C: 290).
- [Totals by project/work area — CSV](disk-space-audit-2026-09-20/projects.csv).
- [Raw project totals, candidates, errors and skipped links — JSON](disk-space-audit-2026-09-20/inventory.json).
- [Deduplicated summary — JSON](disk-space-audit-2026-09-20/summary.json).
- [Read-only scanner](disk-space-audit-2026-09-20/scan.py) and [scan log](disk-space-audit-2026-09-20/scan.log).
- Scan errors: **0**. Skipped links/reparse points: **8649**. Sizes exclude unreadable and linked targets; see the inventory for paths.
- Missing or unscanned roots: **0**; recorded separately in the summary JSON.
- This scan did not inspect running processes, Docker volumes, the Recycle Bin, Windows system folders, or cloud storage. It did not check Git tracking or hash-compare every staging copy. Shared caches are explicitly separated because their use is not project-exclusive.
- Actual cleanup would recheck selected paths and preserve excluded source/data. No deletion commands or automatic cleanup job have been scheduled.

## Confirmation choices

You can approve **A1 only**, **A1+A2**, or specific candidate IDs/paths from the CSV. B and C require explicit selections after their contents/recovery value are checked. Until then, all project and cache files remain in place.
