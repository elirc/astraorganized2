# buildbusinesses — fix report (B13)

Fable, 2026-09-18.

## Done
- review#3 Ticket 1 implemented end to end: src/lib/contact-filter.ts (matchContacts, clampPage), role select + derived matching in the component, two node:test cases, worked solution in 06
- review#2 write() and decimal() inlined in 02, the overpayment invariant in 03, each with file:line anchors read from the current source
- review#1 04 "Reproduce the browser evidence" with prerequisites, command, output location and duration
- review#4 02 glossary
- review#5 README parity table (old sections -> new location, or dropped); review#6 README states the no-server scope and points at server-side courses

## Skipped
- browser evidence (scripts/verify_browser.py) was not re-run: it needs Playwright Chromium and a production build; 04 documents how

## Verification
- npm test (tsx --test) via junctioned stage node_modules: 54 passed (52 delivered + 2 Ticket 1 tests); npm run typecheck exit 0 (component change compiles); eslint exit 0; junction removed

## Course/code consistency check
- Ticket 1 in 05 now has a matching worked solution in 06 that names the real helper file and the component change; 02/03 code blocks are read from the current sources by line index; README parity table built by searching the rewrite.

## Phase 3 addendum (code blocks)

The codeblocks gate found no fenced code block in chapter(s) 06. One real excerpt was added to each, quoted from this project and cited in the chapter text:

- **06** - src/lib/contact-filter.ts (matchContacts, clampPage)

No source code was changed; only the chapter Markdown.
