from pathlib import Path
import hashlib
import json

C = Path(__file__).resolve().parent
S = C.parents[1] / 'stage/71e7b036865c'
result = {'reviewed': True, 'run': 'browser-03',
          'notes': 'Viewed desktop screenshot and original-resolution narrow screenshot. Directory text, actions, navigation and six real fixture records are readable; the narrow layout fits without horizontal overflow.',
          'sha256': {name: hashlib.sha256((S / 'astraupskill/images' / name).read_bytes()).hexdigest() for name in ['desktop.png', 'narrow.png']}}
(C / 'images-reviewed.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print('Recorded the completed visual review.')
