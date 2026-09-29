from pathlib import Path
P=Path(__file__).resolve().parent.parent/'stage/4bda479c4c50/astraupskill'
for f in P.glob('*.md'):
    t=f.read_text(encoding='utf-8-sig')
    t=t.replace('Writing anyway would change `updatedAt`, add an event, rewrite JSON bytes, and make activity feeds report work that did not alter business state.','The baseline changed `updatedAt` and rewrote JSON bytes even when it emitted no event. That mismatch could reorder a ticket list without an explanatory audit entry. The new guard preserves the existing absence of an event while also preventing the timestamp and file write.')
    t=t.replace('node --experimental-vm-modules --test astra-remaining-improvements/stage/4bda479c4c50/tests/runtime-ticket-noop.test.mjs','node --experimental-vm-modules --test tests/runtime-ticket-noop.test.mjs')
    t=t.replace('Run the focused regression from the workspace root:','Run the focused regression from this project root:')
    t=t.replace('The focused command is:', 'From this project root, the focused command is:')
    t=t.replace('Separate processes can still read the same old file and race their writes;', 'Even two requests in one process can read the same old aggregate before their writes are queued, allowing the later snapshot to overwrite the earlier edit. Separate processes add another race;')
    if f.name=='06-SOLUTIONS-AND-REVIEW.md':
        t+='\nFor the tag-order extension, order is significant in the current comparison because JSON.stringify compares arrays in order. Reversing two distinct tags records a change. Treating tags as an unordered set would require an explicit product choice, canonical ordering on both sides, and tests preserving the chosen display behavior. Do not silently add sorting as part of this no-op correction.\n'
    f.write_text(t,encoding='utf-8')
