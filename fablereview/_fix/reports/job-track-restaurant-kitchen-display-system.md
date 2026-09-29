# _Organized Desktop/08 App And Product Projects/job track/restaurant-kitchen-display-system — fix report (B17)

Fable, 2026-09-18.

## Done
- review#1 .nvmrc, engines, POSIX blocks in README and 04; review#3 UTF-8 BOM stripped from 9 files; review#4 README states port 5177 and the URL literally; review#5 README prerequisites
- review#2 02 "The check that is outside the transaction" quotes api.js:188 and asks for the interleaving; 05 exercise 7 implements the updated_at compare-and-set

## Skipped
- (none)

## Verification
- Documentation, .nvmrc and package.json engines only (no code changed); the api.js excerpt in 02 was read from the file at the line the section cites; BOM absence verified by the strip routine

## Course/code consistency check
- README port and URL match client/package.json (vite --port 5177); 05 exercise 7 and the 02 section describe the same compare-and-set.

## Phase 3 addendum (code blocks)

Each chapter below had no fenced code block and now carries one short section with a real excerpt from this project:

- `03-WORKED-CHANGE.md` — quoted from `server/src/lib/validation.js:22-26` (`listOrdersSchema`)
- `06-SOLUTIONS-AND-REVIEW.md` — quoted from `server/test/kds.test.cjs:92-107` (global 86 case)
