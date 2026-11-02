"""Kiểm thử thực nghiệm với bộ kịch bản cố định (scenarios.json).

Trách nhiệm:
- Đọc nạp các kịch bản từ scenarios.json
- Gửi yêu cầu qua luồng gợi ý và so khớp kết quả với expected_top3
- Ghi nhận tỷ lệ trùng khớp và phân tích sai lệch nếu có

Mục tương ứng trong đề cương: Mục 5.2 - Đánh giá chất lượng xếp hạng.
"""

import json
from pathlib import Path
from typing import Any

import pytest

from app.data.repository import TutorRepository
from app.schemas.recommendation import RankedTutor
from app.schemas.search_request import SearchRequest
from app.schemas.tutor import TutorProfile
from app.scoring.eligibility import filter_eligible_candidates
from app.scoring.filters import filter_mandatory
from app.scoring.ranker import score_and_rank
from app.scoring.weights import compute_effective_weights

SCENARIOS_JSON_PATH = Path(__file__).resolve().parent / "scenarios.json"


def load_scenarios() -> list[dict[str, Any]]:
    """Nạp danh sách 14 kịch bản thực nghiệm từ `scenarios.json`."""
    raw = SCENARIOS_JSON_PATH.read_text(encoding="utf-8")
    data = json.loads(raw)
    assert isinstance(data, list)
    return data


def run_scenario_pipeline(
    scenario: dict[str, Any],
    tutors: list[TutorProfile],
) -> tuple[list[RankedTutor], int, list[str]]:
    """Chạy luồng lọc bắt buộc -> trọng số -> ngưỡng dữ liệu -> xếp hạng Top-3."""
    query = SearchRequest.model_validate(scenario["request"])
    qualified = filter_mandatory(tutors, query)
    if not qualified:
        return [], 0, []

    weights = compute_effective_weights(query)
    if weights.total <= 0:
        return [], len(qualified), []

    eligible, insufficient_ids = filter_eligible_candidates(qualified, weights)
    if not eligible:
        return [], len(qualified), insufficient_ids

    ranked = score_and_rank(eligible, query, weights, top_k=3)
    return ranked, len(qualified), insufficient_ids


def evaluate_scenario_match(
    system_top3: list[str],
    expected_top3: list[str],
) -> tuple[int, int, str]:
    """Đo số gia sư trùng khớp (0–3) theo quy ước tại `tests/scenarios/README.md`."""
    expected_len = len(expected_top3)
    if expected_len == 0:
        matched = 0
        label = "no_match (0/0)" if len(system_top3) == 0 else "lệch no_match"
        return matched, 0, label

    matched = len(set(system_top3[:expected_len]) & set(expected_top3))
    return matched, expected_len, f"{matched}/{expected_len}"


def format_scenarios_summary_table(
    scenarios: list[dict[str, Any]],
    tutors: list[TutorProfile],
) -> str:
    """Sinh bảng tổng hợp kết quả đối sánh 14 kịch bản thực nghiệm."""
    lines = [
        "| KB | Qua lọc | Kỳ vọng Top-3 | Hệ thống Top-3 | Điểm hệ thống | Độ khớp |",
        "|:---|---:|:---|:---|:---|:---:|",
    ]
    for sc in scenarios:
        sid = sc["id"]
        expected_top3: list[str] = sc["expected_top3"]
        ranked, qualified_count, _ = run_scenario_pipeline(sc, tutors)
        system_top3 = [r.tutor_id for r in ranked]
        scores_str = ", ".join(f"{r.tutor_id} ({r.total_score:.3f})" for r in ranked) or "(trống)"
        _, _, match_label = evaluate_scenario_match(system_top3, expected_top3)
        lines.append(
            f"| {sid} | {qualified_count} | {expected_top3} | {system_top3} | {scores_str} | {match_label} |"
        )
    return "\n".join(lines)


@pytest.fixture(scope="module")
def all_tutors() -> list[TutorProfile]:
    return TutorRepository().get_all()


@pytest.fixture(scope="module")
def all_scenarios() -> list[dict[str, Any]]:
    return load_scenarios()


def test_scenarios_file_has_all_14_cases(all_scenarios: list[dict[str, Any]]) -> None:
    """Xác nhận tệp `scenarios.json` có đúng 14 kịch bản KB01–KB14."""
    assert len(all_scenarios) == 14
    expected_ids = [f"KB{i:02d}" for i in range(1, 15)]
    assert [sc["id"] for sc in all_scenarios] == expected_ids


@pytest.mark.parametrize(
    "scenario_id",
    [f"KB{i:02d}" for i in range(1, 15)],
)
def test_each_scenario_matches_expected_top3(
    scenario_id: str,
    all_scenarios: list[dict[str, Any]],
    all_tutors: list[TutorProfile],
) -> None:
    """Chạy từng kịch bản KB01–KB14 qua bộ máy xếp hạng và kiểm tra khớp `expected_top3`."""
    scenario = next(sc for sc in all_scenarios if sc["id"] == scenario_id)
    expected_top3: list[str] = scenario["expected_top3"]

    ranked, qualified_count, insufficient_ids = run_scenario_pipeline(
        scenario, all_tutors
    )
    system_top3 = [r.tutor_id for r in ranked]
    matched, expected_len, _ = evaluate_scenario_match(system_top3, expected_top3)

    assert insufficient_ids == []

    if scenario_id == "KB05":
        assert qualified_count == 0
        assert expected_top3 == []
        assert system_top3 == []
    else:
        assert matched == expected_len
        assert system_top3 == expected_top3


def test_special_scenarios_scores_and_behaviors(
    all_scenarios: list[dict[str, Any]],
    all_tutors: list[TutorProfile],
) -> None:
    """Kiểm tra chi tiết các kịch bản đặc biệt: KB02, KB04, KB07, KB09, KB12."""
    by_id = {sc["id"]: sc for sc in all_scenarios}

    # KB02 & KB12: đồng điểm giữa GS-G11 và GS-G12, phá hòa theo tutor_id tăng dần
    ranked_kb02, _, _ = run_scenario_pipeline(by_id["KB02"], all_tutors)
    assert ranked_kb02[0].tutor_id == "GS-G11"
    assert ranked_kb02[1].tutor_id == "GS-G12"
    assert ranked_kb02[0].total_score == pytest.approx(ranked_kb02[1].total_score)

    ranked_kb12, _, _ = run_scenario_pipeline(by_id["KB12"], all_tutors)
    assert ranked_kb12[1].tutor_id == "GS-G11"
    assert ranked_kb12[2].tutor_id == "GS-G12"
    assert ranked_kb12[1].total_score == pytest.approx(ranked_kb12[2].total_score)

    # KB04: học online có time_slots -> 4 tiêu chí áp dụng, thứ hạng GS006 > GS020
    ranked_kb04, _, _ = run_scenario_pipeline(by_id["KB04"], all_tutors)
    assert [r.tutor_id for r in ranked_kb04] == ["GS006", "GS020"]
    assert ranked_kb04[0].criteria_scores["district"] is None
    assert ranked_kb04[0].total_score == pytest.approx(0.88625)
    assert ranked_kb04[1].total_score == pytest.approx(0.78625)

    # KB01 & KB12: gia sư thu thập thực tế (GS-T06, GS-T07) chưa có đánh giá -> s_rating = 0.5 và notes chứa "chưa có đánh giá"
    ranked_kb01, _, _ = run_scenario_pipeline(by_id["KB01"], all_tutors)
    assert ranked_kb01[2].tutor_id == "GS-T06"
    assert ranked_kb01[2].criteria_scores["rating"] == pytest.approx(0.5)
    assert ranked_kb01[2].notes == ["chưa có đánh giá"]
    assert ranked_kb12[0].tutor_id == "GS-T07"
    assert ranked_kb12[0].criteria_scores["rating"] == pytest.approx(0.5)
    assert ranked_kb12[0].notes == ["chưa có đánh giá"]

    # KB09: thiếu khung giờ -> availability là None, điểm chính xác 0.9275
    ranked_kb09, _, _ = run_scenario_pipeline(by_id["KB09"], all_tutors)
    assert ranked_kb09[0].tutor_id == "GS-G08"
    assert ranked_kb09[0].criteria_scores["availability"] is None
    assert ranked_kb09[0].total_score == pytest.approx(0.9275)


def test_generate_summary_comparison_table_without_crashing(
    all_scenarios: list[dict[str, Any]],
    all_tutors: list[TutorProfile],
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Xuất bảng tổng hợp đối sánh 14 kịch bản ra stdout phục vụ báo cáo thực nghiệm."""
    table = format_scenarios_summary_table(all_scenarios, all_tutors)
    print("\n" + table)
    captured = capsys.readouterr()
    assert "KB01" in captured.out
    assert "KB14" in captured.out
    assert "no_match (0/0)" in captured.out
