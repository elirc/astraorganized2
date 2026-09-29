# zz8 dependency repair verification — 2026-09-13

- Preserved original lock snapshot: `package-lock.original-20260913.json`, SHA-256 `76FDB0C4D93600FC989E45CF8DBB48193FA77DAF27BBE1E0BAF74AB328CF3AC3`.
- Stage-only lock repair added `version: "0.27.7"` to exactly 25 nested optional `@esbuild/*` package entries under `node_modules/esbuild`; package.json and source were unchanged. The repaired stage lock has zero missing optional versions.
- `checks/332058fd8671/setup-install-repaired.json`: `npm ci --ignore-scripts --no-audit --no-fund`, stage cwd, exit 0, 784.92 seconds.
- `checks/332058fd8671/setup-verify-npm-ls.json`: `npm ls --depth=0 --json`, stage cwd, exit 0. Declared direct versions resolve, including `esbuild` 0.27.7 as the transitive package. npm reports four extraneous `@emnapi/*`/`@tybys/wasm-util` packages left by the native optional dependency tree; this is non-fatal but should be cleaned only by a later isolated reinstall if needed.
- `checks/332058fd8671/setup-verify-esbuild-native.json`: native smoke passed from stage cwd using the real `node.exe`: `require('esbuild').version === "0.27.7"`; win32/x64 binary transformed `const x: number = 1` with the TypeScript loader successfully. Node v22.16.0, npm 10.9.2. The earlier `node.cmd` launch-failure record is preserved as `setup-verify-esbuild.json` and reflects only an invalid executable name, not a package failure.

This is setup evidence only; no canonical, database, source, or package declaration was changed.
