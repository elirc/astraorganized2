# BuildReviewer approved plan

## Defect and boundary

`PublishService.publish` previously checked `DRAFT` and called the provider before changing the session, so two requests could both create a remote review. Recovery also needed to distinguish a definite GitHub rejection from an ambiguous response or a local commit failure after GitHub accepted the review.

## Change

- Claim `DRAFT -> PUBLISHING` with a conditional update before provider work.
- Allow only the request holding that claim to continue.
- For a definite 422, annotate failed comments and release the claim to `DRAFT` in one database transaction.
- For definite prepublication errors, release the claim conditionally.
- For an ambiguous provider result or local finalization failure, retain `PUBLISHING` and return `PUBLISH_AMBIGUOUS` so a blind retry cannot duplicate a remote review.

## Acceptance and verification

Fake-provider integration tests must prove one of two concurrent requests reaches the provider, a definite 422 returns to a retryable draft with annotations, an uncertain provider error retains the gate, and provider success followed by local finalization failure also retains the gate. Run the API test command and typecheck/build checks after dependencies are available.
