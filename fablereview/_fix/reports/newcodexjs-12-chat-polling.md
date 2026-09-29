# newcodexJS/12-chat-polling — fix report (B07)

Fable, 2026-09-17.

## Done
- review#1 / P4: the membership guard now validates messageId before the lookup; POST /conversations/:id/read with {} is 400 (test added)
- review#3 02-CONCEPTS explains path-regex dispatch vs per-route middleware
- review#2 / 2.2 six distinct trace-lab boundaries (07)
- 2.3 per-exercise review criteria (06)
- 2.4 excerpt shows the changed guard
- 2.4 three concrete variations
- review#4 exercise 7: TOCTOU window made observable with a test hook (05, 06)
- review#5 exercise 8: cursor and unread-count arithmetic (05, 06)
- review#5 chat-specific debugging section (04)
- root package renamed from astra-crud-workspace-63; pg and tsx declared at the root

## Skipped
- (none)

## Verification
- npm install (workspaces) -> added 247 packages
- cmd /c npm test with ASTRA_TEST_DATABASE_URL -> # tests 4 / # pass 4 / # fail 0 (3 delivered + read-receipt 400 test)
- npm run build -> built in 14.04s
- node_modules and dist removed; root package-lock.json kept

## Course/code consistency check
- 03 excerpt re-read against routes/chatRoutes.ts guard (18-62)
- 07 boundaries cite App.tsx 10/73/75, services/api.ts 38, chatRoutes.ts 18, chatController.ts 178, chatModel.ts 117/224, utils/http.ts, middleware/errors.ts
- 02 guard section and exercise 7 hook match the current guard code
