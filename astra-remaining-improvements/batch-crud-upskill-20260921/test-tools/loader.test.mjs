import test from 'node:test';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { loadTypeScript } from './load-typescript.mjs';
const root = fileURLToPath(new URL('.', import.meta.url));
test('executes actual TypeScript source with an explicit dependency contract', async () => {
  const calls = [];
  const module = await loadTypeScript('fixture.ts', { root, stubs: { 'test-adapter': { apply: value => { calls.push(value); return value * 2; } } } });
  assert.equal(module.calculate({ value: 4 }), 9);
  assert.deepEqual(calls, [4]);
});
test('unknown dependencies fail closed rather than silently faking behavior', async () => {
  await assert.rejects(loadTypeScript('fixture.ts', { root }), /Unstubbed external dependency/);
});
