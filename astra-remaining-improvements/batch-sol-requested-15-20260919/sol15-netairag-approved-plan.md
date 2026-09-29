# NetAiRag approved plan

`RunIncidentInvestigationAsync` currently counts logs, emits hand-interpolated JSON, reports three tool calls while saving one, and fabricates confidence, token, and cost values. Existing knowledge documents contain runbooks but no retrieval path uses them.

Add a pure, bounded lexical retriever over title, tags, and content with stable ranking, deterministic tie-breaking, top-k, and explicit no-match behavior. The existing authorized investigation path will query knowledge rows, persist actual document ids and heuristic scores in a `SearchKnowledge` tool call alongside bounded log evidence, and serialize input/output with `System.Text.Json`. The no-LLM path records zero model tokens/cost and does not present a heuristic retrieval score as model confidence. Timestamps use actual operation bounds.

Fixed local evaluation cases cover Billing, Auth, stable ties/top-k, and unrelated no-match. Unit tests cover ranking and JSON escaping. A service persistence test verifies permissions, saved tool count/evidence JSON, and pending approval with an isolated fixture; an EF in-memory fixture, if used, is labeled as service behavior rather than SQL evidence. Verification is `dotnet build` and `dotnet test`; no model, vector provider, external service, or original database is used.
