# Continue Pastebin after LocalOps validation

Four new source files are staged and not wired to the existing API:

- `backend/Domain/WorkspaceDocument.cs`: strict bounded model, capability/hash helpers.
- `backend/Data/WorkspaceFileStore.cs`: shared exclusive lock file, validated reads, temporary-file flush and same-directory replacement, exact migration backup bytes.
- `backend/Domain/PasteCommands.cs`: pure reads, paginated public summaries, exact content, versioned CRUD, durable creation receipts and deleted-request protection. Slug generation reserves names in current records, receipts and activity, so deleted URLs are not reused.
- `backend/Domain/LegacyMigration.cs`: supported old array conversion and bounded source reader. Keeps expired records and legacy hashes/slugs/history. Does not write the source.

All are uncompiled and untested. Original `Program.cs`, old `PasteStore`, old model DTOs, frontend, package manifest and .NET 8 target remain unchanged. Original source review is complete; historical `docs/user-stories.md` was partly truncated during reading and should not be mistaken for implemented work.

Proposed next steps:

1. Finish LocalOps gates and delivery before starting additional heavy checks. Its 52 tests passed; npm installation is still pending. Its overlapping lint was deliberately stopped, not failed by code.
2. Wire Pastebin API and migration CLI. Target installed .NET 10 SDK, bind loopback, serve built frontend from the same origin, and keep dev proxy origins explicit. Request bodies bounded around 512 KiB; unknown JSON members rejected. Keep Host/Origin checks and basic response headers. Use edit keys in headers, never URLs; use strong exact quoted If-Match versions. Public/raw reads must not write view counts.
3. Preserve legacy edit keys containing whitespace or non-ASCII through an explicit header encoding frame if supported: for example `utf8.` followed by base64url of the original UTF-8 key, decoded with strict UTF-8 at the API boundary. New generated 43-character capability tokens can travel directly. Base64 is encoding, not encryption. Legacy 6–256 character SHA-256 keys remain a documented weaker compatibility mode; key rotation is not implemented.
4. Add bounded local rate limiting, structured errors, create request identifiers and unchanged-body replay. The current create service returns the same resource identity/current version on replay, and 410 if that accepted resource is deleted or expired. A changed payload/key with the same request identifier returns 409.
5. Improve the existing React UI with an API helper, full generated edit key and downloadable receipt, exact submitted create retry, retained/exportable drafts, explicit conflict review, complete error/busy states, literal pagination/language filtering, safe raw/download flows and normal-flow status messages. Preserve the original blue/white product and existing fork/copy/download functionality.
6. Add deterministic store/clock tests, actual independent-process HTTP races and failure tests, frontend helper tests, production browser checks and reviewed screenshots. Do not claim platform-wide atomicity or hardware power-loss recovery from temporary-file replacement.
7. Add nine project-specific course chapters, preserve original source snapshots for comparison, mark existing curriculum/user stories historical, prepare a finite spec and deliver only after checks pass.

Storage references already read: Microsoft Learn File.Move, FileStream.Flush and FileShare (.NET 10 views). Keep temporary and active files in the same directory; do not introduce copy/delete fallback. The store is intentionally a bounded local JSON aggregate, not a relational or distributed database.
