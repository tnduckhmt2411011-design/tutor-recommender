# Đặc tả Hình 3.1–3.5 (Chương 3)

- **Trạng thái:** đã chuẩn hóa và đồng bộ 4 hình `3.1, 3.2, 3.3, 3.5` bằng tệp nguồn `.drawio` (`docs/thesis/figures/src/`) qua toolchain `DayuanJiang/next-ai-draw-io` (draw.io v32.0.2).
- **Quyết định liên quan:** 9.3 (Hình 3.4/3.5 vẽ theo phạm vi Mục 3.8; giao diện thật thuộc Hình 4.1–4.4), 9.4 (module tính điểm thuần Python, không phụ thuộc FastAPI và không tự đọc dữ liệu).

## Hình 3.1 — Sơ đồ luồng xử lý khuyến nghị (ISO 5807)

- **Nguồn:** `docs/thesis/figures/src/hinh-3-1-luong-xu-ly-khuyen-nghi.drawio` → `docs/thesis/figures/hinh-3-1-luong-xu-ly-khuyen-nghi.png`.
- Tám bước theo Mục 3.7.1 khớp `recommend.py:47-106`, sử dụng ký hiệu chuẩn ISO 5807 (bầu dục bắt đầu/kết thúc, bình hành nhập/xuất, chữ nhật xử lý, hình thoi rẽ nhánh có nhãn `Có`/`Không`):
  - `SearchRequest` không hợp lệ → `HTTP 422 Unprocessable Entity` → `Kết thúc`.
  - Lọc bắt buộc hết ứng viên → `no_match` (biến thể 1) → `Kết thúc`.
  - Tổng trọng số $\sum w_i = 0$ (`compute_effective_weights`) → `zero_weight` → nhánh quyết định `Điều chỉnh mức ưu tiên (CN03)?`.
  - Kiểm tra ngưỡng dữ liệu tối thiểu (Bảng 3.7 — `filter_eligible_candidates`) hết ứng viên → `no_match` (biến thể 2) → `Kết thúc`.
  - Hiển thị Top-$k$ (CN02) → quyết định `Điều chỉnh mức ưu tiên (CN03)?` (`Có` → quay lại Bước 2; `Không` → `Kết thúc`).

## Hình 3.2 — Kiến trúc hệ thống ba lớp

- **Nguồn:** `docs/thesis/figures/src/hinh-3-2-kien-truc-ba-lop.drawio` → `docs/thesis/figures/hinh-3-2-kien-truc-ba-lop.png`.
- **Lớp giao diện (ReactJS — `frontend/src/`):** `App.jsx`, `SearchPage.jsx`, `ResultPage.jsx` & `components/` (`TutorCard`, `StackedBarScore`), `services/api.js`.
- **Lớp dịch vụ API (FastAPI — `backend/app/`):** `main.py` (`CORSMiddleware`, `GET /health`, `/docs`), `api/recommend.py` (`POST /api/recommend`, điều phối 5 bước).
- **Lớp nghiệp vụ (`backend/app/scoring/`):** `filters.py` → `weights.py` → `eligibility.py` → `criteria.py` → `ranker.py` (thuần Python, không `import` FastAPI, không tự đọc tệp).
- **Khối dùng chung (`Shared Core`):** `core/config.py` và `schemas/` (được cả API, `TutorRepository` và `scoring/` dùng chung).
- **Truy xuất & lưu trữ:** `TutorRepository` (`data/repository.py`) nạp `data/processed/tutors.json` lúc chạy; tách biệt ghi chú `tutors.csv` + `scripts/validate_tutors.py` dùng đối chiếu kiểm định ngoại tuyến.

## Hình 3.3 — Sơ đồ trình tự xử lý yêu cầu khuyến nghị (UML 2.5)

- **Nguồn:** `docs/thesis/figures/src/hinh-3-3-so-do-trinh-tu.drawio` → `docs/thesis/figures/hinh-3-3-so-do-trinh-tu.png`.
- Khung `sd Xử lý yêu cầu khuyến nghị gia sư`, 5 đối tượng (`Người học` UML Actor, `:ReactUI`, `:RecommendAPI`, `:TutorRepository`, `:ScoringModule`), đầy đủ Activation Bars (kể cả thanh lồng cho self-call), mũi tên đồng bộ nét liền đầu đặc và mũi tên trả về nét đứt đầu mở, khung `loop` ngoài cho CN03 và 4 khung `alt` lồng nhau đúng thứ tự `recommend.py`:
  - `1:` `Người học` → `:ReactUI` → `2:` `POST /api/recommend` → `3:` Xác thực Pydantic (`alt`: `3a: HTTP 422`).
  - `4–5:` `TutorRepository.get_all()` → `all_tutors (16 TutorProfile)`.
  - `6–7:` `filter_mandatory(all_tutors, request)` → `qualified` (`alt`: `7a: no_match`).
  - `8–9:` `compute_effective_weights(request)` → `effective_weights` (`alt`: `9a: zero_weight`).
  - `10–11:` `filter_eligible_candidates(qualified, effective_weights)` → `(eligible, insufficient_ids)` (`alt`: `11a: no_match`).
  - `12–15:` `score_and_rank(eligible, request, effective_weights, top_k)` (self-call `13: 5 hàm criteria.py + build_reason() + build_notes()`) → `14: ranked_results` → `15: HTTP 200 (success)` → `16: Hiển thị kết quả (CN02)`.

## Hình 3.4 — Phác thảo màn hình nhập nhu cầu

Theo phạm vi Mục 3.8: biểu mẫu theo Bảng 3.4 (Môn học*, Hình thức học*, Khu vực mong muốn, Ngân sách tối đa/giờ kèm dòng quy đổi bằng chữ, Top-$k$, khung thời gian rảnh 7 ngày × 3 buổi) và khối mức ưu tiên 5 tiêu chí × 4 mức theo Bảng 3.5, kèm thông báo kiểm tra hợp lệ (`SearchPage.jsx:231, 241, 248`). Không đưa vào: banner hero, thanh 14 kịch bản, ô “Mục tiêu học tập” — thuộc Hình 4.1 của Chương 4.

## Hình 3.5 — Phác thảo màn hình kết quả

- **Nguồn:** `docs/thesis/figures/src/hinh-3-5-phac-thao-ket-qua.drawio` → `docs/thesis/figures/hinh-3-5-phac-thao-ket-qua.png`.
- Minh họa nhất quán theo công thức (2.1) và Bảng 3.5–3.6 với mọi tiêu chí ở mức Trung bình ($w_i = 2$, $\sum w_i = 10$, $|L| = 4$ buổi): `GS-01` ($S = 0{,}88$), `GS-02` ($S = 0{,}73$), `GS-03` ($S = 0{,}68$); thanh xếp chồng vẽ tỉ lệ trên nền `1,00`, lý do gợi ý theo đúng `ranker.py:build_reason`; rail phải CN03 có đủ tiêu đề 4 cột (`Bỏ qua (0)`, `Thấp (1)`, `TB (2)`, `Cao (3)`) và hai trạng thái biên `no_match`, `zero_weight`.
