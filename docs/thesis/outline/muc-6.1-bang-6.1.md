> [!NOTE]
> **Đề xuất, nhóm xác nhận**

# Cập nhật Mục 6.1 (Kết quả đạt được) và Bảng 6.1 (Phân công thành viên) — Sprint 1 (US-32)

Tài liệu này lưu trữ nội dung hoàn thiện **Mục 6.1** (đối chiếu kết quả đạt được với 4 mục tiêu cụ thể tại Mục 1.4) và **Bảng 6.1** (phân công trách nhiệm của 3 thành viên tại Mục 6.3) trong đề cương đồ án *(trích từ bản dự thảo `ĐỀ CƯƠNG HỆ THỐNG KHUYẾN NGHỊ_DU-THAO_v3.docx` và đồng bộ với `docs/scrum/roles.md`)*.

---

## 1. Bốn mục tiêu cụ thể đặt ra tại Mục 1.4

1. **Mục tiêu (a) — Mô hình hóa mức độ phù hợp:** Phân loại tiêu chí (bắt buộc / ưu tiên / tùy chọn), xác định công thức điểm cho từng tiêu chí và xây dựng module lọc – tính điểm có trọng số.
2. **Mục tiêu (b) — Dịch vụ API khuyến nghị:** Xây dựng API gợi ý bằng FastAPI, nhận nhu cầu của người học và trả về danh sách gia sư đã xếp hạng kèm điểm thành phần.
3. **Mục tiêu (c) — Giao diện người dùng:** Xây dựng giao diện demo bằng ReactJS cho phép nhập nhu cầu, chọn mức ưu tiên và xem kết quả.
4. **Mục tiêu (d) — Đánh giá thực nghiệm:** Đánh giá chất lượng xếp hạng bằng các kịch bản tìm gia sư có kỳ vọng được xác định trước, đồng thời minh họa ảnh hưởng của việc thay đổi mức ưu tiên đến thứ hạng.

---

## 2. Nội dung hoàn thiện Mục 6.1 (Kết quả đạt được)

### 2.1. Khung đối chiếu theo tiến độ từng giai đoạn

| Mục tiêu cụ thể (Mục 1.4) | Trạng thái kết thúc Sprint 1 (Khóa thiết kế & Dữ liệu) | Lộ trình hoàn thiện toàn bộ đồ án (Sprint 2–6) |
|:---|:---|:---|
| **(a) Mô hình hóa mức độ phù hợp & module lọc – tính điểm** | Đã khóa bảng phân loại tiêu chí (Bảng 3.2), bảng trọng số (Bảng 3.5), 5 công thức điểm thành phần (Bảng 3.6) và bảng ngưỡng dữ liệu tối thiểu tại Mục 3.6 và `docs/design/scoring-spec.md` (PR #50). Đã thiết lập tham số cấu hình và Pydantic schema nền tảng (PR #52). | Cài đặt `repository.py`, `filters.py`, `criteria.py`, `weights.py` ở Sprint 2; cài đặt `eligibility.py` và `ranker.py` ở Sprint 3. |
| **(b) API gợi ý bằng FastAPI** | Đã khởi tạo môi trường Python 3.12 và ghim phiên bản phụ thuộc (PR #41), thiết lập CI GitHub Actions (PR #44), ban hành đặc tả hợp đồng `POST /api/recommend` tại `docs/design/api-contract.md` (PR #46). | Cài đặt endpoint `POST /api/recommend`, xử lý các trạng thái `success` / `no_match` / `zero_weight` / `422` và kiểm thử tích hợp bằng `TestClient` ở Sprint 4. |
| **(c) Giao diện demo bằng ReactJS** | Đã khởi tạo khung dự án frontend ReactJS bằng Vite trong thư mục `frontend/` (PR #45). | Xây dựng màn hình nhập nhu cầu `SearchPage` (CN01) ở Sprint 4; xây dựng màn hình kết quả `ResultPage` (CN02), thanh xếp chồng và đổi mức ưu tiên trực tiếp (CN03) ở Sprint 5. |
| **(d) Đánh giá chất lượng xếp hạng qua kịch bản thực nghiệm** | Đã chuẩn hóa 16 hồ sơ gia sư mẫu từ Phụ lục A sang `data/processed/tutors.{json,csv}` (PR #42, #48) và số hóa 14 kịch bản đánh giá Bảng 5.1 kèm Top-3 kỳ vọng sang `backend/tests/scenarios/scenarios.json` (PR #43, #49). | Chạy kiểm thử tự động 14 kịch bản và phân tích sai lệch ở Sprint 3; điền cột Top-3 hệ thống vào Bảng 5.1 ở Sprint 5; phân tích độ ổn định Mục 5.2 và tổng kết Chương 5–6 ở Sprint 6. |

### 2.2. Đoạn văn bản thảo trong Đề cương (Mục 6.1)

> Kết quả đạt được được đối chiếu lần lượt với bốn mục tiêu cụ thể ở mục 1.4: mô hình hóa mức độ phù hợp và module lọc – tính điểm (mục tiêu a), API gợi ý bằng FastAPI (mục tiêu b), giao diện demo bằng ReactJS (mục tiêu c), và đánh giá chất lượng xếp hạng cùng minh họa ảnh hưởng của mức ưu tiên (mục tiêu d).
>
> *(Dự thảo — chờ nhóm xác nhận và cập nhật cuốn chiếu theo từng Sprint)* Tính đến cuối Sprint 1, các kết quả đã thực sự hoàn thành: (a) công thức điểm thành phần và quy tắc xếp hạng đã được khóa tại Mục 3.6 và tài liệu `docs/design/scoring-spec.md`, module lọc - tính điểm được triển khai từ Sprint 2; (b) hợp đồng API `POST /api/recommend` đã được đặc tả tại `docs/design/api-contract.md`, endpoint được cài đặt ở Sprint 4; (c) khung dự án frontend ReactJS bằng Vite đã được khởi tạo, hai màn hình nghiệp vụ được xây dựng ở Sprint 4–5; (d) 16 hồ sơ gia sư và 14 kịch bản đánh giá kèm Top-3 kỳ vọng đã được số hóa và hợp nhất vào nhánh `main` (PR #42, #43, #48, #49). Các nội dung còn lại sẽ được cập nhật khi thực sự hoàn thành ở các Sprint tiếp theo.

---

## 3. Hoàn thiện Bảng 6.1 — Phân công thành viên (Mục 6.3)

| STT | Thành viên | Mã sinh viên | Công việc phụ trách | Mức độ hoàn thành |
|:---:|:---|:---:|:---|:---:|
| 1 | **Lê Thị Bích Chuyền** | KHMT2411037 | **Scrum Master các Sprint 2, 4, 6 kiêm Developer:** điều phối nghi thức Scrum ở các Sprint chẵn; phát triển giao diện ReactJS (Vite), kết nối API và kiểm thử trải nghiệm người dùng; tham gia thiết kế dữ liệu và kiểm thử hệ thống. | *[Điền cuối khóa luận]* |
| 2 | **Trần Nguyễn Đức** | KHMT2411011 | **Scrum Master các Sprint 1, 3, 5 kiêm Developer:** điều phối nghi thức Scrum ở các Sprint lẻ và phụ trách quản lý nhánh/PR trên GitHub; phát triển lõi chấm điểm backend FastAPI, thuật toán xếp hạng và kiểm thử tự động. | *[Điền cuối khóa luận]* |
| 3 | **Cao Khánh Ngọc** *(Nhóm trưởng)* | KHMT2411025 | **Product Owner kiêm Developer:** đại diện yêu cầu đề tài và làm việc với GVHD (TS. Lê Anh Nhã Uyên), quản lý và ưu tiên Product Backlog, nghiệm thu sản phẩm theo Definition of Done; tham gia phát triển tài liệu, thiết kế dữ liệu và kiểm thử. | *[Điền cuối khóa luận]* |
