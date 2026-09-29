# Aral approved plan

The SQLite event log uses first-write-wins `INSERT OR IGNORE`, while the live Zustand store and shared replay path previously counted repeated ids. The change deduplicates in arrival/storage order before timestamp sorting, serializes local/remote writes, reloads the authoritative DAO rows after success or partial failure, and tests exact retries plus conflicting payloads. The conflict rule is first-write-wins for a single local persisted log; this does not claim convergence for arbitrary UUID collisions across devices.

Acceptance is one XP/completion transition before and after reload, stable handling of a conflicting retry whose timestamp sorts earlier, and passing workspace tests and strict type checking. Store tests use a stateful Map fixture for the DAO's first-write-wins contract; they do not exercise the device SQLite adapter. No external services or original databases are used.
