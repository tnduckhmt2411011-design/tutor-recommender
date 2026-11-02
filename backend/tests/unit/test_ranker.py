"""Kiểm thử đơn vị cho module tổng hợp điểm và xếp hạng Top-k (ranker.py).

Trách nhiệm:
- Kiểm tra tính toán điểm tổng hợp S và đóng góp tiêu chí
- Kiểm tra sắp xếp giảm dần và tính ổn định khi đồng điểm (xếp theo mã gia sư)

Mục tương ứng trong đề cương: Mục 3.6 (Bước 4: Tổng hợp và xếp hạng).
"""

import pytest

from app.core.config import CRITERIA_KEYS
from app.schemas.recommendation import RankedTutor
from app.schemas.search_request import SearchRequest
from app.schemas.tutor import TutorProfile
from app.scoring.ranker import build_notes, build_reason, score_and_rank
from app.scoring.weights import EffectiveWeights, compute_effective_weights


def _make_tutor(
    tutor_id: str = "GS001",
    hourly_fee_vnd: int = 230000,
    districts: list[str] | None = None,
    years_experience: float = 4.0,
    avg_rating: float | None = 4.5,
    availability: list[str] | None = None,
) -> TutorProfile:
    return TutorProfile(
        tutor_id=tutor_id,
        subjects=["Toán"],
        districts=["KV1"] if districts is None else districts,
        hourly_fee_vnd=hourly_fee_vnd,
        years_experience=years_experience,
        teaching_mode="both",
        availability=["T2-tối", "T7-sáng"] if availability is None else availability,
        avg_rating=avg_rating,
        data_source="simulated",
    )


class TestMuc36WeightedScoringExample:
    """Kiểm thử ví dụ minh họa Mục 3.6 trong đề cương và API Contract."""

    def test_muc_3_6_full_example_scores_and_contributions(self) -> None:
        query = SearchRequest(
            subject="Toán",
            learning_mode="in_person",
            preferred_district="KV1",
            max_budget_vnd=200000,
            time_slots=["T2-tối", "T4-tối", "T7-sáng"],
        )
        weights = compute_effective_weights(query)
        tutor = _make_tutor(
            tutor_id="GS001",
            hourly_fee_vnd=230000,
            districts=["KV1"],
            years_experience=4.0,
            avg_rating=4.5,
            availability=["T2-tối", "T7-sáng"],
        )

        results = score_and_rank([tutor], query, weights, top_k=3)

        assert len(results) == 1
        ranked = results[0]
        assert isinstance(ranked, RankedTutor)
        assert ranked.rank == 1
        assert ranked.tutor_id == "GS001"

        # Điểm thành phần s_i theo Bảng 3.6
        assert ranked.criteria_scores["fee"] == pytest.approx(0.7)
        assert ranked.criteria_scores["district"] == pytest.approx(1.0)
        assert ranked.criteria_scores["experience"] == pytest.approx(0.5)
        assert ranked.criteria_scores["rating"] == pytest.approx(0.9)
        assert ranked.criteria_scores["availability"] == pytest.approx(2.0 / 3.0)

        # Đóng góp C_i = w_i * s_i / sum(w_i) với w_i = 2, sum(w_i) = 10
        assert ranked.contributions["fee"] == pytest.approx(0.14)
        assert ranked.contributions["district"] == pytest.approx(0.20)
        assert ranked.contributions["experience"] == pytest.approx(0.10)
        assert ranked.contributions["rating"] == pytest.approx(0.18)
        assert ranked.contributions["availability"] == pytest.approx(2.0 / 15.0)

        # Điểm tổng S = 113/150 ≈ 0.753333... (làm tròn hiển thị 0.753)
        assert ranked.total_score == pytest.approx(113.0 / 150.0)
        assert round(ranked.total_score, 3) == 0.753

        active_contribs = [
            v for v in ranked.contributions.values() if v is not None
        ]
        assert sum(active_contribs) == pytest.approx(ranked.total_score)
        assert ranked.notes == []
        assert isinstance(ranked.reason, str) and len(ranked.reason.strip()) > 0


class TestInactiveCriteriaAndNotes:
    """Kiểm tra tiêu chí không áp dụng nhận None và ghi chú chưa có đánh giá."""

    def test_online_and_unrated_tutor_matches_api_contract_example_2(self) -> None:
        query = SearchRequest(
            subject="Toán",
            learning_mode="online",
            preferred_district=None,
            max_budget_vnd=200000,
            time_slots=["T2-tối", "T4-tối"],
        )
        weights = compute_effective_weights(query)
        tutor = _make_tutor(
            tutor_id="GS002",
            hourly_fee_vnd=180000,
            districts=["KV1"],
            years_experience=4.0,
            avg_rating=None,
            availability=["T2-tối", "T4-tối"],
        )

        results = score_and_rank([tutor], query, weights, top_k=3)
        ranked = results[0]

        assert tuple(ranked.criteria_scores.keys()) == CRITERIA_KEYS
        assert tuple(ranked.contributions.keys()) == CRITERIA_KEYS

        assert ranked.criteria_scores["district"] is None
        assert ranked.contributions["district"] is None
        assert ranked.criteria_scores["rating"] == pytest.approx(0.5)
        assert ranked.contributions["rating"] == pytest.approx(0.125)
        assert ranked.total_score == pytest.approx(0.75)
        assert ranked.notes == ["chưa có đánh giá"]

    def test_zero_priority_criterion_has_none_score_and_contribution(self) -> None:
        query = SearchRequest(
            subject="Toán",
            learning_mode="in_person",
            preferred_district="KV1",
            max_budget_vnd=200000,
            time_slots=["T2-tối"],
            priorities={
                "fee": "high",
                "district": "none",
                "experience": "none",
                "rating": "low",
                "availability": "none",
            },
        )
        weights = compute_effective_weights(query)
        tutor = _make_tutor(tutor_id="GS003", hourly_fee_vnd=200000, avg_rating=4.0)

        ranked = score_and_rank([tutor], query, weights)[0]
        assert ranked.criteria_scores["district"] is None
        assert ranked.criteria_scores["experience"] is None
        assert ranked.criteria_scores["availability"] is None
        assert ranked.contributions["district"] is None
        assert ranked.contributions["experience"] is None
        assert ranked.contributions["availability"] is None
        assert ranked.criteria_scores["fee"] == pytest.approx(1.0)
        assert ranked.criteria_scores["rating"] == pytest.approx(0.8)
        assert ranked.total_score == pytest.approx((3 * 1.0 + 1 * 0.8) / 4.0)


class TestSortingTieBreakerAndTopK:
    """Kiểm tra sắp xếp giảm dần theo S, phá hòa theo tutor_id và cắt Top-k."""

    def test_tie_breaker_sorts_by_tutor_id_ascending(self) -> None:
        query = SearchRequest(
            subject="Toán",
            learning_mode="online",
            max_budget_vnd=200000,
            time_slots=["T2-tối"],
        )
        weights = compute_effective_weights(query)
        t_b = _make_tutor(tutor_id="GS-B", hourly_fee_vnd=200000, years_experience=4.0)
        t_a = _make_tutor(tutor_id="GS-A", hourly_fee_vnd=200000, years_experience=4.0)
        t_c = _make_tutor(tutor_id="GS-C", hourly_fee_vnd=180000, years_experience=8.0)

        results = score_and_rank([t_b, t_a, t_c], query, weights, top_k=3)

        assert [r.tutor_id for r in results] == ["GS-C", "GS-A", "GS-B"]
        assert [r.rank for r in results] == [1, 2, 3]
        assert results[1].total_score == pytest.approx(results[2].total_score)

    def test_top_k_slices_results_and_handles_fewer_candidates(self) -> None:
        query = SearchRequest(
            subject="Toán",
            learning_mode="online",
            max_budget_vnd=200000,
            time_slots=["T2-tối"],
        )
        weights = compute_effective_weights(query)
        tutors = [
            _make_tutor(tutor_id=f"GS-{i:02d}", years_experience=float(i))
            for i in range(1, 6)
        ]

        top2 = score_and_rank(tutors, query, weights, top_k=2)
        assert len(top2) == 2
        assert [r.tutor_id for r in top2] == ["GS-05", "GS-04"]
        assert [r.rank for r in top2] == [1, 2]

        top10 = score_and_rank(tutors[:2], query, weights, top_k=10)
        assert len(top10) == 2
        assert [r.rank for r in top10] == [1, 2]

    def test_invalid_zero_total_weight_raises_value_error(self) -> None:
        query = SearchRequest(subject="Toán", learning_mode="online")
        zero_weights = EffectiveWeights(weights={}, total=0)
        with pytest.raises(ValueError, match="Tổng trọng số"):
            score_and_rank([_make_tutor()], query, zero_weights)


class TestReasonAndNotesGeneration:
    """Kiểm tra sinh lý do gợi ý tất định và ghi chú dữ liệu."""

    def test_reason_is_deterministic_and_highlights_top_contribution(self) -> None:
        query = SearchRequest(
            subject="Toán",
            learning_mode="in_person",
            preferred_district="KV1",
            max_budget_vnd=200000,
            time_slots=["T2-tối", "T4-tối", "T7-sáng"],
        )
        tutor = _make_tutor(
            tutor_id="GS001",
            hourly_fee_vnd=230000,
            districts=["KV1"],
            years_experience=4.0,
            avg_rating=4.5,
            availability=["T2-tối", "T7-sáng"],
        )
        scores = {
            "fee": 0.7,
            "district": 1.0,
            "experience": 0.5,
            "rating": 0.9,
            "availability": 2.0 / 3.0,
        }
        contribs = {
            "fee": 0.14,
            "district": 0.20,
            "experience": 0.10,
            "rating": 0.18,
            "availability": 2.0 / 15.0,
        }

        reason_1 = build_reason(tutor, query, scores, contribs)
        reason_2 = build_reason(tutor, query, scores, contribs)
        assert reason_1 == reason_2
        assert "khu vực" in reason_1.lower()
        assert "4,5/5" in reason_1 or "đánh giá" in reason_1.lower()

    def test_build_notes_for_rated_and_unrated_tutors(self) -> None:
        assert build_notes(_make_tutor(avg_rating=4.5)) == []
        assert build_notes(_make_tutor(avg_rating=None)) == ["chưa có đánh giá"]
