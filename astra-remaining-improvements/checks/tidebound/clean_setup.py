from pathlib import Path
import hashlib
import json
import subprocess
import time

C = Path(__file__).resolve().parent
S = (C.parents[1] / 'stage/4de416cd300b').resolve()
output = C / 'clean-setup-01'
assert not output.exists()
output.mkdir()
node_modules = S / 'node_modules'
assert node_modules.resolve().parent == S and not node_modules.is_symlink() and not node_modules.is_junction()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def assets():
    return {p.relative_to(S / 'dist').as_posix(): sha(p) for p in sorted((S / 'dist').rglob('*')) if p.is_file()}
before = assets()
assert before
lock = sha(S / 'package-lock.json')
commands = [
    ['npm.cmd', 'ci', '--no-audit', '--no-fund', '--cache=' + str(C / 'npm-cache')],
    ['npm.cmd', 'run', 'build'],
]
results = []
try:
    for index, command in enumerate(commands, 1):
        start = time.monotonic()
        with (output / f'{index}.log').open('w', encoding='utf-8') as log:
            run = subprocess.run(command, cwd=S, stdout=log, stderr=subprocess.STDOUT)
        result = {'command': command, 'exitCode': run.returncode, 'seconds': round(time.monotonic() - start, 2)}
        results.append(result)
        print(json.dumps(result), flush=True)
        if run.returncode:
            raise RuntimeError('Clean setup command failed: ' + ' '.join(command))
    after = assets()
    assert after == before, 'Clean build differs from the browser-tested package; investigate and reverify it.'
    assert sha(S / 'package-lock.json') == lock, 'Clean installation changed the lockfile.'
    evidence = {'passed': True, 'commands': results, 'normalInstallScriptsEnabled': True, 'lockSha256': lock,
                'browserPackageMatchesCleanBuild': True, 'assets': after}
    print(f'Clean build matches all {len(after)} browser-tested assets.', flush=True)
except Exception as error:
    evidence = {'passed': False, 'commands': results, 'error': str(error), 'browserTestedAssets': before}
    raise
finally:
    (output / 'results.json').write_text(json.dumps(evidence, indent=2), encoding='utf-8')
