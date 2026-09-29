from pathlib import Path
s=Path('astra-remaining-improvements/stage/993e7c3b44d7')
def put(name,text):
 p=s/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
put('src/lib/http.js','''import {createHash,timingSafeEqual,randomUUID} from 'node:crypto';
import {InputError} from './puzzles/validation.js';
export function requireAuthor(request){const configured=process.env.GLOBS_AUTHOR_TOKEN;if(!configured||configured.length<32||/change|replace|example|placeholder/i.test(configured))throw new InputError('Puzzle authoring is not configured. Set a generated author token on the server.',503);const supplied=request.headers.get('authorization')??'';if(supplied.length>512||!supplied.startsWith('Bearer '))throw new InputError('Author token required.',401);const hash=value=>createHash('sha256').update(value).digest();if(!timingSafeEqual(hash(supplied.slice(7)),hash(configured)))throw new InputError('Author token is invalid.',401);const origin=request.headers.get('origin');if(origin&&origin!==new URL(request.url).origin)throw new InputError('Cross-origin authoring is not allowed.',403);}
export async function readJson(request){if(!(request.headers.get('content-type')??'').toLowerCase().startsWith('application/json'))throw new InputError('Use application/json.',415);if(Number(request.headers.get('content-length'))>32768)throw new InputError('Request exceeds 32 KiB.',413);if(!request.body)throw new InputError('JSON body is required.');const reader=request.body.getReader();let bytes=0;const chunks=[];try{while(true){const {value,done}=await reader.read();if(done)break;bytes+=value.byteLength;if(bytes>32768){await reader.cancel();throw new InputError('Request exceeds 32 KiB.',413);}chunks.push(value);}}finally{reader.releaseLock();}try{return JSON.parse(Buffer.concat(chunks).toString('utf8'));}catch{throw new InputError('Body is not valid JSON.');}}
export function respond(body,status=200,headers={}){return Response.json(body,{status,headers:{'Cache-Control':'no-store',...headers}});}
export async function handle(request,work,{author=true}={}){const requestId=randomUUID();try{if(author)requireAuthor(request);const response=await work();response.headers.set('X-Request-Id',requestId);return response;}catch(error){const status=error instanceof InputError?error.status:error.code==='P2002'?409:error.code==='P2003'?409:503;const message=error instanceof InputError?error.message:error.code==='P2002'?'A puzzle already occupies this locale, size and date.':error.code==='P2003'?'Related records prevent this operation.':'The puzzle store is unavailable. Try again after checking the local database.';if(status>=500)console.error(JSON.stringify({event:'puzzle_request_failed',requestId,status}));return respond({error:message,requestId},status,{'X-Request-Id':requestId});}}
''')
put('src/app/api/studio/puzzles/route.js','''import {prisma} from '@/lib/prisma';
import {handle,readJson,respond} from '@/lib/http';
import {createPuzzle,listPuzzles} from '@/lib/puzzles/authoring';
import {listFilters} from '@/lib/puzzles/validation';
export const dynamic='force-dynamic';
export async function GET(request){return handle(request,async()=>respond(await listPuzzles(prisma,listFilters(new URL(request.url).searchParams))));}
export async function POST(request){return handle(request,async()=>{const result=await createPuzzle(prisma,await readJson(request));return respond(result,201,{Location:'/api/studio/puzzles/'+result.id});});}
''')
put('src/app/api/studio/puzzles/[id]/route.js','''import {prisma} from '@/lib/prisma';
import {handle,readJson,respond} from '@/lib/http';
import {deletePuzzle,getPuzzle,updatePuzzle} from '@/lib/puzzles/authoring';
import {object} from '@/lib/puzzles/validation';
export const dynamic='force-dynamic';
export async function GET(request,context){return handle(request,async()=>respond(await getPuzzle(prisma,(await context.params).id)));}
export async function PUT(request,context){return handle(request,async()=>{const input=object(await readJson(request),['version','draft']);return respond(await updatePuzzle(prisma,(await context.params).id,input.version,input.draft));});}
export async function DELETE(request,context){return handle(request,async()=>{const input=object(await readJson(request),['version']);return respond(await deletePuzzle(prisma,(await context.params).id,input.version));});}
''')
put('src/app/api/studio/puzzles/[id]/publication/route.js','''import {prisma} from '@/lib/prisma';
import {handle,readJson,respond} from '@/lib/http';
import {publishPuzzle} from '@/lib/puzzles/authoring';
import {object} from '@/lib/puzzles/validation';
export const dynamic='force-dynamic';
export async function PUT(request,context){return handle(request,async()=>{const input=object(await readJson(request),['version','published']);return respond(await publishPuzzle(prisma,(await context.params).id,input.version,input.published));});}
''')
put('src/lib/puzzles/resolveDailyPuzzle.js','''import {buildPuzzlePayload} from './payload.js';
import {SAMPLE_PUZZLES} from './samplePuzzles.js';
import {dailyFilters} from './validation.js';
import {prisma} from '../prisma.js';
export async function resolveDailyPuzzle(filters={},db=prisma,{demo=process.env.GLOBS_DEMO_MODE==='true'}={}){
 const params=new URLSearchParams();for(const [key,value]of Object.entries(filters)){if(value!==undefined)params.set(key,value);}const {locale,size,date}=dailyFilters(params);
 if(demo){const sample=SAMPLE_PUZZLES.find(p=>p.locale===locale&&p.size.toLowerCase()===size);return sample?{...buildPuzzlePayload({...sample,id:`demo-${date}-${locale}-${size}`,date}),source:'demo'}:null;}
 const start=new Date(date+'T00:00:00.000Z'),end=new Date(start.getTime()+86400000);
 const puzzle=await db.puzzle.findFirst({where:{locale,size:size.toUpperCase(),type:'DAILY',isPublished:true,date:{gte:start,lt:end}},include:{groups:true},orderBy:{id:'asc'}});
 return puzzle?{...buildPuzzlePayload(puzzle),source:'database'}:null;
}
''')
put('src/app/api/puzzles/daily/route.js','''import {resolveDailyPuzzle} from '@/lib/puzzles/resolveDailyPuzzle';
import {dailyFilters} from '@/lib/puzzles/validation';
import {handle,respond} from '@/lib/http';
export const dynamic='force-dynamic';
export async function GET(request){return handle(request,async()=>{const puzzle=await resolveDailyPuzzle(dailyFilters(new URL(request.url).searchParams));return puzzle?respond(puzzle):respond({error:'No published puzzle matches these filters.'},404);},{author:false});}
''')
put('src/app/page.js','''import Link from 'next/link';
import GameClient from '@/components/globs/GameClient';
import {resolveDailyPuzzle} from '@/lib/puzzles/resolveDailyPuzzle';
import {dailyFilters,InputError} from '@/lib/puzzles/validation';
export const dynamic='force-dynamic';
export default async function Home({searchParams}){const values=await searchParams;const params=new URLSearchParams();for(const [key,value]of Object.entries(values??{})){for(const item of Array.isArray(value)?value:[value])params.append(key,item);}let puzzle,error;try{puzzle=await resolveDailyPuzzle(dailyFilters(params));}catch(e){error=e instanceof InputError?e.message:'The puzzle database is unavailable. Check your local setup and retry.';}
return <main className="mx-auto flex min-h-screen w-full max-w-7xl flex-col gap-5 px-4 py-6 sm:px-6 lg:px-10"><nav className="flex gap-5"><Link href="/">Play</Link><Link href="/studio">Puzzle studio</Link></nav>{error?<section role="alert"><h1 className="text-2xl">Puzzle could not load</h1><p>{error}</p><Link href="/">Retry today</Link></section>:!puzzle?<section><h1 className="text-2xl">No puzzle available</h1><p>Publish a puzzle for this date in the studio, or explicitly enable the sample mode described in the README.</p></section>:<><p className="rounded-xl border border-slate-300 bg-white p-3">{puzzle.source==='demo'?'Demo sample — this is practice content, not a published daily puzzle.':'Published daily puzzle'}</p><GameClient key={puzzle.puzzleId} puzzle={puzzle}/></>}</main>;}
''')
p=s/'src/lib/prisma.js';t=p.read_text(encoding='utf-8').replace('log: process.env.NODE_ENV === "development" ? ["query", "warn", "error"] : ["error"],','log: [],');p.write_text(t,encoding='utf-8')
p=s/'src/lib/puzzles/payload.js';t=p.read_text(encoding='utf-8').replace('return Math.abs(seed) / 2_147_483_647;','return (seed >>> 0) / 4_294_967_296;');t=t.replace('export function buildPuzzlePayload(puzzle) {','''export function buildPuzzlePayload(puzzle) {
  validateGraph(puzzle);
''');t+='''
export function validateGraph(puzzle){
 if(!puzzle||!Array.isArray(puzzle.groups)||!puzzle.groups.length||puzzle.groups.length>85)throw new Error('Invalid puzzle group count.');
 const groups=new Map();let leaves=0;
 for(const group of puzzle.groups){if(typeof group.id!=='string'||!group.id||groups.has(group.id)||!Number.isInteger(group.level)||group.level<0||group.level>3||!Array.isArray(group.members)||typeof group.themeLabel!=='string'||!group.themeLabel.trim()||group.themeLabel.length>80)throw new Error('Invalid puzzle group.');groups.set(group.id,group);if(group.level===0){if(group.members.length<2||group.members.length>16||group.members.some(m=>typeof m!=='string'||!m.trim()||m.length>60))throw new Error('Invalid puzzle members.');leaves+=group.members.length;}}
 if(leaves<2||leaves>256)throw new Error('Invalid puzzle leaf count.');
 const roots=puzzle.groups.filter(g=>!g.parentGroupId);if(roots.length!==1)throw new Error('A puzzle needs one root.');
 for(const group of puzzle.groups){if(group.parentGroupId){const parent=groups.get(group.parentGroupId);if(!parent||parent.level!==group.level+1)throw new Error('Invalid puzzle hierarchy.');}if(group.level>0&&puzzle.groups.filter(child=>child.parentGroupId===group.id).length<2)throw new Error('Parent groups need at least two children.');}
}
''';p.write_text(t,encoding='utf-8')
put('.env.example','''# Use a fresh local learning database. Never point test helpers at personal data.
DATABASE_URL="postgresql://postgres:postgres@127.0.0.1:5432/globgame?schema=public"
# Generate: node -e "console.log(require('node:crypto').randomBytes(32).toString('hex'))"
GLOBS_AUTHOR_TOKEN=""
# Explicit practice mode: no database read and a visibly labeled sample puzzle.
GLOBS_DEMO_MODE="false"
''')
print('Added bounded authenticated authoring routes, explicit demo behavior and graph validation')
