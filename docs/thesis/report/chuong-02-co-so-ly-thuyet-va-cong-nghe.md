# CHƯƠNG 2. CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ

## 2.1. Hệ thống khuyến nghị

Hệ thống khuyến nghị (*recommender system*) ước lượng mức độ phù hợp của một đối tượng với người dùng, rồi xếp hạng để gợi ý những lựa chọn tốt nhất [2]. Có ba nhóm phương pháp phổ biến là Content-Based Filtering (dựa trên đặc trưng đối tượng), Collaborative Filtering (dựa trên hành vi tương tác của nhiều người dùng) và Hybrid (kết hợp cả hai) [2]. Bảng 2.1 so sánh ba nhóm phương pháp này trong bối cảnh bài toán tìm gia sư.

**Bảng 2.1: So sánh ba nhóm phương pháp trong hệ thống khuyến nghị**

| Tiêu chí | Content-Based Filtering | Collaborative Filtering | Hybrid |
|:---|:---|:---|:---|
| Dữ liệu cần có | Đặc trưng hồ sơ (môn dạy, khu vực, học phí, v.v.) | Lịch sử tương tác của nhiều người dùng (rating, số buổi học) | Cả hai loại dữ liệu trên |
| Vấn đề cold-start | Ít bị ảnh hưởng: chỉ cần hồ sơ mới có đủ đặc trưng | Bị ảnh hưởng nặng khi hệ thống, người dùng hoặc gia sư mới chưa có lịch sử | Giảm nhẹ, nhưng vẫn cần một lượng dữ liệu tương tác tối thiểu |
| Độ phức tạp triển khai | Thấp: so khớp đặc trưng hồ sơ với nhu cầu | Trung bình đến cao: cần ma trận tương tác và mô hình học từ dữ liệu | Cao: phải kết hợp và cân bằng hai mô hình con |
| Mức độ phù hợp khi mới vận hành | Phù hợp: không cần dữ liệu tích lũy | Không phù hợp: chưa có dữ liệu tương tác | Chỉ phù hợp một phần |

*(Tổng hợp từ [2].)*

Từ Bảng 2.1, có thể thấy Content-Based Filtering là phương pháp phù hợp nhất đối với một hệ thống mới chưa có lịch sử tương tác. Cách làm của bài toán tìm gia sư khá giống bài toán ghép nối hồ sơ: hệ thống lấy yêu cầu của người học, đem so với các thuộc tính mô tả gia sư để chọn ra những người phù hợp nhất.

## 2.2. Phương pháp Content-Based Filtering trên đặc trưng hồ sơ có cấu trúc

Với phương pháp lọc dựa trên nội dung (*Content-Based Filtering*), hệ thống mô tả mỗi đối tượng bằng một tập đặc trưng rồi so khớp với nhu cầu của người dùng. Đối tượng nào khớp hơn thì xếp trên [2]. Trong đồ án này, mỗi gia sư được mô tả qua bảy đặc trưng: môn dạy, khu vực, học phí theo giờ, số năm kinh nghiệm, hình thức dạy, lịch rảnh và điểm đánh giá trung bình. Về phía người học, hệ thống không suy đoán sở thích từ lịch sử cũ mà lấy trực tiếp nhu cầu vừa nhập lúc tìm kiếm.

Bảy đặc trưng trên có kiểu dữ liệu rất khác nhau. Môn học và khu vực so khớp theo tập hợp, còn hình thức dạy là biến phân loại. Trong dữ liệu hệ thống, học phí (VNĐ/giờ) là số nguyên không âm được đánh giá qua ngưỡng ngân sách mềm, trong khi kinh nghiệm là số thực không âm (bão hòa ở cận trên khi chấm điểm) và điểm đánh giá nằm trên thang điểm $[0, 5]$ (cho phép khuyết dữ liệu với gia sư mới). Riêng lịch rảnh tính theo tỷ lệ giao giữa hai tập khung giờ. Vì các thuộc tính không cùng bản chất như vậy, hệ thống không gom tất cả thành một vector để tính độ tương đồng cosine (*cosine similarity*). Cách tính cosine thường hợp với dữ liệu văn bản tự do hơn.

Xét theo phân loại của Adomavicius và Tuzhilin [2], hướng tiếp cận của đề tài thuộc nhánh Content-Based Filtering (tên đề tài đăng ký ghi là “Content-Base Filtering”). Toàn bộ gợi ý chỉ dựa trên việc so sánh hồ sơ gia sư với yêu cầu hiện tại của người học, không dùng lịch sử tương tác giữa nhiều người dùng. Quy trình xử lý gồm hai bước: lọc các điều kiện bắt buộc trước, sau đó chấm điểm từng tiêu chí về đoạn $[0, 1]$ rồi cộng có trọng số (*Weighted Scoring*).

## 2.3. Lọc theo điều kiện bắt buộc và Weighted Scoring

Hệ thống xử lý hai nhóm điều kiện tách biệt nhau. Điều kiện bắt buộc là ràng buộc cứng. Nếu gia sư không đạt điều kiện bắt buộc thì bị loại ngay, dù các điểm khác có cao đến đâu. Với những gia sư vượt qua bước lọc, hệ thống chấm điểm từng tiêu chí ưu tiên về đoạn $[0, 1]$, sau đó tính tổng điểm bằng công thức Weighted Scoring [1]:

$$S(g) = \frac{\sum_{i \in A} w_i \cdot s_i(g)}{\sum_{i \in A} w_i} \qquad (2.1)$$

Trong công thức (2.1), $s_i(g) \in [0, 1]$ là điểm thành phần của gia sư $g$ ở tiêu chí $i$, còn $w_i \in \{0, 1, 2, 3\}$ là trọng số đi kèm. Tập $A$ gồm các tiêu chí ưu tiên có $w_i > 0$ và có đủ đầu vào hợp lệ từ truy vấn, với điều kiện $\sum_{i \in A} w_i > 0$ (nếu $A = \emptyset \Rightarrow \sum_{i \in A} w_i = 0$, hệ thống bỏ qua bước xếp hạng và trả trạng thái `zero_weight`). Vì phép cộng có trọng số cho phép bù trừ giữa các tiêu chí, điểm cao ở tiêu chí này có thể bù cho điểm thấp ở tiêu chí kia. Vì vậy những điều kiện không thể bù trừ như đúng môn học hay trùng lịch rảnh phải được lọc riêng từ đầu.

Bảng 2.2 đưa ra một ví dụ nhỏ với ba gia sư giả định để thấy trọng số làm đổi thứ hạng như thế nào. Đây chỉ là ví dụ minh họa công thức. Kết quả chạy thật trên bộ dữ liệu mẫu được trình bày ở Chương 5.

**Bảng 2.2: Ví dụ minh họa ảnh hưởng của mức ưu tiên đến thứ hạng**

| Gia sư | Điểm học phí | Điểm khu vực | Điểm đánh giá | Tổng điểm (Bộ 1) | Hạng (Bộ 1) | Tổng điểm (Bộ 2) | Hạng (Bộ 2) |
|:---|---:|---:|---:|---:|:---:|---:|:---:|
| A | 1,00 | 0,00 | 0,80 | 0,76 | 1 | 0,36 | 3 |
| B | 0,60 | 1,00 | 0,90 | 0,74 | 2 | 0,90 | 1 |
| C | 0,40 | 1,00 | 1,00 | 0,64 | 3 | 0,88 | 2 |

*(Ví dụ số minh họa 3 tiêu chí cho công thức (2.1) với Bộ 1 tỷ lệ 3:1:1 và Bộ 2 tỷ lệ 1:3:1, trước khi mở rộng sang mô hình đầy đủ 5 tiêu chí ở Chương 3.)*

Trong Bảng 2.2, bộ 1 ưu tiên học phí với tỷ lệ học phí : khu vực : đánh giá là $3 : 1 : 1$, còn bộ 2 ưu tiên khu vực với tỷ lệ $1 : 3 : 1$. Chẳng hạn với gia sư A ở bộ 1, tổng điểm là $S = (3 \times 1{,}00 + 1 \times 0{,}00 + 1 \times 0{,}80) \div 5 = 0{,}76$. Gia sư A xếp nhất khi người học ưu tiên học phí, nhưng giảm xuống hạng ba khi người học ưu tiên khu vực. Như vậy, trọng số thể hiện ý muốn chủ quan của người tìm gia sư chứ không phải hằng số cố định [1]. Không có một bộ trọng số nào là tốt nhất cho tất cả mọi người, nên bộ mặc định của hệ thống chỉ dùng làm mức khởi đầu.

## 2.4. Công nghệ sử dụng

Để đưa mô hình vào vận hành thử nghiệm, nhóm thực hiện lựa chọn các công cụ gọn nhẹ và thuận tiện cho việc kiểm thử. Phía máy chủ (backend) viết bằng Python với khung FastAPI [4] kết hợp Pydantic v2. FastAPI và Pydantic v2 hỗ trợ kiểm tra kiểu dữ liệu đầu vào chặt chẽ và tự tạo trang Swagger UI (OpenAPI), giúp thử nhanh từng endpoint mà không cần chờ giao diện. Phía người dùng (frontend) viết bằng thư viện React [5] và công cụ đóng gói Vite, gồm màn hình nhập nhu cầu và màn hình xem kết quả có thanh chỉnh mức ưu tiên trực tiếp. Dữ liệu gia sư mẫu được lưu bằng tệp JSON và CSV để dễ đọc, dễ đối chiếu và gọn nhẹ khi thử nghiệm.
