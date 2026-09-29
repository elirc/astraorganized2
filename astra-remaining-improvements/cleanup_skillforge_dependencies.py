from pathlib import Path
import json,shutil
b=Path('astra-remaining-improvements').resolve();delivery=json.loads((b/'deliveries/a9672affc47e.json').read_text(encoding='utf-8'));assert delivery['status']=='delivered';target=(b/'stage/a9672affc47e/node_modules').resolve();assert target.is_relative_to(b/'stage') and target.name=='node_modules';print('Removing reproducible completed staging dependencies:',target,flush=True);shutil.rmtree('\\\\?\\'+str(target));print('Free GiB',round(shutil.disk_usage(b).free/1024**3,2))
