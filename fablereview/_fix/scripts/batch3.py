import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apply_blocks import apply

items = []

items.append(('e12', '06', '## The rule you would extend',
"""Validation feedback lives in one exported function, so a better message is a change in one place rather than in each route. From `src/server/contracts.js:186-194`:

```js
export function validateStrategySettings(value, field = "strategy") {
  strategyType(value.type, `${field}.type`);
  const params = parameters(value.parameters ?? {}, `${field}.parameters`);
  if (value.type === "gradual_rollout") {
    if (!Object.hasOwn(params, "rollout"))
      reject(field, "gradual rollout requires a rollout percentage");
  } else if (Object.keys(params).length)
    reject(field, "only gradual rollout accepts parameters");
  return value;
}
```"""))

items.append(('e12', '07', '## Where Lab A stops being about the browser',
"""Follow the request into `createFlag` and read the order of the guards: role, then required fields, then project write permission, then key uniqueness, then the per-project limit. Nothing here trusts the identifiers the browser already knows. From `src/server/services.js:837-853`:

```js
    createFlag(actor, input) {
      requireAdminRole(actor);
      const state = store.getState();
      assert(
        input.projectId && input.key && input.name && input.type,
        400,
        "Missing required flag fields",
      );
      assert(FLAG_TYPES.includes(input.type), 400, "Invalid flag type");
      requireProjectWrite(state, actor, input.projectId);
      assertUniqueFlagKey(state, input.key);
      assert(
        state.featureFlags.filter((item) => item.projectId === input.projectId)
          .length < state.resourceLimits.maxFlagsPerProject,
        409,
        "Flag limit reached for this project",
      );
```"""))

items.append(('e13', '03', '## The guards that run before the transaction',
"""This is the pre-transaction half of the repaired command, from `src/lib/commerce/orders.ts:261-277`. Uniqueness and quantity are decided here, which is why a duplicated `orderLineId` never opens a write transaction.

```ts
export async function createFulfillment(orderId: string, warehouseId: string, lines: FulfillmentLineInput[], actor?: Actor | null) {
  if (!Array.isArray(lines) || lines.length === 0) {
    throw new AppError("At least one fulfillment line is required.", "INVALID_INPUT", 400);
  }

  const seenLineIds = new Set<string>();
  for (const line of lines) {
    if (!line || typeof line.orderLineId !== "string" || line.orderLineId.trim().length === 0 || seenLineIds.has(line.orderLineId)) {
      throw new AppError("Fulfillment lines must contain unique order line IDs.", "INVALID_INPUT", 400);
    }
    if (!Number.isSafeInteger(line.quantity) || line.quantity <= 0) {
      throw new AppError("Fulfillment quantity must be a positive safe integer.", "INVALID_INPUT", 400);
    }
    seenLineIds.add(line.orderLineId);
  }

  return prisma.$transaction(async (tx) => {
```"""))

items.append(('e13', '04', '## The exclude, and why it is not cosmetic',
"""`npm test` runs `vitest run`. The archived pre-change copies under `astraupskill/original/` include the old test file, and collecting it would reseed the canonical `dev.db`. The config states that in the file itself (`vitest.config.ts`):

```ts
  test: {
    environment: "node",
    // astraupskill/original/ holds byte-identical copies of the PRE-change source,
    // including the old commerce.test.ts. That archived test reseeds the canonical
    // dev.db via `npm run db:push` / `npm run db:seed`, so Vitest must never collect it.
    exclude: ["**/node_modules/**", "**/dist/**", "**/astraupskill/**"],
    fileParallelism: false,
    hookTimeout: 120_000,
    testTimeout: 120_000,
  },
```"""))

items.append(('e13', '06', '## What an independent snapshot looks like',
"""The "two references to one mutable object" mistake is avoided by serializing before and after, then comparing the serialized values. From `src/lib/commerce/commerce.test.ts:277-297`:

```ts
  test("rejects duplicate fulfillment lines without changing order or stock", async () => {
    const ready = await createReadyCheckout(2);
    const order = await completeCheckout(ready.checkoutToken, `complete:${ready.checkoutToken}`);
    const warehouse = await prisma.warehouse.findFirstOrThrow();
    const actor = await getAdminActor();
    const before = JSON.parse(JSON.stringify(await prisma.order.findUniqueOrThrow({
      where: { id: order.id },
      include: { lines: true, stockReservations: { include: { stock: true } }, fulfillments: true },
    })));

    await expect(createFulfillment(order.id, warehouse.id, [
      { orderLineId: order.lines[0].id, quantity: 1 },
      { orderLineId: order.lines[0].id, quantity: 1 },
    ], actor)).rejects.toMatchObject({ code: "INVALID_INPUT" });

    const after = JSON.parse(JSON.stringify(await prisma.order.findUniqueOrThrow({
      where: { id: order.id },
      include: { lines: true, stockReservations: { include: { stock: true } }, fulfillments: true },
    })));
    expect(after).toEqual(before);
  });
```"""))

items.append(('e13', '07', '## The replay boundary, in the order the trace hits it',
"""Read the refund path in source order: the key is looked up and compared for identity *before* the remaining-balance check, which is why replaying a key that emptied the balance returns its receipt instead of failing. From `src/lib/commerce/orders.ts:556-571`:

```ts
    const existingTransaction = await tx.paymentTransaction.findUnique({ where: { idempotencyKey } });
    if (existingTransaction) {
      if (existingTransaction.paymentId !== payment.id || existingTransaction.kind !== PaymentTransactionKind.REFUND || existingTransaction.amount !== amount) {
        throw new AppError("Idempotency key is bound to a different payment transaction.", "IDEMPOTENCY_CONFLICT", 409);
      }
      return tx.order.findUniqueOrThrow({
        where: { id: orderId },
        include: {
          refunds: true,
          payments: true,
        },
      });
    }

    if (payment.amountCaptured <= 0 || amount > payment.amountCaptured) {
      throw new AppError("Refund amount is invalid.", "INVALID_REFUND", 400);
    }
```"""))

items.append(('j1', '03', '## The three methods the edit passes through',
"""`editTask` is deliberately small: the expected version is checked first, a replacement value is built, and only `replace` reaches the durable commit. From `src/todo/service/TaskManager.java:39-51`:

```java
    private Task expected(int id, int version) {
        Task task = findTaskById(id);
        if (task.getVersion() != version) throw new IllegalStateException("Task version changed. Reload and review before retrying.");
        return task;
    }
    private Task replace(Task replacement) throws IOException {
        var tasks = new ArrayList<>(snapshot.tasks());
        tasks.replaceAll(t -> t.getId() == replacement.getId() ? replacement : t);
        commit(tasks, snapshot.nextId()); return replacement;
    }
    public synchronized Task editTask(int id, int version, String title, String description) throws IOException {
        return replace(expected(id, version).edit(title, description));
    }
```"""))

items.append(('j1', '04', '## Running the verification helper',
"""One command compiles `src/` and `test/` into a fresh temporary directory, runs the workflow suite, drives the real CLI and coordinates the two-JVM scenario. Set `TODO_VERIFY_RESULTS_DIR` when you want the logs somewhere other than `.verification`.

```bash
python scripts/verify.py
TODO_VERIFY_RESULTS_DIR=/tmp/todo-evidence python scripts/verify.py
```"""))

items.append(('j1', '06', '## The standard your solution has to meet',
"""Every extension discussed here still has to keep this case green: an injected failure at the commit boundary leaves both memory and the file unchanged. From `test/todo/TaskWorkflowTest.java:64`:

```java
        test("atomic replacement failure retains memory and disk", () -> { Path p=file(); manager(p).addTask("Existing task",""); byte[] before=Files.readAllBytes(p); TaskRepository failing=new TaskRepository(p.toString()) { protected void replaceAtomically(Path a,Path b)throws IOException{throw new IOException("Injected move failure");} }; TaskManager m=new TaskManager(failing,CLOCK); rejects(IOException.class,()->m.addTask("Rejected task","")); check(m.getAllTasks().size()==1&&Arrays.equals(before,Files.readAllBytes(p))); });
```"""))

items.append(('j1', '07', '## The durable boundary Trace C stops at',
"""Trace C ends inside `save`. Note the order: revision and watermark checks, then the file lock, then the baseline byte comparison that produces the "changed in another session" message you will see in the second terminal. From `src/todo/repository/TaskRepository.java:39-51`:

```java
    public synchronized void save(TaskSnapshot candidate) throws IOException {
        if (!loaded) throw new IOException("Load the repository before saving.");
        if (current.revision() == Long.MAX_VALUE || candidate.revision() != current.revision() + 1)
            throw new IOException("Snapshot revision must advance exactly once.");
        if (candidate.nextId() < current.nextId()) throw new IOException("Next-id watermark cannot move backward.");
        byte[] encoded = encode(candidate);
        Files.createDirectories(filePath.getParent());
        Path lockPath = filePath.resolveSibling(filePath.getFileName() + ".lock");
        synchronized (LOCAL_LOCKS.computeIfAbsent(lockPath, ignored -> new Object())) {
            if (Files.isSymbolicLink(lockPath)) throw new IOException("Symbolic-link locks are unsupported.");
            try (FileChannel channel = FileChannel.open(lockPath, CREATE, WRITE); var lock = channel.lock()) {
                if (!Arrays.equals(baseline, bytes())) throw new IOException("File changed in another session. Reload before retrying; no data was overwritten.");
```"""))

apply(items)
