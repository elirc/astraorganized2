"""Verify a fresh finite source copy, dependency-free tests and the real setup/server CLI."""
from pathlib import Path
import hashlib, json, os, queue, re, shutil, socket, subprocess, sys, threading, time, urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(sys.argv[1]).resolve(); OUT.mkdir(parents=True, exist_ok=False)
COPY = OUT/'source'; COPY.mkdir()
checks=[]
for directory in ['src','test','verification']:
    for source in (ROOT/directory).rglob('*'):
        if source.is_file() and source.suffix in {'.js','.cjs','.html','.css','.py','.txt'} and '__pycache__' not in source.parts:
            target=COPY/source.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
for name in ['package.json','package-lock.json']:
    shutil.copyfile(ROOT/name,COPY/name)

def passed(name):
    checks.append({'name':name,'passed':True});print('PASS '+name,flush=True)

def command(name,args):
    with (OUT/(name+'.log')).open('w',encoding='utf-8') as log:
        result=subprocess.run(args,cwd=COPY,stdout=log,stderr=subprocess.STDOUT)
    assert result.returncode==0,(name,result.returncode)
    return (OUT/(name+'.log')).read_text(encoding='utf-8')

process=None; code=1
try:
    output=command('tests',['node','verification/run-tests.js'])
    assert re.search(r'# tests 120\b',output) and re.search(r'# pass 120\b',output) and '# fail 0' in output
    passed('fresh source copy repeats all 120 Node tests without npm install')
    syntax=command('syntax',['node','verification/check-syntax.js'])
    assert 'Syntax checked ' in syntax
    passed('all current source test and verification JavaScript parses in fresh copy')
    data=OUT/'practice.json'; env={**os.environ,'PRACTICE_DATA_FILE':str(data)}
    setup=subprocess.run(['node','src/practice/setup.js','Fresh setup learner'],cwd=COPY,env=env,capture_output=True,text=True,encoding='utf-8')
    assert setup.returncode==0,setup.stderr
    token=setup.stdout.strip().splitlines()[-1];assert re.fullmatch('[a-f0-9]{64}',token)
    before=data.read_bytes(); assert token.encode() not in before
    second=subprocess.run(['node','src/practice/setup.js','Replacement attempt'],cwd=COPY,env=env,capture_output=True,text=True,encoding='utf-8')
    assert second.returncode!=0 and data.read_bytes()==before
    passed('real setup initializes once stores only token hash and refuses overwrite byte-for-byte')
    with socket.socket() as sock:
        sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    env['PRACTICE_PORT']=str(port)
    with (OUT/'server.log').open('w',encoding='utf-8') as log:
        process=subprocess.Popen(['node','src/practice/server.js'],cwd=COPY,env=env,stdout=subprocess.PIPE,stderr=log,text=True,encoding='utf-8')
        lines=queue.Queue();threading.Thread(target=lambda:lines.put(process.stdout.readline()),daemon=True).start()
        assert 'Practice workspace:' in lines.get(timeout=120)
        url=f'http://127.0.0.1:{port}'
        request=urllib.request.Request(url+'/api/bootstrap',headers={'Authorization':'Bearer '+token})
        with urllib.request.urlopen(request,timeout=20) as response:
            bootstrap=json.load(response); assert response.status==200
        assert bootstrap['owner']=='Fresh setup learner' and all(count==0 for count in bootstrap['counts'].values())
        assert token not in json.dumps(bootstrap) and 'auth' not in bootstrap
        for route,name in [('/','index.html'),('/app.js','app.js'),('/styles.css','styles.css')]:
            with urllib.request.urlopen(url+route,timeout=20) as response: content=response.read()
            assert content==(COPY/'src/practice/ui'/name).read_bytes()
        passed('real server CLI starts with clean owner state and serves three exact UI assets')
    code=0
finally:
    if process and process.poll() is None:
        process.terminate();process.wait(timeout=20)
    # The retained disposable copy is inside the requested NEW evidence folder.
    # Remove its authentication database after validation, never a user workspace.
    data=OUT/'practice.json'
    assert data.resolve().parent==OUT
    if data.exists():data.unlink()
    (OUT/'results.json').write_text(json.dumps({'passed':code==0,'checks':checks,'repeatedNodeTests':120,'dependencyInstall':False},indent=2),encoding='utf-8')
sys.exit(code)
