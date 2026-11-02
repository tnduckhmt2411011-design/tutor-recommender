"""Hàm tính điểm chuẩn hóa từng tiêu chí ưu tiên (s_i in [0, 1]).

Trách nhiệm:
- Hiện thực Bước 3 trong quy trình tính điểm mục 3.6
- Tính điểm học phí: s = 1 nếu P <= B, s = max(0, 1 - (P - B) / (delta * B)) nếu P > B (với delta = 0.5)
- Tính điểm khu vực: s = 1 nếu khu vực thuộc danh sách dạy, ngược lại s = 0 (bỏ qua nếu học trực tuyến)
- Tính điểm kinh nghiệm: s = min(E / E_max, 1) với E_max = 8
- Tính điểm đánh giá: s = R / 5; giá trị trung tính 0.5 nếu chưa có đánh giá
- Tính điểm lịch rảnh: s = |L ∩ T| / |L| (tỷ lệ khung giờ giao nhau)

Mục tương ứng trong đề cương:
- Mục 3.6. Thiết kế thuật toán (Bước 3: Tính điểm thành phần)
- Bảng 3.6. Công thức điểm thành phần
"""

from collections.abc import Collection

from app.core.config import DELTA, E_MAX, RATING_DEFAULT


def score_fee(price: float, budget: float, delta: float = DELTA) -> float:
    """Điểm học phí: 1 nếu P <= B, ngược lại max(0, 1 - (P - B) / (delta * B)).

    Khi B = 0 (QĐ-A): P = 0 cho 1, P > 0 cho 0. P < 0 hoặc B < 0 ném ValueError (QĐ-B).
    """
    if price < 0:
        raise ValueError("Học phí gia sư không được âm.")
    if budget < 0:
        raise ValueError("Ngân sách không được âm.")
    if price <= budget:
        return 1.0
    if budget == 0:
        return 0.0
    return max(0.0, 1.0 - (price - budget) / (delta * budget))


def score_location(learner_district: str, tutor_districts: Collection[str]) -> float:
    """Điểm khu vực: 1 nếu khu vực người học thuộc khu vực gia sư dạy, ngược lại 0.

    So khớp chuỗi chính xác (QĐ-D). Việc bỏ qua tiêu chí khi học trực tuyến do
    `weights.py` đảm nhiệm (QĐ-C).
    """
    return 1.0 if learner_district in tutor_districts else 0.0


def score_experience(years: float, e_max: float = E_MAX) -> float:
    """Điểm kinh nghiệm: min(E / E_max, 1). E < 0 ném ValueError (QĐ-B)."""
    if years < 0:
        raise ValueError("Số năm kinh nghiệm không được âm.")
    return min(years / e_max, 1.0)


def score_rating(rating: float | None) -> float:
    """Điểm đánh giá: R / 5; chưa có đánh giá (None) dùng giá trị trung tính.

    R ngoài đoạn [0, 5] ném ValueError (QĐ-B).
    """
    if rating is None:
        return float(RATING_DEFAULT)
    if not 0 <= rating <= 5:
        raise ValueError("Điểm đánh giá phải nằm trong khoảng từ 0 đến 5.")
    return rating / 5


def score_schedule(
    learner_slots: Collection[str], tutor_slots: Collection[str]
) -> float:
    """Điểm lịch rảnh: |L ∩ T| / |L|. Tập khung giờ người học rỗng ném ValueError (QĐ-B).

    Tiền đề |L ∩ T| >= 1 do bộ lọc bắt buộc đảm bảo; hàm thuần vẫn trả 0 nếu không giao.
    """
    learner = set(learner_slots)
    if not learner:
        raise ValueError("Danh sách khung giờ của người học không được rỗng.")
    return len(learner & set(tutor_slots)) / len(learner)
