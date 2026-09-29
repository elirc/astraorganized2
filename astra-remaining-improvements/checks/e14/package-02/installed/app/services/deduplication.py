"""Bounded, organization-scoped ingestion checks inside the write transaction."""

from fastapi import HTTPException
from sqlalchemy import select

from app.models import TraceSpan


def unseen_items(db, organization_id, model, items):
    seen = set()
    fresh = []
    for item in items:
        if model is TraceSpan:
            key = (item["trace_id"], item["span_id"])
            existing = select(model.id).where(
                model.organization_id == organization_id,
                model.trace_id == key[0],
                model.span_id == key[1],
            )
        else:
            key = item.get("dedupe_key")
            existing = select(model.id).where(
                model.organization_id == organization_id, model.dedupe_key == key
            )
        if key is not None and (key in seen or db.scalar(existing) is not None):
            continue
        if key is not None:
            seen.add(key)
        fresh.append(item)
    return fresh, len(items) - len(fresh)


def validate_trace_graph(db, organization_id, spans):
    for trace_id in {span["trace_id"] for span in spans}:
        stored = db.execute(
            select(TraceSpan.span_id, TraceSpan.parent_span_id)
            .where(
                TraceSpan.organization_id == organization_id,
                TraceSpan.trace_id == trace_id,
            )
            .limit(1001)
        ).all()
        graph = dict(stored)
        graph.update(
            {
                span["span_id"]: span.get("parent_span_id")
                for span in spans
                if span["trace_id"] == trace_id
            }
        )
        if len(graph) > 1000:
            raise HTTPException(status_code=422, detail="A trace may contain at most 1000 spans")
        for node in graph:
            visited = set()
            while node in graph:
                if node in visited:
                    raise HTTPException(status_code=422, detail="Trace parent cycle detected")
                visited.add(node)
                if len(visited) > 64:
                    raise HTTPException(
                        status_code=422, detail="Trace depth may not exceed 64 spans"
                    )
                node = graph[node]
