import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'buildcrmpyjs'; P = fe.REG[S]['abs']; os.chdir(P); done = []
B = 'backend/'
def w(path, text):
    open(path, 'w', encoding='utf-8', newline='\n').write(text)

# review#2: explicit rejection message for role
def schema(t):
    old = '  role: z.never().optional()\n}).strict();'
    new = '''  role: z.unknown().optional()
}).strict().superRefine((value, ctx) => {
  if ("role" in value && value.role !== undefined) {
    ctx.addIssue({ code: z.ZodIssueCode.custom, path: ["role"], message: "role cannot be set during registration" });
  }
});'''
    if 'role cannot be set during registration' in t: return t
    assert old in t
    return t.replace(old, new, 1)
fe.rw(B + 'src/modules/auth/auth.schemas.ts', schema)
def authtest(t):
    old = '''    expect(response.status).toBe(400);
    expect(prismaMock.user.create).not.toHaveBeenCalled();
  });

  it("assigns READ_ONLY'''
    new = '''    expect(response.status).toBe(400);
    expect(JSON.stringify(response.body.errors)).toContain("role cannot be set during registration");
    expect(prismaMock.user.create).not.toHaveBeenCalled();
  });

  it("assigns READ_ONLY'''
    if 'role cannot be set during registration' in t: return t
    assert old in t
    return t.replace(old, new, 1)
fe.rw(B + 'src/app.test.ts', authtest)
done.append('review#2 registerSchema rejects role with the message "role cannot be set during registration" (superRefine); the existing test asserts the message')

# review#1: one owned CRUD resource end to end
w(B + 'src/auth/permissions.ts', open(B + 'src/auth/permissions.ts', encoding='utf-8-sig').read().replace('  "dashboard:view",\n  "audit:view"\n] as const;', '  "dashboard:view",\n  "audit:view",\n  "contacts:write"\n] as const;', 1)
  .replace('  SYSTEM_ADMIN: [...permissions],', '  SYSTEM_ADMIN: [...permissions],', 1)
  .replace('    "opportunities:edit:any",\n    "dashboard:view",\n    "audit:view"\n  ],', '    "opportunities:edit:any",\n    "dashboard:view",\n    "audit:view",\n    "contacts:write"\n  ],', 1)
  .replace('    "opportunities:edit:own",\n    "dashboard:view"\n  ],', '    "opportunities:edit:own",\n    "dashboard:view",\n    "contacts:write"\n  ],', 1)
  .replace('    "opportunities:create",\n    "dashboard:view"\n  ],\n  EXECUTIVE_VIEWER', '    "opportunities:create",\n    "dashboard:view",\n    "contacts:write"\n  ],\n  EXECUTIVE_VIEWER', 1))
assert open(B + 'src/auth/permissions.ts', encoding='utf-8-sig').read().count('contacts:write') == 4, 'permission not wired into the list + three explicit writer roles (SYSTEM_ADMIN spreads)'
os.makedirs(B + 'src/modules/contacts', exist_ok=True)
w(B + 'src/modules/contacts/contacts.schemas.ts', '''import { z } from "zod";

const optionalText = (max: number) => z.string().trim().max(max).optional();

export const createContactSchema = z.object({
  firstName: z.string().trim().min(1).max(60),
  lastName: z.string().trim().min(1).max(60),
  email: z.string().trim().email().max(120).optional(),
  phone: optionalText(40),
  jobTitle: optionalText(80),
  companyId: z.string().uuid().optional()
}).strict();

// PATCH: every field optional, but at least one must be present, and unknown keys are still refused.
export const updateContactSchema = createContactSchema.partial().strict().refine(
  (value) => Object.values(value).some((field) => field !== undefined),
  { message: "At least one field must be provided" }
);

export const listContactsQuerySchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  pageSize: z.coerce.number().int().min(1).max(100).default(20),
  q: z.string().trim().max(120).optional()
});

export type CreateContactInput = z.infer<typeof createContactSchema>;
export type UpdateContactInput = z.infer<typeof updateContactSchema>;
export type ListContactsQuery = z.infer<typeof listContactsQuerySchema>;
''')
w(B + 'src/modules/contacts/contacts.service.ts', '''import { Prisma } from "@prisma/client";

import { prisma } from "../../db/prisma.js";
import { AppError } from "../../shared/errors/AppError.js";
import type { CreateContactInput, ListContactsQuery, UpdateContactInput } from "./contacts.schemas.js";

// Output allowlist: the API never leaks columns it did not decide to publish (same idea as toPublicUser).
export const contactSelect = {
  id: true, firstName: true, lastName: true, email: true, phone: true, jobTitle: true,
  companyId: true, createdAt: true, updatedAt: true
} satisfies Prisma.ContactSelect;

function notFound(): never {
  // 404, not 403: a caller who is allowed to read contacts learns nothing extra from "it exists but is deleted".
  throw new AppError("Contact not found", 404, "CONTACT_NOT_FOUND");
}

export class ContactsService {
  async list(query: ListContactsQuery) {
    const where: Prisma.ContactWhereInput = { deletedAt: null };
    if (query.q) {
      where.OR = [
        { firstName: { contains: query.q, mode: "insensitive" } },
        { lastName: { contains: query.q, mode: "insensitive" } },
        { email: { contains: query.q, mode: "insensitive" } }
      ];
    }
    const [total, items] = await Promise.all([
      prisma.contact.count({ where }),
      prisma.contact.findMany({
        where, select: contactSelect,
        orderBy: [{ lastName: "asc" }, { firstName: "asc" }],
        skip: (query.page - 1) * query.pageSize, take: query.pageSize
      })
    ]);
    // Clamp: asking for a page past the end returns an empty list, never an error.
    return { items, page: query.page, pageSize: query.pageSize, total, pageCount: Math.max(1, Math.ceil(total / query.pageSize)) };
  }

  async get(id: string) {
    const contact = await prisma.contact.findFirst({ where: { id, deletedAt: null }, select: contactSelect });
    return contact ?? notFound();
  }

  async create(input: CreateContactInput) {
    try {
      return await prisma.contact.create({ data: input, select: contactSelect });
    } catch (error) {
      // A foreign-key failure (P2003) means the companyId names a company that does not exist.
      if (error instanceof Prisma.PrismaClientKnownRequestError && error.code === "P2003") {
        throw new AppError("Company not found", 400, "COMPANY_NOT_FOUND");
      }
      throw error;
    }
  }

  async update(id: string, input: UpdateContactInput) {
    // updateMany carries the "not deleted" predicate; a count of 0 is the 404, with no read-then-write race.
    const result = await prisma.contact.updateMany({ where: { id, deletedAt: null }, data: input });
    if (result.count === 0) notFound();
    return this.get(id);
  }

  async remove(id: string, now = new Date()) {
    // Soft delete: notes, tasks and opportunities keep their reference; the row simply stops being listed.
    const result = await prisma.contact.updateMany({ where: { id, deletedAt: null }, data: { deletedAt: now } });
    if (result.count === 0) notFound();
  }
}

export const contactsService = new ContactsService();
''')
w(B + 'src/modules/contacts/contacts.controller.ts', '''import type { Request, Response } from "express";

import { contactsService } from "./contacts.service.js";
import { listContactsQuerySchema } from "./contacts.schemas.js";

export class ContactsController {
  async list(req: Request, res: Response) {
    const query = listContactsQuerySchema.parse(req.query);
    res.json(await contactsService.list(query));
  }

  async get(req: Request, res: Response) {
    res.json(await contactsService.get(String(req.params.id)));
  }

  async create(req: Request, res: Response) {
    res.status(201).json(await contactsService.create(req.body));
  }

  async update(req: Request, res: Response) {
    res.json(await contactsService.update(String(req.params.id), req.body));
  }

  async remove(req: Request, res: Response) {
    await contactsService.remove(String(req.params.id));
    res.status(204).send();
  }
}

export const contactsController = new ContactsController();
''')
w(B + 'src/modules/contacts/contacts.routes.ts', '''import type { NextFunction, Request, Response } from "express";
import { Router } from "express";
import { ZodError, type ZodTypeAny } from "zod";

import { authMiddleware } from "../../middleware/auth.middleware.js";
import { requirePermission } from "../../middleware/requirePermission.middleware.js";
import { asyncHandler } from "../../shared/utils/asyncHandler.js";
import { contactsController } from "./contacts.controller.js";
import { createContactSchema, updateContactSchema } from "./contacts.schemas.js";

function validateBody(schema: ZodTypeAny) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      return res.status(400).json({ message: "Validation failed", errors: result.error.flatten() });
    }
    req.body = result.data;
    return next();
  };
}

// Query-string validation failures thrown by the controller become the same 400 shape.
function zodQueryErrors(error: unknown, _req: Request, res: Response, next: NextFunction) {
  if (error instanceof ZodError) {
    return res.status(400).json({ message: "Validation failed", errors: error.flatten() });
  }
  return next(error);
}

export const contactsRouter = Router();

// Every route requires a valid access token; the READ_ONLY role can read, writers need contacts:write.
contactsRouter.use(authMiddleware);
contactsRouter.get("/", asyncHandler(contactsController.list.bind(contactsController)));
contactsRouter.get("/:id", asyncHandler(contactsController.get.bind(contactsController)));
contactsRouter.post("/", requirePermission("contacts:write"), validateBody(createContactSchema), asyncHandler(contactsController.create.bind(contactsController)));
contactsRouter.patch("/:id", requirePermission("contacts:write"), validateBody(updateContactSchema), asyncHandler(contactsController.update.bind(contactsController)));
contactsRouter.delete("/:id", requirePermission("contacts:write"), asyncHandler(contactsController.remove.bind(contactsController)));
contactsRouter.use(zodQueryErrors);
''')
def app(t):
    t = t.replace('import { authRouter } from "./modules/auth/auth.routes.js";', 'import { authRouter } from "./modules/auth/auth.routes.js";\nimport { contactsRouter } from "./modules/contacts/contacts.routes.js";', 1)
    t = t.replace('app.use("/api/auth", authRouter);', 'app.use("/api/auth", authRouter);\napp.use("/api/contacts", contactsRouter);', 1)
    assert 'contactsRouter' in t
    return t
fe.rw(B + 'src/app.ts', app)
w(B + 'src/modules/contacts/contacts.test.ts', '''import request from "supertest";
import { describe, expect, it, vi, beforeEach } from "vitest";
import { Prisma } from "@prisma/client";

const { prismaMock } = vi.hoisted(() => ({
  prismaMock: {
    $queryRaw: vi.fn(),
    user: { findUnique: vi.fn(), create: vi.fn() },
    refreshToken: { findUnique: vi.fn(), create: vi.fn(), updateMany: vi.fn() },
    contact: { findMany: vi.fn(), findFirst: vi.fn(), count: vi.fn(), create: vi.fn(), updateMany: vi.fn() }
  }
}));
vi.mock("../../db/prisma.js", () => ({ prisma: prismaMock }));
import { app } from "../../app.js";
import { signAccessToken } from "../../shared/utils/jwt.js";

const contact = {
  id: "1a2b3c4d-0000-4000-8000-000000000001", firstName: "Ada", lastName: "Lovelace", email: "ada@example.com",
  phone: null, jobTitle: "Analyst", companyId: null, createdAt: new Date("2026-01-01T00:00:00Z"), updatedAt: new Date("2026-01-01T00:00:00Z")
};
const bearer = (role: string) => `Bearer ${signAccessToken({ sub: "user-1", email: "u@example.com", role })}`;

describe("contacts CRUD: auth, role, validation, 404 vs 403, pagination", () => {
  beforeEach(() => { vi.resetAllMocks(); });

  it("refuses anonymous callers with 401 before touching the database", async () => {
    const response = await request(app).get("/api/contacts");
    expect(response.status).toBe(401);
    expect(prismaMock.contact.findMany).not.toHaveBeenCalled();
  });

  it("lets READ_ONLY list with clamped pagination and hides deleted rows", async () => {
    prismaMock.contact.count.mockResolvedValue(1);
    prismaMock.contact.findMany.mockResolvedValue([contact]);
    const response = await request(app).get("/api/contacts?page=5&pageSize=500").set("authorization", bearer("READ_ONLY"));
    expect(response.status).toBe(400); // pageSize above the maximum is a validation error, not a silent clamp
    const ok = await request(app).get("/api/contacts?page=5&pageSize=10&q=ada").set("authorization", bearer("READ_ONLY"));
    expect(ok.status).toBe(200);
    expect(ok.body).toMatchObject({ page: 5, pageSize: 10, total: 1, pageCount: 1, items: [{ id: contact.id, firstName: "Ada" }] });
    expect(prismaMock.contact.findMany).toHaveBeenCalledWith(expect.objectContaining({
      where: expect.objectContaining({ deletedAt: null }), skip: 40, take: 10
    }));
  });

  it("answers 403 to a READ_ONLY write and never calls create", async () => {
    const response = await request(app).post("/api/contacts").set("authorization", bearer("READ_ONLY"))
      .send({ firstName: "Ada", lastName: "Lovelace" });
    expect(response.status).toBe(403);
    expect(prismaMock.contact.create).not.toHaveBeenCalled();
  });

  it("validates the body before the service runs and creates with the output allowlist", async () => {
    const bad = await request(app).post("/api/contacts").set("authorization", bearer("SALES_REP"))
      .send({ firstName: "", lastName: "Lovelace", passwordHash: "x" });
    expect(bad.status).toBe(400);
    expect(prismaMock.contact.create).not.toHaveBeenCalled();

    prismaMock.contact.create.mockResolvedValue(contact);
    const good = await request(app).post("/api/contacts").set("authorization", bearer("SALES_REP"))
      .send({ firstName: "Ada", lastName: "Lovelace", email: "ada@example.com" });
    expect(good.status).toBe(201);
    expect(good.body.id).toBe(contact.id);
    expect(prismaMock.contact.create).toHaveBeenCalledWith(expect.objectContaining({ select: expect.objectContaining({ id: true }) }));
  });

  it("maps a missing company (P2003) to a readable 400", async () => {
    prismaMock.contact.create.mockRejectedValue(new Prisma.PrismaClientKnownRequestError("fk", { code: "P2003", clientVersion: "test" }));
    const response = await request(app).post("/api/contacts").set("authorization", bearer("SALES_MANAGER"))
      .send({ firstName: "Ada", lastName: "Lovelace", companyId: "1a2b3c4d-0000-4000-8000-000000000009" });
    expect(response.status).toBe(400);
    expect(response.body.code).toBe("COMPANY_NOT_FOUND");
  });

  it("updates through a conditional updateMany: count 0 is a 404, a hit re-reads the row", async () => {
    prismaMock.contact.updateMany.mockResolvedValue({ count: 0 });
    const missing = await request(app).patch(`/api/contacts/${contact.id}`).set("authorization", bearer("SALES_REP")).send({ jobTitle: "Lead" });
    expect(missing.status).toBe(404);

    prismaMock.contact.updateMany.mockResolvedValue({ count: 1 });
    prismaMock.contact.findFirst.mockResolvedValue({ ...contact, jobTitle: "Lead" });
    const hit = await request(app).patch(`/api/contacts/${contact.id}`).set("authorization", bearer("SALES_REP")).send({ jobTitle: "Lead" });
    expect(hit.status).toBe(200);
    expect(hit.body.jobTitle).toBe("Lead");
    expect(prismaMock.contact.updateMany).toHaveBeenLastCalledWith({ where: { id: contact.id, deletedAt: null }, data: { jobTitle: "Lead" } });

    const empty = await request(app).patch(`/api/contacts/${contact.id}`).set("authorization", bearer("SALES_REP")).send({});
    expect(empty.status).toBe(400);
  });

  it("soft-deletes with 204 and a second delete is 404, not 403", async () => {
    prismaMock.contact.updateMany.mockResolvedValueOnce({ count: 1 }).mockResolvedValueOnce({ count: 0 });
    const first = await request(app).delete(`/api/contacts/${contact.id}`).set("authorization", bearer("ACCOUNT_MANAGER"));
    expect(first.status).toBe(204);
    const second = await request(app).delete(`/api/contacts/${contact.id}`).set("authorization", bearer("ACCOUNT_MANAGER"));
    expect(second.status).toBe(404);
    expect(prismaMock.contact.updateMany).toHaveBeenCalledWith(expect.objectContaining({ data: { deletedAt: expect.any(Date) } }));
  });
});
''')
done.append('review#1 contacts module (schemas, service, controller, routes) mounted at /api/contacts: Zod validation, authMiddleware + contacts:write permission for writers (READ_ONLY reads only), pagination with validated bounds, soft delete, conditional updateMany, P2003 -> 400, output allowlist; 7 supertest tests in contacts.test.ts')

# review#3: admin provisioning
fe.append_section(S, '03', '## The operational consequence: who makes the first admin?', """Hardcoding `role: "READ_ONLY"` at registration means nobody can register as an administrator, which is the point. It also means the first `SYSTEM_ADMIN` must come from somewhere else. This project's answer is `backend/prisma/seed.ts` (`npx prisma db seed`, wired in `package.json` under `"prisma": { "seed": "tsx prisma/seed.ts" }`): it upserts one `SYSTEM_ADMIN` and one user per other role with known credentials for local development. In production the same job is a one-off CLI or migration that reads the admin password from a secret, never a public route. Promotion after that goes through a `users:manage` route that an existing admin calls, which is exercise material: the permission exists in `src/auth/permissions.ts` and no route uses it yet.""", before='## ')
done.append('review#3 03 explains admin provisioning via prisma/seed.ts and the users:manage gap')

# review#4 TOCTOU, review#6 glossary (02); review#5 harness walk-through (04)
fe.append_section(S, '02', '## Read-then-write is advisory; the unique index is the guard', """`register` calls `findUnique` and answers 409 if the email exists, then `create`s. Between those two statements another request can insert the same email: the check is a *time-of-check to time-of-use* (TOCTOU) race. The database's unique index on `User.email` is the real guard, and the `catch` that maps Prisma's `P2002` to the same 409 is what turns the race into a correct answer instead of a 500. Keep the pre-check for the friendly fast path; never rely on it for correctness. The same pattern appears in the new contacts module: `updateMany` with `deletedAt: null` in its `where` replaces a `findFirst` then `update` pair, so a concurrent delete cannot slip between them.

## Glossary

*Trust boundary*: the line between data the server produced and data a caller sent. *Output allowlist / projection*: the `select` (or `toPublicUser`) that decides which columns leave the server. *JWT claim*: a field inside the signed token (`sub`, `role`); trustworthy only because the signature is verified. *Algorithm confusion*: accepting a token whose header names a weaker algorithm than the one you sign with; pin the algorithm on verify. *Hoisted module mock*: `vi.hoisted` + `vi.mock` so the fake Prisma client exists before the app module imports the real one. *TOCTOU*: see above. *401 vs 403 vs 404*: no valid identity; valid identity without permission; resource not visible to this caller (also used to avoid confirming existence).""")
fe.append_section(S, '04', '## How the harness works, line by line', """```ts
const { prismaMock } = vi.hoisted(() => ({ prismaMock: { user: { findUnique: vi.fn(), create: vi.fn() }, ... } }));
vi.mock("./db/prisma.js", () => ({ prisma: prismaMock }));
import { app } from "./app.js";
```

- `vi.mock` calls are hoisted above every import by Vitest, so `app.js` (and through it `auth.service.js`) receives the fake. Anything the factory closes over must *also* be hoisted, which is what `vi.hoisted` provides; a plain `const prismaMock = ...` would be referenced before it exists.
- The mocked path is `"./db/prisma.js"` with the `.js` extension because this package uses NodeNext resolution: source files import each other by their emitted `.js` names, and the mock key must match the specifier the importing module uses, character for character.
- `mockResolvedValue` answers every call the same way until `vi.resetAllMocks()` in `beforeEach`; `mockResolvedValueOnce` queues answers in order, so the contacts delete test can say "first `updateMany` returns count 1, the second count 0" and the queue drains across the two requests.
- `supertest` drives the real Express app in process: middleware order, the error handler and the JSON shapes are all real; only Prisma is replaced.

Run one file: `npx vitest run src/modules/contacts/contacts.test.ts`.""", before='## ')
done.append('review#4 02 TOCTOU paragraph; review#6 02 glossary; review#5 04 harness walk-through (vi.hoisted, .js specifier, Once-queueing, supertest)')

# chapter for the new resource + README link
w('astraupskill/08-CRUD-CONTACTS.md', """# 08. The house behind the gate: contacts CRUD

[Course index](README.md)

The auth chapters build the gate. This chapter walks one owned resource through it, end to end, so you see every CRUD concern in one place: `backend/src/modules/contacts/`.

## The route table

| method | path | who | validation | success | failure |
|---|---|---|---|---|---|
| GET | `/api/contacts?page&pageSize&q` | any signed-in role | query schema (page >= 1, pageSize 1..100) | 200 `{ items, page, pageSize, total, pageCount }` | 400 bad query, 401 |
| GET | `/api/contacts/:id` | any signed-in role | none | 200 contact | 404 (also for soft-deleted) |
| POST | `/api/contacts` | `contacts:write` | `createContactSchema` (strict) | 201 contact | 400, 401, 403 |
| PATCH | `/api/contacts/:id` | `contacts:write` | `updateContactSchema` (partial, at least one field) | 200 contact | 400, 401, 403, 404 |
| DELETE | `/api/contacts/:id` | `contacts:write` | none | 204 | 401, 403, 404 |

## Decisions worth copying

1. **Authorization before validation.** `requirePermission` runs before `validateBody`, so a READ_ONLY caller gets 403 without learning what a valid body looks like.
2. **404 over 403 for hidden rows.** A soft-deleted or unknown id is 404 for everyone who can read contacts; there is no "exists but you may not see it" answer to enumerate.
3. **Conditional writes.** `updateMany({ where: { id, deletedAt: null } })` returns a count; 0 is the 404. No `findFirst` then `update` pair, so no window for a concurrent delete.
4. **Soft delete.** Notes, tasks and opportunities reference contacts; `deletedAt` keeps those references valid and the row out of every list.
5. **Output allowlist.** `contactSelect` decides what leaves the server, the same way `toPublicUser` does for users.
6. **Foreign key failures are 400 with a code.** `P2003` on `companyId` becomes `COMPANY_NOT_FOUND`, not a 500.

## Exercises

1. **Ownership.** Add `ownerId` to `Contact` (migration), set it from `req.user.id` on create, and make PATCH/DELETE require either ownership or `opportunities:edit:any`. Acceptance: a SALES_REP editing another rep's contact gets 404 (not 403), a SALES_MANAGER succeeds, and the test proves `updateMany` carried the owner predicate.
2. **Restore.** Add `POST /api/contacts/:id/restore` for `SYSTEM_ADMIN` only. Acceptance: restoring a live contact is 409; restoring a deleted one is 200 and it reappears in the list.
3. **Cursor pagination.** Replace page/pageSize with a `cursor` on `(lastName, id)`. Acceptance: inserting a row between two requests never duplicates or skips an item (write the test with three rows and a cursor in the middle).
4. **Red first.** Delete the `deletedAt: null` predicate from `get` and run the suite; write down which test fails and why, then restore it.
""")
fe.rw('astraupskill/README.md', lambda t: t.rstrip('\n') + '\n\n## Chapter 8: the house behind the gate\n\n[08-CRUD-CONTACTS.md](08-CRUD-CONTACTS.md) implements one owned resource (`/api/contacts`) end to end through the auth gate: validation, role check, 404-vs-403, pagination, soft delete, conditional writes. Run its tests with `npx vitest run src/modules/contacts/contacts.test.ts` from `backend/`.\n')
done.append('review#1 08-CRUD-CONTACTS.md chapter (route table, six decisions, four exercises) linked from README')
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w')); print('\n'.join(done))
