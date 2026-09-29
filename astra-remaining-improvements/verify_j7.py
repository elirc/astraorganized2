from pathlib import Path
import subprocess,json,tempfile,os,re
B=Path(__file__).resolve().parent;P=B/'stage/14690be423dc';C=B/'checks/j7';C.mkdir(parents=True,exist_ok=True)
J=Path(r'C:\Users\Owner\AppData\Local\Programs\Microsoft\jdk-17.0.10.7-hotspot');env=os.environ.copy();env['JAVA_HOME']=str(J)
r=subprocess.run(['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File',str(P/'run.ps1'),'-Test'],cwd=P,env=env,capture_output=True,text=True,timeout=120)
(C/'regression.log').write_text(r.stdout+r.stderr,encoding='utf-8');print(r.stdout+r.stderr,flush=True);assert r.returncode==0 and 'RESULT passed=35 failed=0' in r.stdout
checks=[]
with tempfile.TemporaryDirectory(prefix='j7-cli-') as temporary:
 d=Path(temporary)
 def cli(text):
  result=subprocess.run([str(J/'bin/java.exe'),'-cp',str(P/'out'),'oms.App',str(d)],input=text,capture_output=True,text=True,timeout=20)
  assert result.returncode==0,(result.stdout,result.stderr)
  return result.stdout
 out=cli('1\nLearner\nlearner@example.test\n\n3\nNotebook\nNOTE\n10.00\ny\n13\n');customer=re.search(r'Created customer with ID: ([a-f0-9-]+)',out)[1];product=re.search(r'Created product with ID: ([a-f0-9-]+)',out)[1]
 out=cli('2\n4\n13\n');assert 'Learner' in out and 'Notebook' in out;checks.append('customer and product survive separate-process reload')
 out=cli(f'5\n{customer}\n13\n');order=re.search(r'Created order with ID: ([a-f0-9-]+)',out)[1]
 out=cli(f'6\n{order}\n{product}\n2\n10\n{order}\n5.00\n13\n');assert 'Discount applied.' in out
 out=cli(f'8\n{order}\n13\n');assert 'Discount: $5.00' in out and 'Total: $15.00' in out;checks.append('discount survives persisted aggregate reload')
 out=cli(f'14\n{order}\n{product}\n3\n13\n');assert 'Item quantity updated.' in out
 out=cli(f'8\n{order}\n13\n');assert 'qty=3' in out and 'Total: $25.00' in out;checks.append('quantity update persists with original price and discount')
 out=cli(f'10\n{order}\n1.001\n8\n{order}\n13\n');assert 'at most 2 decimal places' in out and 'Discount: $5.00' in out;checks.append('CLI rejects sub-cent discount before service mutation')
 out=cli(f'11\n{order}\nSUBMITTED\n11\n{order}\nPAID\n14\n{order}\n{product}\n4\n8\n{order}\n13\n');assert 'Could not update quantity:' in out and 'Status: PAID' in out and 'Total: $25.00' in out;checks.append('paid order freezes line edits through CLI')
 out=cli('1\nUnfinished\n');assert 'Input ended. Saving completed changes.' in out
 out=cli('2\n13\n');assert 'Unfinished' not in out and 'Learner' in out;checks.append('EOF preserves completed work and discards unfinished input')
 f=d/'oms.snapshot.txt';f.write_bytes(f.read_bytes()+b'broken\n');before=f.read_bytes();out=cli('13\n');assert 'Startup stopped:' in out and 'Order Management System' not in out and f.read_bytes()==before;checks.append('corrupt startup leaves authoritative file unchanged')
(C/'cli.log').write_text('\n'.join('PASS '+x for x in checks)+'\n',encoding='utf-8')
result={'passed':True,'tests':42,'javaRegressionTests':35,'separateProcessCliScenarios':len(checks),'compiler':'Microsoft OpenJDK 17.0.10; --release 17 -Xlint:all','checks':checks,'limits':['Single-threaded local CLI; no database, HTTP, browser, multi-process locking or power-loss test.']}
(C/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))
