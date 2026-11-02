"""Chuyển đổi mức độ ưu tiên của người học thành trọng số tính toán.

Trách nhiệm:
- Ánh xạ mức ưu tiên sang trọng số w_i theo Bảng 3.5:
  + Không quan tâm: 0
  + Thấp: 1
  + Trung bình (mặc định): 2
  + Cao: 3
- Xử lý loại trừ tiêu chí không áp dụng (ví dụ học Trực tuyến không tính tiêu chí khu vực)
- Kiểm tra điều kiện tổng trọng số bằng 0 (sum(w_i) == 0)

Mục tương ứng trong đề cương:
- Mục 3.6. Thiết kế thuật toán (Bảng 3.5 và Các trường hợp đặc biệt)
"""

from dataclasses import dataclass

from app.core.config import CRITERIA_KEYS, DEFAULT_PRIORITY, PRIORITY_WEIGHTS
from app.schemas.search_request import SearchRequest


@dataclass(frozen=True)
class EffectiveWeights:
    """Trọng số hiệu lực của các tiêu chí đang áp dụng và tổng trọng số.

    `weights` chỉ chứa tiêu chí áp dụng có w > 0, theo thứ tự `CRITERIA_KEYS`.
    Tổng trọng số bằng 0 là kết quả hợp lệ; trạng thái `zero_weight` (nếu cần)
    do API (Sprint 4) sinh ra từ `total == 0`.
    """

    weights: dict[str, int]
    total: int


def priority_to_weight(level: str) -> int:
    """Quy đổi mức ưu tiên sang trọng số w theo Bảng 3.5 (`PRIORITY_WEIGHTS`)."""
    return PRIORITY_WEIGHTS[level]


def _applicable_criteria(query: SearchRequest) -> dict[str, bool]:
    """Tiêu chí nào áp dụng cho truy vấn (scoring-spec mục 6, các mục 1 và 2)."""
    return {
        "fee": query.max_budget_vnd is not None,
        "district": query.learning_mode in ("in_person", "any")
        and bool(query.preferred_district),
        "experience": True,
        "rating": True,
        "availability": bool(query.time_slots),
    }


def compute_effective_weights(query: SearchRequest) -> EffectiveWeights:
    """Xác định trọng số hiệu lực: bỏ tiêu chí không áp dụng và tiêu chí có w = 0."""
    applicable = _applicable_criteria(query)
    weights: dict[str, int] = {}
    for key in CRITERIA_KEYS:
        if not applicable[key]:
            continue
        weight = priority_to_weight(query.priorities.get(key, DEFAULT_PRIORITY))
        if weight > 0:
            weights[key] = weight
    return EffectiveWeights(weights=weights, total=sum(weights.values()))
