from pathlib import Path
P=Path(__file__).resolve().parent/'stage/092c5e5b7052'
p=P/'server/index.js';s=p.read_text();s=s.replace('const clientId = decoding.readVarUint(reader); decoding.readVarUint(reader);', 'const clientId = decoding.readVarUint(reader); const clock = decoding.readVarUint(reader);')
s=s.replace("            if (room.owners.has(clientId)", "            // Standard providers relay received presence updates. Ignore stale or\n            // identical echoes before checking ownership of a genuinely new state.\n            const knownClock = room.awareness.meta.get(clientId)?.clock;\n            const knownState = room.awareness.getStates().get(clientId) ?? null;\n            if (knownClock !== undefined && (clock < knownClock || (clock === knownClock && (state !== null || knownState === null)))) continue;\n            if (room.owners.has(clientId)",1)
p.write_text(s,encoding='utf-8')
p=P/'server/test/documents.test.js';s=p.read_text().replace("await until(() => names().includes('Bob'));", "await until(() => names().includes('Bob'), 'Bob presence was not received');").replace("await until(() => !names().includes('Bob'));", "await until(() => !names().includes('Bob'), 'Bob presence remained after disconnect');")
s+=r'''
test('real rename failure leaves disk record intact and cleans temporary file', () => fixture(async ({ app, api, directory }) => {
  await api('', 'POST', { id: 'notes' }); const file = join(directory, 'notes.json'); const backup = join(directory, 'original.backup');
  const before = readFileSync(file); renameSync(file, backup); mkdirSync(file); writeFileSync(join(file, 'keep.txt'), 'keep');
  assert.equal((await api('/notes', 'PATCH', { title: 'Lost', version: 1 })).status, 500);
  assert.deepEqual(readFileSync(backup), before); assert.equal(readFileSync(join(file, 'keep.txt'), 'utf8'), 'keep');
  assert.equal(app.store.get('notes').version, 1); assert.equal(readdirSync(directory).filter(name => name.endsWith('.tmp')).length, 0);
}));
test('corrupt stored JSON stops startup without rewriting the file', () => fixture(async ({ app, api, directory }) => {
  await api('', 'POST', { id: 'notes' }); await app.close(); const file = join(directory, 'notes.json'); writeFileSync(file, '{broken');
  assert.throws(() => new DocumentStore(directory), /could not be loaded/); assert.equal(readFileSync(file, 'utf8'), '{broken');
}));
test('production entrypoint loads accepted state in a separate process', () => fixture(async ({ app, api, connect, directory }) => {
  await api('', 'POST', { id: 'notes', title: 'Restart evidence' }); const client = await connect('notes'); client.text.insert(0, 'Saved text');
  await until(() => app.store.get('notes').characters === 10); client.close(); await app.close();
  const child = spawn(process.execPath, [fileURLToPath(new URL('../index.js', import.meta.url))], { env: { ...process.env, HOST: '127.0.0.1', PORT: '0', DATA_DIR: directory }, stdio: ['ignore', 'pipe', 'pipe'], windowsHide: true });
  let output = ''; let errors = ''; let exited = false;
  const stopped = new Promise(resolveExit => child.once('exit', () => { exited = true; resolveExit(); }));
  child.stdout.on('data', data => { output += data; }); child.stderr.on('data', data => { errors += data; });
  try {
    await until(() => output.includes('listening on') || exited, 'Child server did not start'); assert.equal(exited, false, errors);
    const url = output.match(/http:\/\/127\.0\.0\.1:\d+/)[0]; const document = await (await fetch(`${url}/api/documents/notes`)).json();
    assert.equal(document.title, 'Restart evidence'); assert.equal(document.characters, 10);
  } finally { child.kill(); await stopped; }
}));
'''
p.write_text(s,encoding='utf-8')
