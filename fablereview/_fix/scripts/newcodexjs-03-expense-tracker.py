import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'newcodexjs-03-expense-tracker'
P = fe.REG[S]['abs']
os.chdir(P)
done = []

# review #1: split the overloaded amount error
def patch_service(t):
    old = '  if (!Number.isFinite(amount) || amount <= 0 || amount > 99999999.99 || Math.abs(amount * 100 - Math.round(amount * 100)) > 0.00001) throw new ValidationError("Amount must be greater than zero");'
    new = '''  if (!Number.isFinite(amount)) throw new ValidationError("Amount must be a finite number");
  if (amount <= 0) throw new ValidationError("Amount must be greater than zero");
  if (Math.abs(amount * 100 - Math.round(amount * 100)) > 0.00001) throw new ValidationError("Amount may have at most two decimal places");
  if (amount > 99999999.99) throw new ValidationError("Amount must not exceed 99,999,999.99");'''
    assert old in t
    return t.replace(old, new, 1)
assert fe.rw('server/src/services/expenseService.js', patch_service)
def patch_test(t):
    add = '''
test('each amount rule has its own message', () => {
    const base = { description: 'x', category_id: 1, expense_date: '2024-02-01' };
    for (const [amount, message] of [
        ['abc', /finite number/],
        [0, /greater than zero/],
        [-5, /greater than zero/],
        [1.001, /two decimal places/],
        [100000000, /not exceed/],
    ]) assert.throws(() => service.parseExpense({ ...base, amount }), message, String(amount));
});
'''
    return t.rstrip('\n') + '\n' + add
assert fe.rw('server/test/reports.test.cjs', patch_test)
done.append('review#1 amount validation split into four messages (finite, > 0, two decimals, upper bound); test asserts each')

# review #2: half-open vs inclusive as exercise 1 replacement? keep exercises, add exercise 7 with acceptance test
fe.add_exercise(S, 'half-open or inclusive: make the two report paths agree',
"""`monthlySummary('2024-02')` computes its window from the month, while `byCategory({ start_date, end_date })` takes the range from the caller. Chapter 2 mentions that one is half-open and the other inclusive; prove it and fix it.

1. Seed an expense on `2024-03-01`. Predict what `byCategory({ start_date: '2024-02-01', end_date: '2024-03-01' })` returns for February if `end_date` is inclusive (it counts March 1) and if it is exclusive (it does not).
2. Write the acceptance test first: the February total from `monthlySummary('2024-02')` must equal the sum of `byCategory(...)` totals for the same February, and March 1 must not be double-counted when the next range starts there.
3. Pick one convention (half-open `[start, end)` is the usual choice), change `expenseQuery` in `server/src/models/expenseModel.js` accordingly, and update the message in `02-CONCEPTS.md`.""",
"""Reference acceptance test:

```js
test('monthly summary and category ranges agree on February', async () => {
  const summary = await service.monthlySummary('2024-02');
  const cats = await service.byCategory({ start_date: '2024-02-01', end_date: '2024-03-01' });
  const catTotal = cats.reduce((sum, c) => sum + Math.round(c.total * 100), 0);
  assert.equal(catTotal, Math.round(summary.total * 100)); // 3500 cents with the seeded data
});
```

With inclusive `end_date` this fails by 777.00 (the March 1 row). The fix is `where('expense_date', '<', filters.end_date)` in `expenseQuery` and a note in the API docs that `end_date` is exclusive.

Review: a range convention is an API contract; the test is what keeps the two report paths from drifting apart again."""); done.append('review#2 exercise 7: half-open vs inclusive agreement test with the fix (05, 06)')

# review #3: money representation worked solution in 06 (exercise 4 already asks for it)
fe.append_section(S, '06', '### Exercise 4 — worked solution: integer cents from SQL', """Change the aggregate so the database returns exact cents and the serializer formats them:

```js
// server/src/models/expenseModel.js (byCategory, dailyTotals, monthlySummary)
db.raw("ROUND(SUM(expenses.amount) * 100)::bigint as total_cents")
// serializer
total: Number(row.total_cents) / 100, totalCents: Number(row.total_cents)
```

`numeric` stays exact inside PostgreSQL; the `::float` cast was the only lossy step. With `total_cents` the test can drop `Math.round(x.total * 100)` and compare integers directly. Displayed values do not change because `total` is still returned. Review criterion: the reconciliation test in `reports.test.cjs` must compare `total_cents` sums across monthly, daily and category reports without any rounding in the test.""", before='## Review questions')
done.append('review#3 06 worked solution for integer cents (exercise 4), code left unchanged so the existing tests stay the contract')

RUN = """From the `server` folder, install dependencies once (`npm install`) and run `npm test`. The suite needs a PostgreSQL role that can `CREATE SCHEMA` in a database whose name starts with `astra_test_`; it creates a private schema per run and drops it afterwards. Point it at that database with `ASTRA_TEST_DATABASE_URL` (PowerShell: `$env:ASTRA_TEST_DATABASE_URL = "postgres://postgres:local-test@127.0.0.1:5432/astra_test_learning"`).

No local PostgreSQL? Use a throwaway container and create the database once:

```powershell
docker run --rm -d --name astra-pg -e POSTGRES_PASSWORD=local-test -p 5432:5432 postgres:18
docker exec astra-pg createdb -U postgres astra_test_learning
```

Stop it with `docker stop astra-pg` when you are done; nothing persists."""
fe.rw(fe.chapter(S, '04'), lambda t: fe.replace_section(t, r'Run the checks', RUN) or t)
done.append('review#4/#6 04 "Run the checks" rewritten with the Docker fallback and privilege note')

fe.set_variations(S, """**Normal variation — a non-leap February 29.** `parseExpense({ amount: 5, description: 'x', category_id: <food>, expense_date: '2023-02-29' })`. Predict: `validDate` throws (2023 is not a leap year) and nothing is written; then `'2024-02-29'` is accepted (the seeded leap-day row exists for exactly this reason).

**Invalid variation — the boundary instant.** Seed an expense on `2024-03-01`, then call `monthlySummary('2024-02')`: predict it is excluded. Now call `byCategory({ start_date: '2024-02-01', end_date: '2024-03-01' })`: predict whether the March 1 row is included, then check `expenseQuery` to see which comparison operator decides it (exercise 7).

**Boundary variation — an empty category.** Create a category with no expenses and call `byCategory` for February. Predict whether it appears at all (it does not: the query is an inner join grouped by category) and what exercise 2's `LEFT JOIN` version must return for it (`total: 0`, `count: 0`, never `null`)."""); done.append('review#5 three concrete variations')

B = [
("the report screen asks for a window",
 "`client/src/features` reports pages call the API with `month=YYYY-MM` or `start_date`/`end_date`; the client never sums anything itself, it renders the server's totals."),
("the request leaves the browser",
 "`GET /api/reports/monthly?month=2024-02`, `GET /api/reports/by-category?start_date=...&end_date=...` through the client's API service; errors arrive as the envelope's `error.message`."),
("the service validates the filters",
 "`server/src/services/expenseService.js`: `validDate` rejects impossible dates (`2024-02-30`) before SQL; `parseExpense` (line 12) now gives one message per amount rule; `byCategory`/`monthlySummary` build the filter object the model needs."),
("the model builds the aggregate query",
 "`server/src/models/expenseModel.js`: `expenseQuery(filters)` applies the date range and optional category; `byCategory` (line 166) clears the select and groups by `categories.id` with `SUM(expenses.amount)::float`; `monthlySummary` and the daily report derive their windows from the month. The two window conventions are the subject of exercise 7."),
("PostgreSQL computes the totals",
 "`amount` is `numeric(...)`; the sum is exact until the `::float` cast in the select. The tests seed five rows (`reports.test.cjs` `before`) and reconcile category, daily and monthly totals in cents to detect any drift."),
("the envelope returns numbers the client renders",
 "`sendSuccess` returns `{ success: true, data }` where totals are floats; exercise 4's worked solution returns `total_cents` alongside so the client can format exactly."),
]
fe.set_boundaries(S, B); done.append('2.2 trace-lab call path section (07)')
R = [
"the year-to-date window must be `[Jan 1, today)` computed in one place (the service) with an explicit exclusive end, and the test must seed a row dated today and one dated tomorrow and assert only today's is included.",
"the `LEFT JOIN` version must return every category with `COALESCE(SUM(...), 0)` and `COUNT(expenses.id)` (not `COUNT(*)`, which would count the null row as 1); the test asserts `total: 0, count: 0` for the empty category and unchanged totals for the others.",
"the week test must seed December 30, December 31 and January 1 and assert the week total crosses the year boundary correctly; state whether weeks start on Monday or Sunday in the query and pin it in the test.",
"the cents solution must keep the `numeric` sum exact in SQL (`ROUND(SUM(amount) * 100)::bigint`), keep the displayed `total` unchanged, and remove every `Math.round` from the reconciliation test; show the test diff.",
]
fe.set_reviews(S, R); done.append('2.3 per-exercise review criteria (06)')
fe.rw(fe.chapter(S, 'VERIFICATION'), lambda t: t.replace("Automated test cases: **3**.", "Automated test cases: **3** delivered by Astra, plus **1** added in the fix pass (one message per amount rule), for 4 in `server/test/reports.test.cjs`.", 1))
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w'))
print('\n'.join(done))
