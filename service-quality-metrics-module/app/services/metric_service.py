from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable


@dataclass(frozen=True)
class RequestRecord:
    created_at: datetime
    resolved_at: datetime
    priority: str
    contact: str
    sla_minutes: int


class MetricService:
    """Сервис расчёта ключевых метрик качества обслуживания."""

    @staticmethod
    def calculate_csat(scores: Iterable[int]) -> float:
        values = list(scores)
        if not values:
            return 0.0
        return round(sum(values) / len(values), 2)

    @staticmethod
    def calculate_nps(scores: Iterable[int]) -> int:
        values = list(scores)
        if not values:
            return 0
        promoters = sum(1 for score in values if score >= 9)
        detractors = sum(1 for score in values if score <= 6)
        result = ((promoters - detractors) / len(values)) * 100
        return round(result)

    @staticmethod
    def calculate_aht(records: Iterable[RequestRecord]) -> float:
        values = list(records)
        if not values:
            return 0.0
        total_minutes = sum(
            (record.resolved_at - record.created_at).total_seconds() / 60
            for record in values
        )
        return round(total_minutes / len(values), 2)

    @staticmethod
    def calculate_fcr(records: Iterable[RequestRecord]) -> float:
        values = list(records)
        if not values:
            return 0.0

        contacts_count: dict[str, int] = {}
        for record in values:
            contacts_count[record.contact] = contacts_count.get(record.contact, 0) + 1

        first_contact_resolved = sum(
            1 for record in values if contacts_count[record.contact] == 1
        )
        return round((first_contact_resolved / len(values)) * 100, 2)

    @staticmethod
    def calculate_sla_compliance(records: Iterable[RequestRecord]) -> float:
        values = list(records)
        if not values:
            return 0.0
        within_sla = 0
        for record in values:
            duration_minutes = (record.resolved_at - record.created_at).total_seconds() / 60
            if duration_minutes <= record.sla_minutes:
                within_sla += 1
        return round((within_sla / len(values)) * 100, 2)

    @classmethod
    def build_dashboard_summary(
        cls,
        csat_scores: Iterable[int],
        nps_scores: Iterable[int],
        requests: Iterable[RequestRecord],
    ) -> dict[str, float | int]:
        request_values = list(requests)
        return {
            "csat": cls.calculate_csat(csat_scores),
            "nps": cls.calculate_nps(nps_scores),
            "aht": cls.calculate_aht(request_values),
            "fcr": cls.calculate_fcr(request_values),
            "sla_compliance": cls.calculate_sla_compliance(request_values),
            "requests_total": len(request_values),
        }
