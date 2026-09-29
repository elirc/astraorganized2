# newcodexJS/03-expense-tracker — fix report (B01)

Fable, 2026-09-18.

## Done
- review#1 amount validation split into four messages (finite, > 0, two decimals, upper bound); test asserts each
- review#2 exercise 7: half-open vs inclusive agreement test with the fix (05, 06)
- review#3 06 worked solution for integer cents (exercise 4), code left unchanged so the existing tests stay the contract
- review#4/#6 04 "Run the checks" rewritten with the Docker fallback and privilege note
- review#5 three concrete variations
- 2.2 trace-lab call path section (07)
- 2.3 per-exercise review criteria (06)
- new test goes through createExpense (parseExpense is private) and asserts no rows were written

## Skipped
- (none)

## Verification
- npm install (server) -> added 111 packages
- cmd /c npm test with ASTRA_TEST_DATABASE_URL -> # tests 4 / # pass 4 / # fail 0 (3 delivered + per-rule message test)
- server/node_modules removed

## Course/code consistency check
- expenseService.js 12-17 re-read after the split; 07 call-path cites expenseModel.js 166 and reports.test.cjs seed
- 06 worked cents solution matches the ::float cast at expenseModel.js:170
