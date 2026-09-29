"""Read-only Desktop discovery and documentation content evidence. Writes audit artifacts only."""
from pathlib import Path
import os,json,re,time,hashlib,concurrent.futures,collections
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1];D=R.parent;O=R/'documentation-audit';O.mkdir(exist_ok=True)
from scan_desktop import SKIP_DIRS,SOURCE_EXT,MARKERS
SKIP=(SKIP_DIRS-{'bin','.agents','.agent','.claude','.codex','.gemini','.cursor'})|{'vendor','.npm','_build','.tox','.hypothesis','site-packages','packages-cache'}
EXCLUDE={'astraorganized','astraorganized2','project-inventory'}
DOC={'.md','.mdx','.rst','.txt','.adoc'}
PATTERNS={
 'onboarding':r'\b(?:codebase|repo(?:sitory) tour|reading order|start here|first change|onboarding|local (?:development|setup)|getting started|file map)\b',
 'architecture':r'\b(?:architecture|request (?:flow|lifecycle|path)|data flow|boundar(?:y|ies)|transaction|domain model|component diagram|sequence diagram|dependency injection)\b',
 'explanation':r'\b(?:because|trade[ -]?offs?|why (?:we|this|the|it)|reason(?:ing)?|invariant|mental model|alternatives?|design decision)\b',
 'curriculum':r'\b(?:exercise|challenge|checkpoint|quiz|learning (?:path|objective)|lesson|curriculum|practice task|try (?:this|it)|capstone|rubric)\b',
 'workflow':r'\b(?:code review|pull request|ADR|incident|debugging|refactor|test(?:ing)? strategy|failure scenario|runbook|postmortem|acceptance criteria)\b',
 'advanced':r'\b(?:concurren\w*|idempotenc\w*|observability|tracing|caching|cache invalidation|multi[ -]?tenan\w*|authori[sz]ation|queue|backpressure|outbox|isolation|scalab\w*|reliability|race condition)\b',
}
RX={k:re.compile(v,re.I) for k,v in PATTERNS.items()}
LEARNING=re.compile(r'fable|upskill|learning|onboarding|curriculum|tutorial|architecture|guide|handbook|training|codebase|walkthrough|lesson|module|engineering|adr|design|exercis|trace|concept',re.I)
def long(p):return chr(92)*2+'?'+chr(92)+str(p) if os.name=='nt' else str(p)
def scan(top):
 files=[];docs=[];directories=[];errors=[];skips=collections.Counter();stack=[top]
 while stack:
  p=stack.pop();rel=p.relative_to(D).as_posix()
  try:entries=list(os.scandir(long(p)))
  except OSError as e:errors.append({'path':rel,'error':str(e)});continue
  marks=[];git=False;directsources=0
  for e in entries:
   name=e.name;low=name.lower();child=p/name;crel=child.relative_to(D).as_posix()
   try:
    if e.is_symlink() or (hasattr(e,'is_junction') and e.is_junction()):skips['links']+=1;continue
    if low=='.git':git=True;skips['git']+=1;continue
    if e.is_dir(follow_symlinks=False):
     if low in SKIP or (low=='bin' and any(x.lower() in rel.lower().split('/') for x in ['debug','release'])):skips[low]+=1
     else:stack.append(child)
     continue
    if not e.is_file(follow_symlinks=False):continue
    ext=Path(name).suffix.lower();size=e.stat().st_size
    source=ext in SOURCE_EXT and not low.endswith(('.min.js','.min.css','.d.ts'))
    marker=low in MARKERS or ext in {'.sln','.slnx','.csproj','.fsproj'}
    if marker:marks.append(name)
    if source:directsources+=1
    if source or marker:files.append({'path':crel,'bytes':size,'source':source,'marker':marker})
    if ext not in DOC:continue
    if low in {'license','license.md','license.txt','notice.txt','third-party-notices.txt'}:continue
    if size>3000000:docs.append({'path':crel,'bytes':size,'skipped':'text over 3MB'});continue
    raw=Path(long(child)).read_bytes();text=raw.decode('utf-8-sig',errors='replace');words=len(text.split());hits={k:len(rx.findall(text)) for k,rx in RX.items()}
    lines=text.splitlines();heads=[x.strip()[:180] for x in lines if re.match(r'^#{1,4}\s|^\d+\.\s',x)][:35]
    snippets=[]
    for k,rx in RX.items():
     match=rx.search(text)
     if match:snippets.append({'dimension':k,'text':re.sub(r'\s+',' ',text[max(0,match.start()-90):match.end()+210])})
    refs=re.findall(r'`([^`\n]{3,160}\.(?:tsx?|jsx?|cs|py|go|rs|sql))`',text)
    docs.append({'path':crel,'bytes':size,'words':words,'sha256':hashlib.sha256(raw).hexdigest(),'learning_path':bool(LEARNING.search(crel)),'dimensions':hits,'headings':heads,'snippets':snippets,'code_references':list(dict.fromkeys(refs))[:10],'code_blocks':text.count('```')//2,'placeholder':words<80 or (words<250 and bool(re.search(r'\b(?:TODO|placeholder|coming soon|to be (?:written|completed))\b',text,re.I)))})
   except OSError as e:errors.append({'path':crel,'error':str(e)})
  if marks or git or directsources:directories.append({'path':rel,'markers':marks,'git':git,'direct_sources':directsources})
 return {'top':top.name,'files':files,'docs':docs,'directories':directories,'errors':errors,'skipped':dict(skips)}
def main():
 started=datetime.now(timezone.utc).isoformat();tops=[p for p in D.iterdir() if p.is_dir() and p.name.lower() not in EXCLUDE];results=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  futures={pool.submit(scan,p):p for p in tops}
  for f in concurrent.futures.as_completed(futures):
   r=f.result();results.append(r);name=hashlib.sha256(r['top'].encode()).hexdigest()[:12]+'.json';(O/name).write_text(json.dumps(r,ensure_ascii=False),encoding='utf-8')
   progress={'started':started,'completed_roots':len(results),'total_roots':len(tops),'last':r['top'],'source_or_manifest_files':sum(len(x['files']) for x in results),'text_documents_read':sum(len(x['docs']) for x in results),'errors':sum(len(x['errors']) for x in results)}
   (O/'progress.json').write_text(json.dumps(progress,indent=2),encoding='utf-8');print(json.dumps(progress),flush=True)
 (O/'scan-manifest.json').write_text(json.dumps({'started':started,'completed':datetime.now(timezone.utc).isoformat(),'scope':str(D),'excluded_roots':sorted(EXCLUDE),'top_roots':[r['top'] for r in results],'files':[hashlib.sha256(r['top'].encode()).hexdigest()[:12]+'.json' for r in results]},indent=2),encoding='utf-8')
if __name__=='__main__':main()
