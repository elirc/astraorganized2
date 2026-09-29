const {Client}=require('pg');
const fs=require('node:fs/promises');
const path=require('node:path');
const {pathToFileURL}=require('node:url');
const {spawn}=require('node:child_process');
const {randomUUID}=require('node:crypto');
const B=__dirname,H=path.dirname(B),cwd=path.join(B,'stage','20','server');
const configFile=path.join(cwd,'setup20-temp.mjs');
const connection={host:'127.0.0.1',port:55439,database:'astra_test_ten',user:'astra',password:'local-test'};
const schema='astra_setup_'+randomUUID().replaceAll('-','');
const client=new Client(connection);
const start=Date.now();let output='';let exitCode=1;
async function command(args){
 return new Promise((resolve,reject)=>{
  const child=spawn(process.execPath,args,{cwd,windowsHide:true,env:{...process.env,NO_COLOR:'1'}});
  child.stdout.on('data',b=>{output+=b;});child.stderr.on('data',b=>{output+=b;});
  child.on('error',reject);child.on('exit',code=>code===0?resolve():reject(new Error('CLI exited '+code)));
 });
}
(async()=>{
 try{
  await client.connect();await client.query(`CREATE SCHEMA "${schema}"`);
  const original=pathToFileURL(path.join(cwd,'knexfile.ts')).href;
  await fs.writeFile(configFile,`import config from ${JSON.stringify(original)};\nexport default {development:{...config.development,connection:${JSON.stringify({...connection,options:'-c search_path='+schema+',public'})},migrations:{...config.development.migrations,schemaName:${JSON.stringify(schema)}}}};\n`);
  const loader=pathToFileURL(path.join(H,'node_modules/tsx/dist/loader.mjs')).href;
  const base=['--import',loader,path.join(H,'node_modules/knex/bin/cli.js'),'--knexfile',configFile,'--cwd',cwd,'--env','development'];
  await command([...base,'migrate:latest']);
  await command([...base,'seed:run']);
  const migrations=await client.query(`SELECT count(*)::int AS count FROM "${schema}".knex_migrations`);
  if(migrations.rows[0].count!==1)throw new Error('Expected exactly one migration');
  const rows=await client.query(`SELECT count(*)::int AS count FROM "${schema}".bookmarks`);
  output+='Verified exactly one TypeScript migration; seeded bookmark count: '+rows.rows[0].count+'\n';
  exitCode=0;
 }catch(error){output+=error.stack+'\n';}
 finally{
  try{await client.query(`DROP SCHEMA IF EXISTS "${schema}" CASCADE`);}catch(error){output+=error.message+'\n';exitCode=1;}
  await client.end();await fs.unlink(configFile).catch(()=>{});
  await fs.writeFile(path.join(B,'logs/20-migration-setup.log'),output);
  const file=path.join(B,'checks.json'),checks=JSON.parse(await fs.readFile(file,'utf8'));
  const result={project:'20',check:'migration-setup',exit_code:exitCode,seconds:(Date.now()-start)/1000,log:'logs/20-migration-setup.log',command:'Knex CLI with tsx loader: migrate:latest and seed:run; disposable schema, original migration/seed configuration'};
  await fs.writeFile(file,JSON.stringify([...checks.filter(x=>!(x.project==='20'&&x.check==='migration-setup')),result],null,2));
  console.log(JSON.stringify(result));if(exitCode)console.log(output);process.exitCode=exitCode;
 }
})();
