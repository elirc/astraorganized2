import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'master3'; P = fe.REG[S]['abs']; os.chdir(P); done = []
SVC = 'apps/api/src/modules/tickets/ticketService.ts'

# review#2: P2034 retry wrapper around every serializable transaction
def svc(t):
    if 'withSerializableRetry' in t: return t
    helper = '''
const SERIALIZATION_FAILURE = "P2034";

/**
 * Serializable transactions are allowed to fail with a serialization error when two of them
 * touch the same rows; PostgreSQL expects the caller to retry. Without this wrapper the
 * isolation level is a promise the code cannot keep under contention: the second writer
 * would surface a 500. HttpErrors and every other failure pass through untouched.
 */
export async function withSerializableRetry<T>(work: () => Promise<T>, attempts = 3): Promise<T> {
  for (let attempt = 1; ; attempt += 1) {
    try {
      return await work();
    } catch (error) {
      const retryable = error instanceof Prisma.PrismaClientKnownRequestError && error.code === SERIALIZATION_FAILURE;
      if (!retryable || attempt >= attempts) throw error;
    }
  }
}
'''
    open_pat = '  return prisma.$transaction(async (tx) => {'
    close_ser = '  }, { isolationLevel: Prisma.TransactionIsolationLevel.Serializable });'
    out = []; pos = 0; wrapped = 0
    while True:
        a = t.find(open_pat, pos)
        if a < 0: break
        b = t.find(close_ser, a)
        b_plain = t.find('\n  });', a)
        if b < 0 or (0 <= b_plain < b):
            out.append(t[pos:a + len(open_pat)]); pos = a + len(open_pat); continue  # not serializable; copy through untouched
        out.append(t[pos:a]); out.append('  return withSerializableRetry(() => prisma.$transaction(async (tx) => {')
        out.append(t[a + len(open_pat):b]); out.append('  }, { isolationLevel: Prisma.TransactionIsolationLevel.Serializable }));')
        pos = b + len(close_ser); wrapped += 1
    out.append(t[pos:]); t = ''.join(out)
    assert wrapped >= 2, wrapped
    # insert helper after the imports
    idx = t.find('\n\n', t.rfind('\nimport '))
    t = t[:idx] + '\n' + helper + t[idx:]
    return t
fe.rw(SVC, svc)
def tests(t):
    if 'serializable transactions retry on P2034' in t: return t
    add = '''
describe("serializable transactions retry on P2034", () => {
  const serializationFailure = () =>
    new Prisma.PrismaClientKnownRequestError("could not serialize access", { code: "P2034", clientVersion: "test" });

  beforeEach(() => {
    vi.clearAllMocks();
    mocks.prisma.ticket.findFirst.mockResolvedValue({ id: "ticket-1", status: "NEW", priority: "NORMAL", assignedUserId: null });
    mocks.txTicketUpdate.mockResolvedValue({
      id: "ticket-1", status: "NEW", priority: "URGENT", slaDueAt: null, customer: { company: null }, assignedUser: null, comments: []
    });
    mocks.txAuditCreate.mockResolvedValue({});
    mocks.txOutboxCreate.mockResolvedValue({});
    mocks.prisma.$transaction.mockImplementation(async (callback: (tx: unknown) => unknown) =>
      callback({
        ticket: { update: mocks.txTicketUpdate },
        auditLog: { create: mocks.txAuditCreate },
        outboxEvent: { create: mocks.txOutboxCreate }
      }));
  });

  it("retries once after a serialization failure and then succeeds", async () => {
    mocks.prisma.$transaction.mockRejectedValueOnce(serializationFailure());
    await expect(updateTicket(agent, "ticket-1", { priority: "URGENT" })).resolves.toBeTruthy();
    expect(mocks.prisma.$transaction).toHaveBeenCalledTimes(2);
  });

  it("gives up after three serialization failures and surfaces the last one", async () => {
    mocks.prisma.$transaction
      .mockRejectedValueOnce(serializationFailure())
      .mockRejectedValueOnce(serializationFailure())
      .mockRejectedValueOnce(serializationFailure());
    await expect(updateTicket(agent, "ticket-1", { priority: "URGENT" })).rejects.toMatchObject({ code: "P2034" });
    expect(mocks.prisma.$transaction).toHaveBeenCalledTimes(3);
  });

  it("does not retry other database errors", async () => {
    mocks.prisma.$transaction.mockRejectedValueOnce(
      new Prisma.PrismaClientKnownRequestError("unique", { code: "P2002", clientVersion: "test" })
    );
    await expect(updateTicket(agent, "ticket-1", { priority: "URGENT" })).rejects.toMatchObject({ code: "P2002" });
    expect(mocks.prisma.$transaction).toHaveBeenCalledTimes(1);
  });
});
'''
    if 'import { Prisma } from "@prisma/client";' not in t:
        t = t.replace('import { beforeEach, describe, expect, it, vi } from "vitest";', 'import { beforeEach, describe, expect, it, vi } from "vitest";\nimport { Prisma } from "@prisma/client";', 1)
    return t.rstrip('\n') + '\n' + add
fe.rw('tests/api/ticket-service.test.ts', tests)
done.append('review#2 withSerializableRetry (3 attempts, P2034 only) wraps every Serializable $transaction in ticketService; three unit tests (retry-then-succeed, give up after three, no retry for P2002)')
if 'Serializable means' not in open('astraupskill/02-CONCEPTS.md', encoding='utf-8-sig').read():
    fe.append_section(S, '02', '## Serializable means "retry", or it means nothing', """`Serializable` is the isolation level that lets PostgreSQL refuse a commit whose result could not have come from some serial order of the concurrent transactions. The refusal is an error (`40001`, which Prisma reports as `P2034`), and the contract is that the *application* retries. The delivered service asked for `Serializable` and never retried, so under contention the second writer would have answered 500. `withSerializableRetry` in `ticketService.ts` (fix pass) re-runs the whole transaction callback up to three times on `P2034` and nothing else: an `HttpError` (403, 404, 409) is a decision, not contention, and a `P2002` unique violation will not go away by retrying. Predict before reading the tests: if the callback has already created an audit row when the serialization failure arrives, how many audit rows exist after a successful retry? (One: the failed attempt rolled back with its transaction.)""", before='## ')

# review#4: subheadings + predict prompts (02 and 03)
def heads(t, plan):
    paras = t.split('\n\n'); out = [paras[0]]; i = 1
    for body in paras[1:]:
        if i - 1 < len(plan) and not body.startswith('#') and not body.startswith('```'):
            title, predict = plan[i - 1]
            out.append(f'## {title}\n\n**Predict before you read on:** {predict}\n\n{body}'); i += 1
        else:
            out.append(body)
    return '\n\n'.join(out)
fe.rw('astraupskill/02-CONCEPTS.md', lambda t: heads(t, [
    ('Authentication and authorization are two decisions', 'a viewer sends a PATCH with only `priority`; which layer refuses it, and what has been read from the database by then?'),
    ('Tenant scope is part of every lookup', 'a valid ticket id from tenant B is used with a tenant A session; 403, 404 or 200?'),
    ('Comment visibility is response policy', 'which of GET and PATCH returned the internal note before the repair, and why did they differ?'),
    ('Accepted writes are one transaction', 'the outbox insert fails after the ticket update; what does the client see, and does the audit row exist?'),
]))
fe.rw('astraupskill/03-WORKED-CHANGE.md', lambda t: heads(t, [
    ('Two symptoms, one cause', 'name the two symptoms before reading; is the missing check in the route or the service?'),
    ('The role gate comes first', 'why must the gate run before `findFirst` and not after?'),
    ('The response is shaped by role', 'what changes for an agent, and what changes for a viewer, when `ticketInclude` becomes `ticketIncludeForRole`?'),
    ('Walk the three requests', 'for viewer PATCH, agent PATCH and viewer GET, write the status code and the number of audit rows created.'),
    ('What the patch leaves alone', 'does `createTicket` get a role gate in this change? Why might that be deferred?'),
]))
done.append('review#4 02 and 03 split into ## sections, each opening with a "Predict before you read on" prompt')

# review#3: run it yourself
port = '5432'
m = re.search(r'"(\d+):5432"', open('docker-compose.yml', encoding='utf-8-sig').read())
if m: port = m.group(1)
if 'Run it yourself' not in open('astraupskill/VERIFICATION.md', encoding='utf-8-sig').read():
    fe.append_section(S, 'VERIFICATION', '## Run it yourself', f"""```powershell
docker compose up -d                          # PostgreSQL on localhost:{port} (support/support, db support_desk)
Copy-Item .env.example .env                   # DATABASE_URL points at that container
npm install
npx prisma migrate dev                        # or: npx prisma db push
npm run seed                                  # tenant acme-support, viewer@acme.test, agent@acme.test, ticket t1
npm run dev                                   # API + web + worker; the API listens on the port printed in the terminal (see apps/api)
```

Then, with the API port in `$port` and a ticket id from the seed output in `$ticket`:

```powershell
# viewer PATCH -> 403, no audit row, no outbox event
curl -i -X PATCH "http://localhost:$port/api/tickets/$ticket" -H "content-type: application/json" -H "x-tenant-slug: acme-support" -H "x-user-email: viewer@acme.test" -d '{{"priority":"URGENT"}}'
# agent PATCH -> 200, one ticket.updated audit row, one outbox event, comments filtered for the agent
curl -i -X PATCH "http://localhost:$port/api/tickets/$ticket" -H "content-type: application/json" -H "x-tenant-slug: acme-support" -H "x-user-email: agent@acme.test" -d '{{"priority":"URGENT"}}'
```

Check the rows with `npx prisma studio` or `SELECT action, count(*) FROM "AuditLog" GROUP BY 1;`.""", before='## ')
done.append('review#3 VERIFICATION "Run it yourself": compose, migrate, seed, dev, two curl commands')

# review#1: integration test (guarded)
os.makedirs('tests/integration', exist_ok=True)
open('tests/integration/ticket-patch.int.test.ts', 'w', encoding='utf-8', newline='\n').write('''import { afterAll, beforeAll, describe, expect, it } from "vitest";

// Runs only against a disposable PostgreSQL with the schema pushed:
//   docker run --rm -d -e POSTGRES_PASSWORD=local-test -p 5433:5432 postgres:18
//   $env:TEST_DATABASE_URL = "postgresql://postgres:local-test@127.0.0.1:5433/postgres"
//   $env:DATABASE_URL = $env:TEST_DATABASE_URL; npx prisma db push
//   npx vitest run tests/integration
const url = process.env.TEST_DATABASE_URL;

describe.skipIf(!url)("ticket PATCH against a real database", () => {
  let prisma: import("@prisma/client").PrismaClient;
  let svc: typeof import("../../apps/api/src/modules/tickets/ticketService");
  let tenantA: string, tenantB: string, ticketId: string, viewerId: string, agentId: string;

  beforeAll(async () => {
    process.env.DATABASE_URL = url;
    const { PrismaClient } = await import("@prisma/client");
    prisma = new PrismaClient({ datasources: { db: { url } } });
    svc = await import("../../apps/api/src/modules/tickets/ticketService");
    const stamp = Date.now().toString(36);
    const a = await prisma.tenant.create({ data: { name: "A " + stamp, slug: "int-a-" + stamp } });
    const b = await prisma.tenant.create({ data: { name: "B " + stamp, slug: "int-b-" + stamp } });
    tenantA = a.id; tenantB = b.id;
    const viewer = await prisma.user.create({ data: { tenantId: tenantA, name: "Viewer", email: "viewer@" + stamp, role: "VIEWER" } });
    const agent = await prisma.user.create({ data: { tenantId: tenantA, name: "Agent", email: "agent@" + stamp, role: "AGENT" } });
    viewerId = viewer.id; agentId = agent.id;
    const customer = await prisma.customer.create({ data: { tenantId: tenantA, name: "C", email: "c@" + stamp } });
    const ticket = await prisma.ticket.create({ data: { tenantId: tenantA, customerId: customer.id, number: 1001, subject: "s", description: "d" } });
    ticketId = ticket.id;
    await prisma.ticketComment.createMany({ data: [
      { tenantId: tenantA, ticketId, authorId: agent.id, visibility: "PUBLIC", body: "public" },
      { tenantId: tenantA, ticketId, authorId: agent.id, visibility: "INTERNAL", body: "internal" },
    ] });
  });

  afterAll(async () => {
    if (!prisma) return;
    await prisma.outboxEvent.deleteMany({ where: { tenantId: { in: [tenantA, tenantB] } } });
    await prisma.auditLog.deleteMany({ where: { tenantId: { in: [tenantA, tenantB] } } });
    await prisma.ticketComment.deleteMany({ where: { tenantId: { in: [tenantA, tenantB] } } });
    await prisma.ticket.deleteMany({ where: { tenantId: { in: [tenantA, tenantB] } } });
    await prisma.customer.deleteMany({ where: { tenantId: { in: [tenantA, tenantB] } } });
    await prisma.user.deleteMany({ where: { tenantId: { in: [tenantA, tenantB] } } });
    await prisma.tenant.deleteMany({ where: { id: { in: [tenantA, tenantB] } } });
    await prisma.$disconnect();
  });

  const counts = async () => ({
    audit: await prisma.auditLog.count({ where: { tenantId: tenantA } }),
    outbox: await prisma.outboxEvent.count({ where: { tenantId: tenantA } }),
  });

  it("three viewer PATCH shapes write nothing; an agent PATCH writes exactly one audit row and one outbox event", async () => {
    const viewer = { tenantId: tenantA, userId: viewerId, role: "VIEWER" as const, email: "v" };
    const agent = { tenantId: tenantA, userId: agentId, role: "AGENT" as const, email: "a" };
    const before = await counts();
    for (const input of [{ priority: "URGENT" as const }, { tags: ["billing"] }, {}]) {
      await expect(svc.updateTicket(viewer, ticketId, input)).rejects.toMatchObject({ status: 403 });
      expect(await counts()).toEqual(before);
    }
    const updated = await svc.updateTicket(agent, ticketId, { priority: "URGENT" });
    expect(updated.priority).toBe("URGENT");
    expect(updated.comments.map((c: { visibility: string }) => c.visibility).sort()).toEqual(["INTERNAL", "PUBLIC"]);
    const after = await counts();
    expect(after).toEqual({ audit: before.audit + 1, outbox: before.outbox + 1 });
  });

  it("a ticket id from another tenant is a 404 for an agent of tenant A", async () => {
    const other = await prisma.customer.create({ data: { tenantId: tenantB, name: "O", email: "o@" + tenantB } });
    const foreign = await prisma.ticket.create({ data: { tenantId: tenantB, customerId: other.id, number: 1001, subject: "f", description: "f" } });
    const agent = { tenantId: tenantA, userId: agentId, role: "AGENT" as const, email: "a" };
    await expect(svc.updateTicket(agent, foreign.id, { priority: "LOW" })).rejects.toMatchObject({ status: 404 });
  });
});
''')
done.append('review#1 tests/integration/ticket-patch.int.test.ts written (skips unless TEST_DATABASE_URL is set): two tenants, one ticket, PUBLIC+INTERNAL comments, three viewer shapes leave audit/outbox counts unchanged, agent PATCH adds exactly one of each, cross-tenant id is 404')
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w')); print('\n'.join(done))
