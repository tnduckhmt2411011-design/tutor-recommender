"""Kiểm tra tính hợp lệ của data/processed/tutors.json và tutors.csv.

Script chỉ đọc dữ liệu, không chứa công thức tính điểm. Chạy tại thư mục gốc repo:

    python scripts/validate_tutors.py
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
JSON_PATH = DATA_DIR / "tutors.json"
CSV_PATH = DATA_DIR / "tutors.csv"

FIELDS = [
    "tutor_id",
    "subjects",
    "districts",
    "hourly_fee_vnd",
    "years_experience",
    "teaching_mode",
    "availability",
    "avg_rating",
    "data_source",
]
LIST_FIELDS = ("subjects", "districts", "availability")
TEACHING_MODES = {"in_person", "online", "both"}
DATA_SOURCES = {"public_collected", "simulated", "estimated"}
PII_PATTERN = re.compile(
    r"(\+?84|0)\d{9,10}|[\w.+-]+@[\w-]+\.[\w.]+|"
    r"(facebook|zalo|email|sdt|so dien thoai|hotline|dia chi|contact)",
    re.IGNORECASE,
)

errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def parse_list(value: str) -> list[str]:
    value = value.strip()
    return [] if not value else [item.strip() for item in value.split(",")]


def main() -> int:
    tutors = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    # 1. Số lượng bản ghi và tỉ lệ nguồn dữ liệu
    check(len(tutors) == 16, f"JSON phải có đúng 16 bản ghi, đang có {len(tutors)}")
    check(len(rows) == 16, f"CSV phải có đúng 16 dòng, đang có {len(rows)}")
    public_count = sum(1 for t in tutors if t.get("data_source") == "public_collected")
    simulated_count = sum(1 for t in tutors if t.get("data_source") == "simulated")
    check(public_count == 2, f"Phải có 2 bản ghi public_collected, đang có {public_count}")
    check(simulated_count == 14, f"Phải có 14 bản ghi simulated, đang có {simulated_count}")

    # 2. Mã gia sư duy nhất
    ids = [t.get("tutor_id") for t in tutors]
    check(len(ids) == len(set(ids)), "tutor_id bị trùng trong tutors.json")
    check(len(rows) == len({r.get("tutor_id") for r in rows}), "tutor_id bị trùng trong tutors.csv")

    # 3. Đủ 9 trường, kiểu dữ liệu và enum hợp lệ
    for tutor in tutors:
        tid = tutor.get("tutor_id", "<không có id>")
        check(list(tutor.keys()) == FIELDS, f"{tid}: sai hoặc thiếu trường so với data dictionary")
        check(isinstance(tutor.get("subjects"), list) and tutor["subjects"], f"{tid}: subjects phải là list không rỗng")
        check(isinstance(tutor.get("districts"), list), f"{tid}: districts phải là list")
        check(isinstance(tutor.get("availability"), list) and tutor["availability"], f"{tid}: availability phải là list không rỗng")
        check(isinstance(tutor.get("hourly_fee_vnd"), int) and tutor["hourly_fee_vnd"] >= 0, f"{tid}: hourly_fee_vnd không hợp lệ")
        check(isinstance(tutor.get("years_experience"), (int, float)) and tutor["years_experience"] >= 0, f"{tid}: years_experience không hợp lệ")
        check(tutor.get("teaching_mode") in TEACHING_MODES, f"{tid}: teaching_mode không hợp lệ")
        check(tutor.get("data_source") in DATA_SOURCES, f"{tid}: data_source không hợp lệ")
        rating = tutor.get("avg_rating")
        check(rating is None or (isinstance(rating, (int, float)) and 0 <= rating <= 5), f"{tid}: avg_rating không hợp lệ")

    # 4. Không chứa thông tin định danh cá nhân
    for tutor in tutors:
        for field, value in tutor.items():
            if isinstance(value, str):
                check(not PII_PATTERN.search(value), f"{tutor.get('tutor_id')}: trường {field} có dấu hiệu thông tin liên hệ")
            elif isinstance(value, list):
                for item in value:
                    check(not PII_PATTERN.search(str(item)), f"{tutor.get('tutor_id')}: trường {field} có dấu hiệu thông tin liên hệ")

    # 5. JSON và CSV khớp nhau từng ô
    csv_by_id = {row["tutor_id"]: row for row in rows}
    for tutor in tutors:
        row = csv_by_id.get(tutor["tutor_id"])
        if row is None:
            errors.append(f"{tutor['tutor_id']}: có trong JSON nhưng không có trong CSV")
            continue
        for field in FIELDS:
            if field in LIST_FIELDS:
                json_value = tutor[field]
                csv_value = parse_list(row[field])
            elif field == "avg_rating":
                json_value = tutor[field]
                csv_value = float(row[field]) if row[field].strip() else None
            elif field in ("hourly_fee_vnd", "years_experience"):
                json_value = tutor[field]
                csv_value = int(row[field])
            else:
                json_value = tutor[field]
                csv_value = row[field]
            check(json_value == csv_value, f"{tutor['tutor_id']}: lệch giữa JSON và CSV ở trường {field}")

    if errors:
        print(f"THẤT BẠI - {len(errors)} lỗi:")
        for message in errors:
            print(f"  - {message}")
        return 1

    print("ĐẠT: 16 bản ghi (2 public_collected, 14 simulated); id duy nhất; enum hợp lệ;")
    print("     đủ 9 trường; không có thông tin liên hệ; JSON và CSV khớp nhau từng ô.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
