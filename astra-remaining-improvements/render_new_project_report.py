from report_evidence import check_summary
"""The requested astradocs report: applied work only, with per-project evidence."""
from pathlib import Path
from urllib.parse import quote, unquote
from datetime import datetime, timezone
import json
import re

B = Path(__file__).resolve().parent
R = B.parent
progress = json.loads((B / "progress.json").read_text(encoding="utf-8"))
finished = [item for item in progress["projects"] if item["status"] == "complete"]
manifests = []
for item in finished:
    manifest = json.loads((B / "deliveries" / f'{item["id"]}.json').read_text(encoding="utf-8"))
    assert manifest["status"] == "delivered" and manifest["project"] == item["path"]
    manifests.append(manifest)
manifests.sort(key=lambda item: item.get("deliveredAt", ""))
staged = [item for item in progress["projects"] if item["status"] != "complete" and (B / "stage" / item["id"]).is_dir()]
target = R / "astradocs/NEW_PROJECTS_CHANGE_REPORT.md"
lines = ["# New project improvements: per-project change report", "",
         f"Updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}", "",
         f"**{len(finished)} of {progress['total']} eligible project families are delivered; {progress['total'] - len(finished)} remain.** The overall improvement program is still in progress.", "",
         "This report covers new deliveries from the remaining-project program, outside its recorded exclusions. Each entry summarizes changes applied in that project's original folder and links to its learning course and delivery evidence. Proposed exercises and unfinished staged work are not counted as completed features.", "",
         f"Delivered learning material: **{sum(item['courseFiles'] for item in manifests)} guides**, **{sum(item['courseWords'] for item in manifests):,} words**. Verification counts below are recorded per-project checks; repeated runs are not added again where the manifest identifies them as repeats.", "",
         "## Latest completed project", ""]
if manifests:
    latest = manifests[-1]
    lines += [f"**{latest['project']}** — {len(latest['files'])} delivered files and {latest['courseFiles']} learning guides. Verification: {check_summary(latest)}.", ""]
lines += ["## Changes made to each completed project", ""]
for index, manifest in enumerate(manifests, 1):
    course = quote('../../' + manifest['project'] + '/astraupskill/README.md', safe='/+')
    evidence = f"../astra-remaining-improvements/deliveries/{manifest['id']}.json"
    lines += [f"### {index}. {manifest['project']}", ""]
    lines += ["- " + summary for summary in manifest["summary"]]
    lines += ["", f"**Learning:** [{manifest['courseFiles']} guides]({course}), {manifest['courseWords']:,} words. **Verification:** {check_summary(manifest)}. **Applied:** {len(manifest['files'])} files. [Detailed evidence and limitations]({evidence}).", ""]
lines += ["## Started but not delivered", ""]
if staged:
    lines += ["These copies are being reviewed or improved. Their staged files are not a completed delivery to the original project folder.", ""]
    lines += [f"- `{item['path']}`" for item in staged]
else:
    lines += ["No additional staged project is currently recorded."]
lines += ["", "## Scope and evidence", "",
          "The [full completion ledger and remaining queue](../astrdocs/REMAINING_PROJECTS_IMPLEMENTATION_REPORT.md) lists every eligible family. [Scope and exclusions](../astra-remaining-improvements/scope.json) preserve the original boundary; [machine-readable progress](../astra-remaining-improvements/progress.json) records delivery status.", "",
          "Delivery manifests record finite file lists, before/after hashes, verification outcomes, and known limits. Backups are retained under `astra-remaining-improvements/backups`. This report reads those delivery records; it is not a fresh rerun of every historical test or a claim of production certification. Existing application data is preserved unless a project's evidence explicitly describes a tested migration.", ""]
content = '\n'.join(lines)
for link in re.findall(r'\]\(([^)]+)\)', content):
    if re.match(r'[a-z]+:|#', link, re.I):
        continue
    assert (target.parent / unquote(link.split('#')[0])).exists(), link
target.parent.mkdir(exist_ok=True)
target.write_text(content, encoding="utf-8")
print(json.dumps({"report": str(target), "delivered": len(finished), "remaining": progress["total"] - len(finished), "projectEntries": len(manifests), "staged": len(staged), "linksVerified": True}), flush=True)
