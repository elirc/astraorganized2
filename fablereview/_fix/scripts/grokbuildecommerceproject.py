import sys, json, os, shutil
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'grokbuildecommerceproject'; P = fe.REG[S]['abs']; os.chdir(P); done = []
CK = r'C:\Users\Owner\Desktop\AstraOrganized2\astra-remaining-improvements\checks\commerce-workspace'

os.makedirs('astraupskill/evidence', exist_ok=True); copied = []
d = os.path.join(CK, 'full-final')
for f in os.listdir(d):
    if f.endswith('.json') or f.endswith('-tests.log'):
        shutil.copy(os.path.join(d, f), f'astraupskill/evidence/{f}'); copied.append(f)
shutil.copy(os.path.join(CK, 'results.json'), 'astraupskill/evidence/results-rollup.json')
fe.append_section(S, 'VERIFICATION', '## Evidence inside the repo', f"""`astraupskill/evidence/` holds copies of the `full-final` run: `results.json`, `backend.json`, `frontend.json`, `browser.json`, and `backend-tests.log`, `browser-tests.log`, `frontend-tests.log`, `setup-tests.log` (the roll-up across attempts is `results-rollup.json`). The 80-check claim is the sum in `results.json`; open `backend.json` for the per-test names. Earlier attempts (`api-first`, `full-first`) are superseded and were not copied.""", before='## ')
done.append(f'review#1 {len(copied)} full-final evidence files copied and linked from VERIFICATION')

open('astraupskill/03b-BREAK-IT.md', 'w', encoding='utf-8', newline='\n').write("""# 03b. Break it first

[Course index](README.md) · [Previous](03-WORKED-CHANGE.md) · [Next](04-TESTING-AND-DEBUGGING.md)

Three guards in `backend/src/repositories/orderRepository.ts` carry the course. Remove one at a time, predict, run `npm test` in `backend/` (the integration suite needs the PostgreSQL fixture; see VERIFICATION), record the failing test name, restore.

## a. Remove the advisory lock

Comment out the line `await tx.$queryRaw\\`SELECT 1 AS locked FROM pg_advisory_xact_lock(hashtextextended(${lockKey},0))\\`;` in `checkout`. Prediction: the concurrent-same-key case in `workflow.integration.test.ts` now sees both transactions miss the receipt (`existing` is null for both), both try to create the order, and the unique index on `(userId, checkoutKey)` turns one of them into a P2002 that surfaces as a 500 instead of a replay. The lock is what makes the *second* caller wait until the first receipt exists.

## b. Stop sorting the items

Change `sortedItems` to `return input.items` (no sort). Prediction: two carts with the same products in reversed order now produce different fingerprints; the replay test that sends the reversed cart under the same key gets a 409 "different items" instead of the replayed order. Canonicalization is part of identity.

## c. Drop the fingerprint check

Delete `if (existing.requestHash !== hash) throw new AppError(409, ...)`. Prediction: the test that replays a *modified* cart under the original key now receives the original order with `replayed: true` and a 200, silently ignoring the new items. That is the worst outcome of the three: no error, wrong result.

Each step has an existing test that should fail. If one does not, that is a coverage gap worth a test of your own before you continue.
""")
fe.rw('astraupskill/README.md', lambda t: t.rstrip('\n') + '\n\nAfter chapter 03 read [03b: break it first](03b-BREAK-IT.md).\n\n## Prerequisites\n\nYou should already be comfortable with SQL transactions (BEGIN/COMMIT, what an isolation level changes), HTTP status semantics (200 vs 201, 400 vs 409, when 404 hides existence), and React state updates from async responses. Task 3 in `05-PRACTICE.md` (a payment-provider boundary with a fake adapter) is a stretch goal, not a required step; do tasks 1, 2 and 4 first.\n')
done.append('review#2 03b-BREAK-IT.md with three predicted failures; review#5 README prerequisites and task 3 flagged as a stretch goal')

fe.append_section(S, '06', '## Task 2, worked: stock adjustments', """**Schema** (`backend/prisma/schema.prisma`):

```prisma
model StockAdjustment {
  id          String   @id @default(uuid())
  productId   String
  product     Product  @relation(fields: [productId], references: [id])
  actorId     String
  delta       Int
  reason      String
  before      Int
  after       Int
  requestKey  String
  createdAt   DateTime @default(now())
  @@unique([productId, requestKey])
}
```

`@@unique([productId, requestKey])` is the idempotency receipt: a retried adjustment with the same key is the same adjustment.

**Validation** (`backend/src/lib/validation.ts`):

```ts
export const adjustmentInput = z.object({
  delta: z.number().int().refine((d) => d !== 0, "delta must not be zero").refine((d) => Math.abs(d) <= 1_000_000, "delta out of range"),
  reason: z.string().trim().min(3).max(200),
  requestKey: z.string().uuid(),
}).strict();
```

**Repository** (`backend/src/repositories/productRepository.ts`), one transaction, no product snapshot:

```ts
export async function adjustStock(actor: Actor, productId: string, input: AdjustmentInput) {
  adminScope(actor);
  return prisma.$transaction(async (tx) => {
    await tx.$queryRaw`SELECT 1 FROM pg_advisory_xact_lock(hashtextextended(${"stock:" + productId}, 0))`;
    const receipt = await tx.stockAdjustment.findUnique({ where: { productId_requestKey: { productId, requestKey: input.requestKey } } });
    if (receipt) return { adjustment: receipt, replayed: true };
    // Conditional write: the WHERE carries the floor, so a concurrent checkout cannot push us negative.
    const changed = await tx.product.updateMany({
      where: { id: productId, stock: { gte: input.delta < 0 ? -input.delta : 0 } },
      data: { stock: { increment: input.delta } },
    });
    if (changed.count === 0) throw new AppError(409, "Adjustment would make stock negative, or the product is missing.");
    const product = await tx.product.findUniqueOrThrow({ where: { id: productId }, select: { stock: true } });
    const adjustment = await tx.stockAdjustment.create({
      data: { productId, actorId: actor.id, delta: input.delta, reason: input.reason, requestKey: input.requestKey,
              before: product.stock - input.delta, after: product.stock },
    });
    await audit(tx, actor, "product.stock_adjusted", { productId, delta: input.delta, requestKey: input.requestKey });
    return { adjustment, replayed: false };
  }, { isolationLevel: Prisma.TransactionIsolationLevel.RepeatableRead });
}
```

The product's `version` is untouched: an adjustment is not a metadata edit, so it must not invalidate an admin's open metadata form.

**Route** (`backend/src/routes/productRoutes.ts`): `POST /products/:id/adjustments`, admin only, `adjustmentInput.parse(req.body)`, 200 with `{ adjustment, replayed }`; the 409 above is returned as-is.

**Integration test** (`backend/src/__tests__/workflow.integration.test.ts` style): seed a product with stock 5; fire `adjustStock(-3)` and a checkout of 3 concurrently (`Promise.all`); assert exactly one succeeds, the other is 409, `stock` is 2 (never negative), and one `StockAdjustment` row exists. Then replay the same `requestKey`: `replayed: true` and still one row. Then a delta of `-10` on stock 2: 409 and no row. The advisory lock on `stock:<productId>` is what makes "concurrent" deterministic; the checkout path should take the same key when it decrements stock.""", before='## ')
done.append('review#3 06 worked solution for task 2 (schema, validation, repository with conditional write + receipt, route, concurrency integration test)')

fe.append_section(S, '04', '## The three 500s in the log are deliberate', """`evidence/backend-tests.log` contains three `"status":500,"event":"request_failed"` lines. They come from the `auditFailure` helper in `workflow.integration.test.ts`, which installs a trigger that makes the `AuditEvent` insert raise; the assertion is that registration, checkout and the third mutation *roll back* when their audit write fails, and the error handler in `backend/src/lib/errors.ts` logs any 5xx. A passing log therefore contains exactly three such lines, no more. If you want a log with none, map the injected failure to a controlled 503 ("audit unavailable") in the error handler: the rollback assertion stays the same, and the status becomes a deliberate contract instead of an unexplained 500. That is a reasonable follow-up, not a defect in the delivered run.""", before='## ')
done.append('review#4 04 explains the three deliberate 500s and the optional 503 mapping')
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w')); print('\n'.join(done))
