const $ = (selector) => document.querySelector(selector);
const state = {
  token: "",
  data: null,
  kind: "profiles",
  page: 1,
  total: 0,
  items: [],
  busy: false,
  editor: null,
  review: null,
  listRevision: null,
};
const widgets = new Map();
const singular = {
  profiles: "profile",
  questions: "question",
  sessions: "session",
  attempts: "attempt",
};
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
function node(tag, text, className) {
  const element = document.createElement(tag);
  if (text !== undefined) element.textContent = text;
  if (className) element.className = className;
  return element;
}
function notice(message, error = false) {
  $("#notice").textContent = message;
  $("#notice").classList.toggle("error", error);
}
function controls() {
  for (const item of document.querySelectorAll(
    "#workspace input,#workspace textarea,#workspace select,#workspace button,#session-controls button",
  ))
    item.disabled = state.busy;
  $("#save").disabled = state.busy || !state.editor || state.editor.needsReview;
  $("#delete").disabled =
    state.busy || !state.editor?.record || state.editor.needsReview;
  $("#previous").disabled = state.busy || state.page === 1;
  $("#next").disabled = state.busy || state.page * 20 >= state.total;
}
function busy(value) {
  state.busy = value;
  controls();
}
function raw() {
  return Object.fromEntries(
    [...widgets].map(([key, item]) => [key, item.raw()]),
  );
}
function dirty() {
  return state.editor && !same(raw(), state.editor.baseRaw);
}
function mayLeave() {
  return !state.busy && (!dirty() || confirm("Discard this unsaved draft?"));
}
async function api(path, { method = "GET", body, revision } = {}) {
  const write = method !== "GET";
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 20000);
  try {
    let response;
    try {
      response = await fetch(path, {
        method,
        signal: controller.signal,
        cache: "no-store",
        headers: {
          Authorization: `Bearer ${state.token}`,
          ...(body !== undefined ? { "Content-Type": "application/json" } : {}),
          ...(write ? { "If-Match": `"${revision}"` } : {}),
        },
        ...(body !== undefined ? { body: JSON.stringify(body) } : {}),
      });
    } catch {
      throw Object.assign(
        new Error(
          write
            ? "The response was lost. This change may have been accepted; review the latest state before retrying."
            : "The local workspace could not be reached.",
        ),
        { uncertain: write },
      );
    }
    let value;
    try {
      value = await response.json();
    } catch {
      throw Object.assign(
        new Error(
          "The server response could not be read. Review accepted state before retrying a write.",
        ),
        { uncertain: write },
      );
    }
    if (!response.ok)
      throw Object.assign(
        new Error(
          response.status >= 500 && write
            ? "The server reported an error. Review accepted state before retrying this change."
            : value.error || "Request failed",
        ),
        { status: response.status, uncertain: write && response.status >= 500 },
      );
    return {
      value,
      revision: response.headers.get("etag")?.replaceAll('"', ""),
    };
  } finally {
    clearTimeout(timer);
  }
}
function profileName(id) {
  return state.data.profiles.find((item) => item.id === id)?.name ?? "Shared";
}
function recordName(record) {
  return (
    record.name ?? record.title ?? record.questionSnapshot?.title ?? record.id
  );
}
function choice(items, label) {
  return items.map((item) => ({ value: item.id, label: label(item) }));
}
function selectOptions(element, choices, value, blank = false) {
  element.replaceChildren();
  if (blank) {
    const option = node(
      "option",
      typeof blank === "string" ? blank : "Select a record",
    );
    option.value = "";
    element.append(option);
  }
  for (const item of choices) {
    const option = node("option", item.label);
    option.value = item.value;
    element.append(option);
  }
  if (value && !choices.some((item) => item.value === value)) {
    const option = node("option", "Unavailable reference");
    option.value = value;
    element.append(option);
  }
  element.value = value ?? "";
}
function definitions(record) {
  const create = !record;
  const scope = $("#profile-filter").value;
  const profiles = choice(
    state.data.profiles,
    (item) => `${item.name}${item.archived ? " (archived)" : ""}`,
  );
  const sessions = choice(
    state.data.sessions,
    (item) => `${item.title} · ${item.status}`,
  );
  const f = (key, label, type = "text", options = {}) => ({
    key,
    label,
    type,
    ...options,
  });
  const title = f("title", "Title", "text", { required: true, max: 100 });
  const prose = (key, label, required = false) =>
    f(key, label, "textarea", { required, max: 20000, wide: true });
  const profile = (nullable) =>
    f("profileId", "Profile", "select", {
      choices: profiles,
      nullable,
      required: !nullable,
      blank: nullable ? "Shared question (all profiles)" : "Choose a profile",
      fallback:
        scope ||
        (nullable
          ? ""
          : state.data.profiles.find((item) => !item.archived)?.id),
    });
  const score = f("score", "Score (0–5, optional)", "number", {
    nullable: true,
    max: 5,
  });
  if (state.kind === "profiles")
    return [
      f("name", "Name", "text", { required: true, max: 100 }),
      f("targetRole", "Target role", "text", { max: 100 }),
      prose("background", "Background and learning goals"),
      f("archived", "Archive profile", "checkbox", { fallback: false }),
    ];
  if (state.kind === "questions")
    return [
      title,
      profile(true),
      prose("prompt", "Question prompt", true),
      f("topic", "Topic", "text", { max: 100, fallback: "general" }),
      f("difficulty", "Difficulty (1–5)", "number", {
        required: true,
        min: 1,
        max: 5,
        fallback: 1,
      }),
      f("archived", "Archive question", "checkbox", { fallback: false }),
    ];
  if (state.kind === "sessions")
    return [
      title,
      ...(create ? [profile(false)] : []),
      ...(create
        ? []
        : [
            f("status", "Session status", "select", {
              choices: ["planned", "in_progress", "completed"].map((value) => ({
                value,
                label: value,
              })),
              required: true,
            }),
          ]),
      prose("notes", "Session notes"),
      score,
    ];
  return [
    ...(create
      ? [
          f("sessionId", "Session", "select", {
            choices: sessions,
            fallback: state.data.sessions.find(
              (item) =>
                item.status === "in_progress" &&
                (!scope || item.profileId === scope),
            )?.id,
            required: true,
            blank: true,
          }),
          f("questionId", "Question", "select", {
            choices: choice(state.data.questions, (item) => item.title),
            required: true,
            blank: true,
          }),
        ]
      : []),
    prose("answer", "Your answer"),
    prose("feedback", "Review notes and next improvement"),
    score,
  ];
}
function addField(def, value) {
  const label = node("label", undefined, `field${def.wide ? " wide" : ""}`);
  label.htmlFor = `field-${def.key}`;
  label.append(node("span", def.label));
  const input = document.createElement(
    def.type === "select"
      ? "select"
      : def.type === "textarea"
        ? "textarea"
        : "input",
  );
  input.id = `field-${def.key}`;
  input.name = def.key;
  input.required = Boolean(def.required);
  if (input.tagName === "INPUT")
    input.type =
      def.type === "checkbox"
        ? "checkbox"
        : def.type === "number"
          ? "number"
          : "text";
  if (def.type === "number") {
    input.min = String(def.min ?? 0);
    input.max = String(def.max);
    input.step = "1";
  } else if (def.max) input.maxLength = def.max;
  const set = (value) => {
    if (def.type === "select")
      selectOptions(input, def.choices, value, def.blank);
    else if (def.type === "checkbox") input.checked = Boolean(value);
    else input.value = value ?? "";
  };
  const read = () =>
    def.type === "checkbox"
      ? input.checked
      : def.type === "number"
        ? input.value === "" && def.nullable
          ? null
          : Number(input.value)
        : def.type === "select" && def.nullable
          ? input.value || null
          : input.value;
  const rawValue = () =>
    def.type === "checkbox" ? input.checked : input.value;
  set(value ?? def.fallback);
  label.append(input);
  $("#fields").append(label);
  widgets.set(def.key, { input, def, set, read, raw: rawValue });
}
function configureQuestion(initial = false) {
  if (state.kind !== "attempts" || state.editor.record) return;
  const session = state.data.sessions.find(
    (item) => item.id === widgets.get("sessionId").read(),
  );
  const field = widgets.get("questionId");
  const items = state.data.questions.filter(
    (item) =>
      !item.archived &&
      session &&
      (item.profileId === null || item.profileId === session.profileId),
  );
  field.def.choices = choice(items, (item) => item.title);
  const previous = field.read();
  field.set(
    initial && items.some((item) => item.id === previous)
      ? previous
      : (items[0]?.id ?? ""),
  );
}
function values() {
  return Object.fromEntries(
    [...widgets].map(([key, item]) => [key, item.read()]),
  );
}
function changes() {
  const current = values();
  return state.editor.record
    ? Object.fromEntries(
        Object.entries(current).filter(
          ([key, value]) => !same(value, state.editor.base[key]),
        ),
      )
    : current;
}
function renderEditor(
  record = null,
  revision = state.listRevision,
  draft = null,
) {
  state.editor = {
    record,
    id: record?.id ?? null,
    revision,
    base: {},
    baseRaw: {},
    needsReview: false,
  };
  state.review = null;
  widgets.clear();
  $("#fields").replaceChildren();
  $("#comparison").hidden = true;
  $("#editor-title").textContent =
    `${record ? "Edit" : "New"} ${singular[state.kind]}${record ? `: ${recordName(record)}` : ""}`;
  $("#editor-help").textContent =
    state.kind === "sessions"
      ? "New sessions start planned. Start a session before adding attempts. Answer and score every attempt before completing it; reopen it to revise attempts."
      : state.kind === "attempts"
        ? "Choose an in-progress session and an active shared or matching-profile question. Each attempt preserves the question wording used at creation."
        : state.kind === "questions"
          ? "Questions can be shared or associated with a profile. Used questions retain their profile association; archive them when they should stop appearing in new practice."
          : "Describe a learning context. Archive a profile to stop starting new sessions. Referenced profiles cannot be deleted.";
  $("#record-meta").textContent = record
    ? `Record ${record.id} · Last updated ${new Date(record.updatedAt).toLocaleString()}`
    : "A new record based on the current accepted workspace.";
  $("#question-context").replaceChildren();
  if (record?.questionSnapshot)
    $("#question-context").append(
      node("strong", record.questionSnapshot.title),
      node("p", record.questionSnapshot.prompt),
    );
  for (const def of definitions(record)) addField(def, record?.[def.key]);
  configureQuestion(true);
  state.editor.base = values();
  state.editor.baseRaw = raw();
  if (draft)
    for (const [key, value] of Object.entries(draft))
      widgets.get(key)?.set(value);
  renderList();
  controls();
}
function renderList() {
  $("#records").replaceChildren();
  for (const record of state.items) {
    const button = node(
      "button",
      undefined,
      `record${record.id === state.editor?.id ? " active" : ""}`,
    );
    button.type = "button";
    button.dataset.recordId = record.id;
    button.append(
      node("strong", recordName(record)),
      node(
        "small",
        [
          record.profileId ? profileName(record.profileId) : null,
          record.status,
          record.archived ? "Archived" : null,
          record.score != null ? `Score ${record.score}/5` : null,
        ]
          .filter(Boolean)
          .join(" · ") || "Open record",
      ),
    );
    button.addEventListener("click", () => openRecord(record.id));
    button.disabled = state.busy;
    $("#records").append(button);
  }
  if (!state.items.length)
    $("#records").append(node("p", "No matching records.", "muted"));
  $("#page-label").textContent =
    `Page ${state.page} of ${Math.max(1, Math.ceil(state.total / 20))} · ${state.total} records`;
}
async function loadList() {
  const params = new URLSearchParams({ page: state.page, pageSize: 20 });
  const q = $("#search").value.trim();
  if (q) params.set("q", q);
  if (state.kind !== "profiles" && $("#profile-filter").value)
    params.set("profileId", $("#profile-filter").value);
  let response = await api(`/api/${state.kind}?${params}`);
  const last = Math.max(1, Math.ceil(response.value.total / 20));
  if (state.page > last) {
    state.page = last;
    params.set("page", last);
    response = await api(`/api/${state.kind}?${params}`);
  }
  state.items = response.value.items;
  state.total = response.value.total;
  state.listRevision = response.revision;
  renderList();
}
async function loadBootstrap() {
  const { value } = await api("/api/bootstrap");
  state.data = value;
  const selected = $("#profile-filter").value;
  selectOptions(
    $("#profile-filter"),
    choice(value.profiles, (item) => item.name),
    value.profiles.some((item) => item.id === selected) ? selected : "",
    "All profiles",
  );
  $("#owner").textContent = value.owner;
  $("#counts").textContent = Object.entries(value.counts)
    .map(([key, count]) => `${count} ${key}`)
    .join(" · ");
  $("#activity").replaceChildren();
  for (const entry of value.activity) {
    const item = node("div");
    item.append(
      node("strong", `${singular[entry.resource]} ${entry.action}`),
      node("small", new Date(entry.at).toLocaleString()),
      node("small", entry.fields.join(", ") || "Record removed"),
    );
    $("#activity").append(item);
  }
}
async function openRecord(id) {
  if (!mayLeave()) return;
  busy(true);
  try {
    const response = await api(`/api/${state.kind}/${id}`);
    renderEditor(response.value, response.revision);
    notice("");
  } catch (error) {
    notice(error.message, true);
  } finally {
    busy(false);
  }
}
async function reviewLatest() {
  if (state.busy || !state.editor) return;
  const draft = changes();
  const id = state.editor.id;
  busy(true);
  try {
    await loadBootstrap();
    await loadList();
    let latest = null,
      revision = state.listRevision,
      missing = false;
    if (id) {
      try {
        const response = await api(`/api/${state.kind}/${id}`);
        latest = response.value;
        revision = response.revision;
      } catch (error) {
        if (error.status === 404) missing = true;
        else throw error;
      }
    }
    state.review = { latest, revision, draft, missing };
    $("#latest").textContent = JSON.stringify(latest ?? state.items, null, 2);
    $("#draft").textContent = JSON.stringify(draft, null, 2);
    $("#review-help").textContent = missing
      ? "This record was removed. Copy the draft, then start a new record if appropriate."
      : id
        ? "Keep only your changed fields. Unedited fields will use the latest accepted values."
        : "Before retrying a creation, check the current list for a record that may already have been accepted.";
    $("#accept-review").hidden = missing;
    $("#comparison").hidden = false;
    notice("Latest state loaded. Your draft has not been submitted.");
  } catch (error) {
    notice(error.message, true);
  } finally {
    busy(false);
  }
}
async function accepted(result) {
  state.editor.needsReview = true;
  state.editor.id = result.deleted ? null : result.id;
  state.editor.baseRaw = raw();
  try {
    await loadBootstrap();
    await loadList();
    if (result.deleted) renderEditor();
    else {
      const current = await api(`/api/${state.kind}/${result.id}`);
      renderEditor(current.value, current.revision);
    }
    notice(
      result.deleted
        ? "Record deleted."
        : "Saved. The editor shows the accepted record.",
    );
  } catch (error) {
    notice(
      `The write was accepted, but refreshing failed. Review latest before another write. ${error.message}`,
      true,
    );
  }
}
$("#editor").addEventListener("input", (event) => {
  if (state.busy) return;
  state.review = null;
  $("#comparison").hidden = true;
  if (event.target.name === "sessionId") configureQuestion();
});
$("#editor").addEventListener("submit", async (event) => {
  event.preventDefault();
  if (state.busy || !state.editor || state.editor.needsReview) return;
  const input = changes();
  if (state.editor.record && !Object.keys(input).length) {
    notice("There are no changed fields to save.");
    return;
  }
  busy(true);
  notice("Saving…");
  try {
    const response = await api(
      `/api/${state.kind}${state.editor.record ? "/" + state.editor.record.id : ""}`,
      {
        method: state.editor.record ? "PATCH" : "POST",
        body: input,
        revision: state.editor.revision,
      },
    );
    await accepted(response.value);
  } catch (error) {
    if (error.status === 409 || error.uncertain)
      state.editor.needsReview = true;
    notice(error.message, true);
  } finally {
    busy(false);
  }
});
$("#delete").addEventListener("click", async () => {
  if (
    state.busy ||
    !state.editor.record ||
    state.editor.needsReview ||
    !confirm(
      `Delete ${recordName(state.editor.record)}? Referenced records are protected.`,
    )
  )
    return;
  busy(true);
  try {
    const result = await api(`/api/${state.kind}/${state.editor.record.id}`, {
      method: "DELETE",
      body: {},
      revision: state.editor.revision,
    });
    await accepted(result.value);
  } catch (error) {
    if (error.status === 409 || error.uncertain)
      state.editor.needsReview = true;
    notice(error.message, true);
  } finally {
    busy(false);
  }
});
$("#new").addEventListener("click", () => {
  if (mayLeave()) {
    renderEditor();
    notice("");
  }
});
$("#discard").addEventListener("click", () => {
  if (mayLeave()) {
    renderEditor(state.editor.record, state.editor.revision);
    notice("Draft discarded.");
  }
});
$("#review").addEventListener("click", reviewLatest);
$("#accept-review").addEventListener("click", () => {
  if (!state.review || state.review.missing || state.busy) return;
  const { latest, revision, draft } = state.review;
  renderEditor(latest, revision, draft);
  notice("Reviewed version accepted. Your changes remain unsaved.");
});
async function navigate() {
  busy(true);
  try {
    await loadList();
    renderEditor();
    notice("");
  } catch (error) {
    notice(error.message, true);
  } finally {
    busy(false);
  }
}
$("#resource-kind").addEventListener("change", async () => {
  if (!mayLeave()) {
    $("#resource-kind").value = state.kind;
    return;
  }
  state.kind = $("#resource-kind").value;
  state.page = 1;
  $("#search").value = "";
  state.items = [];
  renderEditor();
  await navigate();
});
$("#profile-filter").addEventListener("change", async () => {
  if (state.busy) return;
  state.page = 1;
  busy(true);
  try {
    await loadList();
  } catch (error) {
    notice(error.message, true);
  } finally {
    busy(false);
  }
});
$("#search-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  if (state.busy) return;
  state.page = 1;
  busy(true);
  try {
    await loadList();
  } catch (error) {
    notice(error.message, true);
  } finally {
    busy(false);
  }
});
for (const [selector, delta] of [
  ["#previous", -1],
  ["#next", 1],
])
  $(selector).addEventListener("click", async () => {
    if (state.busy) return;
    state.page += delta;
    busy(true);
    try {
      await loadList();
    } catch (error) {
      notice(error.message, true);
    } finally {
      busy(false);
    }
  });
$("#refresh").addEventListener("click", async () => {
  if (dirty() || state.editor?.needsReview) {
    await reviewLatest();
    return;
  }
  if (state.busy) return;
  busy(true);
  try {
    const id = state.editor?.id;
    await loadBootstrap();
    await loadList();
    if (id) {
      const response = await api(`/api/${state.kind}/${id}`);
      renderEditor(response.value, response.revision);
    } else renderEditor();
    notice("Workspace refreshed.");
  } catch (error) {
    notice(error.message, true);
  } finally {
    busy(false);
  }
});
$("#login-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  if (state.busy) return;
  state.token = $("#token").value.trim();
  busy(true);
  $("#login-form button").disabled = true;
  try {
    await loadBootstrap();
    await loadList();
    renderEditor();
    $("#token").value = "";
    $("#login").hidden = true;
    $("#workspace").hidden = false;
    $("#session-controls").hidden = false;
    notice("Connected. Start with a profile.");
  } catch (error) {
    state.token = "";
    state.data = null;
    notice(error.message, true);
  } finally {
    busy(false);
    $("#login-form button").disabled = false;
  }
});
$("#sign-out").addEventListener("click", () => {
  if (!mayLeave()) return;
  state.token = "";
  state.data = null;
  state.editor = null;
  state.review = null;
  state.items = [];
  widgets.clear();
  $("#fields").replaceChildren();
  $("#records").replaceChildren();
  $("#latest").textContent = "";
  $("#draft").textContent = "";
  $("#workspace").hidden = true;
  $("#session-controls").hidden = true;
  $("#login").hidden = false;
  notice("Signed out. The token was removed from this tab.");
});
$("#export").addEventListener("click", async () => {
  if (state.busy) return;
  busy(true);
  try {
    const { value } = await api("/api/export");
    const url = URL.createObjectURL(
      new Blob([JSON.stringify(value, null, 2)], { type: "application/json" }),
    );
    const link = node("a");
    link.href = url;
    link.download = "practice-export.json";
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    notice(
      "Export downloaded. It contains practice records, without the access credential.",
    );
  } catch (error) {
    notice(error.message, true);
  } finally {
    busy(false);
  }
});
window.addEventListener("beforeunload", (event) => {
  if (dirty()) {
    event.preventDefault();
    event.returnValue = "";
  }
});
