# CHƯƠNG 2. CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ

> [!NOTE]
> **Đề xuất, nhóm xác nhận**

Chương này trình bày cơ sở lý thuyết của cách tiếp cận “khuyến nghị đa tiêu chí” đã chọn ở mục 1.3.2: vị trí bài toán trong ba nhóm phương pháp khuyến nghị (2.1), cách biểu diễn dựa trên đặc trưng hồ sơ (2.2), cơ chế lọc điều kiện bắt buộc và Weighted Scoring (2.3), và các công nghệ triển khai (2.4).

---

## 2.1. Hệ thống khuyến nghị

Hệ thống khuyến nghị (recommender system) là lớp bài toán dự đoán mức độ phù hợp giữa một người dùng và một tập các đối tượng (sản phẩm, công việc, nội dung...), từ đó xếp hạng và gợi ý những đối tượng phù hợp nhất. Ba nhóm phương pháp phổ biến là Content-Based Filtering (dựa trên đặc trưng của đối tượng), Collaborative Filtering (dựa trên hành vi của nhiều người dùng) và Hybrid (kết hợp cả hai). Bảng 2.1 so sánh ba nhóm theo các tiêu chí liên quan trực tiếp đến bài toán tìm gia sư.

**Bảng 2.1 - So sánh ba nhóm phương pháp trong hệ thống khuyến nghị**

| Tiêu chí | Content-Based Filtering | Collaborative Filtering | Hybrid |
|:---|:---|:---|:---|
| Dữ liệu cần có | Đặc trưng hồ sơ (môn dạy, khu vực, học phí...) | Lịch sử tương tác của nhiều người dùng (rating, số buổi học) | Cả hai loại dữ liệu trên |
| Vấn đề cold-start | Ít bị ảnh hưởng - chỉ cần hồ sơ mới có đủ đặc trưng | Bị ảnh hưởng nặng khi hệ thống, người dùng hoặc gia sư mới chưa có lịch sử | Giảm nhẹ, nhưng vẫn cần một lượng dữ liệu tương tác tối thiểu |
| Độ phức tạp triển khai | Thấp - so khớp đặc trưng hồ sơ với nhu cầu | Trung bình đến cao - cần ma trận tương tác và mô hình học từ dữ liệu | Cao - phải kết hợp và cân bằng hai mô hình con |
| Phù hợp với hệ thống mới vận hành? | Phù hợp - không cần dữ liệu tích lũy | Không phù hợp - chưa có dữ liệu tương tác | Chỉ phù hợp một phần |

*Nguồn: tổng hợp của nhóm từ đặc điểm ba nhóm phương pháp khuyến nghị.*

Bảng 2.1 cho thấy Content-Based Filtering là nhóm phù hợp nhất với một hệ thống mới vận hành: hàng “Phù hợp với hệ thống mới vận hành?” ghi rõ nhóm này không cần dữ liệu tích lũy, trong khi Collaborative Filtering không phù hợp khi chưa có dữ liệu tương tác. Bài toán tìm gia sư có cùng bản chất với các bài toán ghép nối như gợi ý việc làm phù hợp với hồ sơ ứng viên: đều là ghép một “nhu cầu” (tiêu chí của người tìm) với một tập “đối tượng có đặc trưng” (hồ sơ gia sư, tin tuyển dụng) sao cho mức độ phù hợp là cao nhất.

## 2.2. Khuyến nghị dựa trên đặc trưng hồ sơ

Trong Content-Based Recommendation, mỗi đối tượng được biểu diễn bằng các đặc trưng, sau đó được so khớp với hồ sơ sở thích hoặc nhu cầu của người dùng; đối tượng có mức so khớp cao được xếp trước. Trong đồ án này, đối tượng là gia sư, được biểu diễn qua các đặc trưng: môn dạy, khu vực, học phí theo giờ, số năm kinh nghiệm, hình thức dạy, lịch rảnh và điểm đánh giá trung bình. “Hồ sơ nhu cầu” của người học không lấy từ lịch sử mà do người học nhập trực tiếp tại thời điểm tìm kiếm.

Các đặc trưng trên có bản chất khác nhau: môn học là so khớp tập hợp, học phí là đại lượng số có ngưỡng ngân sách, lịch rảnh là giao của hai tập khung giờ, hình thức dạy là danh mục. Vì chưa có một không gian đặc trưng thống nhất cho tất cả, đồ án không ép toàn bộ vào một vector để tính cosine similarity. Thay vào đó, mỗi tiêu chí được xử lý bằng một hàm điểm riêng (mục 3.6). Cosine similarity là kỹ thuật phù hợp khi hồ sơ và nhu cầu được biểu diễn thành vector số (ví dụ vector từ mô tả văn bản của gia sư); kỹ thuật này không được dùng trong đồ án và chỉ được nhắc như một hướng mở rộng. Về tên gọi, đề tài không gọi phương pháp là Content-Based Filtering thuần túy; cụm từ “dựa trên đặc trưng hồ sơ” chỉ mô tả loại dữ liệu đầu vào của hệ thống.

## 2.3. Lọc theo điều kiện bắt buộc và Weighted Scoring

Hệ thống xử lý hai loại điều kiện theo hai cách khác nhau. Điều kiện bắt buộc được kiểm tra trước như ràng buộc lọc: gia sư không thỏa thì bị loại, không được xếp hạng dù các điểm khác cao. Trên tập gia sư còn lại, các tiêu chí ưu tiên được chuyển thành điểm thành phần trong khoảng [0, 1] rồi gộp bằng Weighted Scoring:

S(g) = Σ ( w_i × s_i(g) ) ÷ Σ w_i  (2.1)

trong đó s_i(g) ∈ [0, 1] là điểm của gia sư g theo tiêu chí i, w_i ≥ 0 là trọng số của tiêu chí i, và phép tổng chỉ lấy trên các tiêu chí đang được áp dụng (tiêu chí có w_i > 0 và có dữ liệu đầu vào; quy tắc chi tiết ở mục 3.6). Weighted Scoring là phép tổng có bù trừ: điểm cao ở tiêu chí này có thể bù cho điểm thấp ở tiêu chí khác. Đó là lý do các điều kiện “không thể bù” như đúng môn học phải được lọc trước thay vì đưa vào điểm tổng.

Bảng 2.2 minh họa ảnh hưởng của trọng số bằng một ví dụ số đơn giản với ba gia sư giả định và ba tiêu chí. Đây là ví dụ lý thuyết, không phải dữ liệu thực của hệ thống; dữ liệu thực được dùng ở mục 5.

**Bảng 2.2 - Ví dụ minh họa ảnh hưởng của mức ưu tiên đến thứ hạng**

| Gia sư | Điểm học phí | Điểm khu vực | Điểm đánh giá | Tổng điểm - bộ 1 | Hạng | Tổng điểm - bộ 2 | Hạng |
|:---|---:|---:|---:|---:|:---:|---:|:---:|
| A | 1,00 | 0,00 | 0,80 | 0,76 | 1 | 0,36 | 3 |
| B | 0,60 | 1,00 | 0,90 | 0,74 | 2 | 0,90 | 1 |
| C | 0,40 | 1,00 | 1,00 | 0,64 | 3 | 0,88 | 2 |

*Nguồn: ví dụ số do nhóm lập để minh họa (không phải dữ liệu thực của hệ thống).*

Bộ 1 ưu tiên học phí (trọng số học phí : khu vực : đánh giá = 3 : 1 : 1); bộ 2 ưu tiên khu vực (1 : 3 : 1). Ví dụ với gia sư A ở bộ 1: S = (3×1,00 + 1×0,00 + 1×0,80) ÷ 5 = 0,76. Gia sư A xếp thứ nhất khi ưu tiên học phí nhưng xuống thứ ba khi ưu tiên khu vực, cho thấy thứ hạng phụ thuộc trực tiếp vào trọng số. Vì trọng số phản ánh ưu tiên của từng người học, không tồn tại một bộ trọng số “đúng” cho mọi nhu cầu; bộ mặc định của hệ thống chỉ là giá trị khởi tạo để demo (mục 3.5).

## 2.4. Công nghệ sử dụng

Công nghệ trong đồ án là công cụ triển khai, không phải nội dung nghiên cứu chính. Backend dùng FastAPI [1] (Python) vì cú pháp khai báo kiểu dữ liệu rõ ràng giúp kiểm tra hợp lệ tiêu chí đầu vào và khả năng tự sinh tài liệu API (Swagger UI) giúp kiểm thử endpoint mà chưa cần giao diện. Frontend dùng ReactJS [2] để xây dựng giao diện demo tối giản gồm biểu mẫu nhập nhu cầu và danh sách kết quả tự xếp lại khi mức ưu tiên thay đổi. Dữ liệu gia sư mẫu lưu dạng JSON và CSV, đủ dùng cho quy mô vài chục đến vài trăm bản ghi; phương án SQLite là hướng mở rộng, chưa hiện thực trong đồ án.

---

**[GHI CHÚ BIÊN TẬP — XÓA TRƯỚC KHI GHÉP WORD]**

- **Câu cần trích dẫn học thuật (7 câu, nguồn để nhóm tìm và kiểm chứng):** (1) mục 2.1 — định nghĩa hệ thống khuyến nghị; (2) mục 2.1 — phân loại ba nhóm phương pháp; (3) mục 2.1 sau Bảng 2.1 — tương đồng với bài toán ghép nối (gợi ý việc làm); (4) mục 2.2 — định nghĩa Content-Based Recommendation; (5) mục 2.2 — phạm vi áp dụng cosine similarity; (6) mục 2.3 — tính chất “phép tổng có bù trừ” của Weighted Scoring; (7) mục 2.3 sau Bảng 2.2 — tính chủ quan của bộ trọng số.
- **Câu bổ sung so với đề cương:** câu mở đầu đoạn sau Bảng 2.1 (“Bảng 2.1 cho thấy…”) — dẫn chiếu trực tiếp bảng theo chuẩn report_standards Mục 4.2; nội dung suy ra trực tiếp từ hàng “Phù hợp với hệ thống mới vận hành?” của chính bảng.
- **Sửa so với đề cương (ý không đổi):** bỏ liên từ đầu câu “Do đó,” ở mục 2.2, thay bằng “Về tên gọi,” (quyết định j); bỏ từ “tối ưu” — “một bộ trọng số 'đúng' hay tối ưu khách quan” → “một bộ trọng số 'đúng' cho mọi nhu cầu”; công thức S(g) đánh số (2.1) theo chuẩn trình bày (report_standards Mục 4.3); mục 2.4 nêu SQLite là hướng mở rộng chưa hiện thực (quyết định 9.2); công thức giữ dạng chữ thuần (không dùng LaTeX) để dán vào Word không vỡ định dạng.
