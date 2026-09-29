from pathlib import Path

def write_course(project_id, chapters, root_note):
 P=Path(__file__).resolve().parent.parent/'stage'/project_id
 nav='\n## Course navigation\n\n'+' / '.join(f'[{name.removesuffix(".md")}]({name})' for name in chapters)+'\n'
 (P/'astraupskill').mkdir(exist_ok=True)
 for name,(title,body,excerpts) in chapters.items():
  text='# '+title+'\n\n'+body.strip()+'\n'
  for file,anchor,count in excerpts:
   source=(P/file).read_text(encoding='utf8');source=source[source.index(anchor):] if anchor else source;sample='\n'.join(source.splitlines()[:count])
   text+=f'\n## Source excerpt\n\nFrom [{file}](../{file}).\n\n```{Path(file).suffix.removeprefix(".")}\n{sample}\n```\n'
  text+=nav;assert len(text.split())>=250,(name,len(text.split()));(P/'astraupskill'/name).write_text(text,encoding='utf8');print(name,len(text.split()))
 f=P/'README.md';s=f.read_text(encoding='utf8') if f.exists() else '# Project\n'
 if 'astraupskill/README.md' not in s:s+='\n## Source-based improvement course\n\n[Start the course](astraupskill/README.md). '+root_note+'\n'
 f.write_text(s,encoding='utf8')
