# Astra early review: BuildAsana

Read domain/service/API/test changes. Unsupported new action guard and direct MoveToStatus value validation implemented. Add tests rejecting defined-but-unimplemented actions and proving skipped legacy action has no execution audit. Direct plan tags materialized before any scalar mutation; actual repository holds live entities, so important safeguard.

Release build01 passed. Test01:8passed/1failed HTTP readiness; child dotnet run --no-restore builds Debug while suite usesRelease. Launch builtRelease API DLL or --configuration Release --no-build --no-launch-profile, drain stdout/stderr, bound readiness and expose early exit output. No duplicate current tests.

Docs review:06 must use DomainTaskStatus alias, remove undefined validRequest, complete exercises5?7 and wrap test snippets or label method-body excerpts. 03 normalizedTags is domain source. Don't promise removing service enum guard necessarily makes HTTP test fail because domain guard remains. VERIFICATION commands need portable project-relative dotnet/npm commands, not shared runner path/doubled backend cwd. Actual current suite9 vs claimed10 must reconcile final. Root applies only after terminal checks.
