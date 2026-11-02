> [!NOTE]
> **Đề xuất, nhóm xác nhận**

# Rút kinh nghiệm Sprint 3 (Sprint 3 Retrospective)

- **Ngày họp:** *[Chờ nhóm điền]*
- **Người điều phối:** Scrum Master (Trần Nguyễn Đức)
- **Thành viên tham gia:** *[Chờ nhóm điền]*

---

## 1. Dữ kiện lịch sử repo làm cơ sở thảo luận

- **Tiến độ so với Milestone:** Hạn Milestone của Sprint 3 là `2026-11-20`. Toàn bộ các PR của Sprint 3 (#62–#66) đã được triển khai, vượt qua CI và hợp nhất vào `main` trong ngày `2026-11-02` (sớm hơn 18 ngày lịch so với hạn Milestone).
- **Đồng bộ tên tệp giữa Issue và skeleton mã nguồn:** Phần To-do trong Issue #16 ghi `backend/app/scoring/threshold.py` và Issue #19 ghi `backend/tests/test_scenarios_runner.py`, trong khi skeleton sẵn có của repo là `backend/app/scoring/eligibility.py` (kèm `tests/unit/test_eligibility.py`) và `backend/tests/scenarios/test_scenarios.py`. Nhóm đã triển khai trực tiếp vào đúng các tệp skeleton (đồng thời tạo alias `check_data_threshold = check_tutor_eligibility` trong `eligibility.py`) để gỡ `pytest.skip` đúng lộ trình và không sinh tệp trùng lặp.
- **Đối chiếu thực nghiệm 14 kịch bản Bảng 5.1:** Kết quả chạy tự động trên 16 hồ sơ chuẩn hóa khớp 100% với `expected_top3` ở cả 14/14 kịch bản. Quá trình đối chiếu phát hiện rõ nguyên nhân khác biệt chữ số thập phân ở `KB04` (phép tính tay trong đề cương lược bỏ tiêu chí `availability` dù truy vấn có `time_slots`) và `KB09` (`0,9275` làm tròn theo chuẩn IEEE-754 so với làm tròn nửa lên), giúp hoàn thiện tư liệu cho Mục 5.2 của báo cáo khóa luận mà không cần can thiệp vào dữ liệu kỳ vọng đã khóa.
- **Phối hợp nhánh kiểm thử tích hợp kịch bản:** Nhánh `test/19-kiem-thu-14-kich-ban` (PR #66) tích hợp các commit của PR #63 (`eligibility.py`) và PR #64 (`ranker.py`) để chạy kiểm thử đầu-cuối toàn bộ 14 kịch bản ngay trên GitHub Actions trước khi hợp nhất tuần tự vào `main`.

---

## 2. Những điểm đã làm tốt (What went well?)
- *[Chờ nhóm điền trong buổi họp Retro]*

---

## 3. Những điểm cần cải thiện (What could be improved?)
- *[Chờ nhóm điền trong buổi họp Retro]*

---

## 4. Hành động cải tiến cho Sprint 4 (Action Items)
- *[Chờ nhóm điền trong buổi họp Retro]*
