from pathlib import Path
import re
P=Path(__file__).resolve().parent.parent/'stage/612cdbaa5aa0/astraupskill'
for f in P.glob('*.md'):
    t=f.read_text(encoding='utf-8-sig')
    for word in ['card','row','test','seed','root','Node','Drizzle']:t=t.replace(word+'?s',word+"'s")
    t=t.replace('?one card per user and problem.?','"one card per user and problem."').replace('?create attempt then card?','"create attempt then card"')
    t=t.replace('?is this row id unique??','"is this row id unique?"').replace('?is this user already associated with this problem??','"is this user already associated with this problem?"').replace('?unique means idempotent,?','"unique means idempotent,"')
    t=t.replace(' at line 98','')
    t=t.replace('removes the index, inserts duplicate rows','omits the index from its initial DDL, inserts duplicate rows').replace('removes the index, creates legacy duplicates','omits the index from its initial DDL, creates legacy duplicates')
    t=t.replace('The second insert passes primary-key validation because c2 is new, passes foreign keys because u1 and p1 exist, then fails the composite unique index because the pair is occupied.','The second insert has an unused row id and valid user/problem references, but violates the composite unique index because the pair is occupied. These are logical constraint checks, not a claim about SQLite’s internal evaluation order.')
    t=t.replace('raises before commit','rejects the statement')
    t=t.replace('the six-test evidence attached by root','the captured six-test evidence').replace('The final six-case result is recorded by root.','The captured final run passed all six cases.').replace('the six passing cases are attached by root','the six passing cases have captured evidence')
    t=re.sub(r'\n(?:[ \t]*\n)+','\n\n',t)
    lines=t.splitlines();out=[];inside=False
    for line in lines:
        if line.startswith('```'):inside=not inside
        if inside and not line.strip():continue
        if line.startswith('|') and out and not out[-1] and len(out)>1 and out[-2].startswith('|'):out.pop()
        out.append(line)
    t='\n'.join(out)+'\n'
    if f.name=='06-SOLUTIONS-AND-REVIEW.md':
        t+='\nThe application declares user_id and problem_id NOT NULL, so SQLite’s allowance for multiple NULL values in unique indexes does not bypass this pair constraint. Also distinguish statement failure from an atomic migration: the seed executes several DDL statements without a surrounding transaction. Earlier table creation can remain even when later index creation fails. The preservation test checks card rows, not rollback of the entire schema initialization.\n'
    if f.name=='VERIFICATION.md':
        t=t.replace('this chapter records that result without reproducing an unverified command or claiming a broader suite.','the command below reproduces the bounded check from this project root.')
        t+='\nRun the captured suite from this project root:\n\n```text\nnode --test tests/user-card-constraint.test.mjs\n```\n\nThe initial harness failure came from matching LF text against Windows CRLF bytes. The revised extractor accepts SQL whitespace while still requiring the exact index name and column pair. The successful second run uses the same production DDL; no user database was touched during either run.\n'
    f.write_text(t,encoding='utf-8')
