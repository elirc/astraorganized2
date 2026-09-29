from pathlib import Path
P=Path(__file__).resolve().parent.parent/'stage/5528ac452b91/astraupskill'
replacements={
 'service?s':"service's",'repository?s':"repository's",'schema?s':"schema's",'project?s':"project's",
 'evidence/astra-crud-b06-ww28.log':'evidence/crud-b06-astra-runtime.log',
 'evidence/results-crud-b06.json':'evidence/results.json',
 'Four cases':'Five cases','from the staged project':'from the project directory',
 'repository, storage, auth, and decoding doubles':'repository and storage adapters plus real auth, decoding, and error modules',
 'It stubs only the auth guard, base64 decoder, and HTTP error classes; repository and storage dependencies are supplied through the constructor.':'It loads the real auth guard, permission rules, base64 decoder and HTTP error classes; repository and storage dependencies are supplied through the constructor.',
 'with no repository or storage calls':'with no chunk lookup, metadata write or storage calls (session and file repository reads still occur)',
 'zero side effects on invalid input':'zero chunk mutations on invalid range input',
 'counts chunks, assembles them, verifies total size':'counts chunks, checks contiguous part numbers, sums recorded sizes',
 'count, assembly, size, quota':'count, contiguity, recorded size, quota',
 'Then add a fifth fixture with an existing chunk to exercise the retry branch.':'The fifth fixture retries part 2, checks its existing id is retained, and observes delete, write, then upsert.',
 'The VM lab proves pre-write rejection and one valid write path':'The VM lab proves pre-write rejection, a new part write and an upper-bound retry',
 'A follow-up should cover valid retry replacement, missing middle parts':'A follow-up should cover durable retry replacement, missing middle parts',
 'while an in-range part writes through the service and upserts metadata.':'while part 1 writes metadata and a part 2 retry retains its chunk id after delete/write/upsert.',
 'and valid part 1 reaches the production': 'valid part 2 retries with its existing id, and valid part 1 reaches the production',
 'The staged production fix changes':'The production fix changes',
 'complete inclusive range check':'two-sided inclusive bound check',
 }
for p in P.glob('*.md'):
 t=p.read_text()
 for a,b in replacements.items():t=t.replace(a,b)
 if p.name=='VERIFICATION.md':
  t+='\nThe guard assumes an integer supplied by request validation: it does not by itself reject fractional numbers or NaN. Retry replacement deletes the old chunk before writing new storage, so a write failure can leave the prior metadata without its blob. This patch does not make storage replacement atomic.\n'
 if p.name=='07-TRACE-LAB.md': t=t.replace('| part 1, expected 2', '| part 2 retry, expected 2 | accept | delete then write | upsert existing id | retriedPart true |\n| part 1, expected 2').replace('| none | none | validation error |','| none | session/file reads only | validation error |')
 p.write_text(t,encoding='utf-8')
