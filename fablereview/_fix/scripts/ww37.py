import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'ww37'; P = fe.REG[S]['abs']; os.chdir(P); done = []

# --- review #3: service validation derived from the zod schemas (one definition per rule)
svc = 'src/services/inventoryService.ts'
def derive(t):
    t = t.replace("import type { AdjustStockInput, CreateItemInput, UpdateItemInput } from '@/lib/validation/itemSchemas';",
                  "import type { AdjustStockInput, CreateItemInput, UpdateItemInput } from '@/lib/validation/itemSchemas';\nimport { createItemSchema, updateItemSchema } from '@/lib/validation/itemSchemas';", 1)
    create_new = """function validateCreateInput(input: CreateItemInput): void {
  // The route already parsed this shape; the service parses it again because the service is also
  // called from tests, scripts and future routes that may not. One schema, two call sites.
  const parsed = createItemSchema.safeParse(input);
  if (!parsed.success) {
    throw validationError(parsed.error.issues[0]?.message ?? 'Invalid item.');
  }
}
"""
    update_new = """function validateUpdateInput(input: UpdateItemInput): void {
  const parsed = updateItemSchema.safeParse(input);
  if (!parsed.success) {
    throw validationError(parsed.error.issues[0]?.message ?? 'Invalid item update.');
  }
  const values = input as Record<string, unknown>;
  if (Object.keys(values).every((key) => values[key] === undefined)) {
    throw validationError('At least one valid item field must be provided.');
  }
}
"""
    t, n1 = re.subn(r'function validateCreateInput\(input: CreateItemInput\): void \{.*?\n\}\n', create_new, t, count=1, flags=re.S)
    t, n2 = re.subn(r'function validateUpdateInput\(input: UpdateItemInput\): void \{.*?\n\}\n', update_new, t, count=1, flags=re.S)
    assert n1 == 1 and n2 == 1
    # drop the now-unused numeric assert (assertText is still used by the adjustment reason)
    if t.count('assertNonNegativeInteger(') == 1:
        t = re.sub(r'function assertNonNegativeInteger\(.*?\n\}\n\n', '', t, count=1, flags=re.S)
    return t
fe.rw(svc, derive)
done.append('review#3 validateCreateInput/validateUpdateInput now call createItemSchema/updateItemSchema.safeParse; the hand-rolled numeric assert was removed (assertText stays for the adjustment reason)')

# --- review #5: shallow clone comment + test
def clone(t):
    return t.replace('function cloneItem(', '''// These clones are shallow ({ ...item }): safe today because InventoryItem holds only primitives.
// If a nested object (for example a supplier record) is ever added, a caller mutating it would change
// the repository's copy too; the "clone is shallow" test pins that assumption.
function cloneItem(''', 1)
fe.rw('src/repositories/inMemoryInventoryRepository.ts', clone)
def tests(t):
    add = '''
test('the service rejects an input the schema rejects even when the route is bypassed', async () => {
  // Route validation is one boundary; the service is another. A script or a future route that calls
  // the service directly must get the same 400, from the same schema.
  const repository = new InMemoryInventoryRepository(createSeedData());
  const inventory = createInventoryService(repository, createAlertService(repository));
  await assert.rejects(
    inventory.createItem({ sku: 'ab', name: 'Too short', unit: 'ea', initialOnHand: 1, reorderPoint: 0 }, managerSession),
    (error: unknown) => error instanceof AppError && error.statusCode === 400
  );
  await assert.rejects(
    inventory.updateItem('missing', {}, managerSession),
    (error: unknown) => error instanceof AppError && error.statusCode === 400
  );
});

test('repository clones are shallow: primitives are isolated, nested objects would not be', async () => {
  const repository = new InMemoryInventoryRepository(createSeedData());
  const first = (await repository.listItems())[0];
  first.name = 'mutated by caller';
  const again = (await repository.listItems())[0];
  assert.notEqual(again.name, 'mutated by caller');
  // Document the limit of the guarantee rather than pretend it is deep.
  assert.equal(Object.values(again).every((value) => typeof value !== 'object' || value === null), true,
    'InventoryItem must stay flat, or cloneItem must become a deep copy');
});
'''
    return t.rstrip('\n') + '\n' + add
fe.rw('tests/inventory.test.ts', tests)
done.append('review#2/#5 two tests: the service rejects schema-invalid input when the route is bypassed (400); repository clones are shallow and the item stays flat')

# --- review #1: async params section in 03
fe.append_section(S, '03', '## The async `params` change in Next 15', """`src/app/api/items/[itemId]/route.ts` declares its second argument as `{ params: Promise<{ itemId: string }> }` and awaits it. Before Next 15, `params` was a plain object; the Next 15 migration made it a Promise so the framework can start rendering before route segments are resolved. The sync version still works for one release but prints:

```
Route "/api/items/[itemId]" used `params.itemId`. `params` should be awaited before using its properties.
```

Before / after:

```typescript
// before (Next 14): sync
export async function PATCH(request: Request, { params }: { params: { itemId: string } }) {
  return handle(params.itemId, request);
}
// after (Next 15+): the params object is a Promise
export async function PATCH(request: Request, { params }: { params: Promise<{ itemId: string }> }) {
  const { itemId } = await params;
  return handle(itemId, request);
}
```

Forgetting the `await` compiles under the sync type, reads `undefined` for `itemId`, and turns every request into a 404: the type change is what makes the mistake visible.""", before='## ')
done.append('review#1 03 explains the Next 15 async params change with the warning text and before/after code')

# --- review #2/#4: 02 sub-headings, why-validate-twice, ASCII timeline
def concepts(t):
    add = """
## Why validate twice

The route parses the body with `createItemSchema` and answers 400 on failure; the service then parses the same input with the same schema. This is not duplication of *rules* (there is one schema) but of *enforcement*: the service is called from tests, from seed scripts and from any future route, and none of those pass through the route parser. The new test in `tests/inventory.test.ts` calls the service directly with a two-character SKU and expects the same 400.

## Reservation timeline

```
t0  clerk POST /api/reservations  ->  hold created  (available = onHand - held)
t1  manager PATCH /api/items/:id   ->  metadata only; onHand unchanged; available unchanged
t2  clerk POST .../release         ->  hold released; available restored
t3  clerk POST .../release again   ->  409: releasing a released hold is not idempotent by design
```

`getAvailableQuantity` is the one function that turns `onHand` and open holds into the number the UI shows; every mutation above re-derives it rather than storing it.
"""
    t = t.rstrip('\n') + '\n' + add
    # add sub-headings to a heading-less body: promote bold lead-ins if present
    if t.count('\n## ') < 3:
        t = re.sub(r'\n\*\*([^*\n]{6,60})\*\*\n', r'\n## \1\n', t)
    return t
fe.rw('astraupskill/02-CONCEPTS.md', concepts)
done.append('review#2/#4 02 gains "Why validate twice" and an ASCII reservation timeline, plus sub-headings')

# --- review #6: loader note
fe.rw('astraupskill/VERIFICATION.md', lambda t: t.replace('--experimental-loader', '--experimental-loader (deprecated in favor of `--import` with `module.register`; the alias hook in `tests/register-alias.mjs` is what maps `@/` to `src/`)', 1))
done.append('review#6 VERIFICATION names the experimental loader as deprecated and points at the alias hook')
fe.append_section(S, 'README', '## Prerequisites, glossary and pacing', """**Prerequisites:** one Next.js App Router project with route handlers, and Zod basics (`safeParse`, `issues`).

**Glossary.** *Route handler*: the `GET/POST/PATCH` export in `src/app/api/.../route.ts`. *Hold*: a reservation that reduces available quantity without changing `onHand`. *Available quantity*: `onHand` minus open holds, derived on read. *Shallow clone*: `{ ...item }` copies top-level fields only. *Alias hook*: the loader that resolves `@/` in tests.

**Pacing:** map 45 min, concepts 60 min, worked change 90 min, testing 60 min, practice 3-4 h, solutions 45 min, trace lab 45 min.""", before='## ')
done.append('3.5 README prerequisites, glossary and pacing')
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w')); print('\n'.join(done))
