const { randomUUID, createHash, timingSafeEqual } = require("node:crypto");
const { JsonFile, failure, jsonValue } = require("../shared/json-file");

const KINDS = ["profiles", "questions", "sessions", "attempts"];
const LIMITS = {
  profiles: 200,
  questions: 2000,
  sessions: 2000,
  attempts: 5000,
};
const FIELDS = {
  profiles: ["name", "targetRole", "background", "archived"],
  questions: [
    "profileId",
    "title",
    "prompt",
    "topic",
    "difficulty",
    "archived",
  ],
  sessions: ["profileId", "title", "status", "notes", "score"],
  attempts: ["sessionId", "questionId", "answer", "feedback", "score"],
};
const DEFAULTS = {
  profiles: { targetRole: "", background: "", archived: false },
  questions: {
    profileId: null,
    topic: "general",
    difficulty: 1,
    archived: false,
  },
  sessions: { status: "planned", notes: "", score: null },
  attempts: { answer: "", feedback: "", score: null },
};
const REQUIRED = {
  profiles: ["name"],
  questions: ["title", "prompt"],
  sessions: ["profileId", "title"],
  attempts: ["sessionId", "questionId"],
};
const IMMUTABLE = {
  profiles: [],
  questions: [],
  sessions: ["profileId"],
  attempts: ["sessionId", "questionId"],
};
const ID = /^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$/;
const hash = (value) => createHash("sha256").update(value).digest("hex");
function requireKind(kind) {
  if (!KINDS.includes(kind)) throw failure(404, "Resource not found");
}
function text(value, name, max, { required = false, multiline = false } = {}) {
  if (
    typeof value !== "string" ||
    !value.isWellFormed() ||
    value.length > max ||
    (required && !value.trim()) ||
    (multiline ? /[\x00-\x08\x0b\x0c\x0e-\x1f]/ : /[\x00-\x1f]/).test(value)
  )
    throw failure(
      422,
      `${name} must be ${required ? "non-empty " : ""}text of at most ${max} characters`,
    );
  return multiline ? value : value.trim();
}
function payload(kind, input, create) {
  requireKind(kind);
  jsonValue(input);
  if (!input || typeof input !== "object" || Array.isArray(input))
    throw failure(422, "Expected an object");
  const allowed = FIELDS[kind].filter(
    (key) => create || !IMMUTABLE[kind].includes(key),
  );
  if (Object.keys(input).some((key) => !allowed.includes(key)))
    throw failure(422, "Unknown or immutable resource field");
  if (!create && !Object.keys(input).length)
    throw failure(422, "Provide at least one changed field");
  const result = create ? { ...DEFAULTS[kind], ...input } : { ...input };
  if (create && REQUIRED[kind].some((key) => !Object.hasOwn(input, key)))
    throw failure(422, `Required fields: ${REQUIRED[kind].join(", ")}`);
  for (const [key, value] of Object.entries(result)) {
    if (["profileId", "sessionId", "questionId"].includes(key)) {
      if (
        !(kind === "questions" && key === "profileId" && value === null) &&
        (typeof value !== "string" || !ID.test(value))
      )
        throw failure(422, `${key} must be a valid record identifier`);
    } else if (key === "archived") {
      if (typeof value !== "boolean")
        throw failure(422, "archived must be a boolean");
    } else if (key === "score") {
      if (
        value !== null &&
        (!Number.isInteger(value) || value < 0 || value > 5)
      )
        throw failure(422, "score must be null or an integer from 0 to 5");
    } else if (key === "difficulty") {
      if (!Number.isInteger(value) || value < 1 || value > 5)
        throw failure(422, "difficulty must be an integer from 1 to 5");
    } else if (key === "status") {
      if (!["planned", "in_progress", "completed"].includes(value))
        throw failure(422, "Unknown session status");
    } else {
      const multiline = [
        "background",
        "prompt",
        "notes",
        "answer",
        "feedback",
      ].includes(key);
      result[key] = text(value, key, multiline ? 20000 : 100, {
        required: ["name", "title", "prompt"].includes(key),
        multiline,
      });
    }
  }
  return result;
}
function find(state, kind, id) {
  const record = state[kind].find((item) => item.id === id);
  if (!record) throw failure(404, `${kind} record not found`);
  return record;
}
function validateState(state) {
  try {
    if (
      !state ||
      state.schemaVersion !== 1 ||
      Object.keys(state).some(
        (key) => !["schemaVersion", "auth", "activity", ...KINDS].includes(key),
      )
    )
      throw new Error();
    if (
      !state.auth ||
      typeof state.auth.tokenHash !== "string" ||
      !/^[a-f0-9]{64}$/.test(state.auth.tokenHash)
    )
      throw new Error();
    text(state.auth.owner, "owner", 100, { required: true });
    for (const kind of KINDS) {
      if (!Array.isArray(state[kind]) || state[kind].length > LIMITS[kind])
        throw new Error();
      const ids = new Set();
      for (const record of state[kind]) {
        if (
          !record ||
          !ID.test(record.id) ||
          ids.has(record.id) ||
          !Number.isFinite(Date.parse(record.createdAt)) ||
          !Number.isFinite(Date.parse(record.updatedAt))
        )
          throw new Error();
        ids.add(record.id);
        const fields = Object.fromEntries(
          FIELDS[kind].map((key) => [key, record[key]]),
        );
        payload(kind, fields, true);
        if (kind === "questions" && record.profileId !== null)
          find(state, "profiles", record.profileId);
        if (kind === "sessions") {
          find(state, "profiles", record.profileId);
          if (
            !record.profileSnapshot ||
            typeof record.profileSnapshot.name !== "string" ||
            typeof record.profileSnapshot.targetRole !== "string"
          )
            throw new Error();
        }
        if (kind === "attempts") {
          const session = find(state, "sessions", record.sessionId);
          const question = find(state, "questions", record.questionId);
          if (
            question.profileId !== null &&
            question.profileId !== session.profileId
          )
            throw new Error();
          if (
            !record.questionSnapshot ||
            ["title", "prompt", "topic"].some(
              (key) => typeof record.questionSnapshot[key] !== "string",
            )
          )
            throw new Error();
        }
      }
    }
    if (
      !Array.isArray(state.activity) ||
      state.activity.length > 1000 ||
      state.activity.some(
        (item) =>
          !ID.test(item.id) ||
          !KINDS.includes(item.resource) ||
          !ID.test(item.recordId) ||
          !Array.isArray(item.fields) ||
          !["created", "updated", "deleted"].includes(item.action) ||
          !Number.isFinite(Date.parse(item.at)),
      )
    )
      throw new Error();
  } catch {
    throw failure(
      503,
      "Invalid practice workspace. The file was preserved; restore or repair it explicitly",
    );
  }
}
function createState(owner, token) {
  return {
    schemaVersion: 1,
    auth: {
      owner: text(owner, "owner", 100, { required: true }),
      tokenHash: hash(token),
    },
    profiles: [],
    questions: [],
    sessions: [],
    attempts: [],
    activity: [],
  };
}
function authenticate(state, header) {
  const match = /^Bearer ([a-f0-9]{64})$/.exec(header ?? "");
  if (
    !match ||
    !timingSafeEqual(
      Buffer.from(hash(match[1]), "hex"),
      Buffer.from(state.auth.tokenHash, "hex"),
    )
  )
    throw failure(401, "A valid practice workspace token is required");
}
function bootstrap(snapshot) {
  const state = snapshot.value;
  return {
    revision: snapshot.revision,
    owner: state.auth.owner,
    counts: Object.fromEntries(KINDS.map((kind) => [kind, state[kind].length])),
    profiles: state.profiles.map(({ id, name, targetRole, archived }) => ({
      id,
      name,
      targetRole,
      archived,
    })),
    questions: state.questions.map(({ id, profileId, title, archived }) => ({
      id,
      profileId,
      title,
      archived,
    })),
    sessions: state.sessions.map(({ id, profileId, title, status }) => ({
      id,
      profileId,
      title,
      status,
    })),
    activity: state.activity.slice(-20).reverse(),
  };
}
function references(state, kind, next, previous) {
  if (
    kind === "profiles" &&
    state.profiles.some(
      (item) =>
        item.id !== next.id &&
        item.name.toLowerCase() === next.name.toLowerCase(),
    )
  )
    throw failure(409, "A profile with this name already exists");
  if (kind === "questions") {
    if (next.profileId !== null) {
      const profile = find(state, "profiles", next.profileId);
      if (
        (!previous || previous.profileId !== next.profileId) &&
        profile.archived
      )
        throw failure(409, "Select an active profile");
    }
    if (
      previous &&
      next.profileId !== previous.profileId &&
      state.attempts.some((item) => item.questionId === next.id)
    )
      throw failure(
        409,
        "A used question cannot change its profile association",
      );
  }
  if (kind === "sessions") {
    const profile = find(state, "profiles", next.profileId);
    if (!previous && profile.archived)
      throw failure(409, "Select an active profile");
    if (!previous && next.status !== "planned")
      throw failure(422, "New sessions start planned");
    if (!previous)
      next.profileSnapshot = {
        name: profile.name,
        targetRole: profile.targetRole,
      };
    if (previous && next.status !== previous.status) {
      const transitions = {
        planned: ["in_progress"],
        in_progress: ["planned", "completed"],
        completed: ["in_progress"],
      };
      if (!transitions[previous.status].includes(next.status))
        throw failure(
          409,
          "Start a planned session before completing it; reopen a completed session before further work",
        );
      const attempts = state.attempts.filter(
        (item) => item.sessionId === next.id,
      );
      if (next.status === "planned" && attempts.length)
        throw failure(409, "A session with attempts cannot return to planned");
      if (
        next.status === "completed" &&
        (!attempts.length ||
          attempts.some((item) => !item.answer.trim() || item.score === null))
      )
        throw failure(
          409,
          "Complete and score every attempt before finishing this session",
        );
    }
  }
  if (kind === "attempts") {
    const session = find(state, "sessions", next.sessionId);
    const question = find(state, "questions", next.questionId);
    if (session.status !== "in_progress")
      throw failure(
        409,
        "Start or reopen the session before changing attempts",
      );
    if (!previous && question.archived)
      throw failure(409, "Select an active question");
    if (question.profileId !== null && question.profileId !== session.profileId)
      throw failure(
        409,
        "Question and session must belong to the same profile",
      );
    if (!previous)
      next.questionSnapshot = {
        title: question.title,
        prompt: question.prompt,
        topic: question.topic,
      };
  }
}
function createService(file, options = {}) {
  const disk = new JsonFile(file, {
    maxBytes: 8 * 1024 * 1024,
    validate: validateState,
    ...options,
  });
  function mutate(kind, id, input, revision, action) {
    requireKind(kind);
    if (id !== null && (typeof id !== "string" || !ID.test(id)))
      throw failure(404, "Record not found");
    const clean =
      action === "deleted" ? null : payload(kind, input, action === "created");
    return disk.commit(revision, (state) => {
      const previous = id === null ? null : find(state, kind, id);
      const now = new Date().toISOString();
      let next;
      if (action === "deleted") {
        if (
          kind === "profiles" &&
          (state.questions.some((item) => item.profileId === id) ||
            state.sessions.some((item) => item.profileId === id))
        )
          throw failure(
            409,
            "Remove or reassign referencing questions and sessions before deleting this profile",
          );
        if (
          kind === "questions" &&
          state.attempts.some((item) => item.questionId === id)
        )
          throw failure(
            409,
            "This question is retained by practice attempts; archive it instead",
          );
        if (
          kind === "sessions" &&
          state.attempts.some((item) => item.sessionId === id)
        )
          throw failure(
            409,
            "Remove attempts explicitly before deleting their session",
          );
        if (
          kind === "attempts" &&
          find(state, "sessions", previous.sessionId).status !== "in_progress"
        )
          throw failure(409, "Reopen the session before removing an attempt");
        state[kind] = state[kind].filter((item) => item.id !== id);
        next = { id, deleted: true };
      } else {
        if (!previous && state[kind].length >= LIMITS[kind])
          throw failure(409, `The ${kind} limit is reached`);
        next = previous
          ? { ...previous, ...clean, updatedAt: now }
          : { ...clean, id: randomUUID(), createdAt: now, updatedAt: now };
        references(state, kind, next, previous);
        if (previous)
          state[kind][state[kind].findIndex((item) => item.id === id)] = next;
        else state[kind].push(next);
      }
      state.activity.push({
        id: randomUUID(),
        at: now,
        resource: kind,
        recordId: next.id,
        action,
        fields: Object.keys(clean ?? {}),
      });
      state.activity = state.activity.slice(-1000);
      return next;
    });
  }
  return {
    disk,
    read: () => disk.read(),
    create: (kind, input, revision) =>
      mutate(kind, null, input, revision, "created"),
    update: (kind, id, input, revision) =>
      mutate(kind, id, input, revision, "updated"),
    delete: (kind, id, revision) => mutate(kind, id, null, revision, "deleted"),
    get(snapshot, kind, id) {
      requireKind(kind);
      return structuredClone(find(snapshot.value, kind, id));
    },
    list(snapshot, kind, params) {
      requireKind(kind);
      const allowed = [
        "q",
        "page",
        "pageSize",
        ...(kind !== "profiles" ? ["profileId"] : []),
        ...(kind === "attempts" ? ["sessionId"] : []),
        ...(kind === "sessions" ? ["status"] : []),
        ...(["profiles", "questions"].includes(kind) ? ["archived"] : []),
      ];
      for (const key of params.keys())
        if (!allowed.includes(key) || params.getAll(key).length !== 1)
          throw failure(422, "Unknown or repeated list filter");
      const number = (key, fallback, max) => {
        const raw = params.get(key);
        if (raw !== null && !/^[1-9][0-9]*$/.test(raw))
          throw failure(422, `Invalid ${key}`);
        const value = raw === null ? fallback : Number(raw);
        if (!Number.isSafeInteger(value) || value > max)
          throw failure(422, `Invalid ${key}`);
        return value;
      };
      const page = number("page", 1, 100000),
        pageSize = number("pageSize", 20, 50);
      const q = text(params.get("q") ?? "", "search", 100).toLowerCase();
      const profileId = params.get("profileId"),
        sessionId = params.get("sessionId"),
        status = params.get("status"),
        archived = params.get("archived");
      if (profileId !== null) find(snapshot.value, "profiles", profileId);
      if (sessionId !== null) find(snapshot.value, "sessions", sessionId);
      if (
        status !== null &&
        !["planned", "in_progress", "completed"].includes(status)
      )
        throw failure(422, "Invalid status filter");
      if (archived !== null && !["true", "false"].includes(archived))
        throw failure(422, "Invalid archive filter");
      let items = snapshot.value[kind].filter(
        (item) =>
          (!q ||
            [
              item.name,
              item.title,
              item.prompt,
              item.answer,
              item.feedback,
              item.questionSnapshot?.title,
            ].some((value) => value?.toLowerCase().includes(q))) &&
          (!profileId ||
            (kind === "attempts"
              ? find(snapshot.value, "sessions", item.sessionId).profileId
              : item.profileId) === profileId) &&
          (!sessionId || item.sessionId === sessionId) &&
          (!status || item.status === status) &&
          (archived === null || item.archived === (archived === "true")),
      );
      items = items
        .slice()
        .sort(
          (a, b) =>
            b.updatedAt.localeCompare(a.updatedAt) || a.id.localeCompare(b.id),
        );
      return {
        items: structuredClone(
          items.slice((page - 1) * pageSize, page * pageSize),
        ),
        total: items.length,
        page,
        pageSize,
        revision: snapshot.revision,
      };
    },
  };
}
module.exports = {
  createService,
  createState,
  authenticate,
  bootstrap,
  payload,
  validateState,
  KINDS,
  LIMITS,
};
