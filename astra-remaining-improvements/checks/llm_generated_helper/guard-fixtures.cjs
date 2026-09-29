// Protect cleanup in original tests without changing the baseline application.
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const roots = new Set();
const mkdtemp = fs.mkdtempSync.bind(fs);
const remove = fs.rmSync.bind(fs);
fs.mkdtempSync = (...args) => {
  const result = mkdtemp(...args);
  const root = path.resolve(String(result));
  if (path.dirname(root) !== path.resolve(os.tmpdir())) throw new Error('Unexpected fixture parent');
  roots.add(root);
  return result;
};
fs.rmSync = (target, options) => {
  const resolved = path.resolve(String(target));
  if (![...roots].some(root => resolved === root || resolved.startsWith(root + path.sep))) throw new Error('Refusing cleanup outside a newly owned fixture');
  return remove(target, options);
};
