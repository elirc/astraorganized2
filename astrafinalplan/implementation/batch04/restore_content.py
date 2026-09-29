from pathlib import Path
import hashlib,json,shutil
B=Path('astrafinalplan/implementation/batch04');D=Path('C:/Users/Owner/Desktop');base=json.loads((B/'baseline.json').read_text());seen={(x['stage'],x['file']) for x in base}
for sub in ['src/content']:
 source=D/'devdeck'/sub
 for p in source.rglob('*'):
  if not p.is_file() or p.suffix not in ('.ts','.tsx','.json','.md'):continue
  rel=p.relative_to(D/'devdeck').as_posix();dest=B/'stage/74'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
  if ('74',rel) not in seen:base.append({'project':'devdeck','stage':'74','file':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(B/'baseline.json').write_text(json.dumps(base,indent=2)+'\n');print('Restored bundled DevDeck content; baseline',len(base))
