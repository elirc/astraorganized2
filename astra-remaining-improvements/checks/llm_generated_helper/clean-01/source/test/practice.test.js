const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const { fixture } = require("../verification/practice-fixture.cjs");
const { authenticate, bootstrap } = require("../src/practice/domain");

function scenario(t) {
  const f = fixture(t);
  const profile = f.create("profiles", {
    name: "Junior CRUD developer",
    targetRole: "Software engineer",
  });
  const question = f.create("questions", {
    title: "Stale edits",
    prompt: "How would you prevent a lost update?",
    profileId: profile.id,
  });
  const session = f.create("sessions", {
    title: "Concurrency rehearsal",
    profileId: profile.id,
  });
  return { ...f, profile, question, session };
}
test("a complete practice flow records snapshots, scores attempts, completes and reopens a session", (t) => {
  const f = scenario(t);
  f.update("sessions", f.session.id, { status: "in_progress" });
  const attempt = f.create("attempts", {
    sessionId: f.session.id,
    questionId: f.question.id,
    answer: "Compare an accepted revision.",
    score: 4,
  });
  assert.equal(attempt.questionSnapshot.prompt, f.question.prompt);
  assert.equal(f.session.profileSnapshot.targetRole, "Software engineer");
  f.update("sessions", f.session.id, { status: "completed" });
  assert.throws(() => f.update("attempts", attempt.id, { score: 5 }), /reopen/);
  f.update("sessions", f.session.id, { status: "in_progress" });
  assert.equal(f.update("attempts", attempt.id, { score: 5 }).score, 5);
});
test("PATCH preserves omission and accepts empty text, false and score zero", (t) => {
  const f = scenario(t);
  f.update("profiles", f.profile.id, { background: "Old", archived: true });
  const profile = f.update("profiles", f.profile.id, {
    background: "",
    archived: false,
  });
  assert.equal(profile.name, f.profile.name);
  assert.equal(profile.background, "");
  assert.equal(profile.archived, false);
  const session = f.update("sessions", f.session.id, { score: 0 });
  assert.equal(session.score, 0);
  assert.equal(session.status, "planned");
});
test("invalid creates and updates change neither accepted bytes nor activity", (t) => {
  const f = scenario(t);
  const before = fs.readFileSync(f.file);
  for (const changes of [
    { title: "" },
    { score: "4" },
    { score: 6 },
    { profileId: f.profile.id },
    { status: "unknown" },
    {},
  ])
    assert.throws(() => f.update("sessions", f.session.id, changes));
  for (const input of [
    { name: " " },
    { name: "Valid", unexpected: true },
    { name: "Valid", archived: "false" },
  ])
    assert.throws(() => f.create("profiles", input));
  assert.deepEqual(fs.readFileSync(f.file), before);
});
test("profile names are case-insensitively unique and stale revisions cannot overwrite accepted edits", (t) => {
  const f = scenario(t);
  const old = f.revision();
  assert.throws(
    () => f.create("profiles", { name: "JUNIOR CRUD DEVELOPER" }),
    /already exists/,
  );
  f.update("profiles", f.profile.id, { targetRole: "Mid-level engineer" });
  assert.throws(
    () =>
      f.service.update("profiles", f.profile.id, { name: "Stale rename" }, old),
    /changed/,
  );
  assert.equal(
    f.service.get(f.service.read(), "profiles", f.profile.id).name,
    f.profile.name,
  );
});
test("archived profiles and questions cannot start new associated practice", (t) => {
  const f = scenario(t);
  f.update("profiles", f.profile.id, { archived: true });
  assert.throws(
    () => f.create("sessions", { title: "Blocked", profileId: f.profile.id }),
    /active profile/,
  );
  assert.throws(
    () =>
      f.create("questions", {
        title: "Blocked",
        prompt: "Question",
        profileId: f.profile.id,
      }),
    /active profile/,
  );
  f.update("sessions", f.session.id, { status: "in_progress" });
  f.update("questions", f.question.id, { archived: true });
  assert.throws(
    () =>
      f.create("attempts", {
        sessionId: f.session.id,
        questionId: f.question.id,
      }),
    /active question/,
  );
});
test("attempt references are scoped to the session profile; shared questions are allowed", (t) => {
  const f = scenario(t);
  const other = f.create("profiles", { name: "Other profile" });
  const restricted = f.create("questions", {
    title: "Other",
    prompt: "Other context",
    profileId: other.id,
  });
  const shared = f.create("questions", {
    title: "Shared",
    prompt: "Shared context",
  });
  f.update("sessions", f.session.id, { status: "in_progress" });
  assert.throws(
    () =>
      f.create("attempts", {
        sessionId: f.session.id,
        questionId: restricted.id,
      }),
    /same profile/,
  );
  assert.equal(
    f.create("attempts", { sessionId: f.session.id, questionId: shared.id })
      .questionSnapshot.title,
    "Shared",
  );
});
test("session completion requires answered and scored attempts and enforces lifecycle transitions", (t) => {
  const f = scenario(t);
  assert.throws(
    () => f.update("sessions", f.session.id, { status: "completed" }),
    /Start a planned/,
  );
  assert.throws(
    () =>
      f.create("attempts", {
        sessionId: f.session.id,
        questionId: f.question.id,
      }),
    /Start or reopen/,
  );
  f.update("sessions", f.session.id, { status: "in_progress" });
  assert.throws(
    () => f.update("sessions", f.session.id, { status: "completed" }),
    /every attempt/,
  );
  const attempt = f.create("attempts", {
    sessionId: f.session.id,
    questionId: f.question.id,
  });
  assert.throws(
    () => f.update("sessions", f.session.id, { status: "planned" }),
    /cannot return/,
  );
  f.update("attempts", attempt.id, { answer: "An answer" });
  assert.throws(
    () => f.update("sessions", f.session.id, { status: "completed" }),
    /every attempt/,
  );
});
test("editing a source question does not rewrite the wording of a past attempt", (t) => {
  const f = scenario(t);
  f.update("sessions", f.session.id, { status: "in_progress" });
  const attempt = f.create("attempts", {
    sessionId: f.session.id,
    questionId: f.question.id,
  });
  f.update("questions", f.question.id, {
    prompt: "New wording",
    title: "New title",
  });
  const saved = f.service.get(f.service.read(), "attempts", attempt.id);
  assert.equal(saved.questionSnapshot.prompt, f.question.prompt);
  assert.throws(
    () => f.update("questions", f.question.id, { profileId: null }),
    /cannot change/,
  );
});
test("related records require explicit deletion in dependency order and retain content-free activity", (t) => {
  const f = scenario(t);
  f.update("sessions", f.session.id, { status: "in_progress" });
  const attempt = f.create("attempts", {
    sessionId: f.session.id,
    questionId: f.question.id,
    answer: "Sensitive practice text",
  });
  assert.throws(() => f.remove("profiles", f.profile.id), /referencing/);
  assert.throws(() => f.remove("questions", f.question.id), /retained/);
  assert.throws(() => f.remove("sessions", f.session.id), /Remove attempts/);
  f.remove("attempts", attempt.id);
  f.remove("sessions", f.session.id);
  f.remove("questions", f.question.id);
  f.remove("profiles", f.profile.id);
  const state = f.service.read().value;
  assert.equal(state.attempts.length, 0);
  assert.equal(state.profiles.length, 0);
  assert.ok(
    state.activity.some(
      (item) => item.recordId === attempt.id && item.action === "deleted",
    ),
  );
  assert.ok(!JSON.stringify(state).includes("Sensitive practice text"));
});
test("list search, filtering and pagination compose with bounded validated parameters", (t) => {
  const f = scenario(t);
  for (let i = 1; i <= 24; i++)
    f.create("questions", {
      title: `Practice ${i}`,
      prompt: "CRUD question",
      profileId: f.profile.id,
    });
  const snapshot = f.service.read();
  const page = f.service.list(
    snapshot,
    "questions",
    new URLSearchParams({
      q: "Practice",
      profileId: f.profile.id,
      page: 2,
      pageSize: 20,
    }),
  );
  assert.equal(page.total, 24);
  assert.equal(page.items.length, 4);
  for (const params of [
    "page=0",
    "pageSize=51",
    "page=1&page=2",
    "unknown=yes",
    "archived=maybe",
  ])
    assert.throws(() =>
      f.service.list(snapshot, "questions", new URLSearchParams(params)),
    );
});
test("bootstrap and token authentication do not expose stored authentication material", (t) => {
  const f = scenario(t);
  const snapshot = f.service.read();
  authenticate(snapshot.value, `Bearer ${f.token}`);
  assert.throws(
    () => authenticate(snapshot.value, "Bearer " + "0".repeat(64)),
    /valid practice/,
  );
  const output = bootstrap(snapshot);
  assert.equal(output.auth, undefined);
  assert.ok(!JSON.stringify(output).includes(snapshot.value.auth.tokenHash));
  assert.equal(output.questions[0].prompt, undefined);
});
test("an injected replacement failure rolls back the resource and its activity entry", (t) => {
  let fail = false;
  const fsImpl = Object.create(fs);
  fsImpl.renameSync = (...args) => {
    if (fail) throw new Error("Synthetic replacement failure");
    return fs.renameSync(...args);
  };
  const f = fixture(t, { fsImpl });
  const before = fs.readFileSync(f.file);
  fail = true;
  assert.throws(
    () => f.create("profiles", { name: "Not accepted" }),
    /replacement failure/,
  );
  assert.deepEqual(fs.readFileSync(f.file), before);
  assert.equal(f.service.read().value.activity.length, 0);
});
test("malformed persisted references fail closed without altering the file", (t) => {
  const f = scenario(t);
  const state = f.service.read().value;
  state.sessions[0].profileId = "00000000-0000-0000-0000-000000000000";
  fs.writeFileSync(f.file, JSON.stringify(state));
  const bytes = fs.readFileSync(f.file);
  assert.throws(() => f.service.read(), /Invalid practice workspace/);
  assert.deepEqual(fs.readFileSync(f.file), bytes);
});
