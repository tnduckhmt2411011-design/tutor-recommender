# CHƯƠNG 6. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

## 6.1. Kết quả đạt được

Đến nay, đồ án đã hoàn thành các thành phần chính của đề tài “Hệ thống khuyến nghị gia sư dựa trên phương pháp Content-Base Filtering”. Cụ thể gồm có mô hình điểm, module tính điểm, dịch vụ API, giao diện minh họa và bộ kiểm thử tự động. Dưới đây là kết quả đối chiếu với bốn mục tiêu đã đặt ra ở Mục 1.4.

### 6.1.1. Đối chiếu kết quả thực hiện với bốn mục tiêu đề tài

1. **Mô hình hóa mức độ phù hợp và viết module tính điểm.** Bảy đặc trưng hồ sơ được phân thành ba nhóm theo Bảng 3.2: nhóm điều kiện bắt buộc (môn học, hình thức học và khung giờ giao nhau tối thiểu, trong đó lịch rảnh đồng thời tham gia chấm điểm ưu tiên), nhóm năm tiêu chí ưu tiên có trọng số (học phí, khu vực, kinh nghiệm, đánh giá và lịch rảnh) và nhóm tiêu chí tùy chọn khi người học đặt trọng số $w_i = 0$. Kèm theo đó là bảng ngưỡng dữ liệu tối thiểu (Bảng 3.7) và năm hàm chuẩn hóa điểm thành phần về đoạn $[0, 1]$ (Bảng 3.6). Quy trình bốn bước nằm độc lập trong `backend/app/scoring/` (Mục 4.3, Phụ lục B) và vượt qua 111 bài kiểm thử đơn vị trực tiếp cho gói `scoring/` (nằm trong 132 bài kiểm thử đơn vị và môi trường ở Bảng 5.1) cùng bộ ca biên ở Bảng 5.2. Điểm còn hạn chế là các tham số khởi tạo ($\delta = 0{,}5$, $E_{\max} = 8$ năm, điểm trung tính $0{,}5$) và bộ trọng số $\{0, 1, 2, 3\}$ do nhóm thực hiện đặt theo kinh nghiệm. Chúng chưa được học từ dữ liệu người dùng thật.
2. **Xây dựng dịch vụ API khuyến nghị bằng FastAPI.** Điểm cuối `POST /api/recommend` chạy trên FastAPI và Python 3.12 (Mục 4.4), kiểm tra đầu vào bằng Pydantic (`extra="forbid"`). API trả đủ ba trạng thái HTTP 200 (`success`, `no_match` với hai biến thể, `zero_weight`) cùng mã lỗi HTTP 422 (Bảng 4.4). Bộ kiểm thử tích hợp đạt 41/41 bài, với thời gian xử lý nội tại trung bình 3,54 ms (chậm nhất 7,97 ms trong 140 lượt đo chuẩn ở Mục 5.1.2). Do backend chạy trên gói Render Free Tier, theo tài liệu nền tảng, máy chủ ước tính cần khoảng 30-40 giây để khởi động lại sau thời gian nghỉ; bên cạnh đó, độ trễ mạng thực tế qua Internet chưa được đo đạc định lượng.
3. **Xây dựng giao diện minh họa bằng React.** Giao diện web một trang (SPA) viết bằng React 19 và Vite (Hình 4.1-4.4) đáp ứng cả ba chức năng CN01-CN03. Màn hình nhập nhu cầu có thanh nạp nhanh 14 kịch bản và ô gợi ý trọng số theo mục tiêu học tập (CN01). Màn hình kết quả hiện Top-$k$ gia sư kèm thanh xếp chồng phân rã đóng góp $C_i$ và lý do gợi ý (CN02), cùng khung chọn mức ưu tiên để xem thứ hạng đổi ngay lập tức (CN03). Hiện giao diện mới phục vụ tra cứu một chiều và mới được kiểm tra tĩnh bằng `oxlint`, chưa có bộ kiểm thử giao diện tự động hay các chức năng tài khoản, đặt lịch và đánh giá sau buổi học.
4. **Đánh giá chất lượng xếp hạng trên bộ kịch bản thực nghiệm.** Bộ 14 kịch bản cố định KB01-KB14 được kiểm thử tự động trên 16 hồ sơ mẫu. Kết quả trùng khớp 14/14 (100%) so với Top-3 kỳ vọng (Bảng 5.3, Bảng 5.4), trong đó hai trường hợp chênh lệch điểm so với bảng tính tay ban đầu (KB04, KB09) và hai trường hợp đồng điểm phá hòa theo mã hồ sơ (KB02, KB12) đều đã được kiểm chứng rõ. Khi khảo sát độ nhạy theo bốn yếu tố ($\delta$, $E_{\max}$, ngân sách và bộ mức ưu tiên ở Bảng 5.5-5.8), các hàm giữ đúng tính đơn điệu và trọng số điều hướng được thứ hạng. Tuy nhiên, Top-3 kỳ vọng do nhóm thực hiện lập sẵn theo phân tích nghiệp vụ. Vì vậy kết quả 14/14 mới cho thấy mã nguồn chạy đúng với công thức, chứ chưa phản ánh mức độ hài lòng của học sinh và phụ huynh thực tế.

### 6.1.2. Kết quả mở rộng: Gợi ý mức ưu tiên theo mục tiêu học tập

Trong lúc làm đồ án, giảng viên hướng dẫn (TS. Lê Anh Nhã Uyên) góp ý nên mở rộng mô hình nhu cầu theo bộ ba *(Môn học, Cấp lớp, Mục tiêu học tập)* thay vì chỉ chọn tên môn học. Hai phương án mở rộng đã được khảo sát và Phương án 1 được cài đặt ngay:

- **Phương án 1 (PA1 - Ánh xạ mục tiêu học tập sang bộ mức ưu tiên khởi tạo - đã cài đặt).** Ở màn hình nhập nhu cầu (Hình 4.1), hệ thống bổ sung ô “Mục tiêu học tập (gợi ý mức ưu tiên)”. Ô này có ba lựa chọn mẫu (*preset*):
  1. *Không nêu mục tiêu:* giữ cả năm tiêu chí ở mức Trung bình ($w_i = 2$).
  2. *Điểm cao / luyện thi chuyên - học sinh giỏi:* nâng Kinh nghiệm và Đánh giá lên mức Cao ($w_i = 3$), ba tiêu chí còn lại giữ Trung bình ($w_i = 2$).
  3. *Đủ điểm đậu / lấy lại kiến thức căn bản:* nâng Học phí lên mức Cao ($w_i = 3$), bốn tiêu chí còn lại giữ Trung bình ($w_i = 2$).

  Sau khi chọn một gợi ý, người học vẫn chỉnh tay từng tiêu chí được; lúc đó ô mục tiêu tự chuyển sang “Tùy chỉnh”. Ba bộ cấu hình được thử nghiệm trên 19 truy vấn, gồm 14 kịch bản KB01-KB14 và 5 truy vấn bổ sung TQ1-TQ5 (TQ1: Toán, trực tiếp Bình Thạnh, ngân sách 250.000 VNĐ; TQ2: Toán, trực tiếp Gò Vấp, 150.000 VNĐ; TQ3: Toán, trực tuyến, 300.000 VNĐ, lịch T2-tối & T4-tối; TQ4: Lý, trực tiếp Thủ Đức, 180.000 VNĐ; TQ5: Hóa, trực tiếp Quận 10, 220.000 VNĐ, lịch T7-sáng). Kết quả cho thấy 3/19 trường hợp đổi thứ hạng ở vị trí 2-3 (gồm KB10 và 2/5 truy vấn bổ sung TQ1, TQ2), còn hạng 1 không đổi (0/19). Về phương pháp luận, cần lưu ý rằng kịch bản KB10 nguyên bản đặt tiêu chí Kinh nghiệm ở mức Cao ($w = 3$), nên việc áp preset *Không nêu mục tiêu* (cả 5 tiêu chí $w_i = 2$) sẽ ghi đè mức ưu tiên gốc của kịch bản này; ngoài ra, ba bộ trọng số PA1 đều là cấu hình khởi tạo theo phán đoán nghiệp vụ của nhóm thực hiện, chưa phải trọng số học từ dữ liệu tương tác.
- **Phương án 2 (Đưa Cấp lớp và độ hợp mục tiêu vào hàm điểm - để mở rộng sau).** Hồ sơ gia sư hiện tại (`TutorProfile`, Bảng 3.3) chỉ có 9 thuộc tính cơ bản. Hệ thống chưa có dữ liệu thật về cấp lớp nhận dạy, bằng cấp hay thế mạnh giảng dạy. Vì vậy, Phương án 2 được đề xuất cho hướng phát triển tiếp theo ở Mục 6.2.3.

### 6.1.3. Môi trường triển khai thực tế

Hệ thống đã được triển khai trực tuyến để truy cập và thử nghiệm trực tiếp (Mục 4.6.3):
- **Giao diện người dùng (Frontend):** chạy trên Vercel tại `https://tutor-recommender.vercel.app`.
- **Dịch vụ khuyến nghị (Backend API):** chạy trên Render tại `https://tutor-recommender-api.onrender.com`, kèm Swagger UI tại `https://tutor-recommender-api.onrender.com/docs` và đường dẫn `/health`.
- **Kho mã nguồn (GitHub):** `https://github.com/tnduckhmt2411011-design/tutor-recommender`.

Khi hoàn thành báo cáo này, cả giao diện lẫn API đều chạy bình thường và trả về mã trạng thái HTTP 200 OK.

## 6.2. Hạn chế và hướng phát triển

### 6.2.1. Tóm tắt các hạn chế kỹ thuật

Từ sáu hạn chế đã phân tích ở Mục 5.3, các vấn đề tồn tại được tổng hợp thành bốn nhóm chính:
1. Bộ dữ liệu mẫu còn nhỏ (16 hồ sơ, trong đó 2 hồ sơ công khai phải ước tính học phí và lịch rảnh) và 14 kịch bản do nhóm thực hiện tự xây dựng.
2. Các tham số $\delta = 0{,}5$, $E_{\max} = 8$, điểm trung tính $0{,}5$ cùng thang trọng số $\{0, 1, 2, 3\}$ đều đặt tay ban đầu.
3. Hệ thống chưa có dữ liệu tương tác lịch sử và chưa khảo sát người học thật bên ngoài.
4. Khu vực mới so khớp đúng tên quận/huyện quy ước, mỗi lần tìm một môn, và chưa đo độ trễ mạng thật qua Internet.

### 6.2.2. Hướng phát triển

Nếu tiếp tục phát triển thành đồ án tốt nghiệp, nhóm thực hiện dự kiến mở rộng theo ba hướng sau:

1. **Ghép vào nền tảng quản lý gia sư hoàn chỉnh:** nối bộ máy khuyến nghị với cơ sở dữ liệu quan hệ để quản lý tài khoản người học và xác minh gia sư. Hệ thống cũng cần thêm các bước đăng ký học thử, đặt lịch dạy và nhận đánh giá thật sau khóa học.
2. **Nâng cấp lên mô hình khuyến nghị lai (*Hybrid Recommender System*):** khi đã tích lũy đủ lịch sử tìm kiếm và chọn gia sư, có thể tạo ma trận tương tác người dùng - gia sư (*User-Item Interaction Matrix*). Kết hợp lọc cộng tác (*Collaborative Filtering*) với lọc theo đặc trưng hồ sơ hiện tại sẽ vừa gợi ý được cho gia sư mới (*cold-start*), vừa tận dụng được xu hướng lựa chọn từ cộng đồng người học [2], [6].
3. **Học trọng số tự động bằng Learning-to-Rank (LTR):** thay các tham số và bảng trọng số đặt tay bằng mô hình học máy có giám sát [7]. Mô hình này tự chỉnh trọng số dựa trên phản hồi ngầm (lượt xem, lưu hồ sơ) và phản hồi trực tiếp (đánh giá sau buổi học).

### 6.2.3. Đề xuất mở rộng mô hình theo cấp lớp và mục tiêu học tập

Tiếp nối Phương án 1 ở Mục 6.1.2, việc đưa bộ ba *(Môn học, Cấp lớp, Mục tiêu học tập)* vào dữ liệu và công thức được thực hiện qua hai bước:
- Bổ sung vào hồ sơ `TutorProfile` ba nhóm thông tin mới: cấp lớp nhận dạy (Tiểu học, THCS, THPT, Luyện thi đại học), trình độ (Giảng viên, Thạc sĩ, Cử nhân, Sinh viên sư phạm) và thế mạnh sư phạm. Thế mạnh này gồm luyện thi chuyên sâu, lấy lại kiến thức căn bản hoặc bồi dưỡng học sinh giỏi.
- Khi có đủ dữ liệu thật cho các trường mới, thêm bước lọc bắt buộc theo cấp lớp. Đồng thời đưa tiêu chí thứ sáu đo độ khớp giữa mục tiêu người học với thế mạnh gia sư vào công thức Weighted Scoring (2.1).

## 6.3. Tự đánh giá và phân công công việc

### 6.3.1. Phân công công việc

Bảng 6.1 ghi lại công việc phụ trách và mức độ hoàn thành của từng thành viên qua 6 Sprint.

**Bảng 6.1: Phân công công việc và mức độ hoàn thành của các thành viên trong nhóm**

| STT | Thành viên | Mã sinh viên | Công việc phụ trách | Quỹ giờ | Mức độ hoàn thành |
|:---:|:---|:---:|:---|---:|:---:|
| 1 | **Lê Thị Bích Chuyền** | KHMT2411037 | **Scrum Master các Sprint 2, 4, 6 kiêm Developer:** Điều phối quy trình Scrum ở các Sprint chẵn; phát triển giao diện React (Vite), tích hợp API và kiểm thử trải nghiệm người dùng; tham gia thiết kế dữ liệu và biên soạn báo cáo. | 100 giờ | Hoàn thành |
| 2 | **Trần Nguyễn Đức** | KHMT2411011 | **Scrum Master các Sprint 1, 3, 5 kiêm Developer:** Điều phối quy trình Scrum ở các Sprint lẻ, trao đổi chuyên môn với GVHD (TS. Lê Anh Nhã Uyên) và quản lý nhánh mã nguồn trên GitHub; phát triển lõi tính điểm backend FastAPI, thuật toán xếp hạng, bộ kiểm thử tự động và tham gia biên soạn báo cáo. | 100 giờ | Hoàn thành |
| 3 | **Cao Khánh Ngọc** | KHMT2411025 | **Product Owner kiêm Developer:** Phụ trách yêu cầu nghiệp vụ, quản lý Product Backlog và nghiệm thu sản phẩm theo tiêu chí hoàn thành; tham gia thiết kế dữ liệu, kiểm thử kịch bản và biên soạn báo cáo. | 100 giờ | Hoàn thành |
| | **Tổng cộng** | | **6 Sprint (3 thành viên × 100 giờ theo định mức Bảng 1.2)** | **300 giờ** | **Hoàn thành 100%** |

*(Phân công nhiệm vụ và mức độ hoàn thành do các thành viên trong nhóm thống nhất tự đánh giá qua 6 Sprint thực hiện đồ án.)*

### 6.3.2. Tự đánh giá kết quả thực hiện

Nhìn lại toàn bộ quá trình phát triển đồ án, nhóm thực hiện tự đánh giá kết quả trên bốn mặt:
- **Mức độ hoàn thành:** làm đủ các phần theo mục tiêu ở Mục 1.4, gồm module tính điểm, RESTful API, giao diện hai màn hình và bản chạy trực tuyến trên Vercel, Render.
- **Kiểm thử tự động:** đạt 200/200 bài kiểm thử (độ bao phủ câu lệnh 97%, tương ứng 340/351 câu lệnh trên `backend/app/`); cả 14/14 kịch bản thực nghiệm đều khớp Top-3 kỳ vọng (Bảng 5.3).
- **Toàn vẹn dữ liệu:** 16 hồ sơ mẫu trong `data/processed/tutors.json` và `data/processed/tutors.csv` qua đủ các phép kiểm tra định dạng, ẩn danh và đối chiếu từng ô (Mục 4.2.4, Phụ lục A).
- **Điểm cần cải thiện:** phần frontend chưa có bộ kiểm thử tự động trên CI, và tập 16 hồ sơ mới đủ để kiểm chứng thuật toán chứ chưa phản ánh dữ liệu thị trường lớn.

# PHỤ LỤC

## Phụ lục A. Bộ dữ liệu mẫu

### A.1. Cấu trúc tệp và quy trình xử lý dữ liệu gia sư

Nhóm thực hiện khảo sát và thu thập thủ công 15 hồ sơ gia sư ban đầu từ hai trang công khai tại Việt Nam là `giasudatviet.com` và `giasudantri.vn`. Sau khi lọc trùng và rà soát địa bàn, còn 11 hồ sơ dạy ở Thành phố Hồ Chí Minh.

Thực tế là cả hai trang trên đều không ghi đủ cùng lúc học phí theo giờ, lịch rảnh chi tiết trong tuần và điểm đánh giá trung bình. Do đó, nếu đưa toàn bộ 11 hồ sơ vào tập dữ liệu sẽ phải ước tính hàng loạt trường còn khuyết; để thử nghiệm thuật toán một cách minh bạch và giữ kín danh tính gia sư, bộ dữ liệu mẫu được chuẩn hóa theo các quy tắc sau:
- Chọn giữ lại 2 hồ sơ tiêu biểu có thông tin môn dạy, khu vực và số năm kinh nghiệm rõ ràng (`GS-T06` và `GS-T07`, nhãn `public_collected` - hiển thị là “Thu thập công khai” trong Bảng A.1) sau khi xóa toàn bộ thông tin liên hệ cá nhân (dữ liệu thô không đưa vào kho mã nguồn).
- Học phí theo giờ của hai hồ sơ này được ước tính trong khoảng 130.000-400.000 VNĐ/giờ dựa theo mặt bằng giá trên `daythem.com` và nội suy theo số năm kinh nghiệm; lịch rảnh ước tính theo các ca học phổ biến. Cả hai mục ước tính đều đánh dấu `(*)` ở Bảng A.1. Điểm đánh giá trung bình để trống (`null`) và nhận giá trị trung tính $0{,}5$ khi chấm điểm.
- 14 hồ sơ còn lại (`GS006`, `GS020`, `GS-G01` đến `GS-G12`, nhãn `simulated` - hiển thị là “Giả lập” trong Bảng A.1) là dữ liệu mô phỏng. Các hồ sơ này được tạo lập có chủ đích để thử nghiệm đầy đủ các ca biên, trường hợp `no_match`, học trực tuyến và cặp hồ sơ bằng điểm.
- Tên môn học được chuẩn hóa thống nhất trên cả 16 hồ sơ: tiếng Anh ghi `"Anh Văn"`, riêng `"Anh Văn GT"` ở hồ sơ `GS-T07` là viết tắt của tiếng Anh giao tiếp.

### A.2. Danh sách 16 hồ sơ gia sư mẫu và kiểm tra toàn vẹn

Bảng A.1 liệt kê đủ 16 hồ sơ gia sư mẫu theo thứ tự trong tệp dữ liệu chuẩn hóa, kèm nhãn nguồn dữ liệu và dấu `(*)` cho các thông tin ước tính của `GS-T06`, `GS-T07`.

**Bảng A.1: Danh sách 16 hồ sơ gia sư mẫu**

| STT | Mã gia sư | Môn dạy | Khu vực | Học phí (VNĐ/giờ) | Số năm KN | Hình thức dạy | Lịch rảnh | Đánh giá TB | Nguồn dữ liệu |
|:---:|:---|:---|:---|:---:|:---:|:---:|:---|:---:|:---|
| 1 | GS-T06 | Toán, Lý, Hóa | Bình Thạnh, Gò Vấp, Phú Nhuận, Tân Bình, Tân Phú | 400.000 (*) | 20 | Trực tiếp | T2-tối, T4-tối, T6-tối (*) | để trống | Thu thập công khai |
| 2 | GS-T07 | Anh Văn, Anh Văn GT | Bình Chánh, Nhà Bè, Quận 7, Quận 8 | 190.000 (*) | 6 | Trực tiếp | T3-tối, T5-tối, T7-sáng (*) | để trống | Thu thập công khai |
| 3 | GS006 | Lý, Hóa | để trống | 190.000 | 5 | Trực tuyến | T2-tối, T3-tối, T4-tối, T5-tối | 4,6 | Giả lập |
| 4 | GS020 | Lý, Hóa | để trống | 240.000 | 5 | Trực tuyến | T2-tối, T3-tối, T4-tối, T5-tối | 4,6 | Giả lập |
| 5 | GS-G01 | Toán | Bình Thạnh | 180.000 | 6 | Cả hai | T2-tối, T4-tối, T7-sáng | 5,0 | Giả lập |
| 6 | GS-G02 | Toán | Bình Thạnh | 300.000 | 3 | Cả hai | T2-tối, T4-tối, T7-sáng | 3,0 | Giả lập |
| 7 | GS-G03 | Anh Văn | Gò Vấp | 200.000 | 4 | Trực tuyến | T3-sáng, T5-sáng | 4,5 | Giả lập |
| 8 | GS-G04 | Văn | Quận 1, Quận 3 | 170.000 | 7 | Trực tiếp | T2-chiều, T5-chiều | 4,3 | Giả lập |
| 9 | GS-G05 | Sinh | Thủ Đức, Quận 9 | 190.000 | 4 | Cả hai | T3-tối, T6-tối | 4,0 | Giả lập |
| 10 | GS-G06 | Hóa | Quận 10, Quận 11 | 210.000 | 8 | Trực tiếp | T4-sáng, T7-sáng | 4,7 | Giả lập |
| 11 | GS-G07 | Tin học | Bình Thạnh, Thủ Đức | 220.000 | 5 | Trực tuyến | T2-tối, T4-tối, T6-tối | 4,4 | Giả lập |
| 12 | GS-G08 | Tiếng Nhật | Phú Nhuận, Tân Bình | 260.000 | 6 | Cả hai | T3-chiều, T5-chiều | 4,8 | Giả lập |
| 13 | GS-G09 | Toán | Quận 7 | 350.000 | 2 | Trực tiếp | T2-tối, T4-tối | 3,5 | Giả lập |
| 14 | GS-G10 | Toán | Quận 7 | 130.000 | 12 | Trực tiếp | T2-tối, T4-tối | 4,9 | Giả lập |
| 15 | GS-G11 | Anh Văn | Quận 2, Bình Thạnh | 200.000 | 5 | Trực tiếp | T3-sáng, T6-sáng | 4,5 | Giả lập |
| 16 | GS-G12 | Anh Văn | Quận 2, Thủ Đức | 200.000 | 5 | Trực tiếp | T3-sáng, T6-sáng | 4,5 | Giả lập |

*(Trong Bảng A.1, “Số năm KN” là số năm kinh nghiệm giảng dạy, “Đánh giá TB” là điểm đánh giá trung bình trên thang 5, “Anh Văn GT” là tiếng Anh giao tiếp; dấu `(*)` chỉ học phí và lịch rảnh ước tính của `GS-T06` và `GS-T07`. Điểm đánh giá để trống nhận giá trị trung tính $0{,}5$.)*

**Danh mục khu vực quy ước và kiểm tra toàn vẹn dữ liệu.** Danh mục quận/huyện trong `data/processed/tutors.json` khớp hoàn toàn với biến `DISTRICT_OPTIONS` trên giao diện (`frontend/src/services/api.js`). Bộ dữ liệu giữ tách riêng Quận 2, Quận 9 và Thủ Đức theo địa giới quen thuộc tại Thành phố Hồ Chí Minh để phục vụ kịch bản KB02, KB03 và KB07. Danh sách 16 khu vực gồm: Bình Chánh, Bình Thạnh, Gò Vấp, Nhà Bè, Phú Nhuận, Quận 1, Quận 2, Quận 3, Quận 7, Quận 8, Quận 9, Quận 10, Quận 11, Tân Bình, Tân Phú, Thủ Đức.

Lệnh kiểm tra toàn vẹn bộ dữ liệu:

```powershell
python scripts/validate_tutors.py
```

Kết quả thực thi:

```text
ĐẠT: 16 bản ghi (2 public_collected, 14 simulated); id duy nhất; enum hợp lệ;
     đủ 9 trường; không có thông tin liên hệ; JSON và CSV khớp nhau từng ô.
```

**Ghi chú nguồn Phụ lục A:** `data/processed/tutors.json`, `data/processed/tutors.csv`, `scripts/validate_tutors.py`, `frontend/src/data/tutorsCatalog.js`.

## Phụ lục B. Module tính điểm và xếp hạng

### B.1. Cấu trúc mã nguồn bộ chấm điểm

Bảng B.1 liệt kê các tệp mã nguồn, lớp và hàm chính trong `backend/app/`, gắn với từng bước xử lý ở Mục 3.6.

**Bảng B.1: Danh mục tệp mã nguồn và hàm nghiệp vụ trong module gợi ý gia sư**

| STT | Tệp mã nguồn | Lớp / Hàm chính | Vai trò kỹ thuật | Bước tương ứng trong Mục 3.6 |
|:---:|:---|:---|:---|:---|
| 1 | `backend/app/core/config.py` | Hằng số: `DELTA = 0.5`, `E_MAX = 8`, `RATING_DEFAULT = 0.5`, `PRIORITY_WEIGHTS`, `CRITERIA_KEYS` | Quản lý tham số thuật toán khởi tạo, bảng quy đổi mức ưu tiên sang trọng số nguyên và các khóa tiêu chí dùng chung. | Khởi tạo tham số và bảng quy đổi trọng số (Mục 3.6, Bảng 3.5, Bảng 3.6) |
| 2 | `backend/app/data/repository.py` | Lớp `TutorRepository` (`get_all()`), `TutorDataError` | Đọc dữ liệu từ `data/processed/tutors.json`, kiểm tra toàn vẹn và cung cấp danh sách hồ sơ cho quy trình tính điểm. | Cung cấp dữ liệu hồ sơ gia sư đầu vào |
| 3 | `backend/app/schemas/tutor.py` | Lớp Pydantic `TutorProfile` | Định nghĩa cấu trúc và kiểm tra hợp lệ kiểu dữ liệu cho 9 trường hồ sơ gia sư (`extra="forbid"`). | Cấu trúc dữ liệu đặc trưng hồ sơ gia sư |
| 4 | `backend/app/schemas/search_request.py` | Lớp Pydantic `SearchRequest`, hàm `default_priorities()` | Định nghĩa cấu trúc truy vấn tìm kiếm của người học (7 trường), xác thực dữ liệu đầu vào và gán mức ưu tiên mặc định. | Bước 1: Kiểm tra và chuẩn hóa yêu cầu tìm kiếm đầu vào |
| 5 | `backend/app/scoring/filters.py` | Hàm `filter_mandatory()`, `_matches_subject()`, `_matches_mode()`, `_matches_availability()` | Lọc danh sách gia sư theo các ràng buộc cứng: môn dạy, hình thức dạy/học và điều kiện trùng lịch tối thiểu ($\lvert L \cap T \rvert \ge 1$). | Bước 2: Lọc điều kiện bắt buộc (Bảng 3.2) |
| 6 | `backend/app/scoring/weights.py` | Lớp `EffectiveWeights`, hàm `compute_effective_weights()`, `priority_to_weight()`, `_applicable_criteria()` | Xác định tập tiêu chí ưu tiên áp dụng theo đầu vào và tính bộ trọng số hiệu dụng $w_i$; loại các tiêu chí có $w_i = 0$ khỏi tập trọng số dương. | Xác định tiêu chí áp dụng và tính trọng số hiệu dụng |
| 7 | `backend/app/scoring/eligibility.py` | Hàm `filter_eligible_candidates()`, `check_tutor_eligibility()`, `count_available_criteria()`, `get_min_required_criteria()` | Tính số tiêu chí ưu tiên có hiệu lực $n$ ($w_i > 0$, không tính Đánh giá), đếm số tiêu chí có dữ liệu của gia sư và lọc theo bảng ngưỡng tối thiểu. | Điều kiện đủ dữ liệu để xếp hạng (Bảng 3.7) |
| 8 | `backend/app/scoring/criteria.py` | `score_fee()`, `score_location()`, `score_experience()`, `score_rating()`, `score_schedule()` | Hiện thực 5 công thức tính điểm thành phần $s_i \in [0, 1]$ cho học phí, khu vực, kinh nghiệm, đánh giá và lịch rảnh. | Bước 3: Tính điểm thành phần $s_i$ (Bảng 3.6) |
| 9 | `backend/app/scoring/ranker.py` | `score_and_rank()`, `_compute_single_criterion_score()`, `build_reason()`, `build_notes()` | Tổng hợp điểm Weighted Scoring $S(g) = \sum_{i \in A} (w_i \cdot s_i) / \sum_{j \in A} w_j$, sắp xếp giảm dần, xử lý đồng điểm theo `tutor_id`, trích xuất điểm đóng góp và lý do khuyến nghị. | Bước 4: Tổng hợp điểm Weighted Scoring và xếp hạng |
| 10 | `backend/app/schemas/recommendation.py` | `RankedTutor`, `RecommendationSuccessResponse`, `NoMatchResponse`, `ZeroWeightResponse` | Định nghĩa cấu trúc phản hồi JSON cho các trạng thái `success`, `no_match` và `zero_weight`. | Định dạng cấu trúc dữ liệu phản hồi |
| 11 | `backend/app/api/recommend.py` | Điểm cuối `recommend_tutors()`, phụ trợ `get_tutor_repository()` | Tiếp nhận yêu cầu `POST /api/recommend`, điều phối chuỗi hàm tính điểm và trả kết quả chuẩn hóa. | Điều phối toàn bộ quy trình qua dịch vụ API FastAPI |
| 12 | `backend/app/main.py` | Ứng dụng `app`, `health_check()` (cấu hình `CORSMiddleware`) | Điểm khởi chạy FastAPI, cấu hình CORS, gắn kết router khuyến nghị và cung cấp điểm cuối `/health`. | Khởi tạo và phục vụ dịch vụ RESTful API (Mục 3.7.2, Mục 4.4.1) |

### B.2. Hàm chấm điểm tổng hợp và kiểm tra ràng buộc

Các hàm tính điểm trong `backend/app/scoring/criteria.py` đều viết dạng hàm thuần (*pure functions*), tách hẳn khỏi FastAPI. Khi nhận yêu cầu tại `backend/app/api/recommend.py`, API chạy lần lượt năm bước:
1. Kiểm tra tính hợp lệ của `SearchRequest`.
2. Lọc điều kiện bắt buộc qua `filter_mandatory`, trả `no_match` nếu không còn ứng viên nào.
3. Tính trọng số hiệu dụng qua `compute_effective_weights`, trả `zero_weight` nếu $\sum w_i = 0$.
4. Kiểm tra ngưỡng dữ liệu qua `filter_eligible_candidates`, trả `no_match` kèm `insufficient_data_candidates` nếu không hồ sơ nào đủ dữ liệu.
5. Chấm điểm và xếp hạng qua `score_and_rank` (giảm dần theo điểm, tăng dần theo mã gia sư).

**Ghi chú nguồn Phụ lục B:** `backend/app/core/config.py`, `backend/app/data/repository.py`, `backend/app/schemas/`, `backend/app/scoring/`, `backend/app/api/recommend.py`, `backend/app/main.py`.

## Phụ lục C. Danh mục sơ đồ thiết kế và hình ảnh giao diện

### C.1. Hệ thống sơ đồ thiết kế và hình ảnh giao diện chính thức

Chín sơ đồ và ảnh chụp giao diện chính thức trong báo cáo được lưu tại `docs/thesis/figures/` và tổng hợp ở Bảng C.1.

**Bảng C.1: Danh mục sơ đồ thiết kế và hình ảnh giao diện của hệ thống**

| STT | Số hiệu hình | Tệp hình ảnh (`docs/thesis/figures/`) | Nội dung và chức năng thể hiện | Mục tham chiếu |
|:---:|:---:|:---|:---|:---:|
| 1 | Hình 3.1 | `hinh-3-1-luong-xu-ly-khuyen-nghi.png` | Sơ đồ luồng xử lý khuyến nghị 8 bước theo chuẩn ISO 5807, thể hiện kiểm tra $\sum w_i > 0$, ngưỡng dữ liệu tối thiểu và các nhánh phản hồi biên. | Mục 3.7.1 |
| 2 | Hình 3.2 | `hinh-3-2-kien-truc-ba-lop.png` | Sơ đồ kiến trúc ba lớp tách biệt giữa Giao diện (React), Dịch vụ API (FastAPI) và Module tính điểm (`scoring`). | Mục 3.7.2 |
| 3 | Hình 3.3 | `hinh-3-3-so-do-trinh-tu.png` | Sơ đồ trình tự UML 2.5 mô tả tương tác giữa người học, giao diện React, tầng API FastAPI, `TutorRepository` và gói hàm tính điểm. | Mục 3.7.2 |
| 4 | Hình 3.4 | `hinh-3-4-phac-thao-nhap-nhu-cau.png` | Phác thảo bố cục (*wireframe*) màn hình nhập nhu cầu tìm kiếm và chọn mức ưu tiên (CN01). | Mục 3.8 |
| 5 | Hình 3.5 | `hinh-3-5-phac-thao-ket-qua.png` | Phác thảo bố cục (*wireframe*) màn hình kết quả gợi ý kèm thanh xếp chồng và khung điều chỉnh trọng số (CN02, CN03). | Mục 3.8 |
| 6 | Hình 4.1 | `hinh-ui-01-cn01-nhap-nhu-cau.png` | Giao diện thực tế màn hình nhập nhu cầu (CN01), thanh nạp nhanh 14 kịch bản và ô chọn “Mục tiêu học tập”. | Mục 4.5 |
| 7 | Hình 4.2 | `hinh-ui-02-cn02-ket-qua-kb01.png` | Giao diện thực tế màn hình kết quả Top-3 kịch bản KB01 (CN02) kèm thanh xếp chồng phân rã điểm đóng góp $C_i$ và lý do khuyến nghị. | Mục 4.5 |
| 8 | Hình 4.3 | `hinh-ui-03-cn03-dieu-chinh-uu-tien.png` | Giao diện điều chỉnh mức ưu tiên trực tiếp (CN03) làm thay đổi thứ hạng (`GS-G10` lên hạng 1 kèm huy hiệu tăng bậc). | Mục 4.5 |
| 9 | Hình 4.4 | `hinh-ui-04-zero-weight.png` | Giao diện cảnh báo trạng thái biên khi tổng trọng số bằng 0 ($\sum w_i = 0$, trạng thái `zero_weight`) kèm nút khôi phục mặc định. | Mục 4.5 |

### C.2. Đối chiếu giữa bản phác thảo thiết kế và giao diện hiện thực

Bốn ảnh chụp giao diện ở Chương 4 (Hình 4.1-4.4) đi từ hai bản phác thảo Hình 3.4 và Hình 3.5, có thêm ba tiện ích phục vụ minh họa và kiểm tra:
1. **Thanh nạp nhanh 14 kịch bản (Hình 4.1):** giúp nạp nhanh đầu vào của KB01-KB14 (Bảng 5.3) để thử trực tiếp trên trình duyệt.
2. **Ô chọn mục tiêu học tập (Hình 4.1):** gợi ý sẵn bộ 5 mức ưu tiên theo Phương án 1 (Mục 6.1.2).
3. **Hiển thị biến động hạng và trạng thái biên (Hình 4.2-4.4):** hiện số lượng ứng viên qua từng bước lọc (“Kho: 16 hồ sơ → Hợp lệ: 5 ứng viên → Top-3: 3 gợi ý”). Khi người học chỉnh mức ưu tiên (CN03), thẻ gia sư hiện huy hiệu tăng/giảm hạng, còn trường hợp $\sum w_i = 0$ sẽ chuyển sang màn hình cảnh báo trạng thái biên.

Ngoài giao diện React, backend còn mở sẵn trang Swagger UI tại `/docs` để gửi thử trực tiếp `POST /api/recommend`.

**Ghi chú nguồn Phụ lục C:** `docs/thesis/figures/`, `frontend/src/pages/`, `frontend/src/components/`.

## Phụ lục D. Kịch bản kiểm thử thực nghiệm

### D.1. Danh mục 14 kịch bản kiểm thử thực nghiệm

Bảng D.1 tổng hợp đầy đủ tham số đầu vào và Top-3 kỳ vọng của 14 kịch bản KB01-KB14, lấy từ `backend/tests/scenarios/scenarios.json`.

**Bảng D.1: Yêu cầu đầy đủ của 14 kịch bản thực nghiệm**

| Mã KB | Môn | Hình thức | Khu vực | Ngân sách (VNĐ/giờ) | Khung giờ | Mức ưu tiên khác mặc định | Top-3 kỳ vọng |
|:---:|:---|:---|:---|:---:|:---|:---|:---|
| KB01 | Toán | Trực tiếp | Bình Thạnh | 200.000 | Không nhập | Mặc định (đều $w = 2$) | GS-G01, GS-G10, GS-T06 |
| KB02 | Anh Văn | Trực tiếp | Quận 2 | 220.000 | Không nhập | Mặc định (đều $w = 2$) | GS-G11, GS-G12, GS-T07 |
| KB03 | Anh Văn | Trực tiếp | Thủ Đức | 220.000 | Không nhập | Mặc định (đều $w = 2$) | GS-G12, GS-G11, GS-T07 |
| KB04 | Lý | Trực tuyến | Không nhập | 200.000 | T2-tối, T4-tối | Mặc định (đều $w = 2$) | GS006, GS020 |
| KB05 | Tiếng Trung | Bất kỳ (`any`) | Không nhập | Không nhập | Không nhập | Mặc định (đều $w = 2$) | Không có (0 kết quả) |
| KB06 | Văn | Trực tiếp | Quận 1 | 180.000 | Không nhập | Mặc định (đều $w = 2$) | GS-G04 |
| KB07 | Sinh | Bất kỳ (`any`) | Thủ Đức | 200.000 | Không nhập | Mặc định (đều $w = 2$) | GS-G05 |
| KB08 | Tin học | Trực tuyến | Không nhập | 250.000 | T2-tối, T6-tối | Mặc định (đều $w = 2$) | GS-G07 |
| KB09 | Tiếng Nhật | Bất kỳ (`any`) | Phú Nhuận | 280.000 | Không nhập | Mặc định (đều $w = 2$) | GS-G08 |
| KB10 | Toán | Trực tiếp | Quận 7 | Không nhập | Không nhập | Kinh nghiệm: Cao ($w = 3$) | GS-G10, GS-G01, GS-G09 |
| KB11 | Hóa | Trực tiếp | Quận 10 | 220.000 | Không nhập | Mặc định (đều $w = 2$) | GS-G06, GS-T06 |
| KB12 | Anh Văn | Trực tiếp | Bình Chánh | 200.000 | Không nhập | Mặc định (đều $w = 2$) | GS-T07, GS-G11, GS-G12 |
| KB13 | Toán | Bất kỳ (`any`) | Không nhập | 150.000 | Không nhập | Mặc định (đều $w = 2$) | GS-G10, GS-G01, GS-T06 |
| KB14 | Anh Văn | Trực tuyến | Không nhập | Không nhập | Không nhập | Mặc định (đều $w = 2$) | GS-G03 |

*(Các cột “Khu vực”, “Ngân sách (VNĐ/giờ)” và “Khung giờ” ghi “Không nhập” khi người học bỏ trống tiêu chí tùy chọn tương ứng; mức ưu tiên mặc định của cả 5 tiêu chí là Trung bình ($w_i = 2$). Danh sách Top-3 kỳ vọng có ít hơn 3 mã gia sư ở các kịch bản chỉ có 0-2 hồ sơ thỏa mãn điều kiện lọc bắt buộc.)*

### D.2. Quy trình tái lập kiểm thử và đo thời gian phản hồi

Để chạy lại các phép đo trong Chương 5 bằng trình thông dịch Python của môi trường ảo `backend/.venv`, thực hiện hai lệnh sau:
- **Chạy toàn bộ bộ kiểm thử và đo độ bao phủ (đứng tại thư mục `backend/`):** `pytest --cov=app --cov-report=term-missing -q` cho lại kết quả 200/200 bài đạt (độ bao phủ 97%, Bảng 5.1), bộ ca biên (Bảng 5.2) và kết quả 14 kịch bản (Bảng 5.3).
- **Đo thời gian xử lý nội tại (`TestClient`, đứng tại thư mục gốc kho mã nguồn):** `python scripts/thesis/benchmark_latency.py` chạy lại phép đo 140 lượt và 700 lượt gọi liên tiếp (Mục 5.1.2).

**Ghi chú nguồn Phụ lục D:** `backend/tests/scenarios/scenarios.json`, `backend/tests/scenarios/test_scenarios.py`, `backend/tests/api/test_boundary_muc_5_1.py`, `backend/tests/scenarios/test_sensitivity_muc_5_2.py`, `scripts/thesis/benchmark_latency.py`.
