from pathlib import Path
import hashlib, json, shutil

B = Path(__file__).resolve().parents[2]
S = B / 'stage/767d610cb528'
baseline = json.loads((B / 'baselines/767d610cb528.json').read_text(encoding='utf-8'))['files']
files = ['src/core/evaluation.js', 'src/ui/app.js', 'src/ui/index.html', 'src/ui/styles.css']
for relative in files:
    source = S / relative
    assert hashlib.sha256(source.read_bytes()).hexdigest() == baseline[relative]
    target = S / 'docs/original' / (relative + '.txt')
    assert not target.exists(), target
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
print(json.dumps({'preserved': files}))
