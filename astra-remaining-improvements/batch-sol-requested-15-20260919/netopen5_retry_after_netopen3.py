"""Retry the focused Jellyfin check after Umbraco releases the build slot."""
from pathlib import Path
import json
import subprocess
import sys
import time

base = Path(__file__).resolve().parent.parent
previous = base / 'checks/b8fb41bd6255/astra-netopen3-template-tests-r2.json'
while not previous.exists() or json.loads(previous.read_text())['status'] == 'running':
    time.sleep(5)
raise SystemExit(subprocess.call([sys.executable, str(base / 'run_project_check.py'),
    '--cwd', 'jellyfin', '7115d7be5ffc', 'astra-netopen5-latest-tests-r3', '--',
    'dotnet', 'test', 'tests/Jellyfin.Api.Tests/Jellyfin.Api.Tests.csproj', '--no-restore',
    '--filter', 'FullyQualifiedName~UserLibraryLatestMediaTests', '--nologo',
    '--verbosity', 'minimal', '/m:1', '--logger', 'trx']))
