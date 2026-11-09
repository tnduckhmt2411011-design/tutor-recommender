"""Kiểm thử thực nghiệm khảo sát độ nhạy tham số phục vụ Mục 5.2.

Đề tài: Hệ thống khuyến nghị gia sư dựa trên phương pháp Content-Base Filtering
Bao gồm đúng 10 bài test T1–T10 khảo sát:
- T1: Tái lập baseline với delta=0.5, E_max=8 qua cơ chế patch (khớp 14/14 expected_top3)
- T2: Hiệu lực của patch (chống vô hiệu hóa âm thầm)
- T3: Quét delta trên 6 giá trị (bảo toàn chặn, tất định, thứ hạng liên tục)
- T4: Đơn điệu của điểm tổng hợp S theo delta (không giảm khi delta tăng)
- T5: Quét E_max trên 5 giá trị (bảo toàn chặn, tất định, thứ hạng liên tục)
- T6: Đơn điệu của điểm tổng hợp S theo E_max (không tăng khi E_max tăng)
- T7: Biến động ngân sách +-5% (bảo toàn tập ứng viên, đơn điệu theo ngân sách)
- T8: Biến động ngân sách +-10%
- T9: Biến động ngân sách +-20% và chuỗi đơn điệu đủ 7 mức
- T10: Khảo sát 4 bộ mức ưu tiên (Mặc định, Khu vực, Học phí, KN & Đánh giá)

Khối if __name__ == '__main__' sinh tệp dữ liệu thô:
docs/thesis/report/muc-5.2-ket-qua-tho.json (UTF-8, ensure_ascii=False).
"""

import contextlib
import json
import subprocess
from collections.abc import Generator
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

from app.data.repository import TutorRepository
from app.schemas.recommendation import RankedTutor
from app.schemas.search_request import SearchRequest
from app.schemas.tutor import TutorProfile
from app.scoring import criteria
from app.scoring.eligibility import filter_eligible_candidates
from app.scoring.filters import filter_mandatory
from app.scoring.ranker import score_and_rank
from app.scoring.weights import compute_effective_weights

SCENARIOS_JSON_PATH = Path(__file__).resolve().parent / "scenarios.json"

DELTA_VALUES: list[float] = [0.25, 0.30, 0.50, 0.70, 0.75, 1.00]
E_MAX_VALUES: list[int] = [5, 6, 8, 10, 12]
BUDGET_FACTORS: list[float] = [-0.20, -0.10, -0.05, 0.0, 0.05, 0.10, 0.20]

PRIORITY_SETS: dict[str, dict[str, str]] = {
    "default": {
        "fee": "medium",
        "district": "medium",
        "experience": "medium",
        "rating": "medium",
        "availability": "medium",
    },
    "prioritize_district": {
        "fee": "low",
        "district": "high",
        "experience": "low",
        "rating": "low",
        "availability": "low",
    },
    "prioritize_fee": {
        "fee": "high",
        "district": "low",
        "experience": "low",
        "rating": "low",
        "availability": "low",
    },
    "prioritize_experience_rating": {
        "fee": "low",
        "district": "low",
        "experience": "high",
        "rating": "high",
        "availability": "low",
    },
}

_ORIG_SCORE_FEE = criteria.score_fee
_ORIG_SCORE_EXPERIENCE = criteria.score_experience


@contextlib.contextmanager
def patch_scoring_params(
    delta: float = 0.5,
    e_max: float = 8.0,
) -> Generator[None, None, None]:
    """Bọc hàm tính điểm trong app.scoring.ranker để truyền delta và e_max biến thiên."""

    def _patched_fee(price: float, budget: float, **kwargs: Any) -> float:
        return _ORIG_SCORE_FEE(price, budget, delta=delta)

    def _patched_experience(years: float, **kwargs: Any) -> float:
        return _ORIG_SCORE_EXPERIENCE(years, e_max=e_max)

    with (
        patch("app.scoring.ranker.score_fee", side_effect=_patched_fee),
        patch(
            "app.scoring.ranker.score_experience",
            side_effect=_patched_experience,
        ),
    ):
        yield


def load_scenarios() -> list[dict[str, Any]]:
    """Nạp danh sách 14 kịch bản thực nghiệm từ scenarios.json."""
    raw = SCENARIOS_JSON_PATH.read_text(encoding="utf-8")
    data = json.loads(raw)
    assert isinstance(data, list)
    return data


def run_sensitivity_pipeline(
    scenario: dict[str, Any],
    tutors: list[TutorProfile],
    request_override: dict[str, Any] | None = None,
    top_k: int = 20,
) -> tuple[list[RankedTutor], int, list[str]]:
    """Chạy toàn bộ pipeline lọc -> trọng số -> ngưỡng dữ liệu -> xếp hạng Top-k."""
    req_data = dict(scenario["request"])
    if request_override:
        req_data.update(request_override)

    query = SearchRequest.model_validate(req_data)
    qualified = filter_mandatory(tutors, query)
    if not qualified:
        return [], 0, []

    weights = compute_effective_weights(query)
    if weights.total <= 0:
        return [], len(qualified), []

    eligible, insufficient_ids = filter_eligible_candidates(qualified, weights)
    if not eligible:
        return [], len(qualified), insufficient_ids

    ranked = score_and_rank(eligible, query, weights, top_k=top_k)
    return ranked, len(qualified), insufficient_ids


def evaluate_match(
    system_top3: list[str],
    expected_top3: list[str],
) -> tuple[int, int, str]:
    """Đo số gia sư trùng khớp theo quy ước tests/scenarios/README.md mục 3."""
    expected_len = len(expected_top3)
    if expected_len == 0:
        label = "no_match (0/0)" if len(system_top3) == 0 else "lệch no_match"
        return 0, 0, label

    matched = len(set(system_top3[:expected_len]) & set(expected_top3))
    return matched, expected_len, f"{matched}/{expected_len}"


@pytest.fixture(scope="module")
def all_tutors() -> list[TutorProfile]:
    return TutorRepository().get_all()


@pytest.fixture(scope="module")
def all_scenarios() -> list[dict[str, Any]]:
    return load_scenarios()


# ==============================================================================
# T1: Baseline Reproduction
# ==============================================================================
def test_t1_baseline_patch_reproduction_and_all_14_scenarios(
    all_scenarios: list[dict[str, Any]],
    all_tutors: list[TutorProfile],
) -> None:
    """T1: Tái lập baseline với delta=0.5, E_max=8; trùng kết quả không patch và khớp 14/14 expected_top3."""
    for sc in all_scenarios:
        sid = sc["id"]
        expected_top3: list[str] = sc["expected_top3"]

        ranked_unpatched, q_u, ins_u = run_sensitivity_pipeline(
            sc, all_tutors, top_k=20
        )
        with patch_scoring_params(delta=0.5, e_max=8.0):
            ranked_patched, q_p, ins_p = run_sensitivity_pipeline(
                sc, all_tutors, top_k=20
            )

        assert q_u == q_p, f"Kịch bản {sid}: số qua lọc không khớp giữa patch và không patch"
        assert ins_u == ins_p, f"Kịch bản {sid}: danh sách thiếu dữ liệu không khớp"
        assert len(ranked_unpatched) == len(ranked_patched)

        for u, p in zip(ranked_unpatched, ranked_patched):
            assert u.rank == p.rank
            assert u.tutor_id == p.tutor_id
            assert abs(u.total_score - p.total_score) < 1e-9
            assert u.criteria_scores == p.criteria_scores
            assert u.contributions == p.contributions

        system_top3 = [r.tutor_id for r in ranked_patched[:3]]
        matched, exp_len, _ = evaluate_match(system_top3, expected_top3)

        if sid == "KB05":
            assert q_p == 0
            assert expected_top3 == []
            assert system_top3 == []
        else:
            assert matched == exp_len
            assert set(system_top3[:exp_len]) == set(expected_top3)


# ==============================================================================
# T2: Patch Effectiveness
# ==============================================================================
def test_t2_patch_effectiveness_prevents_silent_noop(
    all_scenarios: list[dict[str, Any]],
    all_tutors: list[TutorProfile],
) -> None:
    """T2: delta=0.25 làm đổi điểm học phí; E_max=12 làm đổi điểm kinh nghiệm."""
    found_fee_diff = False
    for sc in all_scenarios:
        with patch_scoring_params(delta=0.5, e_max=8.0):
            base_ranked, _, _ = run_sensitivity_pipeline(sc, all_tutors, top_k=20)
        with patch_scoring_params(delta=0.25, e_max=8.0):
            test_ranked, _, _ = run_sensitivity_pipeline(sc, all_tutors, top_k=20)

        for b, t in zip(base_ranked, test_ranked):
            if b.tutor_id == t.tutor_id:
                b_fee = b.criteria_scores.get("fee")
                t_fee = t.criteria_scores.get("fee")
                if (
                    b_fee is not None
                    and t_fee is not None
                    and abs(b_fee - t_fee) > 1e-4
                ):
                    found_fee_diff = True
                    break
        if found_fee_diff:
            break

    assert found_fee_diff, "Patch delta=0.25 phải làm thay đổi điểm học phí của ít nhất 1 ứng viên"

    found_exp_diff = False
    for sc in all_scenarios:
        with patch_scoring_params(delta=0.5, e_max=8.0):
            base_ranked, _, _ = run_sensitivity_pipeline(sc, all_tutors, top_k=20)
        with patch_scoring_params(delta=0.5, e_max=12.0):
            test_ranked, _, _ = run_sensitivity_pipeline(sc, all_tutors, top_k=20)

        for b, t in zip(base_ranked, test_ranked):
            if b.tutor_id == t.tutor_id:
                b_exp = b.criteria_scores.get("experience")
                t_exp = t.criteria_scores.get("experience")
                if (
                    b_exp is not None
                    and t_exp is not None
                    and abs(b_exp - t_exp) > 1e-4
                ):
                    found_exp_diff = True
                    break
        if found_exp_diff:
            break

    assert found_exp_diff, "Patch e_max=12 phải làm thay đổi điểm kinh nghiệm của ít nhất 1 ứng viên"


# ==============================================================================
# T3: Sweep Delta
# ==============================================================================
def test_t3_sweep_delta_bounds_determinism_and_tracking(
    all_scenarios: list[dict[str, Any]],
    all_tutors: list[TutorProfile],
) -> None:
    """T3: Quét delta trên 6 giá trị; assert điểm trong [0, 1], tất định, thứ hạng liên tục từ 1."""
    for delta in DELTA_VALUES:
        with patch_scoring_params(delta=delta, e_max=8.0):
            for sc in all_scenarios:
                run1, _, _ = run_sensitivity_pipeline(sc, all_tutors, top_k=20)
                run2, _, _ = run_sensitivity_pipeline(sc, all_tutors, top_k=20)

                assert [r.tutor_id for r in run1] == [r.tutor_id for r in run2]
                assert [r.total_score for r in run1] == [r.total_score for r in run2]

                for r in run1:
                    assert -1e-9 <= r.total_score <= 1.0 + 1e-9
                    for s in r.criteria_scores.values():
                        if s is not None:
                            assert -1e-9 <= s <= 1.0 + 1e-9

                ranks = [r.rank for r in run1]
                assert ranks == list(range(1, len(run1) + 1))


# ==============================================================================
# T4: Monotonicity Delta
# ==============================================================================
def test_t4_monotonicity_score_non_decreasing_with_delta(
    all_scenarios: list[dict[str, Any]],
    all_tutors: list[TutorProfile],
) -> None:
    """T4: Với từng ứng viên ở từng kịch bản có tiêu chí học phí, S không giảm khi delta tăng."""
    for sc in all_scenarios:
        req = sc["request"]
        if (
            req.get("max_budget_vnd") is None
            or req.get("priorities", {}).get("fee") == "none"
        ):
            continue

        for i in range(len(DELTA_VALUES) - 1):
            d_curr = DELTA_VALUES[i]
            d_next = DELTA_VALUES[i + 1]

            with patch_scoring_params(delta=d_curr, e_max=8.0):
                ranked_curr, _, _ = run_sensitivity_pipeline(sc, all_tutors, top_k=20)
            with patch_scoring_params(delta=d_next, e_max=8.0):
                ranked_next, _, _ = run_sensitivity_pipeline(sc, all_tutors, top_k=20)

            score_curr = {r.tutor_id: r.total_score for r in ranked_curr}
            score_next = {r.tutor_id: r.total_score for r in ranked_next}

            assert set(score_curr.keys()) == set(score_next.keys())
            for tid, s_val in score_curr.items():
                assert score_next[tid] >= s_val - 1e-9, (
                    f"Kịch bản {sc['id']}, gia sư {tid}: S giảm khi delta tăng từ {d_curr} lên {d_next}"
                )


# ==============================================================================
# T5: Sweep E_max
# ==============================================================================
def test_t5_sweep_e_max_bounds_determinism_and_tracking(
    all_scenarios: list[dict[str, Any]],
    all_tutors: list[TutorProfile],
) -> None:
    """T5: Quét E_max trên 5 giá trị; assert điểm trong [0, 1], tất định, thứ hạng liên tục từ 1."""
    for e_max in E_MAX_VALUES:
        with patch_scoring_params(delta=0.5, e_max=e_max):
            for sc in all_scenarios:
                run1, _, _ = run_sensitivity_pipeline(sc, all_tutors, top_k=20)
                run2, _, _ = run_sensitivity_pipeline(sc, all_tutors, top_k=20)

                assert [r.tutor_id for r in run1] == [r.tutor_id for r in run2]
                assert [r.total_score for r in run1] == [r.total_score for r in run2]

                for r in run1:
                    assert -1e-9 <= r.total_score <= 1.0 + 1e-9
                    for s in r.criteria_scores.values():
                        if s is not None:
                            assert -1e-9 <= s <= 1.0 + 1e-9

                ranks = [r.rank for r in run1]
                assert ranks == list(range(1, len(run1) + 1))


# ==============================================================================
# T6: Monotonicity E_max
# ==============================================================================
def test_t6_monotonicity_score_non_increasing_with_e_max(
    all_scenarios: list[dict[str, Any]],
    all_tutors: list[TutorProfile],
) -> None:
    """T6: S không tăng khi E_max tăng (dung sai 1e-9)."""
    for sc in all_scenarios:
        req = sc["request"]
        if req.get("priorities", {}).get("experience") == "none":
            continue

        for i in range(len(E_MAX_VALUES) - 1):
            e_curr = E_MAX_VALUES[i]
            e_next = E_MAX_VALUES[i + 1]

            with patch_scoring_params(delta=0.5, e_max=e_curr):
                ranked_curr, _, _ = run_sensitivity_pipeline(sc, all_tutors, top_k=20)
            with patch_scoring_params(delta=0.5, e_max=e_next):
                ranked_next, _, _ = run_sensitivity_pipeline(sc, all_tutors, top_k=20)

            score_curr = {r.tutor_id: r.total_score for r in ranked_curr}
            score_next = {r.tutor_id: r.total_score for r in ranked_next}

            assert set(score_curr.keys()) == set(score_next.keys())
            for tid, s_val in score_curr.items():
                assert score_next[tid] <= s_val + 1e-9, (
                    f"Kịch bản {sc['id']}, gia sư {tid}: S tăng khi E_max tăng từ {e_curr} lên {e_next}"
                )


# ==============================================================================
# T7: Budget +-5%
# ==============================================================================
def test_t7_budget_variation_pm_5_percent(
    all_scenarios: list[dict[str, Any]],
    all_tutors: list[TutorProfile],
) -> None:
    """T7: S(0.95B) <= S(B) <= S(1.05B), tập ứng viên qua lọc không đổi."""
    for sc in all_scenarios:
        orig_b = sc["request"].get("max_budget_vnd")
        if orig_b is None:
            continue

        b_minus = round(orig_b * 0.95)
        b_base = orig_b
        b_plus = round(orig_b * 1.05)

        r_minus, q_minus, _ = run_sensitivity_pipeline(
            sc, all_tutors, {"max_budget_vnd": b_minus}, top_k=20
        )
        r_base, q_base, _ = run_sensitivity_pipeline(
            sc, all_tutors, {"max_budget_vnd": b_base}, top_k=20
        )
        r_plus, q_plus, _ = run_sensitivity_pipeline(
            sc, all_tutors, {"max_budget_vnd": b_plus}, top_k=20
        )

        assert q_minus == q_base == q_plus
        assert [r.tutor_id for r in r_minus] == [r.tutor_id for r in r_base] == [r.tutor_id for r in r_plus]

        s_minus = {r.tutor_id: r.total_score for r in r_minus}
        s_base = {r.tutor_id: r.total_score for r in r_base}
        s_plus = {r.tutor_id: r.total_score for r in r_plus}

        for tid, s_b in s_base.items():
            assert s_minus[tid] <= s_b + 1e-9
            assert s_b <= s_plus[tid] + 1e-9


# ==============================================================================
# T8: Budget +-10%
# ==============================================================================
def test_t8_budget_variation_pm_10_percent(
    all_scenarios: list[dict[str, Any]],
    all_tutors: list[TutorProfile],
) -> None:
    """T8: S(0.90B) <= S(B) <= S(1.10B), tập ứng viên qua lọc không đổi."""
    for sc in all_scenarios:
        orig_b = sc["request"].get("max_budget_vnd")
        if orig_b is None:
            continue

        b_minus = round(orig_b * 0.90)
        b_base = orig_b
        b_plus = round(orig_b * 1.10)

        r_minus, q_minus, _ = run_sensitivity_pipeline(
            sc, all_tutors, {"max_budget_vnd": b_minus}, top_k=20
        )
        r_base, q_base, _ = run_sensitivity_pipeline(
            sc, all_tutors, {"max_budget_vnd": b_base}, top_k=20
        )
        r_plus, q_plus, _ = run_sensitivity_pipeline(
            sc, all_tutors, {"max_budget_vnd": b_plus}, top_k=20
        )

        assert q_minus == q_base == q_plus
        assert [r.tutor_id for r in r_minus] == [r.tutor_id for r in r_base] == [r.tutor_id for r in r_plus]

        s_minus = {r.tutor_id: r.total_score for r in r_minus}
        s_base = {r.tutor_id: r.total_score for r in r_base}
        s_plus = {r.tutor_id: r.total_score for r in r_plus}

        for tid, s_b in s_base.items():
            assert s_minus[tid] <= s_b + 1e-9
            assert s_b <= s_plus[tid] + 1e-9


# ==============================================================================
# T9: Budget +-20% and Full 7 Levels Chain
# ==============================================================================
def test_t9_budget_variation_pm_20_percent_and_full_7_levels_chain(
    all_scenarios: list[dict[str, Any]],
    all_tutors: list[TutorProfile],
) -> None:
    """T9: S(0.80B) <= S(0.90B) <= S(0.95B) <= S(B) <= S(1.05B) <= S(1.10B) <= S(1.20B)."""
    for sc in all_scenarios:
        orig_b = sc["request"].get("max_budget_vnd")
        if orig_b is None:
            continue

        previous_scores: dict[str, float] | None = None
        base_candidate_ids: list[str] | None = None
        base_qualified_count: int | None = None

        for factor in BUDGET_FACTORS:
            varied_b = round(orig_b * (1.0 + factor))
            ranked, q_count, _ = run_sensitivity_pipeline(
                sc, all_tutors, {"max_budget_vnd": varied_b}, top_k=20
            )

            if base_qualified_count is None:
                base_qualified_count = q_count
                base_candidate_ids = [r.tutor_id for r in ranked]
            else:
                assert q_count == base_qualified_count
                assert [r.tutor_id for r in ranked] == base_candidate_ids

            curr_scores = {r.tutor_id: r.total_score for r in ranked}
            if previous_scores is not None:
                for tid, curr_s in curr_scores.items():
                    assert previous_scores[tid] <= curr_s + 1e-9, (
                        f"Kịch bản {sc['id']}, gia sư {tid}: S vi phạm chuỗi đơn điệu ở mức hệ số {factor}"
                    )
            previous_scores = curr_scores


# ==============================================================================
# T10: Priority Sets Comparison
# ==============================================================================
def test_t10_priority_sets_comparison_and_invariants(
    all_scenarios: list[dict[str, Any]],
    all_tutors: list[TutorProfile],
) -> None:
    """T10: Khảo sát 4 bộ mức ưu tiên; assert tập ứng viên đủ điều kiện không đổi, không zero_weight, S in [0, 1]."""
    for sc in all_scenarios:
        eligible_candidate_maps: dict[str, list[str]] = {}

        for set_name, priorities in PRIORITY_SETS.items():
            req_data = dict(sc["request"])
            req_data["priorities"] = priorities
            query = SearchRequest.model_validate(req_data)

            weights = compute_effective_weights(query)
            assert weights.total > 0, f"Kịch bản {sc['id']}, bộ {set_name}: phát sinh zero_weight"

            ranked, _, _ = run_sensitivity_pipeline(
                sc, all_tutors, {"priorities": priorities}, top_k=20
            )

            for r in ranked:
                assert -1e-9 <= r.total_score <= 1.0 + 1e-9
                for s in r.criteria_scores.values():
                    if s is not None:
                        assert -1e-9 <= s <= 1.0 + 1e-9

            eligible_candidate_maps[set_name] = [r.tutor_id for r in ranked]

        default_cand_set = set(eligible_candidate_maps["default"])
        for set_name, cand_ids in eligible_candidate_maps.items():
            assert set(cand_ids) == default_cand_set, (
                f"Kịch bản {sc['id']}: tập ứng viên của bộ {set_name} khác tập default"
            )


# ==============================================================================
# Runner sinh dữ liệu thô JSON (Mục 5.2)
# ==============================================================================
def _serialize_ranked_list(ranked: list[RankedTutor]) -> list[dict[str, Any]]:
    return [
        {
            "rank": r.rank,
            "tutor_id": r.tutor_id,
            "total_score": round(r.total_score, 5),
            "criteria_scores": {
                k: round(v, 4) if v is not None else None
                for k, v in r.criteria_scores.items()
            },
            "contributions": {
                k: round(v, 4) if v is not None else None
                for k, v in r.contributions.items()
            },
        }
        for r in ranked
    ]


def generate_raw_json_data() -> Path:
    """Sinh tệp docs/thesis/report/muc-5.2-ket-qua-tho.json chứa số liệu thực nghiệm."""
    all_tutors = TutorRepository().get_all()
    all_scenarios = load_scenarios()
    repo_root = Path(__file__).resolve().parents[3]

    git_commit = "unknown"
    with contextlib.suppress(subprocess.SubprocessError, FileNotFoundError, OSError):
        res = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
        git_commit = res.stdout.strip()

    baseline_results: dict[str, Any] = {}
    with patch_scoring_params(delta=0.5, e_max=8.0):
        for sc in all_scenarios:
            sid = sc["id"]
            ranked, q_count, ins_ids = run_sensitivity_pipeline(
                sc, all_tutors, top_k=20
            )
            top3 = [r.tutor_id for r in ranked[:3]]
            matched, exp_len, label = evaluate_match(top3, sc["expected_top3"])
            baseline_results[sid] = {
                "id": sid,
                "status": "success" if q_count > 0 else "no_match",
                "qualified_count": q_count,
                "insufficient_data_ids": ins_ids,
                "expected_top3": sc["expected_top3"],
                "priorities_used": sc["request"].get("priorities"),
                "top3_ids": top3,
                "overlap_expected": label,
                "matched_count": matched,
                "expected_count": exp_len,
                "ranking": _serialize_ranked_list(ranked),
            }

    # Quét delta
    delta_results: dict[str, list[dict[str, Any]]] = {}
    for delta in DELTA_VALUES:
        delta_key = f"{delta:.2f}".rstrip("0").rstrip(".")
        delta_list: list[dict[str, Any]] = []
        with patch_scoring_params(delta=delta, e_max=8.0):
            for sc in all_scenarios:
                sid = sc["id"]
                ranked, q_count, _ = run_sensitivity_pipeline(
                    sc, all_tutors, top_k=20
                )
                top3 = [r.tutor_id for r in ranked[:3]]
                matched, _, label = evaluate_match(top3, sc["expected_top3"])
                base_top3 = baseline_results[sid]["top3_ids"]
                same_order = top3 == base_top3
                same_set = set(top3) == set(base_top3)
                delta_list.append(
                    {
                        "id": sid,
                        "status": "success" if q_count > 0 else "no_match",
                        "fee_applicable": sc["request"].get("max_budget_vnd") is not None,
                        "top3_ids": top3,
                        "overlap_expected": label,
                        "same_order_as_baseline": same_order,
                        "same_set_as_baseline": same_set,
                        "ranking": _serialize_ranked_list(ranked),
                    }
                )
        delta_results[delta_key] = delta_list

    # Quét E_max
    e_max_results: dict[str, list[dict[str, Any]]] = {}
    for e_max in E_MAX_VALUES:
        e_key = str(e_max)
        e_list: list[dict[str, Any]] = []
        with patch_scoring_params(delta=0.5, e_max=e_max):
            for sc in all_scenarios:
                sid = sc["id"]
                ranked, q_count, _ = run_sensitivity_pipeline(
                    sc, all_tutors, top_k=20
                )
                top3 = [r.tutor_id for r in ranked[:3]]
                matched, _, label = evaluate_match(top3, sc["expected_top3"])
                base_top3 = baseline_results[sid]["top3_ids"]
                same_order = top3 == base_top3
                same_set = set(top3) == set(base_top3)
                e_list.append(
                    {
                        "id": sid,
                        "status": "success" if q_count > 0 else "no_match",
                        "top3_ids": top3,
                        "overlap_expected": label,
                        "same_order_as_baseline": same_order,
                        "same_set_as_baseline": same_set,
                        "ranking": _serialize_ranked_list(ranked),
                    }
                )
        e_max_results[e_key] = e_list

    # Quét ngân sách
    budget_results: dict[str, list[dict[str, Any]]] = {}
    for factor in BUDGET_FACTORS:
        pct_label = (
            f"+{int(factor * 100)}%"
            if factor > 0
            else f"{int(factor * 100)}%"
        )
        b_list: list[dict[str, Any]] = []
        for sc in all_scenarios:
            sid = sc["id"]
            orig_b = sc["request"].get("max_budget_vnd")
            if orig_b is None:
                b_list.append(
                    {
                        "id": sid,
                        "applicable": False,
                        "note": "không áp dụng",
                        "status": baseline_results[sid]["status"],
                        "top3_ids": baseline_results[sid]["top3_ids"],
                        "same_order_as_baseline": True,
                        "same_set_as_baseline": True,
                        "ranking": baseline_results[sid]["ranking"],
                    }
                )
                continue

            varied_b = round(orig_b * (1.0 + factor))
            ranked, q_count, _ = run_sensitivity_pipeline(
                sc, all_tutors, {"max_budget_vnd": varied_b}, top_k=20
            )
            top3 = [r.tutor_id for r in ranked[:3]]
            base_top3 = baseline_results[sid]["top3_ids"]
            same_order = top3 == base_top3
            same_set = set(top3) == set(base_top3)
            b_list.append(
                {
                    "id": sid,
                    "applicable": True,
                    "varied_budget_vnd": varied_b,
                    "status": "success" if q_count > 0 else "no_match",
                    "top3_ids": top3,
                    "same_order_as_baseline": same_order,
                    "same_set_as_baseline": same_set,
                    "ranking": _serialize_ranked_list(ranked),
                }
            )
        budget_results[pct_label] = b_list

    # Khảo sát 4 bộ mức ưu tiên
    priority_results: dict[str, list[dict[str, Any]]] = {}
    for set_name, priorities in PRIORITY_SETS.items():
        p_list: list[dict[str, Any]] = []
        for sc in all_scenarios:
            sid = sc["id"]
            ranked, q_count, _ = run_sensitivity_pipeline(
                sc, all_tutors, {"priorities": priorities}, top_k=20
            )
            top3 = [r.tutor_id for r in ranked[:3]]
            matched, _, label = evaluate_match(top3, sc["expected_top3"])
            base_top3 = baseline_results[sid]["top3_ids"]
            same_order = top3 == base_top3
            same_set = set(top3) == set(base_top3)
            p_list.append(
                {
                    "id": sid,
                    "status": "success" if q_count > 0 else "no_match",
                    "top3_ids": top3,
                    "overlap_expected": label,
                    "same_order_as_baseline": same_order,
                    "same_set_as_baseline": same_set,
                    "ranking": _serialize_ranked_list(ranked),
                }
            )
        priority_results[set_name] = p_list

    output_payload = {
        "meta": {
            "topic": "Hệ thống khuyến nghị gia sư dựa trên phương pháp Content-Base Filtering",
            "git_commit": git_commit,
            "total_scenarios": len(all_scenarios),
            "total_tutors": len(all_tutors),
            "parameters": {
                "delta_values": DELTA_VALUES,
                "e_max_values": E_MAX_VALUES,
                "budget_factors": BUDGET_FACTORS,
                "priority_sets": PRIORITY_SETS,
            },
        },
        "baseline": baseline_results,
        "delta": delta_results,
        "e_max": e_max_results,
        "budget": budget_results,
        "priority_sets": priority_results,
    }

    out_file = repo_root / "docs" / "thesis" / "report" / "muc-5.2-ket-qua-tho.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(
        json.dumps(output_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return out_file


if __name__ == "__main__":
    out_path = generate_raw_json_data()
    print(f"Generated raw data JSON: {out_path}")
