from pathlib import Path
B=Path('astrafinalplan/implementation/batch04')
for n in range(67,72):
 p=B/'stage'/str(n)/'server/src/models/model.ts';s=p.read_text().replace('`${action} ${before?.title || "record"}`, updates','`${action} ${before.title}`, {status:record.status, archived_at:record.archived_at, deleted_at:record.deleted_at}');p.write_text(s)
 p=B/'stage'/str(n)/'test/crud.test.ts';s=p.read_text().replace('await api(`/${a.id}/archive`,"PATCH",{});','assert.equal((await api(`/${a.id}/archive`,"PATCH",{})).status,200);').replace('await api(`/${a.id}`,"DELETE");','assert.equal((await api(`/${a.id}`,"DELETE")).status,200);');p.write_text(s)
