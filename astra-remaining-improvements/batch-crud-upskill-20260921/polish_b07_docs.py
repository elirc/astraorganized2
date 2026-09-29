from pathlib import Path
import re
B=Path(__file__).resolve().parent.parent
markers={'482e93488b83':'Runtime review addition:','5f8d9a364788':'Additional runtime coverage','cd5a8a522511':'Review extension:','1754dbb384b1':'The extended lab also','f1f996eeb9e7':'Astra review extension:'}
for id,marker in markers.items():
 for p in (B/'stage'/id/'astraupskill').glob('*.md'):
  s=p.read_text(encoding='utf-8')
  if p.name!='VERIFICATION.md':s=re.sub(r'\n'+re.escape(marker)+r'[^\n]*\n','\n',s)
  if id=='f1f996eeb9e7':
   s=s.replace('audit, notification, permission, and error boundaries','audit and notification boundaries; real guards, permissions and errors execute')
   s=s.replace('one-line behavioral dependency','ordering correction')
   s=s.replace('const pendingStage = request.stages\n  .filter((stage) => stage.status === "PENDING")\n  .sort((left, right) => left.sequence - right.sequence)[0];','const pendingStages = request.stages\n  .filter((stage) => stage.status === "PENDING")\n  .sort((left, right) => left.sequence - right.sequence);\nconst pendingStage = pendingStages[0];\n// Later, approval also uses this sorted collection:\nconst nextStage = pendingStages.find(stage => stage.sequence > pendingStage.sequence);')
   s=s.replace('sequence 2 followed by sequence 1','sequences 3, 2 and 1').replace('`[2,1]`','`[3,2,1]`').replace('[2 PENDING, 1 PENDING]','[3 PENDING, 2 PENDING, 1 PENDING]').replace('both rows remain','all three rows remain').replace('order becomes 1, 2','order becomes 1, 2, 3')
   s=s.replace('The permission boundary is represented by a guard stub that permits the known actor, allowing the test to concentrate on ordering. That means this lab does not reprove role policy; the existing production `guards.ts` and permission tests remain the source for that behavior.','Real guards, permissions and errors load from production files. An EMPLOYEE is refused by capability, and SECURITY is refused by assignment to the MANAGER stage. Session lookup and navigation are unused adapters; authentication is not tested.')
   s=s.replace('inspect the repository contract instead of changing the sort','inspect whether next-stage selection also uses the sorted pending collection')
   s=s.replace('audit, notification, and permission boundaries','audit and notification boundaries')
   s=s.replace('limited to selecting the lowest pending sequence','limited to selecting and advancing through pending stages in sequence order')
  p.write_text(s,encoding='utf-8')
