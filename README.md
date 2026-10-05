# Hệ thống khuyến nghị gia sư dựa trên mức độ phù hợp đa tiêu chí

Repository mã nguồn và tài liệu của đồ án tốt nghiệp đại học về hệ thống gợi ý gia sư đa tiêu chí.

## 1. Thông tin nhóm thực hiện

- Lê Thị Bích Chuyền
- Trần Nguyễn Đức
- Cao Khánh Ngọc

## 2. Công nghệ sử dụng

- **Backend:** FastAPI, Pydantic, Uvicorn
- **Frontend:** ReactJS (Vite)
- **Lưu trữ dữ liệu:** JSON, CSV, SQLite
- **Kiểm thử & chất lượng:** Pytest, Ruff

## 3. Bản đồ cấu trúc thư mục và ánh xạ đề cương

| Thư mục / Tệp tin | Vai trò kỹ thuật | Mục tương ứng trong đề cương |
|---|---|---|
| `backend/app/scoring/` | Module tính điểm đa tiêu chí độc lập (lọc, trọng số, chuẩn hóa) | Mục 3.6, Mục 4.3 |
| `backend/app/schemas/` | Lược đồ dữ liệu hồ sơ gia sư và nhu cầu người học | Mục 3.5 (Bảng 3.3, 3.4) |
| `backend/app/api/` | Endpoint FastAPI tiếp nhận yêu cầu và trả về Top-k | Mục 4.4 |
| `backend/tests/` | Kiểm thử đơn vị, ca biên và kịch bản thực nghiệm | Mục 5.1, Mục 5.2 |
| `frontend/` | Giao diện ReactJS (nhập nhu cầu và hiển thị kết quả) | Mục 3.8, Mục 4.5 |
| `data/` | Dữ liệu mẫu thu thập và giả lập (ẩn danh) | Mục 3.5 |
| `docs/design/` | Từ điển dữ liệu, đặc tả thuật toán và hợp đồng API | Chương 3, Chương 4 |
| `docs/scrum/` | Tài liệu quản lý dự án theo khung Scrum | Kế hoạch thực hiện đồ án |
| `docs/thesis/` | Bản thảo đề cương, báo cáo, slides đồ án | Báo cáo đồ án |
| `docs/decisions/` | Hồ sơ ghi nhận quyết định kiến trúc (ADR) | Thiết kế hệ thống |

## 4. Cách chạy hệ thống

Sẽ cập nhật ở Sprint 1.
