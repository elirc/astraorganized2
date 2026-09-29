from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[2]/'stage/af19f6e32dba'
package=root/'.artifacts/publish'
checks=[]
assert (package/'Billing.Api.dll').is_file()
for source in (root/'src/Billing.Web/dist').rglob('*'):
    if source.is_file():
        dest=package/'wwwroot'/source.relative_to(root/'src/Billing.Web/dist')
        assert dest.is_file() and hashlib.sha256(source.read_bytes()).digest()==hashlib.sha256(dest.read_bytes()).digest(),source
checks.append('Published browser assets exactly match the final Vite build')
assert not any(p.is_file() and (p.suffix in {'.sqlite','.db'} or 'App_Data' in p.parts) for p in package.rglob('*'))
checks.append('Published package contains no application database or App_Data files')
for rel in ['src/Billing.Api/packages.lock.json','tests/Billing.Tests/packages.lock.json','src/Billing.Web/package-lock.json']:
    assert (root/rel).is_file()
checks.append('Backend, test and frontend dependency lock files exist')
out={'passed':True,'checks':checks}
(Path(__file__).parent/'package-checks.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out))
