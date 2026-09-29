from pathlib import Path
import hashlib, json, urllib.request, zipfile
B=Path(__file__).resolve().parent
D=B/'toolchains/go1.27.1';D.mkdir(parents=True,exist_ok=True)
archive=D/'go1.27.1.windows-amd64.zip'
url='https://go.dev/dl/go1.27.1.windows-amd64.zip'
expected='a3911b5e0e1b1053f25ed0675f4c1c6aad1e2bfcf253df2b9be4caabd2edd95d'
if not archive.exists():
    with urllib.request.urlopen(url,timeout=60) as response, archive.open('wb') as target:
        size=0
        while chunk:=response.read(1024*1024):
            size+=len(chunk)
            if size>256*1024*1024:raise RuntimeError('Unexpected archive size')
            target.write(chunk)
digest=hashlib.sha256(archive.read_bytes()).hexdigest()
assert digest==expected,('Go archive checksum mismatch',digest)
with zipfile.ZipFile(archive) as z:
    for info in z.infolist():
        target=(D/info.filename).resolve()
        assert target.is_relative_to(D.resolve()),info.filename
    z.extractall(D)
record={'source':url,'publishedChecksumSource':'https://go.dev/dl/','sha256':digest,'verified':True,'executable':str(D/'go/bin/go.exe')}
(D/'verification.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps(record))
