from pathlib import Path
p=Path(__file__).with_name('browser_check.py');t=p.read_text(encoding='utf-8').replace('.read_text()',".read_text(encoding='utf-8')");p.write_text(t,encoding='utf-8')
s=Path(__file__).resolve().parents[2]/'stage/58c5c289a8ce'
p=s/'src/app/globals.css';t=p.read_text(encoding='utf-8');t+='\n@media(max-width: 600px) { .page-meta > select { grid-column: 1 / -1; } .page-meta > button { min-height: 38px; } }\n';p.write_text(t,encoding='utf-8')
