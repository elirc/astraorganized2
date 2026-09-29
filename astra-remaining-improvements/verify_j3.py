from pathlib import Path
import subprocess,json,tempfile,os,re
B=Path(__file__).resolve().parent;P=B/'stage/d0778f38946f';C=B/'checks/j3';C.mkdir(parents=True,exist_ok=True)
J=Path(r'C:\Users\Owner\AppData\Local\Programs\Microsoft\jdk-17.0.10.7-hotspot');env=os.environ.copy();env['JAVA_HOME']=str(J)
r=subprocess.run(['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File',str(P/'run.ps1'),'-Test'],cwd=P,env=env,capture_output=True,text=True,timeout=90)
(C/'regression.log').write_text(r.stdout+r.stderr,encoding='utf-8');print(r.stdout+r.stderr,flush=True);assert r.returncode==0 and 'RESULT passed=28 failed=0' in r.stdout
checks=[]
with tempfile.TemporaryDirectory(prefix='j3-cli-') as temporary:
 d=Path(temporary)
 def cli(text):
  result=subprocess.run([str(J/'bin/java.exe'),'-cp',str(P/'out'),'bankapp.App',str(d)],input=text,capture_output=True,text=True,timeout=20)
  assert result.returncode==0,(result.stdout,result.stderr)
  return result.stdout
 out=cli('1\nAlice\n1\nBob\n7\n');ids=re.findall(r'Account ID: (ACC-[a-f0-9-]+)',out);assert len(ids)==2;alice,bob=ids
 out=cli('2\n7\n');assert 'Accounts loaded: 2' in out and 'Alice' in out and 'Bob' in out;checks.append('create and separate process reload')
 out=cli(f'3\n{alice}\n10.00\nFunding\n5\n{alice}\n{bob}\n2.50\nLunch\n7\n');assert 'Deposit completed successfully.' in out and 'Transfer completed successfully.' in out
 out=cli('2\n7\n');assert 'Balance: $7.50' in out and 'Balance: $2.50' in out
 out=cli(f'6\n{alice}\n6\n{bob}\n7\n');assert 'TRANSFER_OUT' in out and 'TRANSFER_IN' in out and 'DEPOSIT' in out;checks.append('transfer balance and paired history survive reload')
 out=cli(f'3\n{alice}\n1.001\nInvalid\n2\n7\n');assert 'Operation failed:' in out and 'Balance: $7.50' in out;checks.append('CLI rejects precision without balance mutation')
 out=cli(f'8\n{alice}\nAlice Updated\n7\n');assert 'Account holder updated.' in out
 out=cli('2\n7\n');assert 'Alice Updated' in out;checks.append('CLI rename persists')
 out=cli(f'9\n{alice}\nyes\n7\n');assert 'Only a zero-balance account with no transaction history' in out
 out=cli('1\nUnused\n7\n');unused=re.findall(r'Account ID: (ACC-[a-f0-9-]+)',out)[0]
 out=cli(f'9\n{unused}\nno\n9\n{unused}\nyes\n7\n');assert 'Deletion cancelled.' in out and 'Unused account deleted.' in out
 out=cli('2\n7\n');assert 'Accounts loaded: 2' in out;checks.append('CLI delete protects used accounts and confirms unused deletion')
 out=cli('1\n');assert 'Input ended. Completed operations are saved.' in out
 out=cli('2\n7\n');assert 'Accounts loaded: 2' in out;checks.append('EOF does not create unfinished account')
 f=d/'bank.snapshot.txt';before=f.read_bytes();f.write_bytes(before+b'broken\n');corrupt=f.read_bytes();out=cli('7\n');assert 'Failed to load or save bank data:' in out and 'Welcome' not in out and f.read_bytes()==corrupt;checks.append('corrupt startup preserves authoritative snapshot')
(C/'cli.log').write_text('\n'.join('PASS '+x for x in checks)+'\n',encoding='utf-8')
result={'passed':True,'tests':35,'javaRegressionTests':28,'separateProcessCliScenarios':len(checks),'compiler':'Microsoft OpenJDK 17.0.10; --release 17 -Xlint:all','checks':checks,'limits':['No real funds or external services; no HTTP adapter or database; synchronization is per service instance, not cross-process.']}
(C/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))
