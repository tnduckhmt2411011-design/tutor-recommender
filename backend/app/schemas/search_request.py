"""Định nghĩa cấu trúc dữ liệu yêu cầu tìm kiếm và mức độ ưu tiên của người học.

Trách nhiệm:
- Mô hình hóa bản ghi nhu cầu của người học theo ánh xạ từ Bảng 3.4
- Các trường: subject, learning_mode, preferred_district, max_budget_vnd, time_slots, priorities
- Quy tắc kiểm tra tính hợp lệ cơ bản (Mục 3.6 - Bước 1)

Mục tương ứng trong đề cương:
- Mục 3.5. Thiết kế dữ liệu
- Bảng 3.4. Cấu trúc bản ghi nhu cầu của người học
- Bảng 3.5. Quy đổi mức ưu tiên sang trọng số
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.core.config import CRITERIA_KEYS, DEFAULT_PRIORITY

LearningMode = Literal["in_person", "online", "any"]
PriorityLevel = Literal["none", "low", "medium", "high"]


def default_priorities() -> dict[str, PriorityLevel]:
    """Mặc định mọi tiêu chí ở mức trung bình theo Bảng 3.5."""
    return {key: DEFAULT_PRIORITY for key in CRITERIA_KEYS}


class SearchRequest(BaseModel):
    """Nhu cầu tìm gia sư của người học theo Bảng 3.4."""

    model_config = ConfigDict(extra="forbid")

    subject: str
    learning_mode: LearningMode
    preferred_district: str | None = None
    max_budget_vnd: int | None = None
    time_slots: list[str] | None = None
    priorities: dict[str, PriorityLevel] = Field(default_factory=default_priorities)
