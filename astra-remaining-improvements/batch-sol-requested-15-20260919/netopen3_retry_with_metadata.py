"""Supply original checkout metadata to the isolated source-copy test build."""
from pathlib import Path
import json
import subprocess
import sys
import time

base = Path(__file__).resolve().parent.parent
previous = base / 'checks/7115d7be5ffc/astra-netopen5-latest-tests-r2.json'
while not previous.exists() or json.loads(previous.read_text())['status'] == 'running':
    time.sleep(5)
canonical = base.parent.parent / 'netopen3/Umbraco-CMS'
commit = subprocess.check_output(['git', '-C', str(canonical), 'rev-parse', '--short', 'HEAD'], text=True).strip()
assert commit and all(character in '0123456789abcdef' for character in commit)
print('Using canonical checkout GitCommitIdShort=' + commit, flush=True)
raise SystemExit(subprocess.call([sys.executable, str(base / 'run_project_check.py'),
    '--cwd', 'Umbraco-CMS', 'b8fb41bd6255', 'astra-netopen3-template-tests-r2', '--',
    'dotnet', 'test', 'tests/Umbraco.Tests.UnitTests/Umbraco.Tests.UnitTests.csproj', '--no-restore',
    '--filter', 'FullyQualifiedName~SearchTemplateItemControllerTests', '--nologo',
    '--verbosity', 'minimal', '/m:1', '/p:GitCommitIdShort=' + commit, '--logger', 'trx']))
