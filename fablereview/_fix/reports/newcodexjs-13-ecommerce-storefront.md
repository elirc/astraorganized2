# newcodexJS/13-ecommerce-storefront — fix report (B07)

Fable, 2026-09-17.

## Done
- review#2 02-CONCEPTS lock-order box with the A/B deadlock sketch
- review#3 03 explains why removeCartItem and mergeCart do not take the product lock
- review#1 / 2.2 six distinct trace-lab boundaries (07)
- review#4 / 2.3 per-exercise review criteria (06)
- 2.4 excerpt shows the changed cart and checkout transactions
- 2.4 three concrete variations
- 2.5 ownership/authz exercise 7 (05, 06)
- review#5 VERIFICATION states honestly what the browser check covered
- root package renamed from astra-crud-workspace-64; pg and tsx declared at the root

## Skipped
- (none)

## Verification
- npm install (workspaces) -> added 247 packages
- cmd /c npm test with ASTRA_TEST_DATABASE_URL -> # tests 3 / # pass 3 / # fail 0
- npm run build -> built in 12.15s
- node_modules and dist removed; root package-lock.json kept

## Course/code consistency check
- 03 excerpt re-read against services/storeService.ts changeCartQuantity (42) and checkout (134)
- 07 boundaries cite services/api.ts 46, storeRoutes.ts, storeService.ts 42/134, utils/http.ts
- 02 lock-order table matches orderBy("id").forUpdate() at storeService.ts:151
