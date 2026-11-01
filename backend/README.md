# Backend - Hệ thống gợi ý gia sư

Dịch vụ backend phục vụ tính toán mức độ phù hợp đa tiêu chí và cung cấp API RESTful cho hệ thống gợi ý gia sư.

## 1. Công nghệ chính

- **Framework:** FastAPI
- **Validation:** Pydantic
- **Máy chủ ASGI:** Uvicorn
- **Kiểm thử:** Pytest

## 2. Cấu trúc thư mục

```text
backend/
├── app/
│   ├── api/          # Khai báo các API routes (Mục 4.4)
│   ├── core/         # Cấu hình hệ thống và tham số thuật toán (Mục 3.6)
│   ├── data/         # Tầng truy xuất dữ liệu gia sư từ JSON/CSV/SQLite (Mục 3.5)
│   ├── schemas/      # Định nghĩa Pydantic models (Bảng 3.3, 3.4)
│   └── scoring/      # Thuật toán tính điểm và xếp hạng độc lập (Mục 3.6, 4.3)
├── tests/
│   ├── api/          # Kiểm thử tích hợp API endpoints
│   ├── scenarios/    # Kiểm thử bộ kịch bản đánh giá Top-3 (Mục 5.2)
│   └── unit/         # Kiểm thử đơn vị cho từng thành phần thuật toán (Mục 5.1)
├── pytest.ini        # Cấu hình chạy kiểm thử
├── requirements.txt  # Dependencies chính cho ứng dụng
└── requirements-dev.txt # Dependencies cho môi trường phát triển và kiểm thử
```

## 3. Cài đặt và chạy

Yêu cầu: Python 3.12 (đã kiểm tra với Python 3.12.7) và đã đứng tại thư mục `backend/`.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-dev.txt
```

Kiểm tra chất lượng mã nguồn và chạy kiểm thử:

```powershell
.\.venv\Scripts\ruff.exe check .
.\.venv\Scripts\python.exe -m pytest -q
```

Ở Sprint 1, các module kiểm thử nghiệp vụ trong `tests/unit/`, `tests/api/` và `tests/scenarios/` vẫn ở trạng thái `pytest.skip`; chỉ có `tests/test_environment.py` kiểm tra phiên bản Python và khả năng import thư viện. Các bài kiểm thử nghiệp vụ sẽ được triển khai từ Sprint 2.
