from pathlib import Path
import json
BASE=Path(__file__).resolve().parent/'stage'
def read(n,f):return (BASE/n/f).read_text(encoding='utf-8')
def write(n,f,s):
 p=BASE/n/f;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def replace(n,f,a,b):
 s=read(n,f);assert a in s,(n,f,a[:70]);write(n,f,s.replace(a,b))

write('05','src/store/shoppingState.ts', '''import type { Recipe } from '../types';

export interface ShoppingListState {
  recipeSlugs: string[];
  checked: Record<string, boolean>;
  quantities: Record<string, string>;
}

/** Treat browser storage as untrusted input, while retaining valid v1 data. */
export function normalizeShoppingState(value: unknown, recipes: Recipe[]): ShoppingListState {
  const empty: ShoppingListState = { recipeSlugs: [], checked: {}, quantities: {} };
  if (!value || typeof value !== 'object' || Array.isArray(value)) return empty;
  const input = value as Record<string, unknown>;
  const recipeSlugs = Array.isArray(input.recipeSlugs)
    ? [...new Set(input.recipeSlugs.filter((slug): slug is string =>
        typeof slug === 'string' && recipes.some((recipe) => recipe.slug === slug)))] : [];
  const validKeys = new Set(recipeSlugs.flatMap((slug) =>
    recipes.find((recipe) => recipe.slug === slug)!.ingredients.map((_, i) => `${slug}:${i}`)));
  const entries = (field: unknown): [string, unknown][] =>
    field && typeof field === 'object' && !Array.isArray(field) ? Object.entries(field) : [];
  return {
    recipeSlugs,
    checked: Object.fromEntries(entries(input.checked).filter(([key, v]) => validKeys.has(key) && typeof v === 'boolean')) as Record<string, boolean>,
    quantities: Object.fromEntries(entries(input.quantities).filter(([key, v]) => validKeys.has(key) && typeof v === 'string' && v.length <= 100)) as Record<string, string>,
  };
}

/** Use the same effective quantities for the screen and clipboard. */
export function ingredientsWithQuantities(recipe: Recipe, quantities: Record<string, string>) {
  return recipe.ingredients.map((ingredient, index) => ({
    ...ingredient, quantity: quantities[`${recipe.slug}:${index}`] ?? ingredient.quantity,
  }));
}
''')
s=read('05','src/store/ShoppingListContext.tsx')
a=s.index('interface ShoppingListState {');z=s.index('interface ShoppingListContextValue',a)
s=s[:a]+"import { normalizeShoppingState, type ShoppingListState } from './shoppingState';\n\n"+s[z:]
s=s.replace('  checked: Record<string, boolean>;','  checked: Record<string, boolean>;\n  quantities: Record<string, string>;\n  setQuantity: (key: string, value: string) => void;\n  storageError: boolean;')
a=s.index('function loadState()');z=s.index('const ShoppingListContext',a)
s=s[:a]+'''function loadState(): ShoppingListState {
  try {
    return normalizeShoppingState(JSON.parse(window.localStorage.getItem(STORAGE_KEY) ?? 'null'), RECIPES);
  } catch { return normalizeShoppingState(null, RECIPES); }
}

'''+s[z:]
s=s.replace('  const [state, setState] = useState<ShoppingListState>(loadState);','  const [state, setState] = useState<ShoppingListState>(loadState);\n  const [storageError, setStorageError] = useState(false);')
s=s.replace('window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));','window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));\n      setStorageError(false);')
s=s.replace('// storage unavailable (private mode etc.) — keep in memory only','setStorageError(true); // Keep the current session usable; disclose persistence failure.')
# Remove operations must drop stale quantity keys as well as checked keys.
s=s.replace('      recipeSlugs: s.recipeSlugs.filter((x) => x !== slug),','      quantities: Object.fromEntries(Object.entries(s.quantities).filter(([key]) => !key.startsWith(`${slug}:`))),\n      recipeSlugs: s.recipeSlugs.filter((x) => x !== slug),')
s=s.replace('              recipeSlugs: s.recipeSlugs.filter((x) => x !== slug),','              quantities: Object.fromEntries(Object.entries(s.quantities).filter(([key]) => !key.startsWith(`${slug}:`))),\n              recipeSlugs: s.recipeSlugs.filter((x) => x !== slug),')
s=s.replace('setState({ recipeSlugs: [], checked: {} });','setState({ recipeSlugs: [], checked: {}, quantities: {} });')
s=s.replace('  const clearChecked =', '''  const setQuantity = useCallback((key: string, value: string) => {
    if (value.length > 100) return;
    setState((s) => normalizeShoppingState({ ...s, quantities: { ...s.quantities, [key]: value } }, RECIPES));
  }, []);

  const clearChecked =''')
s=s.replace('      checked: state.checked,','      checked: state.checked,\n      quantities: state.quantities,\n      setQuantity,\n      storageError,')
s=s.replace('}, [state, addRecipe,','}, [state, setQuantity, storageError, addRecipe,')
write('05','src/store/ShoppingListContext.tsx',s)
replace('05','src/components/IngredientChecklist.tsx','  onToggle: (key: string) => void;','  onToggle: (key: string) => void;\n  onQuantityChange?: (key: string, value: string) => void;')
replace('05','src/components/IngredientChecklist.tsx','checked, onToggle }: Props','checked, onToggle, onQuantityChange }: Props')
replace('05','src/components/IngredientChecklist.tsx','                  </button>','''                  </button>
                  {onQuantityChange && (
                    <label className="quantity-control">
                      <span>Quantity for {ing.item}</span>
                      <input type="text" maxLength={100} value={ing.quantity}
                        onChange={(event) => onQuantityChange(key, event.target.value)} />
                    </label>
                  )}''')
replace('05','src/pages/ShoppingListPage.tsx',"import { Link }", "import { ingredientsWithQuantities } from '../store/shoppingState';\nimport { Link }")
replace('05','src/pages/ShoppingListPage.tsx','recipes, checked, toggleChecked, removeRecipe, clearChecked, clearAll','recipes, checked, quantities, setQuantity, storageError, toggleChecked, removeRecipe, clearChecked, clearAll')
replace('05','src/pages/ShoppingListPage.tsx','ingredientsToText(r.name, r.ingredients)','ingredientsToText(r.name, ingredientsWithQuantities(r, quantities))')
replace('05','src/pages/ShoppingListPage.tsx','        <div className="shopping-toolbar">','        {storageError && <p role="alert">Changes are available in this tab but could not be saved on this device.</p>}\n        <div className="shopping-toolbar">')
replace('05','src/pages/ShoppingListPage.tsx','ingredients={recipe.ingredients}','ingredients={ingredientsWithQuantities(recipe, quantities)}\n                  onQuantityChange={setQuantity}')
replace('05','src/pages/ShoppingListPage.tsx','className="remove-btn" onClick','className="remove-btn" aria-label={`Remove ${recipe.name} from shopping list`} onClick')
write('05','src/index.css',read('05','src/index.css')+'''
.quantity-control { display: flex; flex-wrap: wrap; align-items: center; gap: .5rem; margin: .25rem 0 1rem 2rem; font-size: .85rem; }
.quantity-control input { max-width: 14rem; padding: .45rem; border: 1px solid currentColor; border-radius: .3rem; font: inherit; }
.quantity-control input:focus-visible { outline: 3px solid #2563eb; outline-offset: 2px; }
''')

write('06','src/jobBackup.js', '''const FORMAT = 'daybook.jobs';
const STATUSES = new Set(['applied', 'screening', 'interview', 'offer', 'closed']);
export const MAX_BACKUP_BYTES = 2 * 1024 * 1024;

/** Validate the entire payload before a single storage mutation is scheduled. */
export function parseJobBackup(text) {
  if (typeof text !== 'string' || new TextEncoder().encode(text).length > MAX_BACKUP_BYTES)
    throw new Error('Choose a JSON backup no larger than 2 MB.');
  let backup;
  try { backup = JSON.parse(text); } catch { throw new Error('The file is not valid JSON.'); }
  if (!backup || backup.format !== FORMAT || backup.version !== 1 || !Array.isArray(backup.applications))
    throw new Error('Expected a Daybook applications backup, version 1.');
  if (backup.applications.length > 10000) throw new Error('A backup may contain at most 10,000 applications.');
  const ids = new Set();
  return backup.applications.map((record, index) => {
    const fail = (reason) => { throw new Error(`Application ${index + 1}: ${reason}`); };
    if (!record || typeof record !== 'object' || Array.isArray(record)) fail('expected an object.');
    const value = {};
    for (const field of ['id', 'company', 'role', 'location', 'url', 'status', 'stack', 'date', 'notes']) {
      const item = record[field] ?? '';
      if (typeof item !== 'string' || item.length > (field === 'notes' ? 100000 : 5000)) fail(`${field} must be bounded text.`);
      value[field] = item;
    }
    if (!value.id.trim() || ids.has(value.id)) fail('id is missing or duplicated.');
    ids.add(value.id);
    if (!value.company.trim()) fail('company is required.');
    if (!STATUSES.has(value.status)) fail('unknown status.');
    if (value.date) {
      const date = new Date(`${value.date}T00:00:00Z`);
      if (!/^\\d{4}-\\d{2}-\\d{2}$/.test(value.date) || !Number.isFinite(date.getTime()) || date.toISOString().slice(0,10) !== value.date)
        fail('date must be a real YYYY-MM-DD date or empty.');
    }
    if (value.url) {
      try { if (!['http:', 'https:'].includes(new URL(value.url).protocol)) fail('URL must use http or https.'); }
      catch { fail('URL must be an absolute http or https URL.'); }
    }
    return value;
  });
}

export function exportJobBackup(applications) {
  const text = JSON.stringify({ format: FORMAT, version: 1, applications }, null, 2);
  parseJobBackup(text); // Never generate a backup the importer cannot restore.
  return text;
}

export async function commitJobBackup(storage, text) {
  const applications = parseJobBackup(text);
  await storage.set('jobtracker:data', JSON.stringify(applications));
  return applications;
}
''')
s=read('06','src/JobTracker.jsx')
s="import { commitJobBackup, exportJobBackup, MAX_BACKUP_BYTES } from './jobBackup.js';\n"+s
s=s.replace('  const [apps, setApps] = useState([]);','  const [apps, setApps] = useState([]);\n  const [importing, setImporting] = useState(false);\n  const [backupMessage, setBackupMessage] = useState("");')
marker='  /* form ------------------------------------------------------------------ */'
s=s.replace(marker,'''  const exportApplications = () => {
    try {
      const text = exportJobBackup(apps);
      const url = URL.createObjectURL(new Blob([text], { type: 'application/json' }));
      const anchor = document.createElement('a');
      anchor.href = url; anchor.download = 'daybook-applications.json';
      document.body.append(anchor); anchor.click(); anchor.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
      setBackupMessage('Application backup exported. Calendar events are separate.');
    } catch (error) { setBackupMessage(error.message); }
  };

  const importApplications = async (event) => {
    const file = event.target.files?.[0];
    event.target.value = '';
    if (!file) return;
    setImporting(true);
    try {
      if (file.size > MAX_BACKUP_BYTES) throw new Error('Choose a JSON backup no larger than 2 MB.');
      const text = await file.text();
      // Join the existing write queue so an older edit cannot overwrite import.
      const operation = writeQueue.current.catch(() => {}).then(() => commitJobBackup(window.storage, text));
      writeQueue.current = operation;
      const next = await operation;
      setApps(next);
      closeForm(); setExpandedId(null); setSaveError(false);
      setBackupMessage(`Imported ${next.length} applications. Calendar events were not changed.`);
    } catch (error) {
      setBackupMessage(`Import failed: ${error.message} Existing applications are unchanged.`);
    } finally { setImporting(false); }
  };

'''+marker)
s=s.replace('    <div style={S.column}>','''    <fieldset disabled={importing} style={{ ...S.column, border: 0, padding: 0, minWidth: 0 }}>
      <div aria-label="Application backups" style={{ marginBottom: 20 }}>
        <button type="button" disabled={!loaded} onClick={exportApplications}>Export applications</button>{' '}
        <label>Import applications (replaces current list)
          <input type="file" accept=".json,application/json" disabled={!loaded} onChange={importApplications} />
        </label>
        <p role="status">{importing ? 'Validating and saving backup…' : backupMessage}</p>
      </div>''')
pos=s.rfind('    </div>');assert pos>=0
s=s[:pos]+'    </fieldset>'+s[pos+len('    </div>'):]
write('06','src/JobTracker.jsx',s)
print('Prepared quantity editing and validated application backups')
