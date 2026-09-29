from pathlib import Path
import hashlib
import json

B = Path(__file__).resolve().parents[2]
S = B / 'stage/4de416cd300b'
D = B.parent.parent / 'astra2'
baseline = json.loads((B / 'baselines/4de416cd300b.json').read_text(encoding='utf-8'))['files']
destination = S / 'docs/original'
assert not destination.exists()
manifest = []
for relative, expected in baseline.items():
    path = D / relative
    if path.suffix.lower() not in {'.md', '.ts', '.css', '.mjs', '.json', '.html'}:
        continue
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == expected, relative
    raw.decode('utf-8-sig')
    target = destination / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    manifest.append({'file': relative, 'sha256': expected})
(destination / 'ORIGINAL_FILES.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(json.dumps({'originalTextFilesPreserved': len(manifest)}))
