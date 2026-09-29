"""Run one immutable recorded check in an owned staged project."""

from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import time


project_id, label, *command = sys.argv[1:]
owned = {
    "5be7edf43612",
    "af5130b3aad2",
    "3b9c30ec3ce2",
    "a81b176807e5",
    "9d3b119f40a0",
}
assert project_id in owned
assert label.startswith("sol15-")
assert all(character.isalnum() or character in "-_" for character in label)
assert command

base = Path(__file__).resolve().parent.parent
cwd = base / "stage" / project_id
output = base / "checks" / project_id
output.mkdir(parents=True, exist_ok=True)
log = output / f"{label}.log"
record = output / f"{label}.json"
assert not log.exists() and not record.exists(), "Use a fresh label; evidence is immutable"

result = {
    "command": command,
    "cwd": str(cwd),
    "startedAt": datetime.now(timezone.utc).isoformat(),
    "status": "running",
    "log": log.name,
}
record.write_text(json.dumps(result, indent=2), encoding="utf-8")
started = time.monotonic()
try:
    with log.open("wb") as stream:
        process = subprocess.Popen(command, cwd=cwd, stdout=stream, stderr=subprocess.STDOUT)
        result["pid"] = process.pid
        record.write_text(json.dumps(result, indent=2), encoding="utf-8")
        exit_code = process.wait()
    result.update(status="complete", exitCode=exit_code, passed=exit_code == 0)
except OSError as error:
    exit_code = 1
    result.update(status="launch-failed", passed=False, error=str(error))
result.update(
    finishedAt=datetime.now(timezone.utc).isoformat(),
    elapsedSeconds=round(time.monotonic() - started, 2),
)
record.write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result), flush=True)
raise SystemExit(exit_code)
