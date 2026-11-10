# CHƯƠNG 5. KIỂM THỬ VÀ ĐÁNH GIÁ

> [!NOTE]
> **Đề xuất, nhóm xác nhận**

**Phạm vi và bối cảnh thực nghiệm.** Chương này trình bày toàn bộ kết quả kiểm thử chức năng, kiểm thử ca biên và đánh giá chất lượng xếp hạng của hệ thống gợi ý gia sư thuộc đề tài "Hệ thống khuyến nghị gia sư dựa trên phương pháp Content-Base Filtering". Mọi số liệu thực nghiệm được thu thập trực tiếp từ việc chạy lại bộ kiểm thử tự động (`pytest`) và quy trình tính toán thực tế trên môi trường phát triển (Python 3.12, FastAPI backend, React frontend trên hệ điều hành Windows), gắn liền với commit gốc `f66f065` (thời điểm trích xuất dữ liệu thô `docs/thesis/report/muc-5.2-ket-qua-tho.json`) và commit `d9548ce` trên nhánh chính (`origin/main`). Không gian dữ liệu thử nghiệm bao gồm 16 hồ sơ gia sư chuẩn hóa tại `data/processed/tutors.json` (trong đó có 14 hồ sơ mô phỏng `simulated` và 2 hồ sơ `public_collected` là GS-T06 và GS-T07 có học phí và lịch rảnh ước tính, điểm đánh giá để trống và được gán giá trị trung tính 0,5 khi tính điểm theo Phụ lục A) cùng 14 kịch bản đánh giá cố định KB01–KB14 tại `backend/tests/scenarios/scenarios.json`.

---

## 5.1. Kiểm thử chức năng và ca biên

### 5.1.1. Tổng quan bộ kiểm thử tự động

Hệ thống được xây dựng và kiểm thử theo phương pháp phát triển hướng kiểm thử (TDD). Toàn bộ quy trình tính toán, lọc điều kiện, chuẩn hóa điểm số và hợp đồng giao tiếp API được kiểm định bởi bộ kiểm thử tự động gồm 200 bài kiểm thử, phân bổ theo các thư mục trong `backend/tests/`:

- **Kiểm thử đơn vị (`backend/tests/unit/` và `backend/tests/test_environment.py`):** Gồm 132 bài kiểm thử (129 bài trong `backend/tests/unit/` và 3 bài kiểm tra môi trường trong `backend/tests/test_environment.py`). Nhóm này bao phủ các hàm chuẩn hóa điểm thành phần Bảng 3.6 (`backend/tests/unit/test_criteria.py`: 47 bài), quy tắc lọc điều kiện bắt buộc (`backend/tests/unit/test_filters.py`: 17 bài), kiểm tra ngưỡng dữ liệu tối thiểu (`backend/tests/unit/test_eligibility.py`: 17 bài), quy đổi trọng số và mức ưu tiên (`backend/tests/unit/test_weights.py`: 22 bài), thuật toán xếp hạng và phá hòa (`backend/tests/unit/test_ranker.py`: 8 bài), tầng truy xuất dữ liệu (`backend/tests/unit/test_repository.py`: 13 bài) và cấu hình hệ thống (`backend/tests/unit/test_config.py`: 5 bài).
- **Kiểm thử kịch bản và độ nhạy (`backend/tests/scenarios/`):** Gồm 27 bài kiểm thử, bao gồm 17 bài kiểm thử hồi quy 14 kịch bản thực nghiệm KB01–KB14 (`backend/tests/scenarios/test_scenarios.py`) và 10 bài kiểm thử thực nghiệm chuyên sâu khảo sát độ nhạy tham số T1–T10 (`backend/tests/scenarios/test_sensitivity_muc_5_2.py`).
- **Kiểm thử tích hợp API và ca biên (`backend/tests/api/`):** Gồm 41 bài kiểm thử, bao gồm 35 bài kiểm thử hợp đồng giao tiếp HTTP API qua `TestClient` (`backend/tests/api/test_recommend_api.py`) và 6 bài kiểm thử tích hợp chuyên sâu cho các ca biên toán học, tính đơn điệu và luồng tương tác điều chỉnh ưu tiên CN03 (`backend/tests/api/test_boundary_muc_5_1.py`).

Kết quả thực thi toàn bộ bộ kiểm thử tự động ghi nhận tỷ lệ đạt 100% (**200/200 bài kiểm thử đạt, 0 lỗi, 0 bỏ qua** với thời gian chạy 1,18 giây). Độ bao phủ mã nguồn đo đạc lại bằng công cụ `pytest-cov` đạt **97%** trên toàn bộ khối mã nguồn nghiệp vụ `backend/app/` (351/362 dòng lệnh thực thi, 11 dòng rẽ nhánh chưa chạm), trong đó toàn bộ các module cốt lõi (`backend/app/api/recommend.py`, `backend/app/main.py`, `backend/app/core/config.py`, `backend/app/data/repository.py`, `backend/app/scoring/criteria.py`, `backend/app/scoring/filters.py`, `backend/app/scoring/weights.py` và các mô hình dữ liệu Pydantic schemas) đều đạt độ bao phủ tuyệt đối 100%.

| Nhóm kiểm thử | Thư mục mã nguồn | Số lượng kiểm thử | Kết quả thực thi | Độ bao phủ mã nguồn (`backend/app/`) |
|:---|:---|:---:|:---:|:---:|
| Kiểm thử đơn vị (Unit Tests) | `backend/tests/unit/`, `backend/tests/test_environment.py` | 132 | 132/132 đạt | 97% |
| Kiểm thử kịch bản & độ nhạy | `backend/tests/scenarios/` | 27 | 27/27 đạt | (tích hợp) |
| Kiểm thử API & ca biên tích hợp | `backend/tests/api/` | 41 | 41/41 đạt | 100% tầng API & Schemas |
| **Tổng cộng toàn hệ thống** | **`backend/tests/`** | **200** | **200/200 đạt (100%)** | **97% (351/362 dòng lệnh)** |

*Nguồn: Kết quả chạy lại lệnh `pytest -q` và `pytest --cov=app` tại thư mục `backend/`.*

### 5.1.2. Kiểm thử hợp đồng API và hiệu năng xử lý nội tại

Giao thức giao tiếp giữa giao diện người dùng (React) và máy chủ tính toán (FastAPI) được kiểm định theo hợp đồng API tại `docs/design/api-contract.md`. Endpoint chính `POST /api/recommend` được kiểm thử với `fastapi.testclient.TestClient`:

1. **Cấu trúc phản hồi chuẩn hóa:** Dữ liệu trả về ở định dạng JSON với cấu trúc phân cấp gồm các trường: `status` (trạng thái xử lý), `total_candidates` (tổng số hồ sơ nạp vào), `qualified_candidates` (số ứng viên vượt qua lọc bắt buộc), `insufficient_data_candidates` (danh sách ứng viên bị loại do thiếu dữ liệu), và mảng kết quả `results[]`. Mỗi phần tử trong `results[]` chứa đầy đủ: `rank` (thứ hạng), `tutor_id` (mã gia sư), `total_score` (điểm tổng hợp), `criteria_scores` (điểm thành phần 5 tiêu chí), `contributions` (mức đóng góp thành phần $C_i$), `reason` (chuỗi lý do ngắn gọn), và `notes` (ghi chú cảnh báo).
2. **Quy tắc sắp xếp và phá hòa tất định:** Danh sách kết quả luôn được sắp xếp theo thứ tự giảm dần của `total_score`. Trong trường hợp hai hoặc nhiều ứng viên có cùng điểm số chính xác, hệ thống áp dụng quy tắc phá hòa tất định theo thứ tự từ điển của mã gia sư `tutor_id` tăng dần, bảo đảm thứ hạng luôn ổn định và tái lập được qua mọi lần gọi.
3. **Bao phủ các trạng thái nghiệp vụ:** Bộ kiểm thử API bao phủ đầy đủ 4 trường hợp trạng thái của hệ thống:
   - `success` (HTTP 200): Gợi ý thành công danh sách gia sư phù hợp kèm điểm số phân rã chi tiết.
   - `no_match` (HTTP 200): Xảy ra khi không có ứng viên nào vượt qua bước lọc bắt buộc (như môn học không tồn tại trong cơ sở dữ liệu ở KB05). Hệ thống trả về `results = []` kèm hướng dẫn người học nới lỏng tiêu chí.
   - `zero_weight` (HTTP 200): Xảy ra khi người học chủ động đặt toàn bộ 5 mức ưu tiên về `none` ($\sum w_i = 0$). Hệ thống không thể chuẩn hóa trọng số để xếp hạng, do đó trả về trạng thái cảnh báo thân thiện kèm danh sách `unranked_candidates` gồm các gia sư thỏa mãn điều kiện bắt buộc để người học tự tham khảo.
   - `422 Unprocessable Entity`: Xảy ra khi yêu cầu gửi lên vi phạm ràng buộc dữ liệu (như thiếu trường `subject`, sai định dạng `learning_mode`, hoặc ngân sách âm), được tầng Pydantic v2 chặn lại và trả thông báo lỗi chi tiết.
4. **Hiệu năng xử lý nội tại:** Đo đạc thực nghiệm trên 14 kịch bản KB01–KB14 qua 140 lượt gọi API liên tục (10 lượt/kịch bản) bằng `TestClient` ghi nhận thời gian phản hồi trung bình đạt **3,54 ms** (lớn nhất **7,97 ms** sau lượt khởi động đầu tiên; đo mẫu mở rộng 700 lượt đạt trung bình 3,72 ms và lớn nhất 26,64 ms). Tốc độ xử lý này đáp ứng yêu cầu phi chức năng về tính tương tác tức thời (< 1.000 ms) khi người học thực hiện điều chỉnh ưu tiên trực tiếp trên giao diện (CN03).

> [!NOTE]
> Chỉ số thời gian phản hồi trên được đo đạc trong bộ nhớ cục bộ bằng `TestClient` (không có độ trễ truyền gói tin mạng). Thời gian này phản ánh tốc độ tính toán thuật toán và xử lý của framework FastAPI, hoàn toàn không đại diện cho độ trễ truyền thông toàn trình (end-to-end) qua mạng Internet giữa trình duyệt máy khách và máy chủ đám mây.

### 5.1.3. Kiểm thử ca biên của hàm điểm và tính đơn điệu

Nhằm kiểm chứng tính đúng đắn toán học của 5 hàm chuẩn hóa điểm thành phần tại Bảng 3.6 và tính ổn định khi tương tác trực tiếp (CN03), các ca kiểm thử biên chuyên sâu đã được xây dựng tại `backend/tests/api/test_boundary_muc_5_1.py` và `backend/tests/unit/test_criteria.py`. Kết quả thực nghiệm được tổng hợp trong Bảng 5.8:

**Bảng 5.8 - Kết quả kiểm thử ca biên của các hàm điểm và tính đơn điệu**

| Nhóm kiểm thử | Ca biên / Tình huống kiểm thử | Đầu vào thực nghiệm | Kết quả kỳ vọng (Bảng 3.6 & Mục 5.1) | Kết quả thực tế hệ thống | Trạng thái |
|:---|:---|:---|:---|:---|:---:|
| **1. Học phí ($s_{\text{fee}}$, $\delta = 0{,}5$)** | Học phí bằng đúng ngân sách ($P = B$) | $B = 200\,000$, $P = 200\,000$ | $s_{\text{fee}} = 1{,}000$; lý do `"học phí trong ngân sách"` | `s_fee = 1.0`, chuỗi lý do chứa `"học phí trong ngân sách"` | Đạt |
| | Học phí nằm giữa vùng dung sai ($P = 1{,}25 B$) | $B = 200\,000$, $P = 250\,000$ | $s_{\text{fee}} = 0{,}500$; lý do `"học phí vượt ngân sách 25%"` | `s_fee = 0.5`, chuỗi lý do chứa `"học phí vượt ngân sách 25%"` | Đạt |
| | Học phí chạm biên trên dung sai 50% ($P = 1{,}50 B$) | $B = 200\,000$, $P = 300\,000$ | $s_{\text{fee}} = 0{,}000$; lý do `"học phí vượt ngân sách 50%"` | `s_fee = 0.0`, chuỗi lý do chứa `"học phí vượt ngân sách 50%"` | Đạt |
| | Học phí vượt quá 50% ngân sách ($P > 1{,}50 B$) | $B = 200\,000$, $P = 400\,000$ (`GS-T06` tại KB01) | $s_{\text{fee}} = 0{,}000$; không bị loại cứng, lý do `"học phí vượt ngân sách 100%"` | `s_fee = 0.0`, xếp hạng 3 tại KB01, `notes = ["chưa có đánh giá"]` | Đạt |
| | Ngân sách bằng 0 ($B = 0$) | $B = 0$, $P > 0$ | $s_{\text{fee}} = 0{,}000$; không phát sinh ngoại lệ chia cho 0 | `HTTP 200 OK`, mọi ứng viên nhận `s_fee = 0.0` | Đạt |
| **2. Kinh nghiệm ($s_{\text{experience}}$, $E_{\max} = 8$)** | Kinh nghiệm bằng 0 năm ($E = 0$) | $E = 0$ | $s_{\text{experience}} = 0{,}000$ | `s_experience = 0.0` | Đạt |
| | Kinh nghiệm chạm mốc bão hòa ($E = 8$) | $E = 8$ (`GS-G06` tại KB11) | $s_{\text{experience}} = 1{,}000$ | `s_experience = 1.0` | Đạt |
| | Kinh nghiệm vượt mốc bão hòa ($E > 8$) | $E = 12$ (`GS-G10`), $E = 20$ (`GS-T06`) | $s_{\text{experience}} = 1{,}000$ (chặn trên bão hòa tại $1{,}0$) | `s_experience = 1.0` | Đạt |
| **3. Điểm đánh giá ($s_{\text{rating}}$)** | Gia sư chưa có đánh giá (`avg_rating = null`) | `GS-T06`, `GS-T07` (`public_collected`) | $s_{\text{rating}} = 0{,}500$ (trung tính); ghi chú `"chưa có đánh giá"`; không bị loại dữ liệu | `s_rating = 0.5`, `notes` chứa `"chưa có đánh giá"` | Đạt |
| | Điểm đánh giá tuyệt đối (`avg_rating = 5.0`) | `GS-G01` (`avg_rating = 5.0`) | $s_{\text{rating}} = 1{,}000$ | `s_rating = 1.0` | Đạt |
| **4. Lịch rảnh ($s_{\text{availability}}$)** | Khớp một phần khung giờ ($m/k$ với $1 \le m < k$) | Yêu cầu `["T2-tối", "T4-tối", "T6-tối"]` ($k=3$); `GS-G01` khớp 2 khung giờ | Vượt qua lọc bắt buộc; $s_{\text{availability}} = 2/3 \approx 0{,}667$ | `s_availability = 0.6667` | Đạt |
| | Khớp toàn bộ khung giờ ($k/k$) | Yêu cầu `["T2-tối", "T4-tối", "T6-tối"]` ($k=3$); `GS-T06` khớp cả 3 | $s_{\text{availability}} = 3/3 = 1{,}000$ | `s_availability = 1.0` | Đạt |
| | Không giao khung giờ nào ($0/k$) | Khung giờ yêu cầu không giao với lịch rảnh của gia sư | Bị loại ngay ở bước lọc điều kiện bắt buộc | Không xuất hiện trong danh sách `results` | Đạt |
| **5. Tính đơn điệu & Tương tác CN03** | Tính đơn điệu theo ngân sách tối đa $B$ | Tăng $B$: `150.000` $\rightarrow$ `200.000` $\rightarrow$ `350.000` VNĐ | Điểm tổng $S(g)$ của mọi ứng viên không giảm: $S_{150k} \le S_{200k} \le S_{350k}$ | Thỏa mãn 100% trên toàn bộ ứng viên | Đạt |
| | Đổi mức ưu tiên trực tiếp trên kết quả (CN03) | Từ KB01 mặc định $\rightarrow$ đặt `fee = none`, `rating = none`, `experience = high` | `GS-T06` (20 năm kinh nghiệm) vươn lên hạng 1 ($S = 1{,}000$); thời gian phản hồi $< 1$ giây | `GS-T06` lên hạng 1 (`S = 1.0`), thời gian xử lý qua TestClient đạt $\approx 3{,}5$ ms | Đạt |
| | Đặt toàn bộ 5 mức ưu tiên về `none` ($\sum w_i = 0$) | `priorities = {fee: none, district: none, experience: none, rating: none, availability: none}` | Trả về `status = "zero_weight"` kèm danh sách `unranked_candidates` | `status = "zero_weight"`, trả đủ 5 ứng viên trong `unranked_candidates` | Đạt |

*Nguồn: Tóm tắt kết quả kiểm thử tự động từ `backend/tests/api/test_boundary_muc_5_1.py` và `backend/tests/unit/test_criteria.py` (tham chiếu tài liệu làm việc `docs/thesis/report/muc-5.1-bang-5.1-ket-qua.md`). Bảng này được đánh số Bảng 5.8 để bảo toàn thứ tự đánh số Bảng 5.1–5.7 theo đề cương và theo Mục 5.2; danh mục bảng biểu sẽ được đồng bộ tại US-36.*

### 5.1.4. Xử lý các trường hợp đặc biệt

Hệ thống xử lý thống nhất các trường hợp nghiệp vụ đặc thù theo nguyên tắc minh bạch dữ liệu:

1. **Trường hợp không có gia sư thỏa mãn điều kiện bắt buộc:** Khi bộ lọc bắt buộc loại bỏ toàn bộ hồ sơ trong cơ sở dữ liệu (ví dụ kịch bản KB05 với môn Tiếng Trung không có gia sư nào nhận dạy), hệ thống phản hồi trạng thái `status = "no_match"`, danh sách `results = []` và `insufficient_data_candidates = []`. Giao diện hiển thị thông báo rõ ràng giúp người học biết môn học chưa có người dạy và gợi ý thay đổi tiêu chí tìm kiếm.
2. **Trường hợp học trực tuyến (`learning_mode = "online"`):** Khi người học chọn hình thức học từ xa, yếu tố khoảng cách địa lý không còn ý nghĩa. Hệ thống tự động vô hiệu hóa tiêu chí khu vực: khóa trường nhập quận/huyện trên giao diện, tự động loại bỏ tiêu chí `district` khỏi danh sách tính điểm ($w_{\text{district}}$ không tham gia vào tổng trọng số), đồng thời trả về `criteria_scores["district"] = null` và `contributions["district"] = null` trong kết quả API (minh chứng tại KB04, KB08, KB14).
3. **Trường hợp tổng trọng số bằng 0 ($\sum w_i = 0$):** Khi người học bỏ chọn quan tâm đối với toàn bộ các tiêu chí, công thức tính điểm trung bình có trọng số bị triệt tiêu mẫu số. Thay vì phát sinh lỗi chia cho 0 hoặc tự ý gán trọng số ngầm định, hệ thống chuyển sang trạng thái nghiệp vụ `zero_weight`. Toàn bộ các gia sư vượt qua bước lọc bắt buộc được trả về trong trường `unranked_candidates` ở dạng danh sách chưa xếp hạng để người học tự lựa chọn, đồng thời giao diện hiển thị hướng dẫn người học thiết lập ít nhất một mức ưu tiên để kích hoạt lại tính năng gợi ý.
4. **Trường hợp người học không nhập ngân sách, khu vực hoặc khung giờ:** Hệ thống cho phép người học để trống các trường tìm kiếm tùy chọn. Khi một trường thông tin bị bỏ trống, tiêu chí tương ứng được hệ thống xem là không áp dụng:
   - Nếu không nhập ngân sách tối đa (`max_budget_vnd = null`, như tại KB10, KB14): Tiêu chí học phí bị vô hiệu hóa, `criteria_scores["fee"] = null`, `contributions["fee"] = null`, điểm số không bị phạt vượt ngân sách.
   - Nếu không chọn quận/huyện mong muốn khi học trực tiếp hoặc khi chọn hình thức bất kỳ (`learning_mode = "any"`, như tại KB13): Tiêu chí khu vực bị vô hiệu hóa.
   - Nếu không chọn khung giờ học rảnh (`time_slots = []`, xuất hiện ở 11/14 kịch bản): Tiêu chí lịch rảnh bị vô hiệu hóa, `criteria_scores["availability"] = null`, `contributions["availability"] = null`.
   Trong mọi trường hợp tiêu chí bị vô hiệu hóa, tổng trọng số mẫu số chỉ tính trên tập các tiêu chí thực sự áp dụng $A$ ($\sum_{j \in A} w_j$), bảo đảm tính nhất quán cho các ứng viên.

---

## 5.2. Đánh giá chất lượng xếp hạng

### 5.2.1. So khớp Top-3 hệ thống với kỳ vọng trên 14 kịch bản

Bảng 5.1 trình bày kết quả thực nghiệm chi tiết của 14 kịch bản đánh giá KB01–KB14, đối chiếu giữa danh sách Top-3 kỳ vọng (được nhóm xây dựng và khóa bất biến trong `backend/tests/scenarios/scenarios.json`) với kết quả Top-3 do hệ thống tính toán thực tế qua pipeline `score_and_rank` trên tập dữ liệu 16 hồ sơ gia sư.

Quy ước chấm khớp tuân thủ hướng dẫn tại `backend/tests/scenarios/README.md` mục 3:
- Khi Top-3 kỳ vọng có $m$ gia sư ($1 \le m \le 3$), số trùng được ghi nhận dưới dạng $x/m$.
- Kịch bản KB05 kiểm tra trường hợp không có ứng viên thỏa điều kiện bắt buộc (`no_match`), kết quả trả về danh sách rỗng được tính là khớp quy ước 0/0.
- Các gia sư đồng hạng trong kỳ vọng (KB02, KB12) được xem là hoán đổi được; hệ thống giải quyết đồng điểm bằng quy tắc phá hòa tất định theo mã hồ sơ `tutor_id` tăng dần.

**Bảng 5.1 - Kết quả thực nghiệm 14 kịch bản đánh giá**

| Mã KB | Mô tả nhu cầu | Top-3 kỳ vọng (Đề cương Bảng 5.1 / `scenarios.json`) | Top-3 hệ thống (Chạy thực tế qua pipeline) | Số trùng (x/m) | Nhận xét thực nghiệm |
|:---:|:---|:---|:---|:---:|:---|
| **KB01** | Toán, trực tiếp, Bình Thạnh, ngân sách 200.000đ, mọi ưu tiên Trung bình | 1. GS-G01 (0,938)<br/>2. GS-G10 (0,745)<br/>3. GS-T06 (0,625) | 1. GS-G01 (0,938)<br/>2. GS-G10 (0,745)<br/>3. GS-T06 (0,625) | 3/3 | Trùng khớp tuyệt đối cả thứ tự và điểm số; GS-T06 vượt ngân sách 100% ($s_{\text{fee}}=0$) nên xếp hạng 3; nhận điểm đánh giá trung tính 0,5. |
| **KB02** | Anh Văn, trực tiếp, Quận 2, ngân sách 220.000đ, mọi ưu tiên Trung bình | 1–2. GS-G11 = GS-G12 (0,881, đồng hạng)<br/>3. GS-T07 (0,5625) | 1. GS-G11 (0,881)<br/>2. GS-G12 (0,881)<br/>3. GS-T07 (0,5625) | 3/3 | Trùng khớp hoàn toàn; GS-G11 và GS-G12 đồng điểm tuyệt đối (0,88125), hệ thống phá hòa tất định đưa GS-G11 xếp trước GS-G12. |
| **KB03** | Anh Văn, trực tiếp, Thủ Đức, ngân sách 220.000đ, mọi ưu tiên Trung bình | 1. GS-G12 (0,881)<br/>2. GS-G11 (0,631)<br/>3. GS-T07 (0,5625) | 1. GS-G12 (0,881)<br/>2. GS-G11 (0,631)<br/>3. GS-T07 (0,5625) | 3/3 | Trùng khớp tuyệt đối cả thứ tự và điểm số; GS-G12 khớp khu vực Thủ Đức nên tách biệt rõ ràng lên vị trí dẫn đầu. |
| **KB04** | Lý, trực tuyến, ngân sách 200.000đ, lịch T2-tối & T4-tối, mọi ưu tiên Trung bình | 1. GS006 (0,848)<br/>2. GS020 (0,715) | 1. GS006 (0,886)<br/>2. GS020 (0,786) | 2/2 | Trùng khớp 100% về thứ tự xếp hạng (GS006 > GS020); điểm hệ thống (0,886 và 0,786) khác điểm tính tay (0,848 và 0,715) do tính tay bỏ sót tiêu chí lịch rảnh. |
| **KB05** | Tiếng Trung, hình thức bất kỳ (`any`), mọi ưu tiên Trung bình | (không có ứng viên)<br/>`[]` | (không có ứng viên)<br/>`[]` (`status = "no_match"`) | 0/0 | Trùng khớp kỳ vọng; hệ thống kích hoạt trạng thái `no_match` khi không có ứng viên nào dạy môn Tiếng Trung. |
| **KB06** | Văn, trực tiếp, Quận 1, ngân sách 180.000đ, mọi ưu tiên Trung bình | 1. GS-G04 (0,934) | 1. GS-G04 (0,934) | 1/1 | Trùng khớp tuyệt đối thứ hạng và điểm số (điểm chính xác: 0,93375 $\approx$ 0,934). |
| **KB07** | Sinh, hình thức bất kỳ (`any`), Thủ Đức, ngân sách 200.000đ, mọi ưu tiên Trung bình | 1. GS-G05 (0,825) | 1. GS-G05 (0,825) | 1/1 | Trùng khớp tuyệt đối thứ hạng và điểm số (0,8250). |
| **KB08** | Tin học, trực tuyến, ngân sách 250.000đ, lịch T2-tối & T6-tối, mọi ưu tiên Trung bình | 1. GS-G07 (0,876) | 1. GS-G07 (0,876) | 1/1 | Trùng khớp tuyệt đối thứ hạng và điểm số (điểm chính xác: 0,87625 $\approx$ 0,876). |
| **KB09** | Tiếng Nhật, hình thức bất kỳ (`any`), Phú Nhuận, ngân sách 280.000đ, mọi ưu tiên Trung bình | 1. GS-G08 (0,928) | 1. GS-G08 (0,9275) | 1/1 | Trùng khớp thứ tự 1/1; điểm chính xác là 0,9275 (đề cương làm tròn lên 0,928; hiển thị số thực nhị phân làm tròn thành 0,927). |
| **KB10** | Toán, trực tiếp, Quận 7, không nhập ngân sách, ưu tiên Kinh nghiệm Cao | 1. GS-G10 (0,994)<br/>2. GS-G01 (0,607)<br/>3. GS-G09 (0,593) | 1. GS-G10 (0,994)<br/>2. GS-G01 (0,607)<br/>3. GS-G09 (0,593) | 3/3 | Trùng khớp tuyệt đối cả thứ tự và điểm số; GS-T06 (0,571) đứng hạng 4 ngoài Top-3 đúng phân tích lý thuyết. |
| **KB11** | Hóa, trực tiếp, Quận 10, ngân sách 220.000đ, mọi ưu tiên Trung bình | 1. GS-G06 (0,985)<br/>2. GS-T06 (0,375) | 1. GS-G06 (0,985)<br/>2. GS-T06 (0,375) | 2/2 | Trùng khớp tuyệt đối cả thứ tự và điểm số; GS-T06 có $s_{\text{fee}}=0$ do học phí vượt trần dung sai. |
| **KB12** | Anh Văn, trực tiếp, Bình Chánh, ngân sách 200.000đ, mọi ưu tiên Trung bình | 1. GS-T07 (0,8125)<br/>2–3. GS-G11 = GS-G12 (0,631, đồng hạng) | 1. GS-T07 (0,8125)<br/>2. GS-G11 (0,631)<br/>3. GS-G12 (0,631) | 3/3 | Trùng khớp hoàn toàn; GS-T07 đứng đầu nhờ khớp khu vực; GS-G11 và GS-G12 đồng điểm hạng 2–3 (0,63125), phá hòa theo mã gia sư. |
| **KB13** | Toán, hình thức bất kỳ (`any`), ngân sách 150.000đ, không nhập khu vực & lịch, mọi ưu tiên Trung bình | 1. GS-G10 (0,993)<br/>2. GS-G01 (0,783)<br/>3. GS-T06 (0,50) | 1. GS-G10 (0,993)<br/>2. GS-G01 (0,783)<br/>3. GS-T06 (0,500) | 3/3 | Trùng khớp tuyệt đối cả thứ tự và điểm số trên 3 tiêu chí áp dụng (học phí, kinh nghiệm, đánh giá). |
| **KB14** | Anh Văn, trực tuyến, không nhập ngân sách, khu vực và lịch, mọi ưu tiên Trung bình | 1. GS-G03 (0,70) | 1. GS-G03 (0,700) | 1/1 | Trùng khớp tuyệt đối thứ hạng và điểm số sau khi chuẩn hóa nhãn môn học của GS-G03 thành "Anh Văn". |

*Nguồn: Kết quả chạy lại pipeline xếp hạng trên dữ liệu `data/processed/tutors.json` và `backend/tests/scenarios/scenarios.json` (tham chiếu tài liệu làm việc `docs/thesis/report/muc-5.1-bang-5.1-ket-qua.md` và `docs/thesis/report/discrepancy_analysis.md`).*

Nhằm phục vụ đối chiếu trực quan về tỷ lệ trùng khớp của tập hợp và thứ tự Top-3, Bảng 5.2 trích dẫn bản rút gọn đối sánh thứ tự ứng viên theo cấu trúc của Mục 5.2:

**Bảng 5.2 - Đối chiếu Top-3 hệ thống với Top-3 kỳ vọng trên 14 kịch bản**

| Mã KB | Top-3 kỳ vọng | Top-3 hệ thống | Số trùng x/m |
|:---:|:---|:---|:---:|
| KB01 | `GS-G01 > GS-G10 > GS-T06` | `GS-G01 > GS-G10 > GS-T06` | 3/3 |
| KB02 | `GS-G11 > GS-G12 > GS-T07` | `GS-G11 > GS-G12 > GS-T07` | 3/3 |
| KB03 | `GS-G12 > GS-G11 > GS-T07` | `GS-G12 > GS-G11 > GS-T07` | 3/3 |
| KB04 | `GS006 > GS020` | `GS006 > GS020` | 2/2 |
| KB05 | `[]` (`no_match`) | `[]` (`no_match`) | 0/0 |
| KB06 | `GS-G04` | `GS-G04` | 1/1 |
| KB07 | `GS-G05` | `GS-G05` | 1/1 |
| KB08 | `GS-G07` | `GS-G07` | 1/1 |
| KB09 | `GS-G08` | `GS-G08` | 1/1 |
| KB10 | `GS-G10 > GS-G01 > GS-G09` | `GS-G10 > GS-G01 > GS-G09` | 3/3 |
| KB11 | `GS-G06 > GS-T06` | `GS-G06 > GS-T06` | 2/2 |
| KB12 | `GS-T07 > GS-G11 > GS-G12` | `GS-T07 > GS-G11 > GS-G12` | 3/3 |
| KB13 | `GS-G10 > GS-G01 > GS-T06` | `GS-G10 > GS-G01 > GS-T06` | 3/3 |
| KB14 | `GS-G03` | `GS-G03` | 1/1 |

*Nguồn: `docs/thesis/report/muc-5.2-ket-qua-tho.json`, khối `baseline`; quy ước chấm khớp tại `backend/tests/scenarios/README.md` mục 3.*

**Tổng kết và phân tích ba trường hợp kỹ thuật đặc thù:**
Tổng thể thực nghiệm đạt tỷ lệ trùng khớp Top-3 kỳ vọng **14/14 kịch bản (100%)**, không ghi nhận hiện tượng đảo lộn thứ tự hoặc xuất hiện ứng viên sai lệch. Qua quá trình đối chiếu độc lập giữa kết quả chạy máy và số liệu đề cương, ba trường hợp kỹ thuật được phân tích và làm rõ như sau:

1. **Kịch bản KB04 (Lệch giá trị điểm do công thức tính tay):**
   - Truy vấn KB04 là học trực tuyến (`online`), có ngân sách 200.000đ và yêu cầu khung giờ `["T2-tối", "T4-tối"]`. Theo Mục 6.1 của đặc tả tính điểm `docs/design/scoring-spec.md`, khi học trực tuyến chỉ duy nhất tiêu chí khu vực bị lược bỏ; tiêu chí lịch rảnh vẫn áp dụng đầy đủ. Vì vậy có 4 tiêu chí áp dụng với tổng trọng số $\sum w_i = 2 + 2 + 2 + 2 = 8$. Cả hai ứng viên GS006 và GS020 đều thỏa mãn toàn bộ khung giờ ($s_{\text{availability}} = 1,0$).
   - Điểm thực tế hệ thống tính:
     $$S(\text{GS006}) = \frac{2 \times 1{,}0 + 2 \times 0{,}625 + 2 \times 0{,}92 + 2 \times 1{,}0}{8} = \frac{7{,}09}{8} = 0{,}88625 \approx 0{,}886$$
     $$S(\text{GS020}) = \frac{2 \times 0{,}6 + 2 \times 0{,}625 + 2 \times 0{,}92 + 2 \times 1{,}0}{8} = \frac{6{,}29}{8} = 0{,}78625 \approx 0{,}786$$
   - Điểm tính tay trong đề cương (0,848 và 0,715) phát sinh do người tính thủ công chỉ cộng 3 tiêu chí (học phí, kinh nghiệm, đánh giá với tổng trọng số bằng 6), bỏ sót tiêu chí lịch rảnh. Vì $s_{\text{availability}} = 1,0$ ở cả hai ứng viên, việc cộng thêm tiêu chí lịch rảnh chỉ tịnh tiến đồng thời điểm của cả hai về phía 1,0 mà bảo toàn nguyên vẹn thứ tự xếp hạng (`GS006 > GS020`).
2. **Kịch bản KB09 (Chênh lệch biểu diễn làm tròn số thực):**
   - Ứng viên GS-G08 có điểm thành phần: $s_{\text{fee}} = 1,0$; $s_{\text{district}} = 1,0$; $s_{\text{experience}} = 6/8 = 0,75$; $s_{\text{rating}} = 4,8/5 = 0,96$. Điểm tổng hợp chính xác là $(1,0 + 1,0 + 0,75 + 0,96)/4 = 3,71/4 = 0,9275$.
   - Khi tính tay theo quy tắc làm tròn nửa lên (*round half up*), số 0,9275 được làm tròn thành 0,928. Trong chuẩn số thực dấu phẩy động IEEE-754 và hàm làm tròn của Python (*round half to even*), số 0,9275 có biểu diễn nhị phân xấp xỉ `0.927499999999999991118...` nên được làm tròn thành 0,927. Hệ thống lưu giữ giá trị thực 0,9275 không làm tròn trung gian; thứ tự xếp hạng 1/1 hoàn toàn không bị ảnh hưởng.
3. **Kịch bản KB02 và KB12 (Xác nhận cơ chế phá hòa tất định):**
   - Tại KB02, hai ứng viên GS-G11 và GS-G12 có cùng mọi chỉ số dữ liệu dẫn đến điểm tổng hợp bằng nhau tuyệt đối ($7,05/8 = 0,88125$). Bộ xếp hạng `score_and_rank` sắp xếp theo khóa `(-total_score, tutor_id)`, đưa `"GS-G11"` lên vị trí 1 và `"GS-G12"` xuống vị trí 2 một cách tất định.
   - Tại KB12, hai ứng viên này tiếp tục đồng điểm tại vị trí hạng 2 và hạng 3 ($5,05/8 = 0,63125$), và cơ chế phá hòa theo mã hồ sơ tiếp tục giữ vững trật tự từ điển `"GS-G11"` trước `"GS-G12"`.

*(Chi tiết phân tích toán học đầy đủ được lưu trữ tại tài liệu làm việc `docs/thesis/report/discrepancy_analysis.md`).*

### 5.2.2. Thứ hạng bất hợp lý và quyết định điều chỉnh

Trong toàn bộ quá trình đối chiếu 14 kịch bản thực nghiệm nền tảng (baseline), không ghi nhận bất kỳ kết quả thứ hạng nào bất hợp lý: các kịch bản có 1 ứng viên đều trả về đúng ứng viên đó; các kịch bản có ứng viên đồng điểm được phá hòa ổn định; các khác biệt tại KB04 và KB09 chỉ mang tính chất hiển thị số học mà không làm thay đổi bản chất thứ hạng.

Do đó, nhóm nghiên cứu thống nhất: **Không tự ý điều chỉnh hàm điểm, không thay đổi các tham số $\delta$, $E_{\max}$ hay trọng số, và không sửa đổi dữ liệu kỳ vọng `expected_top3` hoặc `expected_raw` trong `scenarios.json`**. Mọi hiện tượng số học đều được giải thích tường minh bằng công thức toán học và quy tắc biểu diễn máy tính.

*(Chi tiết xem tài liệu làm việc `docs/thesis/report/muc-5.2-danh-gia-do-on-dinh.md` mục 5.2.2).*

### 5.2.3. Khảo sát tính ổn định và độ nhạy tham số

Tính ổn định của thuật toán được đánh giá qua việc khảo sát độ nhạy khi thay đổi lần lượt các tham số nền tảng: biên dung sai học phí $\delta$, mốc bão hòa kinh nghiệm $E_{\max}$, và mức ngân sách của người học. Baseline sử dụng $\delta = 0,50$; $E_{\max} = 8$ năm; trọng số theo Bảng 3.5 và ngân sách gốc.

**Bảng 5.3 - Độ nhạy của Top-3 theo tham số dung sai học phí $\delta$**

| $\delta$ | Số KB đổi Top-3 | KB đổi | Số KB trùng Top-3 baseline (x/m) |
|:---:|:---:|:---:|:---:|
| 0,25 | 0 | — | 14/14 |
| 0,30 | 0 | — | 14/14 |
| 0,50 (baseline) | 0 | — | 14/14 |
| 0,70 | 0 | — | 14/14 |
| 0,75 | 0 | — | 14/14 |
| 1,00 | 0 | — | 14/14 |

*Nguồn: `docs/thesis/report/muc-5.2-ket-qua-tho.json`, khối `delta`.*

Kết quả ghi nhận **0/14 kịch bản thay đổi Top-3** trên cả 6 mức $\delta$ khảo sát. Điều này phù hợp với công thức hàm điểm học phí: khi $P \le B$, $s_{\text{fee}} = 1$; khi $P > B$, mẫu số $\delta B$ tăng làm giảm mức phạt, do đó $s_{\text{fee}}$ không giảm khi $\delta$ tăng. Tuy nhiên, việc thứ tự giữ nguyên trên tập 16 hồ sơ là quan sát thực nghiệm cụ thể, không đại diện cho tính bất biến trên mọi tập dữ liệu bất kỳ.

**Bảng 5.4 - Độ nhạy của Top-3 theo mốc kinh nghiệm bão hòa $E_{\max}$**

| $E_{\max}$ | Số KB đổi Top-3 | KB đổi | Top-3 của KB10 | Số KB trùng Top-3 baseline (x/m) |
|:---:|:---:|:---:|:---|:---:|
| 5 | 0 | — | `GS-G10 > GS-G01 > GS-G09` | 14/14 |
| 6 | 0 | — | `GS-G10 > GS-G01 > GS-G09` | 14/14 |
| 8 (baseline) | 0 | — | `GS-G10 > GS-G01 > GS-G09` | 14/14 |
| 10 | 1 | KB10 | `GS-G10 > GS-G09 > GS-T06` | 13/14 |
| 12 | 1 | KB10 | `GS-G10 > GS-T06 > GS-G09` | 13/14 |

*Nguồn: `docs/thesis/report/muc-5.2-ket-qua-tho.json`, khối `e_max`.*

Trong khảo sát $E_{\max}$, KB10 là kịch bản duy nhất có sự biến động thứ hạng Top-3 tại hai mốc $E_{\max} = 10$ và $E_{\max} = 12$. Bản chất toán học của hiện tượng này được làm rõ như sau:
- KB10 áp dụng 3 tiêu chí: Khu vực ($w=2$), Kinh nghiệm ($w=3$, mức Cao), và Đánh giá ($w=2$), tổng trọng số bằng 7 (không có ngân sách và lịch rảnh).
- **Tại $E_{\max} = 10$:** Điểm của GS-G09 là $(2 \times 1 + 3 \times 2/10 + 2 \times 0,7)/7 = 4/7$; điểm của GS-T06 là $(2 \times 0 + 3 \times 1 + 2 \times 0,5)/7 = 4/7$. Kiểm tra chạy lại pipeline thực tế và in giá trị đại diện nhị phân `repr(total_score)` xác nhận: cả hai ứng viên đều đạt chính xác cùng một số thực `0.5714285714285714` (độ lệch bằng `0.0`). Do đó, hai ứng viên này **hòa điểm tuyệt đối**, và việc GS-G09 xếp hạng 2 còn GS-T06 xếp hạng 3 hoàn toàn là kết quả của cơ chế phá hòa tất định theo mã gia sư `tutor_id` (`"GS-G09" < "GS-T06"`). Sự thay đổi Top-3 ở đây phản ánh quy tắc phá hòa khi xuất hiện đồng điểm, không phải do hàm điểm tính sai.
- **Tại $E_{\max} = 12$:** Điểm của GS-G09 giảm xuống $(2 \times 1 + 3 \times 2/12 + 2 \times 0,7)/7 = 3,9/7 \approx 0,55714$; trong khi GS-T06 (20 năm kinh nghiệm vẫn chạm trần bão hòa) giữ nguyên $4/7 \approx 0,57143$. Lúc này GS-T06 vượt điểm GS-G09 một cách thực chất, đưa Top-3 thành `GS-G10 > GS-T06 > GS-G09`.

**Bảng 5.5 - Độ nhạy của Top-3 theo mức biến động ngân sách**

| Mức ngân sách | Số KB áp dụng | Số KB đổi Top-3 | KB đổi | Số KB áp dụng trùng Top-3 baseline (x/m) |
|:---:|:---:|:---:|:---:|:---:|
| −20% | 11 | 0 | — | 11/11 |
| −10% | 11 | 0 | — | 11/11 |
| −5% | 11 | 0 | — | 11/11 |
| 0% (baseline) | 11 | 0 | — | 11/11 |
| +5% | 11 | 0 | — | 11/11 |
| +10% | 11 | 0 | — | 11/11 |
| +20% | 11 | 0 | — | 11/11 |

*Nguồn: `docs/thesis/report/muc-5.2-ket-qua-tho.json`, khối `budget` (KB05, KB10, KB14 không có ngân sách nên không áp dụng).*

Trên 11 kịch bản có thiết lập ngân sách, không có bất kỳ kịch bản nào thay đổi Top-3 qua chuỗi 7 mức ngân sách từ −20% đến +20%.

**Tính chất đơn điệu toán học:**
Các bài kiểm thử tự động T4, T6 và T7–T9 xác nhận các tính chất đơn điệu chặt chẽ của mô hình điểm:
- **T4:** Với mỗi ứng viên, điểm tổng hợp $S$ không bao giờ giảm khi $\delta$ tăng (trên các kịch bản có áp dụng tiêu chí học phí).
- **T6:** Với mỗi ứng viên, điểm tổng hợp $S$ không bao giờ tăng khi $E_{\max}$ tăng (trên các kịch bản có áp dụng tiêu chí kinh nghiệm).
- **T7–T9:** Khi ngân sách tăng, điểm tổng hợp $S$ không giảm; tập hợp ứng viên qua lọc và thứ tự xếp hạng được bảo toàn ổn định trên tập thử nghiệm.

Các tính chất đơn điệu này được bảo đảm bởi bản chất toán học của các hàm thành phần: $s_{\text{fee}}$ không giảm khi $B$ hoặc $\delta$ tăng; $s_{\text{experience}}$ không tăng khi $E_{\max}$ tăng. Cần lưu ý rằng tính đơn điệu của hàm điểm là định lý toán học, trong khi việc Top-3 không đổi là quan sát thực nghiệm trên tập 16 hồ sơ cụ thể.

*(Chi tiết xem tài liệu làm việc `docs/thesis/report/muc-5.2-danh-gia-do-on-dinh.md` mục 5.2.3).*

### 5.2.4. Ảnh hưởng của các bộ mức ưu tiên

Khảo sát được thực hiện trên 4 bộ mức ưu tiên chuẩn hóa của bài kiểm thử T10: Mặc định (`default`), Ưu tiên Khu vực (`prioritize_district`), Ưu tiên Học phí (`prioritize_fee`), và Ưu tiên Kinh nghiệm & Đánh giá (`prioritize_experience_rating`).

**Bảng 5.6 - Ảnh hưởng của bốn bộ mức ưu tiên đến Top-3**

| Bộ mức ưu tiên | Số KB đổi Top-3 | KB đổi Top-3 | Thay đổi Top-3 cụ thể |
|:---|:---:|:---:|:---|
| Mặc định (tất cả Trung bình) | 1 | KB10 | `GS-G10 > GS-G09 > GS-G01` thay cho `GS-G10 > GS-G01 > GS-G09`: đảo hạng 2–3, cùng tập hợp 3/3 |
| Ưu tiên Khu vực (district Cao, còn lại Thấp) | 2 | KB01, KB10 | KB01: `GS-G01 > GS-T06 > GS-G02` thay cho `GS-G01 > GS-G10 > GS-T06`; `GS-G10` rời Top-3 do không dạy Bình Thạnh, `GS-T06` lên hạng 2, `GS-G02` hạng 3 (trùng 2/3). KB10: `GS-G10 > GS-G09 > GS-G01` (đảo hạng 2–3, cùng tập 3/3) |
| Ưu tiên Học phí (fee Cao, còn lại Thấp) | 1 | KB10 | `GS-G10 > GS-G09 > GS-G01` thay cho `GS-G10 > GS-G01 > GS-G09` (đảo hạng 2–3, cùng tập 3/3); KB01 giữ nguyên |
| Ưu tiên KN & Đánh giá (experience & rating Cao, còn lại Thấp) | 1 | KB10 | `GS-G10 > GS-G01 > GS-T06` thay cho `GS-G10 > GS-G01 > GS-G09`: `GS-T06` vào Top-3 thay cho `GS-G09` (trùng 2/3) |

*Nguồn: `docs/thesis/report/muc-5.2-ket-qua-tho.json`, khối `priority_sets`.*

**Nhận xét:**
- Tại KB01 khi áp dụng bộ Ưu tiên Khu vực, gia sư GS-G10 không dạy tại quận Bình Thạnh ($s_{\text{district}} = 0$) nên bị đẩy khỏi Top-3; trong khi GS-T06 và GS-G02 đều khớp Bình Thạnh nên thăng hạng. Điều này chứng minh trọng số người dùng đã tác động chính xác đến kết quả gợi ý.
- Tại KB10, ở bộ Mặc định và Ưu tiên Học phí (do KB10 không có ngân sách nên tiêu chí học phí không tác dụng), trọng số kinh nghiệm bị hạ từ mức Cao ($w=3$) về mức Thấp hoặc Trung bình ngang hàng với khu vực, giúp GS-G09 (khớp khu vực) vượt qua GS-G01 (không khớp khu vực). Khi chuyển sang bộ Ưu tiên KN & Đánh giá, GS-T06 (20 năm kinh nghiệm) lập tức vươn vào Top-3 thay cho GS-G09 (chỉ 2 năm kinh nghiệm).
- Đáng chú ý, không có bất kỳ bộ mức ưu tiên nào làm thay đổi vị trí dẫn đầu (Hạng 1) tại KB01 (luôn là GS-G01) và KB10 (luôn là GS-G10).

*(Chi tiết xem tài liệu làm việc `docs/thesis/report/muc-5.2-danh-gia-do-on-dinh.md` mục 5.2.4).*

### 5.2.5. Khả năng giải thích của kết quả gợi ý

Khả năng giải thích là ưu điểm trọng tâm của phương pháp Weighted Scoring kết hợp phân rã điểm đóng góp. Phản hồi thực tế từ `POST /api/recommend` cho kịch bản KB01 minh chứng tính minh bạch này:

**Bảng 5.7 - Thành phần điểm và mức đóng góp của Top-3 gia sư tại KB01**

| Hạng | Gia sư | Điểm tổng $S$ | Điểm thành phần `criteria_scores`<br/>(fee; district; experience; rating; availability) | Mức đóng góp `contributions`<br/>(fee; district; experience; rating; availability) |
|:---:|:---|:---:|:---|:---|
| 1 | GS-G01 | 0,9375 | 1,0000; 1,0000; 0,7500; 1,0000; null | 0,2500; 0,2500; 0,1875; 0,2500; null |
| 2 | GS-G10 | 0,7450 | 1,0000; 0,0000; 1,0000; 0,9800; null | 0,2500; 0,0000; 0,2500; 0,2450; null |
| 3 | GS-T06 | 0,6250 | 0,0000; 1,0000; 1,0000; 0,5000; null | 0,0000; 0,2500; 0,2500; 0,1250; null |

*Nguồn: Phản hồi thực tế của `POST /api/recommend` cho kịch bản KB01 (HTTP 200), đối chiếu với `docs/thesis/report/muc-5.2-ket-qua-tho.json`.*

Chuỗi lý do (`reason`) và ghi chú dữ liệu (`notes`) kèm theo:
- **GS-G01:** Lý do: `"Học phí trong ngân sách, khu vực khớp, đánh giá 5,0/5"`; Ghi chú: `[]`.
- **GS-G10:** Lý do: `"Học phí trong ngân sách, kinh nghiệm 12 năm, đánh giá 4,9/5"`; Ghi chú: `[]`.
- **GS-T06:** Lý do: `"Khu vực khớp, kinh nghiệm 20 năm, đánh giá trung tính (0,5)"`; Ghi chú: `["chưa có đánh giá"]`.

Cấu trúc trên thể hiện rõ:
1. Điểm tổng hợp là tổng đại số chính xác của các mức đóng góp: $S = \sum C_i$.
2. Người học có thể nhìn thấy rõ tiêu chí nào mang lại ưu thế và tiêu chí nào bị trừ điểm (ví dụ GS-G10 nhận $C_{\text{district}} = 0,0$ do không cùng quận, hay GS-T06 nhận $C_{\text{fee}} = 0,0$ do học phí vượt quá trần dung sai).
3. Ghi chú `notes` cảnh báo trung thực tình trạng hồ sơ chưa có lịch sử đánh giá thực tế (`GS-T06`), giúp người học đưa ra quyết định có đầy đủ thông tin.

*(Chi tiết xem tài liệu làm việc `docs/thesis/report/muc-5.2-danh-gia-do-on-dinh.md` mục 5.2.5).*

---

## 5.3. Hạn chế của hệ thống

Trên tinh thần học thuật khách quan và trung thực, nhóm nghiên cứu ghi nhận các hạn chế hiện tại của hệ thống:

1. **Quy mô tập dữ liệu còn nhỏ và mang tính giả lập:** Hệ thống hiện chỉ được kiểm nghiệm trên tập dữ liệu mẫu gồm 16 hồ sơ gia sư tại `data/processed/tutors.json`. Trong đó, 14 hồ sơ là dữ liệu mô phỏng (`simulated`). Hai hồ sơ thu thập công khai (`GS-T06`, `GS-T07`) có học phí và lịch rảnh là các giá trị ước tính của nhóm dựa trên khảo sát thị trường chung; điểm đánh giá trung bình bị để trống và phải áp dụng giá trị trung tính 0,5. Ngoài ra, nhãn nguồn dữ liệu `data_source` của hai hồ sơ này trong cơ sở dữ liệu hiện vẫn ghi là `public_collected` theo đúng Phụ lục A của đề cương, chưa được chuẩn hóa thành nhãn `estimated` (vấn đề này đang chờ quyết định chính thức từ nhóm).
2. **Bộ kịch bản đánh giá do nhóm tự xây dựng:** Toàn bộ 14 kịch bản thực nghiệm và danh sách Top-3 kỳ vọng trong `backend/tests/scenarios/scenarios.json` được xây dựng bởi các thành viên nhóm dựa trên các ca kiểm thử dự kiến, chưa phải là tập dữ liệu đối chứng độc lập thu thập từ nhu cầu tìm kiếm của người học thực tế. Do đó, kết quả trùng khớp 14/14 kịch bản chỉ chứng minh thuật toán cài đặt chính xác, nhất quán và tuân thủ tuyệt đối các công thức toán học đã chốt trong thiết kế, chưa thể xem là bằng chứng thực nghiệm độc lập khẳng định chất lượng khuyến nghị trên thực tế.
3. **Các tham số thuật toán được ấn định thủ công:** Biên dung sai học phí $\delta = 0,5$, mốc kinh nghiệm bão hòa $E_{\max} = 8$, giá trị điểm trung tính 0,5 khi thiếu dữ liệu đánh giá, cũng như bảng chuyển đổi mức ưu tiên sang trọng số số học ($w \in \{0, 1, 2, 3\}$) đều được ấn định thủ công theo suy luận kinh nghiệm của nhóm, chưa được học hay tinh chỉnh từ dữ liệu hành vi người dùng quy mô lớn. Kết quả khảo sát độ nhạy ở Mục 5.2 phản ánh tính chất toán học trên tập tham số này và không thể khái quát hóa cho mọi trường hợp dữ liệu khác.
4. **Chưa có đánh giá thực nghiệm từ người dùng và phản hồi của GVHD:** Hệ thống chưa được triển khai thử nghiệm trên nhóm người học thực tế để đo lường các chỉ số mức độ hài lòng hoặc tỷ lệ chấp nhận gợi ý. Đồng thời, tại thời điểm soạn thảo báo cáo, nhóm chưa nhận được ý kiến nhận xét và đánh giá phản hồi chính thức từ giáo viên hướng dẫn (TS. Lê Anh Nhã Uyên).
5. **Mô hình không gian địa lý và tìm kiếm môn học còn đơn giản:** Tiêu chí vị trí địa lý hiện mới dừng lại ở việc so khớp đúng/sai dựa trên tên quận/huyện trong danh sách nhận dạy của gia sư, chưa tính toán được khoảng cách địa lý thực tế (theo kilômét) hay thời gian di chuyển giữa người dạy và người học. Ngoài ra, mỗi truy vấn tìm kiếm hiện chỉ hỗ trợ tìm kiếm cho một môn học đơn lẻ tại một thời điểm.
6. **Giới hạn về đo lường độ trễ mạng thực tế:** Chỉ số thời gian phản hồi API ghi nhận ở Mục 5.1 ($\approx 3,5$ ms) là thời gian xử lý nội tại trong bộ nhớ được đo bằng `TestClient` trên máy tính cục bộ. Độ trễ toàn trình (end-to-end) truyền qua mạng Internet từ trình duyệt người dùng đến hệ thống triển khai đám mây (gồm frontend trên Vercel và backend trên Render) hiện **chưa được đo đạc**. Đáng lưu ý, do backend sử dụng gói dịch vụ miễn phí (Free Tier) trên nền tảng Render, máy chủ sẽ tự động tạm dừng hoạt động nếu không có yêu cầu truy cập sau 15 phút. Theo tài liệu cẩm nang triển khai `docs/deployment/deploy-vercel-render.md`, yêu cầu đầu tiên để đánh thức máy chủ (hiện tượng "cold start") có thể mất khoảng 30–40 giây; đây là thông số kỹ thuật được mô tả trong tài liệu triển khai, nhóm nghiên cứu ghi nhận hiện tượng này nhưng chưa tiến hành đo đạc thực nghiệm độc lập.

---

> [!NOTE]
> **Đồng bộ danh mục bảng biểu:** Toàn bộ việc đánh số thứ tự bảng trong báo cáo khóa luận (gồm Bảng 5.1 đến Bảng 5.8) sẽ được rà soát và chuẩn hóa đồng bộ trên toàn bộ văn bản khóa luận tại User Story US-36.
