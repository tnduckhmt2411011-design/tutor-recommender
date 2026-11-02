"""Kiểm thử đơn vị cho module quy đổi và chuẩn hóa trọng số (weights.py).

Trách nhiệm:
- Kiểm tra ánh xạ mức ưu tiên sang trọng số (Bảng 3.5)
- Kiểm tra loại trừ tiêu chí không áp dụng và phát hiện tổng trọng số bằng 0

Mục tương ứng trong đề cương: Mục 3.6 (Bảng 3.5 và Các trường hợp đặc biệt).
"""

import pytest

from app.core import config
from app.schemas.search_request import SearchRequest
from app.scoring.weights import compute_effective_weights, priority_to_weight


def make_query(**overrides: object) -> SearchRequest:
    """Dựng yêu cầu đầy đủ: học trực tiếp, có khu vực, ngân sách, khung giờ."""
    data = {
        "subject": "Toán",
        "learning_mode": "in_person",
        "preferred_district": "KV1",
        "max_budget_vnd": 200_000,
        "time_slots": ["T2-tối", "T4-tối"],
    }
    data.update(overrides)
    return SearchRequest(**data)


def priorities(**levels: str) -> dict[str, str]:
    """Mọi tiêu chí mức medium, ghi đè theo `levels`."""
    result = {key: "medium" for key in config.CRITERIA_KEYS}
    result.update(levels)
    return result


# --- Ánh xạ mức ưu tiên (Bảng 3.5) -------------------------------------------


@pytest.mark.parametrize(
    ("level", "expected"),
    [("none", 0), ("low", 1), ("medium", 2), ("high", 3)],
)
def test_priority_levels_map_to_table_3_5_weights(level: str, expected: int) -> None:
    assert priority_to_weight(level) == expected


def test_missing_priority_key_uses_default_medium() -> None:
    query = make_query(priorities={})

    result = compute_effective_weights(query)

    assert config.DEFAULT_PRIORITY == "medium"
    assert result.weights == dict.fromkeys(config.CRITERIA_KEYS, 2)


def test_partially_missing_priorities_only_default_the_missing_keys() -> None:
    query = make_query(priorities={"fee": "high", "rating": "low"})

    result = compute_effective_weights(query)

    assert result.weights == {
        "fee": 3,
        "district": 2,
        "experience": 2,
        "rating": 1,
        "availability": 2,
    }


# --- Ví dụ đầy đủ Mục 3.6 ----------------------------------------------------


def test_full_example_all_medium_gives_weight_2_each_and_total_10() -> None:
    result = compute_effective_weights(make_query())

    assert result.weights == dict.fromkeys(config.CRITERIA_KEYS, 2)
    assert result.total == 10


def test_any_learning_mode_with_district_keeps_district_applicable() -> None:
    result = compute_effective_weights(make_query(learning_mode="any"))

    assert "district" in result.weights
    assert result.total == 10


def test_effective_weights_follow_chosen_levels() -> None:
    query = make_query(
        priorities=priorities(fee="high", district="low", availability="high")
    )

    result = compute_effective_weights(query)

    assert result.weights == {
        "fee": 3,
        "district": 1,
        "experience": 2,
        "rating": 2,
        "availability": 3,
    }
    assert result.total == 11


# --- Tiêu chí không áp dụng --------------------------------------------------


def test_online_learning_mode_removes_district() -> None:
    result = compute_effective_weights(make_query(learning_mode="online"))

    assert "district" not in result.weights
    assert result.total == 8


def test_missing_district_removes_district() -> None:
    result = compute_effective_weights(make_query(preferred_district=None))

    assert "district" not in result.weights
    assert result.total == 8


def test_missing_budget_removes_fee() -> None:
    result = compute_effective_weights(make_query(max_budget_vnd=None))

    assert "fee" not in result.weights
    assert result.total == 8


def test_zero_budget_still_counts_as_entered_budget() -> None:
    """Ngân sách 0 là giá trị đã nhập (xử lý theo QĐ-A ở criteria), không phải thiếu."""
    result = compute_effective_weights(make_query(max_budget_vnd=0))

    assert "fee" in result.weights


@pytest.mark.parametrize("slots", [None, []])
def test_missing_time_slots_removes_availability(slots: list[str] | None) -> None:
    result = compute_effective_weights(make_query(time_slots=slots))

    assert "availability" not in result.weights
    assert result.total == 8


def test_experience_and_rating_are_always_applicable() -> None:
    query = make_query(
        learning_mode="online",
        preferred_district=None,
        max_budget_vnd=None,
        time_slots=None,
    )

    result = compute_effective_weights(query)

    assert result.weights == {"experience": 2, "rating": 2}
    assert result.total == 4


# --- Mức "không quan tâm" ----------------------------------------------------


def test_none_level_removes_criterion_from_effective_weights() -> None:
    result = compute_effective_weights(
        make_query(priorities=priorities(fee="none", experience="none"))
    )

    assert "fee" not in result.weights
    assert "experience" not in result.weights
    assert result.total == 6


# --- Tổng trọng số bằng 0 ----------------------------------------------------


def test_all_none_gives_zero_total_without_raising() -> None:
    query = make_query(priorities=dict.fromkeys(config.CRITERIA_KEYS, "none"))

    result = compute_effective_weights(query)

    assert result.weights == {}
    assert result.total == 0


def test_zero_total_when_remaining_criteria_are_none_or_not_applicable() -> None:
    query = make_query(
        learning_mode="online",
        max_budget_vnd=None,
        time_slots=None,
        priorities=priorities(experience="none", rating="none"),
    )

    result = compute_effective_weights(query)

    assert result.weights == {}
    assert result.total == 0


def test_result_does_not_expose_a_status_string() -> None:
    """Trạng thái `zero_weight` do API (Sprint 4) sinh ra, module này không sinh."""
    result = compute_effective_weights(
        make_query(priorities=dict.fromkeys(config.CRITERIA_KEYS, "none"))
    )

    assert not hasattr(result, "status")
    assert "zero_weight" not in repr(result)


def test_total_equals_sum_of_effective_weights() -> None:
    result = compute_effective_weights(
        make_query(priorities=priorities(fee="low", rating="high"))
    )

    assert result.total == sum(result.weights.values())


def test_weights_keep_criteria_order_from_config() -> None:
    result = compute_effective_weights(make_query())

    assert tuple(result.weights) == config.CRITERIA_KEYS
