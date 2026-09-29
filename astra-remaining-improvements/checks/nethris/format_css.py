from pathlib import Path

path = Path(__file__).resolve().parents[2] / 'stage/71e7b036865c/client/src/workshop.css'
source = path.read_text(encoding='utf-8')
source += '\n.field { margin-bottom: 15px; }\n.field > label { margin-bottom: 6px; }\n.org-panel { overflow-x: auto; }\n'
lines = []; part = ''; depth = 0
def emit():
    global part
    if part.strip():
        lines.append('  ' * depth + part.strip())
    part = ''
for char in source:
    if char == '{':
        part = part.strip() + ' {'; emit(); depth += 1
    elif char == '}':
        emit(); depth -= 1; lines.append('  ' * depth + '}')
    elif char == ';':
        part += char; emit()
    else:
        part += char
emit()
assert depth == 0
path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('Formatted stylesheet and added stable field spacing / bounded org scrolling.')
