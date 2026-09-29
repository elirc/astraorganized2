from pathlib import Path
P=Path(__file__).resolve().parent.parent/'stage/5fd517cae993/astraupskill'
replacements={'`updateStatus`':'`transitionConversationStatus`','conversationId and nextStatus':'conversationId and status','return updatedConversation;':'return { success: true };','returned DTO':'success response','updated response':'success response','permission guard, transaction wrapper, and audit adapter':'transaction wrapper and audit adapter; the real permission policy and error helpers execute','Then assert update and audit counts remain zero.':'Then assert one update attempt occurred and zero audit calls occurred.','move to ACTIVE':'move to OPEN','same-status or lifecycle rejection':'update-error propagation','repository, transaction, permission, audit, and error contracts':'repository, transaction and audit adapters with actual permissions and errors'}
for f in P.glob('*.md'):
 s=f.read_text(encoding='utf-8-sig').replace(".''",'.')
 for a,b in replacements.items():s=s.replace(a,b)
 if f.name=='05-PRACTICE.md':
  s=s.replace('Answer separately: a 404-style service error, no audit call, and no successful DTO.','List the error, audit count and whether a success object is returned.')
  s=s.replace('The status becomes RESOLVED and due dates are cleared.','Predict both due-date values without looking at the assertions.')
  s=s.replace('No. Permission fails first with 403 and the transaction/repository/audit doubles remain untouched.','Identify the error and first permitted dependency call, if any.')
 f.write_text(s,encoding='utf-8')
