from pathlib import Path
from urllib.parse import unquote
import json,re,collections
R=Path(__file__).resolve().parents[1];O=R/'documentation-audit'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
j=read(R/'project-audit.json');s=j['summary'];p=read(O/'progress.json');scan=read(O/'scan-manifest.json')
groups=[j[k] for k in ['enhancedProjects','partiallyEnhancedProjects','remainingProjects','manualReview']]
projects=sum(groups,[]);ids=[x['id'] for x in projects];locations=[l['path'] for x in projects for l in x['locations']]
assert len(ids)==len(set(ids))==s['totalLegitimateProjects']
assert len(locations)==len(set(locations))==s['legitimatePhysicalLocations']
assert len(locations)-len(projects)==s['duplicateLocationsCollapsed']
assert len(locations)+len(j['excludedLocations'])==s['physicalLocationsReviewed']
assert s['remainingFullTreatment']==len(groups[1])+len(groups[2])
assert len(j['topProjects'])==len({x['id'] for x in j['topProjects']})==50
assert all(x['rating'] in ['High','Exceptional'] and x['status']=='Substantially enhanced' and x.get('selectionReason') and len(x['evidence'])>=2 for x in j['topProjects'])
assert len(j['recommendedNextBatch'])==len({x['path'] for x in j['recommendedNextBatch']})==10
assert all(x['status']!='Substantially enhanced' for x in j['recommendedNextBatch'])
assert p['completed_roots']==p['total_roots']==len(scan['top_roots'])==98 and p['errors']==0
assert j['documentationQualityReview']['documentsChangedSinceScan']==0
inventory=read(O/'location-inventory.json');accounted=set(locations)|{x['path'] for x in j['excludedLocations']}
assert accounted=={x['path'] for x in inventory}
assert all(Path(x['absolutePath']).is_dir() for x in projects)
md=(R/'PROJECT_DOCUMENTATION_AUDIT.md').read_text(encoding='utf-8')
links=set(re.findall(r'\]\(([^)]+)\)',md));broken=[]
for target in links:
 if re.match(r'[a-z]+:|#',target,re.I):continue
 if not (R/unquote(target.split('#')[0])).exists():broken.append(target)
assert not broken,broken[:10]
checked_sources=[f['path'] for u in inventory for f in u['files']]
assert len(checked_sources)==len(set(checked_sources)),'Source credit assigned to multiple project locations'
out={'result':'passed','projectRecords':len(projects),'physicalLocationsAccounted':len(accounted),'topProjects':50,'nextBatch':10,'reportLinksChecked':len(links),'brokenReportLinks':broken,'sourceOrManifestPathsAssignedOnce':len(checked_sources),'scanReadErrors':p['errors'],'representativeDocuments':j['documentationQualityReview']['representativeDocumentsRead'],'note':'Read-only audit integrity checks; no project runtime, install, build or test suite was executed.'}
(O/'validation.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))
