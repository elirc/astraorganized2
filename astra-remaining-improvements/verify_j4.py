from pathlib import Path
import subprocess,json,tempfile,os,time
B=Path(__file__).resolve().parent;P=B/'stage/06325f8ab263';C=B/'checks/j4';C.mkdir(parents=True,exist_ok=True)
J=Path(r'C:\Users\Owner\AppData\Local\Programs\Microsoft\jdk-17.0.10.7-hotspot');env=os.environ.copy();env['PATH']=str(J/'bin')+os.pathsep+env['PATH']
r=subprocess.run(['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File',str(P/'run.ps1'),'-Test'],cwd=P,env=env,capture_output=True,text=True,timeout=120)
(C/'regression.log').write_text(r.stdout+r.stderr,encoding='utf-8');assert r.returncode==0 and 'RESULT passed=28' in r.stdout,(r.stdout,r.stderr)
checks=[]
with tempfile.TemporaryDirectory(prefix='j4-cli-') as temporary:
 d=Path(temporary);f=d/'questions.txt';f.write_text('Q1|Atomic means?|All or nothing;Separate writes|A|\n',encoding='utf-8')
 def cli(text):
  r=subprocess.run([str(J/'bin/java.exe'),'-cp',str(P/'out'),'quiz.App',str(f)],input=text,capture_output=True,text=True,timeout=20);assert r.returncode==0,(r.stdout,r.stderr);return r.stdout
 out=cli('5\nQ2\nWhat is CRUD?\n2\nCreate read update delete\nCompile run undo debug\nA\n\n3\n');assert 'Question created and saved.' in out
 out=cli('4\n3\n');assert 'Q2: What is CRUD?' in out;checks.append('created question survives separate-process reload with empty explanation')
 out=cli('6\nQ2\nChanged prompt\n2\nWrong\nRight\nB\nReview the invariant\n3\n');assert 'Question updated and saved.' in out
 assert 'Q2: Changed prompt' in cli('4\n3\n');checks.append('full update persists under the same question id')
 before=f.read_bytes();out=cli('7\nQ2\nno\n3\n');assert 'Deletion cancelled.' in out and f.read_bytes()==before;checks.append('cancelled deletion preserves exact bank bytes')
 out=cli('7\nQ2\nyes\n3\n');assert 'Question deleted and saved.' in out and 'Q2:' not in cli('4\n3\n');checks.append('confirmed deletion persists across processes')
 before=f.read_bytes();out=cli('5\npartial\nUnfinished prompt\n');assert 'incomplete edit was not applied' in out and f.read_bytes()==before;checks.append('EOF during form discards the incomplete command')
 out=cli('1\n');assert 'Quiz interrupted; partial result only.' in out and 'Answered: 0 of 1' in out and 'Unanswered: 1' in out;checks.append('EOF during quiz reports partial scoring without a crash')
 out=cli('7\nQ1\nyes\n3\n');assert 'Question deleted and saved.' in out
 out=cli('1\n3\n');assert 'No questions available.' in out;checks.append('empty bank reloads and quiz offers create guidance')
 f.write_text('QUIZ-BANK\t1\nbroken\n',encoding='utf-8');before=f.read_bytes();out=cli('3\n');assert 'could not be started' in out and f.read_bytes()==before;checks.append('corrupt startup preserves the authoritative file')
 f.write_text('Q1|Atomic means?|All or nothing;Separate writes|A|\n',encoding='utf-8');go=d/'go';workers=[]
 try:
  for index in range(2):
   workers.append(subprocess.Popen([str(J/'bin/java.exe'),'-cp',str(P/'out'),'quiz.QuestionBankTest','--worker',str(f),f'NEW{index}',str(d/f'ready{index}'),str(go)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True))
  deadline=time.monotonic()+15
  while not all((d/f'ready{i}').exists() for i in range(2)):
   assert time.monotonic()<deadline,'Worker readiness timeout';time.sleep(.02)
  go.write_text('go',encoding='utf-8');outputs=[]
  for worker in workers:
   stdout,stderr=worker.communicate(timeout=25);assert worker.returncode==0,(stdout,stderr);outputs.append(stdout)
  assert sum('SAVED' in out for out in outputs)==1 and sum('REJECTED:' in out for out in outputs)==1,outputs
  assert 'There are 2 questions available.' in cli('2\n3\n');checks.append('two gated JVM editors produce one saved winner and one rejected stale or locked command')
 finally:
  for worker in workers:
   if worker.poll() is None:worker.kill();worker.wait()
(C/'cli.log').write_text('\n'.join('PASS '+x for x in checks)+'\n',encoding='utf-8')
result={'passed':True,'tests':28+len(checks),'javaRegressionTests':28,'separateProcessScenarios':len(checks),'compiler':'Microsoft OpenJDK 17.0.10; --release 17 -Xlint:all','checks':checks,'limits':['Local CLI and file storage; no HTTP, browser, database or power-loss testing. Non-cooperating editors do not honor advisory locks.']}
(C/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))
