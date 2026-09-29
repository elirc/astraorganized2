"""One-shot, staged-only edits. Original folders are never opened here."""
from pathlib import Path

S = Path(__file__).resolve().parents[2] / 'stage/ca549816cdd1'
p = S / 'app/services/ingestion.py'
text = p.read_text()
text = text.replace('from sqlalchemy import select', 'from sqlalchemy import select, text')
text = text.replace('from app.models import LogEvent, MetricPoint, TraceSpan', 'from app.models import LogEvent, MetricPoint, TraceSpan\nfrom app.services.deduplication import unseen_items, validate_trace_graph')
for name, variable, model, kind in [('logs','events','LogEvent','logs'), ('metrics','points','MetricPoint','metrics'), ('traces','spans','TraceSpan','traces')]:
    marker = f'    stream = get_stream_or_404(db, principal.organization_id, stream_name, "{kind}")'
    assert marker in text
    text = text.replace(marker, '    db.execute(text("BEGIN IMMEDIATE"))\n' + marker)
    old = f'    transformed, {"derived_metrics" if kind == "logs" else "_"} = apply_pipelines(db, principal.organization_id, "{kind}", {variable})\n    accepted = 0\n    skipped = 0'
    new = f'    fresh, skipped = unseen_items(db, principal.organization_id, {model}, {variable})\n'
    if kind == 'traces': new += '    validate_trace_graph(db, principal.organization_id, fresh)\n'
    new += f'    transformed, {"derived_metrics" if kind == "logs" else "_"} = apply_pipelines(db, principal.organization_id, "{kind}", fresh)\n    accepted = 0'
    assert old in text
    text = text.replace(old, new)
text = text.replace('    db.commit()\n    maybe_enforce_retention(db, request)', '    db.flush()\n    maybe_enforce_retention(db, request, principal.organization_id)\n    db.commit()')
p.write_text(text, encoding='utf-8')

p = S / 'app/services/common.py'; text = p.read_text()
text = text.replace('def maybe_enforce_retention(db: Session, request: Request) -> None:', 'def maybe_enforce_retention(db: Session, request: Request, organization_id: int) -> None:')
start = text.index('    last_run = getattr(request.app.state, "retention_last_run", None)')
end = text.index('    for stream in streams:', start)
text = text[:start] + '    now = utcnow()\n    streams = db.scalars(select(Stream).where(Stream.organization_id == organization_id)).all()\n' + text[end:]
assert text.endswith('    db.commit()\n')
text = text[:-len('    db.commit()\n')]
p.write_text(text, encoding='utf-8')

p = S / 'app/services/pipelines.py'; text = p.read_text()
text = text.replace('from app.models import Pipeline, PipelineRun', 'from app.models import Pipeline, PipelineRun\nfrom app.schemas import LogEventIn, MetricPointIn, TraceSpanIn\nfrom app.services.common import get_stream_or_404')
text = text.replace('            Pipeline.enabled.is_(True),\n        )', '            Pipeline.enabled.is_(True),\n        ).order_by(Pipeline.id)')
text = text.replace('target = current.setdefault("attributes", current.get("labels", {}))', 'target = current.setdefault("labels" if pipeline.source_type == "metrics" else "attributes", {})')
text = text.replace('items: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:\n    pipelines = _load_pipelines(db, organization_id, source_type)', 'items: list[dict[str, Any]], *, selected: Pipeline | None = None) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:\n    pipelines = [selected] if selected is not None else _load_pipelines(db, organization_id, source_type)')
text = text.replace('        dropped = 0\n', '        dropped = 0\n        pipeline_derived = []\n')
text = text.replace('                next_items.append(updated)\n                all_derived.extend(derived)', '''                route = updated.pop('_stream_name', None)
                schema = {'logs': LogEventIn, 'metrics': MetricPointIn, 'traces': TraceSpanIn}[source_type]
                updated = schema.model_validate(updated).model_dump()
                if route:
                    get_stream_or_404(db, organization_id, route, source_type)
                    updated['_stream_name'] = route
                checked_derived = [MetricPointIn.model_validate(metric).model_dump() for metric in derived]
                if checked_derived:
                    get_stream_or_404(db, organization_id, 'metrics-default', 'metrics')
                next_items.append(updated)
                pipeline_derived.extend(checked_derived)''')
text = text.replace('            processed = next_items', '            processed = next_items\n            all_derived.extend(pipeline_derived)')
text = text.replace('except Exception as exc:', 'except (ValueError, TypeError, HTTPException):')
text = text.replace('run.error_message = str(exc)', 'run.error_message = "Transformation failed validation; this pipeline was skipped for the whole batch"')
text = text.replace('    db.commit()\n    return processed, all_derived', '    return processed, all_derived')
text = text.replace('    items = sample_payload or []\n    processed, derived = apply_pipelines(db, principal.organization_id, pipeline.source_type, items)', '''    from fastapi.exceptions import RequestValidationError
    from pydantic import ValidationError
    items = sample_payload or []
    if len(items) > 1000:
        raise HTTPException(status_code=422, detail='At most 1000 sample items are allowed')
    schema = {'logs': LogEventIn, 'metrics': MetricPointIn, 'traces': TraceSpanIn}[pipeline.source_type]
    try:
        items = [schema.model_validate(item).model_dump() for item in items]
    except ValidationError as exc:
        raise RequestValidationError(exc.errors()) from exc
    processed, derived = apply_pipelines(db, principal.organization_id, pipeline.source_type, items, selected=pipeline)
    db.commit()''')
p.write_text(text, encoding='utf-8')
print('Staged ingestion/pipeline changes applied')
