from pathlib import Path
import json,subprocess,sys
B=Path(__file__).resolve().parents[2];F=Path(__file__).resolve().parent
selection=json.loads((F/'selection.json').read_text(encoding='utf-8'));progress=json.loads((B/'progress.json').read_text(encoding='utf-8'));byid={p['id']:p for p in progress['projects']};pending=[p for p in selection['projects'] if byid[p['id']]['status']!='complete']
(F/'REMAINING_QUEUE.md').write_text('# Remaining next-50 queue\n\nOnly canonical deliveries count. Luna implements each assigned project; Astra independently reviews and applies.\n\n'+'\n'.join('- '+p['id']+' — '+p['path'] for p in pending)+'\n',encoding='utf-8')
p=F/'active-work.json';state=json.loads(p.read_text(encoding='utf-8'));state['batchDelivered']=50-len(pending);state['overallDelivered']=sum(p['status']=='complete' for p in progress['projects']);p.write_text(json.dumps(state,indent=2),encoding='utf-8')
for script in ['render_progress_report.py','render_new_project_report.py','render_completion_summary.py','render_finished_summary.py','render_next50_report.py','checks/batch-luna-astra-20260912/render_batch_report.py']:
 cmd=[sys.executable,'-X','utf8',str(B/script)]
 if script.endswith('render_batch_report.py'):cmd.append('2')
 subprocess.run(cmd,check=True)
