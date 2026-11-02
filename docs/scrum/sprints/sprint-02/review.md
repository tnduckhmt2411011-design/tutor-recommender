> [!NOTE]
> **Đề xuất, nhóm xác nhận**

# Sơ kết Sprint 2 (Sprint 2 Review)

- **Ngày họp:** *[Chờ nhóm điền]*
- **Người chủ trì:** Scrum Master (Trần Nguyễn Đức)
- **Thành phần tham dự:** *[Chờ nhóm điền]*

---

## 1. Kết quả thực hiện mục tiêu Sprint

- **Mục tiêu đặt ra:** Xây dựng lõi chấm điểm (E2) — gồm lớp truy xuất và nạp dữ liệu hồ sơ gia sư (`repository.py`), bộ lọc điều kiện bắt buộc (`filters.py`), 5 hàm chuẩn hóa điểm thành phần theo Bảng 3.6 (`criteria.py`), module quy đổi trọng số theo Bảng 3.5 (`weights.py`) và bộ unit test toàn diện cho các module trên.
- **Đánh giá mức độ hoàn thành:** *[Đạt / Chưa đạt]*

---

## 2. Rà soát chi tiết User Stories

| Mã US | Tên User Story | Điểm SP | Trạng thái | Ghi chú nghiệm thu |
|:---|:---|:---:|:---:|:---|
| US-09 | Xây dựng lớp truy xuất và nạp dữ liệu hồ sơ gia sư (Repository) | 2 | Xong (PR #52, PR #54) | Độ bao phủ `app/data/repository.py` đạt 100% (`pytest-cov`, 26/26 dòng lệnh) |
| US-10 | Cài đặt module lọc điều kiện bắt buộc theo Bảng 3.2 | 2 | Xong (PR #55) | 18 unit test tại `test_filters.py` |
| US-11 | Cài đặt 5 hàm chuẩn hóa điểm thành phần theo Bảng 3.6 | 3 | Xong (PR #56) | 5 hàm thuần trong `app/scoring/criteria.py` |
| US-12 | Cài đặt module quy đổi mức ưu tiên sang trọng số theo Bảng 3.5 | 1 | Xong (PR #57) | 18 unit test tại `test_weights.py` |
| US-13 | Bộ unit test toàn diện cho 5 hàm điểm và ca biên theo Bảng 3.6 | 2 | Xong (PR #56) | 47 unit test tại `test_criteria.py` (15 ca Bảng 3.6 + 3 ca bổ sung lịch rảnh + biên Mục 5.1) |

*Ghi chú về các PR đã merge trong Sprint 2 (đều do `tnduckhmt2411011-design` thực hiện):*
- **Nền tảng cấu hình & kế hoạch Sprint 2:** PR #52 (`feat/sprint-02-nen-tang-cau-hinh`, merge `9756bb1`, 2026-11-02) và PR #53 (`docs/sprint-02-planning`, merge `78ef1fb`, 2026-11-02).
- **US-09 (#11):** PR #54 (`feat/11-repository-du-lieu`, merge `4cfc913`, 2026-11-02).
- **US-10 (#12):** PR #55 (`feat/12-bo-loc-bat-buoc`, merge `bce9cb5`, 2026-11-02).
- **US-11 (#13) + US-13 (#15):** PR #56 (`feat/13-15-ham-diem-thanh-phan`, merge `f3b48ba`, 2026-11-02).
- **US-12 (#14):** PR #57 (`feat/14-quy-doi-trong-so`, merge `05f1170`, 2026-11-02).

---

## 3. Kết quả kiểm thử nghiệm thu kỹ thuật (T4)

- [x] `ruff check .` tại `backend/` chạy sạch (`All checks passed!`).
- [x] `pytest -rs` tại `backend/` đạt `107 passed, 4 skipped` (đúng 4 module của Sprint 3–4 còn giữ `pytest.skip`: `test_eligibility.py`, `test_ranker.py`, `test_scenarios.py`, `test_recommend_api.py`).
- [x] `pytest --cov=app.data.repository --cov-report=term-missing` đạt **100%** (26/26 statements).
- **Kết luận:** *[Đủ điều kiện chuyển sang Sprint 3 / Cần bổ sung]*
