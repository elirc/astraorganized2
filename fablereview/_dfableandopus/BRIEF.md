# Brief: `dfableandopus/` job-and-interview content for every project

Owner: Fable (plan, review). Builders: Opus agents, one batch of ~10 projects each (`batches.json`). Date: 2026-09-18.

## Goal

Each of the 153 projects already has an `astraupskill/` course (how the app works, the worked change, practice). Add a sibling folder `dfableandopus/` that turns the **same project** into job-readiness material for CRUD web-app developer roles: interview questions a hiring panel would actually ask about this code, stories the learner can tell, drills that mimic screening rounds, a take-home that mimics a real hiring take-home, and the system-design follow-ups. Everything must be grounded in this project's real files, bugs and decisions; nothing generic.

## Files (exactly these seven, this order, these names)

| file | contents | size |
|---|---|---|
| `README.md` | what this folder is, how to use it in a 2-week interview prep, which target stack(s) it maps to, the one-paragraph pitch of the project ("what I built/fixed and why it matters"). Link every file. | 250-400 words |
| `01-INTERVIEW-QUESTIONS.md` | 24-30 questions with model answers, in four groups: **screening** (6-8: explain this app's data model, the request path, the boundary that validates), **deep-dive** (8-10: the actual bug the astraupskill worked change fixed, the transaction/versioning/idempotency decision, "what breaks if we remove line X"), **behavioral** (4-6: STAR answers built from this project's real change and its verification evidence), **follow-ups an interviewer asks after your answer** (4-6). Every technical answer cites a real `path:line` or symbol. Mark each question junior / mid. | 1500-2500 words |
| `02-STORIES-AND-RESUME.md` | 3 STAR stories from this project (Situation/Task/Action/Result, each Result with a measured fact from VERIFICATION.md or a test count), 5 resume bullets (past tense, quantified, no fluff), a 60-second spoken project summary, and "what I'd do next" (from the astraupskill practice or the fix report). | 600-900 words |
| `03-CODE-READING-DRILL.md` | 6 drills that mimic a live screen-share round: "explain this function" (paste a real 10-25 line excerpt with `path:line`), "spot the bug" (a **deliberately mutated** copy of a real excerpt with the mutation stated in a collapsed `<details>` answer), "predict the output/status code" (real request or call, answer with reasoning), "review this diff" (a small realistic diff against this codebase with 2-3 defects to find). Answers in `<details>` blocks. | 1200-2000 words |
| `04-TAKE-HOME.md` | one take-home assignment on THIS codebase as a company would set it (3-4 hours): a feature that touches validation, persistence and an HTTP or UI boundary; explicit acceptance criteria; what to submit; a **grading rubric** (table, 5-7 criteria, what a strong vs weak submission looks like); and a "reviewer's notes" section saying what the reviewer will look for first (tests, error paths, migration safety). Must be achievable with the project's existing test setup; name the exact test file and command. | 700-1100 words |
| `05-SYSTEM-DESIGN-FOLLOWUPS.md` | 6-8 "now scale it" questions interviewers ask about this app (multi-tenant, concurrent writers, background jobs, pagination at 1M rows, auth, observability, migration to the target stack), each with a grounded answer that starts from what the code does today (cite it) and names the trade-off. Include one ASCII diagram. | 900-1400 words |
| `06-FLASHCARDS.md` | 30-40 Q/A pairs as a two-column table, project-specific (symbol names, status codes, the exact invariant), usable for spaced repetition. | 500-900 words |

## Hard rules

1. **Read before writing.** Read the project's `astraupskill/README.md`, `01`, `02`, `03`, `VERIFICATION.md` and the fix report `fablereview/_fix/reports/<slug>.md`, then open the real source files they name. Quote code only by copying it; cite `path:line`. If you cite a line number, you looked at it.
2. **No template text across projects.** Fable will diff the folders; any paragraph appearing in two projects' folders is a defect. Question wording, stories and drills must be built from the specific project (its entity names, its bug, its status codes, its test names).
3. **Stack framing.** For JS/TS/Node/React/Next and C#/.NET projects, interview questions are about that stack. For off-stack projects (Java `j*`, Python `e14`, `e15`, `aiapplybot`, `andie` is Node) frame the questions as "you did this in X; here is how you'd answer for Node or .NET", using the project's existing `08-TRANSLATION.md` where it exists.
4. **Clones.** The 21 wave-1 clones (JS1: library-lending, gym-membership, campaign-planner, volunteer-coordinator, field-service, research-studies, travel-requests, vendor-contracts, quality-audits, grant-manager, incident-response, procurement-portal, property-rentals, patient-intake; newcodexJS 08, 09, 10, 17, 18, 19, 20) get the full seven files too, but the deep-dive questions, stories and take-home must be about **what differs** in that clone (its entity, its validation rules, its own test names); say in the README which project it is a variant of.
5. **Honesty.** Model answers may not claim behavior the code does not have. Where the astraupskill course names a known limit, an interview answer that mentions the limit is the strong answer; write it that way.
6. **Encoding and style.** UTF-8 without BOM, LF, Markdown headings, no em-dashes, no "in this exercise we will" filler, no agent-process language. Do not modify anything outside `<project>/dfableandopus/` except the log below. Do not run installs, builds or tests.
7. **Log.** After each project append one JSON line to `fablereview/_dfableandopus/progress/<batch>.jsonl`: `{"slug":..., "files":7, "words":N, "cited_files":[...], "notes":"..."}`.

## Review (Fable)

After each batch: duplication scan across all `dfableandopus/` folders (shared-paragraph %), citation spot-check on disk (do the cited lines say what the answer says), size check per file, and a read of one full folder per batch for tone and correctness. Batches that fail are sent back with the exact defects.
