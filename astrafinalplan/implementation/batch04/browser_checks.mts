import { chromium } from "playwright";
import {
  readFile,
  writeFile,
  stat,
  readdir,
  mkdtemp,
  rm,
} from "node:fs/promises";
import { createServer } from "node:http";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { createRequire } from "node:module";
import assert from "node:assert/strict";
const B = path.dirname(fileURLToPath(import.meta.url));
const domains = [
  ...JSON.parse(await readFile(path.join(B, "domain-specs.json"), "utf8")),
  ...JSON.parse(
    await readFile(path.join(B, "memory-domain-specs.json"), "utf8"),
  ),
];
const simple = JSON.parse(
  await readFile(path.join(B, "simple-specs.json"), "utf8"),
);
process.env.ASTRA_TEST_DATABASE_URL =
  "postgres://astra:local-test@127.0.0.1:55439/astra_test_ten";
async function serve(root: string) {
  const server = createServer(async (req, res) => {
    try {
      let file = path.resolve(
        root,
        "." + decodeURIComponent(new URL(req.url!, "http://local").pathname),
      );
      if (file !== root && !file.startsWith(root + path.sep)) {
        res.writeHead(403).end();
        return;
      }
      try {
        if ((await stat(file)).isDirectory())
          file = path.join(file, "index.html");
      } catch {
        file = path.join(root, "index.html");
      }
      res.setHeader(
        "Content-Type",
        (
          {
            ".html": "text/html",
            ".js": "text/javascript",
            ".css": "text/css",
            ".svg": "image/svg+xml",
            ".webmanifest": "application/manifest+json",
          } as any
        )[path.extname(file)] || "application/octet-stream",
      );
      res.end(await readFile(file));
    } catch {
      res.writeHead(404).end();
    }
  });
  await new Promise<void>((r) => server.listen(0, "127.0.0.1", r));
  return {
    url: "http://127.0.0.1:" + (server.address() as any).port,
    close: () =>
      new Promise<void>((r) => {
        server.close(() => r());
        server.closeAllConnections();
      }),
  };
}
async function hostFor(n: number, root: string) {
  if (n === 73 || n === 74) return null;
  if (n === 51 || n === 56)
    return (
      await import(pathToFileURL(path.join(root, "test/http.js")).href)
    ).application();
  if (n <= 71) {
    const host = await (
      await import(pathToFileURL(path.join(root, "test/database.ts")).href)
    ).database();
    try {
      if (n >= 58) {
        for (const file of (await readdir(path.join(root, "server/db/seeds")))
          .filter((f) => f.endsWith(".ts"))
          .sort()) {
          const mod = await import(
            pathToFileURL(path.join(root, "server/db/seeds", file)).href
          );
          await (mod.seed ?? mod.default.seed)(host.db);
        }
      }
      return host;
    } catch (error) {
      await host.close();
      throw error;
    }
  }
  const directory = await mkdtemp(
    path.join(tmpdir(), "astra-browser-" + n + "-"),
  );
  let db: any, app: any;
  if (n === 72) {
    process.env.RECIPE_LAB_DATA = directory;
    db = (await import(pathToFileURL(path.join(root, "server/db.ts")).href)).db;
    app = (await import(pathToFileURL(path.join(root, "server/index.ts")).href))
      .app;
  } else {
    process.env.JOB_TRACK_DATA_DIR = directory;
    process.env.JWT_SECRET = "isolated-browser-fixture-secret";
    const req = createRequire(path.join(root, "server/package.json"));
    app = req("./src/server.js").app;
    db = req("./src/db.js");
  }
  const server = app.listen(0, "127.0.0.1");
  await new Promise<void>((r) => server.once("listening", r));
  return {
    origin: "http://127.0.0.1:" + server.address().port,
    async close() {
      await new Promise<void>((r) => {
        server.close(() => r());
        server.closeAllConnections();
      });
      db.close();
      await rm(directory, { recursive: true, force: true });
    },
  };
}
async function eventually(fn: () => Promise<void>) {
  let last;
  for (let i = 0; i < 50; i++) {
    try {
      await fn();
      return;
    } catch (e) {
      last = e;
      await new Promise((r) => setTimeout(r, 100));
    }
  }
  throw last;
}
const browser = await chromium.launch({
  headless: true,
  executablePath:
    "C:/Users/Owner/AppData/Local/ms-playwright/chromium-1243/chrome-win64/chrome.exe",
});
const selected = new Set(process.argv.slice(2));
try {
  for (let n = 51; n <= 75; n++) {
    if (selected.size && !selected.has(String(n))) continue;
    let host: any, web: any, context: any, page: any;
    const errors: string[] = [],
      calls: any[] = [];
    let closing = false;
    let result: any;
    try {
      const root = path.join(B, "stage", String(n));
      console.log("START", n);
      host = await hostFor(n, root);
      console.log("HOST", n);
      web = await serve(
        path.join(
          root,
          n <= 71
            ? "client/dist"
            : n === 75
              ? "client/dist"
              : n === 72
                ? "dist/web"
                : "dist",
        ),
      );
      console.log("WEB", n);
      context = await browser.newContext({
        viewport: { width: 1280, height: 1000 },
        timezoneId: "America/Los_Angeles",
        serviceWorkers: "block",
      });
      console.log("CONTEXT", n);
      page = await context.newPage();
      console.log("PAGE", n);
      page.setDefaultTimeout(12000);
      page.on("pageerror", (e: any) => errors.push(e.message));
      await page.route("**/*", async (route: any) => {
        const url = new URL(route.request().url());
        if (
          host &&
          url.pathname.startsWith("/api/") &&
          ["localhost", "127.0.0.1"].includes(url.hostname)
        ) {
          try {
            const response = await route.fetch({
              url: host.origin + url.pathname + url.search,
            });
            calls.push({
              method: route.request().method(),
              path: url.pathname,
              status: response.status(),
            });
            return route.fulfill({
              response,
              headers: {
                ...response.headers(),
                "access-control-allow-origin": web.url,
                "access-control-allow-credentials": "true",
              },
            });
          } catch (e) {
            if (!closing) errors.push(String(e));
            return route.abort().catch(() => {});
          }
        }
        if (route.request().url().startsWith(web.url)) return route.continue();
        return route.abort();
      });
      if (n === 57)
        await page.addInitScript(
          ({ origin }: any) => {
            const Original = window.WebSocket;
            window.WebSocket = class extends Original {
              constructor(url: string | URL, protocols?: string | string[]) {
                super(
                  String(url).replace("ws://localhost:4115", origin),
                  protocols,
                );
              }
            };
          },
          { origin: host.origin.replace("http", "ws") },
        );
      const api = async (p: string, method = "GET", body?: unknown) => {
        const r = await fetch(host.origin + p, {
          method,
          headers: { "Content-Type": "application/json" },
          body: body === undefined ? undefined : JSON.stringify(body),
        });
        return {
          status: r.status,
          data: r.status === 204 ? null : await r.json(),
        };
      };
      const d = domains.find((d: any) => Number(d.stage) === n),
        s = simple.find((s: any) => Number(s.stage) === n);
      if (d) {
        const made = await api(d.route, "POST", {
          title: "Browser lesson",
          owner: "Junior Learner",
          category: d.categories[0],
          status: d.statuses[0],
          priority: "Medium",
          amount: 12.5,
          dueDate: "2028-02-29",
          notes: "Trace this fixture",
        });
        assert.equal(made.status, 201);
        await page.goto(web.url);
        console.log("LOADED", n);
        const card = page
          .locator("article")
          .filter({
            has: page.getByRole("heading", {
              name: "Browser lesson",
              exact: true,
            }),
          });
        await card.getByRole("button", { name: "Edit", exact: true }).click();
        await page.locator("#lesson-field-1").fill("Browser revised");
        await page
          .locator("form")
          .first()
          .getByRole("button", { name: "Update", exact: true })
          .click();
        await page
          .getByRole("heading", { name: "Browser revised", exact: true })
          .waitFor();
        assert.equal(
          (await api(d.route + "/" + made.data.id)).data.title,
          "Browser revised",
        );
      } else if (s) {
        await page.goto(web.url);
        console.log("LOADED", n);
        for (const [key, value] of Object.entries(s.valid))
          await page
            .getByLabel(key, { exact: true })
            .fill(Array.isArray(value) ? value.join(", ") : String(value));
        await page
          .getByLabel(s.fields[0], { exact: true })
          .fill("Browser lesson");
        await page.getByRole("button", { name: "Create", exact: true }).click();
        const card = page
          .locator("article")
          .filter({ hasText: "Browser lesson" });
        await card.getByRole("button", { name: "Edit", exact: true }).click();
        await page
          .getByLabel(s.fields[0], { exact: true })
          .fill("Discarded draft");
        await page.getByRole("button", { name: "Cancel", exact: true }).click();
        await page
          .getByRole("heading", { name: "Browser lesson", exact: true })
          .waitFor();
        await card.getByRole("button", { name: "Edit", exact: true }).click();
        await page
          .getByLabel(s.fields[0], { exact: true })
          .fill("Browser revised");
        await page.getByRole("button", { name: "Update", exact: true }).click();
        await page
          .getByRole("heading", { name: "Browser revised", exact: true })
          .waitFor();
      } else if (n >= 67 && n <= 71) {
        await page.goto(web.url);
        console.log("LOADED", n);
        const card = page
          .locator("article")
          .filter({
            has: page.getByRole("button", { name: "Archive", exact: true }),
          })
          .first();
        await card.waitFor();
        const title = await card.locator("h3").innerText();
        await card
          .getByRole("button", { name: "Archive", exact: true })
          .click();
        await page.getByLabel("Include archived").check();
        const archived = page
          .locator("article")
          .filter({
            has: page.getByRole("heading", { name: title, exact: true }),
          });
        await archived
          .getByRole("button", { name: "Restore", exact: true })
          .click();
        await archived
          .getByRole("button", { name: "Archive", exact: true })
          .waitFor();
      } else if (n === 56) {
        await page.goto(web.url);
        console.log("LOADED", n);
        await page
          .getByRole("button", { name: "Register", exact: true })
          .click();
        await page
          .getByLabel("Email", { exact: true })
          .fill("browser@example.com");
        await page.getByLabel("Password", { exact: true }).fill("learning123");
        await page
          .getByRole("button", { name: "Register", exact: true })
          .click();
        await page.getByLabel("Title", { exact: true }).fill("Browser note");
        await page
          .getByLabel("Body", { exact: true })
          .fill("Owner-scoped CRUD");
        await page
          .getByRole("button", { name: "Add note", exact: true })
          .click();
        await page
          .getByRole("heading", { name: "Browser note", exact: true })
          .waitFor();
        await page
          .getByRole("button", { name: "Log out", exact: true })
          .click();
        await page
          .getByRole("button", { name: "Sign in", exact: true })
          .waitFor();
      } else if (n === 55) {
        await page.goto(web.url);
        console.log("LOADED", n);
        await page
          .getByRole("button", { name: "Record movement", exact: true })
          .waitFor();
        await eventually(async () =>
          assert.notEqual(
            await page.locator("#lesson-field-1").inputValue(),
            "",
            "product selection must load",
          ),
        );
        await page.locator("#lesson-field-4").fill("2");
        await page.locator("#lesson-field-5").fill("Browser receipt");
        await page
          .getByRole("button", { name: "Record movement", exact: true })
          .click();
        await eventually(async () =>
          assert.equal(
            calls.some((c) => c.method === "POST" && c.status === 201),
            true,
            "movement must be created",
          ),
        );
      } else if (n === 57) {
        await page.goto(web.url);
        console.log("LOADED", n);
        await page.getByPlaceholder(/^Message #/).fill("Browser live message");
        await eventually(async () =>
          assert.equal(
            await page
              .getByRole("button", { name: "Send", exact: true })
              .isEnabled(),
            true,
          ),
        );
        await page.getByRole("button", { name: "Send", exact: true }).click();
        await page.getByText("Browser live message", { exact: true }).waitFor();
      } else if (n === 62) {
        await page.goto(web.url);
        console.log("LOADED", n);
        await page
          .getByPlaceholder("Customer onboarding feedback")
          .fill("Browser survey");
        await page.getByRole("button", { name: "Create", exact: true }).click();
        const card = page
          .locator("article")
          .filter({
            has: page.getByRole("heading", {
              name: "Browser survey",
              exact: true,
            }),
          });
        await card.getByRole("link", { name: "Builder", exact: true }).click();
        await page.locator("h1").waitFor();
      } else if (n === 73) {
        await page.goto(web.url);
        console.log("LOADED", n);
        await page.getByRole("link", { name: "Settings", exact: true }).click();
        await page
          .locator("input[type=file]")
          .setInputFiles({
            name: "invalid.json",
            mimeType: "application/json",
            buffer: Buffer.from(
              JSON.stringify({
                app: "questboard",
                version: 1,
                events: [null],
                applications: [],
                categories: [{ id: "a" }],
                settings: {},
              }),
            ),
          });
        await page.getByText("Import failed", { exact: true }).waitFor();
      } else if (n === 74) {
        await page.goto(web.url);
        console.log("LOADED", n);
        await page
          .getByRole("button", { name: "Settings", exact: true })
          .click();
        await page
          .locator("input[type=file]")
          .setInputFiles({
            name: "invalid.json",
            mimeType: "application/json",
            buffer: Buffer.from('{"schemaVersion":1}'),
          });
        await page.getByText(/Malformed backup/).waitFor();
      } else if (n === 75) {
        await page.goto(web.url + "/register");
        await page.locator("input[name=name]").fill("Browser Learner");
        await page.locator("input[name=email]").fill("browser@example.com");
        await page.locator("input[name=password]").fill("learning123");
        await page.locator("input[name=confirmPassword]").fill("learning123");
        await page.locator("button[type=submit]").click();
        await eventually(async () =>
          assert.equal(
            calls.some(
              (c) => c.path === "/api/auth/register" && c.status === 201,
            ), true, "registration must succeed",
          ),
        );
      } else {
        await page.goto(web.url);
        console.log("LOADED", n);
        await eventually(async () => {
          assert.equal(
            (await page.locator("body").innerText()).length > 100,
            true,
            "page content must load",
          );
          assert.equal(
            calls.some((c) => c.status === 200),
            true,
            "API must respond",
          );
        });
        const input = page
          .locator("input[placeholder*=Search],input[type=search]")
          .first();
        if (await input.count()) {
          await input.fill("Browser");
          await input.fill("");
        } else {
          const link = page
            .locator("a[href]")
            .filter({ hasText: /Cart|Environment|Provider|Dish/ })
            .first();
          if (await link.count()) await link.click();
        }
      }
      await eventually(async () =>
        assert.equal(
          await page
            .locator("body")
            .innerText()
            .then((t: string) => t.includes("Loading...") && t.length < 50),
          false,
        ),
      );
      assert.deepEqual(errors, []);
      if (host) assert.ok(calls.length > 0);
      await page.screenshot({
        path: path.join(B, "logs", n + "-browser.png"),
        fullPage: true,
      });
      await page.setViewportSize({ width: 390, height: 844 });
      await page.screenshot({
        path: path.join(B, "logs", n + "-mobile.png"),
        fullPage: true,
      });
      const width = await page.evaluate(() => ({
        content: document.documentElement.scrollWidth,
        viewport: innerWidth,
      }));
      result = {
        project: String(n),
        check: "browser",
        passed: true,
        api: host ? "actual isolated HTTP server" : "none; browser storage",
        seed_smoke: n >= 58 && n <= 71 ? "passed" : null,
        api_requests: calls.length,
        responsive: width,
      };
    } catch (error: any) {
      console.log("FAIL", n, String(error));
      if (page)
        await page
          .screenshot({
            path: path.join(B, "logs", n + "-browser-failure.png"),
            fullPage: true,
          })
          .catch(() => {});
      result = {
        project: String(n),
        check: "browser",
        passed: false,
        error: String(error.stack || error),
        page_errors: errors,
        body: page
          ? await page
              .locator("body")
              .innerText()
              .catch(() => "")
          : "",
      };
    } finally {
      console.log("CLOSE", n);
      closing = true;
      if (page) await page.unrouteAll({ behavior: "ignoreErrors" });
      if (context) await context.close();
      if (web) await web.close();
      if (host) await host.close();
    }
    console.log(JSON.stringify(result));
    const file = path.join(B, "browser-checks.json");
    let prior = [];
    try {
      prior = JSON.parse(await readFile(file, "utf8"));
    } catch {}
    await writeFile(
      file,
      JSON.stringify(
        [...prior.filter((r: any) => r.project !== String(n)), result],
        null,
        2,
      ),
    );
  }
} finally {
  await browser.close();
}
