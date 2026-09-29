# ww39 independent final review — REJECTED

Decision: reject the frozen candidate pending focused source and course repairs.

## Blocking source defects

1. `PrismaTicketRepository.markEscalated` conditionally updates `escalatedAt`, but `EscalationService` writes the audit row afterward through a separate repository call. If the audit insert fails, the ticket remains rerouted/escalated without its required durable audit event. The plan explicitly requires transaction-scoped mutation plus audit atomicity. The current mocked tests cannot establish rollback or cross-process behavior. Implement a repository transaction boundary that performs the conditional claim/routing update and audit insert together, and test the rollback contract with an injected transaction-capable fake (while labeling PostgreSQL durability as an integration limitation).
2. `hasCapability` indexes `roleCapabilities[user.role]` without optional lookup. A malformed runtime role can throw a 500 instead of failing closed. Change to `roleCapabilities[user.role]?.includes(capability) ?? false` and add an unknown-role regression at a route/service permission boundary.

## Required evidence/course repairs

- The saved result reports 14 tests across six files and typecheck pass, but the tests are service/helper doubles only. Add a regression that asserts audit failure leaves the claim/routing mutation unapplied through the new transactional fake, plus an actual route permission case for malformed roles.
- The nine guides currently total about 2,544 substantive words (README included), below the handoff target of about 4,000. Expand the worked examples and practice/solution pairs with source-grounded imports, placement instructions, and the transaction rollback/unknown-role cases. Do not pad with repeated prose.
- Preserve the explicit limitation that mocked tests do not prove PostgreSQL cross-process concurrency; the implementation still must expose and exercise the conditional claim contract.

The current SLA deadline selection, explicit rule eligibility/priority, terminal/no-deadline guards, conditional escalation state check, assignment omission/null handling, and foreign visibility helper are directionally correct. Do not apply until the two source blockers and evidence/course gaps are repaired, then rerun the complete source manifest checks including root build evidence.
