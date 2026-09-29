from pathlib import Path
import json
import subprocess
import sys
import time

C = Path(__file__).resolve().parent
S = C.parents[1] / "stage/44013f102ff1"
name = sys.argv[1]
assert name in {"baseline", "settings-before", "settings-after", "ipc-after", "practice-after", "final-01"}
assert not (C / f"{name}.json").exists()
files = sorted(str(path.relative_to(S)) for path in (S / "test").glob("*.test.js"))
if name.startswith("settings-"):
    files = ["test/settings-safety.test.js"]
command = ["node", "--require", str(C / "guard-fixtures.cjs"), "--test", *files]
started = time.time()
with (C / f"{name}.log").open("w", encoding="utf-8") as log:
    result = subprocess.run(command, cwd=S, stdout=log, stderr=subprocess.STDOUT)
evidence = {"command": command, "exitCode": result.returncode, "seconds": round(time.time()-started, 2)}
(C / f"{name}.json").write_text(json.dumps(evidence, indent=2), encoding="utf-8")
print(json.dumps(evidence), flush=True)
print((C / f"{name}.log").read_text(encoding="utf-8")[-10000:], flush=True)
sys.exit(result.returncode)
