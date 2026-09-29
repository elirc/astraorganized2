from pathlib import Path
import codecs,os
B=Path('astrafinalplan/implementation/batch04')
def repair(error):return (error.object[error.start:error.end].decode('cp1252'),error.end)
codecs.register_error('local_punctuation',repair)
fixed=[]
for parent,dirs,files in os.walk(B/'stage'):
 dirs[:]=[d for d in dirs if d not in ['node_modules','dist','.git']]
 for name in files:
  p=Path(parent)/name
  if p.suffix not in ['.ts','.tsx','.js','.jsx','.md','.json','.css','.sql']:continue
  raw=p.read_bytes()
  try:raw.decode('utf-8')
  except UnicodeDecodeError:
   p.write_bytes(raw.decode('utf-8',errors='local_punctuation').encode('utf-8'));fixed.append(str(p))
print('Normalized new punctuation in',len(fixed),'files')
