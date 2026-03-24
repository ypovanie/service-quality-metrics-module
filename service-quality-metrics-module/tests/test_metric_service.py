from datetime import datetime, timedelta

from app.services.metric_service import MetricService, RequestRecord


BASE = datetime(2026, 3, 1, 12, 0)


def make_record(minutes: int, contact: str, sla_minutes: int = 120) -> RequestRecord:
    return RequestRecord(
        created_at=BASE - timedelta(minutes=minutes),
        resolved_at=BASE,
        priority="normal",
        contact=contact,
        sla_minutes=sla_minutes,
    )


def test_calculate_csat_returns_average():
    assert MetricService.calculate_csat([5, 4, 5, 3]) == 4.25


def test_calculate_csat_empty_returns_zero():
    assert MetricService.calculate_csat([]) == 0.0


def test_calculate_nps_returns_expected_score():
    assert MetricService.calculate_nps([10, 9, 8, 6, 5]) == 0


def test_calculate_aht_returns_minutes_average():
    records = [make_record(60, "c1"), make_record(30, "c2")]
    assert MetricService.calculate_aht(records) == 45.0


def test_calculate_fcr_for_unique_contacts():
    records = [make_record(50, "c1"), make_record(40, "c2")]
    assert MetricService.calculate_fcr(records) == 100.0


def test_calculate_fcr_with_repeat_contact():
    records = [make_record(50, "c1"), make_record(40, "c1"), make_record(20, "c2")]
    assert MetricService.calculate_fcr(records) == 33.33


def test_calculate_sla_compliance_detects_violation():
    records = [make_record(90, "c1", 120), make_record(180, "c2", 120)]
    assert MetricService.calculate_sla_compliance(records) == 50.0


def test_build_dashboard_summary_contains_all_metrics():
    records = [make_record(60, "c1", 120), make_record(180, "c2", 240)]
    summary = MetricService.build_dashboard_summary([5, 4], [10, 2], records)
    assert summary == {
        "csat": 4.5,
        "nps": 0,
        "aht": 120.0,
        "fcr": 100.0,
        "sla_compliance": 100.0,
        "requests_total": 2,
    }
