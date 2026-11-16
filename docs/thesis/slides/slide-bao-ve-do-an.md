# Slide thuyết trình bảo vệ đồ án (US-35)

> [!NOTE]
> **Đề xuất, nhóm xác nhận.** Kịch bản 16 slide cho 15 phút trình bày và 5–10 phút hỏi đáp. Mỗi slide ghi rõ nội dung đưa lên slide, lời thoại gợi ý và hình/bảng lấy từ báo cáo. Số liệu trong slide phải trùng với Chương 5; nếu nhóm cập nhật số liệu thì sửa cả hai nơi.

## 0. Thông tin chung

- **Thời lượng:** 15 phút trình bày + 5–10 phút hỏi đáp. Dự phòng: nếu hội đồng giới hạn 12 phút, bỏ slide 8 và gộp slide 12 vào slide 11.
- **Tên đề tài (dùng đúng trên mọi slide):** Hệ thống khuyến nghị gia sư dựa trên phương pháp Content-Base Filtering.
- **Người trình bày gợi ý:** Nhóm trưởng mở đầu và kết luận; thành viên phụ trách dữ liệu trình bày slide 9; thành viên phụ trách kiểm thử trình bày slide 11–13.
- **Quy ước trình bày:** mỗi slide tối đa 5 dòng chữ, cỡ chữ tối thiểu 24 pt, không đọc nguyên văn slide; số thập phân dùng dấu phẩy; mọi hình/bảng ghi số hiệu tương ứng trong báo cáo.

## Slide 1 — Bìa (0:00–0:30)

**Trên slide**

- Tên trường, khoa.
- Tên đề tài.
- Giảng viên hướng dẫn: TS. Lê Anh Nhã Uyên.
- Ba thành viên và mã sinh viên; lớp Khoa học máy tính 2024.
- Cần Thơ, tháng 11 năm 2026.

**Lời thoại**

“Kính thưa hội đồng. Nhóm chúng em trình bày đồ án Hệ thống khuyến nghị gia sư dựa trên phương pháp Content-Base Filtering. Phần trình bày gồm bốn nội dung: bài toán và phạm vi, cách thiết kế mô hình điểm, kết quả kiểm thử, và hạn chế của đồ án.”

## Slide 2 — Bài toán (0:30–2:00)

**Trên slide**

- Người học cân nhắc đồng thời: môn học, khu vực, học phí, hình thức học, thời gian.
- Các tiêu chí xung đột: gia sư rẻ thường ít kinh nghiệm; gia sư gần nhà có thể vượt ngân sách.
- Ba kênh hiện có (Bảng 1.1): hội nhóm mạng xã hội, trung tâm gia sư, nền tảng trực tuyến.
- Khoảng trống: sau bước lọc, người học vẫn phải tự so sánh bằng mắt; không kênh nào trong ba kênh khảo sát có xếp hạng tổng hợp nhiều tiêu chí.

**Lời thoại**

“Vấn đề không phải là thiếu gia sư, mà là thiếu bước chọn giữa các gia sư đã thỏa điều kiện. Nhóm khảo sát ba kênh: giasudatviet.com, giasudantri.vn và daythem.com. Cả ba đều dừng ở lọc theo môn hoặc theo lịch, không có điểm phù hợp tổng hợp và không có lý do gợi ý.”

**Hình/bảng:** Bảng 1.1.

## Slide 3 — Mục tiêu và phạm vi (2:00–3:00)

**Trên slide**

- Bốn mục tiêu: (a) mô hình hóa mức độ phù hợp; (b) API gợi ý; (c) giao diện demo; (d) đánh giá bằng kịch bản.
- Phạm vi: một môn học mỗi lần tìm; khu vực theo danh mục quy ước; một tác nhân là người học.
- Không làm: đăng ký học, thanh toán, quản trị viên, đánh giá sau buổi học.
- Dữ liệu: 16 hồ sơ mẫu, 14 kịch bản KB01–KB14.

**Lời thoại**

“Nhóm giới hạn phạm vi ở bộ máy khuyến nghị và một giao diện demo, không xây nền tảng gia sư đầy đủ. Giới hạn này là lựa chọn có chủ đích để phần đánh giá tập trung vào chất lượng xếp hạng.”

## Slide 4 — Vì sao chọn hướng dựa trên đặc trưng hồ sơ (3:00–4:30)

**Trên slide**

- Ba nhóm phương pháp (Bảng 2.1): Content-Based, Collaborative, Hybrid.
- Hệ thống chưa vận hành nên chưa có ma trận tương tác; Collaborative cần dữ liệu này.
- Hồ sơ gia sư và nhu cầu người học đều thu thập được ngay.
- Đánh đổi: không học được sở thích ẩn; bù lại, mỗi điểm số giải thích được.

**Lời thoại**

“Collaborative Filtering cần biết ai đã học với ai. Đồ án chưa có dữ liệu đó và cũng không thể tự tạo ra một cách trung thực. Chọn Content-Based nghĩa là chấp nhận không học được sở thích ẩn, nhưng đổi lại toàn bộ điểm số đều truy được về một công thức.”

**Hình/bảng:** Bảng 2.1.

## Slide 5 — Kiến trúc ba lớp (4:30–5:30)

**Trên slide**

- Giao diện ReactJS: `SearchPage`, `ResultPage`, `api.js`.
- API FastAPI: `POST /api/recommend`, bốn trạng thái phản hồi.
- Module tính điểm: `filters`, `eligibility`, `weights`, `criteria`, `ranker`.
- Module không tự đọc dữ liệu; lớp API nạp qua `TutorRepository` rồi truyền vào.

**Lời thoại**

“Điểm nhóm muốn nhấn ở slide này là ranh giới trách nhiệm. Module tính điểm là hàm thuần: đưa danh sách hồ sơ và nhu cầu vào, nhận danh sách đã xếp hạng ra. Nhờ vậy kiểm thử đơn vị không cần dựng web server.”

**Hình/bảng:** Hình 3.2.

## Slide 6 — Luồng xử lý tám bước (5:30–6:30)

**Trên slide**

- (1) nhập nhu cầu → (2) kiểm tra, chuẩn hóa → (3) lọc điều kiện bắt buộc.
- (4) kiểm tra ngưỡng dữ liệu tối thiểu → (5) tính điểm thành phần.
- (6) kiểm tra tổng trọng số → (7) tổng hợp, xếp hạng, phá hòa → (8) trả Top-k kèm lý do.
- Bốn nhánh thông báo: 422, `no_match`, `zero_weight`, thiếu dữ liệu.

**Lời thoại**

“Hai bước dễ bị bỏ qua là bước 4 và bước 6. Bước 4 loại hồ sơ thiếu dữ liệu thay vì tính điểm trên vài ô còn lại. Bước 6 xử lý trường hợp người học đặt cả năm tiêu chí về không quan tâm, khi đó không có cơ sở để xếp hạng.”

**Hình/bảng:** Hình 3.1, Bảng 3.7.

## Slide 7 — Mô hình điểm (6:30–8:30)

**Trên slide**

- Năm tiêu chí ưu tiên, mỗi điểm thành phần $s_i \in [0, 1]$ (Bảng 3.6).
- Học phí: 1 nếu trong ngân sách; giảm tuyến tính khi vượt, bằng 0 khi vượt quá $\delta = 0{,}5$.
- Kinh nghiệm: $\min(E / E_{\max}, 1)$ với $E_{\max} = 8$.
- Đánh giá: $R/5$; chưa có đánh giá dùng giá trị trung tính 0,5 kèm ghi chú.
- Tổng hợp: $S(g) = \sum w_i s_i / \sum w_i$, chỉ trên tiêu chí đang áp dụng.

**Lời thoại**

“Mỗi công thức được chọn để giữ tính đơn điệu: học phí tăng thì điểm không tăng, kinh nghiệm và đánh giá tăng thì điểm không giảm. Tính chất này được kiểm tra riêng ở Bảng 5.2. Hai tham số $\delta$ và $E_{\max}$ là lựa chọn của nhóm, không phải quy luật sẵn có, nên nhóm khảo sát độ nhạy ở Chương 5.”

**Hình/bảng:** Bảng 3.6, công thức (2.1).

## Slide 8 — Mức ưu tiên và ngưỡng dữ liệu (8:30–9:15)

**Trên slide**

- Bốn mức: Không quan tâm (0), Thấp (1), Trung bình (2), Cao (3).
- Người học không phải chia phần trăm; đổi mức là đổi trọng số.
- Ngưỡng dữ liệu: $n$ tiêu chí áp dụng thì cần tối thiểu 1, 2, 2, 3, 4 tiêu chí có dữ liệu.
- Ví dụ: hồ sơ chỉ có học phí và khu vực sẽ bị loại khi truy vấn cần 4 tiêu chí.

**Lời thoại**

“Ngưỡng dữ liệu là phần nhóm thêm sau khi thử và thấy một số hồ sơ được xếp hạng dựa trên quá ít thông tin. Thay vì để chúng lên đầu vì may mắn, hệ thống loại khỏi kết quả của truy vấn đó và ghi chú lý do.”

**Hình/bảng:** Bảng 3.5, Bảng 3.7.

## Slide 9 — Dữ liệu và kịch bản (9:15–10:00)

**Trên slide**

- 16 hồ sơ: 14 mô phỏng (`simulated`), 2 thu thập công khai (`public_collected`: GS-T06, GS-T07).
- Hai hồ sơ công khai có học phí và lịch rảnh ước tính, điểm đánh giá để trống.
- Dữ liệu thiết kế để kiểm thử: cặp chỉ khác một tiêu chí, ca xung đột, ca thiếu đánh giá.
- 14 kịch bản KB01–KB14, mỗi kịch bản có Top-3 kỳ vọng viết trước khi chạy.

**Lời thoại**

“Kỳ vọng Top-3 được ghi trước khi chạy, không phải chép lại kết quả. Đây là điểm quan trọng để 14/14 không phải là tự chứng minh. Nhóm cũng tách rõ nhãn dữ liệu thật và dữ liệu mô phỏng để hội đồng kiểm tra được.”

**Hình/bảng:** Bảng A.1, Bảng D.1.

## Slide 10 — Demo giao diện (10:00–11:30)

**Trên slide**

- CN01: nhập nhu cầu, chọn mức ưu tiên, nạp nhanh kịch bản.
- CN02: Top-3 kèm điểm tổng, thanh đóng góp từng tiêu chí, lý do gợi ý.
- CN03: đổi mức ưu tiên ngay trên màn hình kết quả, thấy thứ hạng đổi.
- Trạng thái biên: `no_match`, `zero_weight`.

**Lời thoại**

“Phần demo chạy trực tiếp theo kịch bản riêng, khoảng 3 phút. Nếu mạng hoặc máy chiếu có sự cố, nhóm dùng bốn ảnh Hình 4.1–4.4 và nêu rõ đây là ảnh chụp từ hệ thống đang chạy.”

**Hình/bảng:** Hình 4.1–4.4; kịch bản chi tiết trong `kich-ban-demo-bao-ve.md`.

## Slide 11 — Kiểm thử tự động (11:30–12:30)

**Trên slide**

- 200 bài kiểm thử: 132 đơn vị, 41 API, 27 kịch bản và độ nhạy.
- Kết quả: 200/200 đạt, 0 lỗi, 0 bỏ qua; thời gian chạy 1,18 giây.
- Độ bao phủ 97% trên `backend/app/` (340/351 câu lệnh); tầng API và schemas đạt 100%.
- Kiểm thử ca biên: điểm 0 và 1, đơn điệu của năm hàm điểm, phá hòa theo mã gia sư.

**Lời thoại**

“Nhóm không chỉ kiểm tra trường hợp đúng. Bảng 5.2 kiểm tra các đầu mút và tính đơn điệu, vì đó là chỗ một công thức viết sai vẫn cho kết quả trông hợp lý ở giữa dải.”

**Hình/bảng:** Bảng 5.1, Bảng 5.2.

## Slide 12 — Kết quả 14 kịch bản (12:30–13:15)

**Trên slide**

- 14/14 kịch bản trùng tập hợp Top-3 kỳ vọng.
- Thứ tự trong Top-3 cũng trùng ở cả 14 kịch bản.
- Ca đáng chú ý: KB04 chỉ có 2 gia sư; KB09 chỉ có 1; KB05 không có gia sư (`no_match`).
- Điểm tổng KB01: GS-G01 0,9375; GS-G10 0,7450; GS-T06 0,6250.

**Lời thoại**

“Kết quả 14/14 cần đọc đúng: đây là kiểm chứng rằng hệ thống chạy đúng thiết kế, không phải bằng chứng rằng thiết kế là tốt nhất. Muốn đánh giá chất lượng thiết kế cần người dùng thật, và đó là hạn chế nhóm ghi ở slide sau.”

**Hình/bảng:** Bảng 5.3, Bảng 5.4, Bảng 5.9.

## Slide 13 — Độ nhạy tham số (13:15–14:00)

**Trên slide**

- Thay đổi $\delta$ trong dải khảo sát: Top-3 giữ nguyên.
- Thay đổi $E_{\max}$: Top-3 giữ nguyên trong dải hợp lý.
- Thay đổi ngân sách ±30%: thứ hạng đổi ở các ca sát ngưỡng.
- Đổi bộ mức ưu tiên: thứ hạng đổi rõ — đúng như thiết kế.

**Lời thoại**

“Kết quả này dẫn tới một kết luận thiết kế: trọng số là biến quyết định, nên giao diện phải cho người học đổi trọng số và phải giải thích hệ quả. Đó là lý do CN03 được đặt ngay trên màn hình kết quả.”

**Hình/bảng:** Bảng 5.5–5.8.

## Slide 14 — Hạn chế (14:00–14:30)

**Trên slide**

- 16 hồ sơ là dữ liệu mẫu, chưa đại diện thị trường.
- Chưa có dữ liệu tương tác và phản hồi sau khuyến nghị.
- Hai hồ sơ công khai có trường ước tính.
- Chưa kiểm chứng với người học ngoài nhóm.
- Điểm trung tính 0,5 cho hồ sơ chưa có đánh giá là giải pháp tạm.

**Lời thoại**

“Nhóm chủ động nêu các hạn chế này vì chúng quyết định phạm vi kết luận. Báo cáo không tuyên bố hệ thống sẵn sàng vận hành thương mại.”

## Slide 15 — Hướng phát triển và kết luận (14:30–15:00)

**Trên slide**

- Mở rộng dữ liệu và thu thập phản hồi sau khuyến nghị.
- Thêm tiêu chí cấp lớp và mục tiêu học tập (đề xuất ở Mục 6.2.3, chưa hiện thực).
- Kết luận: bốn mục tiêu đề ra đều có sản phẩm tương ứng và số liệu kiểm chứng.
- Mã nguồn, dữ liệu, kịch bản và báo cáo công khai trong kho lưu trữ của nhóm.

**Lời thoại**

“Nhóm kết thúc ở đúng phạm vi đã đăng ký: một bộ máy khuyến nghị chạy được, giải thích được và đã kiểm thử, cùng giao diện demo. Phần mở rộng xin để ở mức đề xuất.”

## Slide 16 — Hỏi đáp

**Trên slide**

- Dòng chữ “Xin cảm ơn hội đồng” + tên đề tài.
- Ba mã QR (nếu có): báo cáo PDF, kho mã nguồn, bản demo trực tuyến.
- Không đưa thêm nội dung kỹ thuật; slide này để trống.

**Lời thoại**

“Nhóm sẵn sàng nhận câu hỏi. Các câu hỏi thường gặp và câu trả lời đã chuẩn bị trong tài liệu kịch bản demo, mục 6.”

## Phụ lục: kiểm tra trước khi trình bày

- [ ] Tên đề tài trên slide 1 và slide 16 giống nhau và giống bìa báo cáo.
- [ ] Số liệu trên slide 11–13 khớp Chương 5 tại thời điểm nộp.
- [ ] Mọi hình có số hiệu (Hình 3.1, 3.2, 4.1–4.4) và ghi nguồn ở góc dưới.
- [ ] Không còn từ cấm trong slide: “tối ưu”, “thông minh”, “tự học”, “Machine Learning”, “kNN”, “Min-Max”.
- [ ] Số thập phân dùng dấu phẩy; số nguyên có phân cách nghìn bằng dấu chấm.
- [ ] Đã xuất PDF dự phòng và lưu cùng thư mục với bản trình chiếu.
