# grokbuildteamproject — fix report (B15)

Fable, 2026-09-18.

## Done
- review#1 03 section 2 links projectRepository.ts by name and warns that taskRepository.ts/taskService.ts are re-export shims
- review#3 02 traces one forged request (demo_member + x-org-id: maple) end to end in a table with three variations
- review#2 README prerequisites and pacing
- review#4 root README marks the Docker path unverified and VERIFICATION says so explicitly

## Skipped
- review#4 docker-compose.yml was not exercised; it is marked unverified instead

## Verification
- Documentation-only change (no code or tests touched), so no test run; edited files re-read for headings/links after the script

## Course/code consistency check
- The 403 message in the 02 table is read from tenantContext.ts; the shim files are 9 lines as stated; root README and VERIFICATION agree on the Docker path.

## Phase 3 addendum (code blocks)

The codeblocks gate found no fenced code block in chapter(s) 04, 06, 07. One real excerpt was added to each, quoted from this project and cited in the chapter text:

- **04** - backend/src/__tests__/taskRoutes.integration.test.ts (membership revocation case)
- **06** - backend/src/repositories/commentRepository.ts (versioned comment update)
- **07** - backend/src/middleware/tenantContext.ts (attachTenantContext)

No source code was changed; only the chapter Markdown.
