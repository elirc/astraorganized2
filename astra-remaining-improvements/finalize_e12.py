"""Create e12's finite delivery only after completed checks and image review."""
from pathlib import Path
import ast
import hashlib
import json
import re
import shutil
import subprocess

B = Path(__file__).resolve().parent
S = B / "stage/767d610cb528"
C = B / "checks/e12"
read = lambda path: json.loads(path.read_text(encoding="utf-8"))
digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
baseline_record = read(B / "baselines/767d610cb528.json")
baseline = baseline_record["files"]
canonical = B.parent.parent / baseline_record["project"]
assert read(C / "final-01.json")["exitCode"] == 0
backend_log = (C / "final-01.log").read_text(encoding="utf-8")
assert re.search(r"# tests 98\b", backend_log) and re.search(r"# pass 98\b", backend_log)
browser = read(C / "browser-02/results.json")
assert browser["passed"] and len(browser["checks"]) == 20 and all(item["passed"] for item in browser["checks"])
clean = read(C / "clean-01/results.json")
assert clean["passed"] and clean["backendTestsRepeated"] == 98
for relative, expected in clean["sourceHashes"].items():
    assert digest(S / relative) == expected, relative
assert digest(S / "data/state.json") == digest(canonical / "data/state.json") == baseline["data/state.json"]

# These five specific images were opened and visually inspected in this turn.
reviewed = ["01-desktop.png", "02-conflict-review.png", "03-variant-editor.png", "04-viewer.png", "05-mobile.png"]
assert browser["screenshots"] == reviewed
qa = {"passed": True, "directory": "browser-02", "review": "All five images opened: readable desktop forms, literal hostile text, retained-draft comparison, variant JSON, viewer restrictions, and stacked mobile layout. Subsequent CSS only adds long-heading wrapping and full-width metadata.", "files": []}
images = S / "astraupskill/images"
images.mkdir(exist_ok=True)
for name in reviewed:
    source = C / "browser-02" / name
    qa["files"].append({"name": name, "sha256": digest(source)})
    shutil.copyfile(source, images / name)
(C / "screenshots-reviewed.json").write_text(json.dumps(qa, indent=2), encoding="utf-8")

syntax = subprocess.run(["node", "--check", "src/ui/app.js"], cwd=S, capture_output=True, text=True)
assert syntax.returncode == 0, syntax.stderr
ast.parse((S / "verification/verify_browser.py").read_text(encoding="utf-8"))
evidence = {
    "passed": True, "total": 118, "backend": 98, "browser": 20,
    "counting": "98 backend identities plus 20 browser workflows. Clean-copy backend tests repeat the same cases and are not added again. Setup/syntax/assets are additional gates, not inflated test totals.",
    "backendExecution": read(C / "final-01.json"),
    "browserExecution": {"command": ["python", "verification/verify_browser.py", "<new-evidence-directory>"], "seconds": browser["seconds"], "checks": browser["checks"]},
    "cleanSetup": {key: value for key, value in clean.items() if key != "sourceHashes"},
    "syntax": {"command": ["node", "--check", "src/ui/app.js"], "exitCode": syntax.returncode, "pythonBrowserScriptParsed": True},
    "screenshotsReviewed": 5,
    "originalDataPreserved": {"file": "data/state.json", "sha256": baseline["data/state.json"]},
    "limits": ["Loopback local JSON store; no distributed persistence or power-loss guarantee.", "No durable mutation receipts, metrics deduplication/automatic pruning, or account recovery.", "Basic persisted shape/identity validation; no complete relational migration validation or duplicate-JSON-key rejection.", "Chromium desktop/mobile checks, not all-browser or assistive-technology certification."],
}
(C / "results.json").write_text(json.dumps(evidence, indent=2), encoding="utf-8")
(S / "verification/validated-results.json").write_text(json.dumps(evidence, indent=2), encoding="utf-8")

verification = S / "astraupskill/VERIFICATION.md"
content = verification.read_text(encoding="utf-8")
start = content.index("This file explains")
end = content.index("## Reproduce the backend checks")
content = content[:start] + """The completed implementation has **118 distinct passing checks**: 98 backend tests and 20 real Chromium workflows. The [machine-readable results](../verification/validated-results.json) record commands, outcomes, workflow names, setup gates, and preservation evidence. Repeated focused/full/clean-copy cases are counted once.

The full backend run passed all98 cases. It covers typed contracts, current-token authorization, project scoping, reference-safe resource deletion, protected-environment acknowledgment, metrics batches/limits, request snapshots, durable-write ordering and failure injection, SDK/context behavior, and seed isolation. A later fresh source copy ran the documented `npm test` script and passed the same98 cases after source formatting, with no npm installation or runtime package dependencies.

The final browser run passed all20 workflows in92.54seconds against an isolated synthetic dataset. It exercised the eight resource editors, hostile text rendered literally, pagination/search, stale edits preserving changed fields, refreshing unedited fields, explicit protected acknowledgment, malformed JSON with a retained draft, one-time token display/revocation, an accepted creation whose response was lost, server500 review, member/viewer controls, context evaluation, and mobile layout. No uncaught browser JavaScript errors were observed. The first run correctly rejected an invalid role in the test fixture; the fixture was corrected rather than weakening application authorization.

Fresh-copy setup issued a new owner token without logging its plaintext, refused a second initialization without changing the file, started the actual CLI server, authenticated the owner, and served all three UI assets byte-for-byte from that copy. The original `data/state.json` was independently hash-checked against its baseline and is excluded from delivery. Frontend JavaScript syntax and the Python browser script's syntax were checked. Ten older onboarding pages retain historical notices and exact original copies.

All five final workflow screenshots were opened and reviewed. The tested desktop and390-pixel mobile layouts are readable; the mobile workflow also checks page width. Subsequent CSS adds wrapping for long editor headings and gives token metadata the full form width; these limited presentation changes do not alter the checked CRUD behavior. Screenshot coverage is representative, not a claim that every possible input or viewport was inspected.

| Reviewed view | Image |
| --- | --- |
| Desktop list and new-flag form | [Desktop workspace](images/01-desktop.png) |
| Retained draft and latest accepted record | [Conflict review](images/02-conflict-review.png) |
| Typed variant payload editor | [Variant editor](images/03-variant-editor.png) |
| Read-only actor's inspection view | [Viewer workspace](images/04-viewer.png) |
| Stacked layout at390pixels | [Mobile workspace](images/05-mobile.png) |

""" + content[end:]
for before, after in [("all98", "all 98"), ("same98", "same 98"), ("all20", "all 20"), ("in92.54seconds", "in 92.54 seconds"), ("and390-pixel", "and 390-pixel"), ("at390pixels", "at 390 pixels"), ("server500", "server 500")]:
    content = content.replace(before, after)
verification.write_text(content, encoding="utf-8")

changed = []
for path in S.rglob("*"):
    if not path.is_file():
        continue
    parts = path.relative_to(S).parts
    relative = path.relative_to(S).as_posix()
    if any(part in {"__pycache__", ".venv", "node_modules"} for part in parts):
        continue
    if parts[0] not in {"src", "sdk", "test", "verification", "docs", "astraupskill"} and relative not in {"README.md", "package.json", ".gitignore"}:
        continue
    if relative.startswith("astraupskill/") and len(parts) == 2 and path.suffix == ".md":
        continue
    if path.suffix in {".pyc", ".db", ".log"}:
        continue
    if baseline.get(relative) != digest(path):
        changed.append(relative)
spec = {
    "changedFiles": sorted(changed),
    "summary": [
        "Implemented typed, authorized CRUD for projects, environments, flags, strategies, segments, variants and dependencies, with protected-change acknowledgment, reference-safe deletion, current-token checks and retained audit history.",
        "Replaced unsafe direct persistence with bounded validated JSON, per-write leases, revision/digest conflict detection, isolated request snapshots, atomic file replacement before memory publication, explicit owner/demo setup and preserved original data.",
        "Corrected context evaluation and SDK refresh behavior, fail-closed constraints/variants, scoped metrics batches and limits, HTTP input/origin/host boundaries, and mutable seed isolation.",
        "Rebuilt the administration UI with eight resource editors, explicit in-memory sign-in, typed PATCH drafts, search/pagination, stale/uncertain-write review, one-time token display and mobile layout.",
        "Added nine detailed learning guides, worked defects, exercises/solutions, request trace labs, preserved historical sources/docs, reproducible browser verification and reviewed screenshots."
    ],
    "checks": {"format": "json", "resultsFile": "checks/e12/results.json", "expectedTests": 118},
    "limits": evidence["limits"] + ["SDK response JSON has no streaming byte cap; finite Date.parse validation is not strict calendar validation.", "One-time token secrets cannot be recovered after a lost creation response; inspect and revoke/recreate as appropriate."]
}
(B / "specs/767d610cb528.json").write_text(json.dumps(spec, indent=2), encoding="utf-8")
print(json.dumps({"ready": True, "changedFilesBeforeCourse": len(changed), "checks": 118, "screenshots": 5, "originalDataPreserved": True}), flush=True)
