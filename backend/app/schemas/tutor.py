"""Định nghĩa cấu trúc dữ liệu hồ sơ gia sư.

Trách nhiệm:
- Mô hình hóa bản ghi hồ sơ gia sư theo ánh xạ từ Bảng 3.3
- Các trường: tutor_id, subjects, districts, hourly_fee_vnd, years_experience, teaching_mode, availability, avg_rating, data_source

Mục tương ứng trong đề cương:
- Mục 3.5. Thiết kế dữ liệu
- Bảng 3.3. Cấu trúc bản ghi hồ sơ gia sư
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict

TeachingMode = Literal["in_person", "online", "both"]
DataSource = Literal["public_collected", "simulated", "estimated"]


class TutorProfile(BaseModel):
    """Hồ sơ gia sư đã chuẩn hóa theo Bảng 3.3."""

    model_config = ConfigDict(extra="forbid")

    tutor_id: str
    subjects: list[str]
    districts: list[str]
    hourly_fee_vnd: int
    years_experience: float
    teaching_mode: TeachingMode
    availability: list[str]
    avg_rating: float | None
    data_source: DataSource
