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
- `top_k` (int, tùy chọn, mặc định 3): Số lượng kết quả cần lấy, thỏa mãn `1 ≤ top_k ≤ 20` (trần top_k = 20). Nếu `top_k` lớn hơn số gia sư đã xếp hạng được, trả về tất cả kết quả đã xếp hạng, không báo lỗi. Giá trị ngoài khoảng hoặc không phải số nguyên → 422 (mục 4.3).

---

## 3. Cấu trúc Response Body (Thành công - HTTP 200)

Các giá trị điểm trong các ví dụ dưới đây được hiển thị với 3 chữ số thập phân; phép tính dùng phân số chính xác và chỉ làm tròn khi hiển thị, không làm tròn trung gian.

```json
{
  "status": "success",
  "total_candidates": 10,
  "qualified_candidates": 5,
  "insufficient_data_candidates": [],
  "results": [
    {
      "rank": 1,
      "tutor_id": "GS001",
      "total_score": 0.753,
      "criteria_scores": {
        "fee": 0.700,
        "district": 1.000,
        "experience": 0.500,
        "rating": 0.900,
        "availability": 0.667
      },
      "contributions": {
        "fee": 0.140,
        "district": 0.200,
        "experience": 0.100,
        "rating": 0.180,
        "availability": 0.133
      },
      "reason": "Khu vực khớp, đánh giá 4,5/5, học phí vượt ngân sách 15%",
      "notes": []
    }
  ]
}
```

**Ví dụ 2 (người học chọn Trực tuyến):** người học chọn `learning_mode` = `online`, có nhập ngân sách và khung giờ mong muốn, không nhập khu vực; `priorities` để mặc định `medium`. Các tiêu chí đang áp dụng là `fee`, `experience`, `rating`, `availability` (mỗi tiêu chí $w = 2$, tổng $w = 8$); tiêu chí `district` không áp dụng nên có giá trị `null`; gia sư chưa có đánh giá nên `rating` = 0,5 kèm ghi chú.

```json
{
  "status": "success",
  "total_candidates": 10,
  "qualified_candidates": 4,
  "insufficient_data_candidates": [],
  "results": [
    {
      "rank": 1,
      "tutor_id": "GS002",
      "total_score": 0.750,
      "criteria_scores": {
        "fee": 1.000,
        "district": null,
        "experience": 0.500,
        "rating": 0.500,
        "availability": 1.000
      },
      "contributions": {
        "fee": 0.250,
        "district": null,
        "experience": 0.125,
        "rating": 0.125,
        "availability": 0.250
      },
      "reason": "Học phí trong ngân sách, lịch rảnh khớp toàn bộ khung giờ mong muốn",
      "notes": ["chưa có đánh giá"]
    }
  ]
}
```
Mã gia sư trong các ví dụ (GS001, GS002) chỉ để minh họa; mã thật theo data/processed/tutors.json.

---

## 4. Các trường hợp phản hồi đặc biệt

### 4.1. Không có gia sư thỏa điều kiện bắt buộc
- **HTTP Status:** `200 OK`
- **Response:**
  ```json
  {
    "status": "no_match",
    "message": "Không có gia sư thỏa điều kiện bắt buộc",
    "results": [],
    "insufficient_data_candidates": []
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
- Các lỗi trả về 422, ví dụ: thiếu `subject`; `max_budget_vnd` âm; `top_k` không phải số nguyên hoặc ngoài khoảng `1 ≤ top_k ≤ 20`; `learning_mode` có giá trị ngoài enum (`in_person`, `online`, `any`); giá trị tiêu chí trong `priorities` ngoài enum (`none`, `low`, `medium`, `high`).
- Trả về chi tiết lỗi chuẩn của FastAPI / Pydantic.

### 4.4. Biến thể của `no_match`: có gia sư qua lọc nhưng tất cả bị loại vì thiếu dữ liệu

Khi có gia sư qua lọc bắt buộc nhưng tất cả bị loại vì không đủ dữ liệu theo ngưỡng (scoring-spec mục 3), hệ thống vẫn trả `no_match` (không thêm giá trị `status` mới) với `insufficient_data_candidates` không rỗng:

```json
{
  "status": "no_match",
  "message": "Có gia sư thỏa điều kiện bắt buộc nhưng không đủ dữ liệu để xếp hạng",
  "results": [],
  "insufficient_data_candidates": ["GS001", "GS002"]
}
```

---

## 5. Mô tả các trường phản hồi

### 5.1. Bảng mô tả trường

| Trường | Kiểu | Bắt buộc | Ý nghĩa |
|---|---|---|---|
| `status` | string | Có | Trạng thái xử lý: `success`, `no_match` hoặc `zero_weight`. |
| `message` | string | Không | Thông báo cho người học; chỉ xuất hiện ở `no_match` và `zero_weight`. |
| `total_candidates` | int | Có | Tổng số hồ sơ gia sư trong kho dữ liệu. |
| `qualified_candidates` | int | Có | Số gia sư qua lọc bắt buộc (Bảng 3.2), đếm trước khi áp ngưỡng dữ liệu (scoring-spec mục 3). |
| `insufficient_data_candidates` | array of string | Có | Mảng `tutor_id` của gia sư đã qua lọc bắt buộc nhưng bị loại vì không đủ dữ liệu theo ngưỡng (scoring-spec mục 3); là `[]` khi không có. Luôn có trong response `success` và `no_match`. |
| `results` | array of object | Có | Danh sách gia sư đã xếp hạng, tối đa `top_k` phần tử; rỗng khi không có kết quả. |
| `unranked_candidates` | array of string | Chỉ trong `zero_weight` | Danh sách gia sư thỏa điều kiện bắt buộc nhưng không thể xếp hạng do tổng trọng số bằng 0. |
| `results[].rank` | int | Có | Hạng của gia sư trong kết quả, liên tục từ 1 đến số kết quả; đồng điểm sắp theo `tutor_id` tăng dần (scoring-spec mục 5). |
| `results[].tutor_id` | string | Có | Mã định danh gia sư. |
| `results[].total_score` | number | Có | Điểm tổng hợp $S$ theo công thức Weighted Scoring (scoring-spec mục 5). |
| `results[].criteria_scores` | object | Có | Điểm thành phần $s_i \in [0, 1]$ của từng tiêu chí (scoring-spec mục 4); luôn đủ 5 khóa, xem quy ước ở mục 5.2. |
| `results[].contributions` | object | Có | Tỷ lệ đóng góp của từng tiêu chí $C_i = w_i \times s_i \div \sum w_i$ (scoring-spec mục 5); luôn đủ 5 khóa, xem quy ước ở mục 5.2. |
| `results[].reason` | string | Có | Lý do gợi ý tiếng Việt, không rỗng; tất định (cùng đầu vào cho cùng chuỗi) và chỉ dùng dữ liệu đã tính (`criteria_scores`, `contributions`, dữ liệu đầu vào). Contract không quy định mẫu câu cụ thể (thuộc Issue #18, Sprint 3). |
| `results[].notes` | array of string | Có | Cảnh báo về dữ liệu, ví dụ `"chưa có đánh giá"`; có thể rỗng; không chứa lý do gợi ý. |

### 5.2. Quy ước về giá trị

- `criteria_scores` và `contributions` luôn đủ 5 khóa: `fee`, `district`, `experience`, `rating`, `availability`. Tiêu chí không áp dụng hoặc có mức ưu tiên `none` ($w = 0$) có giá trị `null`; khi đó thanh xếp chồng ở frontend bỏ qua khóa `null`.
- Tiêu chí không áp dụng: `fee` khi không nhập `max_budget_vnd`; `district` khi học `online` hoặc không nhập `preferred_district`; `availability` khi không nhập `time_slots`.
- Gia sư chưa có đánh giá: `rating` = 0,5 (không phải `null`) kèm `notes` `"chưa có đánh giá"`.
- `rank` liên tục từ 1 đến số kết quả; gia sư đồng điểm sắp theo `tutor_id` tăng dần (scoring-spec mục 5).
- Làm tròn chỉ khi hiển thị (3 chữ số thập phân); phép sắp xếp và so đồng điểm dùng giá trị chưa làm tròn.
- `total_candidates` là tổng số hồ sơ trong kho dữ liệu; `qualified_candidates` là số gia sư qua lọc bắt buộc, tính trước khi áp ngưỡng dữ liệu (scoring-spec mục 3).

---

## 6. Thứ tự xử lý

Hệ thống xử lý một truy vấn theo trình tự sau:

1. **Kiểm tra đầu vào:** đầu vào vi phạm ràng buộc (mục 4.3) → trả `422`.
2. **Lọc bắt buộc theo Bảng 3.2** (scoring-spec mục 2): không còn gia sư nào qua lọc → trả `no_match` (mục 4.1).
3. **Kiểm tra tổng trọng số:** tổng trọng số các tiêu chí đang áp dụng bằng 0 → trả `zero_weight` kèm `unranked_candidates` (mục 4.2).
4. **Áp ngưỡng đủ dữ liệu** (scoring-spec mục 3): gia sư đã qua lọc nhưng không đủ dữ liệu bị loại khỏi xếp hạng và ghi vào `insufficient_data_candidates`; nếu mọi gia sư qua lọc đều bị loại → trả biến thể `no_match` ở mục 4.4.
5. **Tính điểm, xếp hạng, lấy Top-k:** tính điểm theo scoring-spec mục 4–5, sắp xếp giảm dần theo $S$ (đồng điểm thì theo `tutor_id` tăng dần), trả tối đa `top_k` kết quả.
