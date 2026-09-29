from pathlib import Path
import base64
import hashlib
import io
import json
import tarfile
import urllib.request

C = Path(__file__).resolve().parent
destination = C / 'tooling/npm-11.19.1'
assert not destination.exists()
with urllib.request.urlopen('https://registry.npmjs.org/npm/11.19.1', timeout=60) as response:
    metadata = json.load(response)
url = metadata['dist']['tarball']
assert url == 'https://registry.npmjs.org/npm/-/npm-11.19.1.tgz'
with urllib.request.urlopen(url, timeout=120) as response:
    archive = response.read()
actual = 'sha512-' + base64.b64encode(hashlib.sha512(archive).digest()).decode()
assert actual == metadata['dist']['integrity']
destination.mkdir(parents=True)
with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as tar:
    for member in tar.getmembers():
        assert (destination / member.name).resolve().is_relative_to(destination.resolve()), member.name
        assert not member.issym() and not member.islnk(), member.name
    tar.extractall(destination, filter='data')
result = {'version': metadata['version'], 'url': url, 'integrity': actual, 'bytes': len(archive), 'path': str(destination), 'engines': metadata['engines']}
(C / 'npm-cli-install.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result), flush=True)
