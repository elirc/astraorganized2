# MobileTagalog approved plan

Successful sync previously persisted the server baseline and deleted acknowledged outbox rows in separate transactions. A crash could reload both copies and double-count progress. Overlapping requests could publish stale responses, and a response arriving after logout/account replacement could attach progress to the wrong session.

The change adds one SQLite transaction for baseline adoption plus exact-id acknowledgement and an extracted coordinator that serializes requests, preserves events appended in flight, refreshes credentials within the active session, and rejects stale-session responses. Tests use a pure coordinator fixture and an explicitly mocked SQLite adapter contract; no live Expo device database or API is claimed. Acceptance includes offline/reload reducer coverage, guest-to-account sync, exact acknowledgement, overlapping calls, and logout/account-switch invalidation, followed by tests and strict type checking.
