# Backend - Dịch vụ gợi ý gia sư đa tiêu chí (FastAPI)

Dịch vụ backend phục vụ tính toán mức độ phù hợp đa tiêu chí theo phương pháp Weighted Scoring và cung cấp API RESTful cho hệ thống gợi ý gia sư.

## 1. Công nghệ chính

- **Ngôn ngữ:** Python 3.12 (đã kiểm chứng với Python 3.12.7)
- **Framework API:** FastAPI 0.162.0
- **Kiểm thực dữ liệu:** Pydantic 2.14.2
- **Máy chủ ASGI:** Uvicorn 0.54.0
- **Kiểm thử tự động:** Pytest 9.2.0, Pytest-cov 7.1.0, HTTPX 0.28.1
- **Kiểm tra chất lượng mã nguồn:** Ruff 0.17.3

## 2. Cấu trúc thư mục thực tế

```text
backend/
├── app/
│   ├── api/                  # Khai báo các API router và endpoint
│   │   ├── __init__.py
│   │   └── recommend.py      # Endpoint POST /api/recommend tiếp nhận tìm kiếm và xếp hạng
│   ├── core/                 # Cấu hình hệ thống và tham số thuật toán
│   │   ├── __init__.py
│   │   └── config.py         # Tham số delta, E_max, điểm trung tính, bảng quy đổi w_i
│   ├── data/                 # Tầng truy xuất dữ liệu gia sư
│   │   ├── __init__.py
│   │   └── repository.py     # Quản lý và nạp 16 hồ sơ gia sư từ data/processed/tutors.json
│   ├── schemas/              # Định nghĩa Pydantic models (kiểm thực chặt chẽ extra="forbid")
│   │   ├── __init__.py
│   │   ├── recommendation.py # Schema kết quả: RankedTutor, Success, NoMatch, ZeroWeight
│   │   ├── search_request.py # Schema yêu cầu: SearchRequest (7 trường)
│   │   └── tutor.py          # Schema hồ sơ gia sư: TutorProfile (9 trường)
│   ├── scoring/              # Module thuật toán lọc và tính điểm độc lập
│   │   ├── __init__.py
│   │   ├── criteria.py       # 5 hàm tính điểm thành phần s_i in [0, 1] theo Bảng 3.6
│   │   ├── eligibility.py    # Kiểm tra ngưỡng dữ liệu tối thiểu theo n tiêu chí
│   │   ├── filters.py        # Lọc ràng buộc cứng bắt buộc theo Bảng 3.2
│   │   ├── ranker.py         # Tổng hợp điểm Weighted Scoring, phá hòa tất định theo tutor_id
│   │   └── weights.py        # Tính trọng số hiệu dụng w_i theo mức ưu tiên
│   ├── __init__.py
│   └── main.py               # Khởi tạo FastAPI app, cấu hình CORS và route GET /health
├── tests/
│   ├── api/                  # Kiểm thử tích hợp API endpoints và các ca biên (41 test)
│   │   ├── test_boundary_muc_5_1.py  # Kiểm thử ca biên toán học và tính đơn điệu
│   │   └── test_recommend_api.py     # Kiểm thử hợp đồng API POST /api/recommend
│   ├── scenarios/            # Kiểm thử kịch bản thực nghiệm và độ nhạy (27 test)
│   │   ├── README.md
│   │   ├── scenarios.json            # 14 kịch bản thực nghiệm kèm Top-3 kỳ vọng
│   │   ├── test_scenarios.py         # Kiểm thử tự động khớp 14/14 kịch bản
│   │   └── test_sensitivity_muc_5_2.py # Khảo sát độ nhạy tham số và mức ưu tiên
│   ├── unit/                 # Kiểm thử đơn vị cho từng thành phần thuật toán (129 test)
│   │   ├── test_config.py
│   │   ├── test_criteria.py
│   │   ├── test_eligibility.py
│   │   ├── test_filters.py
│   │   ├── test_ranker.py
│   │   ├── test_repository.py
│   │   └── test_weights.py
│   └── test_environment.py   # Kiểm tra môi trường Python và thư viện (3 test)
├── pytest.ini                # Cấu hình pytest (testpaths = tests)
├── requirements.txt          # Dependencies chính cho ứng dụng runtime
└── requirements-dev.txt      # Dependencies cho môi trường phát triển và kiểm thử
```

## 3. Cài đặt và cấu hình môi trường

Yêu cầu môi trường: Python 3.12 (đã kiểm chứng với phiên bản 3.12.7). Đứng tại thư mục `backend/`:

### Trên Windows PowerShell (môi trường nhóm kiểm chứng):
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt -r requirements-dev.txt
```

### Trên macOS / Linux (chưa kiểm chứng trên macOS/Linux):
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt
```

## 4. Khởi chạy máy chủ phát triển (Uvicorn)

Khởi động máy chủ backend tại cổng 8000 (chế độ tự động tải lại khi đổi code):

```powershell
python -m uvicorn app.main:app --port 8000 --reload
```

- Địa chỉ dịch vụ: `http://localhost:8000`
- Kiểm tra trạng thái sức khỏe: `http://localhost:8000/health` (trả về `{"status":"ok"}`)
- Tài liệu tương tác OpenAPI (Swagger UI): `http://localhost:8000/docs`

## 5. Danh mục Endpoints & Ví dụ gọi API

### 5.1. `GET /health`
Kiểm tra tính sẵn sàng của backend.

### 5.2. `POST /api/recommend`
Tiếp nhận nhu cầu tìm kiếm của người học và trả về danh sách gợi ý gia sư đã xếp hạng.

#### Ví dụ gọi qua PowerShell (`Invoke-RestMethod`):
```powershell
$payload = @{
    subject = "Toán"
    learning_mode = "in_person"
    preferred_district = "Bình Thạnh"
    max_budget_vnd = 200000
    priorities = @{
        fee = "medium"
        district = "medium"
        experience = "medium"
        rating = "medium"
        availability = "medium"
    }
    top_k = 3
} | ConvertTo-Json -Depth 5

$response = Invoke-RestMethod -Uri "http://localhost:8000/api/recommend" -Method Post -ContentType "application/json; charset=utf-8" -Body $payload
$response.results | ForEach-Object {
    Write-Host "Hạng $($_.rank): $($_.tutor_id) - Điểm tổng: $($_.total_score) ($($_.reason))"
}
```

#### Ví dụ gọi qua `curl` (Bash):
```bash
curl -X POST "http://localhost:8000/api/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Toán",
    "learning_mode": "in_person",
    "preferred_district": "Bình Thạnh",
    "max_budget_vnd": 200000,
    "priorities": {
      "fee": "medium",
      "district": "medium",
      "experience": "medium",
      "rating": "medium",
      "availability": "medium"
    },
    "top_k": 3
  }'
```

#### Kết quả trả về kỳ vọng (Kịch bản KB01):
```json
{
  "status": "success",
  "total_eligible": 3,
  "returned_count": 3,
  "results": [
    {
      "rank": 1,
      "tutor_id": "GS-G01",
      "total_score": 0.9375,
      "component_scores": {"fee": 1.0, "district": 1.0, "experience": 0.75, "rating": 1.0, "availability": 0.0},
      "weighted_contributions": {"fee": 0.25, "district": 0.25, "experience": 0.1875, "rating": 0.25, "availability": 0.0},
      "reason": "Phù hợp rất cao về học phí, khu vực và đánh giá",
      "notes": []
    },
    {
      "rank": 2,
      "tutor_id": "GS-G10",
      "total_score": 0.745,
      "component_scores": {"fee": 1.0, "district": 0.0, "experience": 1.0, "rating": 0.98, "availability": 0.0},
      "weighted_contributions": {"fee": 0.25, "district": 0.0, "experience": 0.25, "rating": 0.245, "availability": 0.0},
      "reason": "Phù hợp rất cao về học phí và kinh nghiệm",
      "notes": []
    },
    {
      "rank": 3,
      "tutor_id": "GS-T06",
      "total_score": 0.625,
      "component_scores": {"fee": 0.0, "district": 1.0, "experience": 1.0, "rating": 0.5, "availability": 0.0},
      "weighted_contributions": {"fee": 0.0, "district": 0.25, "experience": 0.25, "rating": 0.125, "availability": 0.0},
      "reason": "Phù hợp rất cao về khu vực và kinh nghiệm",
      "notes": ["Điểm đánh giá đang dùng giá trị trung tính 0,5"]
    }
  ],
  "insufficient_data_candidates": []
}
```

## 6. Kiểm thử tự động & Kiểm tra chất lượng

Từ thư mục `backend/` và khi virtual environment đã kích hoạt:

```powershell
# 1. Kiểm tra linter bằng Ruff
ruff check .

# 2. Chạy toàn bộ 200 bài kiểm thử
python -m pytest -q

# 3. Đo độ bao phủ mã nguồn của app
python -m pytest --cov=app --cov-report=term-missing
```

### Kết quả chuẩn:
- `ruff check .`: `All checks passed!`
- `pytest`: **200 passed** (132 unit & môi trường, 27 kịch bản & độ nhạy, 41 API & ca biên).
- `coverage`: **340/351 câu lệnh được phủ (97%)** (11 câu lệnh chưa phủ nằm ở nhánh ngoại lệ phòng thủ).
