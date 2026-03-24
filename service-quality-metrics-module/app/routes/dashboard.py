from __future__ import annotations

from datetime import datetime, timedelta

from flask import Blueprint, jsonify

from app.services.metric_service import MetricService, RequestRecord

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@bp.get("/summary")
def summary():
    now = datetime(2026, 3, 1, 12, 0)
    records = [
        RequestRecord(
            created_at=now - timedelta(minutes=55),
            resolved_at=now,
            priority="high",
            contact="client-1",
            sla_minutes=120,
        ),
        RequestRecord(
            created_at=now - timedelta(minutes=180),
            resolved_at=now,
            priority="normal",
            contact="client-2",
            sla_minutes=240,
        ),
    ]
    payload = MetricService.build_dashboard_summary([5, 4, 5], [10, 9, 8], records)
    return jsonify(payload)
