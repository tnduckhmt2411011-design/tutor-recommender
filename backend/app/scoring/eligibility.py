"""Quy tắc kiểm tra điều kiện đủ dữ liệu để được xếp hạng.

Trách nhiệm:
- Đếm số tiêu chí ưu tiên mà gia sư có dữ liệu trong số n tiêu chí đang áp dụng (không tính tiêu chí Đánh giá vì luôn dùng giá trị trung tính 0.5)
- So sánh với bảng ngưỡng dữ liệu tối thiểu:
  + n = 1: ngưỡng 1
  + n = 2: ngưỡng 2
  + n = 3: ngưỡng 2
  + n = 4: ngưỡng 3
  + n = 5: ngưỡng 4
- Đánh dấu loại gia sư không đủ dữ liệu kèm ghi chú 'Không đủ dữ liệu để xếp hạng'

Mục tương ứng trong đề cương:
- Mục 3.6. Thiết kế thuật toán (Điều kiện đủ dữ liệu để được xếp hạng)
- Bảng ngưỡng dữ liệu tối thiểu để được xếp hạng
"""
