# Aral dependency restore attempt

Status: not a passing check.

Two staged `npm ci` attempts on 2026-09-19 were stopped after they ceased making progress. The first logged repeated registry tarball `ECONNRESET` failures; the second used bounded retries and two sockets but did not progress beyond dependency extraction. No lifecycle hook output appeared and no test/typecheck result was produced. The install slot was then released for another project.

Raw npm debug logs remain at:

- `npm-cache/_logs/2026-09-19T21_04_04_925Z-debug-0.log`
- `npm-cache/_logs/2026-09-19T21_09_29_279Z-debug-0.log`

Aral still requires a successful clean install followed by workspace tests and strict type checking.
