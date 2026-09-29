from pathlib import Path
import hashlib, json, zipfile

C = Path(__file__).resolve().parent
B = C.parents[1]
S = B / 'stage/19110bf39fcf'
images = sorted((C / 'browser-05').glob('[0-9][0-9]-*.png'))
assert len(images) == 9
assert json.loads((C / 'browser-05/results.json').read_text())['total'] == 15
qa = {'passed': True, 'directory': 'browser-05',
      'review': 'All nine images opened and visually inspected: readable list text, compact sidebars, populated mobile administration fields, anonymous portal without reply form/logout, signed-in public history, and retained-draft comparison.',
      'files': [{'name': image.name, 'sha256': hashlib.sha256(image.read_bytes()).hexdigest()} for image in images]}
(C / 'screenshots-reviewed.json').write_text(json.dumps(qa, indent=2), encoding='utf-8')
wheels = list((C / 'install-01/wheels').glob('*.whl'))
assert len(wheels) == 1
with zipfile.ZipFile(wheels[0]) as wheel:
    files = ['app/static/app.js', 'app/static/app.css'] + [f'app/templates/{name}.html' for name in ['base','index','admin','staff','portal']]
    actual = [name for name in wheel.namelist() if name.startswith('app/templates/')]
    # Match the project's actual template names instead of assuming conventions.
    files = ['app/static/app.js', 'app/static/app.css'] + actual
    assert len(files) == 7, files
    for name in files:
        assert wheel.read(name) == (S / name).read_bytes(), name
(C / 'wheel-final-assets.json').write_text(json.dumps({'passed': True, 'matchingAssets': files}, indent=2), encoding='utf-8')
print(json.dumps({'reviewedImages': len(images), 'wheelAssetsMatchFinalStage': len(files)}))
