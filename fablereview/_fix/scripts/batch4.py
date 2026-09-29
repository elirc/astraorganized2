import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apply_blocks import apply

items = []

items.append(('aiheartbeat', '07', '## The store function the PATCH lands in',
"""This is where the trace crosses into SQLite, from `packages/dashboard/lib/workspace-store.ts:66-76`. `assertCollection` and `assertId` run before `BEGIN IMMEDIATE`, and the merge of existing fields with the partial `data` object happens inside the transaction.

```ts
export function saveWorkspaceItem(db: DatabaseSync, collection: Collection, input: unknown, id?: number) {
  assertCollection(collection);
  if (id !== undefined) assertId(id);
  // Hold the lock across read/merge/write so independent field edits do not overwrite one another.
  db.exec("BEGIN IMMEDIATE");
  try {
    const existing = id === undefined ? undefined : db.prepare(`SELECT * FROM workspace_${collection} WHERE id = ?`).get(id) as Row | undefined;
    if (id !== undefined && !existing) throw new WorkspaceNotFoundError("This item no longer exists. Refresh and try again.");
    if (!input || typeof input !== "object" || Array.isArray(input)) throw new WorkspaceInputError("Invalid item");
    const parsed = schemas[collection].safeParse({ ...(existing ? decode(existing, collection) : {}), ...input });
    if (!parsed.success) throw new WorkspaceInputError(parsed.error.issues[0]?.message ?? "Invalid item");
```"""))

items.append(('netvg', '07', '## The shape gates in the table, in code',
"""The "shape gates pass" row of the trace is this block, from `src/PeblClone.Application/Workforce/HiringQuoteCalculator.cs:17-38`. Country and currency are normalised first, so `de`/`eur` reach the same gates as `DE`/`EUR`, and every failure is a `Result` value rather than an exception.

```csharp
        var countryCode = request.CountryIsoCode?.Trim().ToUpperInvariant();
        var currency = request.Currency?.Trim().ToUpperInvariant();

        if (string.IsNullOrWhiteSpace(countryCode) || countryCode.Length != 2)
        {
            return Result<HiringQuoteDto>.Failure("Country must be a two-letter ISO code.");
        }

        if (string.IsNullOrWhiteSpace(currency) || currency.Length != 3 || currency.Any(character => character is < 'A' or > 'Z'))
        {
            return Result<HiringQuoteDto>.Failure("Currency must be a three-letter ISO code.");
        }

        if (!Enum.IsDefined(request.EmploymentType))
        {
            return Result<HiringQuoteDto>.Failure("Employment type is not supported.");
        }

        if (request.MonthlyCompensation <= 0 || request.MonthlyCompensation > 1_000_000_000_000m)
        {
            return Result<HiringQuoteDto>.Failure("Monthly compensation must be greater than zero and within the demo limit.");
        }
```"""))

items.append(('geminiorganized-opensource-upskilling-ramp', '07', '## Steps 2 to 5 in one method',
"""Rows 2-5 of the table are a single service method, from `backend/Services/ExpenseService.cs:187-201`. Read the order: the per-expense gate, then the visibility check, then the transition rule, then the queue admission — the status only changes after the job is accepted.

```csharp
    public Expense StartReimbursement(User actor, Guid id)
    {
        lock (_store.GetExpenseLock(id))
        {
            var expense = GetForActor(actor, id);
            EnsureLegalHumanTransition(expense, ExpenseStatus.Reimbursing, actor);
            // TryWrite is the admission boundary. The worker takes the same gate,
            // so it cannot observe the expense until this transition is complete.
            if (!_queue.TryEnqueue(BackgroundJobs.ProcessReimbursement(expense.Id)))
                throw new DomainException("Reimbursement queue is full; try again later.");

            Transition(expense, ExpenseStatus.Reimbursing, actor, note: "Reimbursement queued.");
            return expense;
        }
    }
```"""))

items.append(('nettrello', '07', '## Why omitted and explicit-null differ',
"""Trace A and the second-pass rows both depend on `ResolveAgainst`, which reads `JsonValueKind` rather than a nullable CLR property: `Undefined` means "keep the stored value", and any other kind means the caller sent something. From `src/NetTrello.Api/Contracts/BoardDtos.cs:63-78`:

```csharp
    public CardUpdateValues ResolveAgainst(Card current)
    {
        if (Title.ValueKind == JsonValueKind.Undefined && Description.ValueKind == JsonValueKind.Undefined && Priority.ValueKind == JsonValueKind.Undefined && AssigneeId.ValueKind == JsonValueKind.Undefined && DueDate.ValueKind == JsonValueKind.Undefined && Labels.ValueKind == JsonValueKind.Undefined)
        {
            throw DomainException.BadRequest("card.patch_empty", "At least one card field is required.");
        }

        return new CardUpdateValues(
            ReadRequiredString(Title, current.Title, "title"),
            ReadNullableString(Description, current.Description, "description"),
            ReadPriority(Priority, current.Priority),
            ReadNullableGuid(AssigneeId, current.AssigneeId, "assigneeId"),
            ReadNullableDate(DueDate, current.DueDate, "dueDate"),
            ReadNullableLabels(Labels, current.Labels));
    }
```"""))

items.append(('geminiorganized-opensource-upskilling-stripe', '07', '## The retry test Trace 1 asks you to read',
"""Here is `ExactHttpRetryReturnsSameBodyAndEtag` in full, from `tests/Billing.Tests/HttpTests.cs:106-115`. The last line is the point of Trace 1: the same key with a changed payload is a 409, because the key identifies the operation, not the customer.

```csharp
    [Fact] public async Task ExactHttpRetryReturnsSameBodyAndEtag()
    {
        var session = await Register(); var key = Guid.NewGuid().ToString(); var input = new CustomerInput("Same", "same@example.test", "USD");
        var first = await Request("POST", "/api/customers", input, session.Token, key);
        var second = await Request("POST", "/api/customers", input, session.Token, key);
        Assert.Equal(HttpStatusCode.Created, second.StatusCode);
        Assert.Equal(await first.Content.ReadAsStringAsync(), await second.Content.ReadAsStringAsync());
        Assert.Equal(first.Headers.ETag, second.Headers.ETag);
        Assert.Equal(HttpStatusCode.Conflict, (await Request("POST", "/api/customers", input with { Name = "Different" }, session.Token, key)).StatusCode);
    }
```"""))

items.append(('appmakertrack', '07', '## The stop, line by line',
"""The stop trace above is fifteen lines of real code, from `lib/time-entry-service.ts:4-15`. The conditional `updateMany` with `endTime: null` is the race guard: the loser gets `count === 0` and the caller turns that into the 409.

```ts
export async function stopRunningEntry(prisma: PrismaClient, entryId: string, requestedEnd: Date | undefined, notes: string | null | undefined) {
  const entry = await prisma.timeEntry.findUnique({ where: { id: entryId } });
  if (!entry) return { kind: "missing" as const };
  if (entry.endTime) return { kind: "conflict" as const };
  const endTime = requestedEnd ?? new Date();
  if (endTime < entry.startTime) throw new InputError("endTime must be on or after startTime");
  const duration = parseSeconds(Math.round((endTime.getTime() - entry.startTime.getTime()) / 1000));
  const result = await prisma.timeEntry.updateMany({ where: { id: entryId, endTime: null }, data: { endTime, duration, ...(notes !== undefined && { notes }) } });
  if (result.count !== 1) return { kind: "conflict" as const };
  const completed = await prisma.timeEntry.findUnique({ where: { id: entryId } });
  return completed?.endTime ? { kind: "stopped" as const, entry: completed } : { kind: "conflict" as const };
}
```"""))

apply(items)
