"""Quy tắc kiểm tra điều kiện đủ dữ liệu để được xếp hạng.

Trách nhiệm:
- Đếm số tiêu chí ưu tiên mà gia sư có dữ liệu trong số n tiêu chí đang áp dụng (không tính tiêu chí Đánh giá vì luôn dùng giá trị trung tính 0.5)
- So sánh với bảng ngưỡng dữ liệu tối thiểu:
  + n = 1: ngưỡng 1
  + n = 2: ngưỡng 2
  + n = 3: ngưỡng 2
  + n = 4: ngưỡng 3
  + n = 5: ngưỡng 4
- Đánh dấu loại gia sư không đủ dữ liệu kèm ghi chú 'Không đủ dữ liệu để xếp hạng'

Mục tương ứng trong đề cương:
- Mục 3.6. Thiết kế thuật toán (Điều kiện đủ dữ liệu để được xếp hạng)
- Bảng ngưỡng dữ liệu tối thiểu để được xếp hạng
"""

from app.schemas.tutor import TutorProfile
from app.scoring.weights import EffectiveWeights

MIN_DATA_THRESHOLD: dict[int, int] = {
    0: 0,
    1: 1,
    2: 2,
    3: 2,
    4: 3,
    5: 4,
}


def get_min_required_criteria(n_applicable: int) -> int:
    """Tra cứu số tiêu chí tối thiểu cần có dữ liệu theo Bảng ngưỡng Mục 3.6."""
    if n_applicable not in MIN_DATA_THRESHOLD:
        raise ValueError(
            f"Số tiêu chí áp dụng không hợp lệ: {n_applicable} (phải từ 0 đến 5)."
        )
    return MIN_DATA_THRESHOLD[n_applicable]


def _has_criterion_data(tutor: TutorProfile, criterion_key: str) -> bool:
    """Kiểm tra hồ sơ gia sư có dữ liệu thực tế cho tiêu chí chỉ định hay không."""
    if criterion_key == "fee":
        return tutor.hourly_fee_vnd is not None
    if criterion_key == "district":
        return len(tutor.districts) > 0
    if criterion_key == "experience":
        return tutor.years_experience is not None
    if criterion_key == "availability":
        return len(tutor.availability) > 0
    return True


def count_available_criteria(
    tutor: TutorProfile,
    effective_weights: EffectiveWeights,
) -> tuple[int, int]:
    """Đếm `(số_tiêu_chí_có_dữ_liệu, n_tiêu_chí_áp_dụng)` (loại trừ `rating`)."""
    applicable_non_rating = [
        key for key in effective_weights.weights if key != "rating"
    ]
    n_applicable = len(applicable_non_rating)
    available_count = sum(
        1 for key in applicable_non_rating if _has_criterion_data(tutor, key)
    )
    return available_count, n_applicable


def check_tutor_eligibility(
    tutor: TutorProfile,
    effective_weights: EffectiveWeights,
) -> bool:
    """Kiểm tra hồ sơ gia sư có đạt ngưỡng dữ liệu tối thiểu để xếp hạng hay không."""
    available_count, n_applicable = count_available_criteria(tutor, effective_weights)
    min_required = get_min_required_criteria(n_applicable)
    return available_count >= min_required


check_data_threshold = check_tutor_eligibility


def filter_eligible_candidates(
    tutors: list[TutorProfile],
    effective_weights: EffectiveWeights,
) -> tuple[list[TutorProfile], list[str]]:
    """Phân tách danh sách ứng viên thành `(đủ_dữ_liệu, danh_sách_tutor_id_thiếu_dữ_liệu)`."""
    eligible: list[TutorProfile] = []
    insufficient_ids: list[str] = []
    for tutor in tutors:
        if check_tutor_eligibility(tutor, effective_weights):
            eligible.append(tutor)
        else:
            insufficient_ids.append(tutor.tutor_id)
    return eligible, insufficient_ids
