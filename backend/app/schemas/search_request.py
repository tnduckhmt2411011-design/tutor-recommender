"""Định nghĩa cấu trúc dữ liệu yêu cầu tìm kiếm và mức độ ưu tiên của người học.

Trách nhiệm:
- Mô hình hóa bản ghi nhu cầu của người học theo ánh xạ từ Bảng 3.4
- Các trường: subject, learning_mode, preferred_district, max_budget_vnd, time_slots, priorities, top_k
- Quy tắc kiểm tra tính hợp lệ cơ bản (Mục 3.6 - Bước 1 và API Contract Mục 4.3)

Mục tương ứng trong đề cương:
- Mục 3.5. Thiết kế dữ liệu
- Bảng 3.4. Cấu trúc bản ghi nhu cầu của người học
- Bảng 3.5. Quy đổi mức ưu tiên sang trọng số
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, StrictInt, field_validator

from app.core.config import CRITERIA_KEYS, DEFAULT_PRIORITY

LearningMode = Literal["in_person", "online", "any"]
PriorityLevel = Literal["none", "low", "medium", "high"]


def default_priorities() -> dict[str, PriorityLevel]:
    """Mặc định mọi tiêu chí ở mức trung bình theo Bảng 3.5."""
    return {key: DEFAULT_PRIORITY for key in CRITERIA_KEYS}


class SearchRequest(BaseModel):
    """Nhu cầu tìm gia sư của người học theo Bảng 3.4 và Hợp đồng API."""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "subject": "Toán",
                "learning_mode": "in_person",
                "preferred_district": "Bình Thạnh",
                "max_budget_vnd": 200000,
                "time_slots": ["T2-tối", "T4-tối", "T7-sáng"],
                "priorities": {
                    "fee": "medium",
                    "district": "medium",
                    "experience": "medium",
                    "rating": "medium",
                    "availability": "medium",
                },
                "top_k": 3,
            }
        },
    )

    subject: str = Field(
        ...,
        min_length=1,
        description="Môn học cần tìm gia sư (bắt buộc, chọn đúng một môn).",
    )
    learning_mode: LearningMode = Field(
        ...,
        description="Hình thức học mong muốn: in_person (Trực tiếp), online (Trực tuyến), any (Không yêu cầu).",
    )
    preferred_district: str | None = Field(
        default=None,
        description="Khu vực mong muốn khi học trực tiếp (tùy chọn).",
    )
    max_budget_vnd: StrictInt | None = Field(
        default=None,
        ge=0,
        description="Ngân sách tối đa mỗi giờ theo VNĐ (tùy chọn, không âm).",
    )
    time_slots: list[str] | None = Field(
        default=None,
        description="Danh sách các khung thời gian rảnh mong muốn trong tuần (tùy chọn).",
    )
    priorities: dict[str, PriorityLevel] = Field(
        default_factory=default_priorities,
        description="Mức ưu tiên cho 5 tiêu chí (fee, district, experience, rating, availability): none, low, medium, high.",
    )
    top_k: StrictInt = Field(
        default=3,
        ge=1,
        le=20,
        description="Số lượng kết quả gợi ý tối đa cần lấy (1 <= top_k <= 20, mặc định 3).",
    )

    @field_validator("subject")
    @classmethod
    def validate_subject_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Môn học (subject) không được để trống.")
        return value

    @field_validator("priorities")
    @classmethod
    def validate_priority_keys(
        cls, value: dict[str, PriorityLevel]
    ) -> dict[str, PriorityLevel]:
        unknown_keys = [key for key in value if key not in CRITERIA_KEYS]
        if unknown_keys:
            raise ValueError(
                f"Khóa tiêu chí ưu tiên không hợp lệ: {unknown_keys}. Chỉ chấp nhận {CRITERIA_KEYS}."
            )
        return value
