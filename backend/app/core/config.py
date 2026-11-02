"""Quản lý các biến môi trường và thiết lập tham số khởi tạo cho thuật toán tính điểm.

Trách nhiệm:
- Khởi tạo tham số thuật toán: delta = 0.5 (ngưỡng vượt học phí), E_max = 8 (kinh nghiệm trần), rating_default = 0.5 (giá trị đánh giá trung tính)
- Trọng số mặc định của các mức ưu tiên: none=0, low=1, medium=2, high=3 (Bảng 3.5)
- Đường dẫn lưu trữ dữ liệu (tệp JSON, CSV hoặc cơ sở dữ liệu SQLite)

Mục tương ứng trong đề cương:
- Mục 3.6. Thiết kế thuật toán (Cơ sở của các tham số)
- Bảng 3.5. Quy đổi mức ưu tiên sang trọng số
"""

from pathlib import Path

# Tham số thuật toán theo Mục 3.6 và Bảng 3.6.
DELTA = 0.5
E_MAX = 8
RATING_DEFAULT = 0.5

# Quy đổi mức ưu tiên sang trọng số theo Bảng 3.5.
PRIORITY_WEIGHTS = {"none": 0, "low": 1, "medium": 2, "high": 3}
DEFAULT_PRIORITY = "medium"

# Tên khóa của 5 tiêu chí ưu tiên dùng thống nhất trong toàn bộ hệ thống.
CRITERIA_KEYS = ("fee", "district", "experience", "rating", "availability")

# Đường dẫn dữ liệu tính từ vị trí tệp này để không phụ thuộc thư mục chạy.
REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "data" / "processed"
TUTORS_JSON_PATH = DATA_DIR / "tutors.json"
TUTORS_CSV_PATH = DATA_DIR / "tutors.csv"
