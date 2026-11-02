> [!NOTE]
> **Đề xuất, nhóm xác nhận**

# Kế hoạch Sprint 3 (Sprint 3 Planning)

- **Thời gian thực hiện:** Hạn: 2026-11-20 (theo Milestone Sprint 3); ngày bắt đầu: [Chờ nhóm điền]
- **Mục tiêu Sprint (Sprint Goal):** Xếp hạng và giải thích (E3) — cài đặt quy tắc kiểm tra ngưỡng dữ liệu tối thiểu, thuật toán tính điểm tổng hợp Weighted Scoring và xếp hạng Top-k kèm mức đóng góp tiêu chí và lời giải thích, tự động hóa kiểm thử 14 kịch bản thực nghiệm (`KB01`–`KB14`) và lập báo cáo phân tích đối chiếu kết quả để đạt Cổng chất lượng 2 (Quality Gate 2).
- **Giả định công suất nhóm:** 9 Story Points *(9 Must)*.

---

## 1. Danh sách User Stories cam kết trong Sprint

| Mã US | Tên User Story | Điểm SP | Mức ưu tiên | Mục đề cương | Issue | Phụ trách | Trạng thái |
|:---|:---|:---:|:---:|:---|:---:|:---:|:---:|
| **US-14** | Hiện thực cơ chế kiểm tra ngưỡng dữ liệu tối thiểu theo Bảng ngưỡng đề cương | 2 | Must | Mục 3.6 (Bảng ngưỡng dữ liệu tối thiểu) | #16 | *[Chờ nhóm phân công]* | Chưa làm |
| **US-15** | Tính điểm tổng hợp S(g), sắp xếp giảm dần (phá hòa theo mã hồ sơ) và lấy Top-k | 2 | Must | Mục 2.3, Mục 3.6 (Bước 4), CN02 | #17 | *[Chờ nhóm phân công]* | Chưa làm |
| **US-16** | Tính mức đóng góp của từng tiêu chí vào điểm tổng và sinh lời giải thích kèm ghi chú | 2 | Must | Mục 3.3, Mục 3.6 (Bước 4), CN02 | #18 | *[Chờ nhóm phân công]* | Chưa làm |
| **US-17** | Tự động hóa kiểm thử hồi quy 14 kịch bản đánh giá từ `scenarios.json` | 2 | Must | Mục 5.1, Mục 5.2, Bảng 5.1 | #19 | *[Chờ nhóm phân công]* | Chưa làm |
| **US-18** | Phân tích chi tiết nguyên nhân toán học và dữ liệu tại các kịch bản có sai lệch so với `expected_raw` | 1 | Must | Mục 5.2, Bảng 5.1 | #20 | *[Chờ nhóm phân công]* | Chưa làm |

- **Tổng điểm Story Points:** **9 SP** (9 Must).

---

## 2. Phân rã nhiệm vụ kỹ thuật (Tasks)

- **Phụ trách:** *[Chờ nhóm phân công]*
  - [ ] US-14 (#16): cập nhật kiểu tùy chọn trong `TutorProfile` phục vụ kiểm thử thiếu dữ liệu; cài đặt `MIN_DATA_THRESHOLD`, `get_min_required_criteria`, `count_available_criteria`, `check_tutor_eligibility`, `filter_eligible_candidates` trong `backend/app/scoring/eligibility.py`; hoàn thiện `backend/tests/unit/test_eligibility.py`.
  - [ ] US-15 (#17) + US-16 (#18): định nghĩa `RankedTutor` trong `backend/app/schemas/recommendation.py`; cài đặt `score_and_rank`, `build_reason`, `build_notes` trong `backend/app/scoring/ranker.py`; hoàn thiện `backend/tests/unit/test_ranker.py` (bao gồm ví dụ tính điểm tổng Mục 3.6 `S = 0,753`).
  - [ ] US-18 (#20): lập tài liệu `docs/thesis/report/discrepancy_analysis.md` đối chiếu kết quả thực chạy của hệ thống với kết quả kỳ vọng trên cả 14 kịch bản (`KB01`–`KB14`), phân tích chi tiết sai lệch điểm tại `KB04` và cơ chế phá hòa tại `KB02`, `KB12`.
  - [ ] US-17 (#19): hiện thực hóa bộ test tự động `backend/tests/scenarios/test_scenarios.py` chạy toàn bộ 14 kịch bản và xuất bảng tổng hợp đối chiếu; giữ nguyên tệp `scenarios.json`.

Phạm vi Sprint 3 chưa gồm tầng API FastAPI (`/api/recommend`, `test_recommend_api.py`) và giao diện người dùng (thuộc Sprint 4–5).

---

## 3. Tiêu chí Cổng chất lượng 2 (Quality Gate 2)

- [ ] Toàn bộ 5 hàm chuẩn hóa điểm và module xếp hạng vượt qua 100% unit test (bao gồm các ca từ Bảng 3.6).
- [ ] Bộ kiểm thử `test_scenarios.py` chạy tự động trên toàn bộ 14 kịch bản (`KB01`–`KB14`) và xuất bảng tổng hợp đối chiếu.
- [ ] Mọi kịch bản có sự khác biệt giữa kết quả hệ thống và `expected_raw` trong đề cương đều được ghi nhận và giải thích rõ nguyên nhân trong `docs/thesis/report/discrepancy_analysis.md`, không chỉnh sửa ngược `expected_top3` hay `expected_raw` trong `scenarios.json`.
