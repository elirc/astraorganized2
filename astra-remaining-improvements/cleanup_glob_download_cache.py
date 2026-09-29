from pathlib import Path
import shutil
b=Path('astra-remaining-improvements').resolve();target=(b/'npm-cache/_cacache').resolve();assert target.is_relative_to(b) and target.name=='_cacache';print('Removing reproducible package download cache only:',target,flush=True);shutil.rmtree('\\\\?\\'+str(target));print('Free GiB',round(shutil.disk_usage(b).free/1024**3,2))
