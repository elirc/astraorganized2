const { test } = require("node:test");
const assert = require("node:assert/strict");
const http = require("node:http");
const { fixture } = require("../verification/practice-fixture.cjs");

test("the real HTTP API creates, reads, patches and deletes a profile with revision headers", async (t) => {
  const f = fixture(t);
  const { request } = await f.http();
  const created = await request("/api/profiles", {
    method: "POST",
    body: { name: "HTTP learner" },
  });
  assert.equal(created.status, 201);
  const profile = await created.json();
  assert.match(created.headers.get("etag"), /^"[a-f0-9]{64}"$/);
  const read = await request(`/api/profiles/${profile.id}`);
  assert.equal(read.status, 200);
  assert.equal((await read.json()).name, "HTTP learner");
  const update = await request(`/api/profiles/${profile.id}`, {
    method: "PATCH",
    body: { background: "Practicing HTTP" },
  });
  assert.equal(update.status, 200);
  await update.json();
  const removed = await request(`/api/profiles/${profile.id}`, {
    method: "DELETE",
    body: {},
  });
  assert.equal(removed.status, 200);
  assert.equal((await removed.json()).deleted, true);
  const missing = await request(`/api/profiles/${profile.id}`);
  assert.equal(missing.status, 404);
  await missing.json();
});
test("API reads and export require credentials; static files have restrictive headers", async (t) => {
  const f = fixture(t);
  const { url, request } = await f.http();
  for (const route of ["/api/bootstrap", "/api/export", "/api/profiles"]) {
    const denied = await fetch(url + route);
    assert.equal(denied.status, 401);
    await denied.json();
  }
  const page = await fetch(url);
  assert.equal(page.status, 200);
  assert.match(await page.text(), /Practice Journal/);
  assert.match(
    page.headers.get("content-security-policy"),
    /frame-ancestors 'none'/,
  );
  assert.equal(page.headers.get("x-content-type-options"), "nosniff");
  const exported = await request("/api/export");
  assert.equal(exported.status, 200);
  const data = await exported.json();
  assert.equal(data.auth, undefined);
  assert.ok(!JSON.stringify(data).includes(f.token));
  assert.match(exported.headers.get("content-disposition"), /attachment/);
});
test("missing and stale If-Match values do not mutate accepted state", async (t) => {
  const f = fixture(t);
  const { request } = await f.http();
  const old = f.revision();
  let response = await request("/api/profiles", {
    method: "POST",
    body: { name: "Missing revision" },
    headers: { "If-Match": "" },
  });
  assert.equal(response.status, 428);
  await response.json();
  f.create("profiles", { name: "Accepted elsewhere" });
  response = await request("/api/profiles", {
    method: "POST",
    body: { name: "Stale" },
    headers: { "If-Match": `"${old}"` },
  });
  assert.equal(response.status, 409);
  await response.json();
  assert.deepEqual(
    f.service.read().value.profiles.map((item) => item.name),
    ["Accepted elsewhere"],
  );
});
test("cross-origin requests and unexpected Host headers are refused", async (t) => {
  const f = fixture(t);
  const { request, url } = await f.http();
  const response = await request("/api/profiles", {
    method: "POST",
    body: { name: "Blocked" },
    headers: { Origin: "https://unrelated.example" },
  });
  assert.equal(response.status, 403);
  await response.json();
  const status = await new Promise((resolve, reject) => {
    const request = http.get(
      url,
      { headers: { Host: "unrelated.example" } },
      (response) => {
        response.resume();
        response.on("end", () => resolve(response.statusCode));
      },
    );
    request.on("error", reject);
  });
  assert.equal(status, 400);
  assert.equal(f.service.read().value.profiles.length, 0);
});
test("actual chunked body size is bounded without trusting Content-Length", async (t) => {
  const f = fixture(t);
  const { url } = await f.http();
  const status = await new Promise((resolve, reject) => {
    const request = http.request(
      url + "/api/profiles",
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${f.token}`,
          "Content-Type": "application/json",
          "If-Match": `"${f.revision()}"`,
          "Transfer-Encoding": "chunked",
        },
      },
      (response) => {
        response.resume();
        response.on("end", () => resolve(response.statusCode));
      },
    );
    request.on("error", reject);
    request.write('{"name":"');
    request.write("x".repeat(140000));
    request.end('"}');
  });
  assert.equal(status, 413);
  assert.equal(f.service.read().value.profiles.length, 0);
});
test("malformed JSON, reserved properties, wrong media types and unknown routes are explicit errors", async (t) => {
  const f = fixture(t);
  const { url, request } = await f.http();
  for (const raw of ["{bad", "[]", '{"__proto__":{}}']) {
    const response = await fetch(url + "/api/profiles", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${f.token}`,
        "Content-Type": "application/json",
        "If-Match": `"${f.revision()}"`,
      },
      body: raw,
    });
    assert.equal(response.status, 400);
    await response.json();
  }
  let response = await request("/api/profiles", {
    method: "POST",
    body: {},
    headers: { "Content-Type": "text/plain" },
  });
  assert.equal(response.status, 415);
  await response.json();
  response = await request("/api/unknown");
  assert.equal(response.status, 404);
  await response.json();
});
test("storage failures return generic HTTP errors without claiming a successful mutation", async (t) => {
  let fail = false;
  const fs = require("node:fs");
  const fsImpl = Object.create(fs);
  fsImpl.renameSync = (...args) => {
    if (fail) throw new Error("PRIVATE INTERNAL ERROR");
    return fs.renameSync(...args);
  };
  const f = fixture(t, { fsImpl });
  const { request } = await f.http();
  fail = true;
  const response = await request("/api/profiles", {
    method: "POST",
    body: { name: "Not accepted" },
  });
  assert.equal(response.status, 500);
  assert.ok(!(await response.text()).includes("PRIVATE INTERNAL ERROR"));
  assert.equal(f.service.read().value.profiles.length, 0);
});
