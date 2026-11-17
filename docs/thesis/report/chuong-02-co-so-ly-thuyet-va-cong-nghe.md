# CHƯƠNG 2. CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ

Chương này trình bày cơ sở lý thuyết của cách tiếp cận khuyến nghị đa tiêu chí đã chọn ở Mục 1.3.2. Nội dung lần lượt làm rõ vị trí bài toán trong ba nhóm phương pháp khuyến nghị (Mục 2.1), phương pháp Content-Based Filtering trên đặc trưng hồ sơ có cấu trúc (Mục 2.2), cơ chế lọc điều kiện bắt buộc và Weighted Scoring (Mục 2.3), cùng các công nghệ triển khai (Mục 2.4).

---

## 2.1. Hệ thống khuyến nghị

Hệ thống khuyến nghị (*recommender system*) là lớp bài toán ước lượng mức độ hữu ích của một đối tượng đối với một người dùng, từ đó xếp hạng và khuyến nghị những đối tượng phù hợp nhất [2]. Ba nhóm phương pháp phổ biến gồm Content-Based Filtering (dựa trên đặc trưng của đối tượng), Collaborative Filtering (dựa trên hành vi của nhiều người dùng) và Hybrid (kết hợp cả hai) [2]. Bảng 2.1 so sánh ba nhóm theo các tiêu chí liên quan trực tiếp đến bài toán tìm gia sư.

**Bảng 2.1 - So sánh ba nhóm phương pháp trong hệ thống khuyến nghị**

| Tiêu chí | Content-Based Filtering | Collaborative Filtering | Hybrid |
|:---|:---|:---|:---|
| Dữ liệu cần có | Đặc trưng hồ sơ (môn dạy, khu vực, học phí, v.v.) | Lịch sử tương tác của nhiều người dùng (rating, số buổi học) | Cả hai loại dữ liệu trên |
| Vấn đề cold-start | Ít bị ảnh hưởng: chỉ cần hồ sơ mới có đủ đặc trưng | Bị ảnh hưởng nặng khi hệ thống, người dùng hoặc gia sư mới chưa có lịch sử | Giảm nhẹ, nhưng vẫn cần một lượng dữ liệu tương tác tối thiểu |
| Độ phức tạp triển khai | Thấp: so khớp đặc trưng hồ sơ với nhu cầu | Trung bình đến cao: cần ma trận tương tác và mô hình học từ dữ liệu | Cao: phải kết hợp và cân bằng hai mô hình con |
| Mức độ phù hợp khi mới vận hành | Phù hợp: không cần dữ liệu tích lũy | Không phù hợp: chưa có dữ liệu tương tác | Chỉ phù hợp một phần |

*Nguồn: tổng hợp của nhóm từ [2].*

Bảng 2.1 cho thấy Content-Based Filtering phù hợp nhất với một hệ thống mới vận hành chưa có dữ liệu tương tác tích lũy. Bài toán tìm gia sư có cùng bản chất với các bài toán ghép nối như gợi ý việc làm phù hợp với hồ sơ ứng viên. Cả hai đều ghép một “nhu cầu” (tiêu chí của người học hoặc nhà tuyển dụng) với một tập “đối tượng có đặc trưng” (hồ sơ gia sư hoặc tin tuyển dụng) sao cho mức độ phù hợp là cao nhất.

## 2.2. Phương pháp Content-Based Filtering trên đặc trưng hồ sơ có cấu trúc

Trong các hệ thống khuyến nghị dựa trên nội dung (*Content-Based Filtering*), mỗi đối tượng được biểu diễn bằng các đặc trưng rồi so khớp với nhu cầu của người dùng; đối tượng có mức so khớp cao được xếp trước [2]. Trong đồ án này, đối tượng là gia sư, được biểu diễn qua bảy đặc trưng: môn dạy, khu vực, học phí theo giờ, số năm kinh nghiệm, hình thức dạy, lịch rảnh và điểm đánh giá trung bình. “Hồ sơ nhu cầu” của người học không lấy từ lịch sử mà do người học nhập trực tiếp tại thời điểm tìm kiếm.

Bảy đặc trưng trên có bản chất khác nhau: môn học và khu vực là so khớp tập hợp, học phí là đại lượng số có ngưỡng ngân sách, kinh nghiệm và đánh giá là đại lượng số liên tục, lịch rảnh là giao của hai tập khung giờ, còn hình thức dạy là biến phân loại. Vì chưa có một không gian đặc trưng thống nhất cho tất cả, đồ án không ép toàn bộ vào một vector để tính *cosine similarity*. Thay vào đó, mỗi tiêu chí được xử lý bằng một hàm điểm riêng (Mục 3.6). *Cosine similarity* là kỹ thuật phù hợp khi hồ sơ và nhu cầu được biểu diễn thành vector số (ví dụ vector từ mô tả văn bản của gia sư); kỹ thuật này không được dùng trong đồ án và chỉ được nhắc như một hướng mở rộng. Như vậy, xét theo phân loại của Adomavicius và Tuzhilin [2], phương pháp của đồ án thuộc nhánh Content-Based Filtering (trong tên đề tài đăng ký ghi là “Content-Base Filtering”) vì toàn bộ quá trình gợi ý chỉ dựa trên việc đối sánh đặc trưng nội dung hồ sơ gia sư với hồ sơ nhu cầu của người học mà không sử dụng lịch sử tương tác chéo giữa những người dùng. Tuy nhiên, thay vì vector hóa văn bản tự do để tính độ tương đồng góc (*cosine similarity*), đồ án hiện thực hóa Content-Based Filtering trên dữ liệu thuộc tính có cấu trúc thông qua hai bước: lọc điều kiện bắt buộc và tính tổng trọng số đa tiêu chí (*Weighted Scoring*).

## 2.3. Lọc theo điều kiện bắt buộc và Weighted Scoring

Hệ thống xử lý hai loại điều kiện theo hai cách khác nhau. Điều kiện bắt buộc được kiểm tra trước như ràng buộc lọc: gia sư không thỏa mãn điều kiện bắt buộc thì bị loại, không được xếp hạng dù các điểm khác cao. Trên tập gia sư còn lại, các tiêu chí ưu tiên được chuyển thành điểm thành phần trong khoảng $[0, 1]$ rồi gộp bằng Weighted Scoring [1]:

$$S(g) = \frac{\sum w_i \times s_i(g)}{\sum w_i} \qquad (2.1)$$

Trong công thức (2.1), $s_i(g) \in [0, 1]$ là điểm của gia sư $g$ theo tiêu chí $i$, và $w_i \ge 0$ là trọng số của tiêu chí $i$. Phép tổng chỉ lấy trên các tiêu chí đang được áp dụng (tiêu chí có $w_i > 0$ và có dữ liệu đầu vào; quy tắc chi tiết ở Mục 3.6). Weighted Scoring là phép tổng có bù trừ: điểm cao ở tiêu chí này có thể bù cho điểm thấp ở tiêu chí khác. Đó là lý do các điều kiện “không thể bù” như đúng môn học phải được lọc trước thay vì đưa vào điểm tổng.

Bảng 2.2 minh họa ảnh hưởng của trọng số bằng một ví dụ số đơn giản với ba gia sư giả định và ba tiêu chí. Đây là ví dụ lý thuyết, không phải dữ liệu thực của hệ thống; dữ liệu thực được sử dụng và đánh giá tại Chương 5.

**Bảng 2.2 - Ví dụ minh họa ảnh hưởng của mức ưu tiên đến thứ hạng**

| Gia sư | Điểm học phí | Điểm khu vực | Điểm đánh giá | Tổng điểm - bộ 1 | Hạng | Tổng điểm - bộ 2 | Hạng |
|:---|---:|---:|---:|---:|:---:|---:|:---:|
| A | 1,00 | 0,00 | 0,80 | 0,76 | 1 | 0,36 | 3 |
| B | 0,60 | 1,00 | 0,90 | 0,74 | 2 | 0,90 | 1 |
| C | 0,40 | 1,00 | 1,00 | 0,64 | 3 | 0,88 | 2 |

*Nguồn: ví dụ số do nhóm lập để minh họa (không phải dữ liệu thực của hệ thống).*

Bộ 1 ưu tiên học phí (trọng số học phí : khu vực : đánh giá = $3 : 1 : 1$); bộ 2 ưu tiên khu vực ($1 : 3 : 1$). Ví dụ với gia sư A ở bộ 1, tổng điểm là $S = (3 \times 1{,}00 + 1 \times 0{,}00 + 1 \times 0{,}80) \div 5 = 0{,}76$. Gia sư A xếp thứ nhất khi ưu tiên học phí nhưng xuống thứ ba khi ưu tiên khu vực, cho thấy thứ hạng phụ thuộc trực tiếp vào trọng số. Trong biểu diễn cộng tính, trọng số là độ đo mức ưu tiên do người ra quyết định đặt ra chứ không phải hằng số của bài toán [1]. Do đó không tồn tại một bộ trọng số “đúng” cho mọi nhu cầu; bộ mặc định của hệ thống chỉ là giá trị khởi tạo để minh họa (Mục 3.5).

## 2.4. Công nghệ sử dụng

Công nghệ trong đồ án là công cụ triển khai, không phải nội dung nghiên cứu chính. Backend dùng FastAPI [4] (Python) nhờ cú pháp khai báo kiểu dữ liệu rõ ràng giúp kiểm tra hợp lệ tiêu chí đầu vào. Khả năng tự sinh tài liệu API (Swagger UI) cũng hỗ trợ kiểm thử endpoint độc lập trước khi ghép giao diện. Frontend dùng ReactJS [5] để xây dựng giao diện demo tối giản gồm biểu mẫu nhập nhu cầu và danh sách kết quả tự động xếp hạng lại khi mức ưu tiên thay đổi. Dữ liệu gia sư mẫu lưu dạng JSON và CSV, đủ dùng cho quy mô vài chục đến vài trăm bản ghi; phương án SQLite là hướng mở rộng, chưa hiện thực trong đồ án.
