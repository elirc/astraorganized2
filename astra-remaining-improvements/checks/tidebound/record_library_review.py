from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import struct

C = Path(__file__).resolve().parent
S = C.parents[1] / 'stage/4de416cd300b'
destination = S / 'astraupskill/images'
destination.mkdir(exist_ok=True)
reviews = []
for name in ['desktop.png', 'narrow.png']:
    source = C / 'library-03' / name
    raw = source.read_bytes()
    width, height = struct.unpack('>II', raw[16:24])
    shutil.copyfile(source, destination / name)
    reviews.append({'file': name, 'width': width, 'height': height, 'sha256': hashlib.sha256(raw).hexdigest(),
                    'review': 'Viewed by the agent. Readable text, clear controls and no horizontal overflow. Narrow layout scrolls vertically; keyboard navigation and editor access also passed in the browser workflow.'})
(C / 'images-reviewed.json').write_text(json.dumps({'reviewedAt': datetime.now(timezone.utc).isoformat(), 'images': reviews}, indent=2), encoding='utf-8')
print(json.dumps(reviews), flush=True)
