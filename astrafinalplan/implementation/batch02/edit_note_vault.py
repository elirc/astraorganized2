from pathlib import Path
import json
B=Path('astrafinalplan/implementation/batch02/stage')
p=B/'14/server/server.js';s=p.read_text();start=s.index('// The repository reads');repo=s[start:];s=s[:start]
s=s.replace('import { readFile, writeFile, mkdir } from "node:fs/promises";', 'import { createNoteRepository } from "./repository.js";\nimport { pathToFileURL } from "node:url";')
s=s.replace('const app = express();\nconst port = 4106;', 'const port = Number(process.env.PORT || 4106);')
s=s.replace('app.use(cors());\napp.use(express.json());\n\n','')
s=s.replace('const repository = await createNoteRepository(DATA_FILE);','''export async function createApp(file = DATA_FILE) {
const app = express();
app.use(cors());
app.use(express.json({ limit: "128kb" }));
const repository = await createNoteRepository(file);
const wrap = (handler) => (req, res, next) => Promise.resolve(handler(req, res, next)).catch(next);''')
s=s.replace('async (req, res) => {','wrap(async (req, res) => {').replace('\n});','\n}));')
a=s.index('app.listen(port,');b=s.index('\nfunction validateNote',a)
s=s[:a]+'''app.use((error, _req, res, _next) => {
  console.error("Note storage operation failed:", error.message);
  res.status(error.status === 400 ? 400 : 500).json({ error: "Could not complete the operation. Existing notes were preserved." });
});
return app;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const app = await createApp();
  app.listen(port, () => console.log(`Note Vault API listening on http://localhost:${port}`));
}
'''+s[b:]
s=s.replace('  const { title, body } = req.body;','  const { title, body } = req.body || {};').replace('  if (!title || title.trim().length < 2) {','  if (typeof title !== "string" || title.trim().length < 2 || title.length > 255) {').replace('  if (typeof body !== "string") {','  if (typeof body !== "string" || body.length > 100000) {')
s=s.replace('  const { search = "" } = req.query;','  const { search = "" } = req.query;\n  if (typeof search !== "string" || search.length > 200) return res.status(400).json({ error: "Search must be text up to 200 characters." });')
p.write_text(s,encoding='utf-8')
# Serialize read-modify-write as one queue item, not just the final write.
repo=repo.replace('async function createNoteRepository(file) {','export async function createNoteRepository(file, io = fs) {\n  let tail = Promise.resolve();\n  function serial(operation) {\n    const result = tail.then(operation);\n    tail = result.catch(() => {});\n    return result;\n  }')
repo=repo.replace('await readFile(file, "utf8")','await io.readFile(file, "utf8")')
repo=repo.replace('''    await mkdir(dirname(file), { recursive: true });
    await writeFile(file, JSON.stringify(notes, null, 2));''','''    await io.mkdir(dirname(file), { recursive: true });
    const temporary = `${file}.${crypto.randomUUID()}.tmp`;
    try {
      await io.writeFile(temporary, JSON.stringify(notes, null, 2), { flag: "wx" });
      await io.rename(temporary, file);
    } finally {
      await io.unlink(temporary).catch(() => {});
    }''')
repo=repo.replace('      return JSON.parse(raw);','      const notes = JSON.parse(raw);\n      if (!Array.isArray(notes)) throw new Error("The notes file must contain an array.");\n      return notes;')
repo=repo.replace('  return {\n    async list', '  await serial(readAll);\n  const methods = {\n    async list')
repo=repo.replace('''    }
  };
}''','''    }
  };
  return Object.fromEntries(Object.entries(methods).map(([name, operation]) => [name, (...args) => serial(() => operation(...args))]));
}''')
(B/'14/server/repository.js').write_text('import * as fs from "node:fs/promises";\nimport { dirname } from "node:path";\n\n'+repo,encoding='utf-8')
p=B/'14/package.json';d=json.loads(p.read_text());d['scripts']['test']='node --test test/*.test.js';p.write_text(json.dumps(d,indent=2)+'\n')
print('Note Vault serialized persistence and HTTP failure handling implemented.')
