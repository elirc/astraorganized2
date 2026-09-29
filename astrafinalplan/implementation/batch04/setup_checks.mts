import pg from 'pg';
import {randomUUID} from 'node:crypto';
import {spawn} from 'node:child_process';
import {writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const B=path.dirname(fileURLToPath(import.meta.url));
const connection='postgres://astra:local-test@127.0.0.1:55439/astra_test_ten';
const admin=new pg.Client({connectionString:connection});await admin.connect();
const results=[];
try {for(let n=58;n<=71;n++){
 if(process.argv.length>2&&!process.argv.slice(2).includes(String(n)))continue;
 const schema='astra_'+randomUUID().replaceAll('-','');
 await admin.query(`CREATE SCHEMA "${schema}"`);
 const url=new URL(connection);url.searchParams.set('options','-c search_path='+schema+',public');
 const env={...process.env,DATABASE_URL:url.href,NODE_ENV:'test'};
 try {for(const action of ['migrate','seed']){
  const result=await new Promise<{exit_code:number|null,output:string}>(resolve=>{
   const child=spawn(process.execPath,[path.join(B,'../node_modules/tsx/dist/cli.mjs'),'scripts/database.ts',action],{cwd:path.join(B,'stage',String(n),'server'),env,windowsHide:true});let output='';
   child.stdout.on('data',b=>output+=b);child.stderr.on('data',b=>output+=b);child.on('close',exit_code=>resolve({exit_code,output}));
  });
  await writeFile(path.join(B,'logs',`${n}-setup-${action}.log`),result.output);
  results.push({project:String(n),check:'setup-'+action,exit_code:result.exit_code,log:`logs/${n}-setup-${action}.log`});
  console.log(JSON.stringify(results.at(-1)));
  if(result.exit_code)break;
 }}finally{await admin.query(`DROP SCHEMA "${schema}" CASCADE`);}
}}finally{await admin.end();await writeFile(path.join(B,process.argv.length>2?'setup-retry.json':'setup-checks.json'),JSON.stringify(results,null,2));}
process.exitCode=results.some(r=>r.exit_code)?1:0;
