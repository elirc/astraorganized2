from pathlib import Path
B=Path(__file__).resolve().parent.parent
for id,testcount,old in [('42df17f9e984',6,'42df17f9e984-crud-b08-runtime.tap.txt'),('3ee259e51792',5,'3ee259e51792-crud-b08-runtime.tap.txt'),('fa998c611f1d',5,'fa998c611f1d-crud-b08-runtime.tap.txt')]:
 for p in (B/'stage'/id/'astraupskill').glob('*.md'):
  s=p.read_text(encoding='utf-8-sig').replace(old,'crud-b08-astra-runtime.log').replace('3/3 tests',f'{testcount}/{testcount} tests').replace('3 tests',f'{testcount} tests').replace('three passing Node tests',f'{testcount} passing Node tests').replace('three subtests',f'{testcount} subtests').replace('All three Node tests',f'All {testcount} Node tests')
  if id=='42df17f9e984':
   s=s.replace('it preserves the repository contract and the existing status calculation','it preserves the repository contract and derives status from the accumulator without adding incoming quantities again')
   s=s.replace('Prisma, serializer, and error contracts','Prisma and repository adapters; the real serializer and errors execute')
   s=s.replace('repository methods, serializer, and error classes','repository methods and inert Zod schema builders. Real errors, serializer and transition function execute; schema parsing does not')
   s=s.replace('tenant, purchase-order id, next status, and transaction client','tenant, purchase-order id, next status, optional received-at date, and transaction client')
   s=s.replace('one valid full receipt commits','one valid full receipt invokes the write adapters')
   s=s.replace('Change the duplicate fixture to entries 5 and 5 with no persisted receipts.','Set the ordered quantity to12 and change the duplicate fixture to entries5 and5 with no persisted receipts.')
   s=s.replace('?the array is validated?','"the array is validated"')
   if p.name=='03-WORKED-CHANGE.md':s+='\nThe same accumulator feeds status derivation. Adding input a second time would label5 of10 as RECEIVED, so the old second addition loop is removed. A subsequent valid partial receipt may leave status unchanged; receiving skips the transition helper only for that equal-state case after checking the order is APPROVED or PARTIALLY_RECEIVED.\n'
   if p.name=='VERIFICATION.md':s+='\nThe additional cases cover one partial receipt, duplicate entries within bounds, prior4 plus incoming2/6/7, foreign line IDs and a nonreceivable state. These expose double-counting and repeated-partial refusal. The real transition function loads through inert schema builders; no Zod parse claim is made. Prior totals are read before the transaction, so concurrent receipt safety remains unproved.\n'
  elif id=='3ee259e51792':
   s=s.replace('Explicit database and authorization doubles','Explicit database adapters and real authorization helpers')
   s=s.replace('explicit auth, repository, transaction, workflow, and audit doubles','repository, transaction and audit adapters; the real authorization, workflow and errors execute')
   s=s.replace('A repository double that rejects undefined should fail if the implementation writes null for omitted fields, proving that omitted and clear remain separate.','A double that rejects undefined is incompatible with this current service payload. Instead assert that omitted values remain undefined and explicit empty values become null; an always-null implementation must fail the omitted-input test.')
   if p.name=='VERIFICATION.md':s+='\nAdditional assertions cover nonempty replacement, real auditor/foreign-team refusals, forwarding the real owningTeamId scope and filtering restricted notes for a CASE_WORKER. Scope arguments are checked, but database filtering itself is not executed.\n'
  else:
   s=s.replace('DELETE only needs the preflight lookup before its update.','DELETE currently uses only a preflight lookup and ignores affected-row count, so disappearance between lookup and mutation can still return success.')
   s=s.replace('The route’s ID predicate is the current ownership boundary because this app has no tenant column.','The route’s ID predicate selects a resource; it is not an authorization or ownership check.')
   if p.name=='VERIFICATION.md':s+='\nTwo added cases verify a successful PATCH, tag serialization, ignored unexpected input, ID predicate, completion timestamp, and a missing post-write reread. DELETE concurrent disappearance is not resolved by the pre-read. These remain route-function assertions with framework and database adapters.\n'
  p.write_text(s,encoding='utf-8')
