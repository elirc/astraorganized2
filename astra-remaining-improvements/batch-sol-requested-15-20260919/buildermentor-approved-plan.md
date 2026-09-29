# BuilderMentor approved plan

## Defect and boundary

Retrieval failures escaped as provider/database details, while fixture coverage did not establish exact local ingestion provenance, user-scoped retrieval, ranking behavior, or deterministic ties.

## Change

- Keep ownership filtering in production SQL (`sources.user_id`) and expose an injected retrieval core for deterministic fixtures.
- Reject unavailable, empty, or nonfinite embedding results with a stable `retrieval_unavailable` 503 message.
- Preserve similarity floors and topic boost, then break equal scores by chunk identity; use the same stable identity tie-break in SQL candidate ordering.
- Add a checked-in fictional Markdown fixture for extraction and chunk provenance tests.

## Acceptance and verification

Tests must verify exact fixture extraction, character offsets, heading/page metadata, topic boost, minimum similarity, limit, deterministic ties, user scope passed to the query boundary, and safe failures with no provider details. Run the focused API tests and typecheck after dependencies are available; evidence must describe fixture-only retrieval rather than a live provider or pgvector integration.
