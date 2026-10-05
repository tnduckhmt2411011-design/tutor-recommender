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

Sẽ cập nhật ở Sprint 1 khi bắt đầu thiết lập môi trường ảo và cài đặt thư viện thật.
