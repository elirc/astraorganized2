# Missioncontrol Astra review

Decision: CHANGES REQUIRED pending frozen implementation and authentic checks.

Confirmed original create path already validates workspace-filtered projects; update did not. Blank-title validation and filtered reassignment are useful. Reassignment now allocates target-project ticket numbers, but allocation must be protected against concurrent creation/moves in both workflows.

Current manual SqliteConnection.BeginTransaction plus EF UseTransaction has lifecycle defects: EF wrapper is nonowning, underlying rollback/disposal can be missed, and explicit OpenConnection reference counts accumulate. Requested EF-owned BeginTransactionAsync(Serializable), verified nondeferred provider semantics in official Microsoft.Data.Sqlite source. Required regressions include repeated successful calls in one scoped context, rejected mutation followed by valid write without leaking tracked changes, and concurrent creates/moves allocating unique target ticket numbers.

Additional checks: rejected foreign-workspace/missing target must preserve task, project counters and activities; same-project/omitted-project must not allocate; events publish only after commit. Root owns real Release build/test evidence; earlier interrupted test process is not final evidence.

Course must reflect final transaction ownership and actual tests, preserve exact noncompiled originals, and match all practice prompts to complete worked answers. Initial short course is not yet final-approved. No canonical writes by reviewer.
