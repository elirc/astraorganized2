from pathlib import Path
import json
s=Path('astra-remaining-improvements/stage/cf8875344b43')
def w(n,c):
 p=s/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(c.strip()+'\n',encoding='utf-8')
w('package.json',json.dumps({'name':'andie-metaobject-learning-lab','version':'1.0.0','private':True,'description':'Offline-first Shopify metaobject migration learning utility','engines':{'node':'>=22'},'scripts':{'test':'node --test test/*.test.js','plan:example':'node scripts/populate-metaobjects.js plan --source fixtures/source.json --target fixtures/target.json --out plan.example.json','check':'node --check scripts/populate-metaobjects.js && node --check scripts/lib/client.js && node --check scripts/lib/planner.js'}},indent=2))
w('.gitignore','node_modules/\n.env\n.env.*\n!.env.example\nexports/\nplans/\njournals/\nplan.example.json\n')
w('.env.example',r'''
# Set these in the process environment; the script does not automatically load this file.
# Never reuse credentials previously embedded in the legacy script.
SHOPIFY_SOURCE_STORE=your-source-store
SHOPIFY_SOURCE_TOKEN=replace-with-a-new-read-token
SHOPIFY_TARGET_STORE=your-development-target
SHOPIFY_TARGET_TOKEN=replace-with-a-new-target-token
SHOPIFY_API_VERSION=2026-07
''')
w('scripts/lib/client.js',r'''
'use strict';
const API_VERSION = '2026-07';
const DEFINITIONS = `query Definitions($after: String) { metaobjectDefinitions(first: 100, after: $after) { nodes { name description displayNameKey type access { admin storefront } capabilities { publishable { enabled } translatable { enabled } } fieldDefinitions { key name required type { name } validations { name value } } } pageInfo { hasNextPage endCursor } } }`;
const ENTRIES = `query Entries($type: String!, $after: String) { metaobjects(first: 100, type: $type, after: $after) { nodes { handle capabilities { publishable { status } } fields { key value type } } pageInfo { hasNextPage endCursor } } }`;
const CREATE_DEFINITION = `mutation CreateDefinition($definition: MetaobjectDefinitionCreateInput!) { metaobjectDefinitionCreate(definition: $definition) { metaobjectDefinition { id } userErrors { field code message } } }`;
const CREATE_ENTRY = `mutation CreateEntry($metaobject: MetaobjectCreateInput!) { metaobjectCreate(metaobject: $metaobject) { metaobject { id } userErrors { field code message } } }`;
function storeName(value) { if (typeof value !== 'string' || !/^[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$|^[a-z0-9]$/.test(value)) throw new Error('Store must be a bare myshopify subdomain.'); return value; }
function createClient({ store, token, apiVersion = API_VERSION, fetchImpl = globalThis.fetch, delay = ms => new Promise(resolve => setTimeout(resolve, ms)), timeoutMs = 15000, readRetries = 2 }) {
  storeName(store);
  if (typeof token !== 'string' || !token.trim() || /[\r\n]/.test(token)) throw new Error('A token must be supplied through the environment.');
  if (apiVersion !== API_VERSION) throw new Error(`This implementation is reviewed for API ${API_VERSION}; review queries before changing versions.`);
  if (!Number.isInteger(readRetries) || readRetries < 0 || readRetries > 5 || !Number.isInteger(timeoutMs) || timeoutMs < 1) throw new Error('Invalid client limits.');
  return { store, apiVersion, async query(query, variables = {}, { mutation = false } = {}) {
    const limit = mutation ? 0 : readRetries;
    for (let attempt = 0; ; attempt++) {
      let response;
      try { response = await fetchImpl(`https://${store}.myshopify.com/admin/api/${apiVersion}/graphql.json`, { method: 'POST', redirect: 'error', headers: { 'Content-Type': 'application/json', 'X-Shopify-Access-Token': token }, body: JSON.stringify({ query, variables }), signal: AbortSignal.timeout(timeoutMs) }); }
      catch { throw new Error(mutation ? 'Mutation transport failed; outcome is unknown. Re-export before retrying.' : 'Read transport failed or timed out.'); }
      if (!mutation && [429, 502, 503, 504].includes(response.status) && attempt < limit) {
        const retry = Number(response.headers.get('Retry-After')); await delay(Number.isFinite(retry) && retry > 0 ? Math.min(retry * 1000, 10000) : 250 * 2 ** attempt); continue;
      }
      if (!response.ok) throw new Error(`Shopify HTTP ${response.status}${mutation ? '; mutation outcome must be reconciled' : ''}.`);
      const served = response.headers.get('X-Shopify-API-Version');
      if (served && served !== apiVersion) throw new Error('Shopify served a different API version; review compatibility before continuing.');
      let payload; try { payload = await response.json(); } catch { throw new Error('Shopify returned invalid JSON.'); }
      if (payload?.errors?.length) {
        if (!mutation && payload.errors.every(error => error.extensions?.code === 'THROTTLED') && attempt < limit) { await delay(250 * 2 ** attempt); continue; }
        throw new Error('Shopify returned GraphQL errors; no successful result was accepted.');
      }
      if (!payload || !payload.data || typeof payload.data !== 'object') throw new Error('Shopify returned no GraphQL data.');
      return payload.data;
    }
  } };
}
async function pages(client, query, key, variables = {}, maxPages = 1000) {
  let after = null; const seen = new Set(); const nodes = [];
  for (let page = 0; page < maxPages; page++) {
    const data = await client.query(query, { ...variables, after }); const connection = data[key];
    if (!connection || !Array.isArray(connection.nodes) || typeof connection.pageInfo?.hasNextPage !== 'boolean') throw new Error('Malformed paginated response.');
    nodes.push(...connection.nodes);
    if (!connection.pageInfo.hasNextPage) return nodes;
    const cursor = connection.pageInfo.endCursor;
    if (typeof cursor !== 'string' || !cursor || seen.has(cursor)) throw new Error('Pagination cursor did not advance.');
    seen.add(cursor); after = cursor;
  }
  throw new Error('Pagination limit exceeded; snapshot is incomplete.');
}
async function exportSnapshot(client) {
  const definitions = await pages(client, DEFINITIONS, 'metaobjectDefinitions');
  const complete = [];
  for (const definition of definitions) complete.push({ ...definition, metaobjects: await pages(client, ENTRIES, 'metaobjects', { type: definition.type }) });
  return { formatVersion: 1, apiVersion: client.apiVersion, store: client.store, definitions: complete };
}
async function createRemote(client, operation) {
  const definition = operation.kind === 'createDefinition';
  if (!definition && operation.kind !== 'createEntry') throw new Error('Unsupported mutation operation.');
  const data = await client.query(definition ? CREATE_DEFINITION : CREATE_ENTRY, definition ? { definition: operation.input } : { metaobject: operation.input }, { mutation: true });
  const payload = data[definition ? 'metaobjectDefinitionCreate' : 'metaobjectCreate'];
  if (!payload || !Array.isArray(payload.userErrors)) throw new Error('Mutation payload is incomplete; reconcile before retrying.');
  if (payload.userErrors.length) throw new Error('Shopify rejected the mutation with userErrors; inspect the plan and schema.');
  const id = payload[definition ? 'metaobjectDefinition' : 'metaobject']?.id;
  if (typeof id !== 'string' || !id) throw new Error('Mutation returned no resource ID; reconcile before retrying.');
  return id;
}
module.exports = { API_VERSION, storeName, createClient, pages, exportSnapshot, createRemote, DEFINITIONS, ENTRIES };
''')
w('scripts/lib/planner.js',r'''
'use strict';
const { createHash } = require('node:crypto');
const { API_VERSION, storeName, exportSnapshot, createRemote } = require('./client');
function stable(value) { if (Array.isArray(value)) return value.map(stable); if (value && typeof value === 'object') return Object.fromEntries(Object.keys(value).sort().map(key => [key, stable(value[key])])); return value; }
const canonical = value => JSON.stringify(stable(value));
const hash = value => createHash('sha256').update(canonical(value)).digest('hex');
const text = (value, label) => { if (typeof value !== 'string' || !value.trim()) throw new Error(`Invalid ${label}.`); return value; };
function array(value, label) { if (!Array.isArray(value)) throw new Error(`Invalid ${label}.`); return value; }
function unique(values, label) { if (new Set(values).size !== values.length) throw new Error(`Duplicate ${label}.`); }
function normalizeSnapshot(snapshot) {
  if (!snapshot || snapshot.formatVersion !== 1 || snapshot.apiVersion !== API_VERSION) throw new Error('Unsupported snapshot format or API version.');
  storeName(snapshot.store);
  const definitions = array(snapshot.definitions, 'definitions').map(def => {
    text(def.type, 'definition type'); text(def.name, 'definition name');
    const fields = array(def.fieldDefinitions, 'field definitions').map(field => {
      text(field.key, 'field key'); text(field.name, 'field name'); text(field.type?.name, 'field type');
      if (typeof field.required !== 'boolean') throw new Error('Field required must be boolean.');
      const validations = array(field.validations, 'validations').map(v => ({ name: text(v.name, 'validation name'), value: text(v.value, 'validation value') })).sort((a,b) => a.name.localeCompare(b.name));
      return { key: field.key, name: field.name, type: field.type.name, required: field.required, validations };
    }).sort((a,b) => a.key.localeCompare(b.key));
    unique(fields.map(f => f.key), 'field key');
    const input = { name: def.name, type: def.type, fieldDefinitions: fields };
    if (def.description != null && def.description !== '') input.description = text(def.description, 'description');
    if (def.displayNameKey != null && def.displayNameKey !== '') { if (!fields.some(f => f.key === def.displayNameKey)) throw new Error('Unknown display-name field.'); input.displayNameKey = def.displayNameKey; }
    if (def.access != null) {
      input.access = {}; for (const key of ['admin','storefront']) if (def.access[key] != null) input.access[key] = text(def.access[key], 'access setting');
    }
    if (def.capabilities != null) {
      input.capabilities = {};
      for (const key of ['publishable','translatable']) if (def.capabilities[key] != null) { if (typeof def.capabilities[key].enabled !== 'boolean') throw new Error('Invalid capability.'); input.capabilities[key] = { enabled: def.capabilities[key].enabled }; }
    }
    const entries = array(def.metaobjects, 'metaobjects').map(entry => {
      const values = array(entry.fields, 'entry fields').map(field => {
        text(field.key, 'entry field key'); text(field.type, 'entry field type');
        if (field.value !== null && typeof field.value !== 'string') throw new Error('Entry field value must be text or null.');
        const declaration = fields.find(f => f.key === field.key); if (!declaration || declaration.type !== field.type) throw new Error('Entry field does not match its definition.');
        return { key: field.key, value: field.value, type: field.type };
      }).sort((a,b) => a.key.localeCompare(b.key));
      unique(values.map(f => f.key), 'entry field key');
      for (const field of fields) if (field.required && !values.some(v => v.key === field.key && v.value !== null && v.value !== '')) throw new Error('Required entry field is missing.');
      const normalized = { handle: text(entry.handle, 'entry handle'), fields: values };
      if (entry.capabilities?.publishable != null) {
        const status = entry.capabilities.publishable.status; if (!['ACTIVE','DRAFT'].includes(status)) throw new Error('Invalid publication status.');
        normalized.capabilities = { publishable: { status } };
      }
      return normalized;
    }).sort((a,b) => a.handle.localeCompare(b.handle));
    unique(entries.map(e => e.handle), 'entry handle'); return { type: def.type, input, entries };
  }).sort((a,b) => a.type.localeCompare(b.type));
  unique(definitions.map(d => d.type), 'definition type');
  return { formatVersion: 1, apiVersion: snapshot.apiVersion, store: snapshot.store, definitions };
}
function buildPlan(sourceRaw, targetRaw) {
  const source = normalizeSnapshot(sourceRaw), target = normalizeSnapshot(targetRaw);
  if (source.store === target.store) throw new Error('Source and target stores must differ.');
  const operations = [], conflicts = [], unchanged = [], targetOnly = [];
  for (const definition of source.definitions) {
    const existing = target.definitions.find(d => d.type === definition.type);
    if (definition.type.startsWith('$') || definition.type.startsWith('app--')) { conflicts.push({ type: definition.type, reason: 'App-owned type requires a separate ownership migration.' }); continue; }
    if (definition.input.fieldDefinitions.some(f => f.type.includes('reference'))) { conflicts.push({ type: definition.type, reason: 'Reference fields require cross-store ID mapping; no fields will be silently dropped.' }); continue; }
    if (existing && canonical(existing.input) !== canonical(definition.input)) { conflicts.push({ type: definition.type, reason: 'Definition differs; explicit schema migration required.' }); continue; }
    if (!existing) operations.push({ kind: 'createDefinition', type: definition.type, input: definition.input });
    for (const entry of definition.entries) {
      const match = existing?.entries.find(e => e.handle === entry.handle);
      if (match) {
        if (canonical(match) !== canonical(entry)) conflicts.push({ type: definition.type, handle: entry.handle, reason: 'Existing entry differs; update policy must be reviewed.' });
        else unchanged.push({ type: definition.type, handle: entry.handle });
      } else {
        const input = { type: definition.type, handle: entry.handle, fields: entry.fields.filter(f => f.value !== null).map(f => ({ key: f.key, value: f.value })) };
        if (entry.capabilities) input.capabilities = entry.capabilities;
        operations.push({ kind: 'createEntry', type: definition.type, handle: entry.handle, input });
      }
    }
  }
  for (const definition of target.definitions) for (const entry of definition.entries) if (!source.definitions.find(d => d.type === definition.type)?.entries.some(e => e.handle === entry.handle)) targetOnly.push({ type: definition.type, handle: entry.handle });
  return { formatVersion: 1, apiVersion: API_VERSION, sourceStore: source.store, targetStore: target.store, sourceHash: hash(source), targetHash: hash(target), operations, conflicts, unchanged, targetOnly };
}
async function applyPlan(plan, { sourceClient, targetClient, confirmTarget, journal = async () => {} }) {
  if (!plan || plan.targetStore !== confirmTarget || targetClient.store !== confirmTarget || sourceClient.store !== plan.sourceStore || sourceClient.store === targetClient.store) throw new Error('Explicit target confirmation and matching clients are required.');
  const source = await exportSnapshot(sourceClient), target = await exportSnapshot(targetClient); const current = buildPlan(source, target);
  if (canonical(plan) !== canonical(current)) throw new Error('Plan is stale or changed. Export and review a new plan.');
  if (current.conflicts.length) throw new Error('Plan has conflicts; no mutation was sent.');
  const result = { status: 'running', targetStore: targetClient.store, completed: [], failed: null };
  await journal(structuredClone(result));
  for (let index = 0; index < current.operations.length; index++) {
    const operation = current.operations[index];
    try {
      const id = await createRemote(targetClient, operation); result.completed.push({ index, kind: operation.kind, type: operation.type, handle: operation.handle, id });
      await journal(structuredClone(result));
    } catch (error) {
      result.status = 'stopped'; result.failed = { index, message: error.message };
      try { await journal(structuredClone(result)); } catch { /* Preserve the operation failure and completed in-memory receipt. */ }
      const failure = new Error('Apply stopped; earlier creates may exist. Re-export before retrying.'); failure.result = result; throw failure;
    }
  }
  result.status = 'complete'; await journal(structuredClone(result)); return result;
}
module.exports = { canonical, normalizeSnapshot, buildPlan, applyPlan };
''')
print('Dependency-free API boundary and deterministic migration planner written')
