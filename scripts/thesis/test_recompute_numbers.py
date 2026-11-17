"""Kiểm thử cho script tính lại và đối chiếu số liệu báo cáo với mã nguồn."""

from __future__ import annotations

from pathlib import Path

from recompute_numbers import (
    ClaimRow,
    recompute_14_scenarios,
    recompute_sensitivity_checks,
    verify_extra_report_claims,
    verify_tutors_and_versions,
)


def test_recompute_14_scenarios_returns_all_kb01_to_kb14() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    results = recompute_14_scenarios(repo_root)
    assert [row["id"] for row in results] == [f"KB{i:02d}" for i in range(1, 15)]
    kb01 = next(row for row in results if row["id"] == "KB01")
    assert kb01["qualified_count"] == 5
    assert kb01["top3_ids"] == ["GS-G01", "GS-G10", "GS-T06"]
    assert [round(s, 3) for s in kb01["scores"]] == [0.938, 0.745, 0.625]


def test_recompute_sensitivity_checks_produces_structured_claims() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    claims = recompute_sensitivity_checks(repo_root)
    assert len(claims) >= 10
    assert all(isinstance(c, ClaimRow) for c in claims)
    assert any(c.claim_id.startswith("SL-SEN-") for c in claims)


def test_verify_tutors_and_versions_checks_16_tutors_and_packages() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    claims = verify_tutors_and_versions(repo_root)
    assert any(c.claim_id == "SL-DATA-01" and c.matched == "KHỚP" for c in claims)
    assert any(c.claim_id.startswith("SL-VER-") for c in claims)


def test_verify_extra_report_claims_checks_slots_presets_and_19_queries() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    claims = verify_extra_report_claims(repo_root)
    ids = {c.claim_id for c in claims}
    assert "SL-CH5-SLOTS" in ids
    assert "SL-CH6-19Q" in ids
    assert "SL-CH6-PRESETS" in ids
    assert "SL-CH4-FIG43" in ids
    assert "SL-CH5-TESTS-PERFILE" in ids
    assert "SL-CH5-COV" in ids
    lat = next(c for c in claims if c.claim_id == "SL-CH5-LATENCY")
    assert lat.matched == "KHỚP"
