from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "stage"
CHAPTERS = ["README.md", "01-CODEBASE-MAP.md", "02-CONCEPTS.md", "03-WORKED-CHANGE.md", "04-TESTING-AND-DEBUGGING.md", "05-PRACTICE.md", "06-SOLUTIONS-AND-REVIEW.md", "07-TRACE-LAB.md", "VERIFICATION.md"]
PROJECTS = {
    "fdad4e87a703": {
        "name": "zz2 support operations", "entry": "src/server/modules/tickets/service.ts", "test": "src/server/modules/tickets/service.test.ts",
        "bug": "ticket references were made from the last six timestamp digits, so same-millisecond creates could collide with Prisma's unique Ticket.reference constraint",
        "fix": "randomUUID entropy preserves the SUP- prefix while making each request reference independent of wall-clock resolution",
        "trace": "createTicket validates permission and queue access, loads the SLA policy, calculates the snapshot, then calls TicketRepository.createTicket",
        "layers": "Next route and Zod schema -> TicketService policy -> TicketRepository -> Prisma Ticket and audit rows",
    },
    "74faaa8b7040": {
        "name": "buildaffiliate", "entry": "apps/api/src/services/campaign.service.ts", "test": "apps/api/src/services/campaign.service.test.ts",
        "bug": "campaign slugs used Math.random, leaving a weak and untestable collision boundary for a database field that identifies links",
        "fix": "randomUUID supplies the full 32-hex-character UUID entropy after the normalized name, retaining readable URLs while avoiding shared PRNG timing",
        "trace": "the brand route parses input, authentication supplies the brand id, campaignService creates the slug and campaignRepository persists the scoped record",
        "layers": "Fastify route and Zod schemas -> campaign service authorization and lifecycle -> Prisma repository -> Campaign and tracking-link data",
    },
    "54397e702f3f": {
        "name": "buildanalytics", "entry": "backend/src/modules/dashboardConfigs/dashboardConfigs.service.ts", "test": "backend/src/modules/dashboardConfigs/dashboardConfigs.service.test.ts",
        "bug": "a role-only PATCH could move an already-default dashboard config without clearing the previous default for the new role, creating competing defaults",
        "fix": "defaultUpdateTarget derives the effective role and default flag from persisted and patch values before the transaction clears peers",
        "trace": "Express permission middleware authorizes configuration writes, the controller passes validated input, the service computes the target and updates Prisma transactionally",
        "layers": "React dashboard consumer -> Express route and Zod validator -> service transaction -> Prisma DashboardConfig rows",
    },
}

def body(meta, chapter):
    marker = f"The focus of this chapter is {chapter}; use that lens while reading the trace."
    intro = f"This chapter is grounded in {meta['name']}. The production entry point is `{meta['entry']}` and the focused regression is `{meta['test']}`. The bounded correctness issue was that {meta['bug']}. The implementation changes {meta['fix']}. Read the surrounding code before generalizing: this repository has the layers described below and does not gain an imagined service, tenant, or queue merely because the exercise uses CRUD language. {marker}\n\n"
    map_text = f"The request path is concrete: {meta['trace']}. The implemented layers are {meta['layers']}. Start at the route or caller, then follow the parsed input into the domain operation and finally the repository call. Mark each value as untrusted transport data, validated domain data, or persisted data. For `{meta['entry']}`, identify where authorization, validation, state transition or uniqueness is enforced. Then read `{meta['test']}` and name the production function it imports. A test that copies the algorithm into a fake helper can pass while the real regression remains; this course requires the test to exercise the production boundary. {marker}\n\n"
    concepts = "The central lesson is that a TypeScript type, a UI affordance, or a database constraint alone does not describe the complete request contract. Runtime input needs a parser; authorization needs an actor and resource check; a workflow needs an allowed transition; persistence needs a transaction or unique constraint when concurrent writers are possible. Decide which guarantee belongs in which layer and what happens on failure. A 400 means the caller supplied an invalid shape, 403 means the authenticated actor lacks authority, 404 means the resource is absent or intentionally hidden, and a 409 is useful when a uniqueness race is a user-visible conflict. Do not turn a passing unit test into a claim about network retries, browser rendering, or production concurrency unless those behaviors were executed. " + marker + "\n\n"
    worked = f"For the worked trace, compare the baseline snapshot with the staged file. Before the change, the risky path was: accept the request, derive the identifier or default decision, and persist. Under concurrent or partial PATCH input, that path could produce {meta['bug']}. After the change, the operation first derives the value needed for the invariant, then performs the existing write. In `{meta['test']}`, the regression calls the exported production helper or service and asserts the observable contract, including the shape of generated data or the effective default target. Explain why the fix is bounded: it does not redesign the repository, add a new API, or claim that database races disappear without a unique constraint and transaction. {marker}\n\n"
    testing = f"Run the focused test command recorded for this staged project and inspect failures from the first assertion. Add a negative test for the old behavior, then a positive test for the legal path. For {meta['name']}, also run the existing suite if dependencies are already present; installation is recorded separately. Debug by logging the actor, resource id, effective status or identifier, and repository arguments in a local test double, while keeping secrets out of output. Verify that an authorization failure performs no write, that invalid patch data does not reach Prisma, and that a failed transaction does not leave competing defaults or a partially created record. The test file `{meta['test']}` is runtime evidence; static grep is only a supplement. {marker}\n\n"
    practice = "Practice A: draw the UI, HTTP, domain, data and failure edges for one create and one update. Practice B: predict the result for missing ownership, malformed input, a duplicate request, and a concurrent write. Practice C: write a regression that proves the repository is not called after the guard fails. Practice D: propose an idempotency key or optimistic version field and state the schema and transaction changes it would require. Practice E: review the patch as a senior engineer: identify the invariant, the smallest owner of it, the failure status, the test seam, and the remaining operational limitation. Keep solutions separate until you have written your prediction. These exercises should be answered from the concrete files named above, with line-level evidence and a command that another engineer can rerun. " + marker + "\n\n"
    solutions = "A strong solution names the invariant in one sentence, follows the actual call order, and distinguishes validation from authorization and persistence. It tests both the happy path and the prohibited side effect. A weak solution adds a client-only check, swallows a database error, duplicates production logic in the test, or asserts that a random-looking value is unique without acknowledging the database constraint. Review for input normalization, stable error mapping, tenant or owner scoping where the repository has it, atomic updates for coupled records, and clear audit behavior. Ask whether retries are safe, whether a repeated request can duplicate a row, and whether the code leaves a valid previous state after failure. The correct review comment is specific: cite the function, trigger, expected result, and test that should demonstrate it. " + marker + "\n\n"
    trace = f"Trace lab: start with an actor and a representative request. At each boundary record input, guard, side effect and resulting state. The expected path is `{meta['trace']}`. Then replay it with an unauthorized actor, a missing resource, a malformed patch, and a second request. For the old implementation, mark where {meta['bug']} could occur. For the revised implementation, mark where {meta['fix']} is established and what still depends on Prisma or the deployment. Finish by writing one question the current tests cannot answer, such as cross-process contention, real HTTP middleware composition, or frontend rendering. That question belongs in limitations, not in an invented success claim. {marker}\n\n"
    verification = "Verification is evidence, not a slogan. Report the exact command, working directory, pass or fail result, and whether it executed production modules. Separate focused regression results from type checking, linting, integration tests and unavailable external systems. Preserve the original snapshots for every changed baseline file, keep the nine course chapters out of the changedFiles spec list, and list the actual source and test files in the handoff. State limitations plainly: an in-memory fake cannot establish cross-process locking; a helper test cannot establish HTTP middleware; a parser test cannot establish UI behavior. A future maintainer should be able to reproduce the check, understand the invariant, and know which broader test is needed before changing the boundary again. " + marker + "\n"
    sections = {
        "README.md": "# CRUD correctness upskill\n\n" + intro + map_text + concepts + "Use the chapters in order. Make predictions before running tests, then compare them with the recorded behavior.\n",
        "01-CODEBASE-MAP.md": "# Codebase map\n\n" + intro + map_text + trace,
        "02-CONCEPTS.md": "# Concepts\n\n" + intro + concepts + worked,
        "03-WORKED-CHANGE.md": "# Worked change\n\n" + intro + worked + trace,
        "04-TESTING-AND-DEBUGGING.md": "# Testing and debugging\n\n" + intro + testing + verification,
        "05-PRACTICE.md": "# Practice\n\n" + intro + practice + map_text,
        "06-SOLUTIONS-AND-REVIEW.md": "# Solutions and review\n\n" + intro + solutions + testing,
        "07-TRACE-LAB.md": "# Trace lab\n\n" + intro + trace + practice,
        "VERIFICATION.md": "# Verification\n\n" + intro + verification + testing,
    }
    return sections[chapter]

for project, meta in PROJECTS.items():
    out = ROOT / project / "astraupskill"
    out.mkdir(exist_ok=True)
    for chapter in CHAPTERS:
        (out / chapter).write_text(body(meta, chapter), encoding="utf-8")
        assert len(body(meta, chapter).split()) >= 250, (project, chapter)
        print(project, chapter, len(body(meta, chapter).split()))
