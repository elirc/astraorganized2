from pathlib import Path
import hashlib
import json
import os

C = Path(__file__).resolve().parent
B = C.parents[1]
S = B / "stage/767d610cb528"
baseline = json.loads((B / "baselines/767d610cb528.json").read_text(encoding="utf-8"))["files"]
paths = sorted((S / "docs/onboarding").rglob("*.md"))
prepared = []
for path in paths:
    relative = path.relative_to(S).as_posix()
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == baseline[relative], relative
    original = S / "docs/original" / relative
    assert not original.exists()
    link = os.path.relpath(S / "astraupskill/README.md", path.parent).replace("\\", "/")
    notice = f"> Historical documentation: this page describes the original implementation. Setup, storage, SDK evaluation, authorization, and the administration UI have changed. Start with the [current CRUD learning course]({link}); use this page for before/after comparison.\n\n"
    prepared.append((path, original, raw, notice))
for path, original, raw, notice in prepared:
    original.parent.mkdir(parents=True, exist_ok=True)
    original.write_bytes(raw)
    path.write_text(notice + raw.decode("utf-8"), encoding="utf-8")
print(json.dumps({"historicalPagesMarked": len(prepared), "originalCopiesHashVerified": True}))
