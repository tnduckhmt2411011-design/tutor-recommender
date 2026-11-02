"""Kiểm thử đơn vị cho các hàm tính điểm tiêu chí thành phần (criteria.py).

Trách nhiệm:
- Kiểm tra tính điểm học phí, khu vực, kinh nghiệm, đánh giá, lịch rảnh theo Bảng 3.6
- Kiểm tra tính đơn điệu và các ca biên theo mục 5.1

Mục tương ứng trong đề cương: Mục 3.6 (Bảng 3.6), Mục 5.1.

Quy ước đặt tên:
- `test_bang_3_6_*`: đúng 15 ca lấy trực tiếp từ ví dụ Bảng 3.6 (3 ca x 5 tiêu chí).
- `test_bo_sung_*`: ca bổ sung theo Issue #15 (lịch rảnh giao 0/3, 2/3, 3/3).
- `test_bien_*`: ca biên theo Mục 5.1 và quyết định QĐ-A, QĐ-B.
- `test_don_dieu_*`: kiểm thử tính đơn điệu.
"""

import inspect
import itertools

import pytest

from app.core import config
from app.scoring.criteria import (
    score_experience,
    score_fee,
    score_location,
    score_rating,
    score_schedule,
)

BUDGET = 200_000
SLOTS_3 = ["T2-tối", "T4-tối", "T7-sáng"]
SLOTS_7 = [
    "T2-tối",
    "T3-tối",
    "T4-tối",
    "T5-tối",
    "T6-tối",
    "T7-sáng",
    "CN-sáng",
]
SLOTS_4 = ["T2-tối", "T4-tối", "T6-tối", "CN-chiều"]


# --- 15 ca Bảng 3.6 ----------------------------------------------------------


@pytest.mark.parametrize(
    ("price", "expected"),
    [
        pytest.param(180_000, 1.0, id="P=180000"),
        pytest.param(230_000, 0.7, id="P=230000"),
        pytest.param(300_000, 0.0, id="P=300000"),
    ],
)
def test_bang_3_6_fee(price: int, expected: float) -> None:
    assert score_fee(price, BUDGET) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("tutor_districts", "expected"),
    [
        pytest.param(["KV1", "KV2"], 1.0, id="gia_su_day_KV1_KV2"),
        pytest.param(["KV3"], 0.0, id="gia_su_day_KV3"),
        pytest.param([], 0.0, id="gia_su_chi_truc_tuyen"),
    ],
)
def test_bang_3_6_location(tutor_districts: list[str], expected: float) -> None:
    assert score_location("KV1", tutor_districts) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("years", "expected"),
    [
        pytest.param(0, 0.0, id="E=0"),
        pytest.param(4, 0.5, id="E=4"),
        pytest.param(10, 1.0, id="E=10"),
    ],
)
def test_bang_3_6_experience(years: float, expected: float) -> None:
    assert score_experience(years) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("rating", "expected"),
    [
        pytest.param(5, 1.0, id="R=5"),
        pytest.param(4.5, 0.9, id="R=4.5"),
        pytest.param(3, 0.6, id="R=3"),
    ],
)
def test_bang_3_6_rating(rating: float, expected: float) -> None:
    assert score_rating(rating) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("learner_slots", "tutor_slots", "expected"),
    [
        pytest.param(
            SLOTS_3, ["T2-tối", "T7-sáng", "T3-tối"], 2 / 3, id="giao_2_tren_3"
        ),
        pytest.param(
            SLOTS_7,
            ["T2-tối", "T3-tối", "T4-tối", "T5-tối", "T6-tối", "T7-sáng"],
            6 / 7,
            id="giao_6_tren_7",
        ),
        pytest.param(SLOTS_4, ["T2-tối", "T3-tối"], 0.25, id="giao_1_tren_4"),
    ],
)
def test_bang_3_6_schedule(
    learner_slots: list[str], tutor_slots: list[str], expected: float
) -> None:
    assert score_schedule(learner_slots, tutor_slots) == pytest.approx(expected)


# --- Ca bổ sung theo Issue #15 (lịch rảnh 0/3, 2/3, 3/3) ---------------------


def test_bo_sung_schedule_overlap_0_of_3() -> None:
    """Hàm thuần: tiền đề |L ∩ T| >= 1 do bộ lọc đảm bảo, hàm vẫn trả 0,0."""
    assert score_schedule(SLOTS_3, ["T3-tối", "T5-tối"]) == pytest.approx(0.0)


def test_bo_sung_schedule_overlap_2_of_3() -> None:
    assert score_schedule(SLOTS_3, ["T2-tối", "T7-sáng"]) == pytest.approx(2 / 3)


def test_bo_sung_schedule_overlap_3_of_3() -> None:
    assert score_schedule(SLOTS_3, [*SLOTS_3, "CN-tối"]) == pytest.approx(1.0)


# --- Ca biên Mục 5.1 ---------------------------------------------------------


def test_bien_fee_equal_to_budget_is_full_score() -> None:
    assert score_fee(BUDGET, BUDGET) == pytest.approx(1.0)


def test_bien_fee_exceeding_budget_by_exactly_50_percent_is_zero() -> None:
    assert score_fee(300_000, BUDGET) == pytest.approx(0.0)


def test_bien_fee_exceeding_budget_by_more_than_50_percent_is_zero_not_negative() -> (
    None
):
    assert score_fee(400_000, BUDGET) == 0.0


def test_bien_fee_zero_budget_and_zero_price_is_full_score() -> None:
    """QĐ-A: B = 0 và P = 0 thì s = 1."""
    assert score_fee(0, 0) == pytest.approx(1.0)


def test_bien_fee_zero_budget_and_positive_price_is_zero() -> None:
    """QĐ-A: B = 0 và P > 0 thì s = 0 (tránh chia cho δ×B = 0)."""
    assert score_fee(1, 0) == 0.0
    assert score_fee(500_000, 0) == 0.0


def test_bien_experience_zero_is_zero() -> None:
    assert score_experience(0) == 0.0


def test_bien_experience_equal_to_e_max_is_full_score() -> None:
    assert score_experience(config.E_MAX) == pytest.approx(1.0)


def test_bien_experience_greater_than_e_max_is_capped_at_one() -> None:
    assert score_experience(config.E_MAX + 5) == pytest.approx(1.0)


def test_bien_rating_none_uses_neutral_default_from_config() -> None:
    assert score_rating(None) == pytest.approx(config.RATING_DEFAULT)
    assert score_rating(None) == pytest.approx(0.5)


def test_bien_rating_zero_is_zero_and_is_not_confused_with_none() -> None:
    assert score_rating(0) == 0.0


def test_bien_schedule_single_overlap_slot() -> None:
    assert score_schedule(SLOTS_4, ["CN-chiều"]) == pytest.approx(1 / 4)


def test_bien_schedule_overlap_is_all_learner_slots() -> None:
    assert score_schedule(["T2-tối"], ["T2-tối", "T3-tối"]) == pytest.approx(1.0)
    assert score_schedule(SLOTS_4, [*SLOTS_4, "T7-sáng"]) == pytest.approx(1.0)


def test_bien_location_is_exact_string_match() -> None:
    """QĐ-D: so khớp chuỗi chính xác, không chuẩn hóa hoa/thường."""
    assert score_location("kv1", ["KV1"]) == 0.0
    assert score_schedule(["t2-tối"], ["T2-tối"]) == 0.0


# --- Đầu vào ngoài miền hợp lệ (QĐ-B) ----------------------------------------


def test_bien_negative_price_raises_value_error() -> None:
    with pytest.raises(ValueError, match="Học phí gia sư không được âm"):
        score_fee(-1, BUDGET)


def test_bien_negative_budget_raises_value_error() -> None:
    with pytest.raises(ValueError, match="Ngân sách không được âm"):
        score_fee(100_000, -1)


def test_bien_negative_experience_raises_value_error() -> None:
    with pytest.raises(ValueError, match="Số năm kinh nghiệm không được âm"):
        score_experience(-0.5)


@pytest.mark.parametrize("rating", [-0.1, 5.1, 6, 100])
def test_bien_rating_outside_0_to_5_raises_value_error(rating: float) -> None:
    with pytest.raises(ValueError, match="Điểm đánh giá phải nằm trong khoảng"):
        score_rating(rating)


def test_bien_empty_learner_slot_set_raises_value_error() -> None:
    with pytest.raises(ValueError, match="khung giờ của người học không được rỗng"):
        score_schedule([], ["T2-tối"])


# --- Kiểu trả về và tham số mặc định lấy từ config ---------------------------


def test_all_five_functions_return_float_in_unit_interval() -> None:
    results = [
        score_fee(180_000, BUDGET),
        score_fee(230_000, BUDGET),
        score_fee(999_999, BUDGET),
        score_location("KV1", ["KV1"]),
        score_location("KV1", []),
        score_experience(0),
        score_experience(4),
        score_experience(10),
        score_rating(5),
        score_rating(None),
        score_rating(0),
        score_schedule(SLOTS_3, SLOTS_3),
        score_schedule(SLOTS_3, ["T3-tối"]),
    ]

    for value in results:
        assert isinstance(value, float)
        assert 0.0 <= value <= 1.0


def test_default_parameters_come_from_config() -> None:
    fee_default = inspect.signature(score_fee).parameters["delta"].default
    exp_default = inspect.signature(score_experience).parameters["e_max"].default

    assert fee_default == config.DELTA
    assert exp_default == config.E_MAX


def test_custom_delta_changes_fee_score_by_formula() -> None:
    # P = 225000, B = 200000: 1 - 25000 / (delta * 200000)
    assert score_fee(225_000, BUDGET) == pytest.approx(0.75)
    assert score_fee(225_000, BUDGET, delta=0.25) == pytest.approx(0.5)
    assert score_fee(300_000, BUDGET, delta=1.0) == pytest.approx(0.5)


def test_custom_e_max_changes_experience_score_by_formula() -> None:
    assert score_experience(5) == pytest.approx(5 / config.E_MAX)
    assert score_experience(5, e_max=10) == pytest.approx(0.5)
    assert score_experience(2, e_max=4) == pytest.approx(0.5)
    assert score_experience(6, e_max=4) == pytest.approx(1.0)


# --- Tính đơn điệu -----------------------------------------------------------


def test_don_dieu_fee_score_does_not_increase_as_price_increases() -> None:
    scores = [score_fee(price, BUDGET) for price in range(0, 500_001, 10_000)]

    assert all(a >= b for a, b in itertools.pairwise(scores))


def test_don_dieu_experience_score_does_not_decrease_as_years_increase() -> None:
    scores = [score_experience(years / 2) for years in range(41)]

    assert all(a <= b for a, b in itertools.pairwise(scores))


def test_don_dieu_rating_score_does_not_decrease_as_rating_increases() -> None:
    scores = [score_rating(step / 10) for step in range(51)]

    assert all(a <= b for a, b in itertools.pairwise(scores))


def test_don_dieu_schedule_score_does_not_decrease_as_overlap_increases() -> None:
    learner = SLOTS_7
    scores = [score_schedule(learner, learner[:k]) for k in range(len(learner) + 1)]

    assert all(a <= b for a, b in itertools.pairwise(scores))
    assert scores[0] == 0.0
    assert scores[-1] == pytest.approx(1.0)
