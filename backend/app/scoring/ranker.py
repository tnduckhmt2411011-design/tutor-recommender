"""Tổng hợp điểm bằng Weighted Scoring, xếp hạng và trích xuất Top-k gia sư.

Trách nhiệm:
- Hiện thực Bước 4 trong quy trình tính điểm mục 3.6
- Tính điểm tổng hợp: S = sum(w_i * s_i) / sum(w_i)
- Tính mức đóng góp từng tiêu chí: w_i * s_i / sum(w_i)
- Sắp xếp giảm dần theo S; trường hợp đồng điểm sắp xếp theo mã gia sư (tutor_id) để kết quả ổn định
- Trích xuất Top-k kết quả phù hợp nhất

Mục tương ứng trong đề cương:
- Mục 3.6. Thiết kế thuật toán (Bước 4: Tổng hợp và xếp hạng)
- Mục 4.3. Cài đặt module tính điểm
"""
