# Astra source plan: .netvg workforce quote app

Canonical `_Organized Desktop/01 Net Workspaces/.netvg`; ID `9e7b2d32e0fb`. Not staged/assigned yet. Root inspected HiringQuoteCalculator/DTO/controller, Money, in-memory read model, QuoteBuilder, workforceApi and two existing quote tests. Confirm all project/ancestor instructions before staging. This is a C#/React educational workforce dashboard with a calculated quote endpoint, not payroll persistence.

## Concrete improvement

`workforceApi.createQuote` catches every backend rejection and computes a successful synthetic quote. It therefore turns the API's intentional Japan/Contractor rejection into success, and also masks outages. Remove automatic quote success fallback; preserve the separately labeled dashboard mock fallback. Surface typed/readable ProblemDetails or safe network failures in QuoteBuilder, clear or explicitly mark stale quotes while inputs/new submissions change, handle loading/failure/retry accessibly, and prevent an older response replacing the latest request. Do not present calculated mock data as a server-confirmed quote.

At the service boundary validate null/blank/trimmed country and currency, defined EmploymentType enum, positive decimal compensation and overflow/precision cases before arithmetic. Current switch fallbacks accept undefined enums; total arithmetic can overflow decimal. Define a simple documented demo currency contract without implying real currency conversion; preserve supported existing EUR/USD examples if compatible. Fee/rate constants and country data are synthetic teaching inputs, not researched employment or financial facts. Clone returned requirements if the mutable shared read model list would otherwise escape.

## Evidence and course

Keep existing quote/dashboard tests and add undefined enum, unsupported country/type, blank/null/case normalization, zero/negative/max-decimal values, deterministic rounding and successful exact totals. Exercise actual controller 400 mapping and frontend fetch/QuoteBuilder rejected quote, outage, retry and stale response behavior. A backend 400 must never yield a successful frontend result. Use mocked fetch or an isolated test server; no live payroll or external provider.

Run the actual target .NET tests/build and frontend finite tests/TypeScript/Vite build, recording .NET 10 roll-forward explicitly if native target runtime is absent. No suppressions or invented native-runtime pass. Nine detailed guides (~4,000 words), exact snapshots and matched examples should trace form→client→controller→calculator→Result→ProblemDetails→visible UI, explain business rejection versus infrastructure failure, decimal arithmetic and async state. Include a proposed future saved-quote CRUD extension with versioned edits and audit records but label it future work, not delivered persistence. State no real payroll/compliance validation or database writes were performed.
