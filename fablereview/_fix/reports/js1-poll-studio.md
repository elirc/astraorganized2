# JS1/poll-studio — fix report (B03)

Fable, 2026-09-18.

## Done
- review#1 README prerequisites and VERIFICATION limits are specific to a browser-only app
- review#3 index.html maxlength now matches the 160-character rule in handleSubmit; 02 explains the two-layer bound
- review#4 .gitattributes normalizes line endings to LF so future diffs of app.js are readable
- review#2 exercises 1-4 with poll-specific acceptance; review#5 exercise 4 ports commit-before-publish to a fetch store (05, 06)
- 2.2 trace-lab call path section (07)
- 2.4 three concrete variations
- dependencies pinned (dev tooling only: this project has no runtime dependencies)

## Skipped
- (none)

## Verification
- npm install (pinned) -> ok
- cmd /c npm test -> # tests 3 / # pass 3 / # fail 0 (jsdom harness)
- build -> no build script
- node_modules and dist removed; package-lock.json kept

## Course/code consistency check
- 07 call-path section cites the current app.js/server.js line numbers
- 05/06 exercise criteria checked against function names
