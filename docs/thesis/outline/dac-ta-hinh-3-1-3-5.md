# Đặc tả Hình 3.1–3.5 (Chương 3)

- **Trạng thái:** tài liệu làm việc, giữ lại sau khi xóa khối “Ghi chú biên tập” trong `chuong-03-phan-tich-thiet-ke.md`.
- **Nguồn:** khối ghi chú biên tập Chương 3 (bản `docs/chuong-1-3-hoan-thien`) và mục 6.3 của tài liệu rà soát `ra-soat-chuong-1-3.md` (nhánh `docs/ra-soat-chuong-1-3`).
- **Quyết định liên quan:** 9.3 (Hình 3.4/3.5 vẽ theo phạm vi Mục 3.8; giao diện thật thuộc Hình 4.1–4.4), 9.4 (module tính điểm không tự đọc dữ liệu).

## Hình 3.1 — Sơ đồ luồng xử lý khuyến nghị

Tám bước theo Mục 3.7.1; chèn bước kiểm tra ngưỡng dữ liệu tối thiểu (Bảng 3.7) sau bước (3). Ba nhánh thông báo:

- `no_match` — `recommend.py:60, 85`.
- `zero_weight` — `recommend.py:72`.
- Đầu vào không hợp lệ (422) — `SearchRequest`; thông báo `api.js:179`.
- Nhánh “thiếu dữ liệu” — `filter_eligible_candidates` (`eligibility.py:81`).

## Hình 3.2 — Kiến trúc hệ thống ba lớp

- **Giao diện ReactJS:** `App.jsx`, `SearchPage.jsx`, `ResultPage.jsx`, `services/api.js`.
- **API FastAPI:** `backend/app/api/recommend.py`, `POST /api/recommend`, `backend/app/schemas/`.
- **Module tính điểm:** `backend/app/scoring/` — module không tự đọc dữ liệu; `recommend.py` nạp dữ liệu qua `TutorRepository` (`backend/app/data/repository.py`) từ `data/processed/tutors.json`/`tutors.csv`.

## Hình 3.3 — Sơ đồ trình tự

`fetchRecommendations` (`api.js:152`) → `POST /api/recommend` (`api.js:155`) → `recommend_tutors` (`recommend.py:47`) → `TutorRepository.get_all()` (`repository.py:32`) → `compute_effective_weights` (`weights.py:52`) → `filter_mandatory` (`filters.py:34`) → `filter_eligible_candidates` (`eligibility.py:81`) → `score_and_rank` (`ranker.py:157`; gọi 5 hàm `criteria.py:21-65` và `build_reason`/`build_notes` — `ranker.py:125, 118`) → phản hồi. Nhánh CN03 lặp từ đầu (`requestSeqRef` — `App.jsx:52`).

## Hình 3.4 — Phác thảo màn hình nhập nhu cầu

Theo phạm vi Mục 3.8: biểu mẫu theo Bảng 3.4 (Môn học*, Hình thức học*, Khu vực mong muốn, Ngân sách tối đa/giờ kèm dòng quy đổi bằng chữ, Top-k, khung thời gian rảnh 7 ngày × 3 buổi) và khối mức ưu tiên 5 tiêu chí × 4 mức theo Bảng 3.5, kèm thông báo kiểm tra hợp lệ (`SearchPage.jsx:231, 241, 248`). Không đưa vào: banner hero, thanh 14 kịch bản, ô “Mục tiêu học tập” — thuộc Hình 4.1 của Chương 4.

## Hình 3.5 — Phác thảo màn hình kết quả

Theo phạm vi Mục 3.8: danh sách Top-k (`TutorCard`: hạng, điểm S(g), thanh xếp chồng C_i, “Lý do gợi ý”), rail CN03 5 hàng tiêu chí, trạng thái `no_match` (“Không tìm thấy gia sư thỏa mãn điều kiện” — `ResultPage.jsx:459`) và `zero_weight` (“Không thể xếp hạng do tổng trọng số bằng 0” — `:424`). Không đưa vào: dải KPI/phễu, chip độ trễ, huy hiệu đổi hạng, hộp “Nạp nhanh trọng số” — thuộc Hình 4.2–4.4 của Chương 4.
