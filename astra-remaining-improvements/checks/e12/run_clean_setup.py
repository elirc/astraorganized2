"""Verify the documented no-install setup in a fresh finite source copy."""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import socket
import subprocess
import time
import urllib.request

C = Path(__file__).resolve().parent
B = C.parents[1]
S = B / "stage/767d610cb528"
O = C / "clean-01"
W = O / "workspace"
W.mkdir(parents=True, exist_ok=False)
files = [S / "package.json"]
for folder in ["src", "sdk", "test", "verification"]:
    files.extend(path for path in (S / folder).rglob("*") if path.is_file() and path.suffix in {".js", ".html", ".css"})
for source in files:
    target = W / source.relative_to(S)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)

gates = []
def command(name, argv, *, env=None, sensitive=False):
    start = time.time()
    result = subprocess.run(argv, cwd=W, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if not sensitive:
        (O / f"{name}.log").write_text(result.stdout + result.stderr, encoding="utf-8")
    gates.append({"name": name, "command": argv, "exitCode": result.returncode, "seconds": round(time.time()-start, 2), "stdoutOmitted": sensitive})
    print(json.dumps(gates[-1]), flush=True)
    return result

result = command("tests", [shutil.which("npm.cmd") or "npm", "test"])
assert result.returncode == 0
assert re.search(r"# tests 98\b", result.stdout) and re.search(r"# pass 98\b", result.stdout)
data = W / "data/owner.json"
env = {**os.environ, "FEATURE_FLAGS_DATA_FILE": str(data)}
setup = command("owner-setup", ["node", "src/server/setup.js", "owner", "Clean verification owner", "owner@example.invalid"], env=env, sensitive=True)
assert setup.returncode == 0
token = setup.stdout.strip().splitlines()[-1]
assert re.fullmatch(r"[a-f0-9]{64}", token)
digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
before = digest(data)
refusal = command("owner-refuses-overwrite", ["node", "src/server/setup.js", "owner", "Replacement", "replacement@example.invalid"], env=env, sensitive=True)
assert refusal.returncode != 0 and digest(data) == before
assert not (W / "data/state.json").exists()
with socket.socket() as reservation:
    reservation.bind(("127.0.0.1", 0))
    port = reservation.getsockname()[1]
env["PORT"] = str(port)
start = time.time()
with (O / "server.log").open("w", encoding="utf-8") as log:
    process = subprocess.Popen(["node", "src/server/server.js"], cwd=W, env=env, stdout=log, stderr=subprocess.STDOUT)
    try:
        base = f"http://127.0.0.1:{port}"
        deadline = time.monotonic() + 90
        while True:
            try:
                with urllib.request.urlopen(base, timeout=5) as response:
                    assert response.status == 200
                break
            except OSError:
                if process.poll() is not None or time.monotonic() >= deadline:
                    raise
                time.sleep(0.2)
        for route, file in [("/", "index.html"), ("/app.js", "app.js"), ("/styles.css", "styles.css")]:
            with urllib.request.urlopen(base + route, timeout=10) as response:
                assert response.read() == (W / "src/ui" / file).read_bytes()
        request = urllib.request.Request(base + "/api/admin/bootstrap", headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(request, timeout=10) as response:
            bootstrap = json.load(response)
        assert bootstrap["actor"]["name"] == "Clean verification owner"
        assert len(bootstrap["tokens"]) == 1 and "hash" not in bootstrap["tokens"][0]
        assert digest(data) == before
        gates.append({"name": "cli-startup-assets-and-owner-authentication", "passed": True, "staticAssets": 3, "seconds": round(time.time()-start, 2)})
    finally:
        process.terminate()
        try:
            process.wait(timeout=20)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=20)
evidence = {"passed": True, "backendTestsRepeated": 98, "noNpmDependencies": True, "sourceFilesCopied": len(files), "sourceHashes": {path.relative_to(S).as_posix(): digest(path) for path in files}, "gates": gates}
(O / "results.json").write_text(json.dumps(evidence, indent=2), encoding="utf-8")
print(json.dumps({"passed": True, "backendTestsRepeated": 98, "setupRefusedOverwrite": True, "assetsVerified": 3}), flush=True)
