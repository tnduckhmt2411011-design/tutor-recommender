# Slide thuyết trình bảo vệ đồ án — Bộ 40 slide (Hybrid Academic-Keynote)

> [!NOTE]
> Kịch bản gồm **40 slide** bám sát bố cục **6 phần** ở Slide 2 (*Nội dung trình bày*), kèm **6 slide giới thiệu đầu mỗi phần** (`Slide 3`, `Slide 7`, `Slide 11`, `Slide 23`, `Slide 30`, `Slide 36`). Nội dung hiển thị trên slide được tinh gọn nhẹ mắt theo chuẩn thuyết trình (giữ mọi con số, công thức, dẫn chứng cốt lõi), còn phần phân tích chi tiết giữ trọn trong mục **Lời thoại** (Speaker Notes). Mọi số liệu, công thức, ký hiệu bảng/hình đều đồng bộ với bản báo cáo hoàn chỉnh.

## 0. Thông tin chung

- **Thời lượng chuẩn:** 15–18 phút trình bày + 4 phút demo (chạy xen ngay sau Slide 29 hoặc dùng 4 ảnh Hình 4.1–4.4) + 5–10 phút hỏi đáp.
- **Phương án rút gọn nếu Hội đồng giới hạn 12–14 phút:** lướt nhanh 10 giây ở các slide giới thiệu đầu phần, tóm gọn phần công thức chi tiết ở Slide 16–18, và chạy demo 3 phút theo [kich-ban-demo-bao-ve.md](kich-ban-demo-bao-ve.md).
- **Tên đề tài chuẩn (dùng thống nhất trên Slide 1 và Slide 40):** HỆ THỐNG KHUYẾN NGHỊ GIA SƯ DỰA TRÊN PHƯƠNG PHÁP CONTENT-BASE FILTERING.
- **Điều phối thuyết trình nội bộ (không hiển thị lên slide):**
  - **Cao Khánh Ngọc:** Mở đầu (Slide 1–2), Phần 1 (Slide 3–6), Phần 2 (Slide 7–10), Phần 6 (Slide 36–40).
  - **Trần Nguyễn Đức:** Phần 3 (Slide 11–22), Phần 5 (Slide 30–35).
  - **Lê Thị Bích Chuyền:** Phần 4 (Slide 23–29) và thao tác demo trực tiếp.
- **Quy ước trình bày:** cỡ chữ nội dung `16,5–18 pt`, bảng `13,5–15 pt`, nhãn chú thích tối thiểu `11,25 pt`; số thập phân dùng dấu phẩy (`0,5`, `3,54 ms`), hàng nghìn dùng dấu chấm (`200.000 VNĐ/giờ`, `1.000 ms`).

---

## Slide 1 — Trang bìa

**Trên slide**

- **Đơn vị:** Trường Đại học Kỹ thuật - Công nghệ Cần Thơ — Khoa Công nghệ Thông tin.
- **Học phần:** Báo cáo Đồ án môn Khoa học máy tính 1.
- **Đề tài:** HỆ THỐNG KHUYẾN NGHỊ GIA SƯ DỰA TRÊN PHƯƠNG PHÁP CONTENT-BASE FILTERING.
- **GVHD:** TS. Lê Anh Nhã Uyên.
- **Nhóm thực hiện:** Cao Khánh Ngọc (`KHMT2411025`), Trần Nguyễn Đức (`KHMT2411011`), Lê Thị Bích Chuyền (`KHMT2411037`) — Lớp KHMT 2024 (Cần Thơ, tháng 11/2026).

**Lời thoại**

“Kính thưa quý thầy cô trong Hội đồng. Nhóm em gồm ba thành viên đến từ lớp Khoa học máy tính 2024, hôm nay xin trình bày đồ án môn Khoa học máy tính 1 với đề tài *Hệ thống khuyến nghị gia sư dựa trên phương pháp Content-Base Filtering*, dưới sự hướng dẫn của cô TS. Lê Anh Nhã Uyên. Em là Cao Khánh Ngọc, xin đại diện nhóm bắt đầu phần trình bày.”

**Hình/bảng minh họa:** Logo CTUT (`logo_ctut.png`) và ảnh minh họa Editorial/Bauhaus bên phải (`cover_right_illustration.png`).

---

## Slide 2 — Nội dung trình bày theo 6 phần

**Trên slide**

1. **01 · Tổng quan về đề tài:** Bối cảnh 7 đặc trưng, khảo sát hiện trạng và mục tiêu.
2. **02 · Cơ sở lý thuyết và công nghệ:** Content-Based Filtering, công thức (2.1) và công nghệ.
3. **03 · Phân tích và thiết kế hệ thống:** Yêu cầu, dữ liệu, ngưỡng, hàm điểm và kiến trúc.
4. **04 · Xây dựng hệ thống và minh họa UI:** Module scoring, API và giao diện React CN01–CN03.
5. **05 · Kiểm thử và đánh giá thực nghiệm:** 200 bài TDD, ca biên, 14 kịch bản và độ nhạy.
6. **06 · Kết luận và hướng phát triển:** Mở rộng theo góp ý GVHD, Vercel/Render và hướng đi.

**Lời thoại**

“Bài trình bày của nhóm em bám sát sáu phần chính trong báo cáo: mở đầu là tổng quan bài toán và hiện trạng; tiếp theo là cơ sở lý thuyết về Content-Based Filtering và cách chọn công nghệ; phần ba và bốn đi vào phân tích thiết kế cùng phần cài đặt hệ thống thực tế; phần năm báo cáo kết quả kiểm thử và thực nghiệm trên 14 kịch bản; cuối cùng là kết quả mở rộng, hạn chế và hướng phát triển.”

**Hình/bảng minh họa:** Lưới 6 khối chỉ mục vát góc.

---

## PHẦN 1: TỔNG QUAN VỀ ĐỀ TÀI

## Slide 3 — [Giới thiệu Phần 1] Tổng quan về đề tài

**Trên slide**

- **Lộ trình:** `[1. Tổng quan]` → 2. Lý thuyết & CN → 3. Phân tích & TK → 4. Xây dựng HT → 5. Kiểm thử & ĐG → 6. Kết luận.
- **Nội dung trọng tâm:**
  - Bối cảnh 7 đặc trưng và xung đột tiêu chí.
  - Khảo sát 3 nền tảng thực tế và GS360 [3].
  - Mục tiêu, phạm vi và quỹ 300 giờ nhóm.
- **Câu hỏi dẫn dắt:** *Vì sao lọc từng điều kiện riêng lẻ vẫn chưa giúp người học chọn nhanh được gia sư phù hợp?*

**Lời thoại**

“Nhóm em xin bước vào Phần 1: Tổng quan về đề tài. Trong phần này, chúng em làm rõ xuất phát điểm thực tế của bài toán, khoảng trống qua khảo sát các kênh hiện có và phạm vi mục tiêu nhóm đăng ký.”

**Hình/bảng minh họa:** Thanh lộ trình 6 phần (làm sáng Phần 1).

---

## Slide 4 — Bối cảnh và bài toán tìm gia sư đa tiêu chí

**Trên slide**

- **Bài toán 7 đặc trưng:** Môn học, hình thức, khu vực, học phí, lịch rảnh, kinh nghiệm, đánh giá.
- **Hạn chế lọc nhị phân:** Nới rộng thì danh sách quá dài; siết chặt dễ trả về rỗng.
- **Nhu cầu cốt lõi:** Xếp hạng đa tiêu chí có trọng số, tính mềm ngân sách và giải thích lý do.

**Lời thoại**

“Khi tìm gia sư, phụ huynh và học sinh hiếm khi gặp một lựa chọn đạt điểm tuyệt đối ở mọi mặt. Thực tế các tiêu chí hay mâu thuẫn nhau: người dạy phí mềm thì ít kinh nghiệm, còn người nhiều kinh nghiệm thì học phí lại cao hơn ngân sách dự kiến. Nếu chỉ dùng bộ lọc đạt hay không đạt, danh sách trả về hoặc còn rất nhiều hồ sơ phải tự so sánh bằng mắt, hoặc bị rỗng vì vượt nhẹ ngân sách. Đó là bài toán ra quyết định đa tiêu chí mà đề tài hướng tới.”

**Hình/bảng minh họa:** Sơ đồ xung đột 4 đỉnh quanh 7 đặc trưng (Mục 1.1).

---

## Slide 5 — Khảo sát hiện trạng và khoảng trống nghiên cứu

**Trên slide**

- **Bảng 1.1 & GS360 [3]:**
  - `Hội nhóm FB & Trung tâm`: Tin rời rạc, ghép cặp thủ công.
  - `giasudatviet.com`: Chỉ chia trang theo môn, thiếu xếp hạng điểm.
  - `giasudantri.vn`: Bài giới thiệu rời rạc, ít chiều lọc cấu trúc.
  - `daythem.com`: Lọc môn/lịch, xếp theo thời gian hoạt động.
  - Đồ án `GS360 [3]`: Quản lý toàn trình, thiếu bộ chấm điểm `[0,1]`.
- **Khoảng trống lựa chọn:** Bộ máy xếp hạng có trọng số nằm giữa bước lọc và quyết định chọn.

**Lời thoại**

“Nhóm em khảo sát trực tiếp ba trang phổ biến vào tháng 9 năm 2026 như ở Bảng 1.1, cho thấy phần lớn mới dừng ở phân loại theo môn hoặc lọc theo lịch như daythem.com, chứ chưa có điểm tổng hợp nhiều tiêu chí hay lý do gợi ý. Ngoài ra, nhóm cũng tham khảo đồ án cơ sở GS360 — một hệ thống quản lý đầy đủ quy trình đặt lịch và thanh toán nhưng không chuyên về xếp hạng. Từ đó nhóm xác định rõ khoảng trống đồ án giải quyết là bộ máy khuyến nghị giải thích được.”

**Hình/bảng minh họa:** Bảng 1.1 (Mục 1.2) và luồng khoảng trống nghiên cứu.

---

## Slide 6 — Mục tiêu, phạm vi đề tài và kế hoạch 300 giờ

**Trên slide**

- **4 mục tiêu (Mục 1.4):** Module tính điểm · Dịch vụ API FastAPI · Giao diện React CN01–CN03 · Thực nghiệm KB01–KB14.
- **Phạm vi & ranh giới:** 1 tác nhân người học, 1 môn/truy vấn, 16 hồ sơ mẫu; không cài đặt tài khoản, đặt lịch, thanh toán.
- **Quỹ thời gian (Bảng 1.2):** `100 giờ/TV` (`300 giờ` nhóm), trọng tâm C3–C4 (`60%`) và C5 (`16%`).

**Lời thoại**

“Với học phần hai tín chỉ, nhóm em chủ động giới hạn phạm vi ở bộ máy khuyến nghị, dịch vụ API và giao diện hai màn hình minh họa; không ôm đồm phần đăng nhập hay thanh toán. Tổng quỹ thời gian là 100 giờ cho mỗi thành viên như ở Bảng 1.2, trong đó 60% dành cho thiết kế thuật toán và xây dựng hệ thống để bảo đảm phần thực nghiệm đủ chiều sâu.”

**Hình/bảng minh họa:** Bảng 1.2 (Mục 1.5).

---

## PHẦN 2: CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ

## Slide 7 — [Giới thiệu Phần 2] Cơ sở lý thuyết và công nghệ

**Trên slide**

- **Lộ trình:** 1. Tổng quan → `[2. Lý thuyết & CN]` → 3. Phân tích & TK → 4. Xây dựng HT → 5. Kiểm thử & ĐG → 6. Kết luận.
- **Nội dung trọng tâm:**
  - Đối chiếu 3 phương pháp khuyến nghị (Bảng 2.1).
  - Content-Based cấu trúc & công thức `(2.1)`.
  - Tác động trọng số (`Bảng 2.2`) & công nghệ cài đặt.
- **Câu hỏi dẫn dắt:** *Vì sao chọn Content-Based Filtering kết hợp Weighted Scoring khi hệ thống chưa có dữ liệu lịch sử?*

**Lời thoại**

“Tiếp theo, em xin chuyển sang Phần 2: Cơ sở lý thuyết và công nghệ, giải thích cơ sở lựa chọn thuật toán và công cụ cài đặt của nhóm.”

**Hình/bảng minh họa:** Thanh lộ trình 6 phần (làm sáng Phần 2).

---

## Slide 8 — So sánh ba hướng tiếp cận Hệ thống khuyến nghị

**Trên slide**

- **Bảng 2.1 [2]:** `Content-Based` (khớp thuộc tính, **chọn**), `Collaborative Filtering` (cần lịch sử, *cold-start*), `Hybrid` (hướng nâng cấp).
- **Lợi thế Content-Based:** Hoạt động từ ngày đầu trên 7 thuộc tính, minh bạch từng điểm số.

**Lời thoại**

“Theo khảo sát phân loại của Adomavicius và Tuzhilin như trong Bảng 2.1, lọc cộng tác đòi hỏi lịch sử tương tác đủ lớn của nhiều người dùng, nếu áp dụng cho hệ thống mới sẽ vấp ngay tình trạng cold-start. Ngược lại, Content-Based Filtering khai thác trực tiếp đặc trưng hồ sơ gia sư và nhu cầu vừa nhập của người học, nên triển khai khả thi và không cần dữ liệu lịch sử.”

**Hình/bảng minh họa:** Bảng 2.1 (Mục 2.1) + 3 thẻ nhận định.

---

## Slide 9 — Content-Based cấu trúc & Công thức Weighted Scoring (2.1)

**Trên slide**

- **Không dùng cosine similarity:** Hỗn hợp tập hợp, phân loại, số thực ngưỡng mềm và giao khung giờ.
- **Hai pha:** Lọc điều kiện bắt buộc → Chấm điểm $[0, 1]$ và tổng hợp.
- **Công thức Weighted Scoring (2.1) [1]:** $S(g) = \frac{\sum_{i \in A} w_i \times s_i(g)}{\sum_{j \in A} w_j}$; đóng góp $C_i = \frac{w_i \times s_i(g)}{\sum_{j \in A} w_j}$ với $\sum_{i \in A} C_i = S(g)$.

**Lời thoại**

“Do bảy đặc trưng hồ sơ mang bản chất dữ liệu khác nhau, nhóm em không ép thành một vector để tính độ tương đồng cosine mà chuẩn hóa riêng từng tiêu chí về đoạn từ 0 đến 1, sau đó tổng hợp theo công thức Weighted Scoring (2.1). Những điều kiện cứng như đúng môn hay hình thức học được lọc trước để tránh tình trạng điểm cao ở mặt này bù cho việc dạy sai môn ở mặt kia.”

**Hình/bảng minh họa:** Công thức (2.1) (Mục 2.3).

---

## Slide 10 — Ảnh hưởng trọng số (Bảng 2.2) & Công nghệ sử dụng

**Trên slide**

- **Biểu đồ dốc Bảng 2.2:** Đổi trọng số `3:1:1` sang `1:3:1` đảo hạng ngay trên 3 gia sư (`A: 0,76→0,36`, `B: 0,74→0,90`, `C: 0,64→0,88`).
- **Backend:** Python 3.12 · FastAPI [4] · Pydantic v2.
- **Frontend & Lưu trữ:** React 19 [5] · Vite · JSON & CSV đối chiếu.

**Lời thoại**

“Bảng 2.2 minh họa rõ vai trò của trọng số: chỉ cần chuyển ưu tiên từ học phí sang khu vực, thứ hạng của ba gia sư đã đảo chiều ngay. Vì trọng số phản ánh nhu cầu chủ quan của từng người học, hệ thống phải cho phép chỉnh trực tiếp trọng số ngay trên giao diện. Về công nghệ, nhóm chọn FastAPI kết hợp Pydantic cho tầng máy chủ và React với Vite cho giao diện. Tiếp theo, bạn Trần Nguyễn Đức sẽ trình bày Phần 3 về phân tích và thiết kế hệ thống.”

**Hình/bảng minh họa:** Biểu đồ dốc Bảng 2.2 (Mục 2.3) & thẻ công nghệ (Mục 2.4).

---

## PHẦN 3: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG

## Slide 11 — [Giới thiệu Phần 3] Phân tích và thiết kế hệ thống

**Trên slide**

- **Lộ trình:** 1. Tổng quan → 2. Lý thuyết & CN → `[3. Phân tích & TK]` → 4. Xây dựng HT → 5. Kiểm thử & ĐG → 6. Kết luận.
- **Nội dung trọng tâm:**
  - Chức năng CN01–CN03 & 4 phi chức năng.
  - 7 đặc trưng, dữ liệu & 5 hàm chuẩn hóa điểm.
  - Lưu đồ 8 bước, kiến trúc 3 lớp, UML & phác thảo UI.
- **Câu hỏi dẫn dắt:** *Hệ thống chuẩn hóa 5 tiêu chí khác đơn vị đo như thế nào và xử lý các tình huống thiếu dữ liệu ra sao?*

**Lời thoại**

“Kính thưa Hội đồng, em là Trần Nguyễn Đức, xin trình bày Phần 3: Phân tích và thiết kế hệ thống — trọng tâm kỹ thuật để biến mô hình điểm thành đặc tả cài đặt được.”

**Hình/bảng minh họa:** Thanh lộ trình 6 phần (làm sáng Phần 3).

---

## Slide 12 — Yêu cầu chức năng CN01–CN03 (Bảng 3.1)

**Trên slide**

- **CN01 (Nhập nhu cầu):** Chọn môn, hình thức, khu vực, học phí, lịch `7×3`, 4 mức ưu tiên `{0..3}` cho 5 tiêu chí → `SearchRequest`.
- **CN02 (Top-k & Giải thích):** Lọc cứng → chấm `[0,1]` → thanh đóng góp $C_i$ + câu lý do + nhãn *Thực tế (ước tính \*)*.
- **CN03 (Tinh chỉnh tức thì):** Đổi ưu tiên trực tiếp trên trang kết quả, tự xếp lại kèm huy hiệu `↑ / ↓`.

**Lời thoại**

“Hệ thống xoay quanh đúng ba chức năng cốt lõi CN01, CN02 và CN03 ở Bảng 3.1, tạo thành một vòng lặp khép kín: người học nhập nhu cầu ở CN01, kiểm chứng từng phần trăm đóng góp ở CN02 rồi đổi trọng số trực tiếp trên CN03 để thấy ngay thứ hạng thay đổi.”

**Hình/bảng minh họa:** Luồng 3 thẻ CN01 → CN02 → CN03 (Bảng 3.1, Mục 3.2).

---

## Slide 13 — Bốn yêu cầu phi chức năng cốt lõi (Mục 3.3)

**Trên slide**

- **P1 · Hiệu năng (`< 1.000 ms`):** Đo `140` lượt TestClient đạt TB `3,54 ms`, chậm nhất `7,97 ms`.
- **P2 · Độc lập (`Tách lõi`):** 5 module thuần túy Python, chạy `pytest` không cần tầng web.
- **P3 · Giải thích (`100% C_i`):** Tổng cộng tính $\sum C_i = S(g)$ khớp từng đoạn thanh màu.
- **P4 · Tái lập (`Tất định`):** Khóa tham số cấu hình và phá hòa `tutor_id` tăng dần.

**Lời thoại**

“Về bốn yêu cầu phi chức năng ở Mục 3.3, nhóm đặt ngưỡng phản hồi dưới 1 giây để thao tác đổi trọng số ở CN03 diễn ra tức thì, đồng thời tách hoàn toàn lõi tính điểm khỏi FastAPI để dễ kiểm thử độc lập, minh bạch toàn bộ đóng góp C_i và bảo đảm kết quả tái lập tất định.”

**Hình/bảng minh họa:** Lưới 4 chỉ số phi chức năng P1–P4 (Mục 3.3).

---

## Slide 14 — Phân loại 7 đặc trưng và Cấu trúc dữ liệu

**Trên slide**

- **Bảng 3.2:** Lọc cứng (`Môn học`, `Hình thức`, `|L ∩ T| ≥ 1`) · Chấm điểm `[0,1]` (`Lịch rảnh`, `Học phí mềm δ=0,5`, `Khu vực tắt khi online`, `Kinh nghiệm E_max=8`, `Đánh giá null→0,5`).
- **`TutorProfile` (Bảng 3.3 — 9 trường):** Kèm `avg_rating` (`điểm_đánh_giá_tb`) nullable và `data_source` (`nguồn_dữ_liệu`), đối khớp `100% CSV ↔ JSON`.
- **`SearchRequest` (Bảng 3.4 — 7 trường):** `priorities[5] ∈ {0..3}`, `top_k` (`số_kết_quả`) mặc định `3` (`[1, 20]`), chặn trường thừa (`extra=forbid`) ở biên `422`.

**Lời thoại**

“Bảng 3.2 tách rạch ròi ba điều kiện bắt buộc với năm tiêu chí ưu tiên; riêng lịch rảnh đóng hai vai trò: phải giao ít nhất một ca mới qua lọc, còn giao nhiều ca hơn thì nhận điểm thành phần cao hơn. Bảng 3.3 và 3.4 định nghĩa cấu trúc phẳng cho hồ sơ gia sư và truy vấn người học, có tách trường nguồn dữ liệu để phân biệt hồ sơ thu thập công khai với hồ sơ giả lập.”

**Hình/bảng minh họa:** Bảng 3.2–3.4 (Mục 3.4–3.5).

---

## Slide 15 — Quy đổi mức ưu tiên và Ngưỡng dữ liệu tối thiểu

**Trên slide**

- **Bảng 3.5:** Bỏ qua (`0`) · Thấp (`1`) · Trung bình (`2`, mặc định CN01) · Cao (`3`) — chuẩn hóa động không cần tổng `100%`.
- **Ngưỡng Bảng 3.7:** Với $n \in \{1..5\}$ tiêu chí hiệu lực (`w_i > 0`, trừ Đánh giá gán trung tính `0,500`), số trường tối thiểu là **`1, 2, 2, 3, 4`** (`∑w_i = 0 ⇒ zero_weight`; `n = 0` chỉ Đánh giá `⇒` ngưỡng `0`).
- Hồ sơ dưới ngưỡng tách vào `insufficient_data_candidates`; nếu `0` hồ sơ đạt `⇒` `no_match` biến thể `2`.

**Lời thoại**

“Để người dùng dễ thao tác, hệ thống đưa ra bốn mức ưu tiên rời rạc quy đổi sang số nguyên từ 0 đến 3 ở Bảng 3.5. Bên cạnh đó, nhằm tránh việc một hồ sơ chỉ điền 1 tiêu chí nhưng lại đạt điểm trung bình rất cao và lọt lên đầu bảng, nhóm thiết kế bảng ngưỡng dữ liệu tối thiểu 3.7: ví dụ truy vấn áp dụng 4 tiêu chí thì hồ sơ phải có dữ liệu ít nhất 3 tiêu chí mới được đưa vào xếp hạng.”

**Hình/bảng minh họa:** Bảng 3.5 & Bảng 3.7 (Mục 3.5–3.6).

---

## Slide 16 — Công thức điểm — Phần 1: Học phí & Khu vực

**Trên slide**

- **Học phí (`δ = 0,5`):** `1` nếu $P \le B$; giảm tuyến tính về `0` khi $P \ge 1{,}5B$ (ví dụ `B = 200k, P = 230k ⇒ 0,70`); $B = 0 \Rightarrow$ không chia 0.
- **Khu vực:** `1` nếu khớp quận K, ngược lại `0`.
- **Tự tắt `online` (QĐ-C):** Học trực tuyến tự đặt $w_{\text{district}} = 0$.

**Lời thoại**

“Hai slide tiếp theo trình bày năm hàm điểm thành phần ở Bảng 3.6. Điểm nhấn ở hàm Học phí là cơ chế dung sai mềm với $\delta = 0{,}5$: gia sư vượt ngân sách trong phạm vi 50% vẫn giữ lại điểm giảm dần tuyến tính để không bỏ sót ứng viên tốt chỉ vì nhỉnh hơn vài chục nghìn; vượt quá ngưỡng này điểm mới về 0. Với Khu vực, tiêu chí tự động loại khỏi mẫu số khi học trực tuyến hoặc khi người học không chọn quận.”

**Hình/bảng minh họa:** Đồ thị đường gấp khúc $s_{\text{fee}}$ (Bảng 3.6).

---

## Slide 17 — Công thức điểm — Phần 2: KN, ĐG, Lịch & Khuyết dữ liệu

**Trên slide**

- **Kinh nghiệm:** $\min(E \div 8, 1)$ · **Đánh giá:** $R \div 5$ (mặc định trung tính `0,500` nếu `null`) · **Lịch rảnh:** $\lvert L \cap T \rvert \div \lvert L \rvert$.
- **Xử lý khuyết sau Bảng 3.7:** Thiếu học phí/KN gán $s_i = 0$ nhưng giữ $w_i$ ở mẫu số để ứng viên đủ hồ sơ luôn xếp trên; riêng khuyết đánh giá nhận `0,500` tránh bất lợi cho gia sư mới.

**Lời thoại**

“Với Kinh nghiệm, nhóm dùng mốc bão hòa 8 năm để chênh lệch giữa 15 và 20 năm không làm méo bảng điểm. Với Đánh giá, gia sư mới chưa có lượt chấm nhận giá trị trung tính 0,5 và luôn kèm ghi chú công khai trên thẻ. Còn khi thiếu học phí hoặc kinh nghiệm nhưng vẫn vượt ngưỡng Bảng 3.7, hệ thống gán s_i bằng 0 và giữ nguyên w_i ở mẫu số để ứng viên đầy đủ dữ liệu luôn xếp trên.”

**Hình/bảng minh họa:** Bảng 3.6 & quy tắc xử lý khuyết sau Bảng 3.7.

---

## Slide 18 — Ví dụ tính tay minh họa Mục 3.6 (S = 113/150 ≈ 0,753)

**Trên slide**

- **Đầu vào (`w_i = 2` đều nhau → rút gọn `÷ 5`):** Phí `0,70` · Quận `1,00` · KN `0,50` · ĐG `0,90` · Lịch `2/3`.
- **Tổng hợp & đóng góp $C_i$:** $S(g) = \dfrac{0{,}70 + 1{,}00 + 0{,}50 + 0{,}90 + 2/3}{5} = \dfrac{113}{150} \approx 0{,}753$ (`0,140 + 0,200 + 0,100 + 0,180 + 0,133`).
- **Đối chiếu:** Khớp `100%` giữa tính tay Mục 3.6 và lõi Python `backend/app/scoring/`.

**Lời thoại**

“Để minh họa trực quan phép tính, xét ví dụ trong Mục 3.6 với cả năm tiêu chí đặt mức Trung bình nên rút gọn còn chia đều cho 5. Cộng năm điểm thành phần 0,70; 1,00; 0,50; 0,90 và 2/3 ta thu được tổng S(g) bằng đúng phân số 113/150, xấp xỉ 0,753, đồng thời tách được chính xác từng phần trăm C_i khớp hoàn toàn với lõi Python.”

**Hình/bảng minh họa:** Bảng 5 thẻ đầu vào, phân số tổng hợp & thanh cộng tính $C_i$ (Mục 3.6).

---

## Slide 19 — Sơ đồ luồng xử lý khuyến nghị 8 bước (Hình 3.1)

**Trên slide**

- **Lưu đồ ISO 5807 (Hình 3.1):**
  1. Kiểm tra đầu vào CN01 (lỗi trả `HTTP 422`).
  2. Nạp 16 hồ sơ & lọc điều kiện bắt buộc (`no_match` biến thể 1).
  3. Kiểm tra tổng trọng số ($\sum w_i = 0 \Rightarrow$ `zero_weight`).
  4. Lọc ngưỡng dữ liệu Bảng 3.7 (`no_match` biến thể 2).
  5. Chấm điểm, phá hòa `tutor_id`, trả Top-$k$ & vòng lặp CN03.

**Lời thoại**

“Hình 3.1 vẽ toàn bộ luồng xử lý 8 bước theo chuẩn ISO 5807 cùng 5 nút rẽ nhánh kiểm soát biên. Thứ tự kiểm tra tổng trọng số bằng 0 trước bước ngưỡng dữ liệu là một điểm kỹ thuật quan trọng, giúp trạng thái zero_weight luôn trả về đúng danh sách ứng viên đã đạt điều kiện bắt buộc dù người học tắt hết ưu tiên.”

**Hình/bảng minh họa:** Hình 3.1 (`hinh-3-1-luong-xu-ly-khuyen-nghi.png`).

---

## Slide 20 — Kiến trúc hệ thống 3 lớp (Hình 3.2)

**Trên slide**

- **Tầng giao diện (React SPA):** Nhập CN01, hiển thị Top-$k$ CN02 và tinh chỉnh trọng số CN03.
- **Tầng dịch vụ API (FastAPI):** Đón `POST /api/recommend`, xác thực Pydantic, điều phối `TutorRepository`.
- **Tầng lõi (`scoring`):** Thuần Python tách rời hoàn toàn khỏi tầng web HTTP.

**Lời thoại**

“Hình 3.2 trình bày kiến trúc 3 lớp của hệ thống. Điểm cốt lõi là toàn bộ nghiệp vụ tính điểm nằm gọn trong tầng scoring thuần Python, chỉ giao tiếp qua cấu trúc dữ liệu sạch với tầng dịch vụ FastAPI và TutorRepository, giúp cô lập hoàn toàn khỏi khung web khi kiểm thử hay tái sử dụng.”

**Hình/bảng minh họa:** Hình 3.2 (`hinh-3-2-kien-truc-ba-lop.png`).

---

## Slide 21 — Sơ đồ trình tự UML 2.5 (Hình 3.3)

**Trên slide**

- **Chuỗi gọi hàm 5 bước (Hình 3.3):**
  1. `TutorRepository.get_all()` nạp kho 16 hồ sơ.
  2. `filter_mandatory()` loại ứng viên lệch điều kiện cứng.
  3. `compute_effective_weights()` tính trọng số & tắt Khu vực nếu `online`.
  4. `filter_eligible_candidates()` tách hồ sơ dưới ngưỡng Bảng 3.7.
  5. `score_and_rank()` trả danh sách xếp hạng, API bọc thành `RecommendationResponse` cho React UI.

**Lời thoại**

“Trên sơ đồ trình tự UML 2.5 ở Hình 3.3, mỗi yêu cầu từ màn hình React đi qua đúng năm bước xử lý (nạp dữ liệu và bốn hàm thuần tính điểm) theo thứ tự bất biến: lấy dữ liệu, lọc cứng, quy đổi trọng số hiệu dụng, kiểm tra ngưỡng dữ liệu và cuối cùng là chấm điểm, phá hòa rồi trả phản hồi về giao diện.”

**Hình/bảng minh họa:** Hình 3.3 (`hinh-3-3-so-do-trinh-tu.png`).

---

## Slide 22 — Phác thảo giao diện 2 màn hình (Hình 3.4 & 3.5)

**Trên slide**

- **Hình 3.4 (CN01):** Biểu mẫu nhu cầu, lưới lịch `7×3` và 5 bộ chọn mức ưu tiên.
- **Hình 3.5 (CN02 & CN03):** Thẻ kết quả Top-$k$, thanh xếp chồng $C_i$ và khung tinh chỉnh tại chỗ.

**Lời thoại**

“Từ đặc tả chức năng, nhóm phác thảo trước hai màn hình giao diện như Hình 3.4 và Hình 3.5 để thống nhất bố cục trực quan: màn hình CN01 gom nhu cầu và lịch rảnh 7×3, còn màn hình kết quả đặt bảng tinh chỉnh CN03 ngay cạnh các thanh đóng góp $C_i$. Tiếp theo, bạn Lê Thị Bích Chuyền sẽ trình bày Phần 4 về quá trình cài đặt và giao diện thực tế.”

**Hình/bảng minh họa:** Hình 3.4 (`hinh-3-4-phac-thao-nhap-nhu-cau.png`) và Hình 3.5 (`hinh-3-5-phac-thao-ket-qua.png`).

---

## PHẦN 4: XÂY DỰNG HỆ THỐNG VÀ MINH HỌA GIAO DIỆN

## Slide 23 — [Giới thiệu Phần 4] Xây dựng hệ thống và minh họa giao diện

**Trên slide**

- **Lộ trình:** 1. Tổng quan → 2. Lý thuyết & CN → 3. Phân tích & TK → `[4. Xây dựng HT]` → 5. Kiểm thử & ĐG → 6. Kết luận.
- **Nội dung trọng tâm:**
  - Môi trường khóa phiên bản & bộ 16 hồ sơ mẫu.
  - Module `scoring` độc lập (`QĐ-A–QĐ-E`) & API REST.
  - Giao diện thực tế `CN01–CN03` và trình diễn live.
- **Câu hỏi dẫn dắt:** *Hệ thống hiện thực thuật toán thành ứng dụng hoàn chỉnh và trực quan hóa lời giải thích như thế nào?*

**Lời thoại**

“Kính thưa Hội đồng, em là Lê Thị Bích Chuyền. Em xin trình bày Phần 4: Xây dựng hệ thống và minh họa giao diện, đi từ bộ dữ liệu mẫu, cách cài đặt module backend cho tới ứng dụng web React hoàn chỉnh.”

**Hình/bảng minh họa:** Thanh lộ trình 6 phần (làm sáng Phần 4).

---

## Slide 24 — Môi trường phát triển và Bộ dữ liệu 16 hồ sơ

**Trên slide**

- **Bảng 4.1:** Backend Python `3.12.7` · FastAPI `0.162.0` · Pydantic `2.14.2` | Frontend Node `v24.19.0` · React `19.3.1` · Vite `8.3.5` · `motion 14.9.0`.
- **Bộ 16 hồ sơ (Bảng A.1):** Phủ 9 môn; 14 giả lập (`simulated`) + 2 công khai ẩn danh (`GS-T06`, `GS-T07` — `public_collected`, gắn `(*)` và `null` đánh giá).
- **Kiểm tra toàn vẹn:** `scripts/validate_tutors.py` khớp từng ô JSON ↔ CSV.

**Lời thoại**

“Toàn bộ phiên bản thư viện được khóa chặt trong requirements và package-lock để mọi máy chạy đồng nhất, đồng thời cài GitHub Actions CI cho backend. Bộ dữ liệu gồm 16 hồ sơ thiết kế theo 5 nguyên tắc từ Chương 3 nhằm chạm đủ các ca xung đột, đồng điểm và thiếu dữ liệu; hai hồ sơ công khai GS-T06 và GS-T07 được ẩn danh hoàn toàn và đánh dấu rõ những trường ước tính.”

**Hình/bảng minh họa:** Bảng 4.1 (Mục 4.1) & Bảng A.1 (Phụ lục A).

---

## Slide 25 — Module tính điểm độc lập & Quyết định triển khai QĐ-A–QĐ-E

**Trên slide**

- **Gói `backend/app/scoring/`:** `filters → weights → eligibility → criteria → ranker` (**0 import** web framework).
- **Năm chốt chặn kỹ thuật (Mục 4.3.1):**
  - `QĐ-A`: Ngân sách `B = 0` → `s_fee = 1` nếu `P = 0`, ngược lại `0` (tránh chia `0`).
  - `QĐ-B`: Tham số âm hoặc sai miền → hàm thuần tự ném `ValueError`.
  - `QĐ-C`: Học `online` hoặc bỏ trống quận → tự tắt `w_district_eff = 0`.
  - `QĐ-D`: Khớp đúng nhãn môn học, khu vực và khung giờ chuẩn hóa.
  - `QĐ-E`: Tính chuẩn `float64` IEEE 754 ở backend; `round(..., 3)` khi hiển thị UI.

**Lời thoại**

“Khi chuyển công thức sang mã Python ở Bảng 4.3, nhóm xử lý năm tình huống biên qua các quy ước từ QĐ-A đến QĐ-E. Đáng chú ý là QĐ-E: mọi phép tính giữ nguyên độ chính xác số thực IEEE 754 trong suốt quá trình sắp xếp, chỉ làm tròn ba chữ số thập phân lúc hiển thị lên giao diện để không làm mất khả năng phân biệt hai hồ sơ sát điểm nhau.”

**Hình/bảng minh họa:** Dải module `scoring` & Bảng 5 quyết định `QĐ-A–E`.

---

## Slide 26 — Dịch vụ API POST /api/recommend và Xử lý lỗi hai phía

**Trên slide**

- **3 điểm cuối:** `POST /api/recommend` · `GET /health` · `GET /docs` (Swagger UI).
- **Bảng 4.4:** HTTP 200 (`success`, `no_match` biến thể 1–2, `zero_weight`) và HTTP 422 (`extra="forbid"`, `top_k ∉ [1, 20]`).
- **Bảng 4.6 (Frontend):** Chặn form hợp lệ · Báo lỗi kết nối · `requestSeq` chặn phản hồi cũ ghi đè.

**Lời thoại**

“Ở tầng API, nhóm dùng cơ chế tiêm phụ thuộc cho TutorRepository để thay đổi dữ liệu dễ dàng khi chạy test. Phía frontend trong Bảng 4.6 có cơ chế đánh dấu thứ tự yêu cầu để khi người dùng bấm đổi trọng số liên tục ở CN03, phản hồi đến muộn hơn của lượt cũ không bao giờ ghi đè lên kết quả mới nhất.”

**Hình/bảng minh họa:** Bảng 4.4 & 3 bước bảo vệ Bảng 4.6.

---

## Slide 27 — Giao diện màn hình nhập nhu cầu CN01 (Hình 4.1)

**Trên slide**

- **Biểu mẫu & Ngân sách:** Tự động đọc số tiền bằng chữ tiếng Việt.
- **Lưới lịch rảnh 7 ngày × 3 buổi:** Chọn trực quan Sáng/Chiều/Tối.
- **Thanh nạp KB01–KB14 & Ô Mục tiêu học tập:** Gợi ý 3 bộ ưu tiên khởi đầu.

**Lời thoại**

“Hình 4.1 là ảnh chụp màn hình nhập nhu cầu CN01 trên thực tế. Người học điền tiêu chí bên trái và chọn mức ưu tiên bên phải. Ngoài ra, nhóm bố trí thanh nạp nhanh 14 kịch bản KB01–KB14 ở phía trên để tiện kiểm chứng, cùng ô chọn Mục tiêu học tập giúp gợi ý nhanh bộ mức ưu tiên khởi đầu.”

**Hình/bảng minh họa:** Hình 4.1 (`hinh-ui-01-cn01-nhap-nhu-cau.png`).

---

## Slide 28 — Giao diện kết quả & Thanh giải thích CN02 (Hình 4.2)

**Trên slide**

- **Phễu lọc KB01:** Kho `16` → Hợp lệ `5` → Top-3 (`GS-G01 0,938`, `GS-G10 0,745`, `GS-T06 0,625`).
- **Thanh xếp chồng $C_i$:** HTML/CSS thuần tách 4 đoạn (`0,25 / 0,25 / 0,19 / 0,25`), gắn nhãn *Thực tế (ước tính \*)* / *Dữ liệu đối chứng*.
- **Lưu ý đo:** `651,5 ms` ở góc màn hình gồm `650 ms` chờ hiệu ứng chuyển cảnh `App.jsx`.

**Lời thoại**

“Khi nhấn tìm gia sư ở KB01, màn hình kết quả Hình 4.2 hiện Top-3 khớp kỳ vọng: GS-G01 đứng đầu với 0,938 điểm. Mỗi thẻ gia sư đều có thanh xếp chồng chia nhỏ phần đóng góp của từng tiêu chí để người học biết vì sao gia sư được xếp ở hạng đó. Con số 651,5 ms ở góc trên lúc mới chuyển trang đã cộng sẵn 650 ms chờ hiệu ứng giao diện trong App.jsx.”

**Hình/bảng minh họa:** Hình 4.2 (`hinh-ui-02-cn02-ket-qua-kb01.png`).

---

## Slide 29 — Tinh chỉnh CN03, zero_weight & Chuyển tiếp Demo

**Trên slide**

- **CN03 (Hình 4.3):** Hạ Học phí & Khu vực = `0`, nâng KN & Đánh giá = `Cao` ⇒ `GS-G10` lên **Hạng 1 (`0,990`, `↑1`)**.
- **Biên $\sum w_i = 0$ (Hình 4.4):** Vẫn giữ `Hợp lệ: 5 ứng viên`, hiện cảnh báo `zero_weight` & nút khôi phục `w = 2`.
- **Tiếp theo:** Trình diễn live 4 phút theo [kich-ban-demo-bao-ve.md](kich-ban-demo-bao-ve.md).

**Lời thoại**

“Ở Hình 4.3, ngay khi người dùng bấm hạ trọng số Học phí và Khu vực về 0 rồi tăng Kinh nghiệm và Đánh giá lên Cao, hệ thống gọi lại API và đẩy GS-G10 lên hạng 1 với 0,990 điểm kèm huy hiệu tăng bậc. Còn ở Hình 4.4, khi cả năm tiêu chí đặt về Bỏ qua, giao diện báo rõ trạng thái zero_weight và cung cấp nút khôi phục mặc định thay vì chia cho 0. Phần trình diễn trực tiếp nhóm em xin thực hiện trong kịch bản demo kèm theo; tiếp theo bạn Trần Nguyễn Đức sẽ báo cáo Phần 5 về kiểm thử và đánh giá.”

**Hình/bảng minh họa:** Hình 4.3 (`hinh-ui-03-cn03-dieu-chinh-uu-tien.png`) & Hình 4.4 (`hinh-ui-04-zero-weight.png`).

---

## PHẦN 5: KIỂM THỬ VÀ ĐÁNH GIÁ THỰC NGHIỆM

## Slide 30 — [Giới thiệu Phần 5] Kiểm thử và đánh giá thực nghiệm

**Trên slide**

- **Lộ trình:** 1. Tổng quan → 2. Lý thuyết & CN → 3. Phân tích & TK → 4. Xây dựng HT → `[5. Kiểm thử & ĐG]` → 6. Kết luận.
- **Nội dung trọng tâm:**
  - Bộ 200 bài TDD, phủ mã 97% & độ trễ API.
  - Kiểm thử ca biên 5 hàm điểm & đơn điệu.
  - Đối chiếu 14/14 kịch bản, `KB01` & độ nhạy 4 yếu tố.
- **Câu hỏi dẫn dắt:** *Hệ thống có chạy khớp công thức thiết kế ở các ca biên và giữ được tính ổn định xếp hạng hay không?*

**Lời thoại**

“Tiếp theo, em xin trình bày Phần 5: Kiểm thử và đánh giá thực nghiệm, nơi nhóm em dùng số liệu tự động để kiểm chứng thiết kế thuật toán ở Phần 3.”

**Hình/bảng minh họa:** Thanh lộ trình 6 phần (làm sáng Phần 5).

---

## Slide 31 — Bộ kiểm thử 200 bài TDD và Hiệu năng xử lý

**Trên slide**

- **3 chỉ số TDD (Bảng 5.1):** **`200/200`** đạt (`1,18s`) · **`97%`** coverage (`340/351` câu lệnh; API/schemas `100%`) · **`3,54 ms`** TB (`140` calls).
- **Chịu tải `benchmark_latency.py`:** `140` lượt (TB `3,54 ms` · max `7,97 ms`) và `700` lượt (TB `3,72 ms` · max `26,64 ms` `<< 1.000 ms`).

**Lời thoại**

“Khi chạy pytest trong thư mục backend như Bảng 5.1, toàn bộ 200 bài kiểm thử tự động đều đạt trong 1,18 giây với độ bao phủ 97% số câu lệnh nghiệp vụ. Về hiệu năng nội tại qua TestClient, thời gian xử lý trung bình chỉ khoảng 3,54 ms — nghĩa là hoàn toàn đáp ứng ngưỡng dưới 1 giây cho tương tác CN03, dù phép đo này chưa tính thêm độ trễ đường truyền mạng.”

**Hình/bảng minh họa:** 3 Hero KPIs + Bảng 5.1 + đồ thị độ trễ (Mục 5.1.1–5.1.2).

---

## Slide 32 — Kiểm thử ca biên 5 hàm điểm và Tính đơn điệu

**Trên slide**

- **Bảng 5.2 (4 nhóm ca biên):** Học phí ($P \in \{B, 1{,}25B, 1{,}5B, >1{,}5B\}$), $B = 0$ (HTTP 200), Kinh nghiệm bão hòa ($E \ge 8$) & Đánh giá `null` (`0,500`), Lịch rảnh & Phá hòa (`tutor_id`).
- **Tính đơn điệu:** Tăng ngân sách $150.000 \to 200.000 \to 350.000\text{ VNĐ}$ ⇒ 100% ứng viên không giảm $S(g)$.

**Lời thoại**

“Bảng 5.2 kiểm chứng các điểm biên dễ phát sinh lỗi như chia cho 0 khi ngân sách bằng 0, giá trị chặn trên tại mốc 8 năm kinh nghiệm, hay tình huống một hồ sơ vượt trần học phí 100% nhưng vẫn không bị loại cứng. Phép kiểm tra tự động cũng xác nhận tính đơn điệu theo ngân sách trên toàn bộ tập ứng viên.”

**Hình/bảng minh họa:** Bảng 5.2 (Mục 5.1.3) + dải chứng minh đơn điệu.

---

## Slide 33 — Kết quả thực nghiệm 14/14 kịch bản & 3 phát hiện

**Trên slide**

- **Hero Match (Bảng 5.3–5.4):** **`14 / 14` (`100%`)** khớp tập hợp & thứ tự Top-3 kỳ vọng (gồm `KB05` `no_match`, `KB14` #1 `GS-G03`).
- **3 phát hiện minh bạch:**
  - `KB04`: Code tính đủ 4 tiêu chí (`0,886`/`0,786` theo biểu thức `5.1–5.2`), phát hiện bảng tính tay thiếu lịch.
  - `KB09`: Điểm `0,9275` làm tròn biên IEEE 754 ra `0,927` (`QĐ-E`).
  - `KB02`, `KB12`: Đồng điểm tuyệt đối `GS-G11, GS-G12` (`0,88125`, `0,63125`), tách bằng `tutor_id` tăng dần.

**Lời thoại**

“Khi chạy toàn bộ 14 kịch bản ở Bảng 5.3 và tổng hợp ở Bảng 5.4, cả tập hợp lẫn thứ tự Top-3 đều khớp 14 trên 14 kịch bản kỳ vọng viết sẵn trong scenarios.json. Hai điểm chênh nhẹ đã được kiểm chứng rõ: ở KB04 bằng công thức (5.1)–(5.2) do bảng tính tay ban đầu bỏ sót lịch rảnh, còn ở KB09 giá trị toán học 0,9275 được chuẩn nhị phân IEEE 754 float64 lưu thành 0,927499999999999991118... nên làm tròn 3 chữ số ra 0,927; đồng thời ở KB02 và KB12, cặp GS-G11 và GS-G12 đồng điểm tuyệt đối 0,88125 và 0,63125 được phá hòa tất định theo mã tutor_id, giữ nguyên thứ hạng 100%.”

**Hình/bảng minh họa:** Hero `14/14` + 3 thẻ phát hiện (Mục 5.2.1).

---

## Slide 34 — Phân tích khả năng giải thích tại KB01 (Bảng 5.9)

**Trên slide**

- **Biểu đồ & Bảng 5.9 (`KB01`):** `#1 GS-G01` (`0,9375`), `#2 GS-G10` (`0,7450`), `#3 GS-T06 (*)` (`0,6250` — hồ sơ thực tế ẩn danh Mục 4.2, `notes: chưa có đánh giá`).
- **3 giá trị giải thích:** $\sum C_i = S(g)$ · Chỉ rõ điểm mất (`GS-G10` lệch quận, `GS-T06` vượt phí) · Trích câu `reason` tối đa 3 tiêu chí mạnh nhất.

**Lời thoại**

“Bảng 5.9 cho thấy rõ khả năng giải thích kết quả của mô hình qua kịch bản KB01: cộng bốn mức đóng góp C_i lại bằng chính xác tổng điểm S(g). Ví dụ, gia sư GS-T06 đạt điểm tối đa về khu vực và 20 năm kinh nghiệm nhưng mất toàn bộ điểm học phí và nhận điểm đánh giá trung tính 0,5, nên lý do gợi ý nêu rõ ba thế mạnh đầu còn mảng notes nhắc chưa có đánh giá.”

**Hình/bảng minh họa:** Biểu đồ xếp chồng $C_i$ & Bảng 5.9 (Mục 5.2.5).

---

## Slide 35 — Khảo sát tính ổn định và độ nhạy theo 4 yếu tố

**Trên slide**

- **Ổn định nội tại (Bảng 5.5–5.7):** `δ ∈ [0,25; 1,00]`: `0/14` đổi · `E_max ∈ {5..12}`: `1/14` (`KB10`: `GS-T06` vào thay `GS-G01` ở `10`, vượt `GS-G09` ở `12`) · Ngân sách `±20%`: `0/11` đổi.
- **Nhạy đúng bộ ưu tiên (Bảng 5.8):** `1–2/14` kịch bản đổi (`KB01`, `KB10`) khi đổi 4 bộ mức ưu tiên.

**Lời thoại**

“Nhóm khảo sát độ nhạy theo bốn yếu tố từ Bảng 5.5 đến 5.8. Khi thay đổi $\delta$ từ 0,25 đến 1,0, Top-3 của 14 kịch bản giữ nguyên hoàn toàn; khi dao động ngân sách trong khoảng ±20%, Top-3 của 11 kịch bản có nhập ngân sách cũng không đổi; còn đổi mốc E_max chỉ tác động duy nhất ở KB10 khi tăng lên 10 và 12 năm (GS-G01 rời Top-3, GS-T06 vào rồi vượt GS-G09). Ngược lại, thay đổi bộ mức ưu tiên lập tức điều hướng lại Top-3 đúng mục tiêu người học. Tiếp theo, bạn Cao Khánh Ngọc sẽ tổng kết Phần 6.”

**Hình/bảng minh họa:** Lưới KPI 4 nhân tố Bảng 5.5–5.8 (Mục 5.2.3–5.2.4).

---

## PHẦN 6: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

## Slide 36 — [Giới thiệu Phần 6] Kết luận và hướng phát triển

**Trên slide**

- **Lộ trình:** 1. Tổng quan → 2. Lý thuyết & CN → 3. Phân tích & TK → 4. Xây dựng HT → 5. Kiểm thử & ĐG → `[6. Kết luận]`.
- **Nội dung trọng tâm:**
  - Mở rộng GVHD (`19` truy vấn) & Vercel/Render.
  - Tổng kết 4 mục tiêu & 6 Sprint (`Mục 6.1.1 & Bảng 6.1`).
  - 4 hạn chế kỹ thuật & 3 hướng phát triển.
- **Câu hỏi dẫn dắt:** *Đồ án đã đạt những gì so với cam kết ban đầu và đâu là giới hạn cần nâng cấp ở giai đoạn sau?*

**Lời thoại**

“Kính thưa Hội đồng, em xin đại diện nhóm trình bày Phần 6 — phần cuối cùng tổng kết kết quả đạt được, các điểm mở rộng đã cài đặt, hạn chế và hướng phát triển.”

**Hình/bảng minh họa:** Thanh lộ trình 6 phần (làm sáng Phần 6).

---

## Slide 37 — Kết quả mở rộng GVHD & Triển khai trực tuyến

**Trên slide**

- **Mục tiêu học tập — Phương án 1 (Mục 6.1.2):** 3 chế độ gợi ý trên `CN01` (chế độ 3 đẩy Học phí `w = 3`, 4 tiêu chí giữ `w = 2`); thực nghiệm **19 truy vấn** (`14 KB + 5 truy vấn bổ sung`): **`3/19`** đổi hạng `2–3` (`KB10, TQ1, TQ2`), **`0/19`** đổi hạng `1`.
- **Triển khai trực tuyến (Mục 6.1.3):** Vercel (`tutor-recommender.vercel.app`) & Render (`tutor-recommender-api.onrender.com`, lưu ý cold start `~30–40s`).

**Lời thoại**

“Tiếp thu góp ý của cô hướng dẫn về việc gắn nhu cầu theo mục tiêu học tập, nhóm em đã cài đặt Phương án 1 gợi ý nhanh ba bộ trọng số trên màn hình CN01. Thử nghiệm trên 19 truy vấn gồm 14 kịch bản chuẩn và 5 truy vấn bổ sung TQ1–TQ5 cho thấy 3 trên 19 trường hợp đổi thứ hạng ở vị trí 2–3, giúp người học chọn nhanh hơn mà không cần chỉnh tay từng thanh. Đồng thời nhóm đã triển khai bản chạy trực tuyến trên Vercel và Render.”

**Hình/bảng minh họa:** Thẻ KPI `19 · 3/19 · 0/19` & thẻ triển khai Vercel/Render.

---

## Slide 38 — Tổng kết kết quả đạt được (Mục 6.1 & Quỹ 300 giờ)

**Trên slide**

- **4 mục tiêu hoàn thành (Mục 6.1.1):**
  - Scoring thuần túy: 5 module độc lập, toàn bộ `backend/app/` phủ `97%`.
  - API REST chuẩn hóa: `200/200` bài TDD đạt (`1,18s`), TestClient TB `3,54 ms`.
  - React 19 SPA trực tuyến: Live Vercel & Render, đủ `CN01–03` kèm `requestSeq`.
  - Thực nghiệm & mở rộng: `14/14` KB khớp Top-3, độ nhạy 4 yếu tố & PA1 `19` truy vấn.
- **Quỹ thời gian Scrum 6 Sprint:** Đúng `300 giờ` nhóm (`3 SV × 100h`), đồng bộ báo cáo và mã nguồn.

**Lời thoại**

“Đối chiếu lại bốn mục tiêu đăng ký ở Chương 1, nhóm đã hoàn thành trọn vẹn từ lõi tính điểm thuần Python (cùng toàn bộ tầng ứng dụng backend/app bao phủ 97% câu lệnh), 200 bài test đạt 100%, ứng dụng React chạy live trên Vercel và Render cho tới thực nghiệm 14 kịch bản chuẩn và mở rộng 19 truy vấn, với tổng thời lượng Scrum 6 Sprint đúng 300 giờ nhóm.”

**Hình/bảng minh họa:** Lưới 4 thẻ thành tựu & thanh tổng kết Scrum 300 giờ (Mục 6.1).

---

## Slide 39 — Hạn chế đề tài & Hướng phát triển kế tiếp (Mục 6.2)

**Trên slide**

- **4 hạn chế (Mục 6.2.1):** Quy mô 16 hồ sơ mẫu (gồm 2 hồ sơ công khai ước tính `*`) · Tham số $\delta, E_{\max}$ đặt tay · Thiếu khảo sát người học thực · Khớp quận quy ước, chưa đo trễ mạng.
- **3 hướng phát triển (Mục 6.2.2–6.2.3):**
  1. CSDL quan hệ, tài khoản, đặt lịch & đánh giá thật.
  2. Khuyến nghị Hybrid [6] & LTR [7] từ phản hồi tương tác thực.
  3. Mở rộng Phương án 2 đưa *Cấp lớp*, trình độ & thế mạnh vào hàm điểm.

**Lời thoại**

“Bên cạnh kết quả đạt được, nhóm nhìn thẳng vào bốn hạn chế chính: quy mô 16 hồ sơ mẫu mới giúp kiểm chứng đúng thuật toán chứ chưa phản ánh thị trường lớn, bộ tham số đặt tay chưa qua khảo sát người học ngoài nhóm và chưa đo trễ mạng thực tế. Từ đó nhóm xác định ba hướng nâng cấp rõ ràng: chuyển sang cơ sở dữ liệu quan hệ có tài khoản và đặt lịch, thu thập tương tác để nâng cấp thành mô hình Hybrid và học trọng số bằng Learning-to-Rank, đồng thời đưa cấp lớp, trình độ và thế mạnh sư phạm vào hàm chấm điểm theo Phương án 2.”

**Hình/bảng minh họa:** Ma trận 2 cột Hạn chế (Mục 6.2.1) ↔ 3 Hướng phát triển (Mục 6.2.2–6.2.3).

---

## Slide 40 — Lời cảm ơn & Hỏi đáp

**Trên slide**

- **Lời cảm ơn:** Trân trọng cảm ơn **TS. Lê Anh Nhã Uyên** và **Quý thầy cô Hội đồng**.
- **Đề tài:** *HỆ THỐNG KHUYẾN NGHỊ GIA SƯ DỰA TRÊN PHƯƠNG PHÁP CONTENT-BASE FILTERING*.
- **Liên kết:** Vercel (`tutor-recommender.vercel.app`) · Render Swagger (`/docs`) · GitHub (`tnduckhmt2411011-design/tutor-recommender`).

**Lời thoại**

“Phần trình bày của nhóm em đến đây là hết. Nhóm chúng em xin chân thành cảm ơn cô Lê Anh Nhã Uyên và quý thầy cô trong Hội đồng đã lắng nghe. Chúng em rất mong nhận được các câu hỏi và góp ý để hoàn thiện đề tài tốt hơn.”

---

## Phụ lục: Kiểm tra trước khi trình bày

- [ ] Tên đề tài trên Slide 1 và Slide 40 giống nhau và khớp tuyệt đối với trang bìa báo cáo (`CONTENT-BASE FILTERING` ở tên đề tài đăng ký; `Content-Based Filtering` khi mô tả thuật toán).
- [ ] Cả **6 slide giới thiệu đầu phần** (`Slide 3, 7, 11, 23, 30, 36`) thoáng mắt, dùng thanh định vị dọc đồng nhất và hoàn toàn không chứa hộp người trình bày hay thời lượng.
- [ ] Toàn bộ số liệu trên Slide 31–35 và Slide 37 khớp 100% với Chương 5, Chương 6 và tệp `so-lieu-doi-chieu.csv`.
- [ ] Các sơ đồ `Hình 3.2`, `Hình 3.3`, `Hình 3.4 & 3.5` được tách thoáng trên `Slide 20–22`, tối đa 2 ảnh/slide.
- [ ] Đã tinh gọn nội dung trên toàn bộ 40 slide (vùng vàng thuyết trình `75–130` từ/slide, không dùng hộp lồng hộp thừa, cỡ chữ mọi thành phần `>= 15 px`).
- [ ] Số thập phân dùng dấu phẩy (`0,5`, `3,54 ms`); hàng nghìn dùng dấu chấm (`200.000 VNĐ/giờ`, `1.000 ms`); đã xuất bản PDF dự phòng cho file trình chiếu.
