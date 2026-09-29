"""Run the prepared Umbraco regression after the existing .NET check finishes."""
from pathlib import Path
import json
import subprocess
import sys
import time

base = Path(__file__).resolve().parent.parent
previous = base / 'checks/7115d7be5ffc/astra-netopen5-latest-tests-r1.json'
while json.loads(previous.read_text())['status'] == 'running':
    time.sleep(5)
raise SystemExit(subprocess.call([
    sys.executable, str(base / 'run_project_check.py'), '--cwd', 'Umbraco-CMS',
    'b8fb41bd6255', 'astra-netopen3-template-tests-r1', '--',
    'dotnet', 'test', 'tests/Umbraco.Tests.UnitTests/Umbraco.Tests.UnitTests.csproj',
    '--filter', 'FullyQualifiedName~SearchTemplateItemControllerTests',
    '--nologo', '--verbosity', 'minimal', '/m:1', '--logger', 'trx',
]))
