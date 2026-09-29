from pathlib import Path
b=Path(__file__).resolve().parent;s=b/'stage/56044dcd81ce'
files={
'apps/api/src/db.ts':'''import { Injectable, OnModuleDestroy, OnModuleInit } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';
@Injectable()
export class Database extends PrismaClient implements OnModuleInit, OnModuleDestroy {
  async onModuleInit() { await this.$connect(); }
  async onModuleDestroy() { await this.$disconnect(); }
}
''',
'apps/api/src/password.ts':'''import { randomBytes, scrypt, timingSafeEqual } from 'node:crypto';
import { promisify } from 'node:util';
const derive = promisify(scrypt);
export async function hashPassword(password: string) {
  const salt = randomBytes(16).toString('hex');
  const key = await derive(password, salt, 64) as Buffer;
  return `scrypt:${salt}:${key.toString('hex')}`;
}
export async function verifyPassword(password: string, encoded: string) {
  const parts = encoded.split(':');
  if (parts.length !== 3 || parts[0] !== 'scrypt' || !/^[a-f0-9]{32}$/.test(parts[1]) || !/^[a-f0-9]{128}$/.test(parts[2])) return false;
  const key = await derive(password, parts[1], 64) as Buffer;
  return timingSafeEqual(key, Buffer.from(parts[2], 'hex'));
}
''',
'apps/api/src/auth.ts':'''import { Body, CanActivate, Controller, ExecutionContext, ForbiddenException, HttpCode, HttpException, Injectable, Post, Req, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { Request } from 'express';
import { z } from 'zod';
import { Database } from './db';
import { hashPassword, verifyPassword } from './password';
export type Actor = { id: string; tenantId: string; email: string; role: string; tenantName: string };
export type ActorRequest = Request & { actor: Actor };
const credentials = z.object({ email:z.string().trim().email().max(254).transform(v=>v.toLowerCase()), password:z.string().min(1).max(200) }).strict();
@Injectable()
export class AuthService {
  private readonly jwt = new JwtService();
  private readonly secret: string;
  private readonly attempts = new Map<string, { count:number; until:number }>();
  private readonly dummy = hashPassword('unmatched-account-timing-placeholder');
  constructor(private readonly db: Database) {
    this.secret = process.env.JWT_SECRET ?? '';
    if (this.secret.length < 32 || this.secret.startsWith('replace-')) throw new Error('Set JWT_SECRET to at least 32 random characters.');
  }
  private limit(key: string) {
    const now=Date.now();
    for (const [id,item] of this.attempts) if(item.until<=now)this.attempts.delete(id);
    if(!this.attempts.has(key) && this.attempts.size>=10000)throw new HttpException('Sign-in temporarily busy.',429);
    const item=this.attempts.get(key)??{count:0,until:now+60000};
    item.count++;this.attempts.set(key,item);
    if(item.count>20)throw new HttpException('Too many sign-in attempts. Try again in one minute.',429);
  }
  async login(body: unknown, address: string) {
    this.limit(address);
    const input=credentials.parse(body);
    const user=await this.db.user.findUnique({where:{email:input.email},include:{tenant:true}});
    const valid=await verifyPassword(input.password,user?.passwordHash??await this.dummy);
    if(!valid || !user || user.status!=='ACTIVE')throw new UnauthorizedException('Email or password is incorrect.');
    if(!user.tenant || user.tenant.status!=='ACTIVE' || !['INTERNAL_OPS','CLIENT_ADMIN','CLIENT_HR'].includes(user.role))throw new ForbiddenException('This account has no active operations workspace.');
    const actor={id:user.id,tenantId:user.tenant.id,email:user.email,role:user.role,tenantName:user.tenant.name};
    return {token:await this.jwt.signAsync({sub:user.id},{secret:this.secret,algorithm:'HS256',expiresIn:'30m',issuer:'globalworkforce-local',audience:'operations-ui'}),actor};
  }
  async authenticate(header: string|undefined): Promise<Actor> {
    const match=header?.match(/^Bearer ([A-Za-z0-9_.-]+)$/);if(!match || match[1].length>4096)throw new UnauthorizedException('Sign in to continue.');
    let claims:{sub?:unknown};
    try{claims=await this.jwt.verifyAsync(match[1],{secret:this.secret,algorithms:['HS256'],issuer:'globalworkforce-local',audience:'operations-ui'});}catch{throw new UnauthorizedException('Session expired or invalid. Sign in again.');}
    if(typeof claims.sub!=='string')throw new UnauthorizedException();
    const user=await this.db.user.findUnique({where:{id:claims.sub},include:{tenant:true}});
    if(!user || user.status!=='ACTIVE' || !user.tenant || user.tenant.status!=='ACTIVE')throw new UnauthorizedException('Account or workspace is inactive.');
    if(!['INTERNAL_OPS','CLIENT_ADMIN','CLIENT_HR'].includes(user.role))throw new ForbiddenException('Operations role required.');
    return {id:user.id,tenantId:user.tenant.id,email:user.email,role:user.role,tenantName:user.tenant.name};
  }
}
@Injectable()
export class AuthGuard implements CanActivate {
  constructor(private readonly auth:AuthService){}
  async canActivate(context:ExecutionContext){const request=context.switchToHttp().getRequest<ActorRequest>();request.actor=await this.auth.authenticate(request.headers.authorization);return true;}
}
@Controller('auth')
export class AuthController {
  constructor(private readonly auth:AuthService){}
  @Post('login') @HttpCode(200)
  login(@Body() body:unknown,@Req() req:Request){return this.auth.login(body,req.socket.remoteAddress??'unknown');}
}
''',
'apps/api/src/errors.ts':'''import { ArgumentsHost, Catch, ExceptionFilter, HttpException } from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { ZodError } from 'zod';
import { Response, Request } from 'express';
@Catch()
export class ApiErrors implements ExceptionFilter {
 catch(error:unknown,host:ArgumentsHost){
  const response=host.switchToHttp().getResponse<Response>();const request=host.switchToHttp().getRequest<Request & {requestId:string}>();
  let status=500,message='The operation failed. No success was confirmed.';
  if(error instanceof ZodError){status=400;message=error.issues.map(i=>`${i.path.join('.')||'request'}: ${i.message}`).join('; ');}
  else if(error instanceof HttpException){status=error.getStatus();const value=error.getResponse();message=typeof value==='string'?value:(value as {message?:string}).message??error.message;}
  else if(error instanceof Prisma.PrismaClientKnownRequestError){
   if(error.code==='P2002'){status=409;message='A worker with this email already exists in this workspace.';}
   else if(error.code==='P2003'){status=409;message='Related records prevent this operation.';}
   else if(error.code==='P2025'){status=404;message='Record not found.';}
  }
  if(status===500)console.error(JSON.stringify({requestId:request.requestId,error:'unhandled-api-error'}));
  response.status(status).json({error:message,requestId:request.requestId});
 }
}
''',
'apps/api/src/validation.ts':'''import { z } from 'zod';
export const id = z.string().uuid();
const text=(max:number)=>z.string().trim().min(1).max(max);
export const profile=z.object({firstName:text(80),lastName:text(80),email:z.string().trim().email().max(254).transform(v=>v.toLowerCase()),companyId:id,countryCode:z.string().regex(/^[A-Z]{2}$/,'Use a two-letter uppercase country code.'),jobTitle:z.string().trim().max(120),department:z.string().trim().max(100)}).strict();
export const version=z.number().int().min(1).max(2147483646);
export const update=profile.extend({version}).strict();
export const changeStatus=z.object({version,status:z.enum(['DRAFT','ONBOARDING','ACTIVE','PAUSED','TERMINATED'])}).strict();
export const deletion=z.object({version}).strict();
const pageNumber=(max:number,fallback:number)=>z.string().regex(/^[1-9][0-9]*$/).transform(Number).pipe(z.number().int().max(max)).optional().default(String(fallback));
export const query=z.object({page:pageNumber(10000,1),limit:pageNumber(50,20),q:z.string().trim().max(100).optional().default(''),status:z.enum(['DRAFT','ONBOARDING','ACTIVE','PAUSED','TERMINATED']).optional()}).strict();
export const transitions:Record<string,readonly string[]>={DRAFT:['ONBOARDING'],ONBOARDING:['ACTIVE','TERMINATED'],ACTIVE:['PAUSED','TERMINATED'],PAUSED:['ACTIVE','TERMINATED'],TERMINATED:[]};
'''}
for rel,content in files.items():p=s/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content,encoding='utf-8')
print('Wrote database, authentication, validation and error boundaries')
