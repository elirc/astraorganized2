from pathlib import Path
import subprocess,json,re
B=Path(__file__).resolve().parent;S=B/'stage/cf8875344b43';C=B/'checks/andie';C.mkdir(parents=True,exist_ok=True)
r=subprocess.run(['node','--test','test/migration.test.js'],cwd=S,capture_output=True,text=True,timeout=60);(C/'tests.tap').write_text(r.stdout+r.stderr,encoding='utf-8');assert r.returncode==0,(r.stdout,r.stderr);assert '# pass 42' in r.stdout and '# fail 0' in r.stdout and '# skipped 0' in r.stdout
for rel in ['scripts/populate-metaobjects.js','scripts/lib/client.js','scripts/lib/planner.js']:
 r=subprocess.run(['node','--check',rel],cwd=S,capture_output=True,text=True,timeout=20);assert r.returncode==0,r.stderr
# Count matches without printing credential contents from either source or historical artifacts.
files=[p for p in S.rglob('*') if p.is_file() and p.suffix in ['.js','.json','.md']]
assert not any(re.search(r'shpat_[A-Za-z0-9]{16,}',p.read_text(encoding='utf-8')) for p in files),'Embedded token remains in delivery source'
result={'passed':True,'tests':42,'syntaxChecks':3,'embeddedTokenScan':'No Shopify token literals in staged source/docs/JSON','transport':'Controlled fetch boundaries plus one real loopback HTTP server; no live Shopify account requests or mutations','environment':'Node 22.16.0; dependency-free node:test','checks':['Offline CLI and import have no network side effects','Deterministic plans validate source and target snapshots','Paged reads, bounded retries, GraphQL/userErrors and unknown mutation outcomes','Stale/forged plans and conflicts stop before mutation','Partial create and journal failures preserve receipts and stop later work','Exclusive output files and local journal replacement','Source object immutability and explicit reference-field conflicts']}
(C/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))
