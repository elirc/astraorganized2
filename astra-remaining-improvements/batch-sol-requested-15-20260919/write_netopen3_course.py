from pathlib import Path
import json
from course_writer import write_course

base='Umbraco-CMS/'
helper=base+'src/Umbraco.Cms.Api.Management/Controllers/ManagementApiControllerBase.cs'
controller=base+'src/Umbraco.Cms.Api.Management/Controllers/Template/Item/SearchTemplateItemController.cs'
test=base+'tests/Umbraco.Tests.UnitTests/Umbraco.Cms.Api.Management/Controllers/Template/Item/SearchTemplateItemControllerTests.cs'
chapters={}
def add(name,title,body,file=test,anchor='',count=100):
    chapters[name]=(title,body,[(file,anchor,count)])

add('README.md','Preserve requested identity and search ordering','''
Umbraco template search first returns ordered entity identifiers, then hydrates full templates through another service. Hydration order need not match search order, and the two result sets can differ. The response should retain requested order, omit missing entities, and exclude entities that were not requested.

The shared OrderByRequestedIds helper previously sorted hydrated entities by Array.IndexOf. An unrequested identifier received index minus one and moved ahead of legitimate results. Duplicate hydrated rows could also survive, while repeated index searches added unnecessary work. The repair builds a first-entity lookup and iterates requested identifiers, removing each match after use.

The new contract returns each available requested identifier once, in its first requested position, using the first hydrated payload for duplicate entities. Template-controller regressions cover missing and extra entities, duplicate identifiers and payloads, and the existing empty-page short circuit. Search Total remains the search service's metadata rather than being replaced by hydrated item count.

Read the map and identity concepts, then follow the worked helper. Practice and its separate answers explore mismatched result sets. Verification records the focused unit test command and its limits. These tests use service and mapper substitutes; they do not establish search-index freshness, database integration, or back-office browser authorization.
''')
add('01-CODEBASE-MAP.md','Connect search identifiers to hydrated responses','''
SearchTemplateItemController calls IEntitySearchService.Search with the template object type, query, skip, and take. If the returned page has no items, it returns an empty response carrying the search Total. The existing short circuit avoids hydration and mapping for that empty page.

For a nonempty page, the controller extracts the ordered keys and calls ITemplateService.GetAllAsync. That service returns full templates, whose order is not assumed. The shared ManagementApiControllerBase helper selects and orders them according to the requested keys before IUmbracoMapper creates response models.

The helper is shared with other management endpoints, so its behavior is expressed in terms of IEntity keys rather than template-specific aliases. Its dictionary retains the first hydrated entity for a key. Iterating and removing requested keys produces an ordered, duplicate-free subset without enumerating dictionary values as the output.

The controller test fixture substitutes search, hydration, and mapping. Its mapper projection retains key and alias, allowing tests to detect both ordering errors and selection of the wrong duplicate payload. When debugging, compare the requested key sequence, hydrated entity sequence, and mapped response separately. The total count belongs to the search result and can legitimately differ from the number of hydrated items on one page.
''',file=controller,anchor='    public async Task<IActionResult> Search',count=100)
add('02-CONCEPTS.md','Ordering cannot admit an unrequested entity','''
Sorting by a requested identifier's array position assumes every hydrated entity occurs in that array. Array.IndexOf returns minus one when it does not. Sorting ascending then places that extra entity before all requested matches instead of excluding it. The defect is selection as well as ordering.

The corrected contract starts from the requested identifiers as the authority for the output set. Hydrated data supplies payloads for those identifiers. Missing payloads are skipped, extra payloads are excluded, and duplicates have an explicit policy: first hydrated payload and first requested position win.

A dictionary supports average linear work over the hydrated and requested sequences. TryAdd retains the first payload. Remove during requested iteration both retrieves the match and prevents a repeated requested identifier from emitting it again. Output order comes from the requested sequence, not dictionary enumeration order.

Search Total is independent metadata. A page can contain fewer hydrated items because records disappeared or hydration omitted them, while Total still describes the search result. An empty page beyond the available range can likewise retain a nonzero total. This helper does not synchronize the search index with storage, and selecting requested identifiers is not a substitute for the endpoint's authorization rules.
''',file=helper,anchor='    protected static List<TEntity> OrderByRequestedIds',count=100)
add('03-WORKED-CHANGE.md','Build one lookup and consume requested matches','''
The replacement helper first enumerates hydrated entities and attempts to add each key and payload to a dictionary. A duplicate key leaves the original entry intact. No arbitrary last-write replacement or unstable sort tie determines which payload survives.

It then walks requestedIds in order. A successful Remove returns the stored entity and appends it to the result. A missing key does nothing. Because matched entries are removed, a repeated requested identifier cannot append the same entity twice. Any unrequested dictionary entries remain unused and never reach the response.

The template controller continues to call the shared helper before mapping. Its Total assignment and existing empty-page branch are unchanged. The new tests protect those surrounding behaviors while exposing the helper's old extra-entity and duplicate cases.

Review the algorithm with concrete sequences rather than only a normal sorted example. Requested A, missing, B with hydrated B, extra, A must yield A, B. Requested B, A, B with duplicate hydrated payloads must yield one B and one A using the first payload for each. The ordinary scrambled-order regression remains valuable, but those mismatched-set examples are what distinguish the repair from a simple sort refactor.
''',file=helper,anchor='    protected static List<TEntity> OrderByRequestedIds',count=100)
add('04-TESTING-AND-DEBUGGING.md','Assert identity, payload, metadata, and skipped calls','''
The existing normal-order test returns search keys A, B, C and hydrates C, A, B. It verifies the basic ordering contract. The new missing-and-extra case requests A, a missing key, and B, then hydrates B, an extra key, and A. It requires exactly A and B and preserves the supplied total of nineteen.

The duplicate case repeats both requested identifiers and hydrated entities. Distinct aliases on the first and later payloads make the winner observable. Assertions inspect the resulting identifiers and aliases, so an implementation that deduplicates by keeping the last payload cannot pass accidentally.

The empty-page case supplies no search items with a nonzero total. It requires an empty response with that total and verifies hydration and mapping were never called. This protects the controller's existing short circuit rather than claiming a newly introduced optimization.

These are focused controller unit tests. Search and template services are Moq substitutes, and mapping is a small projection. They cannot prove production index ordering, SQL behavior, or browser permissions. If a test fails, identify which sequence or boundary differs before broadening the fix. An item-count-only assertion would miss order and duplicate-payload errors, while an order-only assertion could miss an extra entity at the front.
''',file=test,anchor='    public async Task Search_Template_Item_Excludes_Unrequested',count=110)
add('05-PRACTICE.md','Work through mismatched result sets','''
Exercise one: requested identifiers are A, missing, B, while hydrated entities arrive as B, extra, A. Predict the old Array.IndexOf sort order and the corrected result. Explain why assigning a high sort index to extras would still fail the requirement to exclude them.

Exercise two: request B, A, B, A. Hydration returns A-first, B-first, B-later, A-later. Predict both identifiers and aliases in the response. Identify which dictionary operation chooses the first payload and which operation prevents repeated output.

Exercise three: return an empty search page with Total seventeen. Predict the response Total and the number of hydration and mapper calls. Explain why replacing Total with Items.Count would change pagination meaning.

Exercise four: keep the requested sequence fixed but reverse hydration order for distinct identifiers. Predict whether the response order changes. Then repeat with duplicate payloads and explain why reversing hydration can change the selected alias under the explicit first-payload policy.

Exercise five: consider a large batch. Compare repeated Array.IndexOf lookups with one dictionary construction and one requested-ID pass. State the average complexity assumption and the memory tradeoff. Keep performance reasoning separate from claims about authorization or search-index consistency, which this helper does not establish.
''',file=test,anchor='    public async Task Search_Template_Item_Collapses_Duplicate',count=110)
add('06-SOLUTIONS-AND-REVIEW.md','Keep selection separate from pagination metadata','''
The old sort places extra first because its requested index is minus one, followed by A and B. The corrected response contains A and B only. Moving extra to the end would improve order but still return an unrequested entity, so it would not satisfy the selection contract.

The duplicate example yields B-first followed by A-first. TryAdd preserves each first hydrated payload, and Remove consumes the entry on its first requested occurrence. Later duplicate requests find no entry and emit nothing. Distinct hydrated identifiers can arrive in any order without changing requested output order.

The empty page retains Total seventeen and calls neither hydration nor mapping. Total describes the search result, not simply the count of hydrated page items. Missing entities can reduce the returned page without authorizing this helper to rewrite that metadata.

Reversing hydration with duplicate payloads can change the selected alias because the policy explicitly retains the first hydrated entity. The tests document that choice rather than claiming a canonical payload across contradictory service responses. Average dictionary operations give linear passes at the cost of a lookup proportional to hydrated distinct keys.

During review, check extras, missing keys, requested duplicates, hydrated duplicates, order, and total independently. Also check shared-helper callers for compatibility. These unit results do not establish production authorization or synchronization between an index and persistent storage.
''',file=helper,anchor='    protected static List<TEntity> OrderByRequestedIds',count=100)
add('07-TRACE-LAB.md','Consume the lookup one requested key at a time','''
Draw a hydration column and an output column. Insert A-first into the lookup, then B-first. Attempt to insert B-later and A-later and record that both attempts leave the first values unchanged. Add an extra entity whose key never appears in the requested sequence.

Now iterate requested keys B, missing, A, B. Remove B and append B-first. Missing is absent, so append nothing. Remove A and append A-first. The repeated B is now absent because its entry was consumed earlier. The extra lookup entry remains unused. The final output is exactly B-first, A-first.

Pass those entities through the fixture mapper and inspect identifiers and aliases in the response. Copy Total from the search page without substituting the output length. This separates entity selection from pagination metadata and makes every operation in the algorithm observable in the controller regression.

Repeat the trace with an empty requested page. The controller returns before building keys or hydrating templates, so the helper is not invoked. Verify the mapper spy remains unused as well. Finally, replace the helper with the original sort in a disposable copy and identify which extra and duplicate assertions fail. Restore the reviewed implementation before running acceptance or packaging.
''',file=test,anchor='    public async Task Search_Template_Item_Empty_Page',count=100)
add('VERIFICATION.md','Use the focused controller suite as the boundary','''
The acceptance command uses [TemplateOrder.Tests.csproj](../scripts/template-order-tests/TemplateOrder.Tests.csproj). This focused project links the actual SearchTemplateItemControllerTests source from the upstream unit-test directory and references the real Management API project. It does not copy or reimplement the controller or helper. Run `dotnet test scripts/template-order-tests/TemplateOrder.Tests.csproj` from the project root in a normal checkout. Exact staging arguments, exit status, and TRX results are appended below after successful execution. Building referenced projects does not imply every upstream test or integration environment was exercised.

The four focused cases include the existing scrambled-order example and three new regressions for missing and extra hydration, duplicate identifiers with first-payload selection, and empty-page short-circuit behavior. Assertions preserve search Total independently of the number of returned entities and verify skipped service calls for an empty page.

Moq substitutes the search and template services. The mapper fixture projects key and alias. This establishes controller and shared-helper behavior under supplied results, not search-index quality, database consistency, or back-office browser authorization. No deployed CMS or user content store is modified by these unit checks.

The isolated staging copy omits Git history. The first two build attempts stopped in Umbraco's version task before tests ran. Subsequent commands supply GitVersionBaseDirectory and GitRepoRoot pointing to the original checkout for read-only version calculation; compilation still uses staged source. An intermediate run entered the back-office frontend install and was stopped. UmbracoBuild=true skipped those assets, but the full upstream test project still invoked a nested packaging-schema generator without the metadata arguments. The focused project avoids those unrelated packaging dependencies. Its Directory.Packages.props imports upstream test pins; an initial standalone restore exposed dependency-version conflicts, and an intermediate import location failed restore. The accepted run uses the corrected standard props file. The build also reports existing System.Security.Cryptography.Xml 10.0.9 advisories and upstream documentation warnings. This selection fix does not upgrade those dependencies, certify the full upstream test project, or claim a warning-free build.

The implementation was staged only after the immutable source baseline completed. Original snapshots and canonical hash checks accompany delivery. Earlier restore or build failures remain in the campaign record if any occur. The source-linked exercises explain the selection contract and its limits; reading them or passing the software tests does not establish human mastery. Broader upstream behavior or performance benchmarking would require additional evidence rather than being inferred from the focused suite.
''',file=controller,anchor='    public async Task<IActionResult> Search',count=100)
write_course('b8fb41bd6255',chapters,'Trace requested-ID selection, stable hydration ordering, duplicate policy, and empty-page regressions.')
b=Path(__file__).resolve().parent.parent
(b/'specs/b8fb41bd6255.json').write_text(json.dumps({'changedFiles':[],'summary':['Replaced repeated index sorting with first-payload lookup and requested-ID iteration, excluding unrequested and duplicate entities.','Added template-controller regressions for missing/extra results, duplicate payloads and preserved empty-page metadata.','Added nine source-based guide chapters with focused verification evidence.'],'limits':['Controller tests use service and mapper substitutes; they do not certify production search, database or browser authorization behavior.','Focused unit verification does not imply the complete upstream Umbraco test suite passed.']},indent=2),encoding='utf-8')
