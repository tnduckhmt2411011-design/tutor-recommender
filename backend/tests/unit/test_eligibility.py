"""Kiểm thử đơn vị cho quy tắc kiểm tra điều kiện đủ dữ liệu (eligibility.py).

Trách nhiệm:
- Kiểm tra số lượng tiêu chí có dữ liệu với ngưỡng tối thiểu (Bảng ngưỡng dữ liệu)
- Kiểm tra việc loại gia sư không đủ dữ liệu

Mục tương ứng trong đề cương: Mục 3.6 (Điều kiện đủ dữ liệu để được xếp hạng).
"""

import pytest

from app.schemas.tutor import TutorProfile
from app.scoring.eligibility import (
    MIN_DATA_THRESHOLD,
    check_data_threshold,
    check_tutor_eligibility,
    count_available_criteria,
    filter_eligible_candidates,
    get_min_required_criteria,
)
from app.scoring.weights import EffectiveWeights


def _make_tutor(
    tutor_id: str = "GS-TEST",
    hourly_fee_vnd: int | None = 200000,
    districts: list[str] | None = None,
    years_experience: float | None = 3.0,
    availability: list[str] | None = None,
    avg_rating: float | None = 4.5,
) -> TutorProfile:
    return TutorProfile(
        tutor_id=tutor_id,
        subjects=["Toán"],
        districts=["Quận 1"] if districts is None else districts,
        hourly_fee_vnd=hourly_fee_vnd,
        years_experience=years_experience,
        teaching_mode="both",
        availability=["T2-tối"] if availability is None else availability,
        avg_rating=avg_rating,
        data_source="simulated",
    )


class TestMinDataThresholdTable:
    """Kiểm tra bảng ngưỡng dữ liệu tối thiểu theo Mục 3.6."""

    @pytest.mark.parametrize(
        ("n_criteria", "expected_threshold"),
        [
            (0, 0),
            (1, 1),
            (2, 2),
            (3, 2),
            (4, 3),
            (5, 4),
        ],
    )
    def test_threshold_mapping(self, n_criteria: int, expected_threshold: int) -> None:
        assert MIN_DATA_THRESHOLD[n_criteria] == expected_threshold
        assert get_min_required_criteria(n_criteria) == expected_threshold

    def test_invalid_negative_n_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="Số tiêu chí"):
            get_min_required_criteria(-1)

    def test_invalid_above_max_n_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="Số tiêu chí"):
            get_min_required_criteria(6)


class TestCountAvailableCriteria:
    """Kiểm tra đếm số tiêu chí có dữ liệu thực tế (loại trừ Đánh giá)."""

    def test_all_four_non_rating_criteria_present(self) -> None:
        tutor = _make_tutor(avg_rating=None)
        weights = EffectiveWeights(
            weights={
                "fee": 2,
                "district": 2,
                "experience": 2,
                "rating": 2,
                "availability": 2,
            },
            total=10,
        )
        available, total_applicable = count_available_criteria(tutor, weights)
        # "rating" bị loại trừ khỏi n -> n = 4, có đủ 4 tiêu chí
        assert total_applicable == 4
        assert available == 4

    def test_rating_only_active_yields_zero_non_rating_criteria(self) -> None:
        tutor = _make_tutor(
            hourly_fee_vnd=None,
            districts=[],
            years_experience=None,
            availability=[],
            avg_rating=None,
        )
        weights = EffectiveWeights(weights={"rating": 3}, total=3)
        available, total_applicable = count_available_criteria(tutor, weights)
        assert total_applicable == 0
        assert available == 0
        assert check_tutor_eligibility(tutor, weights) is True

    def test_missing_each_criterion_individually(self) -> None:
        weights = EffectiveWeights(
            weights={
                "fee": 2,
                "district": 2,
                "experience": 2,
                "availability": 2,
            },
            total=8,
        )
        t_no_fee = _make_tutor(hourly_fee_vnd=None)
        assert count_available_criteria(t_no_fee, weights) == (3, 4)

        t_no_district = _make_tutor(districts=[])
        assert count_available_criteria(t_no_district, weights) == (3, 4)

        t_no_exp = _make_tutor(years_experience=None)
        assert count_available_criteria(t_no_exp, weights) == (3, 4)

        t_no_avail = _make_tutor(availability=[])
        assert count_available_criteria(t_no_avail, weights) == (3, 4)


class TestCheckTutorEligibilityByN:
    """Kiểm tra điều kiện đạt ngưỡng cho từng trường hợp n = 1, 2, 3, 4."""

    def test_n_equals_1_requires_1(self) -> None:
        weights = EffectiveWeights(weights={"fee": 3, "rating": 2}, total=5)
        assert check_tutor_eligibility(_make_tutor(hourly_fee_vnd=200000), weights) is True
        assert check_tutor_eligibility(_make_tutor(hourly_fee_vnd=None), weights) is False

    def test_n_equals_2_requires_2(self) -> None:
        weights = EffectiveWeights(
            weights={"fee": 2, "district": 2, "rating": 2},
            total=6,
        )
        assert check_tutor_eligibility(_make_tutor(), weights) is True
        assert check_tutor_eligibility(_make_tutor(hourly_fee_vnd=None), weights) is False
        assert check_tutor_eligibility(_make_tutor(districts=[]), weights) is False

    def test_n_equals_3_requires_2(self) -> None:
        weights = EffectiveWeights(
            weights={"fee": 2, "district": 2, "experience": 2, "rating": 2},
            total=8,
        )
        # Thiếu 1 tiêu chí (còn 2/3) -> vẫn đạt ngưỡng 2
        assert check_tutor_eligibility(_make_tutor(years_experience=None), weights) is True
        # Thiếu 2 tiêu chí (còn 1/3) -> dưới ngưỡng 2 -> loại
        assert (
            check_tutor_eligibility(
                _make_tutor(hourly_fee_vnd=None, years_experience=None),
                weights,
            )
            is False
        )

    def test_n_equals_4_requires_3(self) -> None:
        weights = EffectiveWeights(
            weights={
                "fee": 2,
                "district": 2,
                "experience": 2,
                "rating": 2,
                "availability": 2,
            },
            total=10,
        )
        # Có 3/4 tiêu chí -> đạt ngưỡng 3
        assert check_tutor_eligibility(_make_tutor(hourly_fee_vnd=None), weights) is True
        # Có 2/4 tiêu chí -> dưới ngưỡng 3 -> loại
        assert (
            check_tutor_eligibility(
                _make_tutor(hourly_fee_vnd=None, districts=[]),
                weights,
            )
            is False
        )
        # Alias check_data_threshold hoạt động đồng nhất
        assert (
            check_data_threshold(
                _make_tutor(hourly_fee_vnd=None, districts=[]),
                weights,
            )
            is False
        )


class TestFilterEligibleCandidates:
    """Kiểm tra phân tách danh sách ứng viên đủ dữ liệu và thiếu dữ liệu."""

    def test_splits_eligible_and_insufficient_preserving_order(self) -> None:
        weights = EffectiveWeights(
            weights={
                "fee": 2,
                "district": 2,
                "experience": 2,
                "rating": 2,
                "availability": 2,
            },
            total=10,
        )
        t1 = _make_tutor(tutor_id="GS-01")
        t2 = _make_tutor(tutor_id="GS-02", hourly_fee_vnd=None, districts=[])
        t3 = _make_tutor(tutor_id="GS-03", years_experience=None)
        t4 = _make_tutor(
            tutor_id="GS-04",
            hourly_fee_vnd=None,
            years_experience=None,
            availability=[],
        )

        eligible, insufficient_ids = filter_eligible_candidates([t1, t2, t3, t4], weights)

        assert [t.tutor_id for t in eligible] == ["GS-01", "GS-03"]
        assert insufficient_ids == ["GS-02", "GS-04"]

    def test_empty_input_returns_empty_lists(self) -> None:
        weights = EffectiveWeights(weights={"fee": 2}, total=2)
        eligible, insufficient_ids = filter_eligible_candidates([], weights)
        assert eligible == []
        assert insufficient_ids == []
