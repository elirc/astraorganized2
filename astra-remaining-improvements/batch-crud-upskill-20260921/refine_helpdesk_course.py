from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent
D=B/'stage/707cb3abbb7a/astraupskill'
changes={
'README.md':[
('Agent A reads title `Old` at `updatedAt=19:00`. Agent B changes the title and commits at `20:00`. Agent A then sends its stale form.', 'Request A has already entered the server action and read title `Old` at `updatedAt=19:00`. Request B changes the ticket and commits at `20:00` before A reaches its update statement. A then attempts its write using the timestamp its server action read.'),
('this prevents the stale update path from silently winning, while leaving transaction isolation and every other ticket mutation outside this small change.', 'this detects a changed timestamp between this action\'s server read and write. An old browser form submitted after another edit is not detected if this action reads the newer timestamp before writing. Same-timestamp writes, transaction isolation and other ticket mutations remain outside this bounded guarantee.')],
'01-CODEBASE-MAP.md':[
('organization and capability checks | `access.ts`', 'organization record checks | `access.ts`'),
('“is this row still the one I edited?”', '“does this row still have the timestamp this server request read?”')],
'02-CONCEPTS.md':[
('If two forms are open, the later request can overwrite the earlier request regardless of which form was newer.', 'If two server actions overlap between reading and writing, an unconditional update can overwrite a change that occurred after its read.'),
('what exact value was read, what exact predicate was written, and which side effects happen only after a successful update?', 'what exact value did this server request read, what exact predicate was written, and which side effects happen only after a successful update?'),
('The authorization check remains necessary', 'A stale browser form is not protected across its whole editing session because the form does not submit its originally observed version. Two writes sharing the same timestamp can also evade this check; a dedicated increasing version would give a different contract. The authorization check remains necessary')],
'03-WORKED-CHANGE.md':[
('if (error?.code === "P2025") {', 'if (error && typeof error === "object" && "code" in error && error.code === "P2025") {')],
'04-TESTING-AND-DEBUGGING.md':[
('two important branches of the real action execute with deterministic repository contracts.', 'four focused cases of the real action execute with deterministic repository contracts: stale rejection, accepted update, inaccessible ticket and unrelated persistence failure. Domain transition and SLA helpers are substituted, so their rules are not validated here.')],
'05-PRACTICE.md':[
('Sketch a review comment for a future contributor who wants to replace the post-write `findFirst` with the object returned by `update`.', 'Sketch a review comment for a future contributor who wants to replace the current object returned by `update` with a separate post-write `findFirst` query.'),
('Use the rubric: 1 point for an exact predicate, 1 for each correctly ordered side effect, 2 for a reproducible integration scenario, and 1 for a limitation grounded in a named code path.', 'Award the stated exercise points for exact predicates, correctly ordered effects, reproducible integration steps and limitations grounded in named code paths. The six exercises total twenty points.')],
'06-SOLUTIONS-AND-REVIEW.md':[
('read it into request A, update it through request B so its timestamp changes, then submit A.', 'pause request A immediately after its server-side `findFirst`, update the ticket through request B so its timestamp changes, then resume A at its conditional update.'),
('The patch catches two editors submitting the same ticket version: only the first matching `update` can return one.', 'The patch rejects request A when another writer changes the timestamp after A\'s server-side read and before its update. It does not protect a browser form whose stale values arrive before the action reads a newer timestamp, or writes that retain an identical timestamp.'),
('The current update DTO is the committed result, so a replacement must preserve its fields and avoid observing a later writer.', 'The current update DTO is the committed result. A separate reread could observe another writer\'s fields or a deletion, so retaining the update result keeps audit and notification decisions tied to this accepted mutation.')],
'07-TRACE-LAB.md':[
('both paths revalidate | no redirect', 'detail and list paths revalidate | no redirect'),
('For each trace, write the exact first side effect. In the stale path it is the thrown `ActionError`; in the accepted path it is the normal audit event after the post-write read.', 'For each trace, distinguish mutation, error outcome and follow-up side effects. In the stale path the conditional update matches no row and the action throws `ActionError`; audit and notifications are not reached. In the accepted path the update succeeds first, then the audit uses the returned row. There is no post-write read.')]
}
for name,pairs in changes.items():
    p=D/name;t=p.read_text(encoding='utf-8')
    for old,new in pairs:
        assert old in t,(name,old)
        t=t.replace(old,new)
    p.write_text(t,encoding='utf-8')
p=B/'specs/707cb3abbb7a.json';s=json.loads(p.read_text())
s['limits'].append('Domain capability, transition, normalization and SLA helpers are substituted; status-change notification fan-out is not exercised. Timestamp collisions and edits before the server read are not detected by this guard.')
p.write_text(json.dumps(s,indent=2),encoding='utf-8')
print('Corrected server-read concurrency scope and obsolete reread references in eight chapters.')
