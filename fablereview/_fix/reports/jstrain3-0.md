# _Organized Desktop/04 JavaScript Training/jstrain3.0 — fix report (B16)

Fable, 2026-09-18.

## Done
- review#1 server/package.json gains "test": "node --test tests/*.test.mjs"; VERIFICATION and 04 reference npm test --prefix server
- review#3 02 explains deferred vs immediate vs exclusive and why checkout.js uses immediate
- review#4 05 gains the two missing negative cases (accumulated-total overflow, forced zero-row conditional UPDATE) as exercises with skeleton tests
- review#2 cart.js and orders.js re-indented with prettier in the pipeline (see report); the delivery-record after-hash is not regenerated (no hash field in VERIFICATION)

## Skipped
- (none)

## Verification
- cart.js and orders.js reformatted with prettier (single quotes, 110 cols) and parse-checked; then a temporary npm install in server/ (170 packages) and npm test (the new script): 6/6 passed; node_modules removed

## Course/code consistency check
- VERIFICATION and 04 name the script that now exists; the 02 transaction-mode section quotes the immediate call in checkout.js.

## Phase 3 addendum (glossary)

Added a `## Prerequisites and glossary` section to `astraupskill/README.md` with a prerequisites line and a 12-term table (input boundary, positive safe integer, persisted-state preflight, cart line validation, typed error, re-read inside the transaction, immediate transaction, conditional update, changes count, atomic rollback, owner scope, database seam). Verified every term against the source before citing it: the files `server/src/services/cartValidation.js`, `server/src/routes/cart.js`, `server/src/services/checkout.js`, `server/src/routes/orders.js`, and the symbols and identifiers `positiveSafeInteger`, `Number.isSafeInteger(value) && value >= 1`, `cartValidation.js`, `positiveSafeInteger(existing.quantity, ...)`, `validateCartLine(quantity, stock, name)`, `CartValidationError`, `InsufficientStockError`, `SELECT`, `checkout`, `createOrder.immediate(userId)`, `UPDATE products SET stock = stock - ? WHERE id = ? AND stock >= ?`, `checkout.js`, `if (changed.changes !== 1)`, `database.transaction(...)`, `req.user.id`, `createCartRouter(database, authMiddleware)`.

## Phase 3 addendum (code blocks)

The codeblocks gate found no fenced code block in chapter(s) 07. One real excerpt was added to each, quoted from this project and cited in the chapter text:

- **07** - server/src/services/checkout.js (checkout transaction)

No source code was changed; only the chapter Markdown.
