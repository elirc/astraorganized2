from pathlib import Path
b=Path(__file__).resolve().parent;s=b/'stage/56044dcd81ce'
files={
'apps/api/src/workers.ts':'''import { Body, ConflictException, Controller, Delete, Get, Injectable, NotFoundException, Param, Post, Put, Query, Req, Res, UseGuards } from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { Response } from 'express';
import { Database } from './db';
import { Actor, ActorRequest, AuthGuard } from './auth';
import * as input from './validation';
const include={company:{select:{id:true,name:true}}} satisfies Prisma.WorkerInclude;
@Injectable()
export class Workers {
 constructor(private readonly db:Database){}
 async list(actor:Actor,raw:unknown){
  const {page,limit,q,status}=input.query.parse(raw);
  const where:Prisma.WorkerWhereInput={tenantId:actor.tenantId,...(status?{employmentStatus:status}:{}),...(q?{OR:['firstName','lastName','email'].map(key=>({[key]:{contains:q,mode:'insensitive'}}))}:{})};
  const [total,items]=await this.db.$transaction([this.db.worker.count({where}),this.db.worker.findMany({where,include,orderBy:[{createdAt:'desc'},{id:'asc'}],skip:(page-1)*limit,take:limit})],{isolationLevel:'RepeatableRead'});
  return {items,total,page,limit};
 }
 async get(actor:Actor,id:string){const worker=await this.db.worker.findFirst({where:{id:input.id.parse(id),tenantId:actor.tenantId},include});if(!worker)throw new NotFoundException('Worker not found.');return worker;}
 async company(tx:Prisma.TransactionClient,tenantId:string,companyId:string){const found=await tx.company.findFirst({where:{id:companyId,tenantId,status:'ACTIVE'}});if(!found)throw new ConflictException('Choose an active company in this workspace.');}
 async audit(tx:Prisma.TransactionClient,actor:Actor,id:string,action:string,version:number){await tx.auditLog.create({data:{tenantId:actor.tenantId,actorUserId:actor.id,entityType:'Worker',entityId:id,action,metadata:{version}}});}
 async create(actor:Actor,body:unknown){const data=input.profile.parse(body);return this.db.$transaction(async tx=>{await this.company(tx,actor.tenantId,data.companyId);const worker=await tx.worker.create({data:{...data,tenantId:actor.tenantId},include});await this.audit(tx,actor,worker.id,'WORKER_CREATED',worker.version);return worker;});}
 async update(actor:Actor,id:string,body:unknown){input.id.parse(id);const {version,...data}=input.update.parse(body);return this.db.$transaction(async tx=>{
  const current=await tx.worker.findFirst({where:{id,tenantId:actor.tenantId}});if(!current)throw new NotFoundException('Worker not found.');
  if(current.employmentStatus==='TERMINATED')throw new ConflictException('Terminated profiles are read-only.');
  await this.company(tx,actor.tenantId,data.companyId);
  const result=await tx.worker.updateMany({where:{id,tenantId:actor.tenantId,version,employmentStatus:{not:'TERMINATED'}},data:{...data,version:{increment:1}}});
  if(result.count!==1)throw new ConflictException('Worker changed elsewhere. Reload current data before retrying; keep your draft.');
  const worker=await tx.worker.findUniqueOrThrow({where:{id},include});await this.audit(tx,actor,id,'WORKER_UPDATED',worker.version);return worker;
 });}
 async transition(actor:Actor,id:string,body:unknown){input.id.parse(id);const {version,status}=input.changeStatus.parse(body);return this.db.$transaction(async tx=>{
  const current=await tx.worker.findFirst({where:{id,tenantId:actor.tenantId}});if(!current)throw new NotFoundException('Worker not found.');
  if(current.version!==version)throw new ConflictException('Worker changed elsewhere. Reload before changing status.');
  if(!input.transitions[current.employmentStatus].includes(status))throw new ConflictException('This status transition is not allowed.');
  const changed=await tx.worker.updateMany({where:{id,tenantId:actor.tenantId,version,employmentStatus:current.employmentStatus},data:{employmentStatus:status,version:{increment:1}}});
  if(changed.count!==1)throw new ConflictException('Worker changed elsewhere. Reload before changing status.');
  const worker=await tx.worker.findUniqueOrThrow({where:{id},include});await this.audit(tx,actor,id,`WORKER_${status}`,worker.version);return worker;
 });}
 async remove(actor:Actor,id:string,body:unknown){input.id.parse(id);const {version}=input.deletion.parse(body);return this.db.$transaction(async tx=>{
  const current=await tx.worker.findFirst({where:{id,tenantId:actor.tenantId}});if(!current)throw new NotFoundException('Worker not found.');
  if(current.employmentStatus!=='DRAFT' || current.userId)throw new ConflictException('Only unlinked draft workers can be deleted.');
  const result=await tx.worker.deleteMany({where:{id,tenantId:actor.tenantId,version,employmentStatus:'DRAFT',userId:null}});
  if(result.count!==1)throw new ConflictException('Worker changed elsewhere. Reload before deleting.');
  await this.audit(tx,actor,id,'WORKER_DELETED',version);return {id,deleted:true};
 });}
 async companies(actor:Actor){return this.db.company.findMany({where:{tenantId:actor.tenantId,status:'ACTIVE'},select:{id:true,name:true},orderBy:{name:'asc'},take:100});}
 async audits(actor:Actor){return this.db.auditLog.findMany({where:{tenantId:actor.tenantId,entityType:'Worker'},orderBy:[{createdAt:'desc'},{id:'asc'}],take:30});}
}
@Controller() @UseGuards(AuthGuard)
export class WorkersController {
 constructor(private readonly workers:Workers){}
 @Get('me') me(@Req() req:ActorRequest){return req.actor;}
 @Get('companies') companies(@Req() req:ActorRequest){return this.workers.companies(req.actor);}
 @Get('audit') audits(@Req() req:ActorRequest){return this.workers.audits(req.actor);}
 @Get('workers') list(@Req() req:ActorRequest,@Query() q:unknown){return this.workers.list(req.actor,q);}
 @Get('workers/:id') get(@Req() req:ActorRequest,@Param('id') id:string){return this.workers.get(req.actor,id);}
 @Post('workers') async create(@Req() req:ActorRequest,@Body() body:unknown,@Res({passthrough:true}) res:Response){const worker=await this.workers.create(req.actor,body);res.setHeader('Location',`/api/workers/${worker.id}`);return worker;}
 @Put('workers/:id') update(@Req() req:ActorRequest,@Param('id') id:string,@Body() body:unknown){return this.workers.update(req.actor,id,body);}
 @Post('workers/:id/status') transition(@Req() req:ActorRequest,@Param('id') id:string,@Body() body:unknown){return this.workers.transition(req.actor,id,body);}
 @Delete('workers/:id') remove(@Req() req:ActorRequest,@Param('id') id:string,@Body() body:unknown){return this.workers.remove(req.actor,id,body);}
}
''',
'apps/api/src/app.module.ts':'''import { Module } from '@nestjs/common';
import { Database } from './db';
import { AuthController, AuthGuard, AuthService } from './auth';
import { Workers, WorkersController } from './workers';
@Module({controllers:[AuthController,WorkersController],providers:[Database,AuthService,AuthGuard,Workers]})
export class AppModule {}
''',
'apps/api/src/app.ts':'''import { NestFactory } from '@nestjs/core';
import { json } from 'express';
import { randomUUID } from 'node:crypto';
import { AppModule } from './app.module';
import { ApiErrors } from './errors';
export async function createApp(){
 const app=await NestFactory.create(AppModule,{bodyParser:false,logger:process.env.NODE_ENV==='test'?false:['error','warn','log']});
 app.setGlobalPrefix('api');app.use((req:any,res:any,next:()=>void)=>{req.requestId=randomUUID();res.setHeader('X-Request-Id',req.requestId);res.setHeader('Cache-Control','no-store');res.setHeader('X-Content-Type-Options','nosniff');next();});
 app.use(json({limit:'32kb',strict:true}));app.useGlobalFilters(new ApiErrors());
 app.enableCors({origin:process.env.WEB_ORIGIN??'http://127.0.0.1:5173',methods:['GET','POST','PUT','DELETE'],allowedHeaders:['Content-Type','Authorization'],exposedHeaders:['X-Request-Id','Location']});
 app.enableShutdownHooks();await app.init();return app;
}
''',
'apps/api/src/main.ts':'''import { existsSync } from 'node:fs';
import { createApp } from './app';
async function bootstrap(){
 if(existsSync('.env'))process.loadEnvFile('.env');
 const port=Number(process.env.PORT??3000);if(!Number.isInteger(port)||port<1||port>65535)throw new Error('Invalid PORT.');
 const app=await createApp();await app.listen(port,'127.0.0.1');console.log(`Operations API: http://127.0.0.1:${port}/api`);
}
bootstrap().catch(()=>{console.error('API startup failed. Check configuration and database connectivity.');process.exitCode=1;});
''',
'apps/api/prisma/seed.ts':'''import { PrismaClient, UserRole } from '@prisma/client';
import { hashPassword } from '../src/password';
const db=new PrismaClient();
async function main(){
 const password=process.env.DEMO_PASSWORD;
 if(!password || password.length<12)throw new Error('Set DEMO_PASSWORD to at least 12 characters. Seed only a disposable learning database.');
 const passwordHash=await hashPassword(password);
 await db.$transaction(async tx=>{
  for(const [slug,name,email] of [['acme-corp','Acme Corporation','client.admin@acme.example.com'],['globex','Globex Inc','client.admin@globex.example.com']]){
   const tenant=await tx.tenant.upsert({where:{slug},update:{},create:{slug,name}});
   const companyId=slug==='acme-corp'?'a1111111-1111-4111-8111-111111111111':'b1111111-1111-4111-8111-111111111111';
   const existing=await tx.company.findUnique({where:{id:companyId}});if(existing&&existing.tenantId!==tenant.id)throw new Error('Demo company identity is already owned elsewhere.');
   await tx.company.upsert({where:{id:companyId},update:{},create:{id:companyId,tenantId:tenant.id,name:`${name} Operations`,legalName:name}});
   const existingUser=await tx.user.findUnique({where:{email}});if(existingUser&&existingUser.tenantId!==tenant.id)throw new Error('Demo email is already owned elsewhere.');
   await tx.user.upsert({where:{email},update:{},create:{tenantId:tenant.id,email,passwordHash,firstName:'Demo',lastName:'Admin',role:UserRole.CLIENT_ADMIN}});
   await tx.worker.upsert({where:{tenantId_email:{tenantId:tenant.id,email:`learner@${slug}.example.com`}},update:{},create:{tenantId:tenant.id,companyId,firstName:'Sample',lastName:'Learner',email:`learner@${slug}.example.com`,countryCode:'US',jobTitle:'Junior developer',department:'Engineering'}});
  }
 });
 console.log('Demo tenants, companies, admins and draft workers are present. Existing records/passwords were preserved.');
}
main().catch(()=>{console.error('Seed failed. Check DEMO_PASSWORD, database schema and demo identity ownership.');process.exitCode=1;}).finally(()=>db.$disconnect());
'''}
for rel,content in files.items():p=s/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content,encoding='utf-8')
print('Wrote tenant-scoped worker CRUD, transitions, transactional audit and repeatable seed')
