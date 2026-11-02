# Kết quả kiểm thử chức năng, kiểm thử ca biên (Mục 5.1) và Bảng 5.1 hoàn chỉnh

- **Mục tương ứng trong đề cương:** Mục 5.1 (Kiểm thử chức năng và kiểm thử ca biên), Bảng 5.1 (Kết quả thực nghiệm 14 kịch bản đánh giá).
- **Thuộc User Story:** US-29 (Issue #31) — Kiểm thử chức năng và kiểm thử ca biên trên toàn hệ thống; điền đầy đủ cột "Top-3 hệ thống" của Bảng 5.1 để vượt qua **Cổng chất lượng 3 (Quality Gate 3)**.
- **Tệp kiểm thử tự động tương ứng:**
  - `backend/tests/unit/test_criteria.py` (47 unit test cho 5 hàm điểm thành phần Bảng 3.6)
  - `backend/tests/scenarios/test_scenarios.py` (17 bài kiểm thử hồi quy 14 kịch bản `KB01`–`KB14`)
  - `backend/tests/api/test_recommend_api.py` (35 bài kiểm thử tích hợp hợp đồng API)
  - `backend/tests/api/test_boundary_muc_5_1.py` (6 bài kiểm thử tích hợp chuyên sâu cho các ca biên Mục 5.1, tính đơn điệu và luồng tương tác CN03)

---

## 1. Kết quả kiểm thử chức năng và kiểm thử ca biên (Mục 5.1)

Toàn bộ các ca biên theo đặc tả tại Mục 3.5, Bảng 3.6 và Mục 5.1 của đề cương đã được thực thi tự động qua endpoint tích hợp `POST /api/recommend` (với `fastapi.testclient.TestClient`):

| Nhóm kiểm thử | Ca biên / Tình huống kiểm thử | Đầu vào thực nghiệm | Kết quả kỳ vọng (Bảng 3.6 & Mục 5.1) | Kết quả thực tế hệ thống | Trạng thái |
|:---|:---|:---|:---|:---|:---:|
| **1. Học phí ($s_{\text{fee}}$, $\delta = 0{,}5$)** | Học phí bằng đúng ngân sách ($P = B$) | $B = 200\,000$, $P = 200\,000$ | $s_{\text{fee}} = 1{,}000$; lý do `"học phí trong ngân sách"` | `s_fee = 1.0`, `reason` chứa `"học phí trong ngân sách"` | **Đạt** |
| | Học phí nằm giữa vùng dung sai ($P = 1{,}25 B$) | $B = 200\,000$, $P = 250\,000$ | $s_{\text{fee}} = 0{,}500$; lý do `"học phí vượt ngân sách 25%"` | `s_fee = 0.5`, `reason` chứa `"học phí vượt ngân sách 25%"` | **Đạt** |
| | Học phí chạm biên trên dung sai 50% ($P = 1{,}50 B$) | $B = 200\,000$, $P = 300\,000$ | $s_{\text{fee}} = 0{,}000$; lý do `"học phí vượt ngân sách 50%"` | `s_fee = 0.0`, `reason` chứa `"học phí vượt ngân sách 50%"` | **Đạt** |
| | Học phí vượt quá 50% ngân sách ($P > 1{,}50 B$) | $B = 200\,000$, $P = 400\,000$ (`GS-T06` tại `KB01`) | $s_{\text{fee}} = 0{,}000$; không bị loại cứng, lý do `"học phí vượt ngân sách 100%"` | `s_fee = 0.0`, xếp hạng 3 tại `KB01`, `notes = ["chưa có đánh giá"]` | **Đạt** |
| | Ngân sách bằng 0 ($B = 0$) | $B = 0$, $P > 0$ | $s_{\text{fee}} = 0{,}000$; không phát sinh lỗi chia cho 0 | `HTTP 200 OK`, mọi ứng viên có `s_fee = 0.0` | **Đạt** |
| **2. Kinh nghiệm ($s_{\text{experience}}$, mốc $8$ năm)** | Kinh nghiệm bằng 0 năm ($E = 0$) | $E = 0$ | $s_{\text{experience}} = 0{,}000$ | `s_experience = 0.0` | **Đạt** |
| | Kinh nghiệm chạm mốc bão hòa ($E = 8$) | $E = 8$ (`GS-G06` tại `KB11`) | $s_{\text{experience}} = 1{,}000$ | `s_experience = 1.0` | **Đạt** |
| | Kinh nghiệm vượt mốc bão hòa ($E > 8$) | $E = 12$ (`GS-G10`), $E = 20$ (`GS-T06`) | $s_{\text{experience}} = 1{,}000$ (không vượt quá $1{,}0$) | `s_experience = 1.0` | **Đạt** |
| **3. Điểm đánh giá ($s_{\text{rating}}$)** | Gia sư chưa có đánh giá (`avg_rating = null`) | `GS-T06`, `GS-T07` (`public_collected`) | $s_{\text{rating}} = 0{,}500$ (trung tính); ghi chú `"chưa có đánh giá"`; không bị tính là thiếu dữ liệu | `s_rating = 0.5`, `notes` có `"chưa có đánh giá"` | **Đạt** |
| | Điểm đánh giá tuyệt đối (`avg_rating = 5.0`) | `GS-G01` (`avg_rating = 5.0`) | $s_{\text{rating}} = 1{,}000$ | `s_rating = 1.0` | **Đạt** |
| **4. Lịch rảnh ($s_{\text{availability}}$)** | Khớp một phần khung giờ ($m/k$ với $1 \le m < k$) | Yêu cầu `["T2-tối", "T4-tối", "T6-tối"]` ($k=3$); `GS-G01` khớp 2 khung giờ | Qua lọc bắt buộc; $s_{\text{availability}} = 2/3 \approx 0{,}667$ | `s_availability = 0.6667` | **Đạt** |
| | Khớp toàn bộ khung giờ ($k/k$) | Yêu cầu `["T2-tối", "T4-tối", "T6-tối"]` ($k=3$); `GS-T06` khớp cả 3 | $s_{\text{availability}} = 3/3 = 1{,}000$ | `s_availability = 1.0` | **Đạt** |
| | Không giao khung giờ nào ($0/k$) | Khung giờ yêu cầu không giao với `availability` của gia sư | Bị loại ngay ở bước lọc điều kiện bắt buộc | Không xuất hiện trong `results` | **Đạt** |
| **5. Tính đơn điệu & Tương tác CN03** | Tính đơn điệu theo ngân sách tối đa $B$ | Tăng $B$: `150.000` $\rightarrow$ `200.000` $\rightarrow$ `350.000` VNĐ | Tổng điểm $S(g)$ của mọi ứng viên không giảm: $S_{150k}(g) \le S_{200k}(g) \le S_{350k}(g)$ | Thỏa mãn 100% trên toàn bộ ứng viên | **Đạt** |
| | Đổi mức ưu tiên trực tiếp trên trang kết quả (CN03) | Từ `KB01` mặc định $\rightarrow$ đặt `fee = none`, `rating = none`, `experience = high` | `GS-T06` (20 năm kinh nghiệm) tăng từ hạng 3 lên hạng 1 ($S = 1{,}000$); phản hồi `< 1s` | `GS-T06` lên hạng 1 (`S = 1.0`), thời gian phản hồi `~4–6 ms` | **Đạt** |
| | Đặt toàn bộ 5 mức ưu tiên về `none` ($\sum w_i = 0$) | `priorities = {fee: none, district: none, experience: none, rating: none, availability: none}` | Trả về `status = "zero_weight"` kèm danh sách `unranked_candidates` | `status = "zero_weight"`, trả đủ 5 ứng viên trong `unranked_candidates` | **Đạt** |

---

## 2. Bảng 5.1 — Kết quả thực nghiệm 14 kịch bản đánh giá (Điền đầy đủ cột "Top-3 hệ thống")

Bảng dưới đây ghi nhận đầy đủ kết quả thực nghiệm của hệ thống qua endpoint `POST /api/recommend` vào cột **"Top-3 hệ thống"** đối sánh trực tiếp với cột **"Top-3 kỳ vọng"** của Bảng 5.1 trong đề cương khóa luận:

| Mã KB | Nhu cầu người học & Mức ưu tiên (theo Bảng 5.1 / `scenarios.json`) | Top-3 kỳ vọng (Đề cương Bảng 5.1) | Top-3 hệ thống (Kết quả thực tế `POST /api/recommend`) | Độ khớp Top-3 | Thời gian phản hồi API | Nhận xét thực nghiệm |
|:---:|:---|:---|:---|:---:|:---:|:---|
| **KB01** | **Môn:** Toán \| **Hình thức:** Trực tiếp \| **Khu vực:** Bình Thạnh \| **Ngân sách:** 200.000đ \| **Ưu tiên:** Tất cả Trung bình ($w=2$) | `1. GS-G01 (0,938)`<br/>`2. GS-G10 (0,745)`<br/>`3. GS-T06 (0,625)` | `1. GS-G01 (0,938)`<br/>`2. GS-G10 (0,745)`<br/>`3. GS-T06 (0,625)` | **3/3** | `< 6 ms` | Khớp tuyệt đối cả thứ hạng và điểm số; `GS-T06` vượt ngân sách 100% ($s_{\text{fee}}=0$) nên xếp hạng 3. |
| **KB02** | **Môn:** Anh Văn \| **Hình thức:** Trực tiếp \| **Khu vực:** Quận 2 \| **Ngân sách:** 220.000đ \| **Ưu tiên:** Tất cả Trung bình ($w=2$) | `1–2. GS-G11 = GS-G12 (0,881, đồng hạng)`<br/>`3. GS-T07 (0,5625)` | `1. GS-G11 (0,881)`<br/>`2. GS-G12 (0,881)`<br/>`3. GS-T07 (0,5625)` | **3/3** | `< 6 ms` | Khớp hoàn toàn; `GS-G11` và `GS-G12` đồng điểm `0,88125`, phá hòa tất định theo mã hồ sơ. |
| **KB03** | **Môn:** Anh Văn \| **Hình thức:** Trực tiếp \| **Khu vực:** Thủ Đức \| **Ngân sách:** 220.000đ \| **Ưu tiên:** Tất cả Trung bình ($w=2$) | `1. GS-G12 (0,881)`<br/>`2. GS-G11 (0,631)`<br/>`3. GS-T07 (0,5625)` | `1. GS-G12 (0,881)`<br/>`2. GS-G11 (0,631)`<br/>`3. GS-T07 (0,5625)` | **3/3** | `< 6 ms` | Khớp tuyệt đối cả thứ hạng và điểm số; `GS-G12` khớp Thủ Đức nên tách lên hạng 1. |
| **KB04** | **Môn:** Lý \| **Hình thức:** Trực tuyến \| **Ngân sách:** 200.000đ \| **Lịch:** `T2-tối`, `T4-tối` \| **Ưu tiên:** Tất cả Trung bình ($w=2$) | `1. GS006 (0,848)`<br/>`2. GS020 (0,715)` | `1. GS006 (0,886)`<br/>`2. GS020 (0,786)` | **2/2** | `< 6 ms` | **Khớp 100% thứ hạng (`GS006 > GS020`)**; điểm hệ thống tính đủ 4 tiêu chí có mặt `availability` (xem `discrepancy_analysis.md`). |
| **KB05** | **Môn:** Tiếng Trung \| **Hình thức:** Không yêu cầu (`any`) \| **Ưu tiên:** Tất cả Trung bình ($w=2$) | `(không có)` | `(không có)`<br/>*(`status = "no_match"`, `results = []`)* | **Đạt (0/0)** | `< 5 ms` | Khớp tuyệt đối; bộ lọc bắt buộc trả về danh sách rỗng kèm thông báo thân thiện. |
| **KB06** | **Môn:** Văn \| **Hình thức:** Trực tiếp \| **Khu vực:** Quận 1 \| **Ngân sách:** 180.000đ \| **Ưu tiên:** Tất cả Trung bình ($w=2$) | `1. GS-G04 (0,934)` | `1. GS-G04 (0,934)` | **1/1** | `< 5 ms` | Khớp tuyệt đối thứ hạng và điểm số (`0,934375`). |
| **KB07** | **Môn:** Sinh \| **Hình thức:** Không yêu cầu (`any`) \| **Khu vực:** Thủ Đức \| **Ngân sách:** 200.000đ \| **Ưu tiên:** Tất cả Trung bình ($w=2$) | `1. GS-G05 (0,825)` | `1. GS-G05 (0,825)` | **1/1** | `< 5 ms` | Khớp tuyệt đối thứ hạng và điểm số (`0,825`). |
| **KB08** | **Môn:** Tin học \| **Hình thức:** Trực tuyến \| **Ngân sách:** 250.000đ \| **Lịch:** `T2-tối`, `T6-tối` \| **Ưu tiên:** Tất cả Trung bình ($w=2$) | `1. GS-G07 (0,876)` | `1. GS-G07 (0,876)` | **1/1** | `< 5 ms` | Khớp tuyệt đối thứ hạng và điểm số (`0,87625`). |
| **KB09** | **Môn:** Tiếng Nhật \| **Hình thức:** Không yêu cầu (`any`) \| **Khu vực:** Phú Nhuận \| **Ngân sách:** 280.000đ \| **Ưu tiên:** Tất cả Trung bình ($w=2$) | `1. GS-G08 (0,928)` | `1. GS-G08 (0,9275)`<br/>*(hiển thị 3 chữ số: `0,928` / IEEE-754: `0,927`)* | **1/1** | `< 5 ms` | Khớp thứ hạng 1/1; giá trị chính xác $3{,}71/4 = 0{,}9275$. |
| **KB10** | **Môn:** Toán \| **Hình thức:** Trực tiếp \| **Khu vực:** Quận 7 \| **Ưu tiên:** Kinh nghiệm = Cao ($w=3$), còn lại Trung bình ($w=2$) | `1. GS-G10 (0,994)`<br/>`2. GS-G01 (0,607)`<br/>`3. GS-G09 (0,593)` | `1. GS-G10 (0,994)`<br/>`2. GS-G01 (0,607)`<br/>`3. GS-G09 (0,593)` | **3/3** | `< 6 ms` | Khớp tuyệt đối cả thứ hạng và điểm số; `GS-T06` (`0,571`) đứng hạng 4 ngoài Top-3 đúng như phân tích đề cương. |
| **KB11** | **Môn:** Hóa \| **Hình thức:** Trực tiếp \| **Khu vực:** Quận 10 \| **Ngân sách:** 220.000đ \| **Ưu tiên:** Tất cả Trung bình ($w=2$) | `1. GS-G06 (0,985)`<br/>`2. GS-T06 (0,375)` | `1. GS-G06 (0,985)`<br/>`2. GS-T06 (0,375)` | **2/2** | `< 5 ms` | Khớp tuyệt đối cả thứ hạng và điểm số. |
| **KB12** | **Môn:** Anh Văn \| **Hình thức:** Trực tiếp \| **Khu vực:** Bình Chánh \| **Ngân sách:** 200.000đ \| **Ưu tiên:** Tất cả Trung bình ($w=2$) | `1. GS-T07 (0,8125)`<br/>`2–3. GS-G11 = GS-G12 (0,631, đồng hạng)` | `1. GS-T07 (0,8125)`<br/>`2. GS-G11 (0,631)`<br/>`3. GS-G12 (0,631)` | **3/3** | `< 6 ms` | Khớp tuyệt đối; hồ sơ thu thập thật `GS-T07` đứng hạng 1 nhờ khớp đúng khu vực Bình Chánh và học phí trong ngân sách. |
| **KB13** | **Môn:** Toán \| **Hình thức:** Không yêu cầu (`any`) \| **Ngân sách:** 150.000đ \| **Ưu tiên:** Tất cả Trung bình ($w=2$) | `1. GS-G10 (0,993)`<br/>`2. GS-G01 (0,783)`<br/>`3. GS-T06 (0,50)` | `1. GS-G10 (0,993)`<br/>`2. GS-G01 (0,783)`<br/>`3. GS-T06 (0,500)` | **3/3** | `< 6 ms` | Khớp tuyệt đối cả thứ hạng và điểm số. |
| **KB14** | **Môn:** Anh Văn \| **Hình thức:** Trực tuyến \| **Ưu tiên:** Tất cả Trung bình ($w=2$) | `1. GS-G03 (0,70)` | `1. GS-G03 (0,700)` | **1/1** | `< 5 ms` | Khớp tuyệt đối cả thứ hạng và điểm số. |

---

## 3. Kết luận nghiệm thu Cổng chất lượng 3 (Quality Gate 3)

1. **Độ chính xác xếp hạng:** Toàn bộ **14/14 kịch bản (100%)** trong Bảng 5.1 có danh sách Top-3 của hệ thống trùng khớp hoàn toàn với Top-3 kỳ vọng.
2. **Độ vững chắc tại các điểm biên (Mục 5.1):** Hệ thống xử lý chính xác mọi điểm biên của hàm chuẩn hóa học phí ($P=B$, $P=1{,}25B$, $P=1{,}5B$, $P>1{,}5B$, $B=0$), kinh nghiệm ($E=0, 8, 20$), đánh giá (`null` và `5.0`) và lịch rảnh ($1/k \dots k/k$) mà không phát sinh bất kỳ ngoại lệ nào.
3. **Hiệu năng và trải nghiệm tương tác (CN01 $\rightarrow$ CN02 $\rightarrow$ CN03):** Thời gian phản hồi trung bình của API đạt `~4–6 ms` (dưới ngưỡng `< 1000 ms`), cho phép người học điều chỉnh mức ưu tiên trực tiếp trên màn hình kết quả (CN03) và quan sát sự thay đổi thứ hạng tức thì.
