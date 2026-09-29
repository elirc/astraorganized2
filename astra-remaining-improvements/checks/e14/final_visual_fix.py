from pathlib import Path
p=Path(__file__).resolve().parents[2]/'stage/ca549816cdd1/app/web/styles.css'
text=p.read_text();old='position:sticky;top:12px;z-index:2;';assert old in text
p.write_text(text.replace(old,'position:relative;'),encoding='utf-8')
print('Status feedback now flows beside the active form without covering controls')
