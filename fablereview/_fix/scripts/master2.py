import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'master2'; P = fe.REG[S]['abs']; os.chdir(P); done = []
def has(path, needle): return needle in open(path, encoding='utf-8-sig').read()

# review#2: tenant headers are not a webhook identity
fe.rw('apps/api/src/modules/payments.routes.ts', lambda t: t if 'cannot present tenant headers' in t else t.replace('paymentsRouter.post(\n  "/webhooks/mock",', '// Caveat: a real payment provider cannot present x-org-slug / x-user-email. This mock route resolves\n// the tenant from those headers only because it is exercised by a signed-in operator in local runs.\n// Production must resolve the organization from a verified provider signature or from the stored\n// providerEventId, never from caller-supplied headers (see astraupskill/02-CONCEPTS.md).\npaymentsRouter.post(\n  "/webhooks/mock",', 1))
if not has('astraupskill/02-CONCEPTS.md', 'attacker controls'):
    fe.append_section(S, '02', '## The tenant header is an input the attacker controls', """Every request in this API resolves its tenant from `x-org-slug` and `x-user-email` (`apps/api/src/shared/auth.ts`), which is fine for a demo where a signed-in operator calls the API. It is *not* fine for a webhook. A payment provider posting to `/webhooks/mock` cannot present those headers, and anyone who can reach the endpoint can present any of them. So the tenant scoping the service performs (`payment.findFirst({ where: { id, organizationId: tenant.organizationId } })`) is only as trustworthy as the header. In production the organization must come from something the caller cannot forge: a provider signature over the body verified with the tenant's webhook secret (which identifies the tenant), or the stored `providerEventId` written when the payment was created. The mock route carries this caveat as a comment (fix pass). Predict: with header-derived tenancy, what does a forged `x-org-slug` for another tenant plus a guessed `paymentId` achieve? (It marks another tenant's invoice paid: the scoping check passes because the attacker chose the scope.)""", before='## ')
done.append('review#2 02 paragraph and a route comment: webhook tenancy must not come from caller-supplied headers')

# review#3 + #5: move inline solutions to 06 under anchors
moved = []
for prefix in ['01', '02', '03', '04']:
    path = fe.chapter(S, prefix)
    t, crlf, bom = fe.read(path)
    m = re.search(r'^(Exercise: .*?) Solution: (.*)$', t, re.M)
    if not m: continue
    prompt, solution = m.group(1).strip(), m.group(2).strip()
    t = t[:m.start()] + prompt + f' (answer: [06, chapter {prefix}](06-SOLUTIONS-AND-REVIEW.md#chapter-{prefix}-exercise))' + t[m.end():]
    fe.write(path, t, crlf, bom); moved.append((prefix, prompt, solution))
if moved:
    block = '## Solutions to the chapter exercises\n\n' + '\n\n'.join(f'### Chapter {p} exercise\n\n*{q}*\n\n{s}' for p, q, s in moved)
    t6, crlf, bom = fe.read(fe.chapter(S, '06'))
    if 'Solutions to the chapter exercises' not in t6:
        i = t6.find('\n## Complete review walkthrough')
        t6 = t6[:i] + '\n' + block + '\n' + t6[i:]
        fe.write(fe.chapter(S, '06'), t6, crlf, bom)
done.append(f'review#3 {len(moved)} inline Exercise/Solution pairs in 01-04 now keep only the prompt with a link; review#5 06 has a "Solutions to the chapter exercises" section with one ### anchor per chapter ahead of the existing walkthrough sections')

# review#4 run the app
if not has('astraupskill/VERIFICATION.md', 'Run the app'):
    fe.append_section(S, 'VERIFICATION', '## Run the app and watch a replay', """```powershell
docker compose up -d            # PostgreSQL on localhost:5432 (billing/billing, db billing_platform)
npm install
npm run db:generate
npm run db:push
npm run db:seed                 # organization acme, an owner user, a customer, an open invoice and a payment
npm run dev --workspace @billing/api   # API_PORT defaults to 4000
```

Find a payment id: `npx prisma studio` in `packages/db`, or `SELECT id, status FROM "Payment" LIMIT 1;`. Then, with the seeded owner email in `$email`:

```powershell
$body = '{"providerEventId":"evt-demo-0001","eventType":"payment.succeeded","paymentId":"<payment id>"}'
curl -i -X POST http://localhost:4000/api/payments/webhooks/mock -H "content-type: application/json" -H "x-org-slug: acme" -H "x-user-email: $email" -d $body
# -> 200 { processed: true, eventId }, invoice paid, one audit row, one outbox row
curl -i -X POST http://localhost:4000/api/payments/webhooks/mock -H "content-type: application/json" -H "x-org-slug: acme" -H "x-user-email: $email" -d $body
# -> 200 { duplicate: true, eventId } and no new rows: the replay is absorbed by the stored event
```

Change one character of the body and send it again under the same `providerEventId` to see `webhook.identity_conflict` (409).""", before='## ')
done.append('review#4 VERIFICATION "Run the app": compose, push, seed, dev, a success webhook and its replay')

# review#1 integration test (guarded)
open('apps/api/src/modules/payments.integration.test.ts', 'w', encoding='utf-8', newline='\n').write('''import { afterAll, beforeAll, describe, expect, it } from "vitest";

// Runs only against a disposable PostgreSQL with the schema pushed:
//   docker run --rm -d -e POSTGRES_PASSWORD=local-test -p 5433:5432 postgres:18
//   $env:TEST_DATABASE_URL = "postgresql://postgres:local-test@127.0.0.1:5433/postgres"
//   $env:DATABASE_URL = $env:TEST_DATABASE_URL; npm run db:push
//   npx vitest run src/modules/payments.integration.test.ts   (from apps/api)
const url = process.env.TEST_DATABASE_URL;

describe.skipIf(!url)("mock payment webhook against a real database", () => {
  let prisma: import("@billing/db").PrismaClient;
  let svc: typeof import("./payments.service.js");
  let orgId: string, paymentId: string, invoiceId: string;
  const stamp = Date.now().toString(36);
  const tenant = () => ({
    organizationId: orgId, organizationSlug: "int-" + stamp, userId: "u", userEmail: "u@" + stamp,
    role: "owner" as const, permissions: ["payments:manage"] as never[]
  });

  beforeAll(async () => {
    process.env.DATABASE_URL = url;
    const db = await import("@billing/db");
    prisma = db.prisma;
    svc = await import("./payments.service.js");
    const org = await prisma.organization.create({ data: { name: "Int " + stamp, slug: "int-" + stamp } });
    orgId = org.id;
    const customer = await prisma.customer.create({ data: { organizationId: orgId, email: "c@" + stamp, name: "C" } });
    const invoice = await prisma.invoice.create({ data: { organizationId: orgId, customerId: customer.id, number: "INV-" + stamp, status: "open", currency: "usd", subtotal: 1000, total: 1000, dueAt: new Date() } });
    invoiceId = invoice.id;
    const payment = await prisma.payment.create({ data: { organizationId: orgId, customerId: customer.id, invoiceId, provider: "mock", status: "processing", amount: 1000, currency: "usd" } });
    paymentId = payment.id;
  });

  afterAll(async () => {
    if (!prisma) return;
    await prisma.$executeRawUnsafe('DROP TRIGGER IF EXISTS fail_audit ON "AuditLog"');
    await prisma.$executeRawUnsafe("DROP FUNCTION IF EXISTS fail_audit()");
    await prisma.webhookEvent.deleteMany({ where: { organizationId: orgId } });
    await prisma.outboxEvent.deleteMany({ where: { organizationId: orgId } });
    await prisma.auditLog.deleteMany({ where: { organizationId: orgId } });
    await prisma.payment.deleteMany({ where: { organizationId: orgId } });
    await prisma.invoice.deleteMany({ where: { organizationId: orgId } });
    await prisma.customer.deleteMany({ where: { organizationId: orgId } });
    await prisma.organization.deleteMany({ where: { id: orgId } });
    await prisma.$disconnect();
  });

  const snapshot = async () => ({
    payment: (await prisma.payment.findUniqueOrThrow({ where: { id: paymentId } })).status,
    invoice: (await prisma.invoice.findUniqueOrThrow({ where: { id: invoiceId } })).status,
    events: await prisma.webhookEvent.count({ where: { organizationId: orgId } }),
    outbox: await prisma.outboxEvent.count({ where: { organizationId: orgId } }),
    audit: await prisma.auditLog.count({ where: { organizationId: orgId } }),
  });

  it("rolls every row back when the audit write fails mid-transaction", async () => {
    await prisma.$executeRawUnsafe("CREATE OR REPLACE FUNCTION fail_audit() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN RAISE EXCEPTION 'injected audit failure'; END $$");
    await prisma.$executeRawUnsafe('CREATE TRIGGER fail_audit BEFORE INSERT ON "AuditLog" FOR EACH ROW EXECUTE FUNCTION fail_audit()');
    const before = await snapshot();
    await expect(svc.processMockPaymentWebhook(tenant(), { providerEventId: "evt-fail-" + stamp, eventType: "payment.succeeded", paymentId })).rejects.toBeTruthy();
    expect(await snapshot()).toEqual(before);
    await prisma.$executeRawUnsafe('DROP TRIGGER fail_audit ON "AuditLog"');
    await prisma.$executeRawUnsafe("DROP FUNCTION fail_audit()");
  });

  it("processes exactly one of two identical concurrent events; the other is a 409 or a duplicate", async () => {
    const body = { providerEventId: "evt-race-" + stamp, eventType: "payment.succeeded" as const, paymentId };
    const results = await Promise.allSettled([svc.processMockPaymentWebhook(tenant(), body), svc.processMockPaymentWebhook(tenant(), body)]);
    const processed = results.filter((r) => r.status === "fulfilled" && (r.value as { processed?: boolean }).processed);
    const other = results.filter((r) => r.status === "rejected" || (r.status === "fulfilled" && (r.value as { duplicate?: boolean }).duplicate));
    expect(processed).toHaveLength(1);
    expect(other).toHaveLength(1);
    const rejected = results.find((r) => r.status === "rejected") as PromiseRejectedResult | undefined;
    if (rejected) expect(rejected.reason).toMatchObject({ status: 409 });
    const after = await snapshot();
    expect(after.payment).toBe("succeeded");
    expect(after.invoice).toBe("paid");
    expect(after.events).toBe(1);
    expect(after.outbox).toBe(1);
  });
});
''')
done.append('review#1 payments.integration.test.ts written (skips unless TEST_DATABASE_URL): audit trigger injection proves all-or-nothing; two identical concurrent events yield exactly one processed and one 409/duplicate with one event and one outbox row')
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w')); print('\n'.join(done))
