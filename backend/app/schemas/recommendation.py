"""Định nghĩa cấu trúc dữ liệu phản hồi danh sách gia sư gợi ý (Top-k).

Trách nhiệm:
- Mô hình hóa kết quả đầu ra của thuật toán: điểm tổng hợp (S), điểm thành phần từng tiêu chí (s_i), và mức đóng góp từng tiêu chí (w_i * s_i / sum(w_i))
- Mô hình hóa các trường thông báo đặc biệt (không có gia sư thỏa điều kiện, tổng trọng số bằng 0, không đủ dữ liệu để xếp hạng)

Mục tương ứng trong đề cương:
- Mục 3.6. Thiết kế thuật toán (Bước 4 và Các trường hợp đặc biệt)
- Mục 4.4. Xây dựng API gợi ý
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class RankedTutor(BaseModel):
    """Thông tin một gia sư đã xếp hạng trong danh sách gợi ý Top-k."""

    model_config = ConfigDict(extra="forbid")

    rank: int = Field(
        ...,
        description="Hạng của gia sư trong kết quả (liên tục từ 1).",
    )
    tutor_id: str = Field(
        ...,
        description="Mã định danh gia sư duy nhất.",
    )
    total_score: float = Field(
        ...,
        description="Điểm tổng hợp S theo công thức Weighted Scoring.",
    )
    criteria_scores: dict[str, float | None] = Field(
        ...,
        description="Điểm thành phần s_i trong [0, 1] của 5 tiêu chí (null nếu không áp dụng hoặc w=0).",
    )
    contributions: dict[str, float | None] = Field(
        ...,
        description="Tỷ lệ đóng góp C_i = w_i * s_i / sum(w_i) của 5 tiêu chí.",
    )
    reason: str = Field(
        ...,
        description="Lý do gợi ý tiếng Việt tất định dựa trên các tiêu chí đóng góp cao nhất.",
    )
    notes: list[str] = Field(
        default_factory=list,
        description="Danh sách cảnh báo dữ liệu (ví dụ: ['chưa có đánh giá']).",
    )


class RecommendationSuccessResponse(BaseModel):
    """Phản hồi khi xếp hạng thành công (status = 'success' — Mục 3 API Contract)."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["success"] = Field(
        default="success",
        description="Trạng thái xử lý thành công.",
    )
    total_candidates: int = Field(
        ...,
        description="Tổng số hồ sơ gia sư trong kho dữ liệu.",
    )
    qualified_candidates: int = Field(
        ...,
        description="Số gia sư qua lọc bắt buộc (Bảng 3.2), đếm trước khi áp ngưỡng dữ liệu.",
    )
    insufficient_data_candidates: list[str] = Field(
        default_factory=list,
        description="Danh sách mã gia sư qua lọc bắt buộc nhưng bị loại do không đủ dữ liệu.",
    )
    results: list[RankedTutor] = Field(
        default_factory=list,
        description="Danh sách gia sư đã xếp hạng (tối đa top_k phần tử).",
    )


class NoMatchResponse(BaseModel):
    """Phản hồi khi không có gia sư thỏa điều kiện hoặc tất cả bị loại do thiếu dữ liệu (Mục 4.1 & 4.4)."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["no_match"] = Field(
        default="no_match",
        description="Trạng thái không có kết quả phù hợp.",
    )
    message: str = Field(
        ...,
        description="Thông báo hướng dẫn cho người học.",
    )
    total_candidates: int = Field(
        ...,
        description="Tổng số hồ sơ gia sư trong kho dữ liệu.",
    )
    qualified_candidates: int = Field(
        ...,
        description="Số gia sư qua lọc bắt buộc trước khi áp ngưỡng dữ liệu.",
    )
    insufficient_data_candidates: list[str] = Field(
        default_factory=list,
        description="Danh sách mã gia sư qua lọc bắt buộc nhưng không đủ dữ liệu để xếp hạng.",
    )
    results: list[RankedTutor] = Field(
        default_factory=list,
        description="Danh sách kết quả rỗng ([]).",
    )


class ZeroWeightResponse(BaseModel):
    """Phản hồi khi tổng trọng số các tiêu chí đang áp dụng bằng 0 (Mục 4.2)."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["zero_weight"] = Field(
        default="zero_weight",
        description="Trạng thái tổng trọng số bằng 0.",
    )
    message: str = Field(
        ...,
        description="Thông báo yêu cầu chọn ít nhất một tiêu chí ưu tiên.",
    )
    total_candidates: int = Field(
        ...,
        description="Tổng số hồ sơ gia sư trong kho dữ liệu.",
    )
    qualified_candidates: int = Field(
        ...,
        description="Số gia sư qua lọc bắt buộc.",
    )
    unranked_candidates: list[str] = Field(
        default_factory=list,
        description="Danh sách mã gia sư thỏa điều kiện bắt buộc nhưng chưa thể xếp hạng.",
    )


RecommendationResponse = (
    RecommendationSuccessResponse | NoMatchResponse | ZeroWeightResponse
)
