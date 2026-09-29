from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/7649d96533a4'
for f in (P/'astraupskill').glob('*.md'):
    t=f.read_text(encoding='utf-8-sig')
    for word in ['client','repository','parser','project']:t=t.replace(word+'?s',word+"'s")
    t=t.replace('?what number starts this string??','"what number starts this string?"').replace('?is the entire string a non-negative integer??','"is the entire string a non-negative integer?"')
    t=t.replace('if (!/^\\d+$/.test(value)) return undefined;','if (value === undefined) return undefined;\nif (value.length === 0 || /\\D/.test(value)) return undefined;')
    t=t.replace('the two executable tests','the five executable tests').replace('two executed runtime cases','five executed runtime cases')
    t=t.replace('The dependency free command passed two cases against the actual helper: canonical bounds remain numbers, while suffixes, decimals, and unsafe overflow disappear.','The dependency-free command passed five cases against the actual module: digit-only safe bounds remain numbers, malformed bounds are omitted, server-style arrays keep first-value semantics, valid listing state round-trips, and an independent zero bound survives.')
    t=t.replace('The captured log is `astraupskill/evidence/astra-crud-b03-masterstore.log` and the JSON result records 2/2.','The captured log is [the five-case output](evidence/crud-b03-astra-runtime.log), and [the result record](evidence/results.json) records 5/5.')
    t=t.replace("The URL is the client's create operation for query state; the server reads that state and uses it to retrieve products.", 'This is the read part of CRUD: the server parses query state and uses it to retrieve a product collection. Parsing a filter does not create or update a product.')
    if f.name=='03-WORKED-CHANGE.md':
        t+='\nAstra review caught a JavaScript regex edge: the dollar anchor may match before a final line terminator, so a superficially strict digit regex accepted a value ending in newline. The final implementation rejects any non-digit with /\\D/ and rejects the empty string separately. The executed cases include both LF and CRLF suffixes, not just alphabetic garbage. Leading zeros remain accepted and normalize numerically.\n'
    if f.name=='04-TESTING-AND-DEBUGGING.md':
        t+='\nRun each malformed bound through URLSearchParams constructed from an object so plus signs and newlines arrive as literal decoded values. Test the server record form separately: a repeated price bound uses only its first value, even if a later value is valid. Finally build and parse a valid state, checking that unrelated repeated campaign parameters survive serialization. These checks cover both parser branches and their shared serialization contract.\n'
    if f.name=='06-SOLUTIONS-AND-REVIEW.md':
        t+='\nFor the newline review extension, /\\D/ finds the final line terminator and rejects the bound. A repeated bound ["12px", "8"] is absent because readFirst selects the malformed first entry; the parser does not search later entries for a valid number. A missing minimum and maximum "0" produce only priceMax: 0. These answers separate omission from falsy numeric values and are asserted in the refreshed suite.\n'
    f.write_text(t,encoding='utf-8')
(P/'astraupskill/VERIFICATION.md').write_text('''# Verification and limits

Run from this project's `storefront` directory:

```text
node --experimental-strip-types --experimental-loader ./tests/alias-loader.mjs --test tests/listing-search-params.test.mjs
```

The captured Astra run passed five tests, with zero failures and skips. The tests import the actual [listing module](../storefront/src/lib/utils/listing-search-params.ts), and the local alias loader resolves its real `@/types/filters` dependency. No parser behavior is copied into the harness. Node's type stripping enables execution without claiming a complete TypeScript typecheck or application build.

The first case checks zero, leading-zero input and Number.MAX_SAFE_INTEGER on both bounds. The second covers suffixes, decimals, signs, surrounding spaces, LF and CRLF suffixes, exponent and hexadecimal notation, empty input, Infinity, and unsafe overflow. These values are looped within one test case and are not inflated into additional test counts. The third verifies server-style parameter arrays, first-value semantics, repeated options and trimmed query. The fourth exercises buildListingSearchParams and listingKey as well as the parser, retaining unrelated repeated URL parameters during a valid round trip. The fifth proves that an invalid or missing minimum does not erase a valid zero maximum.

Read [the runtime test](../storefront/tests/listing-search-params.test.mjs), [the alias loader](../storefront/tests/alias-loader.mjs), and [the exact original snapshot](snapshots/src/lib/utils/listing-search-params.ts) together. The new non-digit check prevents the final-newline loophole found during review, while safe-integer checking prevents rounding an oversized digit string into an accepted bound.

This evidence does not include native Vitest, Next rendering, a browser, Spree requests, a catalog database, authorization or webhook handling. Invalid bounds are omitted according to the existing parser shape; no visible validation error is added. Currency units, provider limits and priceMin-versus-priceMax ordering remain existing application decisions. The tests establish the local parse/serialize contract, not catalog completeness or request authorization.
''',encoding='utf-8')
s=B/'specs/7649d96533a4.json';j=json.loads(s.read_text(encoding='utf-8-sig'))
j['changedFiles']=[n for n in j['changedFiles'] if n not in ['astraupskill/evidence/results-crud-b03.json','astraupskill/evidence/astra-crud-b03-masterstore.log']]
j['summary']=['Reject malformed price bounds, including trailing line terminators and unsafe integer overflow.','Preserve valid non-negative digit bounds, server first-value semantics and URL serialization behavior.','Execute five focused tests against the real listing parser, serializer and key builder.']
s.write_text(json.dumps(j,indent=2))
