from pathlib import Path
S=Path(__file__).resolve().parents[2]/'stage/ca549816cdd1'
p=S/'app/services/alerts.py';text=p.read_text()
text=text.replace('import json\nimport urllib.error\nimport urllib.request\n','import hashlib\n')
text=text.replace('from sqlalchemy.orm import Session','from fastapi import HTTPException\nfrom sqlalchemy.orm import Session\nfrom app.config import settings\nfrom app.permissions import has_permission\nfrom app.services.notification_outbox import validate_destination')
text=text.replace('def evaluate_alert_rule(db: Session, principal: Principal, alert: AlertRule) -> dict:\n    condition = alert.condition', '''def evaluate_alert_rule(db: Session, principal: Principal, alert: AlertRule, cfg=settings) -> dict:
    if not has_permission(principal.role, principal.scopes, alert.module + ':read'):
        raise HTTPException(status_code=403, detail='Alert evaluation requires read permission for its telemetry module')
    from app.contracts import validate_alert_condition
    try: condition = validate_alert_condition(alert.module, alert.condition)
    except (ValueError, KeyError) as exc: raise HTTPException(status_code=422, detail='Stored alert configuration needs repair before evaluation') from exc''')
text=text.replace('scan_cap=50_000, row_cap=1_000', 'scan_cap=cfg.query_scan_limit, row_cap=cfg.query_row_limit')
text=text.replace('value = float(len(result["results"]))','value = float(result["matched_rows"])')
text=text.replace('value = max(durations) if durations else 0.0','value = result["max_duration_ms"]')
text=text.replace('def dispatch_notifications(db: Session, alert: AlertRule, evaluation: dict) -> dict:', 'def dispatch_notifications(db: Session, alert: AlertRule, evaluation: dict, cfg=settings) -> dict:')
text=text.replace('fingerprint = f"{alert.id}:{evaluation[\'value\']}:{evaluation[\'threshold\']}:{evaluation[\'operator\']}"', 'fingerprint = hashlib.sha256(f"{alert.id}:{evaluation[\'value\']}:{evaluation[\'threshold\']}:{evaluation[\'operator\']}".encode()).hexdigest()')
start=text.index('        if channel_type in {"webhook", "slack"} and destination.startswith("http"):')
end=text.index('        delivery = AlertDelivery(',start)
text=text[:start]+'''        if cfg.allow_notifications and channel_type in {'webhook', 'slack'}:
            try: validate_destination(destination, cfg)
            except ValueError as exc: raise HTTPException(status_code=422, detail=str(exc)) from exc
            status_value = 'pending'
''' +text[end:]
text=text.replace('def run_alert(db: Session, principal: Principal, alert: AlertRule) -> dict:\n    evaluation = evaluate_alert_rule(db, principal, alert)', '''def run_alert(db: Session, principal: Principal, alert: AlertRule, cfg=settings) -> dict:
    if not alert.enabled: raise HTTPException(status_code=409, detail='Enable this alert before evaluating it')
    evaluation = evaluate_alert_rule(db, principal, alert, cfg)''')
text=text.replace('dispatch_notifications(db, alert, evaluation)', 'dispatch_notifications(db, alert, evaluation, cfg)')
p.write_text(text,encoding='utf-8')
p=S/'app/api.py';text=p.read_text();text=text.replace('run_alert(db, principal, alert)', 'run_alert(db, principal, alert, cfg)');p.write_text(text,encoding='utf-8')
p=S/'app/services/queries.py';text=p.read_text()
text=text.replace('    filtered = filtered[:limit]', '    matched_rows = len(filtered)\n    filtered = filtered[:limit]')
text=text.replace('        "histogram":', '        "matched_rows": matched_rows,\n        "histogram":')
text=text.replace('return {"series": series[:limit],', 'return {"series": series[-limit:],')
text=text.replace('return {"results": results[:limit], "scanned_rows": count,', 'return {"results": results[:limit], "scanned_rows": count, "max_duration_ms": max((item["duration_ms"] for item in results), default=0.0),')
p.write_text(text,encoding='utf-8')
p=S/'app/contracts.py';text=p.read_text();text=text.replace('    request = schema.model_validate(query)', '    request = schema.model_validate(query)\n    if module == "metrics" and request.group_by:\n        raise ValueError("Metric alerts require an ungrouped aggregate")');p.write_text(text,encoding='utf-8')
p=S/'app/crud.py';text=p.read_text();old='        if resource.model is AlertRule: db.execute(delete(AlertDelivery).where(AlertDelivery.alert_rule_id == record.id))';new='''        if resource.model is AlertRule:
            unresolved = db.scalar(select(AlertDelivery.id).where(AlertDelivery.alert_rule_id == record.id, AlertDelivery.status.in_(['pending','sending','uncertain'])).limit(1))
            if unresolved is not None: raise HTTPException(status_code=409, detail='Resolve pending or uncertain deliveries before deleting this alert')
            db.execute(delete(AlertDelivery).where(AlertDelivery.alert_rule_id == record.id))''';assert old in text;text=text.replace(old,new);p.write_text(text,encoding='utf-8')
print('Staged durable notification outbox; no network request made')
