# PHẦN MỞ ĐẦU VÀ HỒ SƠ BÀN GIAO

> [!NOTE]
> Tài liệu này chứa nội dung các trang bìa, phần mở đầu (đánh số La Mã `i-xiii`) và hồ sơ bàn giao của báo cáo đồ án. Khi xuất sang Word (`.docx`) bằng `scripts/thesis/build_docx.py`, phần Mục lục, Danh mục bảng biểu và Danh mục hình ảnh được sinh kèm trường động `TOC` và `PAGEREF` dạng chấm dẫn.

## 1. Căn cứ và phạm vi

- **Quy chuẩn áp dụng:** Cấu trúc, bố cục, trang bìa khung hoa văn kèm logo CTUT, hệ thống phông chữ `Times New Roman`, bảng chuẩn Booktabs và quy ước đánh số trang thống nhất theo mẫu báo cáo Đồ án/Bài tập lớn chuẩn của Khoa Công nghệ Thông tin, Trường Đại học Kỹ thuật - Công nghệ Cần Thơ.
- **Nguồn nội dung:** `chuong-01`-`chuong-06` trong cùng thư mục, `tai-lieu-tham-khao.md`, các bảng/hình trong `docs/thesis/figures/`.
- **Tên đề tài dùng thống nhất:** “Hệ thống khuyến nghị gia sư dựa trên phương pháp Content-Base Filtering”.
- **Đánh số trang:** Bìa chính và bìa phụ không đánh số trang; phần mở đầu (`LỜI CẢM ƠN` đến `DANH MỤC HÌNH ẢNH`) dùng số La Mã thường (`i, ii, iii, ...`) ở giữa chân trang; từ `CHƯƠNG 1` đến hết `PHỤ LỤC` dùng số Ả Rập (`1, 2, 3, ...`) ở giữa chân trang.

## 2. Bảng tổng hợp phần mở đầu

| STT | Mục | Trạng thái | Quy cách trình bày trong `.docx` |
| :-: | :--- | :--- | :--- |
| 1 | Trang bìa chính | Đã chuẩn hóa (Mục 3.1) | Khổ A4, khung viền hoa văn `khung_trang_bia.png`, logo CTUT `3,0 cm`, không đánh số trang |
| 2 | Trang bìa phụ | Đã chuẩn hóa (Mục 3.2) | Khổ A4, cùng khung viền hoa văn bìa chính, không đánh số trang |
| 3 | Lời cảm ơn | Đã chuẩn hóa (Mục 4) | Kiểu `Front Title`, bắt đầu từ trang `i` |
| 4 | Lời cam đoan | Đã chuẩn hóa (Mục 5) | Kiểu `Front Title`, trang `ii` |
| 5 | Tóm tắt tiếng Việt | Đã chuẩn hóa (Mục 6.1) | Kiểu `Front Title`, gói gọn 1 trang `iii` |
| 6 | Abstract tiếng Anh | Đã chuẩn hóa (Mục 6.2) | Kiểu `Front Title`, gói gọn 1 trang `iv` |
| 7 | Mục lục | Tự động (Mục 7) | Kiểu `Front Title`, danh mục chấm dẫn (`TOC` + `PAGEREF`) cấp 1-3 và `Front Title` |
| 8 | Danh mục ký hiệu và chữ viết tắt | Đã chuẩn hóa (Mục 8) | Chia 2 tiểu mục `1. Chữ viết tắt` và `2. Ký hiệu toán học`, bảng Booktabs 3 cột |
| 9 | Danh mục bảng biểu | Tự động (Mục 9) | 31 bảng (`Bảng X.Y: Tên bảng`), dòng chấm dẫn kèm `PAGEREF` |
| 10 | Danh mục hình ảnh | Tự động (Mục 10) | 9 hình (`Hình X.Y: Tên hình`), dòng chấm dẫn kèm `PAGEREF` |

## 3. Trang bìa chính và trang bìa phụ

### 3.1. Trang bìa chính

> ỦY BAN NHÂN DÂN THÀNH PHỐ CẦN THƠ
> **TRƯỜNG ĐẠI HỌC KỸ THUẬT - CÔNG NGHỆ CẦN THƠ**
> **KHOA CÔNG NGHỆ THÔNG TIN**

*(Chèn logo chính thức của Trường Đại học Kỹ thuật - Công nghệ Cần Thơ `docs/thesis/figures/logo_ctut.png`, căn giữa trang, bề rộng `3,0 cm`.)*

> **BÁO CÁO ĐỒ ÁN**
> **KHOA HỌC MÁY TÍNH 1**

> **ĐỀ TÀI:**
> **HỆ THỐNG KHUYẾN NGHỊ GIA SƯ**
> **DỰA TRÊN PHƯƠNG PHÁP CONTENT-BASE FILTERING**

> **GVHD:** TS. Lê Anh Nhã Uyên
>
> **Sinh viên thực hiện:**
> Lê Thị Bích Chuyền - KHMT2411037
> Trần Nguyễn Đức - KHMT2411011
> Cao Khánh Ngọc - KHMT2411025
>
> **Lớp:** Khoa học máy tính 2024

> Cần Thơ, 22 tháng 11 năm 2026

### 3.2. Trang bìa phụ

> **BÁO CÁO ĐỒ ÁN KHOA HỌC MÁY TÍNH 1**
> **HỆ THỐNG KHUYẾN NGHỊ GIA SƯ**
> **DỰA TRÊN PHƯƠNG PHÁP CONTENT-BASE FILTERING**
>
> **Học kỳ:** Học kỳ 1, năm học 2026-2027
> **Lớp:** Khoa học máy tính 2024
> **GVHD:** TS. Lê Anh Nhã Uyên
>
> **Sinh viên thực hiện:**
> Lê Thị Bích Chuyền - KHMT2411037
> Trần Nguyễn Đức - KHMT2411011
> Cao Khánh Ngọc - KHMT2411025
>
> Cần Thơ, 22 tháng 11 năm 2026

## 4. Lời cảm ơn

Chúng em xin gửi lời cảm ơn đến TS. Lê Anh Nhã Uyên, giảng viên hướng dẫn đồ án Khoa học máy tính 1. Cô đã tận tình định hướng cho chúng em trong suốt quá trình làm đề tài. Nhờ các buổi trao đổi với cô, chúng em xác định được phạm vi đề tài là một bộ máy khuyến nghị có thể giải thích được. Cô cũng yêu cầu chúng em kiểm chứng bằng số liệu thực nghiệm thay vì mô tả cảm tính. Những góp ý của cô về cách đặt tiêu chí, kiểm thử ca biên và trình bày kết quả được thể hiện trong Chương 3 và Chương 5.

Chúng em cũng xin cảm ơn quý thầy cô Khoa Công nghệ Thông tin, Trường Đại học Kỹ thuật - Công nghệ Cần Thơ đã tạo điều kiện về tài liệu và môi trường học tập. Cảm ơn gia đình, bạn bè đã động viên, và cảm ơn các thành viên trong nhóm đã phối hợp để hoàn thành các hạng mục đúng tiến độ.

Trong khuôn khổ học phần hai tín chỉ kéo dài 12 tuần, đề tài tập trung hoàn thiện mô hình lõi trên bộ dữ liệu mẫu gồm 16 hồ sơ gia sư và 14 kịch bản kiểm thử; các giới hạn về quy mô dữ liệu và đánh giá thực tế được trình bày cụ thể ở Chương 5 và Chương 6.

## 5. Lời cam đoan

Chúng em là ba thành viên thực hiện đề tài, lớp Khoa học máy tính 2024. Chúng em cam đoan về báo cáo này như sau:

1. Nội dung báo cáo là kết quả làm việc của cả nhóm. Mọi tài liệu tham khảo đều được trích dẫn theo chuẩn IEEE và liệt kê trong mục Tài liệu tham khảo.
2. Số liệu thực nghiệm trong Chương 5 được lấy trực tiếp từ bộ kiểm thử tự động và từ phản hồi của dịch vụ API khuyến nghị, chạy trên bộ dữ liệu mẫu 16 hồ sơ. Các số liệu ước tính trong dữ liệu mẫu đều được đánh dấu và giải thích.
3. Bộ dữ liệu mẫu tách riêng nhóm hồ sơ thu thập công khai và nhóm hồ sơ giả lập. Hai hồ sơ thu thập công khai là GS-T06 và GS-T07 có học phí và lịch rảnh là số ước tính, được đánh dấu hoa thị (*), còn điểm đánh giá để trống. Chương 4, Chương 5 và Phụ lục A có giải thích thêm.
4. Báo cáo không sao chép nội dung từ công trình khác. Chúng em chỉ tham khảo đồ án GS360 [3] để đối chiếu phạm vi chức năng bài toán, không sử dụng lại mã nguồn hay giao diện của đồ án này.
5. Chúng em chịu trách nhiệm trước giảng viên hướng dẫn và hội đồng đánh giá về tính trung thực của nội dung báo cáo.

## 6. Tóm tắt

### 6.1. Tóm tắt tiếng Việt

Khi số hồ sơ gia sư tăng lên, người học phải cân nhắc cùng lúc môn học, khu vực, học phí, hình thức học và thời gian rảnh. Các tiêu chí này thường xung đột nhau, nên chỉ lọc nhị phân theo từng tiêu chí thì khó xác định được danh sách gia sư phù hợp. Đồ án xây dựng một bộ máy khuyến nghị gia sư theo phương pháp lọc dựa trên nội dung (*Content-Based Filtering*), dùng các đặc trưng có cấu trúc của hồ sơ. Đầu tiên, hệ thống lọc theo các điều kiện bắt buộc là môn học, hình thức học và khung giờ giao nhau. Tiếp theo, hệ thống kiểm tra ngưỡng dữ liệu tối thiểu của hồ sơ. Sau đó, hệ thống chấm điểm năm tiêu chí ưu tiên gồm học phí, khu vực, kinh nghiệm, đánh giá và lịch rảnh, rồi tổng hợp bằng tính tổng có trọng số (*Weighted Scoring*). Mỗi tiêu chí có một trong bốn mức ưu tiên, tương ứng trọng số nguyên từ 0 đến 3. Nhờ vậy người học chỉnh được thứ hạng gợi ý mà không phải tự chia tỷ lệ phần trăm.

Phần dịch vụ API được cài đặt bằng FastAPI (Python 3.12) và phần giao diện minh họa bằng React. Hệ thống chạy trên bộ dữ liệu mẫu gồm 16 hồ sơ gia sư và 14 kịch bản đánh giá cố định. Kết quả cho thấy 200/200 bài kiểm thử tự động đạt, độ bao phủ câu lệnh trên khối mã nghiệp vụ là 97%. Cả 14/14 kịch bản đều trả về danh sách Top-3 khớp với kỳ vọng, và thời gian xử lý trung bình phía máy chủ là 3,54 ms. Khi khảo sát độ nhạy, thứ hạng ổn định nếu thay đổi hệ số dung sai học phí và mốc kinh nghiệm bão hòa trong dải hợp lý. Thứ hạng chỉ đổi rõ khi đổi bộ mức ưu tiên, điều này đúng với thiết kế vì trọng số là đầu vào do người học tự điều khiển.

Hạn chế chính là bộ dữ liệu mẫu còn nhỏ, chưa có dữ liệu tương tác lịch sử, và chưa tiến hành đánh giá trên người học thực tế ngoài nhóm. Hướng phát triển tiếp theo là mở rộng dữ liệu, thu thập phản hồi sau khuyến nghị, và thêm tiêu chí cấp lớp cùng mục tiêu học tập vào mô hình tính điểm.

### 6.2. Abstract (English)

Choosing a tutor means weighing subject, district, fee, teaching mode and available time slots at the same time. These criteria often conflict, so filtering on each one separately does not give a sensible shortlist. This project builds a tutor recommendation engine using content-based filtering on structured profile attributes. The system first applies the mandatory conditions: subject, teaching mode and overlapping time slots. It then checks a minimum-data threshold. After that, it scores five preference criteria (fee, district, experience, rating and availability) and combines them with weighted scoring. Each criterion takes one of four priority levels, mapped to integer weights from 0 to 3, so learners can adjust the ranking without setting percentages themselves.

We implemented the API service with FastAPI (Python 3.12) and a demo interface with React. We evaluated the system on a sample dataset of 16 tutor profiles and 14 fixed scenarios. All 200 automated tests pass, with 97% statement coverage of the business modules. All 14 scenarios return the expected top-3 ranking, and the mean server-side processing time is 3.54 ms. In the sensitivity study, rankings stay stable when the fee tolerance and the experience saturation threshold vary within a reasonable range. They change clearly only when the priority preset changes, which fits the design, since the weights are set by the learner.

The main limitations are the small sample dataset, the lack of historical interaction data, and the lack of evaluation with learners outside our group. Future work includes expanding the dataset, collecting feedback after recommendations, and adding grade-level and learning-goal criteria.

## 7. Khung mục lục

Mục lục được tạo tự động trong `.docx` từ kiểu `Front Title` và ba cấp Heading (`Heading 1` = chương / tài liệu tham khảo / phụ lục, `Heading 2` = mục `X.Y` / `Phụ lục A..D`, `Heading 3` = tiểu mục `X.Y.Z` / `A.1..D.2`).

| Cấp / Mục | Tiêu đề | Trang |
| :--- | :--- | :-: |
| **Mở đầu** | LỜI CẢM ƠN | i |
| **Mở đầu** | LỜI CAM ĐOAN | ii |
| **Mở đầu** | TÓM TẮT | iii |
| **Mở đầu** | ABSTRACT | iv |
| **Mở đầu** | MỤC LỤC | … |
| **Mở đầu** | DANH MỤC KÝ HIỆU VÀ CHỮ VIẾT TẮT | … |
| **Mở đầu** | DANH MỤC BẢNG BIỂU | … |
| **Mở đầu** | DANH MỤC HÌNH ẢNH | … |
| **Chương 1** | TỔNG QUAN VỀ ĐỀ TÀI | … |
| 1.1 | Lý do chọn đề tài | … |
| 1.2 | Khảo sát hiện trạng | … |
| 1.3 | Vấn đề còn tồn tại và lý do chọn hướng tiếp cận | … |
| 1.4 | Mục tiêu và phạm vi đề tài | … |
| 1.5 | Công cụ và kế hoạch thực hiện | … |
| 1.6 | Cấu trúc báo cáo | … |
| **Chương 2** | CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ | … |
| 2.1 | Hệ thống khuyến nghị | … |
| 2.2 | Phương pháp Content-Based Filtering trên đặc trưng hồ sơ có cấu trúc | … |
| 2.3 | Lọc theo điều kiện bắt buộc và Weighted Scoring | … |
| 2.4 | Công nghệ sử dụng | … |
| **Chương 3** | PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG | … |
| 3.1 | Phát biểu bài toán | … |
| 3.2 | Yêu cầu chức năng | … |
| 3.3 | Yêu cầu phi chức năng | … |
| 3.4 | Mô hình hóa mức độ phù hợp | … |
| 3.5 | Thiết kế dữ liệu | … |
| 3.6 | Thiết kế thuật toán | … |
| 3.7 | Kiến trúc hệ thống và luồng xử lý | … |
| 3.8 | Thiết kế giao diện | … |
| **Chương 4** | XÂY DỰNG HỆ THỐNG | … |
| 4.1 | Chuẩn bị môi trường phát triển | … |
| 4.2 | Xây dựng tập dữ liệu mẫu | … |
| 4.3 | Cài đặt module tính điểm | … |
| 4.4 | Xây dựng API khuyến nghị | … |
| 4.5 | Xây dựng giao diện demo | … |
| 4.6 | Tích hợp giao diện với API và kiểm tra luồng end-to-end | … |
| 4.7 | Giới hạn của việc hiện thực | … |
| **Chương 5** | KIỂM THỬ VÀ ĐÁNH GIÁ | … |
| 5.1 | Kiểm thử chức năng và ca biên | … |
| 5.2 | Đánh giá chất lượng xếp hạng | … |
| 5.3 | Hạn chế của hệ thống | … |
| **Chương 6** | KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN | … |
| 6.1 | Kết quả đạt được | … |
| 6.2 | Hạn chế và hướng phát triển | … |
| 6.3 | Tự đánh giá và phân công công việc | … |
| **Tham khảo** | TÀI LIỆU THAM KHẢO | … |
| **Phụ lục** | PHỤ LỤC | … |
| A | Phụ lục A. Bộ dữ liệu mẫu | … |
| B | Phụ lục B. Module tính điểm và xếp hạng | … |
| C | Phụ lục C. Danh mục sơ đồ thiết kế và hình ảnh giao diện | … |
| D | Phụ lục D. Kịch bản kiểm thử thực nghiệm | … |

## 8. Danh mục ký hiệu và chữ viết tắt

### 8.1. Chữ viết tắt

| Chữ viết tắt | Nghĩa | Xuất hiện đầu |
| :--- | :--- | :--- |
| API | Application Programming Interface - giao diện lập trình ứng dụng | Mục 1.4 |
| ASGI | Asynchronous Server Gateway Interface - chuẩn máy chủ bất đồng bộ cho Python | Bảng 4.1 (Mục 4.1) |
| BCE | Boundary-Control-Entity - mô hình kiến trúc Biên - Điều khiển - Thực thể | Mục 3.7.2 |
| CI | Continuous Integration - tích hợp và kiểm thử tự động liên tục | Mục 4.7 |
| CN01-CN03 | Ba chức năng chính: nhập nhu cầu, xem gợi ý, điều chỉnh mức ưu tiên | Bảng 3.1 (Mục 3.2) |
| CORS | Cross-Origin Resource Sharing - cơ chế chia sẻ tài nguyên khác nguồn (trong `CORSMiddleware`) | Hình 3.2 (Mục 3.7.2); Mục 4.4.1 |
| CSS | Cascading Style Sheets - ngôn ngữ định kiểu trình bày giao diện web | Mục 4.5 |
| CSV | Comma-Separated Values - định dạng tệp văn bản phân tách bằng dấu phẩy | Mục 1.5 |
| ERD | Entity-Relationship Diagram - sơ đồ thực thể - kết hợp | Mục 3.5 |
| GS | Tiền tố mã hồ sơ gia sư trong bộ dữ liệu mẫu (như `GS-T06`, `GS-G01`, `GS006`) | Bảng 3.3 (Mục 3.5) |
| GVHD | Giảng viên hướng dẫn | Trang bìa |
| HTML | HyperText Markup Language - ngôn ngữ đánh dấu siêu văn bản | Mục 4.5 |
| HTTP | Hypertext Transfer Protocol - giao thức truyền tải siêu văn bản | Mục 3.7.1 |
| IEEE | Institute of Electrical and Electronics Engineers - Viện Kỹ sư Điện và Điện tử (chuẩn trích dẫn tài liệu và chuẩn số thực dấu phẩy động IEEE 754) | Lời cam đoan; Mục 4.3.1 |
| ISO | International Organization for Standardization - Tổ chức Tiêu chuẩn hóa Quốc tế (quy chuẩn lưu đồ ISO 5807) | Mục 3.7.1; Phụ lục C |
| JSON | JavaScript Object Notation - định dạng trao đổi dữ liệu có cấu trúc | Mục 1.5 |
| KB01-KB14 | Mã định danh 14 kịch bản kiểm thử thực nghiệm cố định | Mục 3.5 (KB05); Mục 4.2.3 |
| KV | Khu vực (ký hiệu các khu vực giả định KV1, KV2, KV3 trong ví dụ minh họa) | Bảng 3.6 (Mục 3.6) |
| LTR | Learning-to-Rank - nhóm thuật toán học máy học xếp hạng | Mục 6.2.2 |
| OpenAPI | Đặc tả giao diện lập trình ứng dụng RESTful chuẩn hóa (hiển thị qua Swagger UI) | Mục 2.4; Mục 4.1 |
| PA1 | Phương án 1 - ánh xạ mục tiêu học tập sang bộ mức ưu tiên khởi tạo | Mục 6.1.2 |
| QĐ-A-QĐ-E | Năm quyết định triển khai xử lý tình huống biên của mô-đun tính điểm | Mục 4.3.1 |
| RESTful | Kiến trúc dịch vụ web theo phong cách Representational State Transfer | Mục 4.4 |
| SPA | Single Page Application - ứng dụng web một trang | Bảng 4.1 (Mục 4.1) |
| TDD | Test-Driven Development - phương pháp phát triển hướng kiểm thử | Mục 5.1.1 |
| Top-$k$ | Danh sách $k$ gia sư có điểm phù hợp cao nhất sau khi xếp hạng | Mục 1.3.2 |
| TQ1-TQ5 | Năm truy vấn bổ sung dùng trong thực nghiệm mở rộng Phương án 1 | Mục 6.1.2 |
| UI | User Interface - giao diện người dùng (trong Swagger UI) | Mục 2.4 |
| UML | Unified Modeling Language - ngôn ngữ mô hình hóa thống nhất (sơ đồ trình tự UML 2.5) | Phụ lục C |
| URL | Uniform Resource Locator - địa chỉ định vị tài nguyên thống nhất | Mục 1.2 |
| VNĐ | Việt Nam đồng | Mục 2.2 |

### 8.2. Ký hiệu toán học

| Ký hiệu | Nghĩa | Xuất hiện đầu |
| :--- | :--- | :--- |
| $A$ | Tập các tiêu chí ưu tiên đang áp dụng trong một truy vấn ($w_i > 0$ và có đủ đầu vào hợp lệ) | Công thức (2.1) (Mục 2.3) |
| $B$ | Ngân sách học phí tối đa theo giờ do người học nhập (VNĐ) | Bảng 3.6 (Mục 3.6) |
| $C_i$ | Điểm đóng góp có trọng số của tiêu chí $i$ cho gia sư $g$, $C_i(g) = \frac{w_i \cdot s_i(g)}{\sum_{j \in A} w_j}$ | Mục 3.6 |
| $E$ | Số năm kinh nghiệm giảng dạy của gia sư | Bảng 3.6 (Mục 3.6) |
| $E_{\max}$ | Mốc kinh nghiệm bão hòa (mặc định $8$ năm) dùng trong hàm điểm kinh nghiệm | Bảng 3.6 (Mục 3.6) |
| $g$ | Một hồ sơ ứng viên gia sư trong tập dữ liệu được xem xét chấm điểm và xếp hạng | Công thức (2.1) (Mục 2.3) |
| $K$ | Khu vực dạy học mong muốn của người học | Bảng 3.6 (Mục 3.6) |
| $k$ | Số lượng gia sư tối đa trả về trong danh sách kết quả Top-$k$ (mặc định $k = 3$, miền $[1, 20]$) | Mục 1.3.2; Bảng 3.4 |
| $L$ | Tập khung giờ rảnh do người học yêu cầu | Bảng 3.6 (Mục 3.6) |
| $n$ | Số tiêu chí ưu tiên có hiệu lực ($w_i > 0$) trong một truy vấn, không tính Đánh giá | Mục 3.6; Bảng 3.7 |
| $P$ | Học phí theo giờ trong hồ sơ gia sư (VNĐ) | Bảng 3.6 (Mục 3.6) |
| $R$ | Điểm đánh giá trung bình của gia sư theo thang $5$ | Bảng 3.6 (Mục 3.6) |
| $S(g)$ | Điểm phù hợp tổng hợp của gia sư $g$, thuộc đoạn $[0, 1]$ | Công thức (2.1) (Mục 2.3) |
| $s_i(g)$ | Điểm thành phần của gia sư $g$ theo tiêu chí thứ $i$, thuộc đoạn $[0, 1]$ | Công thức (2.1) (Mục 2.3) |
| $T$ | Tập khung giờ rảnh của gia sư trong tuần | Bảng 3.6 (Mục 3.6) |
| $w_i$ | Trọng số của tiêu chí thứ $i$, quy đổi từ mức ưu tiên thuộc $\{0, 1, 2, 3\}$ | Mục 1.1; Công thức (2.1) (Mục 2.3) |
| $\delta$ | Hệ số dung sai học phí vượt ngân sách (mặc định $0{,}5$) | Bảng 3.6 (Mục 3.6) |
| $\Delta S$ | Độ lệch điểm tổng hợp giữa kết quả hệ thống và tính tay ban đầu, $\Delta S = S_{\text{hệ thống}} - S_{\text{tính tay}}$ | Bảng 5.4 (Mục 5.2.1) |

## 9. Danh mục bảng biểu

| Số hiệu | Tên bảng | Trang |
| :--- | :--- | :-: |
| Bảng 1.1: | Khảo sát chức năng tìm kiếm của một số kênh/nền tảng | … |
| Bảng 1.2: | Phân bổ thời gian thực hiện theo chương | … |
| Bảng 2.1: | So sánh ba nhóm phương pháp trong hệ thống khuyến nghị | … |
| Bảng 2.2: | Ví dụ minh họa ảnh hưởng của mức ưu tiên đến thứ hạng | … |
| Bảng 3.1: | Danh sách chức năng chính | … |
| Bảng 3.2: | Phân loại tiêu chí | … |
| Bảng 3.3: | Cấu trúc bản ghi hồ sơ gia sư | … |
| Bảng 3.4: | Cấu trúc bản ghi nhu cầu của người học | … |
| Bảng 3.5: | Quy đổi mức ưu tiên sang trọng số | … |
| Bảng 3.6: | Công thức điểm thành phần | … |
| Bảng 3.7: | Ngưỡng dữ liệu tối thiểu để được xếp hạng | … |
| Bảng 4.1: | Thành phần và công nghệ của hệ thống tại thời điểm hiện thực | … |
| Bảng 4.2: | Ánh xạ trường dữ liệu thiết kế sang định danh trong mã nguồn | … |
| Bảng 4.3: | Tệp, hàm/lớp chính và bước quy trình tương ứng (Mục 3.6) | … |
| Bảng 4.4: | Các trạng thái phản hồi của `POST /api/recommend` | … |
| Bảng 4.5: | Thành phần giao diện và chức năng theo CN01-CN03 | … |
| Bảng 4.6: | Các tình huống lỗi và nơi xử lý | … |
| Bảng 5.1: | Phân bổ bộ kiểm thử tự động theo nhóm | … |
| Bảng 5.2: | Kết quả kiểm thử ca biên của các hàm điểm và tính đơn điệu | … |
| Bảng 5.3: | Kết quả thực nghiệm 14 kịch bản đánh giá | … |
| Bảng 5.4: | Tổng hợp kết quả đối chiếu Top-3 theo nhóm đặc trưng kịch bản | … |
| Bảng 5.5: | Độ nhạy của Top-3 theo tham số dung sai học phí $\delta$ | … |
| Bảng 5.6: | Độ nhạy của Top-3 theo mốc kinh nghiệm bão hòa $E_{\max}$ | … |
| Bảng 5.7: | Độ nhạy của Top-3 theo mức biến động ngân sách | … |
| Bảng 5.8: | Ảnh hưởng của bốn bộ mức ưu tiên đến Top-3 | … |
| Bảng 5.9: | Thành phần điểm và mức đóng góp của Top-3 gia sư tại KB01 | … |
| Bảng 6.1: | Phân công công việc và mức độ hoàn thành của các thành viên trong nhóm | … |
| Bảng A.1: | Danh sách 16 hồ sơ gia sư mẫu | … |
| Bảng B.1: | Danh mục tệp mã nguồn và hàm nghiệp vụ trong module gợi ý gia sư | … |
| Bảng C.1: | Danh mục sơ đồ thiết kế và hình ảnh giao diện của hệ thống | … |
| Bảng D.1: | Yêu cầu đầy đủ của 14 kịch bản thực nghiệm | … |

## 10. Danh mục hình ảnh

| Số hiệu | Tên hình | Trang |
| :--- | :--- | :-: |
| Hình 3.1: | Sơ đồ luồng xử lý khuyến nghị | … |
| Hình 3.2: | Kiến trúc hệ thống ba lớp | … |
| Hình 3.3: | Sơ đồ trình tự xử lý yêu cầu khuyến nghị | … |
| Hình 3.4: | Phác thảo màn hình nhập nhu cầu | … |
| Hình 3.5: | Phác thảo màn hình kết quả | … |
| Hình 4.1: | Màn hình nhập nhu cầu học tập (CN01) | … |
| Hình 4.2: | Màn hình kết quả gợi ý Top-3 kịch bản KB01 (CN02) | … |
| Hình 4.3: | Điều chỉnh mức ưu tiên trực tiếp (CN03) làm đổi hạng | … |
| Hình 4.4: | Trạng thái biên tổng trọng số bằng 0 ($\sum w_i = 0$) | … |

## 11. Hồ sơ bàn giao

### 11.1. Cấu trúc tệp báo cáo

| Tệp | Nội dung | Trạng thái |
| :--- | :--- | :--- |
| `chuong-01-tong-quan.md` | Chương 1 | Hoàn thành |
| `chuong-02-co-so-ly-thuyet-va-cong-nghe.md` | Chương 2 | Hoàn thành |
| `chuong-03-phan-tich-thiet-ke.md` | Chương 3 | Hoàn thành (5 hình đã chèn) |
| `chuong-04-xay-dung-he-thong.md` | Chương 4 | Hoàn thành (4 ảnh giao diện) |
| `chuong-05-thuc-nghiem-va-danh-gia.md` | Chương 5 | Hoàn thành (9 bảng) |
| `chuong-06-ket-luan-va-huong-phat-trien.md` | Chương 6 và Phụ lục A-D | Hoàn thành |
| `tai-lieu-tham-khao.md` | 7 tài liệu theo chuẩn IEEE | Hoàn thành (đã kiểm chứng DOI/URL gồm 7 nguồn trích dẫn tuần tự [1]-[7]) |
| `muc-luc-va-ho-so-ban-giao.md` | Phần mở đầu theo chuẩn báo cáo đồ án CTUT (KHMT 1) + danh mục bàn giao | Hoàn thành |
| `docs/thesis/figures/*.png` | 9 hình của báo cáo + `khung_trang_bia.png` + `logo_ctut.png` (kèm 4 tệp nguồn `docs/thesis/figures/src/*.drawio`) | Đủ 11 tệp ảnh |
| `docs/thesis/outline/dac-ta-hinh-3-1-3-5.md` | Đặc tả 5 hình Chương 3 (tài liệu làm việc) | Lưu nội bộ |

### 11.2. Việc còn lại trước khi nộp

| # | Việc | Người phụ trách | Trạng thái |
| :-: | :--- | :--- | :--- |
| 1 | Ghép 6 chương + tài liệu tham khảo + phụ lục thành một tệp Word theo chuẩn báo cáo đồ án CTUT (KHMT 1) | Nhóm | Tự động qua `scripts/thesis/build_docx.py` (`BAO_CAO_DO_AN_KHMT1_HOAN_CHINH.docx`) |
| 2 | Điền số trang cho mục lục, danh mục bảng, danh mục hình | Nhóm | Nhúng trường động `TOC` và `PAGEREF` kèm `<w:updateFields w:val="true"/>` và dòng chấm dẫn |
| 3 | Rà từ cấm, chuẩn hóa số liệu và kiểm định tệp DOCX | Nhóm | `check_captions.py`, `recompute_numbers.py` (74/74 KHỚP), `verify_docx.py` |
| 4 | Slide thuyết trình và kịch bản bảo vệ (40 slide) | Nhóm | Đã hoàn thiện (`docs/thesis/slides/`, `SLIDE_BAO_VE_DO_AN_KHMT1.pptx/.pdf`) |

### 11.3. Ghi chú còn treo

- Mục 6.1.1 trình bày phần đối chiếu với 4 mục tiêu đề tài bằng danh sách đánh số `1-4` theo quy chuẩn báo cáo đồ án CTUT (không dùng bảng không đánh số, giữ nguyên 31 bảng được cấp số `Bảng X.Y:`).
- Nhãn `public_collected` của `GS-T06`, `GS-T07` được giữ nguyên; phần học phí và lịch rảnh ước tính đã ghi chú ở Chương 4, Chương 5 và Phụ lục A.
- Bản Abstract tiếng Anh giữ dấu chấm thập phân (`3.54 ms`) theo quy ước tiếng Anh; thân bài tiếng Việt dùng dấu phẩy (`3,54 ms`).
