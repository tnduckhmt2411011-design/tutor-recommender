"""Lớp truy xuất và đọc nạp dữ liệu hồ sơ gia sư từ các nguồn lưu trữ (JSON/CSV/SQLite).

Trách nhiệm:
- Đọc nạp danh sách hồ sơ gia sư từ tập tin JSON/CSV hoặc SQLite
- Cung cấp hàm truy vấn danh sách ứng viên phục vụ quy trình lọc và tính điểm
- Đảm bảo tuân thủ nguyên tắc ẩn danh dữ liệu mẫu

Mục tương ứng trong đề cương:
- Mục 3.5. Thiết kế dữ liệu
- Mục 4.2. Chuẩn bị dữ liệu mẫu
"""

import json
from pathlib import Path

from pydantic import ValidationError

from app.core.config import TUTORS_JSON_PATH
from app.schemas.tutor import TutorProfile


class TutorDataError(Exception):
    """Lỗi khi đọc hoặc xác thực tệp dữ liệu hồ sơ gia sư (thông điệp tiếng Việt)."""


class TutorRepository:
    """Đọc tệp JSON hồ sơ gia sư và ánh xạ thành danh sách `TutorProfile`."""

    def __init__(self, path: Path = TUTORS_JSON_PATH) -> None:
        self.path = Path(path)

    def get_all(self) -> list[TutorProfile]:
        """Trả toàn bộ hồ sơ gia sư theo thứ tự trong tệp, không sửa dữ liệu nguồn."""
        if not self.path.is_file():
            raise TutorDataError(f"Không tìm thấy tệp dữ liệu gia sư: {self.path}")

        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except ValueError as exc:
            raise TutorDataError(
                f"Tệp dữ liệu gia sư không phải JSON hợp lệ: {self.path} ({exc})"
            ) from exc

        if not isinstance(payload, list):
            raise TutorDataError(
                f"Tệp dữ liệu gia sư phải chứa một danh sách bản ghi: {self.path}"
            )

        return [self._parse_record(index, item) for index, item in enumerate(payload, 1)]

    @staticmethod
    def _parse_record(position: int, item: object) -> TutorProfile:
        """Xác thực một bản ghi theo `TutorProfile`; lỗi nêu rõ vị trí và mã gia sư."""
        try:
            return TutorProfile.model_validate(item)
        except ValidationError as exc:
            tutor_id = item.get("tutor_id", "không rõ") if isinstance(item, dict) else "không rõ"
            raise TutorDataError(
                f"Bản ghi số {position} ({tutor_id}) không hợp lệ theo Bảng 3.3: {exc}"
            ) from exc
