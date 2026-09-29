from pathlib import Path
S=Path(__file__).resolve().parents[2]/'stage/ca549816cdd1'
p=S/'app/web/index.html'
text=p.read_text(encoding='utf-8')
assert '\u00e2\u20ac' in text or '\u00e2\u2020' in text
fixed=text.encode('cp1252').decode('utf-8')
assert '\u2192' in fixed and '\u2197' in fixed
p.write_text(fixed,encoding='utf-8')
print('Repaired HTML encoding after a Windows default-codepage helper read')
