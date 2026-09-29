from pathlib import Path
import subprocess,json,re,tempfile,os
B=Path(__file__).resolve().parent;P=B/'stage/d9a27fa7f308';C=B/'checks/j5';C.mkdir(parents=True,exist_ok=True)
J=Path(r'C:\Users\Owner\AppData\Local\Programs\Microsoft\jdk-17.0.10.7-hotspot');env=os.environ.copy();env['JAVA_HOME']=str(J)
r=subprocess.run(['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File',str(P/'run.ps1'),'-Test'],cwd=P,env=env,capture_output=True,text=True,timeout=90)
(C/'regression.log').write_text(r.stdout+r.stderr,encoding='utf-8');print(r.stdout+r.stderr,flush=True)
assert r.returncode==0 and 'RESULT passed=23 failed=0' in r.stdout
checks=[]
with tempfile.TemporaryDirectory(prefix='j5-cli-') as temporary:
 f=Path(temporary)/'expenses.txt'
 def cli(text):
  result=subprocess.run([str(J/'bin/java.exe'),'-cp',str(P/'out'),'expensetracker.App',str(f)],input=text,capture_output=True,text=True,timeout=20)
  assert result.returncode==0,(result.stdout,result.stderr)
  return result.stdout
 out=cli('1\nLunch\n12.30\nFood\n2026-01-02\n\n7\n');assert 'Added expense #1.' in out
 out=cli('2\n7\n');assert 'Loaded 1 expense(s).' in out and 'Lunch' in out;checks.append('separate process reload preserves empty note')
 out=cli('8\n1\nBus\n2.50\nTravel\n2026-02-03\n\n7\n');assert 'Updated expense #1.' in out
 out=cli('2\n7\n');assert 'Bus' in out and '$2.50' in out and 'Lunch' not in out;checks.append('CLI update persists')
 out=cli('9\n1\nno\n2\n7\n');assert 'Deletion cancelled.' in out and 'Bus' in out
 out=cli('9\n1\nyes\n7\n');assert 'Deleted expense #1.' in out
 out=cli('2\n7\n');assert 'Loaded 0 expense(s).' in out;checks.append('CLI delete confirmation and persistence')
 out=cli('1\nLunch\n12.30\nFood\n2026-01-02\n\n1\nUnfinished\n');assert 'Input ended. Saving completed changes.' in out
 out=cli('2\n7\n');assert 'Loaded 1 expense(s).' in out and 'Unfinished' not in out;checks.append('EOF keeps completed changes and discards unfinished command')
 f.write_text(f.read_text()+'broken\n',encoding='utf-8');before=f.read_bytes();out=cli('7\n')
 assert 'Startup stopped.' in out and f.read_bytes()==before and 'Expenses saved to disk.' not in out;checks.append('startup rejects corruption without overwriting original file')
(C/'cli.log').write_text('\n'.join('PASS '+x for x in checks)+'\n',encoding='utf-8')
result={'passed':True,'tests':28,'javaRegressionTests':23,'separateProcessCliScenarios':len(checks),'compiler':'Microsoft OpenJDK 17.0.10; --release 17 -Xlint:all','checks':checks,'limits':['No HTTP server or browser UI; no concurrent-writer or power-loss guarantees.']}
(C/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))
