# CHƯƠNG 1. TỔNG QUAN VỀ ĐỀ TÀI

Chương này xác lập bối cảnh và phạm vi của đề tài “Hệ thống khuyến nghị gia sư dựa trên phương pháp Content-Base Filtering”. Nội dung gồm lý do chọn đề tài (Mục 1.1), khảo sát hiện trạng các kênh tìm gia sư (Mục 1.2), khoảng trống chức năng và lý do chọn hướng tiếp cận (Mục 1.3), mục tiêu và phạm vi (Mục 1.4), cùng công cụ và kế hoạch thực hiện (Mục 1.5). Phạm vi và mục tiêu xác lập trong chương được hiện thực ở Chương 4; các số liệu kiểm chứng trình bày tại Chương 5.

---

## 1.1. Lý do chọn đề tài

Nghiên cứu tại Hồng Kông cho thấy việc thuê gia sư (*private supplementary tutoring*) là một hình thức giáo dục tư nhân có quy mô đáng kể, với nhu cầu học thêm phân hóa theo các yếu tố kinh tế – xã hội [1]. Khi chọn gia sư, người học (học sinh hoặc phụ huynh thay mặt học sinh) phải cân nhắc đồng thời nhiều tiêu chí: môn học, khu vực, học phí, hình thức học (trực tiếp hay trực tuyến) và thời gian học. Khi số hồ sơ gia sư ít, người học có thể tự so sánh. Khi số hồ sơ tăng lên, việc duyệt từng hồ sơ để tìm lựa chọn cân bằng giữa các tiêu chí trở nên tốn nhiều thời gian.

Vấn đề cốt lõi không chỉ là lọc đúng/sai theo từng tiêu chí riêng lẻ, mà là xếp hạng mức độ phù hợp tổng thể khi các tiêu chí xung đột nhau — đúng với bản chất của bài toán ra quyết định đa tiêu chí (*multi-criteria decision making*) [2]. Bài toán này gồm hai loại điều kiện: điều kiện bắt buộc (ví dụ gia sư phải dạy đúng môn cần học) và tiêu chí ưu tiên (ví dụ học phí, khu vực, kinh nghiệm). Trong tập gia sư đã đáp ứng điều kiện bắt buộc, một gia sư có học phí vượt nhẹ ngân sách nhưng giàu kinh nghiệm và có điểm đánh giá cao vẫn có thể đạt tổng điểm cao hơn một gia sư học phí thấp nhưng ít kinh nghiệm. Đây là động lực để xây dựng hệ thống khuyến nghị có khả năng kiểm tra điều kiện bắt buộc, tính điểm phù hợp, xếp hạng và giải thích thứ hạng cho người học, thay vì chỉ lọc nhị phân đúng/sai.

## 1.2. Khảo sát hiện trạng

Theo quan sát ban đầu của nhóm, người học hiện nay thường tiếp cận gia sư qua ba kênh:
- Các hội nhóm mạng xã hội (Facebook, Zalo), nơi phụ huynh đăng yêu cầu và gia sư tự liên hệ.
- Các trung tâm gia sư, nơi nhân viên tư vấn ghép gia sư theo kinh nghiệm cá nhân.
- Các nền tảng kết nối gia sư trực tuyến, thường cho phép lọc theo môn học hoặc khu vực.

Nhằm xác minh nhận định ban đầu này, nhóm đã kiểm tra trực tiếp ba nền tảng cụ thể để ghi nhận tiêu chí lọc được hỗ trợ và khả năng xếp hạng tổng hợp nhiều tiêu chí; kết quả tổng hợp tại Bảng 1.1.

**Bảng 1.1 - Khảo sát chức năng tìm kiếm của một số kênh/nền tảng**

| Kênh / nền tảng | Tiêu chí lọc được hỗ trợ | Có xếp hạng tổng hợp nhiều tiêu chí không? | Nguồn / ngày khảo sát |
|:---|:---|:---|:---|
| giasudatviet.com | Lọc theo môn qua URL riêng từng môn (ví dụ `/gia-su-mon-toan-1.html`); không có ô ngân sách/lịch rảnh trên trang này | Không rõ tiêu chí: danh sách “gia sư tiêu biểu” theo môn không tăng/giảm dần theo mã số, không theo thứ tự chữ cái, không có điểm hiển thị | https://giasudatviet.com/gia-su-mon-toan-1.html, truy cập 26/09/2026 |
| giasudantri.vn | Không có ô lọc: danh sách dạng bài viết giới thiệu từng gia sư, không phải cơ sở dữ liệu tìm kiếm được | Không: hiển thị theo thứ tự bài viết, một số hồ sơ có ghi mức lương/buổi ngay trong bài | https://giasudantri.vn/trung-tam-gia-su-online/, truy cập 26/09/2026 |
| daythem.com | Có bộ lọc “Ngành học”, “Môn học”, “Lịch biểu” (duy nhất trong 3 nền tảng có lọc theo lịch rảnh) | Không: mặc định sắp theo thời gian hoạt động gần nhất, không theo điểm phù hợp; không có lý do khuyến nghị | https://daythem.com/hoc-tai-nha/, truy cập 26/09/2026 |

*Nguồn: khảo sát trực tiếp của nhóm tại ba địa chỉ nêu trong bảng, ngày 26/09/2026.*

Bảng 1.1 cho thấy cả ba nền tảng được khảo sát đều chưa có xếp hạng tổng hợp nhiều tiêu chí. Nhận định về khoảng trống chức năng ở Mục 1.3 vì thế có căn cứ từ khảo sát thực tế.

## 1.3. Vấn đề còn tồn tại và lý do chọn hướng tiếp cận

### 1.3.1. Khoảng trống chức năng mà đồ án lựa chọn giải quyết

Từ kết quả khảo sát ở Mục 1.2, khoảng trống chức năng mà đồ án hướng tới là bước nằm giữa “lọc theo tiêu chí” và “chọn gia sư”: sau khi lọc, người học vẫn phải tự so sánh các kết quả còn lại bằng mắt. Đồ án tập trung giải quyết khoảng trống này ở mức một bộ máy khuyến nghị (*recommendation engine*) có thể giải thích được, không nhằm khẳng định đây là khoảng trống nghiên cứu chưa từng được giải quyết.

### 1.3.2. Lý do chọn hướng tiếp cận

Lý do chọn phương pháp xuất phát từ loại dữ liệu hiện có. Hệ thống trong đồ án chưa vận hành thực tế nên chưa có dữ liệu lịch sử tương tác (lịch sử ghép cặp gia sư – người học, số buổi học đã diễn ra, điểm đánh giá người học dành cho gia sư). Vì vậy, Collaborative Filtering — vốn dựa trên sở thích đã biết của một nhóm người dùng để suy ra sở thích của người dùng khác [3] — chưa có dữ liệu đầu vào (Bảng 2.1). Ngược lại, hai loại dữ liệu sau có thể thu thập hoặc giả lập ngay: (1) hồ sơ gia sư (môn dạy, khu vực, học phí, kinh nghiệm, hình thức dạy, lịch rảnh, điểm đánh giá trung bình) và (2) nhu cầu của người học nhập tại thời điểm tìm kiếm. Điểm đánh giá trung bình ở đây là thuộc tính của hồ sơ gia sư trong tập dữ liệu mẫu, không phải dữ liệu tương tác do hệ thống thu thập.

Trên cơ sở đó, đồ án áp dụng cách tiếp cận dựa trên đặc trưng hồ sơ gồm hai bước: lọc theo điều kiện bắt buộc, rồi tính điểm các tiêu chí ưu tiên bằng Weighted Scoring. Phương pháp này cho phép kiểm soát và giải thích minh bạch cách các tiêu chí được cân nhắc, thay vì phụ thuộc vào mô hình học máy dạng hộp đen [4]. Ví dụ, người học có thể tăng mức ưu tiên khu vực khi cần tìm gia sư gần nhà. Chi tiết thiết kế được trình bày ở Chương 2 và Chương 3.

Nhóm có tham khảo đồ án GS360 [5] như một ví dụ về hướng xây dựng website hỗ trợ tìm kiếm gia sư. Đồ án này không kế thừa khung tính năng của GS360 mà chỉ tập trung vào phần khuyến nghị.

GS360 (Lê Thị Hoài Thương, Lê Nguyễn Quang Minh; Trường Đại học Công nghệ Thông tin và Truyền thông Việt - Hàn, tháng 11/2024) là một website hỗ trợ tìm kiếm gia sư hoàn chỉnh với hai vai trò người dùng chính (người tìm gia sư và gia sư) cùng quản trị viên. Phía gia sư quản lý hồ sơ, tìm và nhận suất dạy; phía phụ huynh/học sinh đăng bài tìm gia sư, đặt lịch, thanh toán và nhận hoàn tiền. Ngoài ra, hệ thống còn hỗ trợ đánh giá gia sư, hỏi đáp và thống kê doanh thu (các use case 1–23, Mục 2.2.4.2, tr. 15–28; giao diện Mục 3.4, tr. 60–69).

Về tìm kiếm, Mục 2.1 (tr. 11) của tài liệu GS360 mô tả chức năng tìm gia sư thông qua từ khóa tên môn học, cấp học và địa điểm. Giao diện “tìm gia sư” ở Mục 3.4.6 (tr. 64) thực chất là biểu mẫu đăng bài tìm gia sư, sau đó bài đăng hiển thị ở trang suất dạy. Tài liệu này không mô tả cơ chế xếp hạng tổng hợp nhiều tiêu chí theo trọng số, cũng không nêu điểm thành phần hay lý do gợi ý. Cụm từ “xếp hạng” chỉ xuất hiện một lần ở Mục Hướng phát triển (tr. 70–71) khi đề xuất bổ sung “hệ thống đánh giá, xếp hạng gia sư”; các cụm “trọng số”, “thuật toán” và “điểm thành phần” không xuất hiện trong toàn văn tài liệu.

Khác với GS360, đồ án này không xây dựng nền tảng gia sư đầy đủ mà tập trung vào bộ máy khuyến nghị. Hệ thống lọc điều kiện bắt buộc (môn học, hình thức học, khung giờ giao nhau), chấm điểm năm tiêu chí ưu tiên theo Bảng 3.6, gộp bằng Weighted Scoring (Mục 2.3, Mục 3.6) và trả Top-$k$ kèm điểm thành phần, đóng góp từng tiêu chí (Mục 3.1, Mục 4.4). Vì vậy, GS360 chỉ là mốc tham chiếu về phạm vi chức năng của một website gia sư, không phải baseline để so sánh độ chính xác xếp hạng. Các kịch bản ở Bảng 5.3 mới là công cụ đánh giá của đồ án.

## 1.4. Mục tiêu và phạm vi đề tài

**Mục tiêu tổng quát.** Đề tài xây dựng và đánh giá một cơ chế hỗ trợ xếp hạng gia sư dựa trên mức độ phù hợp giữa yêu cầu của người học và các đặc trưng trong hồ sơ gia sư. Trong cơ chế này, các điều kiện bắt buộc được kiểm tra trước, các tiêu chí ưu tiên được tổng hợp thành điểm phù hợp có trọng số, và kết quả trình bày kèm các thành phần điểm để người học hiểu cơ sở của thứ hạng. Cách tiếp cận này được gọi trong báo cáo là khuyến nghị đa tiêu chí (gắn với tên đề tài theo hướng dựa trên đặc trưng hồ sơ).

**Mục tiêu cụ thể.** Đồ án đặt ra bốn mục tiêu:

- Mô hình hóa mức độ phù hợp: phân loại tiêu chí (bắt buộc/ưu tiên/tùy chọn), xác định công thức điểm cho từng tiêu chí và xây dựng module lọc – tính điểm có trọng số.
- Xây dựng API khuyến nghị bằng FastAPI, nhận nhu cầu của người học và trả về danh sách gia sư đã xếp hạng kèm điểm thành phần.
- Xây dựng giao diện demo bằng ReactJS cho phép nhập nhu cầu, chọn mức ưu tiên và xem kết quả.
- Đánh giá chất lượng xếp hạng bằng các kịch bản tìm gia sư có kỳ vọng được xác định trước, đồng thời minh họa ảnh hưởng của việc thay đổi mức ưu tiên đến thứ hạng.

**Phạm vi.** Đồ án thực hiện một bộ máy khuyến nghị (*recommendation engine*) kèm giao diện demo tối giản, vận hành trên tập dữ liệu gia sư mẫu. Cụ thể, phạm vi giới hạn ở ba điểm: (1) mỗi lần tìm chỉ xử lý một môn học; (2) so khớp khu vực theo danh mục khu vực do nhóm quy ước, không tính khoảng cách địa lý thực; (3) hệ thống chỉ có một tác nhân là người học. Đồ án không xây dựng nền tảng web đầy đủ (không có đăng ký học, đánh giá sau buổi học, quản trị viên, quản lý lịch dạy). Đề tài cũng không dùng dữ liệu vận hành thật quy mô lớn và không thực hiện so sánh đối chứng định lượng trên tập lớn; các nội dung này là hướng mở rộng khi phát triển thành đồ án tốt nghiệp.

## 1.5. Công cụ và kế hoạch thực hiện

Về công cụ trình bày, nhóm dựng sơ đồ luồng xử lý và kiến trúc hệ thống bằng HTML/CSS rồi kết xuất thành ảnh PNG (Hình 3.1–3.5); giao diện được chụp trực tiếp từ hệ thống đang chạy (Hình 4.1–4.4). Về công nghệ triển khai, backend dùng FastAPI (Python), frontend dùng ReactJS; dữ liệu mẫu lưu dạng JSON và CSV — phương án SQLite là hướng mở rộng, chưa hiện thực trong đồ án.

Thứ tự thực hiện được sắp xếp để phần thiết kế và kiểm chứng đi trước phần lập trình: xác định bài toán và công thức (Chương 3) → thiết kế dữ liệu mẫu và kịch bản kiểm thử → cài đặt module tính điểm → API → giao diện → kiểm thử và đánh giá. Khối lượng công việc được phân bổ theo Bảng 1.2, dựa trên ngân sách 2 tín chỉ (khoảng 90–120 giờ).

**Bảng 1.2 - Phân bổ thời gian thực hiện theo chương**

| Hạng mục | Số giờ dự kiến | Tỷ lệ |
|:---|---:|---:|
| Chương 1 - Tổng quan về đề tài | 8 giờ | 8% |
| Chương 2 - Cơ sở lý thuyết và công nghệ | 10 giờ | 10% |
| Chương 3 - Phân tích và thiết kế hệ thống | 30 giờ | 30% |
| Chương 4 - Xây dựng hệ thống | 30 giờ | 30% |
| Chương 5 - Kiểm thử và đánh giá | 16 giờ | 16% |
| Chương 6 - Kết luận và hướng phát triển | 6 giờ | 6% |
| **Tổng cộng** | **100 giờ** | **100%** |

*Nguồn: kế hoạch phân bổ của nhóm (Mục 1.5).*
*Ghi chú: Ngân sách 100 giờ của mỗi thành viên theo 2 tín chỉ; nhóm 3 người, tổng 300 giờ theo kế hoạch phân bổ nội bộ. Đây là số giờ dự kiến, không phải số giờ thực tế đã làm.*
