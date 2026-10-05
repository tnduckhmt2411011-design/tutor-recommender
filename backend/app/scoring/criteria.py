"""Hàm tính điểm chuẩn hóa từng tiêu chí ưu tiên (s_i in [0, 1]).

Trách nhiệm:
- Hiện thực Bước 3 trong quy trình tính điểm mục 3.6
- Tính điểm học phí: s = 1 nếu P <= B, s = max(0, 1 - (P - B) / (delta * B)) nếu P > B (với delta = 0.5)
- Tính điểm khu vực: s = 1 nếu khu vực thuộc danh sách dạy, ngược lại s = 0 (bỏ qua nếu học trực tuyến)
- Tính điểm kinh nghiệm: s = min(E / E_max, 1) với E_max = 8
- Tính điểm đánh giá: s = R / 5; giá trị trung tính 0.5 nếu chưa có đánh giá
- Tính điểm lịch rảnh: s = |L ∩ T| / |L| (tỷ lệ khung giờ giao nhau)

Mục tương ứng trong đề cương:
- Mục 3.6. Thiết kế thuật toán (Bước 3: Tính điểm thành phần)
- Bảng 3.6. Công thức điểm thành phần
"""
