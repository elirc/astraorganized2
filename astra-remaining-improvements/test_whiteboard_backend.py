from pathlib import Path
P=Path(__file__).resolve().parent/'stage/092c5e5b7052'
p=P/'server/index.js';s=p.read_text().replace("    let content = ''; let bytes = 0; let oversized = false;", "    const chunks = []; let bytes = 0; let oversized = false;").replace("else content += chunk;", "else chunks.push(chunk);").replace('value = JSON.parse(content);', "value = JSON.parse(Buffer.concat(chunks).toString('utf8'));")
s=s.replace("      try {\n        store.require(id);", "      let acceptingUpdate = false;\n      try {\n        store.require(id);")
s=s.replace("            if (store.applyUpdate(id, payload)) {", "            acceptingUpdate = true;\n            if (store.applyUpdate(id, payload)) {")
s=s.replace("        if (!(error instanceof DocumentError)) logger('Collaboration update failed:', error);\n        socket.close(error instanceof DocumentError ? 1008 : 1011, error instanceof DocumentError ? 'Invalid or unavailable document' : 'Document persistence failed');", "        const storageFailure = acceptingUpdate && !(error instanceof DocumentError);\n        if (storageFailure) logger('Collaboration update failed:', error);\n        socket.close(storageFailure ? 1011 : 1008, storageFailure ? 'Document persistence failed' : 'Invalid or unavailable document');")
p.write_text(s,encoding='utf-8')
p=P/'client/src/App.tsx';s=p.read_text().replace('        await refreshDocuments();','        void refreshDocuments().catch(() => { if (active) setError(\'Document opened, but the document list could not refresh.\'); });',1);p.write_text(s,encoding='utf-8')
p=P/'server/test/documents.test.js';p.parent.mkdir(parents=True,exist_ok=True)
p.write_text(r'''import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync, readFileSync, writeFileSync, mkdirSync, renameSync, readdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve, relative, isAbsolute } from 'node:path';
import { setTimeout as delay } from 'node:timers/promises';
import { request as httpRequest } from 'node:http';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import * as Y from 'yjs';
import { WebsocketProvider } from 'y-websocket';
import { WebSocket } from 'ws';
import { createCollaborationServer } from '../index.js';
import { DocumentStore } from '../store.js';

async function until(predicate, message = 'Condition did not become true') {
  const deadline = Date.now() + 5000;
  while (!predicate()) { if (Date.now() > deadline) throw new Error(message); await delay(15); }
}
async function fixture(run, options = {}) {
  const directory = mkdtempSync(join(tmpdir(), 'whiteboard-test-'));
  const apps = []; const clients = [];
  const start = async () => {
    const app = createCollaborationServer({ dataDir: directory, logger: () => {}, ...options });
    const address = await app.listen(0); apps.push(app);
    const base = `http://127.0.0.1:${address.port}`;
    const api = async (path = '', method = 'GET', input) => fetch(`${base}/api/documents${path}`, { method, headers: input === undefined ? undefined : { 'Content-Type': 'application/json' }, body: input === undefined ? undefined : JSON.stringify(input) });
    const connect = async (id, name = 'Editor') => {
      const doc = new Y.Doc();
      const provider = new WebsocketProvider(base.replace('http', 'ws'), id, doc, { WebSocketPolyfill: WebSocket, disableBc: true, connect: false });
      const client = { doc, provider, text: doc.getText('markdown-content'), closed: false, close() { if (!this.closed) { this.closed = true; provider.destroy(); doc.destroy(); } } };
      clients.push(client); provider.awareness.setLocalStateField('user', { name, color: '#76d7c4' }); provider.connect();
      await until(() => provider.synced, `Client did not sync to ${id}`); return client;
    };
    return { app, base, api, connect };
  };
  try { await run({ ...(await start()), start, directory }); }
  finally {
    for (const client of clients) client.close();
    for (const app of apps.reverse()) await app.close();
    const inside = relative(resolve(tmpdir()), resolve(directory));
    assert.ok(inside && !inside.startsWith('..') && !isAbsolute(inside) && inside.startsWith('whiteboard-test-'));
    rmSync(directory, { recursive: true, force: true });
  }
}

test('create returns a readable Location and repeated join preserves title', () => fixture(async ({ api, base }) => {
  const created = await api('', 'POST', { id: 'notes', title: 'Team notes' }); assert.equal(created.status, 201);
  const document = await created.json(); assert.equal(document.version, 1);
  assert.equal((await fetch(base + created.headers.get('location'))).status, 200);
  const repeated = await api('', 'POST', { id: 'notes', title: 'Ignored rename' }); assert.equal(repeated.status, 200); assert.equal((await repeated.json()).title, 'Team notes');
  assert.equal((await (await api()).json()).documents.length, 1);
}));
test('validation rejects traversal blank titles malformed JSON and unexpected fields', () => fixture(async ({ api, base }) => {
  for (const input of [{ id: '../escape' }, { id: 'notes', title: ' ' }, { id: 'notes', extra: true }]) assert.equal((await api('', 'POST', input)).status, 400);
  const malformed = await fetch(`${base}/api/documents`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{' }); assert.equal(malformed.status, 400);
  assert.equal((await (await api()).json()).documents.length, 0);
}));
test('metadata request size and origin rules are enforced', () => fixture(async ({ base }) => {
  assert.equal((await fetch(`${base}/api/documents`, { method: 'POST', body: '{}' })).status, 415);
  assert.equal((await fetch(`${base}/api/documents`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id: 'notes', title: 'x'.repeat(20_000) }) })).status, 413);
  assert.equal((await fetch(`${base}/health`, { headers: { Origin: 'https://unrelated.example' } })).status, 403);
  assert.equal((await fetch(`${base}/health`)).status, 200);
}));
test('UTF-8 titles survive request chunks split inside a character', () => fixture(async ({ base }) => {
  const bytes = Buffer.from(JSON.stringify({ id: 'unicode', title: 'Café notes' })); const split = bytes.indexOf(Buffer.from('é')) + 1;
  const result = await new Promise((resolveResult, reject) => {
    const request = httpRequest(`${base}/api/documents`, { method: 'POST', headers: { 'Content-Type': 'application/json' } }, response => {
      let text = ''; response.on('data', chunk => { text += chunk; }); response.on('end', () => resolveResult({ status: response.statusCode, body: JSON.parse(text) }));
    }); request.on('error', reject); request.write(bytes.subarray(0, split)); request.end(bytes.subarray(split));
  }); assert.equal(result.status, 201); assert.equal(result.body.title, 'Café notes');
}));
test('competing metadata updates have one winner and stale delete conflicts', () => fixture(async ({ api }) => {
  await api('', 'POST', { id: 'notes' });
  const responses = await Promise.all(['First', 'Second'].map(title => api('/notes', 'PATCH', { title, version: 1 })));
  assert.deepEqual(responses.map(response => response.status).sort(), [200, 409]);
  assert.equal((await api('/notes', 'DELETE', { version: 1 })).status, 409);
  assert.equal((await (await api('/notes')).json()).version, 2);
}));
test('deletion persists a tombstone and its ID cannot be recreated', () => fixture(async ({ api, directory }) => {
  await api('', 'POST', { id: 'notes' }); assert.equal((await api('/notes', 'DELETE', { version: 1 })).status, 204);
  assert.equal((await api('/notes')).status, 404); assert.equal((await api('', 'POST', { id: 'notes' })).status, 409);
  assert.equal((await (await api()).json()).documents.length, 0);
  const reopened = new DocumentStore(directory); try { assert.throws(() => reopened.create('notes'), error => error.status === 409); } finally { reopened.destroy(); }
}));
test('failed metadata write preserves version title and saved bytes', () => fixture(async ({ app, api, directory }) => {
  await api('', 'POST', { id: 'notes' }); const before = readFileSync(join(directory, 'notes.json'));
  app.store.persist = () => { throw new Error('injected write failure'); };
  assert.equal((await api('/notes', 'PATCH', { title: 'Lost', version: 1 })).status, 500);
  assert.equal(app.store.get('notes').version, 1); assert.equal(app.store.get('notes').title, 'notes'); assert.deepEqual(readFileSync(join(directory, 'notes.json')), before);
}));
test('two real WebSocket clients sync bidirectionally and isolate another room', () => fixture(async ({ api, connect }) => {
  await api('', 'POST', { id: 'notes' }); await api('', 'POST', { id: 'separate' });
  const a = await connect('notes', 'Alice'); const b = await connect('notes', 'Bob'); const separate = await connect('separate');
  a.text.insert(0, 'Hello'); await until(() => b.text.toString() === 'Hello');
  b.text.insert(5, ' world'); await until(() => a.text.toString() === 'Hello world'); assert.equal(separate.text.toString(), '');
}));
test('simultaneous Yjs inserts converge without losing either edit', () => fixture(async ({ api, connect }) => {
  await api('', 'POST', { id: 'notes' }); const a = await connect('notes'); const b = await connect('notes');
  a.text.insert(0, 'A'); b.text.insert(0, 'B');
  await until(() => a.text.length === 2 && a.text.toString() === b.text.toString()); assert.deepEqual([...a.text.toString()].sort(), ['A', 'B']);
}));
test('accepted collaborative state survives server recreation', () => fixture(async ({ app, api, connect, start }) => {
  await api('', 'POST', { id: 'notes' }); const a = await connect('notes'); a.text.insert(0, 'Persist me');
  await until(() => app.store.require('notes').doc.getText('markdown-content').toString() === 'Persist me'); a.close(); await app.close();
  const restarted = await start(); const b = await restarted.connect('notes'); assert.equal(b.text.toString(), 'Persist me');
}));
test('presence is removed after a client disconnects', () => fixture(async ({ api, connect }) => {
  await api('', 'POST', { id: 'notes' }); const a = await connect('notes', 'Alice'); const b = await connect('notes', 'Bob');
  const names = () => [...a.provider.awareness.getStates().values()].map(state => state.user?.name);
  await until(() => names().includes('Bob')); b.close(); await until(() => !names().includes('Bob')); assert.ok(names().includes('Alice'));
}));
test('deleting an active room closes clients and refuses their reconnection', () => fixture(async ({ api, connect, base }) => {
  await api('', 'POST', { id: 'notes' }); const a = await connect('notes');
  const closed = new Promise(resolveClose => a.provider.on('connection-close', event => { if (event?.code === 4004) resolveClose(event.code); }));
  assert.equal((await api('/notes', 'DELETE', { version: 1 })).status, 204); assert.equal(await closed, 4004); a.close();
  const status = await new Promise(resolveStatus => { const socket = new WebSocket(base.replace('http', 'ws') + '/notes'); socket.on('unexpected-response', (_request, response) => { resolveStatus(response.statusCode); response.resume(); socket.terminate(); }); socket.on('error', () => {}); }); assert.equal(status, 404);
}));
test('failed persistence prevents update broadcast and live server mutation', () => fixture(async ({ app, api, connect, directory }) => {
  await api('', 'POST', { id: 'notes' }); const a = await connect('notes'); const b = await connect('notes'); const before = readFileSync(join(directory, 'notes.json'));
  app.store.persist = () => { throw new Error('injected persistence failure'); };
  const closed = new Promise(resolveClose => a.provider.on('connection-close', event => { if (event) resolveClose(event.code); }));
  a.text.insert(0, 'Unsaved'); assert.equal(await closed, 1011); a.close(); await delay(50);
  assert.equal(b.text.toString(), ''); assert.equal(app.store.require('notes').doc.getText('markdown-content').toString(), ''); assert.deepEqual(readFileSync(join(directory, 'notes.json')), before);
}));
test('oversized and invalid Yjs updates preserve stored state', () => fixture(async ({ app, api }) => {
  await api('', 'POST', { id: 'notes' }); const candidate = new Y.Doc();
  try { candidate.getText('markdown-content').insert(0, 'x'.repeat(1000)); assert.throws(() => app.store.applyUpdate('notes', Y.encodeStateAsUpdate(candidate)), error => error.status === 413); }
  finally { candidate.destroy(); }
  assert.throws(() => app.store.applyUpdate('notes', new Uint8Array([255])), error => error.status === 400); assert.equal(app.store.get('notes').characters, 0);
}), { maxStateBytes: 100 });
''',encoding='utf-8')
# Correct the options argument placement in the final fixture call.
s=p.read_text().replace("}), { maxStateBytes: 100 });", "}, { maxStateBytes: 100 }));")
p.write_text(s,encoding='utf-8')
