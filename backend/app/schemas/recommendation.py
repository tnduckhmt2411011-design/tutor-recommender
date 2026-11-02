"""Định nghĩa cấu trúc dữ liệu phản hồi danh sách gia sư gợi ý (Top-k).

Trách nhiệm:
- Mô hình hóa kết quả đầu ra của thuật toán: điểm tổng hợp (S), điểm thành phần từng tiêu chí (s_i), và mức đóng góp từng tiêu chí (w_i * s_i / sum(w_i))
- Mô hình hóa các trường thông báo đặc biệt (không có gia sư thỏa điều kiện, tổng trọng số bằng 0, không đủ dữ liệu để xếp hạng)

Mục tương ứng trong đề cương:
- Mục 3.6. Thiết kế thuật toán (Bước 4 và Các trường hợp đặc biệt)
- Mục 4.4. Xây dựng API gợi ý
"""

from pydantic import BaseModel, ConfigDict


class RankedTutor(BaseModel):
    """Thông tin một gia sư đã xếp hạng trong danh sách gợi ý Top-k."""

    model_config = ConfigDict(extra="forbid")

    rank: int
    tutor_id: str
    total_score: float
    criteria_scores: dict[str, float | None]
    contributions: dict[str, float | None]
    reason: str
    notes: list[str]
