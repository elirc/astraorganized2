"""Remove reproducible node_modules only from verified, delivered staging copies."""
from pathlib import Path
import json
import os
import shutil

base = Path(__file__).resolve().parent.parent
stage = (base / 'stage').resolve()
state = json.loads((Path(__file__).parent / 'state.json').read_text())
delivered = {item['id'] for item in state['projects'] if item['status'] == 'delivered'}
for identifier in ['1bf7dd59f47b', '46f416b83060', '37844e1ec56d', '5be7edf43612', 'af5130b3aad2']:
    assert identifier in delivered
    project = (stage / identifier).resolve()
    assert project.parent == stage
    targets = []
    for directory, dirs, _ in os.walk(project):
        if 'node_modules' in dirs:
            target = (Path(directory) / 'node_modules').resolve()
            assert target.is_relative_to(project) and target.name == 'node_modules'
            targets.append(target)
            dirs.remove('node_modules')
        dirs[:] = [name for name in dirs if name not in {'.git', 'astraupskill', '.next', 'dist', 'bin', 'obj'}]
    for target in targets:
        assert target.is_relative_to(project) and target != project
        print('Removing disposable staged dependencies: ' + str(target), flush=True)
        # Resolve and validate before adding Windows' long-path prefix.
        deletion_path = '\\\\?\\' + str(target) if os.name == 'nt' else str(target)
        shutil.rmtree(deletion_path)
print('Free bytes: ' + str(shutil.disk_usage(stage).free), flush=True)
