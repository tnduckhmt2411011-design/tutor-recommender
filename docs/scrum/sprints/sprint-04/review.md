> [!NOTE]
> **Đề xuất, nhóm xác nhận**

# Sơ kết Sprint 4 (Sprint 4 Review)

- **Ngày họp:** *[Chờ nhóm điền]*
- **Người chủ trì:** Scrum Master (Trần Nguyễn Đức)
- **Thành phần tham dự:** *[Chờ nhóm điền]*

---

## 1. Kết quả thực hiện mục tiêu Sprint

- **Mục tiêu đặt ra:** API và màn hình nhập (Epic E4 & E5) — hoàn thiện endpoint FastAPI `POST /api/recommend` tuân thủ chặt chẽ `docs/design/api-contract.md`, kiểm tra hợp lệ dữ liệu đầu vào (mã `422`) và các trạng thái nghiệp vụ đặc biệt (`no_match`, `zero_weight`), cấu hình CORS và tài liệu OpenAPI/Swagger UI (`/docs`), viết bộ kiểm thử tích hợp với `TestClient`, đồng thời xây dựng dịch vụ gọi API (`frontend/src/services/api.js`) và màn hình nhập nhu cầu tìm kiếm `SearchPage` (CN01) trên ReactJS.
- **Đánh giá mức độ hoàn thành:** *[Đạt / Chưa đạt]*

---

## 2. Rà soát chi tiết User Stories

| Mã US | Tên User Story | Điểm SP | Trạng thái | Ghi chú nghiệm thu |
|:---|:---|:---:|:---:|:---|
| US-19 | Xây dựng endpoint khuyến nghị `POST /api/recommend` | 2 | Xong (PR #68) | Cài đặt tại `backend/app/api/recommend.py` theo đúng thứ tự xử lý 5 bước tại Mục 6 của `docs/design/api-contract.md`; thời gian phản hồi thực tế qua `TestClient` đạt `~4–20 ms` (`< 1000 ms`) |
| US-20 | Xử lý kiểm tra hợp lệ dữ liệu và các phản hồi nghiệp vụ đặc biệt (`422`, `no_match`, `zero_weight`) | 2 | Xong (PR #68) | Ràng buộc Pydantic v2 tại `search_request.py` và các mô hình phản hồi (`RecommendationSuccessResponse`, `NoMatchResponse`, `ZeroWeightResponse`) tại `recommendation.py` |
| US-21 | Viết bộ integration test cho API endpoint bằng `TestClient` | 2 | Xong (PR #68) | 35 bài kiểm thử tích hợp tại `backend/tests/api/test_recommend_api.py` (bao phủ `200 success`, `200 no_match`, `200 zero_weight`, `422 Unprocessable Entity`, 14 kịch bản `KB01`–`KB14` qua HTTP và hiệu năng `< 1s`) |
| US-22 | Cấu hình CORS và tài liệu Swagger UI tự động (`/docs`) | 1 | Xong (PR #68) | Cấu hình `CORSMiddleware` và metadata OpenAPI/Swagger UI tại `backend/app/main.py` |
| US-23 | Xây dựng màn hình nhập nhu cầu và mức ưu tiên (`SearchPage` — CN01) | 3 | Xong (PR #69) | Giao diện `frontend/src/pages/SearchPage.jsx`, `App.jsx`, `App.css`, `index.html` theo Hình 3.4 đề cương (tự động khóa trường khu vực khi chọn `online`) |
| US-24 | Xây dựng module dịch vụ API phía frontend (`frontend/src/services/api.js`) | 1 | Xong (PR #69) | Hàm `fetchRecommendations(payload)` đọc `import.meta.env.VITE_API_URL` (mặc định `http://localhost:8000`) và chuẩn hóa payload gửi `POST /api/recommend` |

*Ghi chú về các PR đã merge trong Sprint 4 (đều do `tnduckhmt2411011-design` thực hiện):*
- **Biên bản Sprint 3 & kế hoạch Sprint 4:** PR #67 (`docs/sprint-03-review-sprint-04-planning`, merge `bdc8b3f`, 2026-11-02).
- **US-19 (#21) + US-20 (#22) + US-21 (#23) + US-22 (#24):** PR #68 (`feat/21-22-23-24-api-recommend`, merge `b13cb19`, 2026-11-02).
- **US-23 (#25) + US-24 (#26):** PR #69 (`feat/25-26-giao-dien-tim-kiem`, merge `9e043fe`, 2026-11-02).

---

## 3. Kết quả kiểm thử nghiệm thu kỹ thuật

- [x] **Backend (`backend/`):** `ruff check .` chạy sạch (`All checks passed!`); `pytest -v -rs` đạt **`184 passed, 0 skipped`** (toàn bộ unit test, scenario test và API integration test đều xanh).
- [x] **Độ bao phủ mã nguồn (`pytest-cov`):** Toàn bộ `backend/app/` đạt **96%** (`351/367` dòng lệnh), trong đó `app/api/recommend.py`, `app/main.py`, `app/schemas/search_request.py` và `app/schemas/recommendation.py` đều đạt **100%**.
- [x] **Hiệu năng phản hồi API:** Thời gian xử lý `POST /api/recommend` trên 14 kịch bản thực nghiệm (`KB01`–`KB14`) đạt trung bình `4,75 ms` (lớn nhất `5,95 ms` sau khởi tạo, lần gọi đầu tiên `19,34 ms`), thấp hơn rất nhiều so với ngưỡng yêu cầu phi chức năng `< 1000 ms`.
- [x] **Frontend (`frontend/`):** `npm run lint` (`oxlint`) đạt `Found 0 warnings and 0 errors`; `npm run build` (`vite build`) biên dịch thành công (`dist/` sinh sạch trong `~224 ms`).
- **Kết luận:** *[Đủ điều kiện chuyển sang Sprint 5 / Cần bổ sung]*
