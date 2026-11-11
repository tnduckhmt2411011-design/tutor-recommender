# CHƯƠNG 3. PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG

> [!NOTE]
> **Đề xuất, nhóm xác nhận**

Chương này chuyển yêu cầu ở Chương 1–2 thành thiết kế cụ thể: phát biểu bài toán (3.1), yêu cầu chức năng (3.2) và phi chức năng (3.3), mô hình hóa mức độ phù hợp (3.4), thiết kế dữ liệu (3.5), thiết kế thuật toán (3.6), kiến trúc và luồng xử lý (3.7), thiết kế giao diện (3.8).

---

## 3.1. Phát biểu bài toán

Trong báo cáo này, “người học” chỉ học sinh hoặc phụ huynh thay mặt học sinh; thuật ngữ này được dùng thống nhất cho tác nhân duy nhất của hệ thống (không có tác nhân quản trị hay tác nhân hệ thống ngoài).

**Đầu vào:** nhu cầu của người học gồm môn học cần tìm, hình thức học, khu vực mong muốn, ngân sách tối đa theo giờ, khung thời gian rảnh, cùng mức ưu tiên cho từng tiêu chí.

**Đầu ra:** danh sách Top-k gia sư thỏa các điều kiện bắt buộc, xếp hạng giảm dần theo điểm phù hợp, kèm điểm thành phần và lý do gợi ý. Trường hợp không có gia sư nào thỏa điều kiện bắt buộc, hệ thống thông báo rõ thay vì trả danh sách rỗng không giải thích.

## 3.2. Yêu cầu chức năng

Ở quy mô đồ án học phần, hệ thống tập trung vào ba chức năng cốt lõi (Bảng 3.1).

**Bảng 3.1 - Danh sách chức năng chính**

| Mã | Tên chức năng | Mô tả |
|:---:|:---|:---|
| CN01 | Nhập nhu cầu và mức ưu tiên | Người học nhập môn học, hình thức học, khu vực, ngân sách, khung thời gian rảnh và chọn mức ưu tiên cho từng tiêu chí |
| CN02 | Xem danh sách gợi ý kèm điểm | Hệ thống trả về Top-k gia sư xếp hạng theo điểm phù hợp, kèm điểm từng tiêu chí thành phần và lý do gợi ý; thông báo rõ khi không có gia sư thỏa điều kiện bắt buộc |
| CN03 | Điều chỉnh mức ưu tiên minh họa | Người học thay đổi mức ưu tiên của từng tiêu chí và quan sát danh sách xếp hạng lại tương ứng - điểm nhấn thực nghiệm của đồ án |

*Nguồn: thiết kế chức năng của nhóm (Mục 3.2).*

## 3.3. Yêu cầu phi chức năng

- **Hiệu năng:** API phản hồi dưới một giây với tập dữ liệu mẫu quy mô vài trăm bản ghi. Đây là ngưỡng phù hợp cho demo thuật toán, không phải chỉ tiêu vận hành của hệ thống production; mức đạt được khi chạy thực tế trình bày ở mục 5.1.2.
- **Khả năng mở rộng:** module tính điểm tách rời phần API và giao diện để có thể thêm tiêu chí mới hoặc thay công thức (ví dụ chuyển sang hướng Hybrid) mà không viết lại toàn bộ hệ thống.
- **Khả năng giải thích:** mọi kết quả phải kèm điểm thành phần và đóng góp của từng tiêu chí vào điểm tổng.
- **Khả năng tái lập:** tham số của các hàm điểm (mục 3.6) và bộ trọng số mặc định lưu ở một nơi cấu hình riêng để lặp lại được các kịch bản đánh giá.

## 3.4. Mô hình hóa mức độ phù hợp

Mỗi tiêu chí được phân vào một trong ba loại: bắt buộc (không thỏa thì loại), ưu tiên (tính điểm để xếp hạng) và tùy chọn (chỉ tính khi người học thực sự quan tâm). Bảng 3.2 nêu cách phân loại và cách xử lý.

**Bảng 3.2 - Phân loại tiêu chí**

| Tiêu chí | Loại | Cách xử lý | Lý do |
|:---|:---|:---|:---|
| Môn học | Bắt buộc | Người học chọn một môn mỗi lần tìm; gia sư phải dạy môn đó | Sai môn thì không có giá trị, dù điểm khác cao |
| Hình thức học | Bắt buộc có điều kiện | Nếu người học chọn Trực tiếp hoặc Trực tuyến: gia sư phải dạy hình thức đó (gia sư “Cả hai” thỏa cả hai). Nếu chọn “Không yêu cầu”: không lọc | Hình thức không tương thích thì không học được |
| Khung giờ rảnh | Bắt buộc có điều kiện + ưu tiên | Nếu người học nhập khung giờ: phải có ít nhất một khung giờ giao nhau (lọc); số khung giờ giao càng nhiều điểm càng cao (chấm điểm) | Không có giờ chung thì không thể học |
| Học phí | Ưu tiên (ngân sách mềm) | Học phí không vượt ngân sách: điểm tối đa; vượt thì điểm giảm dần, không loại ngay | Cho phép chấp nhận vượt nhẹ nếu gia sư tốt (theo động lực ở mục 1.1) |
| Khu vực | Ưu tiên | Chỉ áp dụng khi người học chọn Trực tiếp hoặc “Không yêu cầu” hình thức và có nhập khu vực; nếu học Trực tuyến thì không áp dụng | Học trực tuyến không phụ thuộc vị trí |
| Kinh nghiệm | Ưu tiên | Càng nhiều năm càng tốt, có mức trần; người học không nhập yêu cầu tối thiểu | Giữ đầu vào đơn giản |
| Điểm đánh giá | Ưu tiên | Điểm trung bình càng cao càng tốt; người học không nhập yêu cầu tối thiểu | Giữ đầu vào đơn giản |

*Nguồn: thiết kế của nhóm (Mục 3.4).*

Tiêu chí tùy chọn trong đồ án là các tiêu chí ưu tiên mà người học đặt mức “Không quan tâm” (trọng số 0) - khi đó tiêu chí bị bỏ qua hoàn toàn. Các quy tắc ở Bảng 3.2 là quyết định thiết kế của nhóm, không phải quy luật có sẵn; nếu thay đổi (ví dụ chuyển ngân sách thành ràng buộc cứng), mục 3.6 và các kịch bản ở Chương 5 phải được cập nhật tương ứng.

## 3.5. Thiết kế dữ liệu

Vì dữ liệu chỉ lưu dạng JSON và CSV, không có quan hệ khóa ngoại giữa nhiều bảng, đồ án không xây dựng sơ đồ ER; cấu trúc bản ghi của hai đối tượng dữ liệu chính được mô tả trực tiếp ở Bảng 3.3 và Bảng 3.4.

**Bảng 3.3 - Cấu trúc bản ghi hồ sơ gia sư**

| Trường dữ liệu | Ý nghĩa |
|:---|:---|
| id | Mã gia sư (dạng GS001), thay cho họ tên để tránh dùng thông tin cá nhân không cần thiết |
| môn_dạy | Một hoặc nhiều môn học gia sư đảm nhận |
| khu_vực | Danh sách khu vực gia sư dạy trực tiếp; để trống nếu chỉ dạy trực tuyến |
| học_phí_giờ | Đơn giá theo giờ (VNĐ) |
| số_năm_kinh_nghiệm | Số năm kinh nghiệm, dùng để tính điểm kinh nghiệm |
| hình_thức_dạy | Trực tiếp / Trực tuyến / Cả hai |
| lịch_rảnh | Tập khung giờ rảnh trong tuần; mỗi khung là một ô (ngày trong tuần × buổi sáng/chiều/tối) |
| điểm_đánh_giá_tb | Điểm đánh giá trung bình (thang 5); có thể trống nếu gia sư chưa có đánh giá |
| nguồn_dữ_liệu | Thu thập công khai / Giả lập - để tách rõ dữ liệu thật và dữ liệu giả lập |

*Nguồn: thiết kế của nhóm (Mục 3.5); ánh xạ sang định danh mã nguồn tại `docs/design/data-dictionary.md`.*

**Bảng 3.4 - Cấu trúc bản ghi nhu cầu của người học**

| Trường dữ liệu | Ý nghĩa |
|:---|:---|
| môn_học | Môn học cần tìm gia sư (chọn một môn) |
| hình_thức_học | Trực tiếp / Trực tuyến / Không yêu cầu |
| khu_vực_mong_muốn | Một khu vực, hoặc để trống nếu không yêu cầu |
| ngân_sách_tối_đa | Mức học phí tối đa mỗi giờ người học mong muốn (VNĐ), hoặc để trống |
| khung_thời_gian | Tập khung giờ rảnh của người học (cùng cách chia ô như lịch_rảnh), hoặc để trống |
| mức_ưu_tiên | Mức ưu tiên của năm tiêu chí: học phí, khu vực, kinh nghiệm, đánh giá, lịch rảnh |

*Nguồn: thiết kế của nhóm (Mục 3.5); ánh xạ sang định danh mã nguồn tại `docs/design/data-dictionary.md`.*

**Mức ưu tiên và trọng số.** Thay vì yêu cầu người học tự chỉnh năm tỷ lệ phần trăm, mỗi tiêu chí được chọn một trong bốn mức và quy đổi thành trọng số theo Bảng 3.5. Mặc định mọi tiêu chí ở mức “Trung bình” (trọng số bằng nhau); đây chỉ là giá trị khởi tạo để demo, không phải bộ cấu hình đã được kiểm chứng.

**Bảng 3.5 - Quy đổi mức ưu tiên sang trọng số**

| Mức ưu tiên | Trọng số w_i |
|:---|---:|
| Không quan tâm | 0 |
| Thấp | 1 |
| Trung bình (mặc định) | 2 |
| Cao | 3 |

*Nguồn: thiết kế của nhóm (Mục 3.5); hiện thực tại `backend/app/core/config.py` (PRIORITY_WEIGHTS).*

**Nguyên tắc thiết kế dữ liệu mẫu.** Dữ liệu mẫu được thiết kế để kiểm thử thuật toán chứ không chỉ để hệ thống chạy được. Bản ghi thu thập từ hồ sơ công khai và bản ghi giả lập được đánh dấu riêng (trường nguồn_dữ_liệu); không lưu họ tên hay thông tin liên hệ. Tập dữ liệu phải có: (1) các trường hợp xung đột tiêu chí (ví dụ gia sư rẻ nhưng ít kinh nghiệm so với gia sư đắt nhưng đánh giá cao); (2) các cặp gia sư chỉ khác nhau ở đúng một tiêu chí để kiểm tra từng hàm điểm; (3) ít nhất một tình huống không có gia sư nào thỏa điều kiện bắt buộc; (4) một số gia sư chưa có điểm đánh giá; (5) dữ liệu không được tạo theo cách vô tình làm thuật toán luôn cho kết quả “đẹp”. Danh mục khu vực do nhóm tự quy ước và ghi rõ trong phụ lục, vì phân chia đơn vị hành chính cấp dưới tỉnh/thành đã có thay đổi trong thời gian gần đây và đồ án không cần phụ thuộc vào cách phân chia đó.

## 3.6. Thiết kế thuật toán

Quy trình tính điểm gồm bốn bước:

- **Bước 1.** Kiểm tra và chuẩn hóa đầu vào (ví dụ ngân sách không âm, bắt buộc có môn học).
- **Bước 2.** Lọc điều kiện bắt buộc theo Bảng 3.2; nếu không còn gia sư nào, trả thông báo “không có gia sư thỏa điều kiện”.
- **Bước 3.** Tính điểm thành phần s_i ∈ [0, 1] cho các tiêu chí ưu tiên theo Bảng 3.6.
- **Bước 4.** Gộp bằng công thức Weighted Scoring (2.1), sắp xếp giảm dần theo S (đồng điểm thì xếp theo mã gia sư để kết quả ổn định), lấy Top-k và trả kèm điểm thành phần cùng đóng góp w_i × s_i ÷ Σ w_i của từng tiêu chí.

**Bảng 3.6 - Công thức điểm thành phần**

| Tiêu chí | Đầu vào | Công thức điểm s_i | Tham số | Ví dụ |
|:---|:---|:---|:---|:---|
| Học phí | P: học phí gia sư; B: ngân sách | s = 1 nếu P ≤ B; s = max(0, 1 − (P − B) ÷ (δ × B)) nếu P > B | δ = 0,5 (vượt 50% ngân sách thì điểm về 0) | B = 200.000: P = 180.000 → 1,00; P = 230.000 → 0,70; P = 300.000 → 0,00 |
| Khu vực | K: khu vực người học; tập khu vực của gia sư | s = 1 nếu K thuộc khu vực dạy của gia sư; ngược lại s = 0 | Không áp dụng nếu học Trực tuyến hoặc không nhập K | K = KV1: gia sư dạy {KV1, KV2} → 1; gia sư dạy {KV3} → 0; gia sư chỉ trực tuyến → 0 |
| Kinh nghiệm | E: số năm kinh nghiệm | s = min(E ÷ E_max, 1) | E_max = 8 | E = 0 → 0,00; E = 4 → 0,50; E = 10 → 1,00 |
| Đánh giá | R: điểm trung bình (thang 5) | s = R ÷ 5; nếu chưa có đánh giá thì s = 0,5 (giá trị trung tính) | Giá trị trung tính 0,5 | R = 5 → 1,00; R = 4,5 → 0,90; R = 3 → 0,60 |
| Lịch rảnh | L: khung giờ người học; T: khung giờ gia sư | s = \|L ∩ T\| ÷ \|L\| (bước 2 đã đảm bảo \|L ∩ T\| ≥ 1) | Không áp dụng nếu người học không nhập L | L = {T2-tối, T4-tối, T7-sáng}; T chứa T2-tối và T7-sáng → 2/3 ≈ 0,67; L = {T2-tối, T3-tối, T4-tối, T5-tối, T6-tối, T7-sáng, CN-sáng}; T chứa 6/7 khung (thiếu đúng T7-sáng) → 6/7 ≈ 0,857; L = {T2-tối, T4-tối, T6-tối, CN-chiều}; T chỉ chứa đúng T2-tối → 1/4 = 0,25 |

*Nguồn: thiết kế của nhóm (Mục 3.6); hiện thực tại `backend/app/scoring/criteria.py`, đối chiếu chi tiết trong `docs/design/scoring-spec.md` mục 4.*

**Cơ sở của các tham số.** δ = 0,5 và E_max = 8 là lựa chọn thiết kế của nhóm, không phải quy luật sẵn có; chúng là giá trị khởi tạo cho demo. Nhóm kiểm tra độ nhạy của kết quả khi thay đổi các tham số này ở mục 5.2. Các hàm điểm được thiết kế đơn điệu: học phí tăng thì điểm không tăng; kinh nghiệm, đánh giá và số khung giờ giao tăng thì điểm không giảm. Tính chất này được kiểm tra bằng các ca biên ở mục 5.1.

**Các trường hợp đặc biệt:**

- Người học chọn học Trực tuyến: tiêu chí khu vực không áp dụng, bị loại khỏi cả tử số và mẫu số của công thức tổng hợp.
- Người học không nhập ngân sách, khu vực hoặc khung giờ: tiêu chí tương ứng không áp dụng, xử lý như trên.
- Tiêu chí có mức “Không quan tâm” (w = 0): không được tính.
- Tổng trọng số của các tiêu chí đang áp dụng bằng 0: không thể xếp hạng; hệ thống hiển thị danh sách gia sư thỏa điều kiện bắt buộc kèm thông báo cho người học chọn ít nhất một tiêu chí ưu tiên.
- Gia sư chưa có điểm đánh giá: dùng giá trị trung tính 0,5 và ghi chú “chưa có đánh giá” trên giao diện; đây là giải pháp tạm, được ghi nhận ở mục 5.3.

**Điều kiện đủ dữ liệu để được xếp hạng.** Sau bước lọc điều kiện bắt buộc và trước bước tính điểm có trọng số, hệ thống đếm số tiêu chí ưu tiên mà gia sư có dữ liệu, trong số các tiêu chí ưu tiên đang áp dụng của truy vấn đó (n; tiêu chí Đánh giá không tính vào n vì luôn dùng được nhờ giá trị trung tính 0,5). Nếu số tiêu chí có dữ liệu nhỏ hơn ngưỡng tối thiểu tương ứng với n (Bảng 3.7), gia sư bị loại khỏi kết quả xếp hạng của truy vấn này, ghi chú “Không đủ dữ liệu để xếp hạng” - không tính điểm trên phần dữ liệu ít ỏi còn lại. Công thức tính điểm của từng tiêu chí giữ nguyên, không đổi.

**Bảng 3.7 - Ngưỡng dữ liệu tối thiểu để được xếp hạng**

| Số tiêu chí ưu tiên đang áp dụng (n) | Ngưỡng tối thiểu phải có dữ liệu |
|:---:|:---:|
| 1 | 1 |
| 2 | 2 |
| 3 | 2 |
| 4 | 3 |
| 5 | 4 |

*Nguồn: thiết kế của nhóm (Mục 3.6); hiện thực tại `backend/app/scoring/eligibility.py` (MIN_DATA_THRESHOLD, kèm hàng n = 0 → ngưỡng 0), đối chiếu `docs/design/scoring-spec.md` mục 3 và 7.*

Ghi chú: hàng n = 5 được giữ nguyên nhưng không được kích hoạt, vì tiêu chí Đánh giá không tính vào n nên n tối đa là 4. Khi n = 0 (chỉ tiêu chí Đánh giá có trọng số lớn hơn 0), ngưỡng tối thiểu là 0, tức là không loại gia sư nào vì thiếu dữ liệu.

**Ví dụ tính điểm đầy đủ** (ví dụ minh họa công thức, không phải dữ liệu thực). Người học cần môn Toán, học Trực tiếp, khu vực KV1, ngân sách 200.000 đồng/giờ, khung giờ L = {T2-tối, T4-tối, T7-sáng}, mọi mức ưu tiên là “Trung bình” (w = 2). Một gia sư dạy Toán, hình thức “Cả hai”, dạy tại KV1, học phí 230.000, kinh nghiệm 4 năm, đánh giá 4,5 và giao được 2 trong 3 khung giờ sẽ vượt qua bước lọc, có các điểm thành phần: học phí 0,70; khu vực 1,00; kinh nghiệm 0,50; đánh giá 0,90; lịch rảnh 0,67. Điểm tổng S = (0,70 + 1,00 + 0,50 + 0,90 + 0,67) ÷ 5 ≈ 0,75 (không làm tròn từng thành phần, S = 113/150 ≈ 0,753 — cùng kết luận xếp hạng).

## 3.7. Kiến trúc hệ thống và luồng xử lý

### 3.7.1. Luồng xử lý ở mức logic bài toán

Luồng xử lý gồm tám bước, độc lập với công nghệ triển khai: (1) người học nhập nhu cầu và mức ưu tiên; (2) kiểm tra, chuẩn hóa tiêu chí đầu vào; (3) lọc các gia sư không thỏa điều kiện bắt buộc; (4) tính điểm phù hợp theo từng tiêu chí ưu tiên; (5) tổng hợp điểm theo trọng số; (6) xếp hạng các gia sư còn lại; (7) trả Top-k kèm điểm thành phần và lý do gợi ý; (8) người học điều chỉnh mức ưu tiên và xem thứ hạng thay đổi. Hình 3.1 minh họa luồng tám bước này; hình vẽ cũng thể hiện việc kiểm tra ngưỡng dữ liệu tối thiểu (Bảng 3.7) sau bước (3), cùng các nhánh thông báo khi không còn gia sư thỏa điều kiện bắt buộc, khi tổng trọng số bằng 0 và khi đầu vào không hợp lệ.

**Hình 3.1 - Sơ đồ luồng xử lý khuyến nghị**

*(Vẽ lại bằng draw.io — đặc tả ở Ghi chú biên tập cuối chương.)*

### 3.7.2. Kiến trúc ba lớp

Hệ thống gồm ba lớp: giao diện ReactJS nhận nhu cầu từ người học và gửi yêu cầu đến API; lớp API (FastAPI) tiếp nhận, kiểm tra hợp lệ, nạp danh sách gia sư mẫu từ `TutorRepository` rồi truyền cho module tính điểm; module tính điểm thực hiện quy trình ở mục 3.6 và trả danh sách đã xếp hạng để API phản hồi lại giao diện. Hình 3.2 mô tả ba lớp này.

**Hình 3.2 - Kiến trúc hệ thống ba lớp**

*(Vẽ lại bằng draw.io — đặc tả ở Ghi chú biên tập cuối chương.)*

Vì hệ thống chỉ có một luồng xử lý đi qua một module tính điểm và không có nhiều đối tượng nghiệp vụ tương tác qua nhiều lớp điều khiển, nhóm không áp dụng mô hình BCE (Boundary-Control-Entity) mà mô tả trực tiếp bằng sơ đồ luồng xử lý và một sơ đồ trình tự đơn giản: client → API → module tính điểm → trả kết quả (Hình 3.3).

**Hình 3.3 - Sơ đồ trình tự: client → API → module tính điểm → kết quả**

*(Vẽ lại bằng draw.io — đặc tả ở Ghi chú biên tập cuối chương.)*

## 3.8. Thiết kế giao diện

Giao diện demo gồm hai màn hình. Màn hình nhập nhu cầu cho phép chọn môn học, hình thức học, khu vực, ngân sách, khung thời gian rảnh và chọn mức ưu tiên (Không quan tâm / Thấp / Trung bình / Cao) cho từng tiêu chí (Hình 3.4). Màn hình kết quả hiển thị Top-k gia sư theo mã gia sư, kèm điểm phù hợp tổng, điểm từng tiêu chí và một biểu đồ thanh xếp chồng thể hiện đóng góp của từng tiêu chí, giúp người học hiểu vì sao một gia sư được xếp cao. Người học có thể đổi mức ưu tiên ngay tại màn hình kết quả để thấy danh sách xếp hạng lại (CN03) (Hình 3.5).

**Hình 3.4 - Phác thảo màn hình nhập nhu cầu**

*(Vẽ lại bằng draw.io — đặc tả ở Ghi chú biên tập cuối chương.)*

**Hình 3.5 - Phác thảo màn hình kết quả**

*(Vẽ lại bằng draw.io — đặc tả ở Ghi chú biên tập cuối chương.)*

---

**[GHI CHÚ BIÊN TẬP — XÓA TRƯỚC KHI GHÉP WORD]**

- **Câu cần trích dẫn học thuật:** Chương 3 không có câu khẳng định lĩnh vực nào trong danh sách rà soát (toàn bộ là thiết kế của nhóm).
- **Đặc tả vẽ lại 5 hình (draw.io; full chi tiết ở mục 6.3 của tài liệu rà soát Chương 1–3 — tệp `ra-soat-chuong-1-3.md` trên nhánh `docs/ra-soat-chuong-1-3`):**
  - **Hình 3.1** — 8 bước theo mục 3.7.1, kèm bước kiểm tra ngưỡng dữ liệu (Bảng 3.7) sau bước (3) và 3 nhánh thông báo: `no_match` (`recommend.py:60, 85`), `zero_weight` (`recommend.py:72`), đầu vào không hợp lệ 422 (`SearchRequest`; thông báo `api.js:179`); nhánh “thiếu dữ liệu” — `filter_eligible_candidates` (`eligibility.py:81`).
  - **Hình 3.2** — 3 lớp: giao diện ReactJS (`App.jsx`, `SearchPage.jsx`, `ResultPage.jsx`, `services/api.js`); API FastAPI (`backend/app/api/recommend.py`, `POST /api/recommend`, `backend/app/schemas/`); module tính điểm `backend/app/scoring/` — **module không tự đọc dữ liệu**; nạp dữ liệu do `recommend.py` thực hiện qua `TutorRepository` (`backend/app/data/repository.py`) từ `data/processed/tutors.json`/`tutors.csv` (quyết định 9.4).
  - **Hình 3.3** — trình tự với tên hàm thật: `fetchRecommendations` (`api.js:152`) → `POST /api/recommend` (`api.js:155`) → `recommend_tutors` (`recommend.py:47`) → `TutorRepository.get_all()` (`repository.py:32`) → `compute_effective_weights` (`weights.py:52`) → `filter_mandatory` (`filters.py:34`) → `filter_eligible_candidates` (`eligibility.py:81`) → `score_and_rank` (`ranker.py:157`, gọi 5 hàm `criteria.py:21-65` + `build_reason`/`build_notes` — `ranker.py:125, 118`) → phản hồi; nhánh CN03 lặp từ đầu (`requestSeqRef` — `App.jsx:52`).
  - **Hình 3.4** — vẽ **theo phạm vi Mục 3.8** (quyết định 9.3): biểu mẫu theo Bảng 3.4 (Môn học*, Hình thức học*, Khu vực mong muốn, Ngân sách tối đa/giờ kèm dòng quy đổi bằng chữ, Top-k, khung thời gian rảnh 7 ngày × 3 buổi) + khối mức ưu tiên 5 tiêu chí × 4 mức theo Bảng 3.5 + thông báo kiểm tra hợp lệ (`SearchPage.jsx:231, 241, 248`); các thành phần demo mở rộng (banner hero, thanh 14 kịch bản, ô “Mục tiêu học tập”) **không đưa vào** — thuộc Hình 4.1 của Chương 4.
  - **Hình 3.5** — vẽ **theo phạm vi Mục 3.8**: danh sách Top-k (`TutorCard`: hạng, điểm S(g), thanh xếp chồng C_i, “Lý do gợi ý”), rail CN03 5 hàng tiêu chí, trạng thái `no_match` (“Không tìm thấy gia sư thỏa mãn điều kiện” — `ResultPage.jsx:459`) và `zero_weight` (“Không thể xếp hạng do tổng trọng số bằng 0” — `:424`); dải KPI/phễu, chip độ trễ, huy hiệu đổi hạng, hộp “Nạp nhanh trọng số” **không đưa vào** — thuộc Hình 4.2–4.4 của Chương 4.
- **Số hiệu bảng mới:** bảng ngưỡng được đánh số **Bảng 3.7** (đề cương để không đánh số, chỉ ghi “bảng dưới”) — cập nhật “DANH MỤC BẢNG BIỂU” khi ghép Word; các dẫn chiếu “bảng dưới” trong văn bản đã đổi thành “Bảng 3.7”.
- **Sửa so với đề cương (ý không đổi):** mục 3.5 câu đầu bỏ nhắc SQLite (quyết định 9.2); “không phải cấu hình tối ưu” → “không phải bộ cấu hình đã được kiểm chứng” (từ cấm); mục 3.6 ví dụ tính điểm thêm “(không làm tròn từng thành phần, S = 113/150 ≈ 0,753)” (khớp `backend/tests/unit/test_ranker.py:84-86`); mục 3.7.2 sửa cụm “module tính điểm đọc dữ liệu gia sư mẫu” → lớp API nạp từ `TutorRepository` rồi truyền cho module (quyết định 9.4); đổi thì “Nhóm sẽ kiểm tra… sẽ được kiểm tra” → “Nhóm kiểm tra… được kiểm tra” (thực nghiệm Chương 5 đã thực hiện).
- **Câu bổ sung so với đề cương (dẫn chiếu theo report_standards Mục 4.2):** các câu nhắc Bảng 2.1/3.7 và Hình 3.1–3.5 trong thân văn bản; câu hiệu năng ở 3.3 dẫn về mục 5.1.2.
- **Điều kiện rút gọn:** câu mô tả Hình 3.1 ở mục 3.7.1 (“hình vẽ cũng thể hiện…”) giả định hình vẽ lại theo đặc tả trên; nếu nhóm quyết định giữ ảnh cũ của đề cương thì gỡ vế này.
- **Điểm chờ nhóm quyết định:** (e) nhãn `estimated` của trường nguồn_dữ_liệu (Bảng 3.3 vẫn 2 giá trị như đề cương — xem `data/README.md` mục 3); (i) bổ sung 1–2 câu ghi nhận thành phần demo mở rộng vào mục 3.8.
- **Dòng Nguồn dưới bảng:** các tệp mã nguồn được dẫn đã kiểm chứng tồn tại (`config.py`, `criteria.py`, `eligibility.py`, `data-dictionary.md`, `scoring-spec.md`); khi ghép Word, dòng Nguồn đặt ngay dưới bảng, cỡ chữ 10–11 pt.
