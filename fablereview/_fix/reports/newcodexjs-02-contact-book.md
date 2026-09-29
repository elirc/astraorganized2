# newcodexJS/02-contact-book — fix report (B01)

Fable, 2026-09-18.

## Done
- review#3/#5 04 "Run the checks" rewritten: no circular pointer, Docker fallback, CREATE SCHEMA privilege named
- review#1 HTTP-level test for POST /api/contacts/import (200 with imported count; 400 for a malformed CSV with no rows saved)
- review#2 03 performance note; exercise 8 batched import with the rollback test as acceptance (05, 06)
- review#4 three concrete CSV variations
- 2.2 trace-lab call path section (07)
- 2.3 per-exercise review criteria (06)
- 2.5 ownership/authz exercise 7 (05, 06)

## Skipped
- (none)

## Verification
- npm install (server) -> added 111 packages
- cmd /c npm test with ASTRA_TEST_DATABASE_URL -> # tests 5 / # pass 5 / # fail 0 (4 delivered + HTTP import test)
- server/node_modules removed

## Course/code consistency check
- 07 call-path section cites contactRoutes.js 12, contactController.js 49, contactService.js 124, contactModel.js 160, utils/csv.js
- 03 performance note line references checked against contactModel.js 160-176
