import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'lucasrouter'; P = fe.REG[S]['abs']; os.chdir(P); done = []

# review#1: budget test tracks the constant
def st(t):
    old = "    const big = `data:image/jpeg;base64,${'A'.repeat(1_499_960)}`;"
    new = "    // Tied to the real budget: if PHOTO_BUDGET_BYTES changes, this test still spends it.\n    const { PHOTO_BUDGET_BYTES } = await import('@/store/useAppStore');\n    const big = `data:image/jpeg;base64,${'A'.repeat(PHOTO_BUDGET_BYTES - 40)}`;"
    assert old in t
    return t.replace(old, new, 1)
fe.rw('tests/store.test.ts', st)
done.append('review#1 tests/store.test.ts reads PHOTO_BUDGET_BYTES from the store module and builds the oversized photo from it')

# review#2: whitespace-tolerant photo pattern, decision recorded
def dv(t):
    old = "  const photo = value.photo;\n  const isDataUrl = typeof photo === 'string' && /^data:image\\/[a-z0-9.+-]+;base64,[a-z0-9+/]+=*$/i.test(photo);"
    new = "  // Camera inputs and copy-paste can add surrounding whitespace; strip it before the strict match.\n  const photo = typeof value.photo === 'string' ? value.photo.trim() : value.photo;\n  const isDataUrl = typeof photo === 'string' && /^data:image\\/[a-z0-9.+-]+;base64,[a-z0-9+/]+=*$/i.test(photo);"
    assert old in t, 'photo pattern block not found'
    return t.replace(old, new, 1)
fe.rw('src/lib/deliveryValidation.ts', dv)
def dvt(t):
    add = """
  it('tolerates surrounding whitespace on a photo data URL but still rejects other schemes', () => {
    expect(sanitizeDeliveryProof({ photo: '  data:image/png;base64,QUJD  ' }).photo).toBe('data:image/png;base64,QUJD');
    expect(sanitizeDeliveryProof({ photo: ' https://example.test/x.png ' })).toEqual({});
  });
"""
    idx = t.rstrip().rfind('});')
    return t[:idx] + add.lstrip('\n') + t[idx:]
fe.rw('tests/delivery-validation.test.ts', dvt)
fe.append_section(S, 'VERIFICATION', '## Decision: a dropped photo is reported, not hidden', """`recordDelivery` returns `{ ok: true, photoDropped: true }` when the photo budget is spent. The delivery is real (the stop is `delivered`, the event is logged) and the driver is told about the missing picture by the caller's toast, so the result is *not* silent: the flag is the signal, and the store test asserts it. The alternative, refusing the delivery because a picture did not fit, would block the driver's actual job for a cosmetic limit. Photo data URLs are trimmed before the strict pattern is applied (fix pass); anything that is not `data:image/...;base64,...` is still dropped, and the delivery-validation test covers both.""", before='## ')
done.append('review#2 photo data URLs are trimmed before matching (test added); VERIFICATION records the dropped-photo decision')

# review#3: test code in 04
runner = 'pnpm test' if os.path.exists('pnpm-lock.yaml') else 'npm test --'
dvtest = open('tests/delivery-validation.test.ts', encoding='utf-8-sig').read().replace('\r\n', '\n')
fe.append_section(S, '04', '## The boundary tests, in full', f"""Run one file:

```powershell
{runner} tests/delivery-validation.test.ts
{runner} tests/store.test.ts -t "photo budget"
```

`tests/delivery-validation.test.ts` as it stands after the fix pass:

```typescript
{dvtest.rstrip()}
```

The store test for the budget builds its oversized photo from `PHOTO_BUDGET_BYTES - 40` so that changing the constant cannot silently make the test meaningless; before the fix pass it hard-coded `1_499_960`.""", before='## ')
done.append('review#3 04 inlines the delivery-validation suite and the exact single-file test commands')

# review#4: exercise 6 solution
fe.append_section(S, '06', '## Practice 6: the same contract on a server', """The demo enforces the proof contract in the store because there is no server. On the CRUD stack you are training for, the same rules move into a route handler, and three things change: rejection replaces silent dropping, the response has a 400 shape, and ownership is checked from the session rather than trusted from the client.

```typescript
// app/api/deliveries/route.ts (Next.js route handler sketch)
import { NextResponse } from 'next/server';
import { z } from 'zod';
import { getSession } from '@/lib/session';
import { db } from '@/lib/db';

const deliveryProof = z.object({
  stopId: z.string().min(1),
  method: z.enum(['door', 'handed', 'mailbox', 'neighbor']),
  recipientName: z.string().trim().max(120).optional(),
  note: z.string().trim().max(500).optional(),
  photo: z.string().trim().regex(/^data:image\\/[a-z0-9.+-]+;base64,[a-z0-9+/]+=*$/i).max(1_500_000).optional(),
}).strict();

export async function POST(request: Request) {
  const session = await getSession(request);
  if (!session) return NextResponse.json({ error: 'unauthenticated' }, { status: 401 });
  const parsed = deliveryProof.safeParse(await request.json().catch(() => null));
  if (!parsed.success) {
    return NextResponse.json({ error: 'invalid_proof', issues: parsed.error.issues }, { status: 400 });
  }
  const stop = await db.stop.findFirst({ where: { id: parsed.data.stopId, route: { driverId: session.userId } } });
  if (!stop) return NextResponse.json({ error: 'not_found' }, { status: 404 });
  if (stop.status !== 'pending') return NextResponse.json({ error: 'already_recorded' }, { status: 409 });
  const [updated] = await db.$transaction([
    db.stop.update({ where: { id: stop.id }, data: { status: 'delivered', proof: parsed.data } }),
    db.deliveryEvent.create({ data: { stopId: stop.id, driverId: session.userId, type: 'delivered' } }),
  ]);
  return NextResponse.json({ stop: updated }, { status: 201 });
}
```

What stays on the client: trimming, enum narrowing and the size hint are still useful for fast feedback. What must be server-side: the ownership check (`driverId` comes from the session, never the body), the `pending` state check, the proof and the event in one transaction, and the size limit (a client can bypass any store). Compare the 400 here with the demo's `sanitizeDeliveryProof` returning `{}`: a server must tell the caller what it refused.""", before='## ')
done.append('review#4 06 Practice 6 solution: a route handler with a Zod schema mirroring sanitizeDeliveryProof, 401/400/404/409 shape and the ownership check')

# review#6 glossary
fe.append_section(S, '02', '## Glossary', """*Runtime guard*: a check that runs on real data (`isDeliveryMethod`), as opposed to a compile-time type that is erased. *Boundary*: the place where untrusted data enters (a form, a store action, a route). *Narrowing*: TypeScript accepting a value as a more specific type after a guard returns true. *Data URL*: `data:image/jpeg;base64,...`, the encoded picture stored inline. *Proof/event parity*: the proof on the stop and the event in the log describe the same delivery and must agree. *`as unknown` cast in tests*: how a test passes deliberately wrong input past the compiler to exercise the runtime guard.""")
done.append('review#6 02 glossary')
done.append('review#5 README line endings: git diff shows 4 insertions and no deletions against HEAD (both CRLF), so the delivered diff is already only the course link')
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w')); print('\n'.join(done))
