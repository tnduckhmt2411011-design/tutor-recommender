> [!NOTE]
> **Đề xuất, nhóm xác nhận**

# Rút kinh nghiệm Sprint 4 (Sprint 4 Retrospective)

- **Ngày họp:** *[Chờ nhóm điền]*
- **Người điều phối:** Scrum Master (Trần Nguyễn Đức)
- **Thành viên tham gia:** *[Chờ nhóm điền]*

---

## 1. Dữ kiện lịch sử repo làm cơ sở thảo luận

- **Tiến độ so với Milestone:** Hạn Milestone của Sprint 4 là `2026-12-04`. Toàn bộ các PR của Sprint 4 (#67–#69) đã được triển khai, vượt qua CI và hợp nhất vào `main` trong ngày `2026-11-02` (sớm hơn 32 ngày lịch so với hạn Milestone).
- **Hoàn tất gỡ bỏ toàn bộ `pytest.skip` trong bộ kiểm thử backend:** Sau khi hợp nhất PR #68 (`b13cb19`), tệp kiểm thử cuối cùng còn giữ `pytest.skip` từ giai đoạn dựng khung (`backend/tests/api/test_recommend_api.py`) đã được thay thế bằng 35 bài kiểm thử tích hợp thực tế, nâng tổng số bài kiểm thử tự động của backend lên `184 passed, 0 skipped` với độ bao phủ `96%`.
- **Tuân thủ nghiêm ngặt thứ tự xử lý 5 bước của Hợp đồng API:** Việc cài đặt `POST /api/recommend` bám sát Mục 6 của `docs/design/api-contract.md` giúp phân biệt chính xác 2 biến thể `no_match` (không có ứng viên qua lọc cứng so với có ứng viên qua lọc cứng nhưng bị loại ở bước ngưỡng dữ liệu tối thiểu kèm `insufficient_data_candidates`) và trạng thái `zero_weight` (trả về danh sách `unranked_candidates` khi cả 5 mức ưu tiên đều là `none`).
- **Tổ chức mã nguồn Frontend theo quy tắc linter `oxlint`:** Cấu hình `.oxlintrc.json` bật quy tắc `react/only-export-components`, đòi hỏi các tệp `.jsx` chỉ xuất component React; các hằng số danh mục và hàm chuẩn hóa payload được tách riêng sang tầng dịch vụ (`frontend/src/services/api.js`), giúp mã nguồn sạch lỗi lint ngay từ lần kiểm tra đầu tiên.

---

## 2. Những điểm đã làm tốt (What went well?)
- *[Chờ nhóm điền trong buổi họp Retro]*

---

## 3. Những điểm cần cải thiện (What could be improved?)
- *[Chờ nhóm điền trong buổi họp Retro]*

---

## 4. Hành động cải tiến cho Sprint 5 (Action Items)
- *[Chờ nhóm điền trong buổi họp Retro]*
