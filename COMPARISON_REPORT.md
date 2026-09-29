# AstraOrganized vs. AstraOrganized2

**The independent inventory contains 388 records versus 341 in the earlier catalog: a net increase of 47.** This is mainly a difference in grouping, not evidence that 47 new applications appeared.

The new inventory was completed and hashed before `AstraOrganized` was opened. Its assessments have not been changed using the earlier catalog. See [the baseline checkpoint](independent-baseline.json). The original index is retained in `independent-snapshot`; only its navigation anchors were subsequently corrected.

## Main differences

| Area | AstraOrganized | AstraOrganized2 |
|---|---|---|
| `geminiorganized` | One container record | 78 project/resource records, with copied versions visible |
| `gitvg` | One container record | 17 independently versioned projects plus the `astra` learning collection |
| `jsharness` | One container record | Separate `ctvodejs` and `VTCode` repositories |
| `newcodexJS` | 22 rows: 20 practice apps, `docs`, and `scripts` | One workspace record with component paths in JSON |
| Empty folders counted by the earlier catalog | 27 project rows | Listed in coverage notes rather than counted as projects |
| Records with explicit inspected-file references | 239 of 341 | 377 of 388 |
| Relationships | Primarily similar-name relationships | 56 likely copy/version groups based on matching multi-file samples |
| Grouping for browsing | Mostly Desktop folder/category names | Project purpose/type, plus a location summary |
| IDs and paths | Readable `proj-...` IDs and absolute paths | UUIDs, Desktop-relative paths, and absolute paths |

**Count reconciliation:** 341 − 27 empty-folder rows − 3 container rows − 22 `newcodexJS` rows + 78 Gemini records + 18 `gitvg` records + 2 `jsharness` records + 1 `newcodexJS` workspace = **388**.

The earlier index is more convenient if you want each `newcodexJS` exercise shown as its own row. The new index is more useful for seeing the separate repositories inside the larger containers and identifying copied versions. Neither row count is a count of unique, production-ready applications.

## Matching and assessment changes

- **289 records match by normalized Desktop path.** The 99 new-only paths and 52 old-only paths are fully explained by the scope changes above.
- **195 shared records have different apparent-state labels.** The new labels use sampled code and configuration. These differences are not runtime test results and do not prove that a project became working or broken.
- Stack detail is stored differently: the new catalog separates languages, frameworks, data stores, infrastructure, testing, and integrations. Comparing raw tag counts would be misleading.
- Missing inspected-file references in the older JSON mean the evidence was not recorded there; they do not establish that no files were inspected.
- The older catalog reuses three IDs across different paths: `proj-nethris`, `proj-aiapplybot`, and `proj-new-folder`. New IDs are unique. When joining catalogs, use the path-aware crosswalk rather than the old ID alone.
- Neither inventory runs projects. The new inventory also records documentation caveats, including archived sources, scaffolds, mocked services, and unimplemented plans.

## Examples of clarified descriptions

| Project | Earlier description | New description |
|---|---|---|
| [.netarchitectureproject](../.netarchitectureproject) | Application project or component in .netarchitectureproject. | Full Modular Monolith .NET application with Domain-Driven Design approach. |
| [buildsmallplates](../buildsmallplates) | **A local-first weightlifting log for beginner and intermediate lifters — React Native (Expo) build.** | Small Plates mobile weightlifting log with workout progression and on-device storage. |
| [_Organized Desktop/03 Master Projects/masterrnative](../_Organized%20Desktop/03%20Master%20Projects/masterrnative) | Application project or component in masterrnative. | Expo farm-batch tracker for feed, mortality, expenses, and sales. |
| [_Organized Desktop/05 Numbered Experiments/ww49](../_Organized%20Desktop/05%20Numbered%20Experiments/ww49) | This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app). | Order-operations dashboard with coupons, fulfillment, refunds, and audit services. |
| [_Organized Desktop/02 Build Projects/buildjira](../_Organized%20Desktop/02%20Build%20Projects/buildjira) | BuildJira is now migrated to C# and ASP.NET Core. | Jira-style project and issue tracker; the active app is C#, with earlier JavaScript code retained as archival reference. |

## Evidence and limitations

- The independent scan covered 100,421 directories and 415,133 files after exclusions, and accounted for all 108 discovered Git roots.
- All 24 initial long-path errors were recovered. Every catalog evidence/material path and relationship reference passed validation.
- Matching sample fingerprints indicate likely copies or versions; the full source trees were not byte-compared. Changed copies may not be linked.
- The comparison reads the two saved catalogs. It does not reinterpret differences as confirmed feature changes, and it does not merge the older assessments into the independent catalog.
- UUIDs differ from the older IDs. Use [the ID crosswalk](project-id-crosswalk.json) to join the 289 exact path matches and inspect changed project boundaries.

## Full difference data

- [Independent project index](PROJECT_INDEX.md)
- [Machine-readable field differences and coverage changes](comparison-details.json)
- [ID crosswalk and scope mappings](project-id-crosswalk.json)
- [Independent validation](inventory-validation.json)

## Empty-folder rows removed from the project count

- [.nethris](../.nethris)
- [_Organized Desktop/02 Build Projects/aff-wt-be06](../_Organized%20Desktop/02%20Build%20Projects/aff-wt-be06)
- [_Organized Desktop/03 Master Projects/master 5](../_Organized%20Desktop/03%20Master%20Projects/master%205)
- [_Organized Desktop/03 Master Projects/master555](../_Organized%20Desktop/03%20Master%20Projects/master555)
- [_Organized Desktop/04 JavaScript Training/jsinterview](../_Organized%20Desktop/04%20JavaScript%20Training/jsinterview)
- [_Organized Desktop/04 JavaScript Training/jstran2.0](../_Organized%20Desktop/04%20JavaScript%20Training/jstran2.0)
- [_Organized Desktop/04 JavaScript Training/rewritepy2jsodoo](../_Organized%20Desktop/04%20JavaScript%20Training/rewritepy2jsodoo)
- [_Organized Desktop/05 Numbered Experiments/f1](../_Organized%20Desktop/05%20Numbered%20Experiments/f1)
- [_Organized Desktop/05 Numbered Experiments/j6](../_Organized%20Desktop/05%20Numbered%20Experiments/j6)
- [_Organized Desktop/06 AI And Learning/booklearn](../_Organized%20Desktop/06%20AI%20And%20Learning/booklearn)
- [_Organized Desktop/06 AI And Learning/claudelearnpath](../_Organized%20Desktop/06%20AI%20And%20Learning/claudelearnpath)
- [_Organized Desktop/08 App And Product Projects/recipegen](../_Organized%20Desktop/08%20App%20And%20Product%20Projects/recipegen)
- [_Organized Desktop/10 New Folders/New folder](../_Organized%20Desktop/10%20New%20Folders/New%20folder)
- [_Organized Desktop/10 New Folders/New folder (10)](../_Organized%20Desktop/10%20New%20Folders/New%20folder%20%2810%29)
- [_Organized Desktop/10 New Folders/New folder (11)](../_Organized%20Desktop/10%20New%20Folders/New%20folder%20%2811%29)
- [_Organized Desktop/10 New Folders/New folder (12)](../_Organized%20Desktop/10%20New%20Folders/New%20folder%20%2812%29)
- [_Organized Desktop/10 New Folders/New folder (13)](../_Organized%20Desktop/10%20New%20Folders/New%20folder%20%2813%29)
- [_Organized Desktop/10 New Folders/New folder (2)](../_Organized%20Desktop/10%20New%20Folders/New%20folder%20%282%29)
- [_Organized Desktop/10 New Folders/New folder (3)](../_Organized%20Desktop/10%20New%20Folders/New%20folder%20%283%29)
- [_Organized Desktop/10 New Folders/New folder (4)](../_Organized%20Desktop/10%20New%20Folders/New%20folder%20%284%29)
- [_Organized Desktop/10 New Folders/New folder (5)](../_Organized%20Desktop/10%20New%20Folders/New%20folder%20%285%29)
- [_Organized Desktop/10 New Folders/New folder (6)](../_Organized%20Desktop/10%20New%20Folders/New%20folder%20%286%29)
- [_Organized Desktop/10 New Folders/New folder (7)](../_Organized%20Desktop/10%20New%20Folders/New%20folder%20%287%29)
- [_Organized Desktop/10 New Folders/New folder (8)](../_Organized%20Desktop/10%20New%20Folders/New%20folder%20%288%29)
- [Amasterplan](../Amasterplan)
- [codexlearnp1](../codexlearnp1)
- [New folder](../New%20folder)

## New records within expanded containers

- [geminiorganized/FableDocs_Projects_Hermes](../geminiorganized/FableDocs_Projects_Hermes)
- [geminiorganized/General_.Architectureproject](../geminiorganized/General_.Architectureproject)
- [geminiorganized/General_.Open2](../geminiorganized/General_.Open2)
- [geminiorganized/General_.Todo](../geminiorganized/General_.Todo)
- [geminiorganized/General_Alanandelisoccer](../geminiorganized/General_Alanandelisoccer)
- [geminiorganized/General_Ankijs](../geminiorganized/General_Ankijs)
- [geminiorganized/General_Aral](../geminiorganized/General_Aral)
- [geminiorganized/General_Borrowbox](../geminiorganized/General_Borrowbox)
- [geminiorganized/General_C#Interview](../geminiorganized/General_C%23Interview)
- [geminiorganized/General_Campusops](../geminiorganized/General_Campusops)
- [geminiorganized/General_Cleanarch](../geminiorganized/General_Cleanarch)
- [geminiorganized/General_Csharptut](../geminiorganized/General_Csharptut)
- [geminiorganized/General_Devdeck](../geminiorganized/General_Devdeck)
- [geminiorganized/General_Finance-Dashboard](../geminiorganized/General_Finance-Dashboard)
- [geminiorganized/General_Formforge](../geminiorganized/General_Formforge)
- [geminiorganized/General_Gitjira](../geminiorganized/General_Gitjira)
- [geminiorganized/General_Gitjira-App](../geminiorganized/General_Gitjira-App)
- [geminiorganized/General_Gitvg](../geminiorganized/General_Gitvg)
- [geminiorganized/General_Globehire](../geminiorganized/General_Globehire)
- [geminiorganized/General_Jsharness](../geminiorganized/General_Jsharness)
- [geminiorganized/General_Jstut](../geminiorganized/General_Jstut)
- [geminiorganized/General_Masternocu](../geminiorganized/General_Masternocu)
- [geminiorganized/General_Masteroutline](../geminiorganized/General_Masteroutline)
- [geminiorganized/General_MasterPlan](../geminiorganized/General_MasterPlan)
- [geminiorganized/General_Meterforge](../geminiorganized/General_Meterforge)
- [geminiorganized/General_Missioncontrol](../geminiorganized/General_Missioncontrol)
- [geminiorganized/General_Mobiletagalog](../geminiorganized/General_Mobiletagalog)
- [geminiorganized/General_Newcodecjs2](../geminiorganized/General_Newcodecjs2)
- [geminiorganized/General_Newcodex3](../geminiorganized/General_Newcodex3)
- [geminiorganized/General_Newcodexjs](../geminiorganized/General_Newcodexjs)
- [geminiorganized/General_Nopsolutions](../geminiorganized/General_Nopsolutions)
- [geminiorganized/General_Open1](../geminiorganized/General_Open1)
- [geminiorganized/General_Open3](../geminiorganized/General_Open3)
- [geminiorganized/General_Open5](../geminiorganized/General_Open5)
- [geminiorganized/General_Perch](../geminiorganized/General_Perch)
- [geminiorganized/General_Readme](../geminiorganized/General_Readme)
- [geminiorganized/General_Recipeview](../geminiorganized/General_Recipeview)
- [geminiorganized/General_Recipeweb](../geminiorganized/General_Recipeweb)
- [geminiorganized/General_Resume](../geminiorganized/General_Resume)
- [geminiorganized/General_Skillforgejs](../geminiorganized/General_Skillforgejs)
- [geminiorganized/General_Spacegame](../geminiorganized/General_Spacegame)
- [geminiorganized/General_Tagalog](../geminiorganized/General_Tagalog)
- [geminiorganized/LLM_Generated_Applybot](../geminiorganized/LLM_Generated_Applybot)
- [geminiorganized/LLM_Generated_Buildbusinesses](../geminiorganized/LLM_Generated_Buildbusinesses)
- [geminiorganized/LLM_Generated_Buildermentor](../geminiorganized/LLM_Generated_Buildermentor)
- [geminiorganized/LLM_Generated_Buildevent](../geminiorganized/LLM_Generated_Buildevent)
- [geminiorganized/LLM_Generated_Buildreviewer](../geminiorganized/LLM_Generated_Buildreviewer)
- [geminiorganized/LLM_Generated_Buildsmallplates](../geminiorganized/LLM_Generated_Buildsmallplates)
- [geminiorganized/LLM_Generated_Buildsql](../geminiorganized/LLM_Generated_Buildsql)
- [geminiorganized/LLM_Generated_Buildwhiteboard](../geminiorganized/LLM_Generated_Buildwhiteboard)
- [geminiorganized/LLM_Generated_ClaudeDocs](../geminiorganized/LLM_Generated_ClaudeDocs)
- [geminiorganized/LLM_Generated_Ecommerceproject](../geminiorganized/LLM_Generated_Ecommerceproject)
- [geminiorganized/LLM_Generated_Fablehelperv2](../geminiorganized/LLM_Generated_Fablehelperv2)
- [geminiorganized/LLM_Generated_Fablehelperv3](../geminiorganized/LLM_Generated_Fablehelperv3)
- [geminiorganized/LLM_Generated_Gptdocs](../geminiorganized/LLM_Generated_Gptdocs)
- [geminiorganized/LLM_Generated_Grokjs](../geminiorganized/LLM_Generated_Grokjs)
- [geminiorganized/LLM_Generated_Groktuts](../geminiorganized/LLM_Generated_Groktuts)
- [geminiorganized/LLM_Generated_Helper](../geminiorganized/LLM_Generated_Helper)
- [geminiorganized/LLM_Generated_Hrproject](../geminiorganized/LLM_Generated_Hrproject)
- [geminiorganized/LLM_Generated_Js1](../geminiorganized/LLM_Generated_Js1)
- [geminiorganized/LLM_Generated_Jsprojectlearn](../geminiorganized/LLM_Generated_Jsprojectlearn)
- [geminiorganized/LLM_Generated_Multitenantproject](../geminiorganized/LLM_Generated_Multitenantproject)
- [geminiorganized/LLM_Generated_Orderproject](../geminiorganized/LLM_Generated_Orderproject)
- [geminiorganized/LLM_Generated_Ppmproject](../geminiorganized/LLM_Generated_Ppmproject)
- [geminiorganized/LLM_Generated_Rag](../geminiorganized/LLM_Generated_Rag)
- [geminiorganized/LLM_Generated_Supportproject](../geminiorganized/LLM_Generated_Supportproject)
- [geminiorganized/LLM_Generated_Teamproject](../geminiorganized/LLM_Generated_Teamproject)
- [geminiorganized/OpenSource_Upskilling_.Ramp](../geminiorganized/OpenSource_Upskilling_.Ramp)
- [geminiorganized/OpenSource_Upskilling_.Stripe](../geminiorganized/OpenSource_Upskilling_.Stripe)
- [geminiorganized/OpenSource_Upskilling_Auth](../geminiorganized/OpenSource_Upskilling_Auth)
- [geminiorganized/OpenSource_Upskilling_Docu](../geminiorganized/OpenSource_Upskilling_Docu)
- [geminiorganized/OpenSource_Upskilling_Drop](../geminiorganized/OpenSource_Upskilling_Drop)
- [geminiorganized/OpenSource_Upskilling_Intercom](../geminiorganized/OpenSource_Upskilling_Intercom)
- [geminiorganized/OpenSource_Upskilling_Linear](../geminiorganized/OpenSource_Upskilling_Linear)
- [geminiorganized/OpenSource_Upskilling_Notion](../geminiorganized/OpenSource_Upskilling_Notion)
- [geminiorganized/OpenSource_Upskilling_Shop](../geminiorganized/OpenSource_Upskilling_Shop)
- [geminiorganized/OpenSource_Upskilling_Snapshot](../geminiorganized/OpenSource_Upskilling_Snapshot)
- [geminiorganized/OpenSource_Upskilling_Snapshot1](../geminiorganized/OpenSource_Upskilling_Snapshot1)
- [gitvg/agora](../gitvg/agora)
- [gitvg/agora-net](../gitvg/agora-net)
- [gitvg/astra](../gitvg/astra)
- [gitvg/atlas](../gitvg/atlas)
- [gitvg/atlas-net](../gitvg/atlas-net)
- [gitvg/bazaar](../gitvg/bazaar)
- [gitvg/bazaar-app](../gitvg/bazaar-app)
- [gitvg/folio](../gitvg/folio)
- [gitvg/folio-app](../gitvg/folio-app)
- [gitvg/harbor](../gitvg/harbor)
- [gitvg/harbor-net](../gitvg/harbor-net)
- [gitvg/pulse](../gitvg/pulse)
- [gitvg/pulse-net](../gitvg/pulse-net)
- [gitvg/relay](../gitvg/relay)
- [gitvg/relay-app](../gitvg/relay-app)
- [gitvg/storefront](../gitvg/storefront)
- [gitvg/tracer](../gitvg/tracer)
- [gitvg/tracer-net](../gitvg/tracer-net)
- [jsharness/ctvodejs](../jsharness/ctvodejs)
- [jsharness/VTCode](../jsharness/VTCode)
- [newcodexJS](../newcodexJS)
