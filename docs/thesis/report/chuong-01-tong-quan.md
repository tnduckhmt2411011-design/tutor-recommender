# CHƯƠNG 1. TỔNG QUAN VỀ ĐỀ TÀI

## 1.1. Lý do chọn đề tài

Học sinh và phụ huynh ngày càng có nhu cầu tìm gia sư theo môn học và mục tiêu riêng. Đây là bài toán thực tế của đề tài “Hệ thống khuyến nghị gia sư dựa trên phương pháp Content-Base Filtering” (giữ nguyên tên đề tài đã đăng ký *Content-Base Filtering* ở tên chính thức; trong nội dung học thuật sử dụng thuật ngữ chuẩn tiếng Anh là *Content-Based Filtering*). Khi chọn gia sư, người học (học sinh hoặc phụ huynh thay mặt học sinh) phải cân nhắc cùng lúc môn học, khu vực, học phí, hình thức học (trực tiếp hay trực tuyến) và khung thời gian rảnh. Số hồ sơ ít thì có thể tự đối chiếu. Danh sách càng dài thì việc duyệt từng hồ sơ để tìm phương án cân bằng giữa các tiêu chí càng tốn thời gian.

Lọc nhị phân theo từng tiêu chí riêng lẻ là chưa đủ. Điều người học cần là xếp hạng mức độ phù hợp tổng thể khi các tiêu chí xung đột nhau, đúng với bản chất của bài toán ra quyết định đa tiêu chí (*multi-criteria decision making*) [1]. Hệ thống phân chia các tiêu chí thành ba loại: điều kiện bắt buộc (như đúng môn cần học và hình thức dạy phù hợp), tiêu chí ưu tiên có trọng số (học phí, khu vực, kinh nghiệm, đánh giá, lịch rảnh) và tiêu chí tùy chọn. Tiêu chí tùy chọn thực chất là tiêu chí ưu tiên khi người học đặt trọng số $w_i = 0$ để bỏ qua khi xếp hạng. Trong số gia sư đã đạt điều kiện bắt buộc, người có học phí vượt nhẹ ngân sách nhưng giàu kinh nghiệm và điểm đánh giá cao vẫn có thể phù hợp hơn người học phí thấp nhưng ít kinh nghiệm. Vì vậy, đề tài xây dựng một hệ thống khuyến nghị có khả năng lọc điều kiện bắt buộc, chấm điểm phù hợp có trọng số, xếp hạng và giải thích trực quan cơ sở của thứ hạng cho người học.

## 1.2. Khảo sát hiện trạng

Qua khảo sát thực tế, người học hiện nay thường tìm gia sư qua ba kênh chính:

- Các hội nhóm mạng xã hội (Facebook, Zalo), nơi phụ huynh đăng yêu cầu và gia sư tự liên hệ.
- Các trung tâm gia sư truyền thống, nơi nhân viên tư vấn ghép nối thủ công dựa trên kinh nghiệm cá nhân.
- Các nền tảng kết nối gia sư trực tuyến, thường cung cấp bộ lọc cơ bản theo môn học hoặc khu vực.

Để đánh giá mức độ hỗ trợ tìm kiếm của các kênh trực tuyến, quá trình khảo sát trực tiếp ba nền tảng được tiến hành nhằm ghi nhận các tiêu chí lọc hiện có và khả năng xếp hạng tổng hợp nhiều tiêu chí. Kết quả được tổng hợp trong Bảng 1.1.

**Bảng 1.1: Khảo sát chức năng tìm kiếm của một số kênh/nền tảng**

| Kênh / nền tảng | Tiêu chí lọc được hỗ trợ | Có xếp hạng tổng hợp nhiều tiêu chí không? | Nguồn / ngày khảo sát |
|:---|:---|:---|:---|
| giasudatviet.com | Lọc theo môn qua URL riêng từng môn (ví dụ `/gia-su-mon-toan-1.html`); không có ô ngân sách/lịch rảnh trên trang này | Không rõ tiêu chí: danh sách “gia sư tiêu biểu” theo môn không tăng/giảm dần theo mã số, không theo thứ tự chữ cái, không có điểm hiển thị | https://giasudatviet.com/gia-su-mon-toan-1.html, truy cập 26/09/2026 |
| giasudantri.vn | Không có ô lọc: danh sách dạng bài viết giới thiệu từng gia sư, không phải cơ sở dữ liệu tìm kiếm được | Không: hiển thị theo thứ tự bài viết, một số hồ sơ có ghi mức lương/buổi ngay trong bài | https://giasudantri.vn/trung-tam-gia-su-online/, truy cập 26/09/2026 |
| daythem.com | Có bộ lọc “Ngành học”, “Môn học”, “Lịch biểu” (duy nhất trong 3 nền tảng có lọc theo lịch rảnh) | Không: mặc định sắp theo thời gian hoạt động gần nhất, không theo điểm phù hợp; không có lý do khuyến nghị | https://daythem.com/hoc-tai-nha/, truy cập 26/09/2026 |

Trong ba nền tảng được khảo sát, chưa nền tảng nào xếp hạng tổng hợp nhiều tiêu chí theo mức ưu tiên của người học. Đây là cơ sở để xác định khoảng trống chức năng ở Mục 1.3.

## 1.3. Vấn đề còn tồn tại và lý do chọn hướng tiếp cận

### 1.3.1. Khoảng trống chức năng mà đồ án lựa chọn giải quyết

Từ kết quả khảo sát, khoảng trống mà đề tài lựa chọn giải quyết nằm giữa bước “lọc theo tiêu chí” và bước “lựa chọn gia sư”. Sau khi lọc cơ bản, người học vẫn phải tự đọc và so sánh thủ công các hồ sơ còn lại. Đồ án giải quyết khoảng trống này bằng một bộ máy khuyến nghị (*recommendation engine*) có thể giải thích kết quả.

### 1.3.2. Lý do chọn hướng tiếp cận

Phương pháp khuyến nghị được lựa chọn dựa trên đặc điểm dữ liệu hiện có. Hệ thống của đồ án chưa vận hành thương mại, nên chưa có dữ liệu lịch sử tương tác như lịch sử ghép cặp, số buổi đã học hay đánh giá chéo giữa nhiều người dùng. Lọc cộng tác (*Collaborative Filtering*) suy diễn sở thích từ hành vi cộng đồng [2], nên chưa có dữ liệu đầu vào để chạy (Bảng 2.1). Ngược lại, có hai nguồn thông tin có thể thu thập hoặc mô phỏng có kiểm soát ngay từ đầu. Thứ nhất là hồ sơ thuộc tính của gia sư (môn dạy, khu vực, học phí, số năm kinh nghiệm, hình thức dạy, lịch rảnh, điểm đánh giá trung bình). Thứ hai là yêu cầu tìm kiếm do người học nhập trực tiếp lúc tra cứu. Điểm đánh giá trung bình ở đây chỉ là thuộc tính tĩnh trong bộ dữ liệu mẫu, không phải ma trận tương tác do hệ thống thu thập.

Vì vậy, đồ án áp dụng hướng lọc dựa trên nội dung (*Content-Based Filtering*) trên đặc trưng hồ sơ có cấu trúc, gồm hai giai đoạn. Giai đoạn đầu lọc điều kiện bắt buộc. Giai đoạn sau chấm điểm các tiêu chí ưu tiên rồi tổng hợp bằng phương pháp tính tổng có trọng số (*Weighted Scoring*). Cách này minh bạch và giải thích được từng kết quả xếp hạng, không phụ thuộc vào mô hình hộp đen. Chẳng hạn, người học có thể nâng mức ưu tiên khu vực khi cần gia sư dạy trực tiếp gần nhà. Cơ sở lý thuyết và thiết kế thuật toán được trình bày ở Chương 2 và Chương 3.

Ngoài ba nền tảng trên, nhóm thực hiện có tham khảo báo cáo đồ án cơ sở GS360 [3] (Lê Thị Hoài Thương và Lê Nguyễn Quang Minh, Trường Đại học Công nghệ Thông tin và Truyền thông Việt - Hàn, tháng 11/2024). GS360 là website quản lý toàn trình việc tìm và thuê gia sư, gồm đăng bài tìm gia sư, đặt lịch, thanh toán và đánh giá cho người tìm gia sư, gia sư và quản trị viên. Website này không có xếp hạng đa tiêu chí.

Điểm khác biệt của đồ án này là tập trung chuyên sâu vào bộ máy khuyến nghị. Hệ thống lọc các điều kiện bắt buộc gồm môn học, hình thức học và khung giờ giao nhau. Sau đó, mô hình chấm điểm năm tiêu chí ưu tiên theo Bảng 3.6, tổng hợp bằng Weighted Scoring và trả về Top-$k$ kèm điểm thành phần cùng mức đóng góp của từng tiêu chí. Vì vậy GS360 chỉ dùng để đối sánh phạm vi chức năng, không phải mốc đối chứng (*baseline*) về độ chính xác xếp hạng. Chất lượng xếp hạng của đồ án được kiểm định trên bộ 14 kịch bản thực nghiệm ở Bảng 5.3.

## 1.4. Mục tiêu và phạm vi đề tài

**Mục tiêu tổng quát.** Đề tài xây dựng và kiểm định một bộ máy khuyến nghị xếp hạng gia sư theo mức độ phù hợp giữa nhu cầu của người học và đặc trưng trong hồ sơ gia sư. Hệ thống kiểm tra điều kiện bắt buộc trước, sau đó chuẩn hóa các tiêu chí ưu tiên và tổng hợp thành điểm phù hợp có trọng số. Kết quả hiển thị kèm điểm thành phần và mức đóng góp, để người học hiểu vì sao gia sư đứng ở thứ hạng đó.

**Mục tiêu cụ thể.** Đồ án đặt ra bốn mục tiêu cụ thể:

- Mô hình hóa mức độ phù hợp: phân loại tiêu chí (điều kiện bắt buộc, tiêu chí ưu tiên có trọng số và tiêu chí tùy chọn với $w_i = 0$), thiết lập công thức chuẩn hóa điểm cho từng tiêu chí và xây dựng module lọc - tính điểm có trọng số.
- Xây dựng dịch vụ API khuyến nghị bằng FastAPI, nhận nhu cầu của người học và trả về danh sách gia sư đã xếp hạng kèm điểm thành phần và điểm đóng góp.
- Xây dựng giao diện minh họa bằng React, cho phép nhập nhu cầu, chọn mức ưu tiên và quan sát kết quả xếp hạng thay đổi.
- Đánh giá chất lượng xếp hạng bằng bộ kịch bản tìm gia sư có kết quả kỳ vọng xác định trước, kết hợp khảo sát độ nhạy tham số và ảnh hưởng của việc đổi mức ưu tiên đến thứ hạng.

**Phạm vi.** Đồ án cài đặt bộ máy khuyến nghị kèm giao diện minh họa hai màn hình, chạy trên tập dữ liệu gia sư mẫu. Phạm vi kỹ thuật giới hạn ở ba điểm: mỗi truy vấn chỉ tìm một môn học; khu vực so khớp theo danh mục quận/huyện quy ước chứ chưa tính khoảng cách địa lý; và hệ thống chỉ phục vụ một tác nhân là người học. Trong phạm vi học phần hai tín chỉ, đồ án chưa xây dựng các phân hệ quản trị, đăng ký tài khoản, đặt lịch - thanh toán hay đánh giá sau buổi học, và chưa thu thập dữ liệu tương tác vận hành ở quy mô lớn. Các hạng mục này thuộc hướng mở rộng ở Mục 6.2 khi phát triển thành hệ thống hoàn chỉnh hoặc đồ án tốt nghiệp.

## 1.5. Công cụ và kế hoạch thực hiện

Về công nghệ, dịch vụ xử lý phía máy chủ (backend) viết bằng FastAPI trên Python 3.12. Giao diện người dùng (frontend) xây dựng bằng React (Vite). Dữ liệu gia sư mẫu lưu ở định dạng JSON và CSV.

Quá trình phát triển áp dụng cách tiếp cận thiết kế đặc tả và kịch bản kiểm chứng trước khi lập trình. Quy trình bắt đầu từ việc xác định bài toán và mô hình điểm (Chương 3), rồi tạo bộ dữ liệu mẫu và kịch bản kiểm thử. Tiếp theo, hệ thống được hoàn thiện lần lượt từ module tính điểm, dịch vụ API đến giao diện minh họa. Cuối cùng là chạy thực nghiệm kiểm thử và đánh giá kết quả (Chương 4 và Chương 5). Thời gian dự kiến cho mỗi thành viên được chia theo từng hạng mục báo cáo ở Bảng 1.2, theo định mức học phần 2 tín chỉ (100 giờ/thành viên).

**Bảng 1.2: Phân bổ thời gian thực hiện theo chương**

| Hạng mục | Số giờ dự kiến (1 SV) | Tỷ lệ | Tổng nhóm (3 SV) |
|:---|---:|---:|---:|
| Chương 1 - Tổng quan về đề tài | 8 giờ | 8% | 24 giờ |
| Chương 2 - Cơ sở lý thuyết và công nghệ | 10 giờ | 10% | 30 giờ |
| Chương 3 - Phân tích và thiết kế hệ thống | 30 giờ | 30% | 90 giờ |
| Chương 4 - Xây dựng hệ thống | 30 giờ | 30% | 90 giờ |
| Chương 5 - Kiểm thử và đánh giá | 16 giờ | 16% | 48 giờ |
| Chương 6 - Kết luận và hướng phát triển | 6 giờ | 6% | 18 giờ |
| **Tổng cộng** | **100 giờ** | **100%** | **300 giờ** |

*(Định mức thời gian dự kiến 100 giờ cho mỗi thành viên theo quy mô học phần 2 tín chỉ; tổng quỹ thời gian của nhóm 3 thành viên là 300 giờ.)*

## 1.6. Cấu trúc báo cáo

Báo cáo gồm sáu chương và bốn phụ lục. Chương 1 nêu bối cảnh, khảo sát hiện trạng, lý do chọn hướng tiếp cận, mục tiêu và phạm vi. Chương 2 trình bày cơ sở lý thuyết về hệ thống khuyến nghị, phương pháp Content-Based Filtering trên dữ liệu hồ sơ có cấu trúc, mô hình Weighted Scoring, cùng các công nghệ cài đặt được lựa chọn (Mục 2.4). Chương 3 phân tích yêu cầu và thiết kế dữ liệu, công thức điểm thành phần, ngưỡng dữ liệu tối thiểu, kiến trúc ba lớp và giao diện. Chương 4 trình bày quá trình cài đặt hệ thống bằng FastAPI và React. Chương 5 trình bày kết quả kiểm thử tự động, đối chiếu 14 kịch bản thực nghiệm, khảo sát độ nhạy tham số và các hạn chế. Chương 6 tổng kết theo bốn mục tiêu, nêu hướng phát triển và bảng phân công công việc. Bốn phụ lục trình bày bộ dữ liệu mẫu 16 hồ sơ (Phụ lục A) và cấu trúc mã nguồn module tính điểm (Phụ lục B). Phụ lục C liệt kê các sơ đồ thiết kế và ảnh giao diện, còn Phụ lục D đặc tả 14 kịch bản thực nghiệm.
