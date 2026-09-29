# Fable review rubric: how good is each Astra course at upskilling a junior SWE in CRUD web dev?

Target learner: a junior software engineer who wants to become dependable at CRUD web development on the
JS/TS stack (React, Node/Express, Next.js, TypeScript) and the C#/.NET stack (ASP.NET, EF Core), with SQL.

Astra's deliverable per project = code changes applied to the original folder + a 9-file `astraupskill/` course
(README, 01-CODEBASE-MAP, 02-CONCEPTS, 03-WORKED-CHANGE, 04-TESTING-AND-DEBUGGING, 05-PRACTICE,
06-SOLUTIONS-AND-REVIEW, 07-TRACE-LAB, VERIFICATION).

Score each dimension 1-5. Evidence beats impression: every score below 4 needs a concrete file:line or quote.

| # | Dimension | 5 looks like | 1 looks like |
|---|---|---|---|
| D1 | **Accuracy** (course vs. actual code) | Every excerpt, path, line reference, command and claimed behavior matches the code on disk today. | Course describes code that is not there, wrong paths, stale line refs, or claims features that do not exist. |
| D2 | **Code-change quality** | The change is a real, meaningful CRUD/reliability improvement; tests exercise the changed behavior (not just "calls happened"); no regressions or dead code introduced. | Cosmetic edits, tests that pass trivially, or the "improvement" breaks or bypasses existing behavior. |
| D3 | **Pedagogy** | Predict -> run -> change -> verify loop is real; first-principles explanations; failure cases; solutions kept separate from exercises; exercises escalate from guided to independent. | Wall of prose, no predictions, exercises are "read the code", solutions inline with prompts, no failure lab. |
| D4 | **CRUD relevance to the target stacks** | Teaches validation, ownership/authz, transactions, idempotency, pagination, error handling, persistence on JS/TS/React/Node/Next or C#/.NET. | Project or lesson is off-stack (Python, game, AI plumbing) or the lesson teaches something unrelated to CRUD web dev. |
| D5 | **Reproducibility** | A junior can follow the setup section on a fresh machine: pinned toolchain, exact commands, fixtures, ports, what to expect. | Setup commands missing, wrong, or depend on state only Astra's sandbox had. |
| D6 | **Verification honesty** | VERIFICATION.md matches evidence JSON; limits are stated; test counts are real; nothing is overclaimed. | Claims "browser check passed" with no evidence, inflated counts, limits hidden. |
| D7 | **Junior fit** | Vocabulary defined, reading order sane, chunked, session plan realistic (a few hours per chapter); doesn't assume senior knowledge. | Assumes DI/CQRS/CRDT fluency, 20k-word dumps, or so shallow it teaches nothing. |
| D8 | **Specificity** (anti generic-template) | Content is specific to this project's domain and code. | Boilerplate paragraphs copy-pasted across projects with the noun swapped; exercises could apply to any app. |

**Verdict** (one per project):
- **KEEP** — use as-is in the learning path (avg >= 4.0, no dimension < 3).
- **IMPROVE** — worth keeping, needs listed fixes (avg 3.0-3.9, or any dimension = 2).
- **REWORK** — course or change is misleading/off-target; redo or drop from the path (avg < 3.0, or any dimension = 1, or D1/D6 <= 2).

**Learning-path role** (one per project): `core` (should be in the main sequence), `elective` (good for a specific
gap), `reference` (read, don't do), `skip` (not worth a junior's time for CRUD upskilling).

Reviewers must NOT install dependencies, run builds, run tests, or modify any project folder. Read-only review.
Spot-check claims by reading code, tests, backups and evidence JSON. If a claim cannot be verified read-only, say so.
