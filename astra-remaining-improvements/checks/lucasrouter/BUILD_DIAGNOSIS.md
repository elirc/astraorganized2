# Build diagnosis

The first captured default Next 16.3.1 build failed in Turbopack's PostCSS transform because an extended Windows path under the staged pnpm dependency tree was treated as outside the root. `build-final-01.json` and `.log` contain the terminal failure.

The documented Webpack option compiled the application, then failed TypeScript on `deliveryValidation.ts:40`. It also reported an invalid generated arbitrary-width utility containing control characters. Compilation took 9.3 minutes. These are observed outcomes; the warning alone does not identify the original file that supplied that token.

The validator narrowing was corrected by the implementation worker. Root then scoped Tailwind's source discovery to `src`, using `source("../")` in `src/app/globals.css`. The intent is to exclude documentation snapshots and dependency artifacts from class discovery. Build and browser checks must establish the resulting behavior; no speedup or successful default build is presumed.

Sources read before the CSS edit: the installed Next 16.3.1 `01-app/01-getting-started/11-css.md` guide, and [Tailwind's source detection documentation](https://tailwindcss.com/docs/detecting-classes-in-source-files#setting-your-base-path). Installed Tailwind is 4.3.3. The source option is relative to the stylesheet, so `../` from `src/app` selects `src`.
