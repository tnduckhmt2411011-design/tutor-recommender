"""Kiểm thử đơn vị cho module lọc điều kiện bắt buộc (filters.py).

Trách nhiệm:
- Kiểm tra lọc môn học, hình thức dạy và giao khung thời gian
- Kiểm thử các ca biên theo mục 5.1

Mục tương ứng trong đề cương: Mục 3.6 (Bước 2), Mục 5.1.
"""

from app.schemas.search_request import SearchRequest
from app.schemas.tutor import TutorProfile
from app.scoring.filters import filter_mandatory


def make_tutor(tutor_id: str = "GS-X", **overrides: object) -> TutorProfile:
    """Dựng hồ sơ gia sư giả; mặc định dạy Toán, hình thức both, rảnh T2-tối."""
    data = {
        "tutor_id": tutor_id,
        "subjects": ["Toán"],
        "districts": ["Quận 1"],
        "hourly_fee_vnd": 200000,
        "years_experience": 3,
        "teaching_mode": "both",
        "availability": ["T2-tối"],
        "avg_rating": 4.0,
        "data_source": "simulated",
    }
    data.update(overrides)
    return TutorProfile(**data)


def make_query(**overrides: object) -> SearchRequest:
    """Dựng yêu cầu tìm kiếm giả; mặc định học Toán, hình thức any, không nhập giờ."""
    data = {"subject": "Toán", "learning_mode": "any"}
    data.update(overrides)
    return SearchRequest(**data)


def ids(tutors: list[TutorProfile]) -> list[str]:
    return [t.tutor_id for t in tutors]


# --- Môn học -----------------------------------------------------------------


def test_subject_mismatch_is_removed() -> None:
    tutors = [make_tutor("A", subjects=["Lý"]), make_tutor("B", subjects=["Toán"])]

    assert ids(filter_mandatory(tutors, make_query(subject="Toán"))) == ["B"]


def test_tutor_with_multiple_subjects_is_kept_when_one_matches() -> None:
    tutor = make_tutor("A", subjects=["Lý", "Hóa", "Toán"])

    assert ids(filter_mandatory([tutor], make_query(subject="Hóa"))) == ["A"]


def test_subject_match_is_exact_string_match() -> None:
    """QĐ-D: so khớp chuỗi chính xác, không chuẩn hóa hoa/thường."""
    tutors = [make_tutor("A", subjects=["Toán"])]

    assert filter_mandatory(tutors, make_query(subject="toán")) == []


# --- Hình thức học -----------------------------------------------------------


def test_in_person_query_removes_online_only_tutor() -> None:
    tutor = make_tutor("A", teaching_mode="online")

    assert filter_mandatory([tutor], make_query(learning_mode="in_person")) == []


def test_in_person_query_keeps_in_person_and_both_tutors() -> None:
    tutors = [
        make_tutor("A", teaching_mode="in_person"),
        make_tutor("B", teaching_mode="both"),
    ]

    result = filter_mandatory(tutors, make_query(learning_mode="in_person"))

    assert ids(result) == ["A", "B"]


def test_online_query_removes_in_person_only_tutor() -> None:
    tutor = make_tutor("A", teaching_mode="in_person")

    assert filter_mandatory([tutor], make_query(learning_mode="online")) == []


def test_online_query_keeps_online_and_both_tutors() -> None:
    tutors = [
        make_tutor("A", teaching_mode="online"),
        make_tutor("B", teaching_mode="both"),
    ]

    result = filter_mandatory(tutors, make_query(learning_mode="online"))

    assert ids(result) == ["A", "B"]


def test_any_query_keeps_every_teaching_mode() -> None:
    tutors = [
        make_tutor("A", teaching_mode="in_person"),
        make_tutor("B", teaching_mode="online"),
        make_tutor("C", teaching_mode="both"),
    ]

    result = filter_mandatory(tutors, make_query(learning_mode="any"))

    assert ids(result) == ["A", "B", "C"]


# --- Lịch rảnh ---------------------------------------------------------------


def test_zero_overlapping_slots_removes_tutor() -> None:
    tutor = make_tutor("A", availability=["T3-tối", "T5-tối"])

    result = filter_mandatory([tutor], make_query(time_slots=["T2-tối", "T4-tối"]))

    assert result == []


def test_exactly_one_overlapping_slot_keeps_tutor() -> None:
    tutor = make_tutor("A", availability=["T3-tối", "T4-tối"])

    result = filter_mandatory([tutor], make_query(time_slots=["T2-tối", "T4-tối"]))

    assert ids(result) == ["A"]


def test_no_time_slots_entered_does_not_filter_by_availability() -> None:
    tutor = make_tutor("A", availability=[])

    assert ids(filter_mandatory([tutor], make_query(time_slots=None))) == ["A"]


def test_empty_time_slot_list_is_treated_as_not_entered() -> None:
    tutor = make_tutor("A", availability=["T2-tối"])

    assert ids(filter_mandatory([tutor], make_query(time_slots=[]))) == ["A"]


def test_time_slot_match_is_exact_string_match() -> None:
    """QĐ-D: khung giờ so khớp chuỗi chính xác."""
    tutor = make_tutor("A", availability=["T2-tối"])

    assert filter_mandatory([tutor], make_query(time_slots=["t2-tối"])) == []


# --- Kết hợp và ca biên -----------------------------------------------------


def test_all_conditions_must_hold_together() -> None:
    query = make_query(
        subject="Toán", learning_mode="online", time_slots=["T2-tối"]
    )
    tutors = [
        make_tutor("ok", teaching_mode="online", availability=["T2-tối"]),
        make_tutor("sai_mon", subjects=["Lý"], teaching_mode="online"),
        make_tutor("sai_hinh_thuc", teaching_mode="in_person"),
        make_tutor("sai_gio", teaching_mode="online", availability=["T3-tối"]),
    ]

    assert ids(filter_mandatory(tutors, query)) == ["ok"]


def test_empty_input_returns_empty_list() -> None:
    result = filter_mandatory([], make_query())

    assert result == []
    assert isinstance(result, list)


def test_no_tutor_satisfies_returns_empty_list() -> None:
    tutors = [make_tutor("A", subjects=["Lý"]), make_tutor("B", subjects=["Hóa"])]

    result = filter_mandatory(tutors, make_query(subject="Toán"))

    assert result == []
    assert isinstance(result, list)


def test_input_order_is_preserved_and_input_is_not_modified() -> None:
    tutors = [make_tutor("C"), make_tutor("A", subjects=["Lý"]), make_tutor("B")]
    snapshot = list(tutors)

    result = filter_mandatory(tutors, make_query())

    assert ids(result) == ["C", "B"]
    assert tutors == snapshot
    assert result is not tutors
