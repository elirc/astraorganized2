from course_writer import write_course

CHAPTERS = [
    "README.md",
    "01-CODEBASE-MAP.md",
    "02-CONCEPTS.md",
    "03-WORKED-CHANGE.md",
    "04-TESTING-AND-DEBUGGING.md",
    "05-PRACTICE.md",
    "06-SOLUTIONS-AND-REVIEW.md",
    "07-TRACE-LAB.md",
    "VERIFICATION.md",
]

PROJECTS = [
    dict(
        id="5be7edf43612", name="GitJira", purpose="Jira-style issue and sprint management",
        entry="apps/web/src/pages/BacklogPage.jsx", service="apps/api/src/services/sprint.service.js",
        test="apps/api/test/sprint.test.js", storage="apps/api/prisma/schema.prisma",
        boundary="sprint assignment and completion", state="PLANNED, ACTIVE, and COMPLETED sprint states plus Issue.updatedAt",
        defect="an assignment could race completion, and a stale browser could overwrite a newer sprint choice",
        fix="serializable bounded transactions, state-qualified updates, destination validation, and an updatedAt compare-and-swap",
        valid="a member assigns a current issue to an eligible sprint", invalid="a nonmember, stale timestamp, foreign sprint, or completed destination",
        race="assignment versus completion and duplicate completion", command="python scripts/test-local.py sprint.test.js",
        limit="The checks use a helper-owned PostgreSQL cluster; they do not certify deployment, Redis, or browser end-to-end behavior.",
    ),
    dict(
        id="af5130b3aad2", name="BuildEvent", purpose="event ticket reservation, payment, and venue check-in",
        entry="apps/api/src/routes/order.routes.ts", service="apps/api/src/services/order.service.ts",
        test="apps/api/tests/order-checkin.test.ts", storage="apps/api/prisma/schema.prisma",
        boundary="checkout creation, order completion, and QR check-in", state="PENDING and COMPLETED orders, VALID and CHECKED_IN tickets, and reserved versus sold inventory",
        defect="concurrent checkout or completion could duplicate provider work or inventory changes, while a QR was not bound to the route event",
        fix="stable provider idempotency keys, conditional persistence, one-winner completion and check-in predicates, and event binding",
        valid="the owner starts checkout and staff scans a valid ticket for the authorized event", invalid="an invalid amount, changed order, repeated scan, or cross-event QR",
        race="two checkout calls, two completion calls, and two scanners", command="npm --workspace @ticketing/api test -- order-checkin.test.ts",
        limit="Provider behavior is simulated with fakes; the course does not claim Stripe exactly-once delivery or production webhook certification.",
    ),
    dict(
        id="3b9c30ec3ce2", name="ReviewDeck", purpose="local-first pull-request review drafting and batch publication",
        entry="apps/web/src/lib/api.ts", service="apps/api/src/modules/publish/publish.service.ts",
        test="apps/api/test/api.e2e.spec.ts", storage="apps/api/prisma/schema.prisma",
        boundary="claiming and publishing a review session", state="DRAFT, PUBLISHING, and PUBLISHED sessions plus DRAFT, FAILED, and PUBLISHED comments",
        defect="two requests could both pass a DRAFT read, while an uncertain remote outcome was reset to retryable DRAFT",
        fix="an atomic DRAFT-to-PUBLISHING claim, conditional rollback for definite rejection, and an explicit ambiguous outcome",
        valid="one publisher claims a current session and records returned review identifiers", invalid="a concurrent publisher, moved head, definite 422 rejection, or ambiguous timeout",
        race="two publish requests and remote success followed by local finalization failure", command="npm run test -w @reviewdeck/api -- --runInBand",
        limit="Tests use a fake code-host provider and SQLite; ambiguous outcomes still require human reconciliation with the pull request.",
    ),
    dict(
        id="a81b176807e5", name="ShipShape", purpose="source ingestion, grounded retrieval, and adaptive study generation",
        entry="apps/api/src/ingest/pipeline.ts", service="apps/api/src/rag/retrieve.ts",
        test="apps/api/test/ingest-retrieval.test.ts", storage="apps/api/src/db/schema.ts",
        boundary="turning a local source into provenance-preserving chunks and user-scoped retrieval results", state="source pipeline states and ranked chunks filtered by owner, readiness, model, and similarity",
        defect="retrieval dependencies failed as generic internal errors and fixture-level provenance and ranking lacked regression coverage",
        fix="an injected retrieval seam, deterministic row ranking, a safe typed unavailable error, and a checked local Markdown fixture",
        valid="a user retrieves ready chunks from that user's library with exact source offsets", invalid="an unavailable embedding tool or a result below the similarity floor",
        race="provider failure while generation requests grounded context", command="pnpm --filter @shipshape/api test -- ingest-retrieval.test.ts",
        limit="The fixture verifies local parsing and ranking logic; it does not measure production embedding quality or run an external model.",
    ),
    dict(
        id="9d3b119f40a0", name="Skillforge", purpose="short coding lessons, spaced review, quests, and learner progress",
        entry="src/features/lessons/lesson-player.tsx", service="src/server/completion.ts",
        test="tests/unit/completion.test.ts", storage="prisma/schema.prisma",
        boundary="lesson completion through review seeding and the award ledger", state="LessonCompletion, ReviewState, Progress, XpEvent, Quest, and UserAchievement rows",
        defect="concurrent completions could both award progress and a failure could commit completion without review or XP state",
        fix="one SQLite transaction, a unique completion gate, one injected clock, transaction-client propagation, and bounded known-busy retry",
        valid="an eligible lesson completes once and seeds every knowledge item at the same due time", invalid="an unknown or empty lesson, repeated completion, or injected late failure",
        race="two completion actions for one learner and lesson", command="node scripts/test-completion-local.mjs",
        limit="The test uses a helper-owned temporary SQLite database and local fixtures; it does not exercise browsers or external code runners.",
    ),
]


def paragraph(project, focus, instructions):
    return f"""
{project['name']} is a useful study system because its visible product behavior crosses a real state boundary. Its purpose is {project['purpose']}. In this course, the central slice is {project['boundary']}. Read `{project['entry']}` first to learn how an input is formed, then `{project['service']}` to see where authority and state are checked, and finally `{project['storage']}` to confirm which invariants the database can actually enforce. The relevant state is {project['state']}. Keep those nouns on paper while tracing; vague labels such as “save” hide the decision points that matter.

The concrete failure examined here is that {project['defect']}. The repair uses {project['fix']}. That combination matters because validation before a write is only a snapshot. A competing request can change the same rows after validation. A reliable path therefore binds the decision to the mutation with a conditional predicate, transaction, unique constraint, stable idempotency key, or an explicit failure state. The exact mechanism differs by repository, but the reasoning stays transferable: identify who owns the state, state the allowed transition, make one operation the winner, and give every loser an honest result.

For the {focus} pass, {instructions} A valid example is {project['valid']}. A meaningful invalid example is {project['invalid']}. The concurrency probe is {project['race']}. Predict database state and outward response before running anything. Then compare the prediction with `{project['test']}`. A useful explanation names both: “the response is rejected” is incomplete unless it also says which rows remained unchanged; “the row changed” is incomplete unless it states what the caller sees and can safely do next.

Use `{project['command']}` only in the prepared isolated environment. Record the exact command, exit status, test count, and relevant runtime in the verification chapter. Do not convert an unexecuted command into evidence. {project['limit']} That limitation is part of the engineering result: it tells the next maintainer which conclusion is supported, which boundary is simulated, and where another integration or operational test would add information.
"""


def chapters_for(project):
    bodies = {
        "README.md": paragraph(project, "orientation", "build a vocabulary of actors, inputs, durable rows, external effects, and returned errors before changing code."),
        "01-CODEBASE-MAP.md": paragraph(project, "mapping", "draw arrows from the entry point to validation, service logic, persistence, and response shaping. Mark every read and write, and circle external calls."),
        "02-CONCEPTS.md": paragraph(project, "concept", "separate authorization, validation, idempotency, atomicity, isolation, and optimistic concurrency. Explain which mechanism answers which failure."),
        "03-WORKED-CHANGE.md": paragraph(project, "worked change", "reconstruct the before path, locate the check-then-write gap, and walk the changed predicate or transaction line by line. State why each new condition exists."),
        "04-TESTING-AND-DEBUGGING.md": paragraph(project, "testing", "start with one valid operation, one domain rejection, and one competing operation. Inspect stored state after the response instead of asserting status alone."),
        "05-PRACTICE.md": paragraph(project, "practice", "first annotate the supplied flow without editing it. Next design an additional failure test. Finally propose one bounded variant and list the invariant it must preserve."),
        "06-SOLUTIONS-AND-REVIEW.md": paragraph(project, "review", "compare a candidate solution against the database predicate, error contract, and retry behavior. Reject solutions that only narrow the timing window."),
        "07-TRACE-LAB.md": paragraph(project, "trace lab", "make a two-column timeline for request A and request B. At every await or database statement, write the state each request can observe and the next lock or predicate."),
        "VERIFICATION.md": paragraph(project, "verification", "distinguish static inspection, fixture tests, database integration, and provider simulation. Leave result fields pending until the named commands actually finish."),
    }
    excerpts = {
        "README.md": [("README.md", "", 8)],
        "01-CODEBASE-MAP.md": [(project["entry"], "", 12)],
        "02-CONCEPTS.md": [(project["storage"], "", 10)],
        "03-WORKED-CHANGE.md": [(project["service"], "", 14)],
        "04-TESTING-AND-DEBUGGING.md": [(project["test"], "", 12)],
        "05-PRACTICE.md": [(project["service"], "", 10)],
        "06-SOLUTIONS-AND-REVIEW.md": [(project["test"], "", 10)],
        "07-TRACE-LAB.md": [(project["service"], "", 12)],
        "VERIFICATION.md": [("package.json", "", 12)],
    }
    titles = {
        "README.md": f"{project['name']} source-based improvement course",
        "01-CODEBASE-MAP.md": "Codebase map",
        "02-CONCEPTS.md": "Concepts behind the state boundary",
        "03-WORKED-CHANGE.md": "Worked change",
        "04-TESTING-AND-DEBUGGING.md": "Testing and debugging",
        "05-PRACTICE.md": "Practice",
        "06-SOLUTIONS-AND-REVIEW.md": "Solutions and review rubric",
        "07-TRACE-LAB.md": "Trace lab",
        "VERIFICATION.md": "Verification record",
    }
    return {name: (titles[name], bodies[name], excerpts[name]) for name in CHAPTERS}


for project in PROJECTS:
    write_course(
        project["id"],
        chapters_for(project),
        "It complements the existing project and learning documentation with a focused trace, regression, and practice sequence.",
    )
