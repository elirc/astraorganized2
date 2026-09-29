# newcodexJS/07-blog-platform — fix report (B06)

Fable, 2026-09-17.

## Done
- review#3 client test suite: client/src/App.test.tsx (Vitest + Testing Library, jsdom) proves the stale-search guard and the double-submit guard; `npm test --workspace client`
- review#4 root package renamed from astra-crud-workspace-58 to blog-platform-workspace; root `npm test` runs server then client suites; pg and tsx declared at the root so test/database.ts does not rely on hoisting
- review#5 kept `tsx --test ../test/*.test.ts`: Node 22 expands the glob itself, so it works under cmd.exe (a bare directory is rejected by Node 22.16); VERIFICATION notes where the recorded evidence came from
- review#2 / 2.2 six distinct trace-lab boundaries (07)
- 2.3 per-exercise review criteria (06)
- 2.4 excerpt shows the changed service and model lines
- 2.4 three concrete variations
- 2.5 ownership/authz exercise 7 (05, 06)
- review#6 harness walkthrough (04)
- review#6 01-CODEBASE-MAP warns about unused scaffold dependencies

## Skipped
- review#1 (drop 08/09 courses) handled by the clone banners (sweep 2.10)

## Verification
- npm install (workspaces, pinned root devDeps) -> added 399 packages
- cmd /c npm run test --workspace server with ASTRA_TEST_DATABASE_URL -> # tests 4 / # pass 4 / # fail 0
- cmd /c npm run test --workspace client -> Test Files 1 passed, Tests 2 passed (stale-search guard, double-submit guard)
- npm run build (tsc -b && vite build for client; tsc for server) -> built in 13.36s
- node_modules and dist removed; root package-lock.json kept

## Course/code consistency check
- 03 excerpt re-read against services/service.ts 22-35 and models/model.ts 4-17, 58-62
- 07 boundaries cite App.tsx 30/47/72, services/api.ts, routes.ts, service.ts 17/22, model.ts 4/31/58, migration 001, response.ts, errorMiddleware.ts
- 01 scaffold-leftover list checked against both package.json files
