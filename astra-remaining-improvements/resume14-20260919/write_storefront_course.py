from pathlib import Path
P = Path(__file__).resolve().parent.parent / 'stage/f9326daabc23'
chapters = {
'README.md': ('A consistent catalog without per-card queries', '''
Storefront is a Next.js, TypeScript and Prisma learning project with an existing curriculum and architectural decision records. This companion course improves the implemented catalog read path. It does not claim to implement the future cart, checkout or administration sprints described in the product specification. Begin with docs/curriculum/SPEC.md and the decisions about service DTOs, integer money and URL-backed pagination.

The completed work aligns category counts with the buyable-product filter used by catalog lists. It returns complete card data from the page repository instead of asking the page component to make separate image and stock reads for every card. Display prices come from current variants even when a product's denormalized price window is missing or stale. Detail attributes become owned plain-object values, and page URLs accept only complete positive safe integers.

You should be comfortable with promises, array transformations, TypeScript interfaces and basic SQL filtering. A repository owns database access. A service converts repository rows into public view models. A denormalized value is a stored summary that must be maintained when its source changes. An N+1 pattern issues additional reads for each item in an already fetched list; batching removes that growth in repository calls.

Install with the project's pinned pnpm version and lockfile, generate the Prisma client, and use the finite test, typecheck, lint and build commands in VERIFICATION. Client generation does not initialize a database. Unit tests replace data access and check real mapping and query construction. Build verification uses the existing no-database behavior and must not be interpreted as a successful live catalog request.

Read the codebase map and concepts, then compare the worked change with original snapshots. Try the practice cases before checking the solutions. Finish by tracing a twelve-card page through the service and UI, counting repository calls and identifying which fields cross the boundary.
''', None),
'01-CODEBASE-MAP.md': ('Repository rows become complete card values', '''
The products page awaits searchParams and calls parseCatalogParams in lib/catalog-params.ts. That framework-free helper narrows sort to known values, trims category and validates page text. The page asks the catalog service for categories and a paginated result, then hands complete card DTOs to ProductGrid. It no longer loops over items and awaits image and stock helpers for each one.

server/services/catalog.ts contains the application-facing view models. listCatalog counts matching products, clamps the requested page and requests one bounded slice. The returned rows contain only the product fields, variant price and stock fields, and a selected cover image required by the cards. The service converts cents to Money and reduces the relation data to priceVaries, inStock and a small image object. Prisma-shaped relation arrays do not cross into the UI.

server/data/products.ts remains the only relevant location for Prisma queries. buyableProductWhere expresses the requirement for at least one variant and an optional category filter. Product listing and count use it, and server/data/categories.ts uses the same base predicate inside each category's product count. The existing SQL ordering and ID tie-break remain intact.

Detail reads still use getBySlug with the existing variants, images and categories. getProductDetail now normalizes attributes instead of asserting that every JSON value is a record. Scalars and arrays become an empty object, while accepted plain objects are deeply cloned. This prevents a consumer mutating nested DTO values from changing a repository fixture or cached object by alias.

The architecture rules remain enabled. Services import shared helpers and data access, components import services, and Prisma stays in server/data. Read ADR-0001 and ADR-0003 before moving a query into a component or returning a database row directly.
''', ('server/data/categories.ts', 'export function findCategoriesWithCounts', None)),
'02-CONCEPTS.md': ('Count consistency and bounded query growth', '''
A category badge and a catalog page must describe the same population. If a category count includes products without variants while the list excludes them, the badge promises items the shopper cannot see or buy. Sharing the variant-existence predicate fixes that logical mismatch. It does not turn separate queries into a database snapshot: concurrent insertion or deletion can still change the population between count and page reads.

For twelve cards, the previous page loop performed twenty-four additional repository reads after fetching the page: one image and one stock aggregate per item. The new paged query selects the relation fields needed for all cards. Prisma may implement relation loading as several batched SQL statements, so the claim is bounded query growth, not necessarily exactly one SQL statement. The UI receives a complete DTO and performs no per-card database follow-up.

Prices have two roles. The denormalized minPriceCents column supports indexed SQL sorting, as ADR-0004 describes. Actual variants own the displayed price. A null summary must not become an invented zero-dollar offer, and a stale summary must not override the current variant amounts. This change computes the display range from selected variants while retaining the existing indexed sort. Future price-write paths still need to maintain the summary to keep sorting accurate.

Stock is an existence question for the card: at least one variant has positive stock. Summing positive and negative values can hide a buyable variant. The new mapping checks each variant for stock greater than zero. Money remains integer minor units and uses the project's existing Money constructor and single-store USD policy.

Finally, a DTO should own mutable nested values. A type assertion changes TypeScript's view but neither validates JSON shape nor copies it. cloneAttributes performs both the top-level shape check and the deep copy needed by the detail response.
''', ('server/services/catalog.ts', 'function cloneAttributes', 'export async function getProductDetail')),
'03-WORKED-CHANGE.md': ('Replace the actual listing follow-up loop', '''
Start at app/(storefront)/products/page.tsx rather than adding an unused batch helper. The old page iterated over listCatalog items, awaited getCardImage, then awaited getCardStock, and assembled a second products array. Removing that loop is the integration step that makes the repository improvement affect the real route. ProductGrid now receives the service's complete items directly.

listPaged selects variant priceCents and stock and one image per product. Image ordering prefers isPrimary, then position, then ID as a deterministic final tie-break. Selecting only URL and alt avoids returning unrelated image columns. The service filters a defensively encountered variantless row and computes minimum and maximum from real variant prices. A missing denormalized window no longer implies free merchandise.

The shared buyableProductWhere function is exported within the data layer. Category counts call it without a category argument because the enclosing relation already selects each category's products. List and count pass an optional category slug. This keeps the inclusion rule in one place without moving database knowledge into the UI.

parseCatalogParams replaces parseInt with full-string digit validation and a safe-integer check. Values such as 2x, 1.5 and 1e2 fall back to page one. Leading zeros in otherwise valid integer text normalize to the same numeric page. buildCatalogHref passes its inputs through the same normalization before emitting query parameters, so invalid fractional or infinite numbers do not produce unstable links.

The existing sort order still ends in an ID tie-break; that behavior was preserved rather than newly introduced. The delivered tests target the new inclusion, mapping, query-cost and ownership boundaries while retaining the earlier pagination, money and component coverage.
''', ('server/services/catalog.ts', '  const items: ProductListCore[]', '  return { items')),
'04-TESTING-AND-DEBUGGING.md': ('Connect mock contracts to production call sites', '''
The service suite replaces repository exports and calls the actual catalog service. A twelve-card regression requires one count call and one page call, and explicitly requires no findPrimaryImage or sumVariantStock calls. It verifies returned images, positive-stock behavior and actual variant pricing when a denormalized summary is stale. A second case covers null summaries and a row whose variants are absent.

The repository boundary suite calls the production functions with a query-spying Prisma client. It checks that category counts, product counts and list queries contain the same variant-existence predicate. It also inspects the page select: only required variant fields, one cover image, and deterministic image ordering. These assertions ensure that a service mock promising batched data corresponds to the real adapter query.

Detail tests pass null, scalar and array attribute values and require empty objects. A nested accepted object is then mutated through the returned DTO; the original fixture must remain unchanged. This catches the difference between a shallow spread and the deep ownership guarantee. URL tests cover partial numeric strings, unsafe integers, repeated parameters, whitespace and canonical link generation.

The project's existing component tests still verify card and grid rendering. The real products page was inspected and changed to consume complete items, so the new service helper is not disconnected from the application. Typechecking validates the expanded row inference and DTO compatibility. Lint enforces the architectural import boundaries, and the production build checks framework integration.

When a typecheck reports that Prisma has no exported generated types, first generate the client from the checked-in schema. Do not weaken types or add any casts to hide missing generated code. When a test fails, distinguish malformed fixtures from a real missing behavior; keep valid positive controls so a mapping that returns no products cannot satisfy all assertions.
''', ('server/data/catalog-boundaries.test.ts', '  it("selects only card', None)),
'05-PRACTICE.md': ('Extend the catalog without breaking its boundaries', '''
Exercise one: add a repository test for a category containing one product with variants and another with none. At the unit layer, inspect the filtered relation count query rather than inventing a separate counting function. Design a later database integration fixture that inserts both products and verifies that the category badge and listing total each report one. Explain which part your unit test proves and which part needs the provider.

Exercise two: extend the twelve-card service test with multiple positive-stock variants and an image-free product. Verify that stock uses an existential condition, image absence becomes null, and priceVaries reflects current variant prices. Assert that the returned item exposes neither relation arrays nor createdAt. Keep the repository call-count assertions so adding a display field cannot quietly reintroduce a per-card query.

Exercise three: add URL roundtrip cases. Parse a repeated page parameter whose first value is invalid, build a link from the result, and parse that link again. The default page should stay omitted. Repeat with a valid leading-zero number and a category containing spaces. Distinguish category trimming from URL encoding and confirm the deterministic category, sort, page parameter order.

Exercise four: propose a future variant-price write operation that maintains minPriceCents and maxPriceCents atomically. Identify where validation, authorization, variant mutation and summary recomputation belong under the existing layering rules. Explain why sorting only the twelve fetched products in JavaScript would not repair a stale global price ordering. This is a design exercise; the current catalog change does not implement an administration write path.

For every exercise, include a positive visible result and a rejection or absence case. Preserve integer cents and the single-store currency rule. Use source links and actual call sites when explaining your result, and record executed tests separately from future integration plans.
''', None),
'06-SOLUTIONS-AND-REVIEW.md': ('What a correct extension demonstrates', '''
The category exercise should assert a relation count filtered by variants some, matching the page's shared buyableProductWhere condition. A live database test would additionally prove provider execution and actual returned counts for inserted rows. The unit fixture cannot prove that by returning a constant one; it proves the query's intended population. Keep that distinction explicit in any test report.

For the card exercise, use variants whose current prices disagree even when the product summary does not. The DTO should display the minimum actual price and priceVaries true. At least one positive stock value makes inStock true even if another fixture value is negative. An empty image selection becomes null. The service should still issue exactly one page call and one count call, with no per-item follow-ups. The database adapter may use multiple batched relation statements internally.

For the URL exercise, repeated values follow the existing first-value rule. An invalid first page value becomes one even if a later repeated value is valid. The href builder omits page one and the default newest sort. Leading zeros normalize through a numeric value, categories are trimmed, and URLSearchParams handles encoding. Partial text, fractions, exponent notation and unsafe integers must not become alternate representations of a page.

For the future price-write design, put Prisma operations in the data layer and business orchestration in a framework-free service. Update the variant and recompute the product summary in one transaction under a concurrency strategy appropriate to competing variant edits. Authorization belongs before mutation. Updating only the displayed card or sorting a fetched slice cannot restore the global SQL ordering needed for correct pagination.

Review existing decisions before adding another cache or DTO field. Preserve server-only boundaries, integer Money and explicit empty states. Do not claim the preserved ID tie-break is a new fix, or that the no-database build validates live query execution. The course should describe the precise behavior supported by the executed evidence.
''', None),
'07-TRACE-LAB.md': ('Trace a twelve-card category request', '''
Open /products?category=audio&page=2&sort=price_asc. The server page awaits searchParams and calls parseCatalogParams. The category remains audio, page becomes the safe integer two, and the known sort value is retained. Category navigation obtains filtered product counts. listCatalog counts products with variants in audio and computes totalPages before deciding the clamped page and skip offset.

Suppose the total is twenty. Page two is valid, skip is twelve, and the page repository returns at most twelve rows in the existing SQL price order with its final ID tie-break. Each returned row already contains current variant price/stock fields and its selected cover image. The service builds Money values in USD, determines whether prices vary, tests for a positive-stock variant and projects a small image object or null.

The products page gives those complete DTOs to ProductGrid. Each ProductCard renders heading, formatted price, image fallback and its disabled future cart affordance. There is no loop calling separate image and stock services. Count the repository calls at the application boundary and distinguish that number from the internal SQL statements Prisma may issue to batch relation loading.

Now corrupt only a product's stored minPriceCents summary in your fixture. The displayed price still follows actual variants, but the existing SQL price ordering can remain stale until a writer repairs the summary. Explain why the read change deliberately does not sort the returned slice in memory. Such sorting would rearrange only one page and could not correct which products belong on that page.

Finally, remove a product between count and page read. The shared predicate keeps their definitions aligned but cannot freeze time across separate queries. The returned total may briefly describe the earlier population. Use this trace to separate filter consistency, deterministic ordering, display correctness and snapshot consistency instead of treating all four as a single pagination guarantee.
''', None),
'VERIFICATION.md': ('Finite checks and explicit database limits', '''
Verification runs the complete finite Vitest suite, TypeScript typecheck, architectural lint and Next production build. Exact command records and logs are linked in the evidence table after packaging. The project uses pnpm and its existing lockfile; client generation is recorded separately because it creates the Prisma types required by type inference. A successful installation or generated client is not counted as a test result.

The added regressions cover shared buyable predicates, lean relation selection, a twelve-card mapping with bounded repository calls, null and stale price windows, positive-stock semantics, defensive variant absence, JSON attribute ownership and strict URL integer parsing. Earlier money, pagination and component tests remain part of the full suite. Unit tests use repository or Prisma-client spies and do not require a live PostgreSQL connection.

Build verification uses an inert loopback database URL. The existing product detail generateStaticParams implementation already catches unavailable database reads and returns an empty static-parameter list. That fallback was not introduced to hide a failure in this change. The build therefore validates compilation and route integration, but it does not prove live catalog queries or pre-rendered product content. No user database is migrated, seeded or reset for this verification.

The repository-query assertions establish intended predicates and selected relations. They do not measure exact SQL counts or query latency. Prisma can load relations in a bounded set of batched statements, so performance claims are limited to removing per-card application follow-ups. A production workload benchmark and provider integration fixture would be separate evidence.

The denormalized sort summary still needs maintenance by future write paths, and separate count/list queries do not promise a concurrent snapshot. Cart and checkout remain future curriculum work. Use the original snapshots to review the implemented read changes, preserve the existing architectural rules, and rerun relevant commands after later source edits rather than treating this report as permanent validation.
''', None),
}
nav = '\n## Course navigation\n\n' + ' / '.join(f'[{n.removesuffix(".md")}]({n})' for n in chapters) + '\n'
(P / 'astraupskill').mkdir(exist_ok=True)
for name, (title, body, excerpt) in chapters.items():
    text = '# ' + title + '\n\n' + body.strip() + '\n'
    if excerpt:
        filename, start, end = excerpt; source = (P / filename).read_text(encoding='utf-8-sig'); index = source.index(start)
        sample = source[index:source.index(end, index) if end else len(source)].rstrip()
        text += f'\n## Source excerpt\n\nFrom [{filename}](../{filename}).\n\n```ts\n{sample}\n```\n'
    text += nav
    assert len(text.split()) >= 250, (name, len(text.split()))
    (P / 'astraupskill' / name).write_text(text, encoding='utf-8')
    print(name, len(text.split()))
p = P / 'README.md'; text = p.read_text(encoding='utf-8')
if 'astraupskill/README.md' not in text: text += '\n## Catalog consistency course\n\n[Start the source-based companion course](astraupskill/README.md) for buyable counts, complete card DTOs, current variant prices, URL validation and verification evidence.\n'
p.write_text(text, encoding='utf-8')
