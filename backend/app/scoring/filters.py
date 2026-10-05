"""Lọc danh sách gia sư theo các điều kiện bắt buộc (ràng buộc cứng).

Trách nhiệm:
- Hiện thực Bước 2 trong quy trình tính điểm mục 3.6
- Lọc theo điều kiện môn học: gia sư phải đảm nhận môn học được yêu cầu
- Lọc theo hình thức học: khớp hình thức Trực tiếp/Trực tuyến/Cả hai (theo Bảng 3.2)
- Lọc theo lịch rảnh: phải có ít nhất 1 khung giờ giao nhau (|L ∩ T| >= 1) nếu người học có nhập lịch rảnh

Mục tương ứng trong đề cương:
- Mục 3.6. Thiết kế thuật toán (Bước 2: Lọc điều kiện bắt buộc)
- Bảng 3.2. Phân loại tiêu chí
"""
