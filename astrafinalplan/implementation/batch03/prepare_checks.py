from pathlib import Path
import json
B=Path('astrafinalplan/implementation/batch03');kinds=json.loads((B/'kinds.json').read_text(encoding='utf-8'));ts=[x['stage'] for x in kinds if x['typescript']]
s=(B.parent/'batch02/run_checks.py').read_text(encoding='utf-8');a=s.index('tasks=[]');b=s.index('select=set(',a)
s=s[:a]+'''tasks=[]
TS=TS_LIST
for n in range(21,51):
 cwd=B/'stage'/str(n)
 pattern='*.test.ts' if str(n) in TS else '*.test.cjs' if n in [21,22] else '*.test.js'
 files=list((cwd/'test').glob(pattern))
 if files:
  cmd=['node',str(H/'node_modules/tsx/dist/cli.mjs'),'--test',*map(str,files)] if str(n) in TS else ['node','--test',*map(str,files)]
  tasks.append((str(n),'tests',cwd,cmd))
 if n>=23:tasks.append((str(n),'build',cwd,['node',str(H/'node_modules/vite/bin/vite.js'),'build']))
 if str(n) in TS:tasks.append((str(n),'typecheck',cwd,['node',str(H/'node_modules/typescript/bin/tsc'),'--noEmit']))
'''.replace('TS_LIST',repr(ts))+s[b:];(B/'run_checks.py').write_text(s,encoding='utf-8')
helper='''import pg from "pg";
import { readFile } from "node:fs/promises";
import { randomUUID } from "node:crypto";

export async function database() {
  const supplied = process.env.ASTRA_TEST_DATABASE_URL;
  if (!supplied) throw new Error("Set ASTRA_TEST_DATABASE_URL to a dedicated astra_test_* database.");
  const url = new URL(supplied);
  if (!url.pathname.slice(1).startsWith("astra_test_")) throw new Error("Refusing a non-test database.");
  const schema = "astra_" + randomUUID().replaceAll("-", "");
  const admin = new pg.Client({ connectionString: supplied }); await admin.connect();
  await admin.query(`CREATE SCHEMA "${schema}"`);
  try {
    await admin.query(`SET search_path TO "${schema}", public`);
    // Each schema is fresh. Remove destructive reset statements from the teaching setup script.
    const sql = (await readFile(new URL("../server/db/schema.sql", import.meta.url), "utf8"))
      .replace(/^DROP (?:TABLE|MATERIALIZED VIEW|VIEW|INDEX|FUNCTION|TRIGGER)[^;]*;/gm, "")
      .replace(/^CREATE EXTENSION[^;]*;/gm, "");
    await admin.query(sql);
    url.searchParams.set("options", "-c search_path=" + schema + ",public");
    process.env.DATABASE_URL = url.href;
    const { app } = await import("../server/src/index.js");
    const { pool } = await import("../server/src/db.js");
    const server = app.listen(0,"127.0.0.1"); await new Promise<void>(resolve => server.once("listening",resolve));
    const origin = "http://127.0.0.1:" + (server.address() as any).port;
    return { admin, pool, schema, origin, async close() {
      await new Promise<void>(resolve => { server.close(() => resolve()); server.closeAllConnections(); });
      await pool.end(); await admin.query(`DROP SCHEMA "${schema}" CASCADE`); await admin.end();
    }};
  } catch (error) { await admin.query(`DROP SCHEMA "${schema}" CASCADE`); await admin.end(); throw error; }
}
export async function request(origin: string, path: string, method = "GET", body?: unknown) {
  const response = await fetch(origin + path, { method, headers: body === undefined ? {} : { "Content-Type": "application/json" }, body: body === undefined ? undefined : JSON.stringify(body) });
  const data = response.status === 204 ? null : await response.json();
  return { status: response.status, data };
}
'''
for n in ts:
 p=B/'stage'/n/'test';p.mkdir(exist_ok=True);(p/'database.ts').write_text(helper,encoding='utf-8')
print('Prepared test runner and disposable-schema HTTP helpers.')
