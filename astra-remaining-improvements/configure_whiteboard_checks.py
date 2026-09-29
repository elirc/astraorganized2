from pathlib import Path
import json
B=Path(__file__).resolve().parent;P=B/'stage/092c5e5b7052'
p=P/'client/src/App.tsx';s=p.read_text().replace("        provider.on('status',", "        let deleted = false;\n        provider.on('status',",1).replace("if (active) setStatus(connection ===", "if (active && !deleted) setStatus(connection ===",1).replace("if (active && synced) setStatus('Live')", "if (active && !deleted && synced) setStatus('Live')",1).replace("            provider.disconnect(); setStatus('Deleted');", "            deleted = true; provider.disconnect(); setStatus('Deleted');",1)
s=s.replace("  const editable = status === 'Live' && !busy;", "  const editable = status === 'Live' && !busy;\n  const changingRoom = busy || status === 'Connecting' || status === 'Synchronizing';")
s=s.replace("disabled={busy} className={`document-item", "disabled={changingRoom} className={`document-item")
s=s.replace('value={roomInput} disabled={busy}', 'value={roomInput} disabled={changingRoom}').replace('className="primary-action" disabled={busy}', 'className="primary-action" disabled={changingRoom}')
s=s.replace('disabled={!current || busy}', 'disabled={!current || !editable}')
s=s.replace('if (sessionRef.current === target && window.confirm', 'if (sessionRef.current === target && target.provider.synced && target.provider.wsconnected && window.confirm')
p.write_text(s,encoding='utf-8')
p=P/'package.json';data=json.loads(p.read_text());data['scripts']['install:all']='npm ci --prefix client && npm ci --prefix server && npm ci';data['scripts']['test:server']='npm test --prefix server';data['scripts']['verify']='npm run test:server && npm run lint && npm run build && npm run test:e2e';p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
p=P/'server/package.json';data=json.loads(p.read_text());data['scripts']['test']='node --test test/*.test.js';p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
(P/'playwright.config.ts').write_text(r'''import { defineConfig, devices } from '@playwright/test';
import { resolve } from 'node:path';

const apiPort = Number(process.env.WHITEBOARD_API_PORT || 24123);
const clientPort = Number(process.env.WHITEBOARD_CLIENT_PORT || 25173);
const baseURL = `http://127.0.0.1:${clientPort}`;
const apiURL = `http://127.0.0.1:${apiPort}`;
export default defineConfig({
  testDir: './tests', timeout: 30_000, expect: { timeout: 8_000 },
  fullyParallel: false, workers: 1,
  reporter: [['list'], ['html', { open: 'never' }]],
  use: { baseURL, trace: 'retain-on-failure', screenshot: 'only-on-failure' },
  webServer: [
    {
      command: 'npm run dev:server', url: `${apiURL}/health`, reuseExistingServer: false, timeout: 30_000,
      env: { HOST: '127.0.0.1', PORT: String(apiPort), DATA_DIR: process.env.WHITEBOARD_E2E_DATA_DIR || resolve('.test-data'), ALLOWED_ORIGINS: baseURL },
    },
    {
      command: `npm run dev:client -- --port ${clientPort} --strictPort`, url: baseURL, reuseExistingServer: false, timeout: 45_000,
      env: { VITE_SYNC_URL: apiURL.replace('http', 'ws') },
    },
  ],
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
});
''',encoding='utf-8')
p=P/'tests/collaboration.spec.ts';s=p.read_text();s+=r'''

test('renames with an explicit version and preserves another tab after deletion cancellation', async ({ page }) => {
  const room = `metadata-${Date.now()}`;
  await page.goto('/'); await joinRoom(page, room);
  await page.getByLabel('Document title').fill('Review notes');
  await page.getByRole('button', { name: 'Save title', exact: true }).click();
  await expect(page.getByRole('status')).toContainText('Title saved');
  await page.reload(); await expect(page.getByTestId('connection-status')).toHaveText('Live');
  await expect(page.getByLabel('Document title')).toHaveValue('Review notes');
  page.once('dialog', dialog => dialog.dismiss());
  await page.getByRole('button', { name: 'Delete document' }).click();
  await expect(page.getByTestId('connection-status')).toHaveText('Live');
  await expect(page.getByLabel('Document title')).toHaveValue('Review notes');
});

test('confirmed deletion closes another tab and prevents the old ID from returning', async ({ browser }) => {
  const context = await browser.newContext(); const a = await context.newPage(); const b = await context.newPage();
  try {
    const room = `delete-${Date.now()}`;
    await a.goto('/'); await b.goto('/'); await joinRoom(a, room); await joinRoom(b, room);
    await a.getByTestId('markdown-editor').fill('Keep until confirmed');
    await expect(b.getByTestId('markdown-editor')).toHaveValue('Keep until confirmed');
    a.once('dialog', dialog => dialog.accept());
    await a.getByRole('button', { name: 'Delete document' }).click();
    await expect(a.getByTestId('connection-status')).toHaveText('Deleted');
    await expect(b.getByTestId('connection-status')).toHaveText('Deleted');
    await b.getByLabel('Room name').fill(room); await b.getByRole('button', { name: 'Join', exact: true }).click();
    await expect(b.getByRole('alert')).toContainText('was deleted');
    await expect(b.getByTestId('markdown-editor')).toBeDisabled();
  } finally { await context.close(); }
});

test('switches rooms without copying old content and treats replacement dollars literally', async ({ page }) => {
  await page.goto('/'); await joinRoom(page, `switch-a-${Date.now()}`);
  await page.getByTestId('markdown-editor').fill('Alpha Alpha');
  await page.getByPlaceholder('Search').fill('Alpha'); await page.getByPlaceholder('Replace').fill('$&');
  await page.getByRole('button', { name: 'First', exact: true }).click();
  await expect(page.getByTestId('markdown-editor')).toHaveValue('$& Alpha');
  await joinRoom(page, `switch-b-${Date.now()}`);
  await expect(page.getByTestId('markdown-editor')).toHaveValue('');
});

test('two stale title editors receive a conflict and can review before retrying', async ({ browser }) => {
  const context = await browser.newContext(); const a = await context.newPage(); const b = await context.newPage();
  try {
    const room = `conflict-${Date.now()}`; await a.goto('/'); await b.goto('/'); await joinRoom(a, room); await joinRoom(b, room);
    await a.getByLabel('Document title').fill('First title'); await a.getByRole('button', { name: 'Save title', exact: true }).click();
    await expect(a.getByRole('status')).toContainText('Title saved');
    await b.getByLabel('Document title').fill('Second title'); await b.getByRole('button', { name: 'Save title', exact: true }).click();
    await expect(b.getByRole('alert')).toContainText('metadata changed'); await expect(b.getByLabel('Document title')).toHaveValue('Second title');
    await b.getByRole('button', { name: 'Save title', exact: true }).click(); await expect(b.getByRole('status')).toContainText('Title saved');
  } finally { await context.close(); }
});

test('imports a file only after confirmation and applies toolbar formatting', async ({ page }) => {
  await page.goto('/'); await joinRoom(page, `import-${Date.now()}`);
  page.once('dialog', dialog => dialog.accept());
  await page.getByLabel('Import Markdown file').setInputFiles({ name: 'sample.md', mimeType: 'text/markdown', buffer: Buffer.from('# Imported\n\nA note') });
  await expect(page.getByTestId('markdown-editor')).toHaveValue('# Imported\n\nA note');
  const editor = page.getByTestId('markdown-editor'); await editor.fill('Bold me');
  await editor.selectText(); await page.getByRole('button', { name: 'Bold', exact: true }).click();
  await expect(editor).toHaveValue('**Bold me**');
  await expect(page.getByTestId('markdown-preview').locator('strong')).toHaveText('Bold me');
});
''';p.write_text(s,encoding='utf-8')
p=P/'.gitignore';s=p.read_text();s+='\n.test-data/\nserver/data/\n';p.write_text(s,encoding='utf-8')
p=B/'.gitignore';s=p.read_text();s+='\n/playwright-browsers/\n';p.write_text(s,encoding='utf-8')
