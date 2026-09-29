# Astra final improvement plan

[All 50 implemented projects and learning courses](../astrdocs/ALL_50_PROJECTS_REPORT.md), including the next-30 delivery.

[Completed implementations and learning courses for the first ten projects](TEN_PROJECTS_IMPLEMENTED.md).

**Created:** 2026-09-08. **Scope:** 389 Desktop project/workspace/resource records, including all 202 `_Organized Desktop` records, plus 75 individually planned nested teaching apps: **464 entries**.

The recommendation is to improve a small sequence deeply and use the rest as targeted exercises or references. Every reviewed location has an improvement plan; it is not necessary to finish every location. Copies remain separate because the prior review did not establish full-tree identity.

## Five sections

| Section | Focus | Root records | Nested apps |
|---|---|---:|---:|
| [1. Foundations and learning content](01-foundations-and-learning-content.md) | Original milestones 0–1 | 48 | 0 |
| [2. Client apps, APIs and persistence](02-client-apps-and-apis.md) | Original milestones 2–3 | 40 | 5 |
| [3. Full-stack workflows and a capstone](03-full-stack-workflows.md) | Original milestones 4 | 66 | 18 |
| [4. Domain rules and reliability](04-domain-rules-and-reliability.md) | Original milestones 5 | 86 | 37 |
| [5. Architecture and specializations](05-architecture-and-specializations.md) | Original milestones 6–7 | 149 | 15 |

## Suggested execution order

This is a milestone sequence, not a calendar commitment. Keep one main project and at most one short reinforcement exercise active. Move on when you meet the stage criterion; skip a fundamentals milestone you can already demonstrate.

1. **Foundations:** use [_Organized Desktop/04 JavaScript Training/jstrain2.2](01-foundations-and-learning-content.md#p073) as the main course; use [JS1](01-foundations-and-learning-content.md#p351) for a small independent browser exercise. Improve the diagnostic, attempt/solution separation and feedback. JSProjectLearn and other courses are alternatives, not parallel homework.
2. **Client, API and SQL:** improve [recipeweb](02-client-apps-and-apis.md#p384) with a persisted, keyboard-usable shopping-list flow; [jobtrack](02-client-apps-and-apis.md#p350) is an alternative for local-data practice. Then complete [newcodexJS/01-task-manager](02-client-apps-and-apis.md#p440). Verify setup and the source behind the FABLE lesson; document where the scaffold differs from the explanation.
3. **Full-stack capstone:** use [newcodexJS/05-recipe-manager](03-full-stack-workflows.md#p444) for account ownership and a transaction, then choose [gitjira-app](03-full-stack-workflows.md#p319) as the capstone. Own one useful issue workflow from UI to stored state, including authorization and failure feedback. Continue improving it instead of adding another full-stack app.
4. **Reliability:** add a concurrency/retry or transaction case to that capstone. Use [gitvg/agora](04-domain-rules-and-reliability.md#p320) only if checkout/stock teaches the missing rule. After the capstone, [borrowbox](02-client-apps-and-apis.md#p221) followed by [campusops](04-domain-rules-and-reliability.md#p231) is an optional C#/.NET branch if it serves your role goals.
5. **Advanced branch:** use [gitvg/relay](05-architecture-and-specializations.md#p333) for one bounded retry/adapter exercise after the reliability gate. Alternatively choose one advanced reference, AI, mobile or game project after its relevant prerequisites; do not start all branches.

## What to improve in the learning content

For the chosen project, improve the existing populated Fable/tutorial location first. Use a single linked entrypoint rather than create another competing edition. Add these components only where missing:

- **Start here:** audience, prerequisites, measured setup instructions, fixtures and the one supported learning path.
- **Codebase map:** source-linked entrypoints, major boundaries, a request/event/data-flow example and the observed state before and after.
- **Practice:** predict the behavior, run a worked example, complete a guided change, then solve an independent variation; keep answers separate.
- **Failure lab:** one relevant invalid action, interrupted write, retry or concurrency case. Include expected results and debugging clues, not only the happy path.
- **Completion rubric:** explain the changed code, demonstrate behavior, show focused verification and record the tradeoff.
- **Provenance:** reviewed revision/date, actual implementation versus plans/mocks, and a list of outdated or empty chapters. Do not delete intentional exercise TODOs.

For resource-only folders, improve the index, exercises, evidence and relevance to the active project. For large upstream codebases, write one feature trace and a bounded contribution exercise. Neither needs a speculative full rewrite.

## How to carry out each project plan

Each entry has an evidence baseline, documentation starting point, a content task, a project/resource task and a completion criterion. The existing review’s learning focus and next action supply the project-specific scope; documentation maturity determines whether to extend a course or create a first walkthrough. Acceptance scenarios are proposed engineering exercises, not newly observed failures.

Use this order for an activated entry: **reproduce → explain → change → verify → update the lesson**. Record the setup commands and their results in that project when implementation begins. If a proposed behavior already works, improve its explanation or add a missing meaningful regression rather than rebuild it. Keep the current dependency versions initially; investigate any actual setup failure before proposing upgrades.

For alternate copies, first compare the relevant manifest, source, docs and working setup. Pick a baseline and record why; preserve distinct exercises and do not infer that a later name or folder suffix means better code. For JS/.NET pairs, complete one implementation, then use the other for a small comparison exercise.

Use fake providers and local data for payment, email, AI and external integration lessons. A UI prototype gets honest local behavior and a clear future API contract before production architecture. Backend-only projects do not need a frontend merely to satisfy a checklist.

## Progress tracking

| Entry | Status | Baseline/setup evidence | Content change | Project change | Completion evidence | Next decision |
|---|---|---|---|---|---|---|
| Selected project path | Not started / Active / Verified / Deferred | Commands and observed result | Guide or exercise | Bounded behavior | Test/demo and explanation | Continue / consolidate / switch |

A useful study session ends with a small demonstrated behavior or a diagnosed obstacle. Count independently explained and verified changes, not pages read or repositories opened. Keep remaining entries deferred until they address a measured gap.

## Coverage and evidence

- [Master source review](../astradocs/MASTER_REPORT.md) and [structured project review](../astradocs/project-review.json): project identity, stack, learning focus, prerequisites, assessment and next action.
- [Tutorial report](../astradocs/PROJECT_TUTORIALS_REPORT.md) and [structured tutorial review](../astradocs/project-tutorials.json): guide classification, populated entrypoints, placeholders and caveats.
- [Final Desktop coverage review](../astradocs/FINAL_REVIEW.md): recursive discovery coverage and excluded dependency/generated directories. The 29 empty placeholders remain documented there; they have no codebase to improve and are not counted as projects here.
- [Machine-readable improvement plans](project-plans.json) and [validation results](validation.json).

This is a planning synthesis of the completed September 6–7 reviews, not a new execution audit or a new full Desktop scan. No source app was built, tested or modified for this plan. The baseline assessments remain static observations; reproduce them against the selected current checkout before implementation. Scope reconciliation and local-link validation are performed for this deliverable.

## Rebuild the report

`python astrafinalplan/_build_plan.py` regenerates the five sections, index and structured plans from the two reviewed JSON inputs, then validates coverage and links. Edit the generator’s curated overrides/rules if regenerating; direct edits to generated reports would otherwise be replaced.

## Latest implementation: 75 projects

[All 75 projects and learning courses](../astrdocs/ALL_75_PROJECTS_REPORT.md). The latest 25 CRUD-focused improvements are applied to their original folders, with nine detailed learning files each.
