# Hợp đồng giao diện lập trình ứng dụng (API Contract)

Tài liệu này đặc tả chi tiết giao diện RESTful API cho hệ thống gợi ý gia sư theo **Mục 4.4 (Xây dựng API gợi ý)** trong đề cương đồ án.

## 1. Tổng quan Endpoint

- **Mục tiêu:** Nhận nhu cầu của người học dạng JSON qua phương thức POST, gọi module tính điểm và trả về Top-$k$ gia sư kèm điểm tổng, điểm thành phần và đóng góp của từng tiêu chí.
- **URL:** `/api/recommend`
- **Method:** `POST`
- **Content-Type:** `application/json`

---

## 2. Cấu trúc Request Body (theo Bảng 3.4)

```json
{
  "subject": "Toán",
  "learning_mode": "in_person",
  "preferred_district": "KV1",
  "max_budget_vnd": 200000,
  "time_slots": ["T2-tối", "T4-tối", "T7-sáng"],
  "priorities": {
    "fee": "medium",
    "district": "medium",
    "experience": "medium",
    "rating": "medium",
    "availability": "medium"
  },
  "top_k": 3
}
```

### Chi tiết các trường:
- `subject` (string, bắt buộc): Môn học cần tìm gia sư.
- `learning_mode` (string, bắt buộc): `in_person` | `online` | `any`.
- `preferred_district` (string, tùy chọn): Khu vực mong muốn.
- `max_budget_vnd` (int, tùy chọn): Mức ngân sách tối đa/giờ.
- `time_slots` (array of strings, tùy chọn): Các khung thời gian mong muốn.
- `priorities` (object, tùy chọn, mặc định medium): Mức ưu tiên 5 tiêu chí (`none`, `low`, `medium`, `high`).
- `top_k` (int, tùy chọn, mặc định 3): Số lượng kết quả cần lấy.

---

## 3. Cấu trúc Response Body (Thành công - HTTP 200)

Các giá trị điểm trong ví dụ dưới đây được làm tròn tối đa 3 chữ số thập phân.

```json
{
  "status": "success",
  "total_candidates": 10,
  "qualified_candidates": 5,
  "results": [
    {
      "rank": 1,
      "tutor_id": "GS001",
      "total_score": 0.754,
      "criteria_scores": {
        "fee": 0.70,
        "district": 1.00,
        "experience": 0.50,
        "rating": 0.90,
        "availability": 0.67
      },
      "contributions": {
        "fee": 0.14,
        "district": 0.20,
        "experience": 0.10,
        "rating": 0.18,
        "availability": 0.134
      },
      "notes": []
    }
  ]
}
```

---

## 4. Các trường hợp phản hồi đặc biệt

### 4.1. Không có gia sư thỏa điều kiện bắt buộc
- **HTTP Status:** `200 OK`
- **Response:**
  ```json
  {
    "status": "no_match",
    "message": "Không có gia sư thỏa điều kiện bắt buộc",
    "results": []
  }
  ```

### 4.2. Tổng trọng số các tiêu chí bằng 0
- **HTTP Status:** `200 OK`
- **Response:**
  ```json
  {
    "status": "zero_weight",
    "message": "Vui lòng chọn mức ưu tiên cho ít nhất một tiêu chí để tiến hành xếp hạng",
    "unranked_candidates": ["GS001", "GS002"]
  }
  ```

### 4.3. Dữ liệu đầu vào không hợp lệ
- **HTTP Status:** `422 Unprocessable Entity`
- Trả về chi tiết lỗi chuẩn của FastAPI / Pydantic (ví dụ thiếu môn học, ngân sách âm...).
