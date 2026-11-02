> [!NOTE]
> **Đề xuất, nhóm xác nhận**

# Kế hoạch Sprint 4 (Sprint 4 Planning)

- **Thời gian thực hiện:** Hạn: 2026-12-04 (theo Milestone Sprint 4); ngày bắt đầu: [Chờ nhóm điền]
- **Mục tiêu Sprint (Sprint Goal):** API và màn hình nhập (E4 & E5) — hoàn thiện endpoint FastAPI `POST /api/recommend` tuân thủ chặt chẽ `docs/design/api-contract.md`, kiểm tra hợp lệ dữ liệu đầu vào (mã 422) và các trạng thái nghiệp vụ đặc biệt (`no_match`, `zero_weight`), cấu hình CORS và tài liệu OpenAPI/Swagger UI, viết bộ kiểm thử tích hợp với `TestClient`, đồng thời xây dựng dịch vụ gọi API (`frontend/src/services/api.js`) và màn hình nhập nhu cầu tìm kiếm `SearchPage` (CN01) trên ReactJS.
- **Giả định công suất nhóm:** 11 Story Points *(10 Must, 1 Should)*.

---

## 1. Danh sách User Stories cam kết trong Sprint

| Mã US | Tên User Story | Điểm SP | Mức ưu tiên | Mục đề cương | Issue | Phụ trách | Trạng thái |
|:---|:---|:---:|:---:|:---|:---:|:---:|:---:|
| **US-19** | Xây dựng endpoint khuyến nghị `POST /api/recommend` | 2 | Must | Mục 4.4, Bảng 3.4 | #21 | *[Chờ nhóm phân công]* | Chưa làm |
| **US-20** | Xử lý kiểm tra hợp lệ dữ liệu và các phản hồi nghiệp vụ đặc biệt (`422`, `no_match`, `zero_weight`) | 2 | Must | Mục 3.1, Mục 3.6, Mục 4.4 | #22 | *[Chờ nhóm phân công]* | Chưa làm |
| **US-21** | Viết bộ integration test cho API endpoint bằng `TestClient` | 2 | Must | Mục 4.4, Mục 5.1 | #23 | *[Chờ nhóm phân công]* | Chưa làm |
| **US-22** | Cấu hình CORS và tài liệu Swagger UI tự động (`/docs`) | 1 | Should | Mục 2.4, Mục 4.4 | #24 | *[Chờ nhóm phân công]* | Chưa làm |
| **US-23** | Xây dựng màn hình nhập nhu cầu và mức ưu tiên (`SearchPage` — CN01) | 3 | Must | Mục 3.2 (CN01), Mục 3.8 (Hình 3.4), Mục 4.5 | #25 | *[Chờ nhóm phân công]* | Chưa làm |
| **US-24** | Xây dựng module dịch vụ API phía frontend (`frontend/src/services/api.js`) | 1 | Must | Mục 4.5, Mục 4.6 | #26 | *[Chờ nhóm phân công]* | Chưa làm |

- **Tổng điểm Story Points:** **11 SP** (10 Must, 1 Should).

---

## 2. Phân rã nhiệm vụ kỹ thuật (Tasks)

- **Phụ trách:** *[Chờ nhóm phân công]*
  - [ ] US-19 (#21) + US-20 (#22) + US-22 (#24):
    - Bổ sung kiểm tra ràng buộc đầu vào trong `backend/app/schemas/search_request.py` theo `docs/design/api-contract.md` mục 2 và 4.3 (`subject` không rỗng, `max_budget_vnd >= 0` khi có nhập, `top_k: StrictInt` mặc định `3` trong khoảng `1 <= top_k <= 20`).
    - Định nghĩa các mô hình phản hồi (`RecommendationSuccessResponse`, `NoMatchResponse`, `ZeroWeightResponse`) trong `backend/app/schemas/recommendation.py` đúng theo `docs/design/api-contract.md` mục 3, 4 và 5.
    - Hiện thực router `POST /api/recommend` trong `backend/app/api/recommend.py` theo đúng thứ tự xử lý 5 bước tại mục 6 của `docs/design/api-contract.md` (bao gồm cả biến thể `no_match` ở mục 4.4 khi tất cả ứng viên qua lọc đều bị loại vì không đủ dữ liệu).
    - Khởi tạo ứng dụng FastAPI, cấu hình `CORSMiddleware` và metadata OpenAPI/Swagger UI trong `backend/app/main.py`.
  - [ ] US-21 (#23):
    - Gỡ `pytest.skip` và viết bộ integration test trong `backend/tests/api/test_recommend_api.py` dùng `fastapi.testclient.TestClient` kiểm thử các ca: `200 OK` (`success`), `200 OK` (`no_match` khi lọc rỗng và khi thiếu dữ liệu), `200 OK` (`zero_weight`), `422 Unprocessable Entity` (thiếu `subject`, `max_budget_vnd` âm, `top_k` ngoài `[1, 20]` hoặc không nguyên, enum không hợp lệ) và thời gian phản hồi `< 1s`.
  - [ ] US-24 (#26) + US-23 (#25):
    - Xây dựng `frontend/src/services/api.js` đọc `import.meta.env.VITE_API_URL` (mặc định `http://localhost:8000`) và hàm `fetchRecommendations(payload)`.
    - Xây dựng biểu mẫu nhập nhu cầu tìm kiếm và chọn 4 mức ưu tiên cho 5 tiêu chí trong `frontend/src/pages/SearchPage.jsx` (CN01, theo Hình 3.4 đề cương; tự động vô hiệu hóa/ẩn trường khu vực khi chọn hình thức `online`) và tích hợp vào `frontend/src/App.jsx`.

Phạm vi Sprint 4 chưa gồm màn hình hiển thị kết quả chi tiết `ResultPage` (CN02), biểu đồ thanh xếp chồng và tương tác cập nhật ưu tiên tức thì (CN03) — các hạng mục này thuộc Sprint 5.

---

## 3. Rủi ro dự kiến và phương án xử lý

- *Rủi ro 1:* Thứ tự kiểm tra giữa `zero_weight` và ngưỡng dữ liệu (`insufficient_data_candidates`) có thể gây lệch mã phản hồi nếu đặt sai bước. $\rightarrow$ *Phương án:* Tuân thủ nghiêm ngặt thứ tự 5 bước tại Mục 6 của `docs/design/api-contract.md`: (1) Validate đầu vào (`422`) $\rightarrow$ (2) Lọc bắt buộc (`no_match` nếu rỗng) $\rightarrow$ (3) Kiểm tra tổng trọng số (`zero_weight` kèm `unranked_candidates` nếu $\sum w_i = 0$) $\rightarrow$ (4) Áp ngưỡng dữ liệu (`no_match` kèm `insufficient_data_candidates` nếu không còn ai) $\rightarrow$ (5) Tính điểm và trả `success`.
- *Rủi ro 2:* Kiểu `int` mặc định của Pydantic v2 có thể tự ép kiểu số thực hoặc chuỗi số (ví dụ `top_k = 3.5` hoặc `"3"`), trong khi `api-contract.md` mục 4.3 yêu cầu `top_k` không phải số nguyên phải trả `422`. $\rightarrow$ *Phương án:* Kiểm tra chặt kiểu số nguyên cho `top_k` (loại trừ `bool` và `float`) và miền giá trị `1 <= top_k <= 20`.
- *Rủi ro 3:* Lỗi chặn CORS hoặc lệch tên trường JSON khi kết nối từ ReactJS (Vite) sang FastAPI. $\rightarrow$ *Phương án:* Cấu hình `CORSMiddleware` trong `backend/app/main.py` và đối chiếu toàn bộ khóa payload trong `frontend/src/services/api.js` với `SearchRequest` của `docs/design/api-contract.md`.
