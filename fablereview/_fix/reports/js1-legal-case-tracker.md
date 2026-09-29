# JS1/legal-case-tracker — fix report (B06)

Fable, 2026-09-17.

## Done
- review#2 / 2.2 six distinct trace-lab boundaries (07)
- review#3 / 2.3 per-exercise review criteria (06)
- 2.4 excerpt now shows changed lines
- 2.4 three concrete variations
- 2.5 ownership/authz exercise 7 with reference code and test (05, 06)
- review#6 harness description (04)
- review#4 / 2.7 dependencies pinned (react 18.3.1, vite 8.2.2 (the versions Astra verified with), express 4.22.2, cors 2.8.6, plugin-react 5.1.2, concurrently 9.2.1)
- review#5: kept `node --test test/*.test.js` after confirming Node 22 expands the glob itself under cmd.exe (a bare directory argument is NOT accepted by Node 22.16); README already explains this
- 1.3 fractional-cent claim corrected in 02, 03, 07 (Fable, scripted pass)
- package-lock.json generated from the pinned install

## Skipped
- review#1 alternative (implement the cent check) not taken: the course now states the real behavior; rounding is exercise material

## Verification
- npm install (pinned) -> added 165 packages
- cmd /c npm test -> # tests 3 / # pass 3 / # fail 0 (Node 22.16.0)
- npm run build -> vite built in 2.42s
- node_modules and dist removed afterwards; package-lock.json kept

## Course/code consistency check
- 03 excerpt re-read against server/server.js lines 290-303, 147, 349
- 07 boundaries cite App.jsx 88/120, api.js, server.js 50/97/151/290/349
- 06 reviews and 05/06 exercise 7 checked against route names and test helper signature
