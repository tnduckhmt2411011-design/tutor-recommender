"""Chuyển đổi mức độ ưu tiên của người học thành trọng số tính toán.

Trách nhiệm:
- Ánh xạ mức ưu tiên sang trọng số w_i theo Bảng 3.5:
  + Không quan tâm: 0
  + Thấp: 1
  + Trung bình (mặc định): 2
  + Cao: 3
- Xử lý loại trừ tiêu chí không áp dụng (ví dụ học Trực tuyến không tính tiêu chí khu vực)
- Kiểm tra điều kiện tổng trọng số bằng 0 (sum(w_i) == 0)

Mục tương ứng trong đề cương:
- Mục 3.6. Thiết kế thuật toán (Bảng 3.5 và Các trường hợp đặc biệt)
"""
