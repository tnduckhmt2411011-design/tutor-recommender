# Kịch bản demo bảo vệ đồ án

> [!NOTE]
> Kịch bản demo 4 phút, chạy trên hệ thống cục bộ. Các bước CN01–CN03 và trạng thái biên khớp với README mục 6, Bảng 5.3 và Hình 4.1–4.4 (bổ sung thêm Bước 5 kiểm chứng trạng thái `no_match` với KB05).

## 1. Mục tiêu buổi demo

Trong 4 phút, người xem phải thấy được bốn điều:

1. Người học nhập nhu cầu và chọn mức ưu tiên (CN01).
2. Kết quả là danh sách có thứ hạng, điểm tổng, đóng góp từng tiêu chí và lý do gợi ý (CN02).
3. Đổi mức ưu tiên thì thứ hạng đổi ngay, không phải nhập lại nhu cầu (CN03).
4. Hai trạng thái biên `no_match` và `zero_weight` có thông báo rõ ràng, không phải màn hình trắng.

Không demo phần quản trị, đăng nhập hay thanh toán vì đồ án không xây các phần này.

## 2. Chuẩn bị trước giờ bảo vệ (10 phút)

| # | Việc | Lệnh / thao tác | Dấu hiệu đạt |
| :-: | :--- | :--- | :--- |
| 1 | Cập nhật mã nguồn | `git pull origin main` | Không có xung đột |
| 2 | Chạy backend | `cd backend` → kích hoạt `.venv` → `python -m uvicorn app.main:app --port 8000` | Terminal báo `Uvicorn running on http://127.0.0.1:8000` |
| 3 | Kiểm tra backend | Mở `http://localhost:8000/health` | Trả về `{"status":"ok"}` |
| 4 | Chạy frontend | `cd frontend` → `npm run dev` | Terminal báo địa chỉ `http://localhost:5173` |
| 5 | Mở sẵn trình duyệt | Tab 1: `http://localhost:5173`; tab 2: `http://localhost:8000/docs` | Tab 1 hiện màn hình nhập nhu cầu |
| 6 | Dọn màn hình | Tắt thông báo hệ điều hành, đóng ứng dụng chat, đặt zoom 100% | Không có cửa sổ lạ |
| 7 | Chạy thử một lần | Nạp KB01 → xem kết quả → tải lại trang | Kết quả đúng, không có lỗi console |
| 8 | Chuẩn bị dự phòng | Mở sẵn 4 ảnh `docs/thesis/figures/hinh-ui-01..04` trong thư mục | Ảnh mở được khi không có mạng |

**Không dùng bản trực tuyến cho buổi demo chính.** Backend trên Render có thể ngủ và mất 30–40 giây cho lượt truy cập đầu; nếu buộc phải dùng, mở sẵn một tab và gọi `/health` trước khi vào phần demo ít nhất 2 phút.

## 3. Kịch bản 4 phút

### Bước 1 — Nạp kịch bản KB01 (0:00–0:40)

**Thao tác:** tại thanh “Kịch bản thực nghiệm (Bảng 5.3 · KB01 - KB14)” ở phía trên màn hình, lưu ý ô `Tự động chuyển kết quả` mặc định đang tích sẵn; có thể đọc trực tiếp biểu mẫu khởi tạo mặc định (hoặc bỏ tích ô này rồi bấm **KB01** để xem lại thông số: môn Toán, hình thức Trực tiếp, khu vực Bình Thạnh, ngân sách 200.000 đồng/giờ, cả năm mức ưu tiên ở Trung bình) rồi bấm **Tìm gia sư phù hợp →**.

**Nói:** “Đây là kịch bản KB01, một trong 14 kịch bản nhóm dùng để đánh giá. Nhu cầu được nạp sẵn để buổi demo không phụ thuộc vào việc gõ tay.”

### Bước 2 — Đọc kết quả (0:40–1:40)

**Thao tác:** chỉ vào dải kết quả và thẻ hạng 1.

**Nói:**

- “Top-3 lần lượt là GS-G01 0,938; GS-G10 0,745; GS-T06 0,625 — đúng bằng cột kỳ vọng ở Bảng 5.3.”
- “Thanh xếp chồng vẽ tối đa năm đoạn theo các tiêu chí đang áp dụng. Ở KB01, GS-G01 có bốn tiêu chí áp dụng với mức đóng góp lần lượt là Học phí 0,250; Khu vực 0,250; Kinh nghiệm 0,1875 (hiển thị 0,19 trên thanh, 0,188 ở chú giải); Đánh giá 0,250 — tổng đúng bằng 0,9375 (hiển thị 0,938); tiêu chí Lịch rảnh không áp dụng vì nhu cầu không nhập khung giờ.”
- “Dòng lý do gợi ý giải thích vì sao gia sư này đứng đầu, không chỉ đưa ra con số.”

**Nếu bị hỏi vì sao GS-T06 đứng thứ ba (cuộn nhẹ trang ở màn hình 1440×900 để xem thẻ #3):** hồ sơ này mang huy hiệu **Thực tế (ước tính \*)**, chưa có điểm đánh giá nên dùng giá trị trung tính 0,5 và có ghi chú “chưa có đánh giá”; học phí 400.000 đồng vượt ngân sách 200.000 nên điểm học phí bằng 0.

### Bước 3 — Đổi mức ưu tiên (1:40–2:40)

**Thao tác:** trên khung điều chỉnh CN03, bấm chọn đưa **Học phí** và **Khu vực** về “Bỏ qua (w = 0)”; đưa **Kinh nghiệm** và **Đánh giá** lên “Cao (w = 3)” (hoặc bấm nhanh nút 1 chạm **“Ưu tiên KN & Đánh giá”** để gán cùng cấu hình trọng số). Danh sách tự tính lại.

**Nói:**

- “Học phí và khu vực không còn được tính; kinh nghiệm và đánh giá có trọng số cao nhất.”
- “GS-G10 lên hạng 1 với 0,990 vì có 12 năm kinh nghiệm và 4,9/5, đúng như Hình 4.3.”
- “Huy hiệu tăng/giảm bậc cho biết thứ hạng thay đổi so với lần gợi ý trước.”

### Bước 4 — Trạng thái tổng trọng số bằng 0 (2:40–3:10)

**Thao tác:** bấm **“Thử ∑w_i = 0”**.

**Nói:** “Khi cả năm tiêu chí ở mức Không quan tâm, không có cơ sở để xếp hạng. Phía API trả danh sách ứng viên đã đạt điều kiện bắt buộc trong trường JSON `unranked_candidates`, còn giao diện hiển thị thống kê `Hợp lệ: 5 ứng viên` ở thanh trên kèm thông báo ‘Không thể xếp hạng do tổng trọng số bằng 0’ và nút khôi phục mặc định, thay vì chia cho 0.”

**Sau đó:** bấm **“Khôi phục trọng số mặc định (w = 2)”**.

### Bước 5 — Trạng thái không có ứng viên (3:10–3:40)

**Thao tác:** bấm **“← Điều chỉnh điều kiện tìm kiếm (CN01)”** để quay lại màn hình nhập nhu cầu, sau đó bấm nút **KB05** (môn Tiếng Trung; nếu đã bỏ tích tự động chuyển thì bấm **Tìm gia sư phù hợp →**).

**Nói:** “Bộ dữ liệu không có gia sư Tiếng Trung, nên bước lọc bắt buộc trả về rỗng. Hệ thống hiện thông báo ‘Không tìm thấy gia sư thỏa mãn điều kiện’ kèm lý do ‘Không có gia sư thỏa điều kiện bắt buộc’ và nút quay lại màn hình tìm kiếm, không trả danh sách rỗng thiếu giải thích.”

### Bước 6 — Kết thúc (3:40–4:00)

**Thao tác:** tải lại trang để đưa giao diện về trạng thái ban đầu.

**Nói:** “Toàn bộ luồng vừa rồi chạy trên API cục bộ; cùng một bộ mã nguồn cũng đã triển khai trên Vercel và Render, đường dẫn ghi trong README.”

## 4. Phương án dự phòng

| Sự cố | Xử lý | Câu nói |
| :--- | :--- | :--- |
| Backend không khởi động | Mở terminal khác, chạy lại `uvicorn`; kiểm tra cổng 8000 có bị chiếm | “Nhóm khởi động lại dịch vụ trong giây lát.” |
| Frontend báo lỗi kết nối | Kiểm tra `api.js` trỏ về `localhost:8000`; tải lại trang | “Lỗi cấu hình cổng, không phải lỗi nghiệp vụ.” |
| Máy chiếu không nhận tín hiệu | Chuyển sang bộ 4 ảnh đã mở sẵn | “Nhóm dùng ảnh chụp từ hệ thống đang chạy, số liệu giữ nguyên.” |
| Mất mạng | Demo cục bộ không cần mạng; chỉ bản trực tuyến mới cần | Không cần nói |
| Hội đồng yêu cầu nhập tay | Nhập môn Toán, Trực tiếp, Bình Thạnh, 200.000, không chọn khung giờ | Kết quả giống KB01 |

## 5. Sau buổi demo

- Đưa giao diện về KB01, mức ưu tiên mặc định, để người hỏi sau có thể thao tác tiếp.
- Giữ terminal backend và frontend mở đến hết buổi; không tắt máy.
- Nếu hội đồng yêu cầu xem mã nguồn, mở sẵn `backend/app/scoring/ranker.py` và `backend/app/api/recommend.py`.

## 6. Câu hỏi thường gặp và câu trả lời chuẩn bị

**1. Vì sao không dùng Collaborative Filtering?**
Vì phương pháp này cần ma trận tương tác (ai học với ai, bao nhiêu buổi), trong khi hệ thống chưa vận hành nên chưa có dữ liệu đó; dùng sẽ mắc cold start ngay từ hồ sơ đầu tiên. So sánh ở Bảng 2.1.

**2. 14/14 kịch bản có phải là tự chứng minh?**
Kỳ vọng Top-3 được ghi trước khi chạy và lưu trong `scenarios.json`, nên kết quả 14/14 xác nhận hệ thống chạy đúng thiết kế. Nó không chứng minh thiết kế là tốt nhất; muốn vậy cần người học thật, và đó là hạn chế ở Mục 5.3.

**3. Vì sao chọn δ = 0,5 và E_max = 8?**
Đây là giá trị khởi tạo do nhóm chọn, không phải quy luật sẵn có. Nhóm khảo sát độ nhạy ở Bảng 5.5–5.6: mọi mức $\delta \in [0{,}25; 1{,}00]$ và các mốc $E_{\max} \in \{5, 6, 8\}$ giữ nguyên Top-3 của 14/14 kịch bản; khi tăng $E_{\max}$ lên 10 và 12, chỉ duy nhất 1/14 kịch bản (`KB10`) đổi Top-3 (`GS-G01` rời Top-3, `GS-T06` vào ở mốc 10 và vượt `GS-G09` ở mốc 12).

**4. Hồ sơ chưa có đánh giá được cho 0,5 có công bằng?**
Đây là giải pháp tạm để không loại oan hồ sơ mới. Giao diện hiện ghi chú “chưa có đánh giá”, và ngưỡng dữ liệu tối thiểu vẫn loại các hồ sơ thiếu quá nhiều tiêu chí. Cách xử lý tốt hơn là thu thập đánh giá thật, thuộc hướng phát triển.

**5. Con số 3,54 ms nghĩa là gì?**
Là thời gian xử lý nội tại của endpoint khi gọi bằng `TestClient` trên máy cục bộ, không phải độ trễ end-to-end qua mạng. Chip 651,5 ms trên ảnh Hình 4.2 đã bao gồm khoảng dừng 650 ms dành cho hiệu ứng chuyển trang trong `App.jsx` khi chuyển từ màn hình tìm kiếm sang kết quả, nên không dùng để so sánh trực tiếp với hiệu năng API.

**6. Đồ án khác gì GS360?**
GS360 là một nền tảng gia sư đầy đủ (đăng ký, đặt lịch, thanh toán, đánh giá). Đồ án chỉ làm bộ máy khuyến nghị và đối chiếu phạm vi chức năng; không kế thừa mã nguồn hay khung tính năng của GS360.

**7. Dữ liệu là thật hay giả?**
14 hồ sơ mô phỏng (`simulated`) và 2 hồ sơ thu thập công khai (`public_collected`). Hai hồ sơ công khai có học phí và lịch rảnh ước tính, điểm đánh giá để trống; nhãn dữ liệu được tách rõ trong tệp và trong Phụ lục A.

**8. Nếu có 10.000 hồ sơ thì hệ thống còn chạy được không?**
Bộ lọc hiện duyệt tuần tự trên 16 hồ sơ, chưa kiểm chứng ở quy mô lớn. Với 10.000 hồ sơ cần đánh chỉ mục theo môn và khu vực rồi đo lại; nhóm chưa thực hiện nên không đưa ra con số.

**9. Vì sao tên đề tài ghi “Content-Base” nhưng trong bài dùng “Content-Based”?**
Tên đề tài giữ nguyên theo bản đã đăng ký. Khi trình bày phương pháp, báo cáo dùng thuật ngữ chuẩn “Content-Based Filtering”. Nếu hội đồng yêu cầu, nhóm sẽ điều chỉnh tên trong văn bản chính thức.

**10. Vì sao mặc định Top-3?**
API cho phép chọn tham số `top_k` là số nguyên trong đoạn $[1, 20]$ và giao diện cung cấp lựa chọn `{3, 5, 10}`, mặc định `3` để danh sách gọn (khi nạp nhanh kịch bản hệ thống đặt lại `top_k = 3`). Các kịch bản đánh giá cũng dùng Top-3 để so sánh nhất quán.

## 7. Câu không nên nói

- Không nói “hệ thống tối ưu” hoặc “chính xác nhất”; chỉ nói “khớp kỳ vọng trên 14 kịch bản”.
- Không nói “dữ liệu thật” khi chưa phân biệt 14 hồ sơ mô phỏng và 2 hồ sơ công khai.
- Không hứa “sẽ triển khai” các đề xuất ở Mục 6.2.3; chỉ nói đó là đề xuất chưa hiện thực.
- Không so sánh trực tiếp với GS360 về chất lượng xếp hạng, vì GS360 không công bố cơ chế xếp hạng tổng hợp.
