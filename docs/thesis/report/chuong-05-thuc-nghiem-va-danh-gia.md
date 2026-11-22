# CHƯƠNG 5. KIỂM THỬ VÀ ĐÁNH GIÁ

## 5.1. Kiểm thử chức năng và ca biên

### 5.1.1. Tổng quan bộ kiểm thử tự động

Nhóm em viết mã theo hướng phát triển dựa trên kiểm thử (*Test-Driven Development – TDD*). Mọi số liệu thực nghiệm trong chương này đều lấy trực tiếp từ bộ test tự động (`pytest`) và chuỗi hàm tính điểm chạy trên Python 3.12 (Windows). Phép đo thực hiện trên 16 hồ sơ gia sư mẫu cùng 14 kịch bản đánh giá KB01–KB14. Bộ dữ liệu gồm 14 hồ sơ mô phỏng (`simulated`) và 2 hồ sơ thu thập công khai (`public_collected` là `GS-T06`, `GS-T07`, có học phí và lịch rảnh ước tính, điểm đánh giá nhận giá trị trung tính $0{,}5$). Tổng cộng có 200 bài kiểm thử tự động kiểm tra từ bước lọc bắt buộc, chuẩn hóa điểm, tổng hợp trọng số đến API (Bảng 5.1):

- **Kiểm thử đơn vị (132 bài):** gồm 129 bài kiểm thử logic trong `backend/tests/unit/` và 3 bài kiểm tra môi trường trong `backend/tests/test_environment.py`:
  - Năm hàm tính điểm thành phần ở Bảng 3.6 (`test_criteria.py`: 47 bài).
  - Lọc điều kiện bắt buộc (`test_filters.py`: 17 bài).
  - Ngưỡng dữ liệu tối thiểu (`test_eligibility.py`: 17 bài).
  - Quy đổi trọng số và chọn tiêu chí áp dụng (`test_weights.py`: 22 bài).
  - Xếp hạng và xử lý đồng điểm (`test_ranker.py`: 8 bài).
  - Tầng đọc và kiểm tra dữ liệu hồ sơ (`test_repository.py`: 13 bài).
  - Tham số cấu hình hệ thống (`test_config.py`: 5 bài).
- **Kiểm thử kịch bản và độ nhạy (27 bài trong `backend/tests/scenarios/`):** gồm 17 bài kiểm thử hồi quy cho 14 kịch bản KB01–KB14 (`test_scenarios.py`) và 10 bài khảo sát độ nhạy (`test_sensitivity_muc_5_2.py`).
- **Kiểm thử tích hợp API và ca biên (41 bài trong `backend/tests/api/`):** gồm 35 bài thử giao tiếp HTTP qua `TestClient` (`test_recommend_api.py`) và 6 bài thử ca biên, tính đơn điệu cùng thao tác đổi mức ưu tiên CN03 (`test_boundary_muc_5_1.py`).

Cả 200/200 bài test đều đạt (0 lỗi, 0 bỏ qua) và chạy hết trong 1,18 giây. Khi đo độ bao phủ bằng lệnh `pytest --cov=app`, tổng độ bao phủ đạt 97% trên toàn bộ khối mã nghiệp vụ `backend/app/` (340/351 câu lệnh, còn 11 câu lệnh chưa phủ). Mọi mô-đun xử lý chính như định tuyến API, cấu hình, đọc hồ sơ, lọc bắt buộc, tính trọng số, năm hàm điểm và mô hình Pydantic đều phủ đủ 100%. 11 câu lệnh còn lại nằm ở các nhánh kiểm tra phòng vệ bên trong `eligibility.py` (1 câu lệnh) và `ranker.py` (10 câu lệnh), vốn đã được tầng xác thực dữ liệu chặn trước khi vào API.

**Bảng 5.1: Phân bổ bộ kiểm thử tự động theo nhóm**

| Nhóm kiểm thử | Thư mục mã nguồn | Số lượng kiểm thử | Kết quả thực thi | Độ bao phủ mã nguồn (`backend/app/`) |
|:---|:---|:---:|:---:|:---:|
| Kiểm thử đơn vị (Unit Tests) | `backend/tests/unit/`, `backend/tests/test_environment.py` | 132 | 132/132 đạt | 84% (294/351 câu lệnh khi chạy riêng) |
| Kiểm thử kịch bản & độ nhạy | `backend/tests/scenarios/` | 27 | 27/27 đạt | 80% (280/351 câu lệnh khi chạy riêng) |
| Kiểm thử API & ca biên tích hợp | `backend/tests/api/` | 41 | 41/41 đạt | 93% (326/351 câu lệnh; 100% tầng API) |
| **Tổng cộng toàn hệ thống** | **`backend/tests/`** | **200** | **200/200 đạt (100%)** | **97% tổng hợp (340/351 câu lệnh)** |

*(Kết quả đo từ bộ kiểm thử tự động và thống kê độ bao phủ câu lệnh trên khối mã nghiệp vụ backend.)*

### 5.1.2. Kiểm thử hợp đồng API và hiệu năng xử lý nội tại

Nhóm em kiểm thử điểm cuối `POST /api/recommend` bằng `fastapi.testclient.TestClient` để đối chiếu với đặc tả ở Mục 4.4.1 trên bốn điểm:

1. **Cấu trúc JSON trả về:** dữ liệu gồm `status`, `total_candidates`, `qualified_candidates`, `insufficient_data_candidates` và mảng `results[]`. Mỗi phần tử trong `results[]` có đủ `rank`, `tutor_id`, `total_score`, `criteria_scores` (điểm thành phần 5 tiêu chí), `contributions` (mức đóng góp $C_i$), `reason` (lý do khuyến nghị) và `notes` (ghi chú dữ liệu).
2. **Thứ tự xếp hạng và xử lý đồng điểm:** kết quả sắp giảm dần theo `total_score`. Nếu bằng điểm nhau, hệ thống xếp tăng dần theo mã `tutor_id` để thứ tự luôn cố định qua mỗi lần chạy.
3. **Đủ các trạng thái phản hồi:** bộ test kiểm tra cả ba trạng thái trả về mã HTTP 200 (`success`, `no_match` cho hai trường hợp không có người qua lọc hoặc thiếu dữ liệu, và `zero_weight` khi $\sum w_i = 0$ kèm `unranked_candidates`). Ngoài ra còn có mã lỗi HTTP 422 (`422 Unprocessable Entity`) khi đầu vào sai ràng buộc Pydantic. Các tình huống đặc biệt được giải thích thêm ở Mục 5.1.4.
4. **Tốc độ xử lý nội tại:** nhóm em chạy kịch bản đo `scripts/thesis/benchmark_latency.py` trên 14 kịch bản KB01–KB14 với 140 lượt gọi API liên tiếp (10 lượt/kịch bản) qua `TestClient`. Thời gian xử lý trung bình là 3,54 ms và chậm nhất là 7,97 ms (sau lượt khởi tạo đầu). Khi tăng lên 700 lượt gọi liên tiếp, thời gian trung bình là 3,72 ms và chậm nhất là 26,64 ms. Mức này dư sức đáp ứng ngưỡng dưới 1.000 ms khi người học chỉnh mức ưu tiên trực tiếp trên giao diện (CN03).

Cần nói rõ là phép đo trên chạy trực tiếp trong bộ nhớ qua `TestClient`, nên chưa tính độ trễ truyền qua mạng. Kết quả phản ánh riêng tốc độ tính toán của thuật toán và tầng FastAPI, thấp hơn ngưỡng 1.000 ms khoảng hai bậc độ lớn.

### 5.1.3. Kiểm thử ca biên của hàm điểm và tính đơn điệu

Để kiểm tra năm hàm chấm điểm thành phần (Bảng 3.6) có chạy đúng ở các điểm biên và giữ tính đơn điệu khi chỉnh trọng số (CN03) hay không, nhóm em viết bộ test biên tự động cho từng tiêu chí. Kết quả được tổng hợp ở Bảng 5.2.

**Bảng 5.2: Kết quả kiểm thử ca biên của các hàm điểm và tính đơn điệu**

| Nhóm kiểm thử | Ca biên / Tình huống kiểm thử | Đầu vào thực nghiệm | Kết quả kỳ vọng (theo Bảng 3.6) | Kết quả thực tế hệ thống | Trạng thái |
|:---|:---|:---|:---|:---|:---:|
| **1. Học phí ($s_{\text{fee}}$, $\delta = 0{,}5$)** | Học phí bằng đúng ngân sách ($P = B$) | $B = 200.000\text{ VNĐ}$, $P = 200.000\text{ VNĐ}$ | $s_{\text{fee}} = 1{,}000$; lý do “học phí trong ngân sách” | $s_{\text{fee}} = 1{,}000$; lý do chứa “học phí trong ngân sách” | Đạt |
| | Học phí nằm giữa vùng dung sai ($P = 1{,}25 B$) | $B = 200.000\text{ VNĐ}$, $P = 250.000\text{ VNĐ}$ | $s_{\text{fee}} = 0{,}500$; lý do “học phí vượt ngân sách 25%” | $s_{\text{fee}} = 0{,}500$; lý do chứa “học phí vượt ngân sách 25%” | Đạt |
| | Học phí chạm biên trên dung sai 50% ($P = 1{,}50 B$) | $B = 200.000\text{ VNĐ}$, $P = 300.000\text{ VNĐ}$ | $s_{\text{fee}} = 0{,}000$; lý do “học phí vượt ngân sách 50%” | $s_{\text{fee}} = 0{,}000$; lý do chứa “học phí vượt ngân sách 50%” | Đạt |
| | Học phí vượt quá 50% ngân sách ($P > 1{,}50 B$) | $B = 200.000\text{ VNĐ}$, $P = 400.000\text{ VNĐ}$ (`GS-T06` tại KB01) | $s_{\text{fee}} = 0{,}000$; không bị loại cứng, lý do “học phí vượt ngân sách 100%” | $s_{\text{fee}} = 0{,}000$; lý do chứa “học phí vượt ngân sách 100%”, xếp hạng 3 tại KB01 | Đạt |
| | Ngân sách bằng 0 ($B = 0$) | $B = 0\text{ VNĐ}$, $P > 0$ | $s_{\text{fee}} = 0{,}000$; không phát sinh lỗi chia cho 0 | HTTP 200 OK; mọi ứng viên nhận $s_{\text{fee}} = 0{,}000$ | Đạt |
| **2. Kinh nghiệm ($s_{\text{experience}}$, $E_{\max} = 8$)** | Kinh nghiệm bằng 0 năm ($E = 0$) | $E = 0$ | $s_{\text{experience}} = 0{,}000$ | $s_{\text{experience}} = 0{,}000$ | Đạt |
| | Kinh nghiệm chạm mốc bão hòa ($E = 8$) | $E = 8$ (`GS-G06` tại KB11) | $s_{\text{experience}} = 1{,}000$ | $s_{\text{experience}} = 1{,}000$ | Đạt |
| | Kinh nghiệm vượt mốc bão hòa ($E > 8$) | $E = 12$ (`GS-G10`), $E = 20$ (`GS-T06`) | $s_{\text{experience}} = 1{,}000$ (chặn trên bão hòa tại $1{,}0$) | $s_{\text{experience}} = 1{,}000$ | Đạt |
| **3. Điểm đánh giá ($s_{\text{rating}}$)** | Gia sư chưa có đánh giá (`avg_rating = null`) | `GS-T06`, `GS-T07` (`public_collected`) | $s_{\text{rating}} = 0{,}500$ (trung tính); ghi chú “chưa có đánh giá”; không bị loại | $s_{\text{rating}} = 0{,}500$; `notes` chứa “chưa có đánh giá” | Đạt |
| | Điểm đánh giá tối đa ($R = 5{,}0$) | `GS-G01` ($R = 5{,}0$) | $s_{\text{rating}} = 1{,}000$ | $s_{\text{rating}} = 1{,}000$ | Đạt |
| **4. Lịch rảnh ($s_{\text{availability}}$)** | Khớp một phần khung giờ ($m/k$ với $1 \le m < k$) | Yêu cầu `["T2-tối", "T4-tối", "T6-tối"]` ($k=3$); `GS-G01` khớp 2 khung | Vượt lọc bắt buộc; $s_{\text{availability}} = 2/3 \approx 0{,}667$ | $s_{\text{availability}} = 0{,}6667 \approx 0{,}667$ | Đạt |
| | Khớp toàn bộ khung giờ ($k/k$) | Yêu cầu `["T2-tối", "T4-tối", "T6-tối"]` ($k=3$); `GS-T06` khớp cả 3 | $s_{\text{availability}} = 3/3 = 1{,}000$ | $s_{\text{availability}} = 1{,}000$ | Đạt |
| | Không giao khung giờ nào ($0/k$) | Khung giờ yêu cầu không giao với lịch rảnh của gia sư | Bị loại ngay ở bước lọc điều kiện bắt buộc | Không xuất hiện trong danh sách `results` | Đạt |
| **5. Tính đơn điệu & Tương tác CN03** | Tính đơn điệu theo ngân sách tối đa $B$ | Tăng $B$: $B_1 = 150.000 \rightarrow B_2 = 200.000 \rightarrow B_3 = 350.000\text{ VNĐ}$ | Điểm tổng $S(g)$ của mọi ứng viên không giảm: $S(g \mid B_1) \le S(g \mid B_2) \le S(g \mid B_3)$ | Thỏa mãn 100% trên toàn bộ ứng viên | Đạt |
| | Đổi mức ưu tiên trực tiếp trên kết quả (CN03) | Từ KB01 mặc định → đặt `fee = none`, `rating = none`, `experience = high` | `GS-T06` (20 năm kinh nghiệm) lên hạng 1 ($S = 1{,}000$); phản hồi $< 1.000$ ms | `GS-T06` lên hạng 1 ($S = 1{,}000$); xử lý qua `TestClient` đạt $\approx 3{,}5$ ms | Đạt |
| | Đặt toàn bộ 5 mức ưu tiên về `none` ($\sum w_i = 0$) | `priorities = {fee: none, district: none, experience: none, rating: none, availability: none}` | Trả về `status = "zero_weight"` kèm `unranked_candidates` | `status = "zero_weight"`; trả đủ 5 ứng viên của KB01 trong `unranked_candidates` | Đạt |

*(Các ca kiểm thử biên đều được tự động hóa trong bộ kiểm thử đơn vị và tích hợp API của hệ thống.)*

### 5.1.4. Xử lý các trường hợp đặc biệt

Với bốn tình huống biên đặc biệt, hệ thống xử lý nhất quán như sau:

1. **Không có gia sư thỏa điều kiện bắt buộc:** khi bộ lọc loại hết hồ sơ (ví dụ kịch bản KB05 tìm môn Tiếng Trung), API trả về `status = "no_match"`, `results = []` và `insufficient_data_candidates = []`. Giao diện hiện thông báo rõ lý do và gợi ý người học nới lỏng điều kiện.
2. **Học trực tuyến (`learning_mode = "online"`):** vì học qua mạng không phụ thuộc quận/huyện, hệ thống tắt tiêu chí khu vực. Giao diện khóa ô chọn quận, bộ tính trọng số bỏ `district` khỏi tổng trọng số, còn API trả `criteria_scores["district"] = null` và `contributions["district"] = null` (như KB04, KB08, KB14).
3. **Tổng trọng số bằng 0 ($\sum w_i = 0$):** khi người học chọn “Không quan tâm” (`none`) cho cả 5 tiêu chí, mẫu số công thức (2.1) bằng $0$. Hệ thống không chia cho 0 hay tự gán trọng số ngầm, mà trả về `zero_weight` kèm `unranked_candidates` là những gia sư đã qua lọc bắt buộc (Hình 4.4).
4. **Bỏ trống các trường tùy chọn:** nếu người học không nhập ngân sách, khu vực hoặc lịch rảnh thì hệ thống bỏ tiêu chí đó khỏi phép tính:
   - Bỏ trống ngân sách tối đa (`max_budget_vnd = null`, như KB05, KB10, KB14): không tính điểm học phí (`criteria_scores["fee"] = null`, `contributions["fee"] = null`).
   - Không chọn quận/huyện khi học trực tiếp hoặc hình thức bất kỳ (`any`, như KB05, KB13): không tính điểm khu vực.
   - Không chọn lịch rảnh (`time_slots = []`, gặp ở 12/14 kịch bản: KB01–KB03, KB05–KB07, KB09–KB14): không tính điểm lịch rảnh (`criteria_scores["availability"] = null`, `contributions["availability"] = null`).

Mỗi khi có tiêu chí bị bỏ qua, mẫu số chỉ cộng trọng số của tập tiêu chí còn lại $A$ ($\sum_{j \in A} w_j$). Nhờ vậy tổng điểm $S(g)$ luôn nằm trong đoạn $[0, 1]$.

## 5.2. Đánh giá chất lượng xếp hạng

### 5.2.1. So khớp Top-3 hệ thống với kỳ vọng trên 14 kịch bản

Bảng 5.3 đối chiếu kết quả chạy thật của hệ thống với danh sách Top-3 kỳ vọng (lập sẵn trong `scenarios.json`) trên 14 kịch bản KB01–KB14 với 16 hồ sơ mẫu.

Nhóm em quy ước cách ghi tỷ lệ trùng khớp như sau:
- Nếu danh sách kỳ vọng có $m$ gia sư ($1 \le m \le 3$), số gia sư khớp đúng được ghi dạng $x/m$.
- Kịch bản KB05 thử trường hợp không có ứng viên (`no_match`), nếu hệ thống trả về mảng rỗng đúng kỳ vọng thì ghi là `0/0`.
- Các gia sư bằng điểm tuyệt đối (ở KB02 và KB12) được xếp tăng dần theo mã `tutor_id`.

**Bảng 5.3: Kết quả thực nghiệm 14 kịch bản đánh giá**

| Mã KB | Mô tả nhu cầu | Top-3 kỳ vọng (`scenarios.json`) | Top-3 hệ thống (Chạy thực tế qua pipeline) | Số trùng ($x/m$) | Nhận xét thực nghiệm |
|:---:|:---|:---|:---|:---:|:---|
| **KB01** | Toán, trực tiếp, Bình Thạnh, ngân sách 200.000 VNĐ, mọi ưu tiên Trung bình | 1. GS-G01 (0,938)<br/>2. GS-G10 (0,745)<br/>3. GS-T06 (0,625) | 1. GS-G01 (0,938)<br/>2. GS-G10 (0,745)<br/>3. GS-T06 (0,625) | 3/3 | Khớp thứ hạng và điểm số; `GS-T06` vượt ngân sách 100% ($s_{\text{fee}} = 0$) nên xếp hạng 3 và nhận điểm đánh giá trung tính $0{,}5$. |
| **KB02** | Anh Văn, trực tiếp, Quận 2, ngân sách 220.000 VNĐ, mọi ưu tiên Trung bình | 1–2. GS-G11 = GS-G12 (0,881, đồng hạng)<br/>3. GS-T07 (0,5625) | 1. GS-G11 (0,881)<br/>2. GS-G12 (0,881)<br/>3. GS-T07 (0,5625) | 3/3 | Khớp tập hợp, thứ hạng và điểm số; `GS-G11` và `GS-G12` đồng điểm tuyệt đối ($0{,}88125$), xử lý đồng điểm đưa `GS-G11` xếp trước. |
| **KB03** | Anh Văn, trực tiếp, Thủ Đức, ngân sách 220.000 VNĐ, mọi ưu tiên Trung bình | 1. GS-G12 (0,881)<br/>2. GS-G11 (0,631)<br/>3. GS-T07 (0,5625) | 1. GS-G12 (0,881)<br/>2. GS-G11 (0,631)<br/>3. GS-T07 (0,5625) | 3/3 | Khớp thứ hạng và điểm số; `GS-G12` khớp khu vực Thủ Đức nên xếp hạng 1. |
| **KB04** | Lý, trực tuyến, ngân sách 200.000 VNĐ, lịch T2-tối & T4-tối, mọi ưu tiên Trung bình | 1. GS006 (0,848)<br/>2. GS020 (0,715) | 1. GS006 (0,886)<br/>2. GS020 (0,786) | 2/2 | Khớp thứ hạng (`GS006 > GS020`); điểm hệ thống ($0{,}886$ và $0{,}786$) khác điểm tính tay ban đầu ($0{,}848$ và $0{,}715$) do tính tay bỏ sót tiêu chí lịch rảnh. |
| **KB05** | Tiếng Trung, hình thức bất kỳ (`any`), mọi ưu tiên Trung bình | (không có ứng viên)<br/>`[]` | (không có ứng viên)<br/>`[]` (`status = "no_match"`) | 0/0 | Khớp kỳ vọng; hệ thống kích hoạt trạng thái `no_match` khi không có ứng viên nào dạy môn Tiếng Trung. |
| **KB06** | Văn, trực tiếp, Quận 1, ngân sách 180.000 VNĐ, mọi ưu tiên Trung bình | 1. GS-G04 (0,934) | 1. GS-G04 (0,934) | 1/1 | Khớp thứ hạng và điểm làm tròn (điểm chính xác: $2 \times (1 + 1 + 0{,}875 + 0{,}86) / 8 = 7{,}47 / 8 = 0{,}93375 \approx 0{,}934$). |
| **KB07** | Sinh, hình thức bất kỳ (`any`), Thủ Đức, ngân sách 200.000 VNĐ, mọi ưu tiên Trung bình | 1. GS-G05 (0,825) | 1. GS-G05 (0,825) | 1/1 | Khớp thứ hạng và điểm số ($0{,}825$). |
| **KB08** | Tin học, trực tuyến, ngân sách 250.000 VNĐ, lịch T2-tối & T6-tối, mọi ưu tiên Trung bình | 1. GS-G07 (0,876) | 1. GS-G07 (0,876) | 1/1 | Khớp thứ hạng và điểm làm tròn (điểm chính xác: $0{,}87625 \approx 0{,}876$). |
| **KB09** | Tiếng Nhật, hình thức bất kỳ (`any`), Phú Nhuận, ngân sách 280.000 VNĐ, mọi ưu tiên Trung bình | 1. GS-G08 (0,928) | 1. GS-G08 (0,9275) | 1/1 | Khớp thứ hạng 1/1; điểm chính xác là $0{,}9275$ (tính tay làm tròn thập phân lên $0{,}928$; biểu diễn nhị phân IEEE 754 làm tròn thành $0{,}927$). |
| **KB10** | Toán, trực tiếp, Quận 7, không nhập ngân sách, ưu tiên Kinh nghiệm Cao | 1. GS-G10 (0,994)<br/>2. GS-G01 (0,607)<br/>3. GS-G09 (0,593) | 1. GS-G10 (0,994)<br/>2. GS-G01 (0,607)<br/>3. GS-G09 (0,593) | 3/3 | Khớp thứ hạng và điểm số; `GS-T06` ($0{,}571$) đứng hạng 4 ngoài Top-3 đúng phân tích lý thuyết. |
| **KB11** | Hóa, trực tiếp, Quận 10, ngân sách 220.000 VNĐ, mọi ưu tiên Trung bình | 1. GS-G06 (0,985)<br/>2. GS-T06 (0,375) | 1. GS-G06 (0,985)<br/>2. GS-T06 (0,375) | 2/2 | Khớp thứ hạng và điểm số; `GS-T06` có $s_{\text{fee}} = 0$ do học phí vượt trần dung sai. |
| **KB12** | Anh Văn, trực tiếp, Bình Chánh, ngân sách 200.000 VNĐ, mọi ưu tiên Trung bình | 1. GS-T07 (0,8125)<br/>2–3. GS-G11 = GS-G12 (0,631, đồng hạng) | 1. GS-T07 (0,8125)<br/>2. GS-G11 (0,631)<br/>3. GS-G12 (0,631) | 3/3 | Khớp tập hợp, thứ hạng và điểm số; `GS-T07` đứng đầu nhờ khớp khu vực; `GS-G11` và `GS-G12` đồng điểm hạng 2–3 ($0{,}63125$), xếp theo mã gia sư. |
| **KB13** | Toán, hình thức bất kỳ (`any`), ngân sách 150.000 VNĐ, không nhập khu vực & lịch, mọi ưu tiên Trung bình | 1. GS-G10 (0,993)<br/>2. GS-G01 (0,783)<br/>3. GS-T06 (0,50) | 1. GS-G10 (0,993)<br/>2. GS-G01 (0,783)<br/>3. GS-T06 (0,500) | 3/3 | Khớp thứ hạng và điểm số trên 3 tiêu chí áp dụng (học phí, kinh nghiệm, đánh giá). |
| **KB14** | Anh Văn, trực tuyến, không nhập ngân sách, khu vực và lịch, mọi ưu tiên Trung bình | 1. GS-G03 (0,70) | 1. GS-G03 (0,700) | 1/1 | Khớp thứ hạng và điểm số ($0{,}700$) trên hai tiêu chí áp dụng (kinh nghiệm và đánh giá). |

*(Đối chiếu giữa danh sách Top-3 kỳ vọng trong bộ kịch bản đánh giá và kết quả thực thi trên 16 hồ sơ mẫu; quy ước KB05 không có ứng viên trả về trạng thái `no_match` với tỷ lệ khớp 0/0.)*

Bảng 5.4 gom 14 kịch bản thành năm nhóm đặc trưng để dễ nhìn kết quả tổng hợp.

**Bảng 5.4: Tổng hợp kết quả đối chiếu Top-3 theo nhóm đặc trưng kịch bản**

| Nhóm kịch bản thực nghiệm | Các kịch bản | Số kịch bản | Tỷ lệ khớp tập hợp & thứ tự Top-3 | Độ lệch điểm tuyệt đối lớn nhất $\max \lvert \Delta S \rvert$ | Ghi chú kỹ thuật |
|:---|:---|:---:|:---:|:---:|:---|
| Đủ $\ge 3$ ứng viên, điểm khớp hoàn toàn (đến 3 chữ số thập phân) | KB01, KB03, KB10, KB13 | 4 | 4/4 (100%) | $\le 0{,}0005$ | Khớp cả thứ tự lẫn giá trị điểm hiển thị |
| Đủ $\ge 3$ ứng viên, có đồng điểm tuyệt đối trong Top-3 | KB02, KB12 | 2 | 2/2 (100%) | $\le 0{,}00025$ | `GS-G11` và `GS-G12` đồng điểm ($0{,}88125$ ở KB02; $0{,}63125$ ở KB12), xử lý đồng điểm theo mã `tutor_id` |
| Môn hoặc điều kiện hiếm, chỉ có 1–2 ứng viên qua lọc | KB06, KB07, KB08, KB11, KB14 | 5 | 5/5 (100%) | $\le 0{,}00025$ | Khớp toàn bộ ứng viên qua lọc ($1/1$ hoặc $2/2$) |
| Có chênh lệch giữa điểm hệ thống tính và điểm tính tay ban đầu nhưng bảo toàn thứ tự | KB04, KB09 | 2 | 2/2 (100%) | $0{,}07125$ (KB04); $0{,}0005$ (KB09) | KB04: tính tay bỏ sót $s_{\text{availability}}$; KB09: khác quy tắc làm tròn tại biên $0{,}9275$ |
| Không có ứng viên thỏa điều kiện bắt buộc (`no_match`) | KB05 | 1 | 1/1 (100%) | Không áp dụng | Trả về `status = "no_match"`, `results = []` (khớp quy ước `0/0`) |
| **Tổng hợp toàn bộ tập kịch bản** | **KB01–KB14** | **14** | **14/14 (100%)** | **$0{,}07125$** | **Bảo toàn 100% tập hợp và thứ tự Top-3 kỳ vọng** |

*(Tổng hợp từ kết quả chạy cấu hình gốc trên toàn bộ 14 kịch bản thực nghiệm.)*

Nhìn chung, hệ thống trả về Top-3 khớp 14/14 kịch bản (100%), không có ca nào bị đảo hạng hay gợi ý nhầm người. Khi rà lại từng con số giữa kết quả máy chạy và bảng tính tay ban đầu, nhóm em thấy ba điểm đáng chú ý:

1. **Kịch bản KB04 (lệch điểm do khi tính tay quên cộng lịch rảnh):**
   - KB04 tìm gia sư môn Lý, học trực tuyến (`online`), ngân sách 200.000 VNĐ/giờ và chọn lịch `["T2-tối", "T4-tối"]`. Theo quy tắc ở Mục 3.6, học trực tuyến chỉ bỏ tiêu chí khu vực, còn lịch rảnh vẫn tính bình thường. Thành ra hệ thống tính đủ 4 tiêu chí (học phí, kinh nghiệm, đánh giá, lịch rảnh) với tổng trọng số $\sum w_i = 2 + 2 + 2 + 2 = 8$. Cả `GS006` và `GS020` đều trùng đủ lịch rảnh nên đạt $s_{\text{availability}} = 1{,}0$.
   - Thay số vào công thức (2.1) và Bảng 3.6, kết quả máy tính ra ở biểu thức (5.1) và (5.2):
     $$S(\text{GS006}) = \frac{2 \times 1{,}0 + 2 \times 0{,}625 + 2 \times 0{,}92 + 2 \times 1{,}0}{8} = \frac{7{,}09}{8} = 0{,}88625 \approx 0{,}886 \qquad (5.1)$$
     $$S(\text{GS020}) = \frac{2 \times 0{,}6 + 2 \times 0{,}625 + 2 \times 0{,}92 + 2 \times 1{,}0}{8} = \frac{6{,}29}{8} = 0{,}78625 \approx 0{,}786 \qquad (5.2)$$
   - Sở dĩ bảng tính tay ban đầu ra thấp hơn ($0{,}848$ và $0{,}715$) là vì lúc tính tay nhóm em chỉ cộng 3 tiêu chí (chia cho 6) mà quên mất tiêu chí lịch rảnh. Do cả hai gia sư đều được $s_{\text{availability}} = 1{,}0$, việc tính đủ 4 tiêu chí chỉ làm điểm cả hai tăng lên chứ thứ tự `GS006 > GS020` vẫn giữ nguyên.
2. **Kịch bản KB09 (lệch ở chữ số làm tròn theo chuẩn IEEE 754):**
   - Ứng viên `GS-G08` có $s_{\text{fee}} = 1{,}0$, $s_{\text{district}} = 1{,}0$, $s_{\text{experience}} = 6/8 = 0{,}75$ và $s_{\text{rating}} = 4{,}8/5 = 0{,}96$. Chia cho 4 tiêu chí thì tổng điểm đúng toán học là $(1{,}0 + 1{,}0 + 0{,}75 + 0{,}96)/4 = 3{,}71/4 = 0{,}9275$.
   - Tính tay theo kiểu thập phân thì $0{,}9275$ làm tròn lên thành $0{,}928$. Nhưng Python lưu số thực theo chuẩn nhị phân IEEE 754, trong đó $0{,}9275$ bị xấp xỉ thành `0.927499999999999991118...` (hơi nhỏ hơn $0{,}9275$). Do đó khi làm tròn 3 chữ số để hiển thị, kết quả ra $0{,}927$. Vì hàm xếp hạng dùng giá trị số thực gốc chưa làm tròn (quy ước QĐ-E) nên vị trí hạng 1 của `GS-G08` không bị ảnh hưởng.
3. **Kịch bản KB02 và KB12 (tách hạng khi bằng điểm):**
   - Ở KB02, `GS-G11` và `GS-G12` có các điểm thành phần giống hệt nhau nên tổng điểm bằng nhau ($7{,}05/8 = 0{,}88125$). Hệ thống xếp theo mã gia sư tăng dần nên `GS-G11` đứng hạng 1 và `GS-G12` đứng hạng 2.
   - Tương tự ở KB12, hai gia sư này cùng đạt $5{,}05/8 = 0{,}63125$ ở hạng 2–3, và `GS-G11` tiếp tục đứng trước `GS-G12`.

### 5.2.2. Thứ hạng bất hợp lý và quyết định điều chỉnh

Khi kiểm tra lại cả 14 kịch bản ở cấu hình gốc (*baseline*), nhóm em không thấy thứ hạng nào bị bất hợp lý. Những kịch bản chỉ có 1 ứng viên đều trả về đúng người đó. Hai chỗ lệch số ở KB04 và KB09 cũng chỉ do sót tiêu chí lúc tính tay và cách làm tròn hiển thị, không làm sai thứ tự.

Vì vậy, nhóm em giữ nguyên công thức điểm (Bảng 3.6), bộ tham số gốc ($\delta = 0{,}5$, $E_{\max} = 8$, trọng số Bảng 3.5) và bộ kịch bản chuẩn trong `scenarios.json` để các phép đối chiếu sau được nhất quán.

### 5.2.3. Khảo sát tính ổn định và độ nhạy tham số

Nhóm em thử độ ổn định của mô hình bằng cách thay đổi lần lượt ba yếu tố trên cả 14 kịch bản: hệ số dung sai học phí $\delta$, mốc kinh nghiệm bão hòa $E_{\max}$ và ngân sách tối đa của người học. Cấu hình gốc (*baseline*) dùng $\delta = 0{,}50$, $E_{\max} = 8$ năm, trọng số theo Bảng 3.5 và ngân sách gốc của từng kịch bản. Kết quả nằm ở Bảng 5.5 ($\delta$), Bảng 5.6 ($E_{\max}$) và Bảng 5.7 (ngân sách).

**Bảng 5.5: Độ nhạy của Top-3 theo tham số dung sai học phí $\delta$**

| $\delta$ | Số KB đổi Top-3 | KB đổi | Số KB trùng Top-3 baseline ($x/m$) |
|:---:|:---:|:---:|:---:|
| 0,25 | 0 | — | 14/14 |
| 0,30 | 0 | — | 14/14 |
| 0,50 (baseline) | 0 | — | 14/14 |
| 0,70 | 0 | — | 14/14 |
| 0,75 | 0 | — | 14/14 |
| 1,00 | 0 | — | 14/14 |

Ở Bảng 5.5, cả 6 mức $\delta \in [0{,}25; 1{,}00]$ đều cho 0/14 kịch bản đổi Top-3. Lý do khá dễ thấy: gia sư có học phí nằm trong ngân sách luôn giữ $s_{\text{fee}} = 1$, còn gia sư vượt ngân sách thì khi tăng $\delta$ điểm học phí có nhích lên nhưng vẫn thấp hơn người không vượt. Trên tập 16 hồ sơ mẫu, mức thay đổi đó chưa đủ làm đảo thứ tự Top-3.

**Bảng 5.6: Độ nhạy của Top-3 theo mốc kinh nghiệm bão hòa $E_{\max}$**

| $E_{\max}$ | Số KB đổi Top-3 | KB đổi | Top-3 của KB10 | Số KB trùng Top-3 baseline ($x/m$) |
|:---:|:---:|:---:|:---|:---:|
| 5 | 0 | — | `GS-G10 > GS-G01 > GS-G09` | 14/14 |
| 6 | 0 | — | `GS-G10 > GS-G01 > GS-G09` | 14/14 |
| 8 (baseline) | 0 | — | `GS-G10 > GS-G01 > GS-G09` | 14/14 |
| 10 | 1 | KB10 | `GS-G10 > GS-G09 > GS-T06` | 13/14 |
| 12 | 1 | KB10 | `GS-G10 > GS-T06 > GS-G09` | 13/14 |

Khi thay đổi $E_{\max}$ (Bảng 5.6), chỉ có kịch bản KB10 đổi Top-3 ở mốc $E_{\max} = 10$ và $E_{\max} = 12$. Nhóm em tính lại chi tiết để kiểm chứng nguyên nhân:
- Truy vấn KB10 tìm môn Toán ở Quận 7, không nhập ngân sách và lịch rảnh. Hệ thống chỉ dùng 3 tiêu chí là Khu vực ($w = 2$), Kinh nghiệm ($w = 3$, mức Cao) và Đánh giá ($w = 2$), tổng trọng số bằng 7.
- **Vì sao `GS-G01` rời khỏi Top-3:** ở mốc gốc $E_{\max} = 8$, `GS-G01` ($E = 6$ năm, dạy Bình Thạnh nên $s_{\text{district}} = 0$, đánh giá $5{,}0/5$) được $(2 \times 0 + 3 \times 6/8 + 2 \times 1{,}0)/7 = 4{,}25/7 \approx 0{,}6071$, đứng hạng 2. Khi tăng $E_{\max}$ lên $10$ và $12$, điểm kinh nghiệm của `GS-G01` tụt xuống $6/10 = 0{,}60$ và $6/12 = 0{,}50$. Tổng điểm giảm còn $3{,}8/7 \approx 0{,}5429$ rồi $3{,}5/7 = 0{,}5000$ (hạng 4). Vị trí trong Top-3 lúc này thuộc về `GS-T06` ($E = 20$ năm, luôn chạm trần $s_{\text{experience}} = 1{,}0$).
- **Vì sao `GS-G09` và `GS-T06` đổi chỗ từ $E_{\max} = 10$ sang $12$:** tại $E_{\max} = 10$, `GS-G09` ($E = 2$ năm, đúng Quận 7, đánh giá $3{,}5/5$) đạt $(2 \times 1 + 3 \times 2/10 + 2 \times 0{,}7)/7 = 4/7$. Đúng lúc này `GS-T06` cũng đạt $(2 \times 0 + 3 \times 1 + 2 \times 0{,}5)/7 = 4/7$ (hai số thực bằng nhau tuyệt đối `0.5714285714285714`). Nhờ quy tắc xếp theo mã gia sư (`"GS-G09" < "GS-T06"`), `GS-G09` đứng hạng 2 còn `GS-T06` hạng 3. Sang $E_{\max} = 12$, điểm của `GS-G09` tụt xuống $(2 \times 1 + 3 \times 2/12 + 2 \times 0{,}7)/7 = 3{,}9/7 \approx 0{,}5571$. Trong khi đó `GS-T06` vẫn giữ $4/7 \approx 0{,}5714$ nên vượt lên hạng 2, tạo thành thứ tự `GS-G10 > GS-T06 > GS-G09`.

**Bảng 5.7: Độ nhạy của Top-3 theo mức biến động ngân sách**

| Mức ngân sách | Số KB áp dụng | Số KB đổi Top-3 | KB đổi | Số KB áp dụng trùng Top-3 baseline ($x/m$) |
|:---:|:---:|:---:|:---:|:---:|
| −20% | 11 | 0 | — | 11/11 |
| −10% | 11 | 0 | — | 11/11 |
| −5% | 11 | 0 | — | 11/11 |
| 0% (baseline) | 11 | 0 | — | 11/11 |
| +5% | 11 | 0 | — | 11/11 |
| +10% | 11 | 0 | — | 11/11 |
| +20% | 11 | 0 | — | 11/11 |

*(Ba kịch bản KB05, KB10 và KB14 không thiết lập ngân sách nên phép biến thiên ngân sách áp dụng trên 11 kịch bản còn lại.)*

Trong 11 kịch bản có nhập ngân sách (Bảng 5.7), không kịch bản nào đổi Top-3 khi thay đổi ngân sách trong khoảng từ −20% đến +20%. Bộ test tự động cũng xác nhận hàm điểm giữ đúng tính đơn điệu: $S(g)$ không giảm khi $\delta$ hoặc ngân sách $B$ tăng, và không tăng khi $E_{\max}$ tăng. Tính đơn điệu là hệ quả trực tiếp của công thức, còn việc Top-3 ít biến động khi đổi $\delta$ và ngân sách là do phân bố của 16 hồ sơ mẫu hiện tại.

### 5.2.4. Ảnh hưởng của các bộ mức ưu tiên

Tiếp theo, nhóm em thử áp bốn bộ mức ưu tiên khác nhau lên toàn bộ 14 kịch bản: Mặc định (`default`), Ưu tiên Khu vực (`prioritize_district`), Ưu tiên Học phí (`prioritize_fee`) và Ưu tiên Kinh nghiệm & Đánh giá (`prioritize_experience_rating`). Kết quả được tóm tắt ở Bảng 5.8.

**Bảng 5.8: Ảnh hưởng của bốn bộ mức ưu tiên đến Top-3**

| Bộ mức ưu tiên | Số KB đổi Top-3 | KB đổi Top-3 | Thay đổi Top-3 cụ thể |
|:---|:---:|:---:|:---|
| Mặc định (tất cả Trung bình) | 1 | KB10 | `GS-G10 > GS-G09 > GS-G01` thay cho `GS-G10 > GS-G01 > GS-G09`: đảo hạng 2–3, cùng tập hợp 3/3 |
| Ưu tiên Khu vực (`district` Cao, còn lại Thấp) | 2 | KB01, KB10 | KB01: `GS-G01 > GS-T06 > GS-G02` thay cho `GS-G01 > GS-G10 > GS-T06`; `GS-G10` rời Top-3 do không dạy Bình Thạnh, `GS-T06` lên hạng 2, `GS-G02` hạng 3 (trùng 2/3). KB10: `GS-G10 > GS-G09 > GS-G01` (đảo hạng 2–3, cùng tập 3/3) |
| Ưu tiên Học phí (`fee` Cao, còn lại Thấp) | 1 | KB10 | `GS-G10 > GS-G09 > GS-G01` thay cho `GS-G10 > GS-G01 > GS-G09` (đảo hạng 2–3, cùng tập 3/3); KB01 giữ nguyên |
| Ưu tiên Kinh nghiệm & Đánh giá (`experience` & `rating` Cao, còn lại Thấp) | 1 | KB10 | `GS-G10 > GS-G01 > GS-T06` thay cho `GS-G10 > GS-G01 > GS-G09`: `GS-T06` vào Top-3 thay cho `GS-G09` (trùng 2/3) |

Từ Bảng 5.8, nhóm em rút ra ba nhận xét chính:
- Ở KB01, khi bật bộ Ưu tiên Khu vực, gia sư `GS-G10` không dạy ở Bình Thạnh ($s_{\text{district}} = 0$) nên rớt khỏi Top-3. Hai gia sư dạy tại Bình Thạnh là `GS-T06` và `GS-G02` ($s_{\text{district}} = 1$) lên hạng 2 và hạng 3. Điều này cho thấy trọng số ưu tiên điều chỉnh thứ hạng đúng như người học mong muốn.
- Ở KB10 (mặc định đặt Kinh nghiệm mức Cao, $w = 3$), khi chuyển sang bộ Mặc định hoặc Ưu tiên Học phí (mà KB10 lại không nhập ngân sách), trọng số Kinh nghiệm giảm xuống ngang Khu vực. Nhờ vậy `GS-G09` (khớp Quận 7) vượt `GS-G01` để lên hạng 2. Ngược lại, khi dùng bộ Ưu tiên Kinh nghiệm & Đánh giá, `GS-T06` (20 năm kinh nghiệm) vượt `GS-G09` (2 năm kinh nghiệm) để lọt vào Top-3.
- Cả bốn lần thử đều giữ nguyên hạng 1 ở KB01 (`GS-G01`) và KB10 (`GS-G10`), vì hai gia sư này nổi trội hơn hẳn ở nhiều tiêu chí cùng lúc.

### 5.2.5. Khả năng giải thích của kết quả gợi ý

Với mô hình Weighted Scoring, người học nhìn thấy rõ điểm tổng hợp $S(g)$ được cộng từ mức đóng góp $C_i$ của từng tiêu chí nào, kèm theo câu lý do ngắn gọn. Bảng 5.9 trích kết quả thật từ `POST /api/recommend` cho kịch bản KB01.

**Bảng 5.9: Thành phần điểm và mức đóng góp của Top-3 gia sư tại KB01**

| Hạng | Gia sư | Điểm tổng $S$ | Điểm thành phần `criteria_scores`<br/>(`fee`; `district`; `experience`; `rating`; `availability`) | Mức đóng góp `contributions`<br/>(`fee`; `district`; `experience`; `rating`; `availability`) |
|:---:|:---|:---:|:---|:---|
| 1 | GS-G01 | 0,9375 | 1,0000; 1,0000; 0,7500; 1,0000; null | 0,2500; 0,2500; 0,1875; 0,2500; null |
| 2 | GS-G10 | 0,7450 | 1,0000; 0,0000; 1,0000; 0,9800; null | 0,2500; 0,0000; 0,2500; 0,2450; null |
| 3 | GS-T06 | 0,6250 | 0,0000; 1,0000; 1,0000; 0,5000; null | 0,0000; 0,2500; 0,2500; 0,1250; null |

*(Giá trị điểm thành phần và mức đóng góp trích từ phản hồi HTTP 200 của dịch vụ khuyến nghị cho kịch bản KB01.)*

Mỗi gia sư trong Bảng 5.9 đi kèm chuỗi lý do (`reason`) và ghi chú (`notes`) như sau:
- **GS-G01:** Lý do: “Học phí trong ngân sách, khu vực khớp, đánh giá 5,0/5”; Ghi chú: `[]`.
- **GS-G10:** Lý do: “Học phí trong ngân sách, kinh nghiệm 12 năm, đánh giá 4,9/5”; Ghi chú: `[]`.
- **GS-T06:** Lý do: “Khu vực khớp, kinh nghiệm 20 năm, đánh giá trung tính (0,5)”; Ghi chú: `["chưa có đánh giá"]`.

Nhìn vào kết quả này, người học biết ngay ba điều:
1. Cộng tất cả các mức đóng góp $C_i$ lại thì đúng bằng tổng điểm $S(g) = \sum C_i$.
2. Dễ thấy ngay điểm mạnh và điểm trừ của từng người: chẳng hạn `GS-G10` bị $C_{\text{district}} = 0{,}0000$ vì khác quận, còn `GS-T06` bị $C_{\text{fee}} = 0{,}0000$ vì học phí vượt trần dung sai.
3. Hồ sơ nào chưa có đánh giá thực tế (`GS-T06`) đều hiện chú thích rõ ở trường `notes`, tránh gây hiểu nhầm điểm trung tính $0{,}5$ là điểm đánh giá thật.

## 5.3. Hạn chế của hệ thống

Bên cạnh các kết quả đạt được, nhóm em nhận thấy hệ thống còn sáu hạn chế:

1. **Bộ dữ liệu mẫu còn ít:** mới có 16 hồ sơ (14 hồ sơ giả lập `simulated` và 2 hồ sơ lấy từ nguồn công khai `public_collected` là `GS-T06`, `GS-T07`). Ở hai hồ sơ công khai, học phí và lịch rảnh phải ước tính theo mặt bằng khảo sát (đánh dấu `(*)` ở Phụ lục A), còn điểm đánh giá để trống nên nhận mức trung tính $0{,}5$.
2. **Kịch bản thử nghiệm do nhóm em tự lập:** 14 kịch bản KB01–KB14 và Top-3 kỳ vọng được xây dựa trên phân tích bài toán để kiểm tra thuật toán, chưa phải dữ liệu thu từ lựa chọn thật của phụ huynh hay học sinh. Vì vậy tỷ lệ khớp 14/14 cho thấy mã nguồn chạy đúng với công thức ở Chương 3, chưa đo được mức độ hài lòng của người dùng ngoài đời.
3. **Tham số công thức đặt thủ công:** các mốc $\delta = 0{,}5$, $E_{\max} = 8$ năm, điểm trung tính $0{,}5$ và bộ trọng số $\{0, 1, 2, 3\}$ do nhóm em tự chọn ban đầu, chưa được học từ dữ liệu tương tác thực tế.
4. **Chưa thử nghiệm với người dùng ngoài nhóm:** nhóm em chưa tổ chức khảo sát học sinh hay phụ huynh bên ngoài để xem họ có đồng ý với gợi ý của hệ thống hay không.
5. **So khớp khu vực và môn học còn đơn giản:** khu vực chỉ so khớp đúng tên quận/huyện quy ước, chưa tính khoảng cách đường đi hay các quận giáp ranh. Mỗi lần tìm cũng chỉ chọn được một môn học.
6. **Chưa đo độ trễ mạng thật qua Internet:** con số trung bình 3,54 ms ở Mục 5.1.2 đo nội bộ qua `TestClient`. Độ trễ thật khi người dùng gọi từ trình duyệt trên Vercel sang máy chủ Render (cộng thêm 30–40 giây khởi động lại của gói Render miễn phí sau 15 phút nghỉ) chưa được đo thành số liệu cụ thể.

Tóm lại, thực nghiệm ở Chương 5 cho thấy bộ máy khuyến nghị chạy ổn định: đạt 200/200 bài kiểm thử tự động (độ bao phủ 97%), khớp 14/14 kịch bản Top-3 và tính toán nội tại chỉ mất vài phần nghìn giây. Sáu hạn chế vừa nêu cũng là cơ sở để nhóm em tổng kết và đề xuất hướng phát triển ở Chương 6.
