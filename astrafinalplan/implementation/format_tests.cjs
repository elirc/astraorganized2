const fs = require('node:fs');
const path = require('node:path');
const ts = require('./stage/05/node_modules/typescript/lib/typescript.js');
const base = path.join(__dirname, 'stage');
const printer = ts.createPrinter({ newLine: ts.NewLineKind.LineFeed });
let count = 0;
for (let i = 1; i <= 10; i++) {
  const root = path.join(base, String(i).padStart(2, '0'));
  const test = path.join(root, i >= 7 ? 'server/test' : 'test');
  const files = fs.readdirSync(test).filter(name => /\.(cjs|js|ts)$/.test(name)).map(name => path.join(test, name));
  if (i === 5) files.push(path.join(root, 'src/store/shoppingState.ts'));
  if (i === 6) files.push(path.join(root, 'src/jobBackup.js'));
  if (i === 8) files.push(path.join(root, 'server/src/utils/csv.js'));
  for (const file of files) {
    if (i === 6 && !file.endsWith('jobBackup.test.js') && !file.endsWith('jobBackup.js')) continue;
    const text = fs.readFileSync(file, 'utf8');
    const source = ts.createSourceFile(file, text, ts.ScriptTarget.Latest, true, file.endsWith('.ts') ? ts.ScriptKind.TS : ts.ScriptKind.JS);
    if (source.parseDiagnostics.length) throw new Error('Cannot format ' + file);
    fs.writeFileSync(file, printer.printFile(source));
    count++;
  }
}
console.log('Formatted ' + count + ' new learning/test files for readable examples.');
