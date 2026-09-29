# calendar+jobtrack — fix report (B08)

Fable, 2026-09-17.

## Done
- review#3 02 paragraph on the strict version check (forward vs backward compatibility, migrateBackup shape); new test for version 0
- review#4 exercise 7: categoryId referential check with policy trade-off and reference test (05, 06)
- review#5 / 2.2 six distinct trace-lab boundaries (07)
- 2.3 per-exercise review criteria (06)
- 2.4 excerpt shows parseBackup
- 2.4 three concrete variations
- review#2 src/lib/backup.ts, backupValidation.ts and backup.test.ts reformatted to the repository's single-quote, no-semicolon style with Prettier
- review#1 VERIFICATION already states 2 delivered vs 92 inherited after the sweep; now 93 with the version-0 test

## Skipped
- (none)

## Verification
- npx prettier@3 --single-quote --no-semi on the three touched files
- npm ci -> added 183 packages
- cmd /c npm test (vitest) -> Test Files 8 passed, Tests 93 passed (92 inherited + version-0 test)
- npm run typecheck -> clean
- node_modules and dist removed

## Course/code consistency check
- 03 excerpt re-cut from src/lib/backup.ts after formatting
- 07 boundaries cite SettingsPage.tsx 53, backup.ts 44/61, backupValidation.ts 4/63, store/*.ts replaceAll
