> [!NOTE]
> **Đề xuất, nhóm xác nhận**

# Kế hoạch Sprint 2 (Sprint 2 Planning)

- **Thời gian thực hiện:** Hạn: 2026-11-06 (theo Milestone Sprint 2); ngày bắt đầu: [Chờ nhóm điền]
- **Mục tiêu Sprint (Sprint Goal):** Lõi chấm điểm — cài đặt module repository nạp dữ liệu, bộ lọc điều kiện bắt buộc, 5 hàm chuẩn hóa điểm theo Bảng 3.6, module quy đổi trọng số và 100% unit test cho các thành phần này.
- **Giả định công suất nhóm:** 10 Story Points *(10 Must)*.

---

## 1. Danh sách User Stories cam kết trong Sprint

| Mã US | Tên User Story | Điểm SP | Mức ưu tiên | Mục đề cương | Issue | Phụ trách | Trạng thái |
|:---|:---|:---:|:---:|:---|:---:|:---:|:---:|
| **US-09** | Xây dựng lớp truy xuất và nạp dữ liệu hồ sơ gia sư (Repository) | 2 | Must | Mục 3.5, Mục 4.2 | #11 | *[Chờ nhóm phân công]* | Chưa làm |
| **US-10** | Cài đặt module lọc điều kiện bắt buộc theo Bảng 3.2 | 2 | Must | Mục 2.3, 3.4, 3.6 (Bước 2), Bảng 3.2 | #12 | *[Chờ nhóm phân công]* | Chưa làm |
| **US-11** | Cài đặt 5 hàm chuẩn hóa điểm thành phần theo Bảng 3.6 | 3 | Must | Mục 3.6 (Bước 3), Bảng 3.6 | #13 | *[Chờ nhóm phân công]* | Chưa làm |
| **US-12** | Cài đặt module quy đổi mức ưu tiên sang trọng số theo Bảng 3.5 | 1 | Must | Mục 3.4, 3.6, Bảng 3.5 | #14 | *[Chờ nhóm phân công]* | Chưa làm |
| **US-13** | Bộ unit test toàn diện cho 5 hàm điểm và ca biên theo Bảng 3.6 | 2 | Must | Mục 3.6, Mục 5.1, Bảng 3.6 | #15 | *[Chờ nhóm phân công]* | Chưa làm |

- **Tổng điểm Story Points:** **10 SP** (10 Must).

---

## 2. Phân rã nhiệm vụ kỹ thuật (Tasks)

- **Phụ trách:** *[Chờ nhóm phân công]*
  - [ ] US-09: cấu hình tham số và đường dẫn dữ liệu; mô hình `TutorProfile`; repository đọc JSON/CSV; unit test repository.
  - [ ] US-10: hàm lọc theo môn, hình thức học và giao khung giờ; unit test các ca bắt buộc.
  - [ ] US-11 + US-13: 5 hàm điểm thành phần; 15 ca Bảng 3.6, ca biên Mục 5.1, kiểm thử đơn điệu và độ nhạy `delta`/`e_max`.
  - [ ] US-12: ánh xạ mức ưu tiên sang trọng số, loại tiêu chí không áp dụng, phát hiện tổng trọng số bằng 0; unit test.

Phạm vi Sprint 2 chưa gồm xếp hạng, ngưỡng dữ liệu, API và giao diện.

---

## 3. Rủi ro dự kiến và phương án xử lý

- *Rủi ro 1:* Đặc tả Bảng 3.6 chưa nói rõ trường hợp ngân sách bằng 0 (công thức chia cho `delta × B`). $\rightarrow$ *Phương án:* Áp dụng QĐ-A đã đề xuất (`B = 0`: học phí 0 điểm 1, học phí dương điểm 0) và ghi rõ trong PR để Product Owner xác nhận.
- *Rủi ro 2:* Issue #12 ghi tên tệp `filter.py`, trong khi skeleton thực tế là `filters.py`. $\rightarrow$ *Phương án:* Dùng `filters.py` theo skeleton hiện có, không tạo tệp song song; ghi rõ khác biệt trong PR và báo cáo Sprint.
- *Rủi ro 3:* Các module test còn lại (`test_eligibility`, `test_ranker`, `test_scenarios`, `test_recommend_api`) vẫn phải giữ `pytest.skip` để không vượt phạm vi. $\rightarrow$ *Phương án:* Chỉ bỏ skip ở `test_filters.py`, `test_criteria.py`, `test_weights.py`; kiểm tra lại danh sách skip sau mỗi PR.
