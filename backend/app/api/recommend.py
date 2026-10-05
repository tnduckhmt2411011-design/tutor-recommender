"""Endpoint tiếp nhận yêu cầu tìm kiếm gia sư và trả về danh sách gợi ý.

Trách nhiệm:
- Endpoint POST /api/recommend nhận dữ liệu nhu cầu người học (Bảng 3.4)
- Gọi repository để lấy tập ứng viên, gọi luồng scoring thực thi 4 bước
- Trả về danh sách Top-k gia sư kèm điểm tổng và mức đóng góp tiêu chí
- Xử lý các tình huống biên: không có gia sư thỏa điều kiện, tổng trọng số bằng 0

Mục tương ứng trong đề cương:
- Mục 4.4. Xây dựng API gợi ý
"""
