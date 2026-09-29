from pathlib import Path
P=Path(__file__).resolve().parent/'stage/092c5e5b7052'
(P/'server/index.js').write_text(r'''import { createServer } from 'node:http';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import { WebSocketServer, WebSocket } from 'ws';
import * as encoding from 'lib0/encoding';
import * as decoding from 'lib0/decoding';
import * as sync from 'y-protocols/sync';
import * as awarenessProtocol from 'y-protocols/awareness';
import { DocumentStore, DocumentError, validateId } from './store.js';

const defaults = ['http://127.0.0.1:5173', 'http://localhost:5173', 'http://127.0.0.1:8080', 'http://localhost:8080'];
function json(response, status, body) {
  response.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' });
  response.end(JSON.stringify(body));
}
function body(request, allowed) {
  return new Promise((resolveBody, reject) => {
    let content = ''; let bytes = 0; let oversized = false;
    request.on('data', chunk => { bytes += chunk.length; if (bytes > 16 * 1024) oversized = true; else content += chunk; });
    request.on('error', reject);
    request.on('end', () => {
      try {
        if (oversized) throw new DocumentError(413, 'Request body is too large.');
        if (!request.headers['content-type']?.toLowerCase().startsWith('application/json')) throw new DocumentError(415, 'Use application/json.');
        let value;
        try { value = JSON.parse(content); } catch { throw new DocumentError(400, 'Malformed JSON.'); }
        if (!value || Array.isArray(value) || typeof value !== 'object' || Object.keys(value).some(key => !allowed.includes(key))) throw new DocumentError(400, 'Unexpected request fields.');
        resolveBody(value);
      } catch (error) { reject(error); }
    });
  });
}
function envelope(type, write) {
  const encoder = encoding.createEncoder(); encoding.writeVarUint(encoder, type); write(encoder); return encoding.toUint8Array(encoder);
}
function send(socket, message) { if (socket.readyState === WebSocket.OPEN) socket.send(message); }

export function createCollaborationServer({ dataDir, allowedOrigins = defaults, logger = console.error, maxStateBytes } = {}) {
  const store = new DocumentStore(dataDir ?? resolve(dirname(fileURLToPath(import.meta.url)), 'data'), { maxStateBytes });
  const rooms = new Map();
  const origins = new Set(allowedOrigins);
  const originAllowed = request => !request.headers.origin || origins.has(request.headers.origin);
  const roomFor = id => {
    let room = rooms.get(id);
    if (room) return room;
    const awareness = new awarenessProtocol.Awareness(store.require(id).doc);
    awareness.setLocalState(null);
    room = { sockets: new Set(), awareness, owners: new Map() };
    awareness.on('update', ({ added, updated, removed }) => {
      const message = envelope(1, encoder => encoding.writeVarUint8Array(encoder, awarenessProtocol.encodeAwarenessUpdate(awareness, [...added, ...updated, ...removed])));
      for (const socket of room.sockets) send(socket, message);
    });
    rooms.set(id, room);
    return room;
  };
  const server = createServer(async (request, response) => {
    if (!originAllowed(request)) { json(response, 403, { error: 'Origin is not allowed.' }); return; }
    if (request.headers.origin) {
      response.setHeader('Access-Control-Allow-Origin', request.headers.origin);
      response.setHeader('Vary', 'Origin');
    }
    response.setHeader('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS');
    response.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    if (request.method === 'OPTIONS') { response.writeHead(204); response.end(); return; }
    try {
      let pathname;
      try { pathname = decodeURIComponent(new URL(request.url, 'http://local').pathname); }
      catch { throw new DocumentError(400, 'Invalid URL.'); }
      if (pathname === '/health' && request.method === 'GET') { json(response, 200, { status: 'ok' }); return; }
      if (pathname === '/api/documents') {
        if (request.method === 'GET') { json(response, 200, { documents: store.list() }); return; }
        if (request.method === 'POST') {
          const input = await body(request, ['id', 'title']);
          const result = store.create(input.id, input.title ?? input.id);
          response.setHeader('Location', `/api/documents/${result.document.id}`);
          json(response, result.created ? 201 : 200, result.document); return;
        }
      }
      const match = pathname.match(/^\/api\/documents\/([^/]+)$/);
      if (match) {
        const id = validateId(match[1]);
        if (request.method === 'GET') { json(response, 200, store.get(id)); return; }
        if (request.method === 'PATCH') {
          const input = await body(request, ['title', 'version']);
          json(response, 200, store.rename(id, input.title, input.version)); return;
        }
        if (request.method === 'DELETE') {
          const input = await body(request, ['version']);
          store.delete(id, input.version);
          const room = rooms.get(id);
          if (room) for (const socket of room.sockets) socket.close(4004, 'Document deleted');
          response.writeHead(204); response.end(); return;
        }
      }
      json(response, 404, { error: 'Route not found.' });
    } catch (error) {
      if (!(error instanceof DocumentError)) logger('Document request failed:', error);
      json(response, error instanceof DocumentError ? error.status : 500, { error: error instanceof DocumentError ? error.message : 'Document storage is unavailable.' });
    }
  });
  server.requestTimeout = 15_000;
  const wss = new WebSocketServer({ noServer: true, maxPayload: 1024 * 1024 });
  server.on('upgrade', (request, socket, head) => {
    try {
      if (!originAllowed(request)) throw new DocumentError(403, 'Origin is not allowed.');
      const id = validateId(decodeURIComponent(new URL(request.url, 'http://local').pathname.slice(1)));
      store.require(id);
      wss.handleUpgrade(request, socket, head, connection => wss.emit('connection', connection, id));
    } catch (error) {
      const status = error instanceof DocumentError ? error.status : 400;
      socket.end(`HTTP/1.1 ${status} Rejected\r\nConnection: close\r\nContent-Length: 0\r\n\r\n`);
    }
  });
  wss.on('connection', (socket, id) => {
    const room = roomFor(id); const controlledIds = new Set(); room.sockets.add(socket);
    socket.on('error', () => {});
    socket.on('message', (data, binary) => {
      if (!binary) { socket.close(1003, 'Binary messages required'); return; }
      try {
        store.require(id);
        const decoder = decoding.createDecoder(new Uint8Array(data));
        const type = decoding.readVarUint(decoder);
        if (type === 0) {
          const subtype = decoding.readVarUint(decoder);
          const payload = decoding.readVarUint8Array(decoder);
          if (decoding.hasContent(decoder)) throw new DocumentError(400, 'Unexpected message data.');
          if (subtype === sync.messageYjsSyncStep1) {
            send(socket, envelope(0, encoder => sync.writeSyncStep2(encoder, store.require(id).doc, payload)));
          } else if (subtype === sync.messageYjsSyncStep2 || subtype === sync.messageYjsUpdate) {
            if (store.applyUpdate(id, payload)) {
              const message = envelope(0, encoder => sync.writeUpdate(encoder, payload));
              for (const peer of room.sockets) send(peer, message);
            }
          } else throw new DocumentError(400, 'Unknown sync message.');
        } else if (type === 1) {
          const update = decoding.readVarUint8Array(decoder);
          const reader = decoding.createDecoder(update);
          const count = decoding.readVarUint(reader);
          if (count > 10 || decoding.hasContent(decoder)) throw new DocumentError(400, 'Invalid presence update.');
          const ids = [];
          for (let index = 0; index < count; index++) {
            const clientId = decoding.readVarUint(reader); decoding.readVarUint(reader);
            const state = JSON.parse(decoding.readVarString(reader));
            if (state !== null && (typeof state !== 'object' || !state.user || typeof state.user.name !== 'string' || state.user.name.length > 50 || !/^#[0-9a-f]{6}$/i.test(state.user.color))) throw new DocumentError(400, 'Invalid presence profile.');
            if (room.owners.has(clientId) && room.owners.get(clientId) !== socket) throw new DocumentError(400, 'Presence ID belongs to another connection.');
            ids.push({ clientId, state });
          }
          if (decoding.hasContent(reader)) throw new DocumentError(400, 'Unexpected presence data.');
          for (const { clientId, state } of ids) {
            if (state === null) { controlledIds.delete(clientId); room.owners.delete(clientId); }
            else { controlledIds.add(clientId); room.owners.set(clientId, socket); }
          }
          awarenessProtocol.applyAwarenessUpdate(room.awareness, update, socket);
        } else if (type === 3) {
          send(socket, envelope(1, encoder => encoding.writeVarUint8Array(encoder, awarenessProtocol.encodeAwarenessUpdate(room.awareness, [...room.awareness.getStates().keys()]))));
        } else throw new DocumentError(400, 'Unknown message type.');
      } catch (error) {
        if (!(error instanceof DocumentError)) logger('Collaboration update failed:', error);
        socket.close(error instanceof DocumentError ? 1008 : 1011, error instanceof DocumentError ? 'Invalid or unavailable document' : 'Document persistence failed');
      }
    });
    socket.on('close', () => {
      room.sockets.delete(socket);
      for (const clientId of controlledIds) if (room.owners.get(clientId) === socket) room.owners.delete(clientId);
      awarenessProtocol.removeAwarenessStates(room.awareness, [...controlledIds], socket);
      if (room.sockets.size === 0) { room.awareness.destroy(); rooms.delete(id); }
    });
    send(socket, envelope(0, encoder => sync.writeSyncStep1(encoder, store.require(id).doc)));
    if (room.awareness.getStates().size) send(socket, envelope(1, encoder => encoding.writeVarUint8Array(encoder, awarenessProtocol.encodeAwarenessUpdate(room.awareness, [...room.awareness.getStates().keys()]))));
  });
  return {
    server, store,
    listen(port = 1234, host = '127.0.0.1') { return new Promise((resolveListen, reject) => { server.once('error', reject); server.listen(port, host, () => { server.off('error', reject); resolveListen(server.address()); }); }); },
    async close() {
      for (const socket of wss.clients) socket.terminate();
      await new Promise(resolveClose => wss.close(resolveClose));
      for (const room of rooms.values()) room.awareness.destroy(); rooms.clear();
      if (server.listening) await new Promise(resolveClose => server.close(resolveClose));
      store.destroy();
    },
  };
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const port = Number(process.env.PORT ?? 1234);
  if (!Number.isInteger(port) || port < 0 || port > 65535) throw new Error('PORT must be an integer from 0 to 65535.');
  const app = createCollaborationServer({ dataDir: process.env.DATA_DIR, allowedOrigins: process.env.ALLOWED_ORIGINS?.split(',').map(value => value.trim()) });
  const address = await app.listen(port, process.env.HOST ?? '127.0.0.1');
  console.log(`Collaborative editor listening on http://${address.address}:${address.port}`);
  for (const signal of ['SIGINT', 'SIGTERM']) process.once(signal, () => { app.close().catch(console.error); });
}
''',encoding='utf-8')
