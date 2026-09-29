from pathlib import Path
S=Path(__file__).resolve().parents[2]/'stage/ca549816cdd1'
p=S/'pyproject.toml';text=p.read_text()
for old,new in [('0.1.0','0.2.0'),('email-validator>=2.2.0','email-validator==2.3.0'),('fastapi>=0.116.0','fastapi==0.135.1'),('pydantic>=2.11.0','pydantic==2.13.4'),('sqlalchemy>=2.0.38','sqlalchemy==2.0.48'),('uvicorn>=0.35.0','uvicorn==0.42.0'),('httpx>=0.28.0','httpx==0.28.1'),('pytest>=8.4.0','pytest==9.0.2'),('"setuptools>=80", "wheel"','"setuptools==80.9.0", "wheel==0.45.1"')]:
    assert old in text;text=text.replace(old,new)
text=text.replace('  "pytest==9.0.2",', '  "pytest==9.0.2",\n  "playwright==1.59.0",')
text+='\n[tool.setuptools.package-data]\napp = ["web/*.html", "web/*.css", "web/*.js"]\n\n[tool.ruff]\ntarget-version = "py313"\nline-length = 100\n\n[tool.ruff.lint]\nselect = ["F", "I"]\n'
p.write_text(text,encoding='utf-8')
p=S/'app/api.py';text=p.read_text();text=text.replace('from fastapi import Depends, FastAPI, HTTPException, Request','from fastapi import Depends, FastAPI, HTTPException, Request, Query')
text=text.replace('payload.email, payload.password, payload.display_name)', 'payload.email, payload.password, payload.display_name, session_days=cfg.session_days)')
text=text.replace('payload.email, payload.password, payload.org_slug)', 'payload.email, payload.password, payload.org_slug, session_days=cfg.session_days)')
text=text.replace('payload.admin_email, payload.admin_password, payload.admin_display_name)', 'payload.admin_email, payload.admin_password, payload.admin_display_name, session_days=cfg.session_days)')
for name,params in [('list_users',''),('list_tokens',''),('alerts_evaluate',''),('alerts_deliveries','alert_id: int, '),('pipelines_runs','pipeline_id: int, ')]:
    old=f'def {name}({params}principal:';new=f'def {name}({params}limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0, le=10000), principal:';assert old in text;text=text.replace(old,new)
text=text.replace('.where(Membership.organization_id == principal.organization_id)\n', '.where(Membership.organization_id == principal.organization_id).order_by(User.id).offset(offset).limit(limit)\n')
text=text.replace('select(ApiToken).where(ApiToken.organization_id == principal.organization_id)).all()', 'select(ApiToken).where(ApiToken.organization_id == principal.organization_id).order_by(ApiToken.id).offset(offset).limit(limit)).all()')
text=text.replace('AlertRule.enabled.is_(True))).all()', 'AlertRule.enabled.is_(True)).order_by(AlertRule.id).offset(offset).limit(limit)).all()')
text=text.replace('select(AlertDelivery).where(AlertDelivery.alert_rule_id == alert_id)).all()', 'select(AlertDelivery).where(AlertDelivery.alert_rule_id == alert_id).order_by(AlertDelivery.id.desc()).offset(offset).limit(limit)).all()')
text=text.replace('.order_by(PipelineRun.started_at.desc())).all()', '.order_by(PipelineRun.started_at.desc(), PipelineRun.id.desc()).offset(offset).limit(limit)).all()')
p.write_text(text,encoding='utf-8')
p=S/'app/services/auth.py';text=p.read_text()
text=text.replace('display_name: str) -> tuple[Organization, User, str]:', 'display_name: str, session_days: int = 7) -> tuple[Organization, User, str]:')
text=text.replace('audit_action="bootstrap")','audit_action="bootstrap", session_days=session_days)')
text=text.replace('audit_action: str = "organization.create",','audit_action: str = "organization.create",\n    session_days: int = 7,')
text=text.replace('"org_admin", [], user.id)', '"org_admin", [], user.id, expires_in_days=session_days)')
text=text.replace('password: str, org_slug: str) -> tuple[Organization, User, str, str]:', 'password: str, org_slug: str, session_days: int = 7) -> tuple[Organization, User, str, str]:')
text=text.replace('membership.role, [], user.id)', 'membership.role, [], user.id, expires_in_days=session_days)')
p.write_text(text,encoding='utf-8')
p=S/'app/deps.py';text=p.read_text();anchor='    user_email = None\n';assert anchor in text
text=text.replace(anchor,'''    if token.token_type.value == 'ingest' and (token.role != 'service_account' or not token.scopes or not set(token.scopes) <= {'logs:write','metrics:write','traces:write'}):
        raise HTTPException(status_code=401, detail='Legacy ingest token needs rotation to explicit write scopes')
''' +anchor);p.write_text(text,encoding='utf-8')
p=S/'app/web/index.html';text=p.read_text();status='<p id="status" role="status" aria-live="polite"></p>';assert text.count(status)==1;text=text.replace(status,'');text=text.replace('<main>','<main>\n'+status);p.write_text(text,encoding='utf-8')
p=S/'app/web/styles.css';text=p.read_text();text=text.replace('position:sticky;bottom:12px;', 'position:sticky;top:12px;z-index:2;');p.write_text(text,encoding='utf-8')
print('Staged tested dependency pins, package assets, bounded histories, session expiry and status placement')
