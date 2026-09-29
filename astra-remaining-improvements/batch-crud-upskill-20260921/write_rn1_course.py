from pathlib import Path
p=Path(__file__).resolve().parent.parent/'stage/195e77d61335/astraupskill'
chapters={
'README.md':'''# Deleting a block and refreshing its read model

This lesson follows an unblock operation in the Bluesky social-app source. The remote block record is deleted through an agent, while the blocked-accounts screen reads a separate cached query. Before this change, successful blocking invalidated that query but successful unblocking only reset profile feeds. The deleted account could therefore remain in cached blocked-list data until another refresh occurred.

The correction adds one invalidation in the success callback of `useProfileUnblockMutation` in [profile.ts](../social-app/src/state/queries/profile.ts). It uses the existing query-key function from [my-blocked-accounts.ts](../social-app/src/state/queries/my-blocked-accounts.ts), preserving the same identity used by the reader. Original source and package metadata are preserved in [snapshots](snapshots).

Study this as CRUD across two representations: a server record and a client read model. Start with the code map, compare the worked change, then predict the pending and rejected traces before reading the solutions. The portable [test](../social-app/tests/crud-upskill/profile-unblock.test.mjs) executes the extracted production hook and the real blocked-query key with explicit adapters. It does not mount React or execute TanStack's cache engine. Invalidation requests a refresh; it does not prove that a network refetch succeeded or that every visible list changed immediately.
''',
'01-CODEBASE-MAP.md':'''# Follow identity through the mutation

In [profile.ts](../social-app/src/state/queries/profile.ts), `useProfileBlockMutationQueue` chooses between block and unblock mutations. For an unblock, it supplies the target DID and the existing block URI. `useProfileUnblockMutation` reads the current account and agent, parses the record key from the URI, and calls `agent.app.bsky.graph.block.delete` with the current account's repository DID and that record key.

The mutation's `onSuccess` receives the target DID separately. It now invalidates `RQKEY_MY_BLOCKED()` and retains `resetProfilePostsQueries(queryClient, did, 1000)`. These are different cache effects: one refreshes the account-level blocked list; the other resets profile feeds for the target.

[my-blocked-accounts.ts](../social-app/src/state/queries/my-blocked-accounts.ts) defines the key as `['my-blocked-accounts']`. Its infinite query loads pages with `getBlocks`, a limit of thirty and an optional cursor. The mutation imports this key rather than spelling a new cache identity.

Draw three arrows: block URI to record key, signed-in account to repository, and target DID to feed reset. Then add the account-level invalidation. Keeping those identities separate helps catch a deletion aimed at the wrong repository or an invalidation aimed at an unrelated profile. The test models URI parsing and session state; native agent and cache behavior remain outside its boundary.
''',
'02-CONCEPTS.md':'''# A successful write can leave a stale read

A server mutation and a cached query serve different purposes. Deleting the block record changes authoritative state. The query cache still contains the result of an earlier read until it is updated, invalidated and refetched, or discarded. Returning success from a mutation therefore does not automatically establish that the blocked-list view has current data.

Invalidation is a request to reconsider cached data. It is weaker than directly proving a successful refresh, but avoids inventing a second local implementation of paginated server state. This change follows the existing blocking path's invalidation convention. It does not optimistically remove an item from every page or manufacture a replacement response.

The callback belongs after successful deletion. If the remote operation rejects, the modeled lifecycle skips `onSuccess`; a failed delete must not be presented as a committed state change. However, a network failure can be ambiguous: the server might have committed before a response was lost. Handling that ambiguity requires a deliberate retry and reconciliation policy, which this small patch does not add.

Query identity also matters. The target profile DID identifies the feed to reset, whereas `RQKEY_MY_BLOCKED()` identifies the blocked list for the active session. Session-switch behavior, cancellation and account-scoped cache clearing require separate evidence. Review the real [key definition](../social-app/src/state/queries/my-blocked-accounts.ts) instead of assuming that similar function names address the same cached data.
''',
'03-WORKED-CHANGE.md':'''# Repair the missing success effect

The original unblock success callback only reset profile feeds:

```ts
onSuccess(_, {did}) {
  resetProfilePostsQueries(queryClient, did, 1000)
}
```

The revised callback uses the blocked-list key already imported by the module:

```ts
onSuccess(_, {did}) {
  void queryClient.invalidateQueries({queryKey: RQKEY_MY_BLOCKED()})
  resetProfilePostsQueries(queryClient, did, 1000)
}
```

Compare the exact [original](snapshots/profile.ts.original.txt) with [profile.ts](../social-app/src/state/queries/profile.ts). Remote deletion, the signed-out guard, URI parsing and the feed-reset delay are unchanged. The `void` convention matches the existing block callback: the mutation does not wait for a query refetch to finish before continuing its success work.

For a concrete trace, delete record `block-1` from `did:actor` while viewing `did:target`. Once deletion resolves, invalidate `['my-blocked-accounts']` and reset target feeds with delay 1000. The first operation addresses the blocked list, not a profile-specific key. If deletion rejects, neither success effect is reached in the modeled lifecycle.

A package script named `test:crud-upskill` exposes the focused harness through Yarn, following this project's command convention. No application dependencies or translation outputs were regenerated. This is a targeted read-model correction, not a redesign of the mutation queue or a guarantee about mounted user-interface timing.
''',
'04-TESTING-AND-DEBUGGING.md':'''# Control the remote completion boundary

The [test](../social-app/tests/crud-upskill/profile-unblock.test.mjs) reads the exact `useProfileUnblockMutation` section from production source, strips TypeScript types and evaluates it in a VM. Its `useMutation` adapter returns the hook options. A small runner explicitly awaits `mutationFn` and then invokes `onSuccess`; that runner models the lifecycle and does not test TanStack itself.

Four cases cover successful deletion and both cache effects, signed-out rejection before the API call, identity-preserving propagation of a remote error, and a deferred deletion whose success effects remain absent while pending. The blocked-query key comes from the actual production query module. Session, agent, URI parser, query client and feed-reset dependencies are explicit doubles.

When a case fails, inspect the call ledger in order: deletion arguments, invalidation key, then feed-reset DID and delay. A wrong record key is different from a missing cache effect. A success assertion before resolving the deferred promise would hide the ordering boundary the fourth case is designed to expose.

Run the dedicated Yarn script from `social-app`. This device has Node 22 while the application requires Node 24.15 or later; the focused harness is run with Yarn's explicit engine override. That does not validate the native application on an unsupported Node version. See [verification](VERIFICATION.md) for the captured result and command.
''',
'05-PRACTICE.md':'''# Predict, debug, and extend

First, write the remote delete arguments for a current account `did:alice`, target `did:bob`, and block URI ending in `/block-7`. Explain why the target DID is not the repository owner passed to delete. Identify which values later reach the feed reset and which identify the blocked-list query.

Second, draw a timeline with the API promise pending at time one, resolved at time two, and cache effects at time three. State how many invalidations and feed resets should exist before resolution. Repeat with rejection, preserving the original error object in your expected result.

Third, review a proposed patch that invalidates `['profile', did]` instead of `RQKEY_MY_BLOCKED()`. Use the actual blocked-query definition to explain whether that patch addresses the demonstrated stale list. Do not accept matching variable names as evidence of matching query identities.

Fourth, design a mounted integration test. Include a cached blocked-list page, successful remote deletion, the library's actual invalidation behavior, a refetch response and an assertion about rendered items. Add a failed-refetch variant and distinguish stale display from failed deletion.

Score each answer on identity tracing, operation order, negative assertions and evidence limits. Keep the design extension separate from executed checks. Solutions follow in the next chapter; try the trace before reading them so the exercise tests reasoning rather than recall.
''',
'06-SOLUTIONS-AND-REVIEW.md':'''# Answers and review criteria

The delete arguments are `{repo: 'did:alice', rkey: 'block-7'}`. Alice owns the block record; Bob is its subject. The feed reset receives Bob's DID and delay 1000. The blocked-list invalidation uses `['my-blocked-accounts']`, independently of Bob's profile identity.

While deletion is pending, the success effects have not run. After resolution, the modeled lifecycle records one invalidation and one feed reset. On rejection, it records the attempted delete and propagates the same error, with no success effects. The signed-out case rejects even earlier, before deletion. These assertions concern the explicitly modeled lifecycle; they do not establish library scheduling under a mounted component.

Invalidating `['profile', did]` alone would target a different query family. The actual reader uses the blocked-list key, so the proposed substitution would leave the demonstrated mismatch unresolved. The worked patch reuses the reader's key function and preserves the existing profile-feed reset.

Award two points each for correct repository identity, target identity, pending/rejected ordering, query-key reasoning and honest test boundaries. For the integration extension, require an actual cache engine and rendered blocked-list observation before claiming UI coverage. A failed refetch after successful deletion is a read reconciliation problem; it should not be described as a rolled-back server write. Request a separate policy for session changes or ambiguous network failures rather than pretending this one-line fix solves them.
''',
'07-TRACE-LAB.md':'''# Remote state and cached state on one timeline

Use a two-column worksheet: the remote block record and the local blocked-list cache. Begin with the block present and a cached page containing its subject. Predict each row before reading the assertions in the [test](../social-app/tests/crud-upskill/profile-unblock.test.mjs).

| Event | Remote boundary | Local effect observed by harness |
|---|---|---|
| Hook created | No request | None |
| Mutation starts | Delete called with repository and record key | None |
| Promise pending | Result unknown | No success effects |
| Promise resolves | Double reports successful delete | Invalidate blocked-list key; reset target feeds |
| Promise rejects instead | Error propagated | No success effects |
| No current account | Delete not called | No success effects |

The table deliberately stops at invalidation. It does not invent a completed refetch or an updated screen. Add those as separate rows only in a future test with a real query client and controlled read response.

Now introduce a session change while deletion is pending. Which account owns the request, and which cache does the callback address? The present tests do not answer that lifecycle question. Record the needed session fixture and cancellation policy as follow-up work. Finally, compare block and unblock success callbacks: both should express the same blocked-list refresh intent even though one creates a remote record and the other deletes it. That symmetry helps locate missing effects during code review.
''',
'VERIFICATION.md':'''# Verification scope and reproduction

The focused suite targets [profile.ts](../social-app/src/state/queries/profile.ts) and the actual blocked-query key. It executes the exact extracted unblock hook with controlled dependencies. Four runtime cases cover success, signed-out rejection, remote failure identity and delayed completion. A modeled runner calls success only after the mutation resolves; React and TanStack are not mounted.

From `social-app`, run:

```text
yarn --ignore-engines run test:crud-upskill
```

The project requires Node 24.15 or later. The device's Node 22.16 runs this dependency-free learning harness with an explicit Yarn engine override. The first attempt without that override was rejected by Yarn before tests executed. This record must not be interpreted as native application compatibility or a successful full Jest, lint, typecheck, Expo, browser or mobile run. No translation extraction or compilation was performed.

The original production file and package metadata are stored in [snapshots](snapshots). The package change only adds the dedicated script. The test uses actual query-key source, but its agent, session, URI parser, query client and feed-reset collaborators are adapters. Consequently, it proves callback arguments and ordering, not a successful server commit, query refetch, rendered removal, session-switch safety or durable retry behavior. The captured evidence appended below is authoritative for the accepted command, terminal result and numeric test count.
'''}
for name,body in chapters.items():
 (p/name).write_text(body,encoding='utf-8')
 print(name,len(body.split()))
