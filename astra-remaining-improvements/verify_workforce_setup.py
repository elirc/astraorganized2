from pathlib import Path
import subprocess,os,json
b=Path(__file__).resolve().parent;s=b/'stage/56044dcd81ce';c=b/'checks/workforce/setup';c.mkdir(parents=True,exist_ok=True);e=os.environ.copy();e['DATABASE_URL']='postgresql://learning@127.0.0.1:1/unused';
for label,args,cwd in [('prisma-validate',['node',str(s/'node_modules/prisma/build/index.js'),'validate'],s/'apps/api'),('prisma-generate',['node',str(s/'node_modules/prisma/build/index.js'),'generate'],s/'apps/api'),('migration-diff',['node',str(s/'node_modules/prisma/build/index.js'),'migrate','diff','--from-empty','--to-schema-datamodel','prisma/schema.prisma','--script'],s/'apps/api')]:
 r=subprocess.run(args,cwd=cwd,env=e,capture_output=True,text=True,encoding='utf-8',timeout=180);(c/(label+'.log')).write_text(r.stdout+r.stderr,encoding='utf-8');print(label,r.returncode,flush=True)
 if r.returncode:print((r.stdout+r.stderr)[-7000:]);raise SystemExit(1)
 if label=='migration-diff':
  p=s/'apps/api/prisma/migrations/202609090001_worker_directory';p.mkdir(parents=True,exist_ok=True)
  checks='''\nALTER TABLE "Worker" ADD CONSTRAINT "Worker_profile_bounds" CHECK (version > 0 AND length(trim("firstName")) BETWEEN 1 AND 80 AND length(trim("lastName")) BETWEEN 1 AND 80 AND length(email) BETWEEN 3 AND 254 AND email = lower(email) AND "countryCode" ~ '^[A-Z]{2}$' AND ("jobTitle" IS NULL OR length("jobTitle") <= 120) AND (department IS NULL OR length(department) <= 100));\n'''
  (p/'migration.sql').write_text(r.stdout+checks,encoding='utf-8');(p.parent/'migration_lock.toml').write_text('provider = "postgresql"\n',encoding='utf-8')
for label,args,cwd in [('api-typecheck',['npm.cmd','run','typecheck'],s/'apps/api'),('web-build',['npm.cmd','run','build'],s/'apps/web')]:
 r=subprocess.run(args,cwd=cwd,env=e,capture_output=True,text=True,encoding='utf-8',timeout=180);(c/(label+'.log')).write_text(r.stdout+r.stderr,encoding='utf-8');print(label,r.returncode,flush=True)
 if r.returncode:print((r.stdout+r.stderr)[-7000:])
