"""Quản lý các biến môi trường và thiết lập tham số khởi tạo cho thuật toán tính điểm.

Trách nhiệm:
- Khởi tạo tham số thuật toán: delta = 0.5 (ngưỡng vượt học phí), E_max = 8 (kinh nghiệm trần), rating_default = 0.5 (giá trị đánh giá trung tính)
- Trọng số mặc định của các mức ưu tiên: none=0, low=1, medium=2, high=3 (Bảng 3.5)
- Đường dẫn lưu trữ dữ liệu (tệp JSON, CSV hoặc cơ sở dữ liệu SQLite)

Mục tương ứng trong đề cương:
- Mục 3.6. Thiết kế thuật toán (Cơ sở của các tham số)
- Bảng 3.5. Quy đổi mức ưu tiên sang trọng số
"""
