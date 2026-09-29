from pathlib import Path
import re
B=Path(__file__).resolve().parent
original=(B.parent/'write_learning.py').read_text(encoding='utf-8')
body=original[original.index('def source('):]
body=body.replace('for i,c in enumerate(COURSES,1):','for i,c in enumerate(COURSES,11):').replace('name=NAMES[i-1]','name=NAMES[i-11]')
body=re.sub(r'^ testcmd=.*$'," testcmd=c['testcmd']",body,flags=re.M)
body=re.sub(r'^ setup=.*$'," setup=c['setup']",body,flags=re.M)
a=body.index(" dbguide='''");b=body.index(" write(n,'04-TESTING-AND-DEBUGGING.md'",a)
body=body[:a]+" dbguide=c['dbguide']\n"+body[b:]
header="from pathlib import Path\nimport json,re\nBASE=Path(__file__).resolve().parent/'stage'\nNAMES=json.loads((BASE.parent/'projects.json').read_text(encoding='utf-8'))\nCOURSES=json.loads((BASE.parent/'courses.json').read_text(encoding='utf-8'))\n"
(B/'write_learning.py').write_text(header+body,encoding='utf-8')
print('Adapted the proven course templates for projects 11-20 with project-specific setup.')
