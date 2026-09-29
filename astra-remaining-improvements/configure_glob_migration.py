from pathlib import Path
import subprocess,json
b=Path(__file__).resolve().parent;s=b/'stage/993e7c3b44d7';out=b/'checks/glob/setup';out.mkdir(parents=True,exist_ok=True);env=__import__('os').environ.copy();env['DATABASE_URL']='postgresql://unused:unused@127.0.0.1:1/unused'
for name,args in [('schema',['validate']),('migration',['migrate','diff','--from-empty','--to-schema-datamodel','prisma/schema.prisma','--script'])]:
 r=subprocess.run(['node','node_modules/prisma/build/index.js',*args],cwd=s,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',errors='replace');(out/(name+'.log')).write_text(r.stdout+r.stderr,encoding='utf-8');print(name,r.returncode,flush=True)
 if r.returncode:print(r.stderr[-2500:],flush=True);raise SystemExit(r.returncode)
 if name=='migration':
  target=s/'prisma/migrations/202609090001_puzzle_studio';target.mkdir(parents=True,exist_ok=True);sql=r.stdout+'\nALTER TABLE "Puzzle" ADD CONSTRAINT "Puzzle_version_positive" CHECK ("version" > 0);\nALTER TABLE "PuzzleAudit" ADD CONSTRAINT "PuzzleAudit_version_positive" CHECK ("version" > 0);\n';(target/'migration.sql').write_text(sql,encoding='utf-8');(target.parent/'migration_lock.toml').write_text('provider = "postgresql"\n',encoding='utf-8')
