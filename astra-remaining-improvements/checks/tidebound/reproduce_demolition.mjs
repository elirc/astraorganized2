import ts from '../../stage/4de416cd300b/node_modules/typescript/lib/typescript.js';
import fs from 'node:fs/promises';
import { createRequire } from 'node:module';
import assert from 'node:assert/strict';

const stage = new URL('../../stage/4de416cd300b/', import.meta.url);
const evidence = [];
for (const variant of ['original', 'current']) {
  const destination = new URL(`./demolition-${variant}/`, import.meta.url);
  await fs.mkdir(destination, { recursive: true });
  await fs.writeFile(new URL('package.json', destination), '{"type":"commonjs"}\n');
  for (const name of ['types', 'data', 'engine']) {
    const source = new URL(`${variant === 'original' ? 'docs/original/' : ''}src/${name}.ts`, stage);
    const text = await fs.readFile(source, 'utf8');
    const result = ts.transpileModule(text, { compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.CommonJS } });
    await fs.writeFile(new URL(name + '.js', destination), result.outputText);
  }
  const require = createRequire(new URL('package.json', destination));
  const engine = require('./engine.js');
  const state = engine.newGame('demolition-regression');
  const home = state.islands[0];
  for (const resource of Object.keys(home.inventory)) home.inventory[resource] = 0;
  home.inventory.wood = 1000;
  home.buildings.find(building => building.type === 'warehouse').enabled = false;
  const lumberyard = home.buildings.find(building => building.type === 'lumberyard');
  const result = engine.removeBuilding(state, home.id, lumberyard.id);
  assert.equal(result.ok, true);
  assert.equal(home.inventory.wood, variant === 'original' ? 400 : 1000);
  evidence.push({ variant, beforeWood: 1000, afterWood: home.inventory.wood, result });
}
await fs.writeFile(new URL('demolition-comparison.json', import.meta.url), JSON.stringify(evidence, null, 2));
console.log(JSON.stringify(evidence, null, 2));
