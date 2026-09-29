from pathlib import Path
S=Path(__file__).resolve().parents[2]/'stage/ca549816cdd1'
p=S/'app/services/queries.py';text=p.read_text()
text=text.replace('import json\n','import json\nimport math\n')
text=text.replace('from sqlalchemy import func, or_, select','from sqlalchemy import func, select')
text=text.replace('from app.security import Principal','from app.security import Principal\nfrom app.permissions import has_permission\nfrom app.services.query_safety import bounded_rows, execute_subset')
text=text.replace('    rows = db.scalars(query.order_by(LogEvent.event_ts.desc()).limit(limit)).all()', '    rows = bounded_rows(db.scalars(query.order_by(LogEvent.event_ts.desc(), LogEvent.id.desc()).limit(scan_cap)).yield_per(100))')
text=text.replace('            value = getattr(row, key, None)', '            value = getattr(row, key, None) if key in {"level", "message", "service", "trace_id", "span_id"} else None')
text=text.replace('    histogram: dict[str, int] = defaultdict(int)', '    filtered = filtered[:limit]\n    histogram: dict[str, int] = defaultdict(int)')
text=text.replace('limit: int, scan_cap: int, row_cap: int) -> dict[str, Any]:\n    validate_time_range(start_time, end_time)', 'limit: int, scan_cap: int, row_cap: int, timeout_ms: int = 5000) -> dict[str, Any]:\n    validate_time_range(start_time, end_time)')
old='    if SQL_BLOCKLIST.search(query) or not query.strip().lower().startswith("select "):\n        raise HTTPException(status_code=400, detail="Only bounded SELECT queries are allowed")\n'
assert text.count(old)==2;text=text.replace(old,'')
text=text.replace('    rows = db.scalars(scoped_query.limit(scan_cap)).all()', '    rows = bounded_rows(db.scalars(scoped_query.limit(scan_cap)).yield_per(100))')
for kind,table in [('log','log_events'),('metrics','metric_points')]:
    old=f'    conn = _build_sqlite_subset_{kind}(rows)\n    cursor = conn.execute(query)\n    columns = [col[0] for col in cursor.description]\n    records = cursor.fetchmany(effective_limit)\n    conn.close()'
    assert old in text
    text=text.replace(old,f'    conn = _build_sqlite_subset_{kind}(rows)\n    columns, records = execute_subset(conn, "{table}", query, effective_limit, timeout_ms)')
text=text.replace('rows = [row for row in db.scalars(query.order_by(MetricPoint.ts.asc()).limit(scan_cap)).all() if _matches_labels(row.labels, req.filters)]', 'rows = [row for row in bounded_rows(db.scalars(query.order_by(MetricPoint.ts.asc(), MetricPoint.id.asc()).limit(scan_cap)).yield_per(100)) if _matches_labels(row.labels, req.filters)]')
text=text.replace('group_values = tuple(row.labels.get(key, "unknown") for key in req.group_by)', 'group_values = tuple(json.dumps(row.labels.get(key), sort_keys=True, allow_nan=False) for key in req.group_by)')
text=text.replace('labels = {key: bucket_key[index + 1] for index, key in enumerate(req.group_by)}', 'if not math.isfinite(value): raise HTTPException(status_code=400, detail="Aggregation exceeded the finite numeric range")\n        labels = {key: json.loads(bucket_key[index + 1]) for index, key in enumerate(req.group_by)}')
text=text.replace('            key, value = pair.split("=", 1)\n            labels[key.strip()] = value.strip().strip(\'"\')', '''            label = re.fullmatch(r'\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*("(?:[^"\\\\]|\\\\.)*")\s*', pair)
            if not label or label.group(1) in labels:
                raise HTTPException(status_code=400, detail='Labels must be unique name="value" pairs')
            try: labels[label.group(1)] = json.loads(label.group(2))
            except ValueError as exc: raise HTTPException(status_code=400, detail='Invalid label string') from exc''')
text=text.replace('    rows = db.scalars(query.order_by(TraceSpan.start_ts.desc()).limit(limit)).all()', '    rows = bounded_rows(db.scalars(query.order_by(TraceSpan.start_ts.desc(), TraceSpan.id.desc()).limit(scan_cap)).yield_per(100))')
text=text.replace('    return {"results": results[:limit], "scanned_rows": count}', '    return {"results": results[:limit], "scanned_rows": count, "span_scope": "Counts and durations describe spans matching the request filters and time window"}')
start=text.index('def _build_trace_tree(');end=text.index('\ndef trace_detail(',start)
text=text[:start]+'''def _build_trace_tree(spans: list[TraceSpan]) -> list[dict[str, Any]]:
    parents = {span.span_id: span.parent_span_id for span in spans}
    for start in parents:
        seen = set()
        node = start
        while node in parents:
            if node in seen or len(seen) >= 64:
                raise HTTPException(status_code=400, detail='Stored trace contains a cycle or exceeds depth 64')
            seen.add(node)
            node = parents[node]
    nodes = {span.span_id: {
        'span_id': span.span_id, 'parent_span_id': span.parent_span_id,
        'service_name': span.service_name, 'operation_name': span.operation_name,
        'status': span.status, 'duration_ms': span.duration_ms,
        'start_ts': span.start_ts, 'end_ts': span.end_ts,
        'attributes': span.attributes, 'children': [],
    } for span in spans}
    roots = []
    for span in spans:
        if span.parent_span_id in nodes:
            nodes[span.parent_span_id]['children'].append(nodes[span.span_id])
        else:
            roots.append(nodes[span.span_id])
    return roots

''' +text[end:]
text=text.replace('    spans = db.scalars(\n', '    spans = bounded_rows(db.scalars(\n')
text=text.replace('order_by(TraceSpan.start_ts.asc())\n    ).all()', 'order_by(TraceSpan.start_ts.asc(), TraceSpan.id.asc()).limit(1001)\n    ).yield_per(100))\n    if len(spans) > 1000: raise HTTPException(status_code=400, detail="Stored trace exceeds 1000 spans")')
text=text.replace('    span_ids = [span.span_id for span in spans]\n    logs = db.scalars(', '    logs = bounded_rows(db.scalars(')
text=text.replace('            or_(LogEvent.trace_id == trace_id, LogEvent.span_id.in_(span_ids)),', '            LogEvent.trace_id == trace_id,')
text=text.replace('        ).order_by(LogEvent.event_ts.asc())\n    ).all()', '        ).order_by(LogEvent.event_ts.asc(), LogEvent.id.asc()).limit(1001)\n    ).yield_per(100)) if has_permission(principal.role, principal.scopes, "logs:read") else []')
text=text.replace('        "trace_id": trace_id,\n        "span_tree":', '        "trace_id": trace_id,\n        "correlated_logs_truncated": len(logs) > 1000,\n        "correlated_logs_authorized": has_permission(principal.role, principal.scopes, "logs:read"),\n        "span_tree":')
text=text.replace('            for log in logs\n', '            for log in logs[:1000]\n')
p.write_text(text,encoding='utf-8')
p=S/'app/api.py';text=p.read_text()
for func in ['execute_log_sql','execute_metric_sql']:
    old=f'return {func}(db, principal, payload.start_time, payload.end_time, payload.query, payload.limit, cfg.query_scan_limit, cfg.query_row_limit)'
    assert old in text
    text=text.replace(old,old[:-1]+', cfg.query_timeout_ms)')
p.write_text(text,encoding='utf-8')
print('Staged bounded SQL, filtered searches and trace correlation changes')
