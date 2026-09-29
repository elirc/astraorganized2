"""Observe original API behavior using a private, disposable database only."""
from pathlib import Path
from datetime import date, timedelta
import json
import os
import socket
import subprocess
import tempfile
import time
import urllib.request
import urllib.error

C=Path(__file__).resolve().parent
S=C.parents[1]/'stage/71e7b036865c/server/Nethris.Api'
assert not (C/'baseline-probe.json').exists()
observations={}
with tempfile.TemporaryDirectory(prefix='nethris-baseline-') as temporary:
    private_root=Path(temporary).resolve()
    assert private_root.parent==Path(tempfile.gettempdir()).resolve()
    with socket.socket() as probe:
        probe.bind(('127.0.0.1',0));port=probe.getsockname()[1]
    base=f'http://127.0.0.1:{port}'
    env=os.environ.copy()
    env['ConnectionStrings__DefaultConnection']='Data Source='+str(private_root/'baseline.db')
    env['DOTNET_ROLL_FORWARD']='Major'
    process=None
    def request(method,path,body=None,token=None):
        headers={'Content-Type':'application/json'}
        if token:headers['Authorization']='Bearer '+token
        req=urllib.request.Request(base+path,data=None if body is None else json.dumps(body).encode(),headers=headers,method=method)
        try:
            with urllib.request.urlopen(req,timeout=20) as response:
                text=response.read().decode('utf-8');return response.status,json.loads(text) if text else None
        except urllib.error.HTTPError as error:
            text=error.read().decode('utf-8',errors='replace')
            try:body=json.loads(text)
            except ValueError:body={'textLength':len(text)}
            return error.code,body
    with (C/'baseline-probe-server.log').open('w',encoding='utf-8') as log:
        try:
            process=subprocess.Popen(['dotnet','bin/Debug/net8.0/Nethris.Api.dll','--urls',base],cwd=S,env=env,
                stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
            deadline=time.monotonic()+60
            while True:
                if process.poll() is not None:raise RuntimeError('Baseline API exited; inspect log.')
                try:
                    if request('GET','/api/health')[0]==200:break
                except OSError:
                    if time.monotonic()>deadline:raise TimeoutError('Baseline startup timed out.')
                    time.sleep(.2)
            status,login=request('POST','/api/auth/login',{'email':'hr@nethris.local','password':'Password123!'})
            assert status==200
            token=login['token']
            observations['loginRoleValue']=login['user']['role']
            observations['readStatuses']={path:request('GET',path,token=token)[0] for path in ['/api/departments','/api/job-roles','/api/employees','/api/org-chart','/api/pto','/api/audit-logs']}
            _,departments=request('GET','/api/departments',token=token)
            _,roles=request('GET','/api/job-roles',token=token)
            employee={'employeeNumber':'BASELINE-001','firstName':'Probe','lastName':'Account','email':'probe@nethris.local',
                'phone':None,'location':'Local test','hireDate':'2026-01-01','status':0,'ptoBalanceHours':10,
                'departmentId':departments[0]['id'],'jobRoleId':roles[0]['id'],'managerId':None,'accountRole':3}
            status,_=request('POST','/api/employees',employee,token)
            observations['hrCreatesAdminStatus']=status
            status,elevated=request('POST','/api/auth/login',{'email':'probe@nethris.local','password':'Password123!'})
            observations['newAccountRole']=elevated['user']['role'] if status==200 else None
            status,employee_login=request('POST','/api/auth/login',{'email':'alex@nethris.local','password':'Password123!'})
            assert status==200
            start=(date.today()+timedelta(days=60)).isoformat()
            status,pto=request('POST','/api/pto',{'startDate':start,'endDate':start,'hours':9999,'reason':'Disposable baseline probe'},employee_login['token'])
            observations['overdrawRequestStatus']=status
            status,decision=request('POST','/api/pto/'+pto['id']+'/decision',{'decision':0,'comment':'Disposable baseline probe'},token)
            observations['directHrApprovalStatus']=status
            _,employee=request('GET','/api/employees/'+employee_login['user']['employeeId'],token=token)
            observations['balanceAfterApproval']=employee['ptoBalanceHours']
        finally:
            if process is not None and process.poll() is None:
                process.terminate()
                try:process.wait(timeout=10)
                except subprocess.TimeoutExpired:process.kill();process.wait(timeout=10)
            observations['serverStopped']=process is None or process.poll() is not None
            observations['originalDatabaseOpened']=False
            observations['runtimeNote']='Original net8.0 assembly probed with DOTNET_ROLL_FORWARD=Major in this local environment.'
            (C/'baseline-probe.json').write_text(json.dumps(observations,indent=2),encoding='utf-8')
print(json.dumps(observations))
