from pathlib import Path
BASE=Path(__file__).resolve().parent/'stage'
def read(n,f):return (BASE/n/f).read_text(encoding='utf-8')
def write(n,f,s):
 p=BASE/n/f;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def replace(n,f,a,b):
 s=read(n,f);assert a in s,(n,f,a[:70]);write(n,f,s.replace(a,b))

replace('07','server/src/services/taskService.js','!Number.isInteger(id)', '!Number.isSafeInteger(id)')
replace('07','server/src/services/taskService.js','  if (title.length === 0)', "  if (title.length > 255) throw new ValidationError('Title must be 255 characters or fewer.');\n\n  if (title.length === 0)")
replace('07','server/src/services/taskService.js',"    updates.due_date = normalizeDueDate(payload.due_date);", '''    // An overdue task must remain editable when its existing date is submitted.
    const existingDate = existingTask.due_date ? toDateOnly(new Date(existingTask.due_date)) : null;
    updates.due_date = payload.due_date === existingDate ? existingDate : normalizeDueDate(payload.due_date);''')

write('08','server/src/utils/csv.js', '''const { ValidationError } = require('../middleware/errors');
const HEADERS = ['first_name','last_name','email','phone','company','street_address','city','state','zip_code','country','notes','tags'];

function escapeCsv(value) {
  const text = value == null ? '' : String(value);
  return /[",\\r\\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
}
function contactsToCsv(contacts) {
  return [HEADERS.join(','), ...contacts.map((contact) => HEADERS.map((key) =>
    escapeCsv(key === 'tags' ? (contact.tags || []).map((tag) => tag.name).join('|') : contact[key])).join(','))].join('\\n');
}

/** A small state machine: delimiters only split fields outside quoted text. */
function csvToContacts(csv) {
  if (typeof csv !== 'string' || !csv.trim()) throw new ValidationError('CSV text is required');
  const text = csv.replace(/^\\uFEFF/, '');
  const rows = []; let row = []; let field = ''; let quoted = false; let closed = false;
  function endField() { row.push(field); field = ''; closed = false; }
  function endRow() {
    endField();
    if (row.some((value) => value.trim())) rows.push(row);
    row = [];
  }
  for (let i = 0; i < text.length; i++) {
    const char = text[i];
    if (quoted) {
      if (char === '"' && text[i + 1] === '"') { field += '"'; i++; }
      else if (char === '"') { quoted = false; closed = true; }
      else field += char;
    } else if (char === ',') endField();
    else if (char === '\\n' || char === '\\r') {
      if (char === '\\r' && text[i + 1] === '\\n') i++;
      endRow();
    } else if (closed) {
      throw new ValidationError('Unexpected text after a closing CSV quote');
    } else if (char === '"') {
      if (field.length) throw new ValidationError('A quoted CSV field must start with a quote');
      quoted = true;
    } else field += char;
  }
  if (quoted) throw new ValidationError('Unclosed CSV quote');
  if (field.length || row.length || closed) endRow();
  const headers = (rows.shift() || []).map((value) => value.trim());
  if (!headers.includes('first_name') || !headers.includes('last_name'))
    throw new ValidationError('CSV headers must include first_name and last_name');
  if (new Set(headers).size !== headers.length || headers.some((key) => !HEADERS.includes(key)))
    throw new ValidationError('CSV has duplicate or unsupported headers');
  if (!rows.length || rows.length > 1000) throw new ValidationError('Import between 1 and 1000 contacts at a time');
  return rows.map((values, index) => {
    if (values.length !== headers.length) throw new ValidationError(`CSV record ${index + 2} has the wrong number of fields`);
    return Object.fromEntries(headers.map((key, i) => [key, values[i]]));
  });
}
module.exports = { contactsToCsv, csvToContacts };
''')
s=read('08','server/src/services/contactService.js')
a=s.index('function parseContactPayload(');z=s.index('\n/**',a)
s=s[:a]+'''function parseContactPayload(payload) {
  if (!payload || typeof payload !== 'object' || Array.isArray(payload)) throw new ValidationError('Contact must be an object');
  const limits = { first_name:100, last_name:100, email:255, phone:30, company:255, street_address:255, city:100, state:100, zip_code:20, country:100, notes:100000 };
  const contact = {};
  for (const [key, limit] of Object.entries(limits)) {
    const value = payload[key];
    if (value != null && typeof value !== 'string') throw new ValidationError(`${key} must be text`);
    if (value && value.trim().length > limit) throw new ValidationError(`${key} exceeds ${limit} characters`);
    contact[key] = value?.trim() || null;
  }
  if (!contact.first_name || !contact.last_name) throw new ValidationError('First name and last name are required');
  if (contact.email && !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(contact.email)) throw new ValidationError('Email must be valid');
  const tagIds = [...new Set(Array.isArray(payload.tagIds) ? payload.tagIds.map(Number) : [])];
  if (tagIds.some((id) => !Number.isSafeInteger(id) || id < 1)) throw new ValidationError('Tag ids must be positive integers');
  return { contact, tagIds };
}
'''+s[z:]
a=s.index('async function importContacts(');z=s.index('\nmodule.exports',a)
s=s[:a]+'''async function importContacts(csv) {
  const rows = csvToContacts(csv);
  // Parse every row before opening a transaction: invalid row 20 saves no rows.
  const batch = rows.map((row, index) => {
    try {
      const { contact } = parseContactPayload(row);
      const tags = [...new Set((row.tags || '').split('|').map((tag) => tag.trim()).filter(Boolean))];
      if (tags.some((tag) => tag.length > 50)) throw new ValidationError('Tag names must be 50 characters or fewer');
      return { contact, tags };
    } catch (error) { throw new ValidationError(`CSV record ${index + 2}: ${error.message}`); }
  });
  try {
    const created = await contactModel.importContactBatch(batch);
    return { imported: created.length, contacts: created };
  } catch (error) {
    if (error.code === '23505') throw new ValidationError('An email already exists or is repeated in the CSV; no contacts were imported');
    throw error;
  }
}
'''+s[z:]
# Avoid NaN/fractional offsets, and add stable ordering for equal surnames.
s=s.replace('  const page = Math.max(Number(query.page || 1), 1);\n  const limit = Math.min(Math.max(Number(query.limit || 20), 1), 100);', '''  const page = Number(query.page ?? 1);
  const limit = Number(query.limit ?? 20);
  if (!Number.isSafeInteger(page) || page < 1 || !Number.isInteger(limit) || limit < 1 || limit > 100 || !Number.isSafeInteger((page - 1) * limit))
    throw new ValidationError('page must be a positive integer and limit must be from 1 to 100');''')
write('08','server/src/services/contactService.js',s)
replace('08','server/src/models/contactModel.js','.orderBy(`contacts.${sort}`, order)','.orderBy(`contacts.${sort}`, order)\n    .orderBy("contacts.id", "asc")')
replace('08','server/src/models/contactModel.js','module.exports = {', '''/** One transaction covers contacts, tag creation and junction rows. */
async function importContactBatch(batch) {
  return db.transaction(async (trx) => {
    const contacts = [];
    for (const { contact, tags } of batch) {
      const [created] = await trx('contacts').insert(contact).returning('*');
      const attached = [];
      for (const name of tags) {
        await trx('tags').insert({ name }).onConflict('name').ignore();
        const tag = await trx('tags').where({ name }).first();
        await trx('contact_tags').insert({ contact_id: created.id, tag_id: tag.id });
        attached.push(tag);
      }
      contacts.push({ ...created, tags: attached });
    }
    return contacts;
  });
}

module.exports = {
  importContactBatch,''')

# An aggregate query cannot retain the raw expense columns from the base query.
replace('09','server/src/models/expenseModel.js','  return expenseQuery(filters)\n    .groupBy','  return expenseQuery(filters)\n    .clearSelect()\n    .groupBy')
s=read('09','server/src/services/expenseService.js')
s=s.replace('  if (!amount || amount <= 0)', '  if (!Number.isFinite(amount) || amount <= 0 || amount > 99999999.99 || Math.abs(amount * 100 - Math.round(amount * 100)) > 0.00001)')
s=s.replace('  if (!payload.expense_date) throw new ValidationError("Expense date is required");','  validDate(payload.expense_date);')
s=s.replace('  return model.listExpenses(query);','  return model.listExpenses(validFilters(query));')
s=s.replace('expensesToCsv(await model.listExpenses(query))','expensesToCsv(await model.listExpenses(validFilters(query)))')
s=s.replace('  monthlySummary: model.monthlySummary,\n  byCategory: model.byCategory,\n  dailyTrend: model.dailyTrend,\n  weeklyTrend: model.weeklyTrend', '''  monthlySummary: (month) => model.monthlySummary(validMonth(month)),
  byCategory: (filters) => model.byCategory(validFilters(filters)),
  dailyTrend: (month) => model.dailyTrend(validMonth(month)),
  weeklyTrend: (start) => model.weeklyTrend(validDate(start))''')
s=s.replace('module.exports = {','''function validDate(value) {
  if (typeof value !== 'string' || !/^\\d{4}-\\d{2}-\\d{2}$/.test(value)) throw new ValidationError('Use a YYYY-MM-DD date');
  const date = new Date(`${value}T00:00:00Z`);
  if (!Number.isFinite(date.getTime()) || date.toISOString().slice(0,10) !== value) throw new ValidationError('Use a real calendar date');
  return value;
}
function validMonth(value) {
  if (typeof value !== 'string' || !/^\\d{4}-(0[1-9]|1[0-2])$/.test(value)) throw new ValidationError('Use a YYYY-MM month');
  return value;
}
function validFilters(query = {}) {
  if (query.start_date) validDate(query.start_date);
  if (query.end_date) validDate(query.end_date);
  if (query.start_date && query.end_date && query.start_date > query.end_date) throw new ValidationError('start_date must not follow end_date');
  if (query.category_id && (!Number.isSafeInteger(Number(query.category_id)) || Number(query.category_id) < 1)) throw new ValidationError('category_id must be a positive integer');
  return query;
}

module.exports = {''')
write('09','server/src/services/expenseService.js',s)

s=read('10','server/src/services/recipeService.ts')
a=s.index('function parseRecipeInput(');z=s.index('\n/**',a)
s=s[:a]+'''export function parseRecipeInput(body: Record<string, unknown>): RecipeInput {
  if (!body || typeof body !== 'object' || Array.isArray(body)) throw new ValidationError('Recipe must be an object');
  function text(value: unknown, field: string, limit: number, required = false): string | undefined {
    if (value == null && !required) return undefined;
    if (typeof value !== 'string' || value.trim().length > limit || (required && !value.trim()))
      throw new ValidationError(`${field} must be ${required ? 'non-empty ' : ''}text, at most ${limit} characters`);
    return value.trim();
  }
  function positive(value: unknown, field: string): number | undefined {
    if (value == null || value === '') return undefined;
    if ((typeof value !== 'number' && typeof value !== 'string') || !Number.isSafeInteger(Number(value)) || Number(value) < 1 || Number(value) > 2147483647)
      throw new ValidationError(`${field} must be a positive integer`);
    return Number(value);
  }
  function object(value: unknown): Record<string, unknown> {
    if (!value || typeof value !== 'object' || Array.isArray(value)) throw new ValidationError('Ingredients and steps must be objects');
    return value as Record<string, unknown>;
  }
  if (!Array.isArray(body.ingredients) || body.ingredients.length < 1 || body.ingredients.length > 100)
    throw new ValidationError('Provide 1 to 100 ingredients');
  if (!Array.isArray(body.steps) || body.steps.length < 1 || body.steps.length > 200)
    throw new ValidationError('Provide 1 to 200 steps');
  const difficulty = body.difficulty ?? 'medium';
  if (!['easy','medium','hard'].includes(String(difficulty))) throw new ValidationError('Difficulty must be easy, medium or hard');
  if (body.isPublic !== undefined && typeof body.isPublic !== 'boolean') throw new ValidationError('isPublic must be a boolean');
  if (body.categoryIds !== undefined && !Array.isArray(body.categoryIds)) throw new ValidationError('categoryIds must be an array');
  const categoryIds = [...new Set((body.categoryIds as unknown[] ?? []).map((id) => {
    const value = positive(id, 'Category id');
    if (!value) throw new ValidationError('Category ids must be positive integers');
    return value;
  }))];
  return {
    title: text(body.title, 'Title', 255, true)!,
    description: text(body.description, 'Description', 100000),
    imageUrl: text(body.imageUrl, 'Image URL', 500),
    prepTimeMinutes: positive(body.prepTimeMinutes, 'Prep time'),
    cookTimeMinutes: positive(body.cookTimeMinutes, 'Cook time'),
    servings: positive(body.servings, 'Servings'),
    difficulty: difficulty as RecipeInput['difficulty'], isPublic: body.isPublic !== false,
    ingredients: body.ingredients.map((value) => {
      const item = object(value);
      return { name: text(item.name,'Ingredient name',200,true)!, quantity: text(item.quantity,'Quantity',50), unit: text(item.unit,'Unit',30) };
    }),
    steps: body.steps.map((value) => {
      const item = object(value);
      return { instruction: text(item.instruction,'Step instruction',100000,true)!, imageUrl: text(item.imageUrl,'Step image URL',500) };
    }), categoryIds,
  };
}
'''+s[z:]
a=s.index('  const owner = await findRecipeOwner(recipeId);',s.index('export async function updateRecipeForUser'))
z=s.index('  return getRecipe(recipeId, userId);',a)
s=s[:a]+'''  await db.transaction(async (trx) => {
    // Lock and authorize inside the same transaction as the nested replacement.
    const owner = await trx('recipes').where({ id: recipeId }).forUpdate().first();
    if (!owner) throw new NotFoundError('Recipe not found');
    if (owner.user_id !== userId) throw new ForbiddenError('Only the owner can edit this recipe');
    const input = parseRecipeInput(body);
    await saveRecipeGraph(trx, userId, input, recipeId);
  });
'''+s[z:]
write('10','server/src/services/recipeService.ts',s)
replace('10','server/src/models/recipeModel.ts',"where({ id: recipeId }).update(row)","where({ id: recipeId, user_id: userId }).update(row)")
print('Prepared server validation, atomic CSV import and corrected reporting')
