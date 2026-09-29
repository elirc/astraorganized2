from pathlib import Path
import hashlib
import json

C = Path(__file__).resolve().parent
B = C.parents[1]
S = B / "stage/44013f102ff1"
baseline = json.loads((B / "baselines/44013f102ff1.json").read_text(encoding="utf-8"))["files"]
items = [(relative, S / relative) for relative in baseline if relative.startswith(("src/", "test/")) or relative in {"README.md", "package.json", "package-lock.json"}]
for relative, source in items:
    assert hashlib.sha256(source.read_bytes()).hexdigest() == baseline[relative]
    destination = S / "docs/original" / (relative + ".txt")
    assert not destination.exists()
for relative, source in items:
    destination = S / "docs/original" / (relative + ".txt")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(source.read_bytes())
print(json.dumps({"originalsPreserved": len(items)}))
