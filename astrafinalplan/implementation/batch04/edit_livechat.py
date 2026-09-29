from pathlib import Path
import json
B=Path('astrafinalplan/implementation/batch04')
p=B/'stage/66/server/src/app.ts';s=p.read_text().replace('\n  next();\n});','');p.write_text(s)
p=B/'stage/64/test/checkout.test.ts';s=p.read_text().replace('quantity:2})).status,200','quantity:2})).status,201');p.write_text(s)
p=B/'stage/57/server/src/index.ts';s=p.read_text();s='import {pathToFileURL} from "node:url";\n'+s;s=s.replace('const app = express();','export const app = express();').replace('const server = createServer(app);','export const server = createServer(app);').replace('new WebSocketServer({ server })','new WebSocketServer({ server, maxPayload: 16384 })')
s=s.replace('  const slug = String(req.body.slug ?? "").trim().toLowerCase().replace(/[^a-z0-9-]/g, "-");\n  const name = String(req.body.name ?? "").trim();','  const slug = typeof req.body?.slug === "string" ? req.body.slug.trim().toLowerCase() : "";\n  const name = typeof req.body?.name === "string" ? req.body.name.trim() : "";').replace('if (!slug || !name)','if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug) || slug.length > 80 || !name || name.length > 100)')
s=s.replace('app.get("/api/rooms", async (_req, res) => {','app.get("/api/rooms", asyncRoute(async (_req, res) => {').replace('FROM rooms ORDER BY name"));\n});','FROM rooms ORDER BY name"));\n}));')
s=s.replace('app.post("/api/rooms", async (req, res) => {','app.post("/api/rooms", asyncRoute(async (req, res) => {').replace('    throw error;\n  }\n});','    throw error;\n  }\n}));')
s=s.replace('app.get("/api/rooms/:slug/messages", async (req, res) => {','app.get("/api/rooms/:slug/messages", asyncRoute(async (req, res) => {').replace('  res.json(history);\n});','  res.json(history);\n}));').replace('ORDER BY m.created_at DESC','ORDER BY m.created_at DESC, m.id DESC')
s=s.replace('wss.on("connection", async (socket, req) => {','wss.on("connection", (socket, req) => {\n void connectSocket(socket,req).catch(error=>{console.error(error);socket.close(1011,"Database unavailable");});\n});\nasync function connectSocket(socket:WebSocket,req:import("node:http").IncomingMessage) {')
s=s.replace('  join(room.id, socket);','  if(socket.readyState !== WebSocket.OPEN)return;\n  join(room.id, socket);').replace('    if (event.type !== "message") return;','    if (!event || typeof event !== "object" || event.type !== "message" || typeof event.author !== "string" || typeof event.body !== "string") return;\n    if(event.author.length>40 || event.body.length>2000)return;')
s=s.replace('    await query("INSERT INTO messages','    try { await query("INSERT INTO messages').replace('      body\n    ]);','      body\n    ]); } catch(error) {console.error(error);socket.close(1011,"Message could not be saved");}')
s=s.replace('  socket.on("error", () => leave(socket));\n});','  socket.on("error", () => leave(socket));\n}')
start=s.index('async function startListener()');s=s[:start]+'''let listener: ReturnType<typeof createListenerClient> | undefined;
let retry: ReturnType<typeof setTimeout> | undefined;
let stopping = false;
async function startListener() {
  const client = createListenerClient();
  listener = client;
  client.on("error", error => {
    console.error("Listener error:",error.message);
    void client.end().catch(()=>{});
    if(!stopping&&!retry)retry=setTimeout(()=>{retry=undefined;void startListener().catch(console.error);},1000);
  });
  await client.connect();
  await client.query("LISTEN chat");
  client.on("notification", msg => {
    if(!msg.payload)return;
    try {const message=JSON.parse(msg.payload) as ChatMessage;if(message.roomId)broadcast(message.roomId,{type:"message",message});}catch{ /* Ignore malformed notifications from other demos. */ }
  });
}
export async function startRuntime(listenPort=port) {
  stopping=false;
  await startListener();
  await new Promise<void>((resolve,reject)=>{server.once("error",reject);server.listen(listenPort,"127.0.0.1",()=>{server.off("error",reject);resolve();});});
  return server;
}
export async function stopRuntime() {
  stopping=true;if(retry)clearTimeout(retry);retry=undefined;
  for(const socket of wss.clients)socket.terminate();
  await new Promise<void>(resolve=>wss.close(()=>resolve()));
  await new Promise<void>(resolve=>{server.close(()=>resolve());server.closeAllConnections();});
  await listener?.end().catch(()=>{});roomClients.clear();
}
function asyncRoute(handler:(req:express.Request,res:express.Response)=>Promise<unknown>):express.RequestHandler {
 return(req,res,next)=>{Promise.resolve(handler(req,res)).catch(next);};
}
app.use((error:unknown,_req:express.Request,res:express.Response,_next:express.NextFunction)=>{console.error(error);res.status(500).json({error:"Request failed."});});
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href)startRuntime().catch(error=>{console.error(error);process.exitCode=1;});
''';p.write_text(s)
root=B/'stage/57';(root/'test').mkdir(exist_ok=True);s=(B/'stage/55/test/database.ts').read_text().replace('const { app }','const { startRuntime, stopRuntime }').replace('const server = app.listen(0,"127.0.0.1"); await new Promise<void>(resolve => server.once("listening",resolve));','const server = await startRuntime(0);').replace('await new Promise<void>(resolve => { server.close(() => resolve()); server.closeAllConnections(); });','await stopRuntime();');(root/'test/database.ts').write_text(s)
(root/'client/src/vite-env.d.ts').write_text('/// <reference types="vite/client" />\n');p=root/'package.json';d=json.loads(p.read_text());d['scripts'].update(build='vite build',test='tsx --test test/*.test.ts');p.write_text(json.dumps(d,indent=2)+'\n')
(root/'test/chat.test.ts').write_text('''import {test,before,after} from "node:test";
import assert from "node:assert/strict";
import WebSocket from "ws";
import {database,request} from "./database.js";
let h:Awaited<ReturnType<typeof database>>;
before(async()=>{h=await database();});after(async()=>{if(h)await h.close();});
test("room names reject malformed values and duplicate slugs",async()=>{for(const body of [{slug:{},name:"Room"},{slug:"bad slug",name:"Room"},{slug:"valid",name:[]}])assert.equal((await request(h.origin,"/api/rooms","POST",body)).status,400);assert.equal((await request(h.origin,"/api/rooms","POST",{slug:"study",name:"Study"})).status,201);assert.equal((await request(h.origin,"/api/rooms","POST",{slug:"study",name:"Again"})).status,409);});
test("malformed socket events do not crash; valid message persists and broadcasts",async()=>{const socket=new WebSocket(h.origin.replace("http","ws")+"/?room=study");try{await new Promise<void>((resolve,reject)=>{socket.on("message",raw=>{if(JSON.parse(String(raw)).type==="presence")resolve();});socket.on("error",reject);});const received=new Promise<any>((resolve,reject)=>{const timer=setTimeout(()=>reject(new Error("Missing broadcast")),5000);socket.on("message",raw=>{const event=JSON.parse(String(raw));if(event.type==="message"){clearTimeout(timer);resolve(event.message);}});});for(const raw of ["{", "null",JSON.stringify({type:"message",author:3,body:{}})])socket.send(raw);socket.send(JSON.stringify({type:"message",author:"Learner",body:"Trace this insert"}));const message=await received;assert.equal(message.body,"Trace this insert");const history=await request(h.origin,"/api/rooms/study/messages");assert.equal(history.data.length,1);assert.equal(history.data[0].id,message.id);}finally{socket.terminate();}});
''')
