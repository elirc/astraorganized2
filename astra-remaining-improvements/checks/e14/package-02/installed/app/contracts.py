"""Validate executable configuration before it becomes a stored database row."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import TypeAdapter

from app.schemas import (
    MetricPointIn,
    MetricsQueryRequest,
    Name,
    RequestModel,
    SearchRequest,
    StreamName,
    TraceSearchRequest,
    bounded_json,
)


class Comparison(RequestModel):
    operator: Literal["gt", "gte", "lt", "lte", "eq"] = "gte"
    threshold: float = 1


def validate_alert_condition(module: str, value: dict[str, Any]) -> dict[str, Any]:
    bounded_json(value)
    comparison = Comparison.model_validate(
        {key: value[key] for key in ("operator", "threshold") if key in value}
    )
    query = {key: item for key, item in value.items() if key not in ("operator", "threshold")}
    schema = {"logs": SearchRequest, "metrics": MetricsQueryRequest, "traces": TraceSearchRequest}[
        module
    ]
    request = schema.model_validate(query)
    if module == "metrics" and request.group_by:
        raise ValueError("Metric alerts require an ungrouped aggregate")
    return {**request.model_dump(mode="json"), **comparison.model_dump(mode="json")}


def validate_pipeline_definition(source_type: str, value: dict[str, Any]) -> dict[str, Any]:
    bounded_json(value)
    if (
        set(value) != {"steps"}
        or not isinstance(value["steps"], list)
        or not 1 <= len(value["steps"]) <= 20
    ):
        raise ValueError("Definition must contain only steps, with 1 to 20 entries")
    required = {
        "enrich": {"fields"},
        "redact": {"fields"},
        "filter_equals": {"field", "value"},
        "normalize_field": {"from", "to"},
        "route_stream": {"stream"},
        "logs_to_metric": {"metric_name", "field"},
    }
    for step in value["steps"]:
        if not isinstance(step, dict) or step.get("type") not in required:
            raise ValueError("Unsupported pipeline step")
        kind = step["type"]
        optional = {"labels", "unit"} if kind == "logs_to_metric" else set()
        if not required[kind] <= step.keys() or step.keys() - {"type"} - required[kind] - optional:
            raise ValueError(f"Invalid fields for {kind}")
        for key in ("field", "from", "to"):
            if key in step:
                TypeAdapter(Name).validate_python(step[key])
        if kind == "enrich":
            if not isinstance(step["fields"], dict) or not step["fields"]:
                raise ValueError("Enrich fields must be a nonempty object")
            if source_type == "metrics" and any(
                item is not None and type(item) not in (str, int, float, bool)
                for item in step["fields"].values()
            ):
                raise ValueError("Metric labels must be scalar values")
        if kind == "redact":
            fields = step["fields"]
            if not isinstance(fields, list) or not fields or len(fields) > 64:
                raise ValueError("Redact fields must contain 1 to 64 names")
            for field in fields:
                TypeAdapter(Name).validate_python(field)
        if kind == "route_stream":
            TypeAdapter(StreamName).validate_python(step["stream"])
        if kind == "logs_to_metric":
            if source_type != "logs":
                raise ValueError("logs_to_metric requires a logs source")
            MetricPointIn.model_validate(
                {
                    "timestamp": "2026-01-01T00:00:00Z",
                    "value": 0,
                    "metric_name": step["metric_name"],
                    "labels": step.get("labels", {}),
                    "unit": step.get("unit"),
                }
            )
    return value
