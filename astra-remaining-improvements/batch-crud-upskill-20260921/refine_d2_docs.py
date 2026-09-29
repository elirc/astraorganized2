from pathlib import Path
p=Path(__file__).resolve().parent.parent/'stage/3c142f8c1521/astraupskill'
for f in p.glob('*.md'):
    s=f.read_text(encoding='utf-8-sig')
    for a,b in {"route?s":"route's","handler?s":"handler's","project?s":"project's","test?s":"test's","review?s":"review's","table?s":"table's","?fully integration tested.?":'"fully integration tested."'}.items(): s=s.replace(a,b)
    s=s.replace('original route and schema snapshots are preserved','the exact original route snapshot is preserved')
    s=s.replace('The original route and relevant schema/validation files remain in `astraupskill/snapshots`','The original route remains in `astraupskill/snapshots/reviews-route.ts.original.txt`')
    s=s.replace('`astraupskill/snapshots/src/app/api/reviews/route.ts`','`astraupskill/snapshots/reviews-route.ts.original.txt`')
    s=s.replace('project rules update returns new rules','project rules update completes without returning a row')
    f.write_text(s,encoding='utf-8')
f=p/'01-CODEBASE-MAP.md'
s=f.read_text(encoding='utf-8')
s=s.replace('loads the project, loads the prompt template, loads existing project rules, and normalizes the submitted source. It then inserts a review record, handles optional rules, updates review metadata, and returns JSON.', 'loads the project, normalizes the submitted source, builds initial metadata, and loads a specifically requested prompt template if present. It then inserts a review record, loads existing project rules, handles submitted rules, resolves the effective template, updates review metadata, and returns JSON.')
s=s.replace('request -> schema validation -> project lookup -> template lookup -> normalize source -> insert review -> update or insert rules if submitted -> assemble source metadata -> update review -> response.', 'request -> schema validation -> project lookup -> normalize source -> optional selected-template lookup -> insert review -> load rules -> update or insert rules if submitted -> resolve template -> assemble review metadata -> update review -> response.')
s+='\nThere are two template lookup paths: an explicit template is checked before insertion, while the active default is loaded afterward. Neither path changes the origin of accepted rules: metadata uses parsed request data after a successful write, not a returned database row.\n'
f.write_text(s,encoding='utf-8')
f=p/'03-WORKED-CHANGE.md';s=f.read_text(encoding='utf-8');start=s.index('```ts',s.index('The exact') if 'The exact' in s else 0) if False else 0
s=s.replace('const sourceMetadata = { source, rules: existingRules };\nawait updateReview(review.id, { sourceMetadata });\nreturn NextResponse.json({ sourceMetadata });','const storedMetadata = { source, rules: existingRules };\nawait updateReview(review.id, { sourceMetadata: storedMetadata });\nreturn NextResponse.json({ sourceMetadata: review.sourceMetadata });')
s=s.replace('When the request submits `newRules`, both metadata and response can still describe `oldRules`.','Before the fix, persisted metadata used old rules while the response reused the initial insert metadata, which lacked finalized rules and template.')
a=s.index('```ts',s.index('The staged route')) if 'The staged route' in s else s.index('```ts',s.index('The exact')) if False else s.index('```ts',s.index('staged route'))
b=s.index('```',a+5)+3
s=s[:a]+'''```ts
const reviewMetadata = {
  ...sourceMetadata,
  template,
  rules: parsedRules?.success ? parsedRules.data : rules ? { ...rules } : undefined
};
// After optional rules persistence succeeds:
await db.update(reviews).set({ sourceMetadata: reviewMetadata })
  .where(eq(reviews.id, row.id));
// The response uses this same object as its sourceMetadata.
```'''+s[b:]
s=s.replace('old rules loaded -> submitted rules detected -> update or insert returns final row -> metadata uses final row -> response reuses metadata.', 'old rules loaded -> submitted rules parsed -> update or insert completes -> metadata uses parsed submitted rules -> response reuses metadata. Persistence calls do not return the final rules row; generated database fields are not added to the submitted snapshot.')
f.write_text(s,encoding='utf-8')
for name in ['05-PRACTICE.md','07-TRACE-LAB.md']:
 f=p/name;s=f.read_text(encoding='utf-8').replace('template lookup, source normalization, review insert','source normalization, optional selected-template lookup, review insert').replace('project and template load; source normalizes; review inserts;', 'project loads; source normalizes; a selected template loads if requested; review inserts; existing rules load;').replace('metadata writes new rules;', 'the effective template resolves; metadata writes parsed new rules;')
 s+='\nCompare the submitted-rules branch with the omitted-rules branch at field level. Parsed input has the validation schema shape, while an existing row can also contain database identifiers. This patch preserves that distinction. A future canonical snapshot schema should explicitly select fields and test both branches before changing compatibility.\n'
 f.write_text(s,encoding='utf-8')
