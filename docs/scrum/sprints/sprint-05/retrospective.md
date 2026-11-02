> [!NOTE]
> **Đề xuất, nhóm xác nhận**

# Rút kinh nghiệm Sprint 5 (Sprint 5 Retrospective)

- **Ngày họp:** *[Chờ nhóm điền]*
- **Người điều phối:** Scrum Master (Trần Nguyễn Đức)
- **Thành viên tham gia:** *[Chờ nhóm điền]*

---

## 1. Dữ kiện lịch sử repo làm cơ sở thảo luận

- **Tiến độ so với Milestone:** Hạn Milestone của Sprint 5 là `2026-12-18`. Toàn bộ các PR của Sprint 5 (#70–#73) đã được triển khai, vượt qua CI và hợp nhất vào `main` trong ngày `2026-11-02` (sớm hơn 46 ngày lịch so với hạn Milestone), hoàn tất **Cổng chất lượng 3 (Quality Gate 3)**.
- **Bảo toàn bất biến Hợp đồng API (`docs/design/api-contract.md`) khi hiển thị thẻ gia sư theo Hình 3.5:** Do phản hồi của `POST /api/recommend` theo hợp đồng chỉ trả về `tutor_id`, `full_name`, điểm số và lời giải thích, tầng giao diện đã tách danh mục tra cứu tĩnh `frontend/src/data/tutorsCatalog.js` (đồng bộ từ 16 hồ sơ chuẩn hóa `data/processed/tutors.json`) để hiển thị đầy đủ môn dạy, khu vực, hình thức, học phí, năm kinh nghiệm và điểm đánh giá trên `TutorCard.jsx` mà không phải thay đổi cấu trúc response của backend.
- **Tương tác trực tiếp CN03 và nạp nhanh 14 kịch bản thực nghiệm (`KB01`–`KB14`):** Bảng điều khiển mức ưu tiên trực tiếp trên `ResultPage.jsx` sử dụng bộ đếm `requestId` để chống chồng lấn khi người học đổi mức ưu tiên liên tiếp, đồng thời đo và hiển thị trực tiếp độ trễ phản hồi (`ms`) cùng huy hiệu thay đổi thứ hạng (`rankDeltas`). Bộ chọn nhanh 14 kịch bản tại `frontend/src/data/scenariosCatalog.js` giúp tái hiện tức thì mọi kịch bản trong Bảng 5.1 ngay trên giao diện web.
- **Hoàn thiện kiểm thử ca biên Mục 5.1 và bảng kết quả Bảng 5.1:** Việc bổ sung `backend/tests/api/test_boundary_muc_5_1.py` (6 bài kiểm thử tích hợp sâu cho các điểm biên, tính đơn điệu và luồng CN03) nâng tổng số bài kiểm thử tự động của backend lên **`190 passed, 0 skipped`** (độ bao phủ `96%`), làm cơ sở dữ liệu thực nghiệm vững chắc để điền đầy đủ cột **"Top-3 hệ thống"** của **Bảng 5.1** tại `docs/thesis/report/muc-5.1-bang-5.1-ket-qua.md`.

---

## 2. Những điểm đã làm tốt (What went well?)
- *[Chờ nhóm điền trong buổi họp Retro]*

---

## 3. Những điểm cần cải thiện (What could be improved?)
- *[Chờ nhóm điền trong buổi họp Retro]*

---

## 4. Hành động cải tiến cho Sprint 6 (Action Items)
- *[Chờ nhóm điền trong buổi họp Retro]*
