# CHƯƠNG 5. KIỂM THỬ VÀ ĐÁNH GIÁ

Chương này trình bày toàn bộ kết quả kiểm thử chức năng, kiểm thử ca biên và đánh giá chất lượng xếp hạng của hệ thống thuộc đề tài “Hệ thống khuyến nghị gia sư dựa trên phương pháp Content-Base Filtering”. Mọi số liệu thực nghiệm được thu thập từ bộ kiểm thử tự động (`pytest`) và pipeline tính điểm thực tế trên môi trường Python 3.12 (hệ điều hành Windows). Không gian dữ liệu thử nghiệm gồm 16 hồ sơ gia sư chuẩn hóa tại `data/processed/tutors.json` (14 hồ sơ mô phỏng `simulated` và 2 hồ sơ `public_collected` là `GS-T06`, `GS-T07` có học phí và lịch rảnh ước tính, điểm đánh giá để trống và nhận giá trị trung tính $0{,}5$ theo Phụ lục A) cùng 14 kịch bản đánh giá cố định KB01–KB14 tại `backend/tests/scenarios/scenarios.json`.

---

## 5.1. Kiểm thử chức năng và ca biên

### 5.1.1. Tổng quan bộ kiểm thử tự động

Hệ thống được xây dựng và kiểm thử theo phương pháp phát triển hướng kiểm thử (TDD). Toàn bộ quy trình lọc điều kiện, chuẩn hóa điểm số, tổng hợp trọng số và hợp đồng giao tiếp API được kiểm định bởi 200 bài kiểm thử tự động trong `backend/tests/` (Bảng 5.1):

- **Kiểm thử đơn vị (`backend/tests/unit/` và `backend/tests/test_environment.py`, gồm 132 bài):** gồm 129 bài trong `backend/tests/unit/` và 3 bài kiểm tra môi trường trong `backend/tests/test_environment.py`. Nhóm này bao phủ:
  - Năm hàm chuẩn hóa điểm thành phần tại Bảng 3.6 (`backend/tests/unit/test_criteria.py`: 47 bài).
  - Quy tắc lọc điều kiện bắt buộc (`backend/tests/unit/test_filters.py`: 17 bài).
  - Kiểm tra ngưỡng dữ liệu tối thiểu (`backend/tests/unit/test_eligibility.py`: 17 bài).
  - Quy đổi trọng số và mức ưu tiên (`backend/tests/unit/test_weights.py`: 22 bài).
  - Thuật toán xếp hạng và phá hòa (`backend/tests/unit/test_ranker.py`: 8 bài).
  - Tầng truy xuất dữ liệu (`backend/tests/unit/test_repository.py`: 13 bài).
  - Cấu hình hệ thống (`backend/tests/unit/test_config.py`: 5 bài).
- **Kiểm thử kịch bản và độ nhạy (`backend/tests/scenarios/`, gồm 27 bài):** gồm 17 bài kiểm thử hồi quy 14 kịch bản thực nghiệm KB01–KB14 (`backend/tests/scenarios/test_scenarios.py`) và 10 bài khảo sát độ nhạy tham số T1–T10 (`backend/tests/scenarios/test_sensitivity_muc_5_2.py`).
- **Kiểm thử tích hợp API và ca biên (`backend/tests/api/`, gồm 41 bài):** gồm 35 bài kiểm thử hợp đồng giao tiếp HTTP API qua `TestClient` (`backend/tests/api/test_recommend_api.py`) và 6 bài kiểm thử tích hợp cho các ca biên toán học, tính đơn điệu và luồng điều chỉnh ưu tiên CN03 (`backend/tests/api/test_boundary_muc_5_1.py`).

Toàn bộ bộ kiểm thử tự động đạt tỷ lệ 100% (**200/200 bài đạt, 0 lỗi, 0 bỏ qua**, thời gian chạy 1,18 giây ở phiên đo báo cáo; xác minh lại đạt 200/200 trong 1,32 giây). Độ bao phủ mã nguồn đo bằng lệnh `pytest --cov=app` đạt **97%** trên khối mã nghiệp vụ `backend/app/` (340/351 câu lệnh được phủ, 11 câu lệnh chưa phủ). Trong đó, các module xử lý chính (`backend/app/api/recommend.py`, `backend/app/main.py`, `backend/app/core/config.py`, `backend/app/data/repository.py`, `backend/app/scoring/criteria.py`, `backend/app/scoring/filters.py`, `backend/app/scoring/weights.py` và các mô hình dữ liệu Pydantic) đều đạt độ bao phủ 100%; 11 câu lệnh chưa phủ thuộc `eligibility.py` (1 câu lệnh) và các nhánh bảo vệ đầu vào không đạt qua API của `ranker.py` (10 câu lệnh).

**Bảng 5.1 - Phân bổ bộ kiểm thử tự động theo nhóm**

| Nhóm kiểm thử | Thư mục mã nguồn | Số lượng kiểm thử | Kết quả thực thi | Độ bao phủ mã nguồn (`backend/app/`) |
|:---|:---|:---:|:---:|:---:|
| Kiểm thử đơn vị (Unit Tests) | `backend/tests/unit/`, `backend/tests/test_environment.py` | 132 | 132/132 đạt | 84% (294/351 câu lệnh khi chạy riêng) |
| Kiểm thử kịch bản & độ nhạy | `backend/tests/scenarios/` | 27 | 27/27 đạt | 80% (280/351 câu lệnh khi chạy riêng) |
| Kiểm thử API & ca biên tích hợp | `backend/tests/api/` | 41 | 41/41 đạt | 93% chung (100% tầng API & Schemas) |
| **Tổng cộng toàn hệ thống** | **`backend/tests/`** | **200** | **200/200 đạt (100%)** | **97% tổng hợp (340/351 câu lệnh)** |

*Nguồn: Kết quả chạy lệnh `pytest -q` và `pytest --cov=app` từ thư mục `backend/`.*

### 5.1.2. Kiểm thử hợp đồng API và hiệu năng xử lý nội tại

Giao thức giao tiếp giữa giao diện (React) và máy chủ tính toán (FastAPI) được kiểm định theo hợp đồng API tại `docs/design/api-contract.md`. Endpoint `POST /api/recommend` được kiểm thử qua `fastapi.testclient.TestClient`:

1. **Cấu trúc phản hồi chuẩn hóa:** Dữ liệu JSON trả về gồm các trường `status`, `total_candidates`, `qualified_candidates`, `insufficient_data_candidates` và mảng kết quả `results[]`. Mỗi phần tử trong `results[]` chứa `rank`, `tutor_id`, `total_score`, `criteria_scores` (điểm thành phần 5 tiêu chí), `contributions` (mức đóng góp $C_i$), `reason` (chuỗi lý do) và `notes` (ghi chú dữ liệu).
2. **Quy tắc sắp xếp và phá hòa tất định:** Danh sách kết quả được sắp xếp theo thứ tự giảm dần của `total_score`. Khi hai hoặc nhiều ứng viên có cùng điểm số, hệ thống phá hòa tất định theo thứ tự từ điển tăng dần của mã `tutor_id` để giữ thứ hạng ổn định qua mọi lần gọi.
3. **Bao phủ bốn trạng thái phản hồi:** Bộ kiểm thử API kiểm chứng đủ bốn trạng thái: `success` (HTTP 200 kèm danh sách xếp hạng), `no_match` (HTTP 200, `results = []`), `zero_weight` (HTTP 200 khi $\sum w_i = 0$, kèm `unranked_candidates`) và `422 Unprocessable Entity` khi dữ liệu vi phạm ràng buộc Pydantic. Chi tiết xử lý các tình huống đặc biệt được trình bày tại Mục 5.1.4.
4. **Hiệu năng xử lý nội tại:** Đo đạc thực nghiệm qua kịch bản `scripts/thesis/benchmark_latency.py` trên 14 kịch bản KB01–KB14 qua 140 lượt gọi API liên tục (10 lượt/kịch bản) bằng `TestClient` ở phiên đo chuẩn ghi nhận thời gian phản hồi trung bình đạt **3,54 ms** (lớn nhất **7,97 ms** sau lượt khởi động đầu tiên). Phép đo mở rộng 700 lượt ghi nhận trung bình **3,72 ms** và lớn nhất **26,64 ms**. Tốc độ xử lý này đáp ứng yêu cầu phi chức năng về thời gian phản hồi dưới 1.000 ms khi người học điều chỉnh mức ưu tiên trực tiếp trên giao diện (CN03).

> [!NOTE]
> Chỉ số thời gian phản hồi trên được đo trong bộ nhớ cục bộ bằng `TestClient` (không có độ trễ truyền gói tin mạng). Thời gian này phản ánh tốc độ tính toán thuật toán và xử lý của FastAPI, không đại diện cho độ trễ truyền tải toàn trình (*end-to-end*) qua Internet giữa trình duyệt và máy chủ đám mây. Khi chạy lại kịch bản `scripts/thesis/benchmark_latency.py` trên các cấu hình phần cứng hoặc mức tải CPU khác nhau, thời gian xử lý trung bình thực tế dao động ở mức vài phần nghìn giây (thường từ 3 ms đến 15 ms), luôn thấp hơn hai bậc độ lớn so với ngưỡng yêu cầu phi chức năng 1.000 ms.

### 5.1.3. Kiểm thử ca biên của hàm điểm và tính đơn điệu

Nhằm kiểm chứng tính đúng đắn của 5 hàm chuẩn hóa điểm thành phần tại Bảng 3.6 và tính ổn định khi tương tác trực tiếp (CN03), các ca kiểm thử biên được xây dựng tại `backend/tests/api/test_boundary_muc_5_1.py` và `backend/tests/unit/test_criteria.py`. Kết quả được tổng hợp trong Bảng 5.2.

**Bảng 5.2 - Kết quả kiểm thử ca biên của các hàm điểm và tính đơn điệu**

| Nhóm kiểm thử | Ca biên / Tình huống kiểm thử | Đầu vào thực nghiệm | Kết quả kỳ vọng (Bảng 3.6 & Mục 5.1) | Kết quả thực tế hệ thống | Trạng thái |
|:---|:---|:---|:---|:---|:---:|
| **1. Học phí ($s_{\text{fee}}$, $\delta = 0{,}5$)** | Học phí bằng đúng ngân sách ($P = B$) | $B = 200.000\text{ VNĐ}$, $P = 200.000\text{ VNĐ}$ | $s_{\text{fee}} = 1{,}000$; lý do “học phí trong ngân sách” | $s_{\text{fee}} = 1{,}0$; lý do chứa “học phí trong ngân sách” | Đạt |
| | Học phí nằm giữa vùng dung sai ($P = 1{,}25 B$) | $B = 200.000\text{ VNĐ}$, $P = 250.000\text{ VNĐ}$ | $s_{\text{fee}} = 0{,}500$; lý do “học phí vượt ngân sách 25%” | $s_{\text{fee}} = 0{,}5$; lý do chứa “học phí vượt ngân sách 25%” | Đạt |
| | Học phí chạm biên trên dung sai 50% ($P = 1{,}50 B$) | $B = 200.000\text{ VNĐ}$, $P = 300.000\text{ VNĐ}$ | $s_{\text{fee}} = 0{,}000$; lý do “học phí vượt ngân sách 50%” | $s_{\text{fee}} = 0{,}0$; lý do chứa “học phí vượt ngân sách 50%” | Đạt |
| | Học phí vượt quá 50% ngân sách ($P > 1{,}50 B$) | $B = 200.000\text{ VNĐ}$, $P = 400.000\text{ VNĐ}$ (`GS-T06` tại KB01) | $s_{\text{fee}} = 0{,}000$; không bị loại cứng, lý do “học phí vượt ngân sách 100%” | $s_{\text{fee}} = 0{,}0$; xếp hạng 3 tại KB01, `notes = ["chưa có đánh giá"]` | Đạt |
| | Ngân sách bằng 0 ($B = 0$) | $B = 0\text{ VNĐ}$, $P > 0$ | $s_{\text{fee}} = 0{,}000$; không phát sinh lỗi chia cho 0 | HTTP 200 OK; mọi ứng viên nhận $s_{\text{fee}} = 0{,}0$ | Đạt |
| **2. Kinh nghiệm ($s_{\text{experience}}$, $E_{\max} = 8$)** | Kinh nghiệm bằng 0 năm ($E = 0$) | $E = 0$ | $s_{\text{experience}} = 0{,}000$ | $s_{\text{experience}} = 0{,}0$ | Đạt |
| | Kinh nghiệm chạm mốc bão hòa ($E = 8$) | $E = 8$ (`GS-G06` tại KB11) | $s_{\text{experience}} = 1{,}000$ | $s_{\text{experience}} = 1{,}0$ | Đạt |
| | Kinh nghiệm vượt mốc bão hòa ($E > 8$) | $E = 12$ (`GS-G10`), $E = 20$ (`GS-T06`) | $s_{\text{experience}} = 1{,}000$ (chặn trên bão hòa tại $1{,}0$) | $s_{\text{experience}} = 1{,}0$ | Đạt |
| **3. Điểm đánh giá ($s_{\text{rating}}$)** | Gia sư chưa có đánh giá (`avg_rating = null`) | `GS-T06`, `GS-T07` (`public_collected`) | $s_{\text{rating}} = 0{,}500$ (trung tính); ghi chú “chưa có đánh giá”; không bị loại | $s_{\text{rating}} = 0{,}5$; `notes` chứa “chưa có đánh giá” | Đạt |
| | Điểm đánh giá tối đa (`avg_rating = 5,0`) | `GS-G01` (`avg_rating = 5,0`) | $s_{\text{rating}} = 1{,}000$ | $s_{\text{rating}} = 1{,}0$ | Đạt |
| **4. Lịch rảnh ($s_{\text{availability}}$)** | Khớp một phần khung giờ ($m/k$ với $1 \le m < k$) | Yêu cầu `["T2-tối", "T4-tối", "T6-tối"]` ($k=3$); `GS-G01` khớp 2 khung | Vượt lọc bắt buộc; $s_{\text{availability}} = 2/3 \approx 0{,}667$ | $s_{\text{availability}} = 0{,}6667$ | Đạt |
| | Khớp toàn bộ khung giờ ($k/k$) | Yêu cầu `["T2-tối", "T4-tối", "T6-tối"]` ($k=3$); `GS-T06` khớp cả 3 | $s_{\text{availability}} = 3/3 = 1{,}000$ | $s_{\text{availability}} = 1{,}0$ | Đạt |
| | Không giao khung giờ nào ($0/k$) | Khung giờ yêu cầu không giao với lịch rảnh của gia sư | Bị loại ngay ở bước lọc điều kiện bắt buộc | Không xuất hiện trong danh sách `results` | Đạt |
| **5. Tính đơn điệu & Tương tác CN03** | Tính đơn điệu theo ngân sách tối đa $B$ | Tăng $B$: 150.000 → 200.000 → 350.000 VNĐ | Điểm tổng $S(g)$ của mọi ứng viên không giảm: $S_{150k} \le S_{200k} \le S_{350k}$ | Thỏa mãn 100% trên toàn bộ ứng viên | Đạt |
| | Đổi mức ưu tiên trực tiếp trên kết quả (CN03) | Từ KB01 mặc định → đặt `fee = none`, `rating = none`, `experience = high` | `GS-T06` (20 năm kinh nghiệm) lên hạng 1 ($S = 1{,}000$); phản hồi $< 1.000$ ms | `GS-T06` lên hạng 1 ($S = 1{,}0$); xử lý qua `TestClient` đạt $\approx 3{,}5$ ms | Đạt |
| | Đặt toàn bộ 5 mức ưu tiên về `none` ($\sum w_i = 0$) | `priorities = {fee: none, district: none, experience: none, rating: none, availability: none}` | Trả về `status = "zero_weight"` kèm `unranked_candidates` | `status = "zero_weight"`; trả đủ 5 ứng viên trong `unranked_candidates` | Đạt |

*Nguồn: Tóm tắt kết quả kiểm thử tự động từ `backend/tests/api/test_boundary_muc_5_1.py` và `backend/tests/unit/test_criteria.py`.*

### 5.1.4. Xử lý các trường hợp đặc biệt

Hệ thống xử lý thống nhất các trường hợp nghiệp vụ đặc thù theo nguyên tắc minh bạch dữ liệu:

1. **Không có gia sư thỏa điều kiện bắt buộc:** Khi bộ lọc bắt buộc loại toàn bộ hồ sơ (như KB05 với môn Tiếng Trung), API trả về `status = "no_match"`, `results = []` và `insufficient_data_candidates = []`. Giao diện hiển thị thông báo rõ ràng kèm gợi ý người học nới lỏng tiêu chí tìm kiếm.
2. **Học trực tuyến (`learning_mode = "online"`):** Khi chọn học từ xa, khoảng cách địa lý không còn ý nghĩa nên tiêu chí khu vực bị vô hiệu hóa. Giao diện khóa ô chọn quận/huyện, bộ tính trọng số loại `district` khỏi tổng trọng số và API trả về `criteria_scores["district"] = null`, `contributions["district"] = null` (như tại KB04, KB08, KB14).
3. **Tổng trọng số bằng 0 ($\sum w_i = 0$):** Khi người học đặt tất cả mức ưu tiên về “Không quan tâm” (`none`), mẫu số của công thức Weighted Scoring bằng $0$. Thay vì báo lỗi chia cho 0 hay gán trọng số ngầm định, hệ thống trả về trạng thái `zero_weight` cùng danh sách `unranked_candidates` gồm các gia sư qua lọc để người học tham khảo, và giao diện nhắc chọn ít nhất một mức ưu tiên để kích hoạt lại chức năng xếp hạng.
4. **Người học không nhập ngân sách, khu vực hoặc khung giờ:** Khi một trường tùy chọn bị bỏ trống, tiêu chí tương ứng được xem là không áp dụng:
   - Không nhập ngân sách tối đa (`max_budget_vnd = null`, như KB05, KB10, KB14): tiêu chí học phí vô hiệu hóa, không phạt vượt ngân sách (`criteria_scores["fee"] = null`, `contributions["fee"] = null`).
   - Không chọn quận/huyện khi học trực tiếp hoặc `any` (như KB05, KB13): tiêu chí khu vực vô hiệu hóa.
   - Không chọn khung giờ rảnh (`time_slots = []`, xuất hiện ở 12/14 kịch bản: KB01–KB03, KB05–KB07, KB09–KB14): tiêu chí lịch rảnh vô hiệu hóa (`criteria_scores["availability"] = null`, `contributions["availability"] = null`).
   Trong mọi trường hợp tiêu chí bị vô hiệu hóa, mẫu số tổng trọng số chỉ tính trên tập tiêu chí thực sự áp dụng $A$ ($\sum_{j \in A} w_j$), bảo đảm tính công bằng khi so sánh điểm giữa các ứng viên.

---

## 5.2. Đánh giá chất lượng xếp hạng

### 5.2.1. So khớp Top-3 hệ thống với kỳ vọng trên 14 kịch bản

Bảng 5.3 trình bày kết quả thực nghiệm chi tiết của 14 kịch bản đánh giá KB01–KB14, đối chiếu giữa Top-3 kỳ vọng trong tệp `backend/tests/scenarios/scenarios.json` với Top-3 do hệ thống tính toán qua pipeline `score_and_rank` trên 16 hồ sơ gia sư.

Quy ước chấm khớp tuân thủ `backend/tests/scenarios/README.md` mục 3:
- Khi Top-3 kỳ vọng có $m$ gia sư ($1 \le m \le 3$), số trùng được ghi nhận dạng $x/m$.
- Kịch bản KB05 kiểm tra trường hợp không có ứng viên thỏa điều kiện bắt buộc (`no_match`), trả về danh sách rỗng được tính là khớp quy ước `0/0`.
- Các gia sư đồng hạng trong kỳ vọng (KB02, KB12) được xem là hoán đổi được và phá hòa tất định theo mã `tutor_id` tăng dần (Mục 5.1.2).

**Bảng 5.3 - Kết quả thực nghiệm 14 kịch bản đánh giá**

| Mã KB | Mô tả nhu cầu | Top-3 kỳ vọng (`scenarios.json`) | Top-3 hệ thống (Chạy thực tế qua pipeline) | Số trùng ($x/m$) | Nhận xét thực nghiệm |
|:---:|:---|:---|:---|:---:|:---|
| **KB01** | Toán, trực tiếp, Bình Thạnh, ngân sách 200.000 VNĐ, mọi ưu tiên Trung bình | 1. GS-G01 (0,938)<br/>2. GS-G10 (0,745)<br/>3. GS-T06 (0,625) | 1. GS-G01 (0,938)<br/>2. GS-G10 (0,745)<br/>3. GS-T06 (0,625) | 3/3 | Khớp thứ hạng và điểm số; `GS-T06` vượt ngân sách 100% ($s_{\text{fee}} = 0$) nên xếp hạng 3 và nhận điểm đánh giá trung tính $0{,}5$. |
| **KB02** | Anh Văn, trực tiếp, Quận 2, ngân sách 220.000 VNĐ, mọi ưu tiên Trung bình | 1–2. GS-G11 = GS-G12 (0,881, đồng hạng)<br/>3. GS-T07 (0,5625) | 1. GS-G11 (0,881)<br/>2. GS-G12 (0,881)<br/>3. GS-T07 (0,5625) | 3/3 | Khớp tập hợp, thứ hạng và điểm số; `GS-G11` và `GS-G12` đồng điểm tuyệt đối ($0{,}88125$), phá hòa đưa `GS-G11` xếp trước. |
| **KB03** | Anh Văn, trực tiếp, Thủ Đức, ngân sách 220.000 VNĐ, mọi ưu tiên Trung bình | 1. GS-G12 (0,881)<br/>2. GS-G11 (0,631)<br/>3. GS-T07 (0,5625) | 1. GS-G12 (0,881)<br/>2. GS-G11 (0,631)<br/>3. GS-T07 (0,5625) | 3/3 | Khớp thứ hạng và điểm số; `GS-G12` khớp khu vực Thủ Đức nên xếp hạng 1. |
| **KB04** | Lý, trực tuyến, ngân sách 200.000 VNĐ, lịch T2-tối & T4-tối, mọi ưu tiên Trung bình | 1. GS006 (0,848)<br/>2. GS020 (0,715) | 1. GS006 (0,886)<br/>2. GS020 (0,786) | 2/2 | Khớp thứ hạng (`GS006 > GS020`); điểm hệ thống ($0{,}886$ và $0{,}786$) khác điểm tính tay ($0{,}848$ và $0{,}715$) do tính tay bỏ sót tiêu chí lịch rảnh. |
| **KB05** | Tiếng Trung, hình thức bất kỳ (`any`), mọi ưu tiên Trung bình | (không có ứng viên)<br/>`[]` | (không có ứng viên)<br/>`[]` (`status = "no_match"`) | 0/0 | Khớp kỳ vọng; hệ thống kích hoạt trạng thái `no_match` khi không có ứng viên nào dạy môn Tiếng Trung. |
| **KB06** | Văn, trực tiếp, Quận 1, ngân sách 180.000 VNĐ, mọi ưu tiên Trung bình | 1. GS-G04 (0,934) | 1. GS-G04 (0,934) | 1/1 | Khớp thứ hạng và điểm làm tròn (điểm chính xác: $2 \times (1 + 1 + 0{,}875 + 0{,}86) / 8 = 7{,}47 / 8 = 0{,}93375 \approx 0{,}934$). |
| **KB07** | Sinh, hình thức bất kỳ (`any`), Thủ Đức, ngân sách 200.000 VNĐ, mọi ưu tiên Trung bình | 1. GS-G05 (0,825) | 1. GS-G05 (0,825) | 1/1 | Khớp thứ hạng và điểm số ($0{,}825$). |
| **KB08** | Tin học, trực tuyến, ngân sách 250.000 VNĐ, lịch T2-tối & T6-tối, mọi ưu tiên Trung bình | 1. GS-G07 (0,876) | 1. GS-G07 (0,876) | 1/1 | Khớp thứ hạng và điểm làm tròn (điểm chính xác: $0{,}87625 \approx 0{,}876$). |
| **KB09** | Tiếng Nhật, hình thức bất kỳ (`any`), Phú Nhuận, ngân sách 280.000 VNĐ, mọi ưu tiên Trung bình | 1. GS-G08 (0,928) | 1. GS-G08 (0,9275) | 1/1 | Khớp thứ hạng 1/1; điểm chính xác là $0{,}9275$ (kỳ vọng đề cương làm tròn lên $0{,}928$; hàm làm tròn IEEE-754 của Python cho $0{,}927$). |
| **KB10** | Toán, trực tiếp, Quận 7, không nhập ngân sách, ưu tiên Kinh nghiệm Cao | 1. GS-G10 (0,994)<br/>2. GS-G01 (0,607)<br/>3. GS-G09 (0,593) | 1. GS-G10 (0,994)<br/>2. GS-G01 (0,607)<br/>3. GS-G09 (0,593) | 3/3 | Khớp thứ hạng và điểm số; `GS-T06` ($0{,}571$) đứng hạng 4 ngoài Top-3 đúng phân tích lý thuyết. |
| **KB11** | Hóa, trực tiếp, Quận 10, ngân sách 220.000 VNĐ, mọi ưu tiên Trung bình | 1. GS-G06 (0,985)<br/>2. GS-T06 (0,375) | 1. GS-G06 (0,985)<br/>2. GS-T06 (0,375) | 2/2 | Khớp thứ hạng và điểm số; `GS-T06` có $s_{\text{fee}} = 0$ do học phí vượt trần dung sai. |
| **KB12** | Anh Văn, trực tiếp, Bình Chánh, ngân sách 200.000 VNĐ, mọi ưu tiên Trung bình | 1. GS-T07 (0,8125)<br/>2–3. GS-G11 = GS-G12 (0,631, đồng hạng) | 1. GS-T07 (0,8125)<br/>2. GS-G11 (0,631)<br/>3. GS-G12 (0,631) | 3/3 | Khớp tập hợp, thứ hạng và điểm số; `GS-T07` đứng đầu nhờ khớp khu vực; `GS-G11` và `GS-G12` đồng điểm hạng 2–3 ($0{,}63125$), phá hòa theo mã gia sư. |
| **KB13** | Toán, hình thức bất kỳ (`any`), ngân sách 150.000 VNĐ, không nhập khu vực & lịch, mọi ưu tiên Trung bình | 1. GS-G10 (0,993)<br/>2. GS-G01 (0,783)<br/>3. GS-T06 (0,50) | 1. GS-G10 (0,993)<br/>2. GS-G01 (0,783)<br/>3. GS-T06 (0,500) | 3/3 | Khớp thứ hạng và điểm số trên 3 tiêu chí áp dụng (học phí, kinh nghiệm, đánh giá). |
| **KB14** | Anh Văn, trực tuyến, không nhập ngân sách, khu vực và lịch, mọi ưu tiên Trung bình | 1. GS-G03 (0,70) | 1. GS-G03 (0,700) | 1/1 | Khớp thứ hạng và điểm số sau khi chuẩn hóa nhãn môn học của `GS-G03` thành “Anh Văn”. |

*Nguồn: Kết quả chạy pipeline xếp hạng trên dữ liệu `data/processed/tutors.json` và `backend/tests/scenarios/scenarios.json`.*

Nhằm phục vụ đối chiếu trực quan mức độ trùng khớp của tập hợp, thứ tự Top-3 và sai số điểm theo từng đặc thù truy vấn, Bảng 5.4 tổng hợp kết quả thực nghiệm theo 5 nhóm kịch bản.

**Bảng 5.4 - Tổng hợp kết quả đối chiếu Top-3 theo nhóm đặc trưng kịch bản**

| Nhóm kịch bản thực nghiệm | Các kịch bản | Số kịch bản | Tỷ lệ khớp tập hợp & thứ tự Top-3 | Độ lệch điểm tuyệt đối lớn nhất $\max \lvert \Delta S \rvert$ | Ghi chú kỹ thuật |
|:---|:---|:---:|:---:|:---:|:---|
| Đủ $\ge 3$ ứng viên, điểm khớp hoàn toàn (đến 3 chữ số thập phân) | KB01, KB03, KB10, KB13 | 4 | 4/4 (100%) | $\le 0{,}0005$ | Khớp cả thứ tự lẫn giá trị điểm hiển thị |
| Đủ $\ge 3$ ứng viên, có đồng điểm tuyệt đối trong Top-3 | KB02, KB12 | 2 | 2/2 (100%) | $\le 0{,}00025$ | `GS-G11` và `GS-G12` đồng điểm ($0{,}88125$ ở KB02; $0{,}63125$ ở KB12), phá hòa tất định theo mã `tutor_id` |
| Môn hoặc điều kiện hiếm, chỉ có 1–2 ứng viên qua lọc | KB06, KB07, KB08, KB11, KB14 | 5 | 5/5 (100%) | $\le 0{,}00025$ | Khớp toàn bộ ứng viên qua lọc ($1/1$ hoặc $2/2$) |
| Có sai lệch giữa điểm chạy máy và điểm tính tay đề cương nhưng bảo toàn thứ tự | KB04, KB09 | 2 | 2/2 (100%) | $0{,}07125$ (KB04); $0{,}0005$ (KB09) | KB04: tính tay bỏ sót $s_{\text{availability}}$; KB09: khác quy tắc làm tròn tại biên $0{,}9275$ |
| Không có ứng viên thỏa điều kiện bắt buộc (`no_match`) | KB05 | 1 | 1/1 (100%) | Không áp dụng | Trả về `status = "no_match"`, `results = []` (khớp quy ước `0/0`) |
| **Tổng hợp toàn bộ tập kịch bản** | **KB01–KB14** | **14** | **14/14 (100%)** | **$0{,}07125$** | **Bảo toàn 100% tập hợp và thứ tự Top-3 kỳ vọng** |

*Nguồn: Tổng hợp từ `docs/thesis/report/muc-5.2-ket-qua-tho.json` (khối `baseline`) và `backend/tests/scenarios/scenarios.json`.*

**Tổng kết và phân tích ba trường hợp kỹ thuật đặc thù:**

Tổng thể thực nghiệm đạt tỷ lệ trùng khớp Top-3 kỳ vọng **14/14 kịch bản (100%)**, không ghi nhận đảo lộn thứ tự hoặc xuất hiện ứng viên sai lệch. Qua đối chiếu giữa kết quả chạy máy và số liệu kỳ vọng ban đầu trong đề cương, ba trường hợp kỹ thuật được làm rõ như sau:

1. **Kịch bản KB04 (Lệch giá trị điểm do công thức tính tay):**
   - Truy vấn KB04 là học trực tuyến (`online`), có ngân sách 200.000 VNĐ và yêu cầu khung giờ `["T2-tối", "T4-tối"]`. Theo Mục 6.1 của `docs/design/scoring-spec.md`, khi học trực tuyến chỉ tiêu chí khu vực bị loại bỏ, còn tiêu chí lịch rảnh vẫn áp dụng đầy đủ. Vì vậy có 4 tiêu chí áp dụng với tổng trọng số $\sum w_i = 2 + 2 + 2 + 2 = 8$, và cả hai ứng viên `GS006`, `GS020` đều thỏa toàn bộ khung giờ ($s_{\text{availability}} = 1{,}0$).
   - Điểm thực tế hệ thống tính theo công thức (5.1) và (5.2):
     $$S(\text{GS006}) = \frac{2 \times 1{,}0 + 2 \times 0{,}625 + 2 \times 0{,}92 + 2 \times 1{,}0}{8} = \frac{7{,}09}{8} = 0{,}88625 \approx 0{,}886 \qquad (5.1)$$
     $$S(\text{GS020}) = \frac{2 \times 0{,}6 + 2 \times 0{,}625 + 2 \times 0{,}92 + 2 \times 1{,}0}{8} = \frac{6{,}29}{8} = 0{,}78625 \approx 0{,}786 \qquad (5.2)$$
   - Điểm tính tay ban đầu ($0{,}848$ và $0{,}715$) phát sinh do phép tính thủ công chỉ cộng 3 tiêu chí (học phí, kinh nghiệm, đánh giá với tổng trọng số bằng 6), bỏ sót tiêu chí lịch rảnh. Vì $s_{\text{availability}} = 1{,}0$ ở cả hai ứng viên, việc cộng thêm tiêu chí lịch rảnh nâng đều điểm của cả hai mà vẫn giữ nguyên thứ tự xếp hạng (`GS006 > GS020`).
2. **Kịch bản KB09 (Chênh lệch làm tròn số thực):**
   - Ứng viên `GS-G08` có điểm thành phần: $s_{\text{fee}} = 1{,}0$; $s_{\text{district}} = 1{,}0$; $s_{\text{experience}} = 6/8 = 0{,}75$; $s_{\text{rating}} = 4{,}8/5 = 0{,}96$. Điểm tổng hợp chính xác là $(1{,}0 + 1{,}0 + 0{,}75 + 0{,}96)/4 = 3{,}71/4 = 0{,}9275$.
   - Theo quy tắc làm tròn nửa lên (*round half up*), $0{,}9275$ làm tròn thành $0{,}928$. Trong chuẩn số thực dấu phẩy động IEEE-754 của Python (*round half to even*), $0{,}9275$ có biểu diễn xấp xỉ `0.927499999999999991118...` nên làm tròn thành $0{,}927$. Hệ thống giữ giá trị thực $0{,}9275$ không làm tròn trung gian; thứ tự xếp hạng 1/1 không bị ảnh hưởng.
3. **Kịch bản KB02 và KB12 (Phá hòa tất định):**
   - Tại KB02, hai ứng viên `GS-G11` và `GS-G12` có cùng mọi chỉ số dẫn đến điểm tổng hợp bằng nhau tuyệt đối ($7{,}05/8 = 0{,}88125$). Bộ xếp hạng `score_and_rank` sắp xếp theo khóa `(-total_score, tutor_id)`, đưa `GS-G11` lên hạng 1 và `GS-G12` xuống hạng 2 theo quy tắc tất định.
   - Tại KB12, hai ứng viên này tiếp tục đồng điểm tại hạng 2 và hạng 3 ($5{,}05/8 = 0{,}63125$), và cơ chế phá hòa tiếp tục giữ trật tự `GS-G11` trước `GS-G12`.

### 5.2.2. Thứ hạng bất hợp lý và quyết định điều chỉnh

Trong đối chiếu 14 kịch bản nền tảng (*baseline*), không ghi nhận trường hợp thứ hạng nào bất hợp lý. Các kịch bản có 1 ứng viên trả về đúng ứng viên đó; các khác biệt số học tại KB04 và KB09 chỉ ảnh hưởng giá trị hiển thị mà không làm đổi thứ hạng.

Vì vậy, nhóm thống nhất **không điều chỉnh hàm điểm, không thay đổi tham số $\delta$, $E_{\max}$ hay trọng số, và không sửa dữ liệu kỳ vọng `expected_top3`, `expected_raw` trong `scenarios.json`**. Mọi chênh lệch số học được giải thích bằng công thức và quy tắc biểu diễn số thực như trên.

### 5.2.3. Khảo sát tính ổn định và độ nhạy tham số

Tính ổn định của thuật toán được khảo sát bằng cách thay đổi lần lượt ba yếu tố nền tảng: biên dung sai học phí $\delta$, mốc bão hòa kinh nghiệm $E_{\max}$, và mức ngân sách của người học. Cấu hình *baseline* sử dụng $\delta = 0{,}50$; $E_{\max} = 8$ năm; trọng số theo Bảng 3.5 và ngân sách gốc. Kết quả tổng hợp trong Bảng 5.5 ($\delta$), Bảng 5.6 ($E_{\max}$) và Bảng 5.7 (biến động ngân sách).

**Bảng 5.5 - Độ nhạy của Top-3 theo tham số dung sai học phí $\delta$**

| $\delta$ | Số KB đổi Top-3 | KB đổi | Số KB trùng Top-3 baseline ($x/m$) |
|:---:|:---:|:---:|:---:|
| 0,25 | 0 | — | 14/14 |
| 0,30 | 0 | — | 14/14 |
| 0,50 (baseline) | 0 | — | 14/14 |
| 0,70 | 0 | — | 14/14 |
| 0,75 | 0 | — | 14/14 |
| 1,00 | 0 | — | 14/14 |

*Nguồn: `docs/thesis/report/muc-5.2-ket-qua-tho.json`, khối `delta`.*

Kết quả ghi nhận **0/14 kịch bản thay đổi Top-3** trên cả 6 mức $\delta$ khảo sát. Khi $P \le B$, $s_{\text{fee}} = 1$; khi $P > B$, mẫu số $\delta B$ tăng làm giảm mức phạt nên $s_{\text{fee}}$ không giảm khi $\delta$ tăng. Việc giữ nguyên thứ tự trên tập 16 hồ sơ là quan sát thực nghiệm trên dữ liệu cụ thể, không đại diện cho tính bất biến trên mọi tập dữ liệu.

**Bảng 5.6 - Độ nhạy của Top-3 theo mốc kinh nghiệm bão hòa $E_{\max}$**

| $E_{\max}$ | Số KB đổi Top-3 | KB đổi | Top-3 của KB10 | Số KB trùng Top-3 baseline ($x/m$) |
|:---:|:---:|:---:|:---|:---:|
| 5 | 0 | — | `GS-G10 > GS-G01 > GS-G09` | 14/14 |
| 6 | 0 | — | `GS-G10 > GS-G01 > GS-G09` | 14/14 |
| 8 (baseline) | 0 | — | `GS-G10 > GS-G01 > GS-G09` | 14/14 |
| 10 | 1 | KB10 | `GS-G10 > GS-G09 > GS-T06` | 13/14 |
| 12 | 1 | KB10 | `GS-G10 > GS-T06 > GS-G09` | 13/14 |

*Nguồn: `docs/thesis/report/muc-5.2-ket-qua-tho.json`, khối `e_max`.*

Trong khảo sát $E_{\max}$, KB10 là kịch bản duy nhất thay đổi Top-3 tại hai mốc $E_{\max} = 10$ và $E_{\max} = 12$. Nguyên nhân toán học như sau:
- KB10 áp dụng 3 tiêu chí: Khu vực ($w = 2$), Kinh nghiệm ($w = 3$, mức Cao) và Đánh giá ($w = 2$), tổng trọng số bằng 7 (không có ngân sách và lịch rảnh).
- **Tại $E_{\max} = 10$:** Điểm của `GS-G09` là $(2 \times 1 + 3 \times 2/10 + 2 \times 0{,}7)/7 = 4/7$; điểm của `GS-T06` là $(2 \times 0 + 3 \times 1 + 2 \times 0{,}5)/7 = 4/7$. Kiểm tra giá trị số thực đầy đủ qua hàm `repr(total_score)` xác nhận cả hai ứng viên đều đạt chính xác `0.5714285714285714` (độ lệch bằng `0.0`). Hai ứng viên hòa điểm tuyệt đối, nên cơ chế phá hòa theo `tutor_id` (`"GS-G09" < "GS-T06"`) xếp `GS-G09` ở hạng 2 và `GS-T06` ở hạng 3.
- **Tại $E_{\max} = 12$:** Điểm của `GS-G09` giảm xuống $(2 \times 1 + 3 \times 2/12 + 2 \times 0{,}7)/7 = 3{,}9/7 \approx 0{,}55714$, trong khi `GS-T06` (20 năm kinh nghiệm vẫn chạm trần bão hòa) giữ nguyên $4/7 \approx 0{,}57143$. Lúc này `GS-T06` vượt điểm `GS-G09`, đưa Top-3 thành `GS-G10 > GS-T06 > GS-G09`.

**Bảng 5.7 - Độ nhạy của Top-3 theo mức biến động ngân sách**

| Mức ngân sách | Số KB áp dụng | Số KB đổi Top-3 | KB đổi | Số KB áp dụng trùng Top-3 baseline ($x/m$) |
|:---:|:---:|:---:|:---:|:---:|
| −20% | 11 | 0 | — | 11/11 |
| −10% | 11 | 0 | — | 11/11 |
| −5% | 11 | 0 | — | 11/11 |
| 0% (baseline) | 11 | 0 | — | 11/11 |
| +5% | 11 | 0 | — | 11/11 |
| +10% | 11 | 0 | — | 11/11 |
| +20% | 11 | 0 | — | 11/11 |

*Nguồn: `docs/thesis/report/muc-5.2-ket-qua-tho.json`, khối `budget` (KB05, KB10, KB14 không có ngân sách nên không áp dụng).*

Trên 11 kịch bản có thiết lập ngân sách, không có kịch bản nào thay đổi Top-3 qua chuỗi 7 mức ngân sách từ −20% đến +20%.

**Tính chất đơn điệu toán học:**
Các bài kiểm thử tự động T4, T6 và T7–T9 xác nhận tính đơn điệu (không giảm theo $B$, $\delta$ và không tăng theo $E_{\max}$) của mô hình điểm:
- **T4:** Với mỗi ứng viên, điểm tổng hợp $S$ không giảm khi $\delta$ tăng (trên các kịch bản có áp dụng tiêu chí học phí).
- **T6:** Với mỗi ứng viên, điểm tổng hợp $S$ không tăng khi $E_{\max}$ tăng (trên các kịch bản có áp dụng tiêu chí kinh nghiệm).
- **T7–T9:** Khi ngân sách tăng, điểm tổng hợp $S$ không giảm; tập hợp ứng viên qua lọc và thứ tự xếp hạng được bảo toàn trên tập thử nghiệm.

Tính đơn điệu của các hàm thành phần ($s_{\text{fee}}$ không giảm khi $B$ hoặc $\delta$ tăng; $s_{\text{experience}}$ không tăng khi $E_{\max}$ tăng) là hệ quả trực tiếp từ công thức toán học, còn việc Top-3 giữ nguyên là kết quả quan sát trên tập 16 hồ sơ mẫu.

### 5.2.4. Ảnh hưởng của các bộ mức ưu tiên

Khảo sát được thực hiện trên 4 bộ mức ưu tiên của bài kiểm thử T10: Mặc định (`default`), Ưu tiên Khu vực (`prioritize_district`), Ưu tiên Học phí (`prioritize_fee`) và Ưu tiên Kinh nghiệm & Đánh giá (`prioritize_experience_rating`). Bảng 5.8 tổng hợp số kịch bản đổi Top-3 và thay đổi thứ hạng ở từng bộ.

**Bảng 5.8 - Ảnh hưởng của bốn bộ mức ưu tiên đến Top-3**

| Bộ mức ưu tiên | Số KB đổi Top-3 | KB đổi Top-3 | Thay đổi Top-3 cụ thể |
|:---|:---:|:---:|:---|
| Mặc định (tất cả Trung bình) | 1 | KB10 | `GS-G10 > GS-G09 > GS-G01` thay cho `GS-G10 > GS-G01 > GS-G09`: đảo hạng 2–3, cùng tập hợp 3/3 |
| Ưu tiên Khu vực (`district` Cao, còn lại Thấp) | 2 | KB01, KB10 | KB01: `GS-G01 > GS-T06 > GS-G02` thay cho `GS-G01 > GS-G10 > GS-T06`; `GS-G10` rời Top-3 do không dạy Bình Thạnh, `GS-T06` lên hạng 2, `GS-G02` hạng 3 (trùng 2/3). KB10: `GS-G10 > GS-G09 > GS-G01` (đảo hạng 2–3, cùng tập 3/3) |
| Ưu tiên Học phí (`fee` Cao, còn lại Thấp) | 1 | KB10 | `GS-G10 > GS-G09 > GS-G01` thay cho `GS-G10 > GS-G01 > GS-G09` (đảo hạng 2–3, cùng tập 3/3); KB01 giữ nguyên |
| Ưu tiên KN & Đánh giá (`experience` & `rating` Cao, còn lại Thấp) | 1 | KB10 | `GS-G10 > GS-G01 > GS-T06` thay cho `GS-G10 > GS-G01 > GS-G09`: `GS-T06` vào Top-3 thay cho `GS-G09` (trùng 2/3) |

*Nguồn: `docs/thesis/report/muc-5.2-ket-qua-tho.json`, khối `priority_sets`.*

**Nhận xét:**
- Tại KB01 với bộ Ưu tiên Khu vực, gia sư `GS-G10` không dạy tại Bình Thạnh ($s_{\text{district}} = 0$) nên rời khỏi Top-3, trong khi `GS-T06` và `GS-G02` khớp Bình Thạnh nên lên hạng. Kết quả này minh họa việc thay đổi mức ưu tiên của người học làm dịch chuyển thứ hạng đúng theo thiết kế trọng số.
- Tại KB10, do không có ngân sách nên tiêu chí học phí không áp dụng. Ở bộ Mặc định và bộ Ưu tiên Học phí, trọng số kinh nghiệm giảm từ mức Cao ($w = 3$) xuống ngang hàng với khu vực, giúp `GS-G09` (khớp Quận 7) vượt qua `GS-G01`. Khi chuyển sang bộ Ưu tiên KN & Đánh giá, `GS-T06` (20 năm kinh nghiệm) vào Top-3 thay cho `GS-G09` (2 năm kinh nghiệm).
- Không bộ mức ưu tiên nào làm thay đổi vị trí hạng 1 tại KB01 (luôn là `GS-G01`) và KB10 (luôn là `GS-G10`).

### 5.2.5. Khả năng giải thích của kết quả gợi ý

Phương pháp Weighted Scoring cho phép phân rã điểm tổng hợp thành mức đóng góp từng tiêu chí cùng chuỗi lý do kèm theo. Bảng 5.9 trình bày phản hồi thực tế của `POST /api/recommend` cho kịch bản KB01.

**Bảng 5.9 - Thành phần điểm và mức đóng góp của Top-3 gia sư tại KB01**

| Hạng | Gia sư | Điểm tổng $S$ | Điểm thành phần `criteria_scores`<br/>(`fee`; `district`; `experience`; `rating`; `availability`) | Mức đóng góp `contributions`<br/>(`fee`; `district`; `experience`; `rating`; `availability`) |
|:---:|:---|:---:|:---|:---|
| 1 | GS-G01 | 0,9375 | 1,0000; 1,0000; 0,7500; 1,0000; null | 0,2500; 0,2500; 0,1875; 0,2500; null |
| 2 | GS-G10 | 0,7450 | 1,0000; 0,0000; 1,0000; 0,9800; null | 0,2500; 0,0000; 0,2500; 0,2450; null |
| 3 | GS-T06 | 0,6250 | 0,0000; 1,0000; 1,0000; 0,5000; null | 0,0000; 0,2500; 0,2500; 0,1250; null |

*Nguồn: Phản hồi thực tế của `POST /api/recommend` cho kịch bản KB01 (HTTP 200), đối chiếu với `docs/thesis/report/muc-5.2-ket-qua-tho.json`.*

Chuỗi lý do (`reason`) và ghi chú dữ liệu (`notes`) kèm theo:
- **GS-G01:** Lý do: “Học phí trong ngân sách, khu vực khớp, đánh giá 5,0/5”; Ghi chú: `[]`.
- **GS-G10:** Lý do: “Học phí trong ngân sách, kinh nghiệm 12 năm, đánh giá 4,9/5”; Ghi chú: `[]`.
- **GS-T06:** Lý do: “Khu vực khớp, kinh nghiệm 20 năm, đánh giá trung tính (0,5)”; Ghi chú: `["chưa có đánh giá"]`.

Cấu trúc trên thể hiện ba đặc điểm giải thích:
1. Điểm tổng hợp là tổng đại số chính xác của các mức đóng góp: $S = \sum C_i$.
2. Người học nhận biết ngay tiêu chí tạo ưu thế và tiêu chí bị trừ điểm (ví dụ `GS-G10` nhận $C_{\text{district}} = 0{,}0$ do không cùng quận, hay `GS-T06` nhận $C_{\text{fee}} = 0{,}0$ do học phí vượt trần dung sai).
3. Trường `notes` cảnh báo rõ hồ sơ chưa có lịch sử đánh giá thực tế (`GS-T06`) để người học cân nhắc đầy đủ thông tin.

---

## 5.3. Hạn chế của hệ thống

Nhóm ghi nhận sáu hạn chế hiện tại của hệ thống và bộ dữ liệu thử nghiệm:

1. **Quy mô tập dữ liệu còn nhỏ và mang tính giả lập:** Hệ thống hiện chỉ kiểm nghiệm trên 16 hồ sơ trong `data/processed/tutors.json`, gồm 14 hồ sơ mô phỏng (`simulated`) và 2 hồ sơ `public_collected` (`GS-T06`, `GS-T07`). Hai hồ sơ thu thập công khai có học phí và lịch rảnh là ước tính từ khảo sát thị trường chung; điểm đánh giá trung bình để trống và nhận giá trị trung tính $0{,}5$. Nhóm giữ nguyên nhãn `data_source = "public_collected"` vì môn dạy, khu vực và số năm kinh nghiệm là số liệu thực tế; việc đổi sang nhãn `estimated` sẽ làm mất thông tin về phần dữ liệu thu thập thật và đòi hỏi sửa đồng loạt tệp dữ liệu cùng script kiểm tra `validate_tutors.py`. Do đó, nhóm đánh dấu ký hiệu `(*)` tại Phụ lục A và ghi chú công khai các trường ước tính này.
2. **Bộ kịch bản đánh giá do nhóm tự xây dựng:** Toàn bộ 14 kịch bản và danh sách Top-3 kỳ vọng trong `backend/tests/scenarios/scenarios.json` do nhóm tự xây dựng theo các ca kiểm thử dự kiến, chưa phải dữ liệu đối chứng thu thập từ người học thật. Kết quả trùng khớp 14/14 kịch bản chứng minh thuật toán cài đặt chính xác và tính đúng theo công thức đã chốt trong thiết kế, chưa phải bằng chứng thực nghiệm độc lập về độ hài lòng ngoài thực tế.
3. **Các tham số thuật toán được ấn định thủ công:** Biên dung sai học phí $\delta = 0{,}5$, mốc kinh nghiệm bão hòa $E_{\max} = 8$, điểm trung tính $0{,}5$ và thang trọng số $w \in \{0, 1, 2, 3\}$ được thiết lập thủ công thay vì học từ dữ liệu hành vi người dùng quy mô lớn. Như đã lưu ý tại Mục 5.2.3, kết quả khảo sát độ nhạy gắn với tập tham số và dữ liệu 16 hồ sơ này, không khái quát hóa cho mọi bộ dữ liệu khác.
4. **Chưa có đánh giá thực nghiệm từ người dùng thật:** Hệ thống chưa được thử nghiệm trên nhóm học viên, phụ huynh thực tế để đo lường mức độ hài lòng hay tỷ lệ chấp nhận gợi ý sau khuyến nghị.
5. **Mô hình không gian địa lý và tìm kiếm môn học còn đơn giản:** Tiêu chí vị trí địa lý mới dừng ở so khớp nhị phân theo tên quận/huyện quy ước, chưa tính khoảng cách đường đi hay thời gian di chuyển. Mỗi truy vấn hiện chỉ hỗ trợ tìm kiếm một môn học tại một thời điểm.
6. **Chưa đo đạc độ trễ mạng thực tế:** Thời gian phản hồi ở Mục 5.1.2 ($\approx 3{,}5$ ms) là thời gian xử lý nội tại trong bộ nhớ bằng `TestClient` trên máy cục bộ. Độ trễ toàn trình (*end-to-end*) qua mạng Internet giữa trình duyệt (Vercel) và máy chủ backend (Render) chưa được đo đạc. Ngoài ra, gói Render miễn phí tự tạm dừng sau 15 phút không có truy cập; theo `docs/deployment/deploy-vercel-render.md`, yêu cầu đầu tiên đánh thức máy chủ (*cold start*) có thể mất khoảng 30–40 giây (thông số mô tả từ tài liệu triển khai, nhóm ghi nhận nhưng chưa đo thực nghiệm độc lập).
