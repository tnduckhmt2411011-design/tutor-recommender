# Kịch bản kiểm thử thực nghiệm gợi ý Top-3

Thư mục này chứa tập kịch bản thực nghiệm dùng để đánh giá độ chính xác và tính hợp lý của thuật toán gợi ý theo mục 5.2 của đề cương.

## 1. Cấu trúc một kịch bản trong `scenarios.json`

Mỗi kịch bản được định nghĩa dưới dạng một đối tượng JSON với các trường sau:

```json
{
  "id": "SCENARIO_01",
  "request": {
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
    }
  },
  "expected_top3": ["GS001", "GS005", "GS003"],
  "lý do": "GS001 thỏa mãn toàn bộ tiêu chí với điểm cao, GS005 học phí vừa phải và giao 2/3 lịch, GS003 kinh nghiệm tốt.",
  "ghi chú": "Kịch bản kiểm tra trường hợp các tiêu chí có cùng mức ưu tiên."
}
```

`expected_top3` và `expected_raw` của 14 kịch bản KB01–KB14 trong `scenarios.json` được **khóa bất biến** kể từ khi nhóm chốt: không chỉnh sửa để làm khớp với kết quả hệ thống.

## 2. Quy tắc bắt buộc khi đánh giá thực nghiệm

- **Chốt trước khi chạy:** Danh sách `expected_top3` và lý do kỳ vọng phải được các thành viên nhóm thảo luận, phân tích dữ liệu và **chốt cố định TRƯỚC KHI chạy hệ thống**.
- **Không sửa kỳ vọng để làm đẹp kết quả:** Tuyệt đối không được chỉnh sửa `expected_top3` để khớp với kết quả thực tế mà thuật toán đưa ra.
- **Xử lý khi kết quả bị lệch:** Nếu kết quả thực tế khác với kỳ vọng:
  1. Ghi nhận chi tiết độ lệch vào biên bản/báo cáo thực nghiệm (mục 5.2).
  2. Điều tra nguyên nhân: do phân tích chủ quan ban đầu chưa tính hết tương tác đa tiêu chí, hay do trọng số / hàm điểm chưa phản ánh đúng mong muốn thực tế.
  3. Báo cáo trung thực trong khóa luận tốt nghiệp.
