# CHƯƠNG 6. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

> [!NOTE]
> **Đề xuất, nhóm xác nhận**

Chương này tổng kết toàn bộ kết quả thực hiện của đồ án *"Hệ thống khuyến nghị gia sư dựa trên phương pháp Content-Base Filtering"*, đối chiếu trực tiếp với bốn mục tiêu cụ thể đã đăng ký trong đề cương; phân tích các hạn chế kỹ thuật hiện hữu và định hướng phát triển mở rộng trong tương lai; trình bày phân công trách nhiệm cùng kết quả tự đánh giá của nhóm nghiên cứu; đồng thời cung cấp bốn phụ lục kỹ thuật (Phụ lục A–D) chứa bộ dữ liệu mẫu, cấu trúc module tính điểm, danh mục hình ảnh giao diện thực tế và đặc tả chi tiết 14 kịch bản kiểm thử nền tảng.

---

## 6.1. Kết quả đạt được

Hệ thống khuyến nghị gia sư đã hoàn thiện các thành phần cốt lõi từ thuật toán tính điểm, dịch vụ API backend, giao diện tương tác người dùng frontend cho đến bộ kiểm thử tự động và tài liệu thiết kế. Kết quả thực tế được đối chiếu chi tiết với bốn mục tiêu cụ thể tại Mục 1.4 của đề cương đồ án trong Khung đối chiếu dưới đây.

### Khung đối chiếu kết quả thực hiện với bốn mục tiêu cụ thể (Mục 1.4 đề cương)

| Mục tiêu cụ thể (Mục 1.4) | Kết quả đạt được | Bằng chứng thực tế trong repo | Mức độ và giới hạn cụ thể |
|:---|:---|:---|:---|
| **(a) Mô hình hóa mức độ phù hợp và module lọc – tính điểm:** Phân loại tiêu chí (bắt buộc / ưu tiên / tùy chọn), công thức điểm cho từng tiêu chí, ngưỡng dữ liệu tối thiểu, module lọc – tính điểm có trọng số (Weighted Scoring). | Đã hiện thực trọn vẹn pipeline lọc và tính điểm: (1) Lọc điều kiện bắt buộc theo Bảng 3.2 (môn học, hình thức dạy, lịch rảnh tối thiểu); (2) Kiểm tra ngưỡng dữ liệu tối thiểu tương ứng với số tiêu chí áp dụng $n$; (3) Tính điểm thành phần $s_i \in [0, 1]$ cho 5 tiêu chí ưu tiên theo Bảng 3.6; (4) Tổng hợp điểm bằng công thức Weighted Scoring, phá hòa tất định theo mã gia sư (`tutor_id`) và trích xuất điểm đóng góp giải thích. | Mã nguồn backend: `backend/app/scoring/filters.py`, `backend/app/scoring/eligibility.py`, `backend/app/scoring/criteria.py`, `backend/app/scoring/weights.py`, `backend/app/scoring/ranker.py`, `backend/app/core/config.py`, tài liệu đặc tả `docs/design/scoring-spec.md`, 132 bài kiểm thử unit tại `backend/tests/unit/`, Bảng 5.8 (ca biên) tại Chương 5 `docs/thesis/report/chuong-05-thuc-nghiem-va-danh-gia.md`. | **Đã hiện thực, có giới hạn:** Pipeline hoạt động chính xác theo đặc tả; tuy nhiên các tham số ($\delta = 0,5$, $E_{\max} = 8$, điểm trung tính $0,5$) và bộ trọng số nguyên {0, 1, 2, 3} do nhóm ấn định theo phán đoán nghiệp vụ, chưa được ước lượng tự động từ dữ liệu hành vi người dùng. |
| **(b) Dịch vụ API gợi ý bằng FastAPI:** Tiếp nhận nhu cầu tìm kiếm của người học và trả về danh sách gia sư đã xếp hạng kèm điểm thành phần và điểm đóng góp. | Đã xây dựng hoàn chỉnh endpoint `POST /api/recommend` trên nền tảng FastAPI (Python 3.12). Dịch vụ xử lý hợp lệ dữ liệu đầu vào theo Pydantic schema, phân luồng phản hồi chính xác cho cả 4 trạng thái nghiệp vụ: `success` (HTTP 200), `no_match` (HTTP 200 khi không có ứng viên vượt qua vòng lọc), `zero_weight` (HTTP 200 khi tổng trọng số bằng 0), và lỗi kiểm thực `422 Unprocessable Entity`. | Mã nguồn endpoint: `backend/app/api/recommend.py`, cấu trúc schema: `backend/app/schemas/search_request.py`, `backend/app/schemas/recommendation.py`, hợp đồng API: `docs/design/api-contract.md`, 41 bài kiểm thử API tại `backend/tests/api/test_recommend_api.py`, số liệu đo đạc TestClient trong Chương 5 (trung bình 3,54 ms, tối đa 7,97 ms). | **Đã hiện thực, có giới hạn:** API xử lý đúng chuẩn trong môi trường kiểm thử bộ nhớ; đã triển khai thực tế trên đám mây Render; tuy nhiên phiên bản Render miễn phí (Free Tier) có độ trễ khởi động lại (cold start) khoảng 30–40 giây sau thời gian không hoạt động, và độ trễ truyền thông qua mạng Internet chưa được đo đạc định lượng. |
| **(c) Giao diện demo bằng ReactJS:** Cho phép người học nhập nhu cầu, chọn mức ưu tiên và xem kết quả xếp hạng kèm giải thích. | Đã xây dựng giao diện tương tác người dùng Single Page Application bằng React 18 và Vite: Màn hình nhập nhu cầu `SearchPage` (CN01) với bộ nạp nhanh 14 kịch bản; Màn hình kết quả `ResultPage` (CN02) hiển thị Top-$k$ gia sư kèm biểu đồ thanh xếp chồng điểm đóng góp và lý do gợi ý; Thanh điều chỉnh mức ưu tiên trực tiếp (CN03) cho phép cập nhật thứ hạng tức thì. | Mã nguồn frontend: `frontend/src/App.jsx`, `frontend/src/pages/SearchPage.jsx`, `frontend/src/pages/ResultPage.jsx`, `frontend/src/components/TutorCard.jsx`, `frontend/src/components/StackedBarScore.jsx`, `frontend/src/data/goalPresets.js`, `frontend/src/services/api.js`, ứng dụng trực tuyến tại Vercel. | **Đã hiện thực, có giới hạn:** Giao diện đáp ứng trọn vẹn kịch bản kiểm thử trải nghiệm và trực quan hóa thuật toán; tuy nhiên hệ thống dừng lại ở phạm vi demo tra cứu một chiều, chưa có hệ thống xác thực người dùng, chưa hỗ trợ đăng ký học hoặc đánh giá gia sư sau buổi học. |
| **(d) Đánh giá chất lượng xếp hạng qua kịch bản thực nghiệm:** Đánh giá chất lượng xếp hạng bằng các kịch bản có kỳ vọng xác định trước, minh họa ảnh hưởng của mức ưu tiên. | Đã số hóa và kiểm thử tự động 14 kịch bản tại Bảng 5.1; đạt độ trùng khớp 14/14 (100%) so với Top-3 kỳ vọng; phân tích chi tiết bản chất kỹ thuật của các ca biên (KB04, KB09, KB02, KB12); thực hiện khảo sát độ nhạy toàn diện trên 5 nhóm tham số tại Mục 5.2 (Bảng 5.2–5.7) xác nhận tính ổn định thứ hạng và vai trò điều hướng của mức ưu tiên. | Bộ kịch bản: `backend/tests/scenarios/scenarios.json`, `backend/tests/scenarios/test_scenarios.py` (27 bài kiểm thử), kết quả thực nghiệm tại Chương 5 `docs/thesis/report/chuong-05-thuc-nghiem-va-danh-gia.md`, tài liệu phân tích `docs/thesis/report/muc-5.2-danh-gia-do-on-dinh.md`, `docs/thesis/report/muc-5.2-ket-qua-tho.json`, `docs/thesis/report/discrepancy_analysis.md`. | **Đã hiện thực, có giới hạn:** Top-3 kỳ vọng do nhóm tự xác định dựa trên logic phán đoán nghiệp vụ; do đó kết quả 14/14 chỉ chứng minh hệ thống tính toán chính xác và nhất quán theo công thức toán học đã lựa chọn, chưa phản ánh độ thỏa mãn thực tế của người học ngoài đời thực. |

*Nguồn: Đối chiếu giữa Mục 1.4 đề cương đồ án với mã nguồn và kết quả thực nghiệm trong kho lưu trữ.*

### Mở rộng ngoài đề cương: Hỗ trợ Mục tiêu học tập tại giao diện người dùng

Xuất phát từ chỉ dẫn chuyên môn của Giáo viên hướng dẫn (TS. Lê Anh Nhã Uyên) ghi nhận trong báo cáo tiến độ giữa kỳ (`docs/thesis/review/sprint-05-midterm-progress-report.md`) — cho rằng nhu cầu của người học nên được mở rộng theo bộ ba *(Môn học, Cấp lớp, Mục tiêu học tập)* thay vì chỉ dừng ở tên môn học — nhóm đã nghiên cứu và ban hành tài liệu thiết kế `docs/design/de-xuat-mo-rong-cap-lop-muc-tieu.md`.

Hiện trạng triển khai thực tế như sau:
- **Phương án 1 (Adaptive Weight Mapping) đã hiện thực ở tầng giao diện người dùng (US-41):** Tại màn hình nhập nhu cầu `SearchPage` (`frontend/src/pages/SearchPage.jsx` và `frontend/src/data/goalPresets.js`), hệ thống bổ sung ô lựa chọn "Mục tiêu học tập" với ba thiết lập sẵn (preset) tự động điền bộ mức ưu tiên tương ứng: (1) *Mặc định* (các tiêu chí đều ở mức Trung bình $w=2$); (2) *Luyện thi điểm cao / học chuyên* (ưu tiên Kinh nghiệm và Đánh giá ở mức Cao $w=3$); (3) *Đậu tốt nghiệp / lấy lại căn bản* (ưu tiên Học phí ở mức Cao $w=3$). Sau khi chọn preset, người học vẫn có thể chủ động tinh chỉnh từng thanh trượt ưu tiên theo nhu cầu riêng.
- **Phương án 2 (bổ sung tiêu chí thành phần thứ sáu $s_6$ Goal Compatibility) và trường Cấp lớp CHƯA hiện thực:** Nguyên nhân do cơ sở dữ liệu hồ sơ gia sư hiện tại (`TutorProfile`) chỉ có 9 trường thông tin cơ bản, không có dữ liệu về cấp lớp nhận dạy, trình độ học vấn hay phong cách sư phạm.
- **Thống kê thực nghiệm:** Trích dẫn nguyên văn kết quả thử nghiệm từ tài liệu `docs/design/de-xuat-mo-rong-cap-lop-muc-tieu.md`: thử nghiệm trên 19 truy vấn (gồm 14 kịch bản nền tảng và 5 truy vấn tự đặt TQ1–TQ5) cho thấy có 2/5 truy vấn tự đặt đổi thứ hạng 2–3 giữa các preset mục tiêu, không có truy vấn nào đổi thứ hạng 1 (tổng 19 ca có 3 ca biến động thứ hạng 2–3; ca được chọn sau khi thử 19 truy vấn).
- **Trạng thái ghi nhận:** Đề xuất này là giải pháp kỹ thuật do nhóm chủ động nghiên cứu và hiện tại **chưa có phản hồi chính thức của GVHD**.

### Môi trường triển khai thực tế

Hệ thống đã được đóng gói và triển khai trực tuyến trên hạ tầng đám mây công cộng theo tài liệu hướng dẫn `docs/deployment/deploy-vercel-render.md`:
- **Giao diện người dùng (Frontend):** Triển khai trên nền tảng Vercel tại địa chỉ `https://tutor-recommender.vercel.app`.
- **Dịch vụ gợi ý (Backend API):** Triển khai trên nền tảng Render tại địa chỉ `https://tutor-recommender-api.onrender.com`.

Kiểm tra kiểm chứng ngày 10/11/2026 ghi nhận cả hai địa chỉ phản hồi mã trạng thái HTTP 200 OK (trang chủ frontend và endpoint kiểm tra sức khỏe `https://tutor-recommender-api.onrender.com/health`). Nhóm lưu ý rằng thời gian xử lý đo đạc bằng công cụ kiểm thử nội bộ `TestClient` trong Chương 5 (trung bình 3,54 ms, lớn nhất 7,97 ms) là thời gian xử lý nội tại trong bộ nhớ máy cục bộ; các số liệu này hoàn toàn tách biệt với độ trễ truyền thông qua mạng Internet thực tế và hiện tượng khởi động lại (cold start khoảng 30–40 giây) của dịch vụ Render gói miễn phí.

---

## 6.2. Hạn chế và hướng phát triển

### 6.2.1. Tổng hợp các hạn chế kỹ thuật hiện hữu

Dựa trên kết quả thực nghiệm và phân tích chuyên sâu tại Mục 5.3 của Chương 5 (`docs/thesis/report/chuong-05-thuc-nghiem-va-danh-gia.md`), hệ thống còn tồn tại các giới hạn cụ thể sau:

1. **Quy mô và tính đại diện của bộ dữ liệu:** Cơ sở dữ liệu thử nghiệm chỉ gồm 16 hồ sơ gia sư (14 hồ sơ mô phỏng và 2 hồ sơ thật thu thập công khai). Dù hai hồ sơ thật (`GS-T06`, `GS-T07`) giữ nguyên môn dạy, khu vực và số năm kinh nghiệm thực tế, các trường học phí và lịch rảnh bắt buộc phải ước tính do nền tảng gốc không công khai.
2. **Tính chủ quan của bộ kịch bản đánh giá:** Kết quả Top-3 kỳ vọng trong 14 kịch bản kiểm thử do nhóm tự xác định dựa trên lập luận nghiệp vụ và công thức đề xuất, chưa qua đánh giá mù độc lập từ học viên thật hay chuyên gia giáo dục.
3. **Tham số và bộ trọng số ấn định thủ công:** Ngưỡng vượt học phí $\delta = 0,5$, kinh nghiệm trần $E_{\max} = 8$, điểm đánh giá trung tính $0,5$ và thang trọng số {0, 1, 2, 3} được nhóm thiết lập cứng trong cấu hình (`backend/app/core/config.py`), chưa được học từ dữ liệu lịch sử.
4. **Thiếu vắng dữ liệu tương tác người dùng thực:** Hệ thống chưa ghi nhận các hành vi tương tác sau khuyến nghị như lượt nhấn xem hồ sơ (click), thời gian dừng đọc, tỷ lệ kết nối thành công hoặc phản hồi đánh giá của học viên sau các buổi học.
5. **Mô hình không gian địa lý đơn giản hóa:** Tiêu chí khu vực chỉ so khớp nhị phân (thuộc hoặc không thuộc quận/huyện), chưa đo lường khoảng cách địa lý đường bộ thực tế hay thời gian di chuyển giữa học viên và gia sư.
6. **Môi trường triển khai đám mây miễn phí:** Gói dịch vụ miễn phí trên đám mây có hiện tượng cold start và độ trễ truyền mạng biến động chưa được đo lường định lượng chính thức.

### 6.2.2. Hướng phát triển theo đề cương đồ án

Để từng bước hoàn thiện giải pháp và nâng cao khả năng ứng dụng thực tiễn, đề cương đồ án định hướng ba giai đoạn phát triển tiếp theo:

1. **Tích hợp làm module khuyến nghị lõi cho nền tảng gia sư hoàn chỉnh:** Kết nối module lọc – tính điểm hiện tại với hệ thống cơ sở dữ liệu quan hệ hoàn chỉnh (quản lý tài khoản người học, hồ sơ gia sư đã xác minh danh tính, nghiệp vụ đăng ký học thử, xếp lịch dạy học và cổng thanh toán học phí an toàn).
2. **Nâng cấp mô hình Hybrid kết hợp Collaborative Filtering:** Khi nền tảng tích lũy đủ số lượng học viên và lịch sử tương tác, xây dựng ma trận tương tác người dùng – gia sư (User-Item Interaction Matrix) để kết hợp phương pháp lọc cộng tác (Collaborative Filtering) với phương pháp dựa trên đặc trưng hồ sơ, giúp giải quyết bài toán khởi động lạnh (cold-start) cho người dùng mới đồng thời khai thác được thị hiếu cộng đồng.
3. **Ứng dụng học máy xếp hạng (Learning-to-Rank):** Thay thế bảng quy đổi trọng số thủ công bằng các mô hình học máy xếp hạng có giám sát. Bộ trọng số và hàm số kết hợp sẽ được tự động học và hiệu chỉnh dựa trên tín hiệu phản hồi ngầm định (như hành vi bấm chọn, lưu hồ sơ) và phản hồi tường minh (điểm đánh giá sau khóa học) của người học.

### 6.2.3. Đề xuất mở rộng mô hình: Cấp lớp, Mục tiêu học tập và tiêu chí $s_6$

Bên cạnh ba hướng phát triển nêu trên, nhóm đề xuất hướng mở rộng cấu trúc dữ liệu và giải thuật đã được phác thảo tại `docs/design/de-xuat-mo-rong-cap-lop-muc-tieu.md`:
- Mở rộng cấu trúc `TutorProfile` trong cơ sở dữ liệu để lưu trữ chính thức các trường: Cấp lớp nhận dạy (Tiểu học, THCS, THPT, Luyện thi), Trình độ chuyên môn (Giảng viên, Thạc sĩ, Cử nhân, Sinh viên sư phạm), và Thế mạnh giảng dạy (Luyện thi chuyên sâu, Lấy lại căn bản, Kiên nhẫn, Nhiệt tình).
- Khi có đầy đủ dữ liệu hồ sơ, hiện thực chính thức Phương án 2: bổ sung tiêu chí thành phần thứ sáu $s_6$ (Goal Compatibility) vào backend và điều chỉnh công thức tổng hợp điểm Weighted Scoring.
- Đây là **đề xuất kỹ thuật của nhóm, hiện đang chờ ý kiến đóng góp và định hướng chuyên môn từ GVHD** trước khi triển khai vào mã nguồn chính thức.

---

## 6.3. Tự đánh giá và phân công công việc

### Bảng 6.1 - Phân công công việc và mức độ hoàn thành của các thành viên trong nhóm

| STT | Thành viên | Mã sinh viên | Công việc phụ trách | Mức độ hoàn thành |
|:---:|:---|:---:|:---|:---:|
| 1 | **Lê Thị Bích Chuyền** | KHMT2411037 | **Scrum Master các Sprint 2, 4, 6 kiêm Developer:** Điều phối nghi thức Scrum ở các Sprint chẵn; phát triển giao diện ReactJS (Vite), kết nối API và kiểm thử trải nghiệm người dùng; tham gia thiết kế dữ liệu và kiểm thử hệ thống. | *[Điền cuối khóa luận]* |
| 2 | **Trần Nguyễn Đức** | KHMT2411011 | **Scrum Master các Sprint 1, 3, 5 kiêm Developer:** Điều phối nghi thức Scrum ở các Sprint lẻ và phụ trách quản lý nhánh/PR trên GitHub; phát triển lõi chấm điểm backend FastAPI, thuật toán xếp hạng và kiểm thử tự động. | *[Điền cuối khóa luận]* |
| 3 | **Cao Khánh Ngọc** *(Nhóm trưởng)* | KHMT2411025 | **Product Owner kiêm Developer:** Đại diện yêu cầu đề tài và làm việc với GVHD (TS. Lê Anh Nhã Uyên), quản lý và ưu tiên Product Backlog, nghiệm thu sản phẩm theo Definition of Done; tham gia phát triển tài liệu, thiết kế dữ liệu và kiểm thử. | *[Điền cuối khóa luận]* |

*Ghi chú: Phân công thực tế do nhóm xác nhận. Toàn bộ mã nguồn và tài liệu trên GitHub được quản trị và hợp nhất thông qua tài khoản điều phối kỹ thuật, do đó số lượng commit hoặc Pull Request trên Git không đại diện cho tỷ lệ đóng góp của từng cá nhân; mức độ hoàn thành sẽ được tập thể nhóm và GVHD đánh giá ở giai đoạn tổng kết khóa luận.*  
*Nguồn: `docs/scrum/roles.md` và `docs/thesis/outline/muc-6.1-bang-6.1.md`.*

### Tự đánh giá kết quả thực hiện

Tập thể nhóm tự đánh giá quá trình thực hiện đồ án dựa trên các bằng chứng kỹ thuật có thể kiểm chứng độc lập trong kho lưu trữ mã nguồn:
- **Tính đầy đủ của sản phẩm:** Nhóm đã hoàn thành toàn bộ các thành phần phần mềm đã đăng ký trong đề cương, bao gồm module thuật toán tính điểm backend, dịch vụ RESTful API, ứng dụng web frontend tương tác trực quan và hạ tầng triển khai trực tuyến.
- **Chất lượng kiểm thử và độ tin cậy:** Hệ thống đạt 200/200 bài kiểm thử tự động thành công (100% passed) thực hiện qua thư viện pytest; độ bao phủ mã nguồn backend đạt 97% (340/351 câu lệnh được phủ theo lệnh đo `pytest --cov=app`); 14/14 kịch bản thực nghiệm nền tảng đạt kết quả trùng khớp hoàn toàn với thứ tự kỳ vọng đã thiết lập.
- **Tính toàn vẹn dữ liệu:** Toàn bộ 16 hồ sơ gia sư trong `data/processed/tutors.json` và `data/processed/tutors.csv` vượt qua kiểm tra toàn vẹn định dạng và bảo toàn cấu trúc dữ liệu theo kịch bản xác thực `scripts/validate_tutors.py`.
- **Kỷ luật kỹ thuật và tài liệu hóa:** Quy trình phát triển phần mềm được tổ chức bài bản theo mô hình Scrum qua 6 Sprint; toàn bộ các tài liệu kiến trúc, đặc tả thuật toán, hợp đồng API, biên bản hồi tưởng và báo cáo thực nghiệm đều được cập nhật đồng bộ, lưu trữ phiên bản minh bạch trong kho lưu trữ Git.
- Cột "Mức độ hoàn thành" tại Bảng 6.1 được giữ nguyên quy ước `[Điền cuối khóa luận]` để hội đồng đánh giá và GVHD đưa ra kết luận chính thức tại buổi bảo vệ đồ án.

---

## PHỤ LỤC A. BỘ DỮ LIỆU MẪU

### 1. Mô tả nguồn gốc và quy trình xử lý dữ liệu gia sư

Nhóm nghiên cứu đã thực hiện khảo sát và thu thập thủ công 15 hồ sơ gia sư ban đầu từ hai nền tảng gia sư trực tuyến công khai tại Việt Nam là giasudatviet.com và giasudantri.vn. Sau bước xác minh sơ bộ, nhóm chọn lọc được 11 hồ sơ đáp ứng phạm vi nhận dạy thực tế trên địa bàn Thành phố Hồ Chí Minh.

Đặc điểm dữ liệu trên các nền tảng thực tế cho thấy các thông tin như học phí theo giờ, khung giờ rảnh cụ thể trong tuần và điểm đánh giá trung bình không được công khai theo từng hồ sơ cá nhân. Nhằm phục vụ nghiên cứu học thuật mà vẫn tuân thủ đạo đức nghiên cứu và bảo vệ tính riêng tư cá nhân:
- Nhóm giữ lại 2 hồ sơ thu thập thực tế (mã hóa danh tính thành `GS-T06` và `GS-T07`) làm bằng chứng đại diện cho quy trình khảo sát thủ công từ nguồn công khai. Các trường thông tin về môn dạy, danh sách khu vực nhận dạy và số năm kinh nghiệm là số liệu thu thập thực tế đã được ẩn danh hóa.
- Học phí của hai hồ sơ này được nhóm ước tính trong khoảng từ 130.000 đến 400.000 VNĐ/giờ dựa trên quan sát mức học phí thị trường tại daythem.com và nội suy tương ứng theo số năm kinh nghiệm giảng dạy; khung giờ rảnh được nhóm giả định theo các ca học phổ biến; hai trường này được đánh dấu ký hiệu `(*)` trong bảng dữ liệu. Điểm đánh giá trung bình của hai hồ sơ được để trống (`null`) và hệ thống tự động gán giá trị trung tính $0,5$ khi tính toán.
- 14 hồ sơ gia sư còn lại (`GS006`, `GS020`, và `GS-G01` đến `GS-G12`) là dữ liệu mô phỏng do nhóm tự xây dựng nhằm đảm bảo độ bao phủ các tổ hợp điều kiện biên, kiểm thử trường hợp không có kết quả (`no_match`), trường hợp học trực tuyến hoàn toàn, và các tình huống đồng điểm phức tạp.
- **Ghi nhận minh bạch về kho lưu trữ:** Trong cấu trúc mã nguồn hiện tại, thư mục `data/raw` chỉ chứa tệp `.gitkeep` lưu chỗ, quy trình thu thập 15 hồ sơ ban đầu không lưu trữ tệp dữ liệu thô trong repo (nguồn trích dẫn: bản thuyết minh đề cương đồ án).
- **Chuẩn hóa nhãn môn học hồ sơ GS-G03:** Nhãn môn học của hồ sơ `GS-G03` được chuẩn hóa từ "Tiếng Anh" thành "Anh Văn" theo ghi nhận tại `data/README.md` (mục 4) nhằm đồng bộ với danh mục môn học chung của toàn hệ thống.
- **Nhãn nguồn dữ liệu:** Nhãn `data_source` của hai hồ sơ `GS-T06` và `GS-T07` được giữ nguyên giá trị `public_collected` trong toàn bộ cơ sở dữ liệu (`data/processed/tutors.json`, `data/processed/tutors.csv`, `frontend/src/data/tutorsCatalog.js`) theo đúng quyết định thống nhất của nhóm nghiên cứu.

### 2. Danh sách 16 hồ sơ gia sư mẫu

| STT | Mã gia sư | Môn dạy | Khu vực | Học phí (VNĐ/giờ) | Số năm KN | Hình thức dạy | Lịch rảnh | Đánh giá TB | Nguồn dữ liệu |
|:---:|:---|:---|:---|:---:|:---:|:---:|:---|:---:|:---|
| 1 | GS-T06 | Toán, Lý, Hóa | Bình Thạnh, Gò Vấp, Phú Nhuận, Tân Bình, Tân Phú | 400.000 (*) | 20 | Trực tiếp | T2-tối, T4-tối, T6-tối (*) | để trống | Thu thập công khai |
| 2 | GS-T07 | Anh Văn, Anh Văn GT | Bình Chánh, Nhà Bè, Quận 7, Quận 8 | 190.000 (*) | 6 | Trực tiếp | T3-tối, T5-tối, T7-sáng (*) | để trống | Thu thập công khai |
| 3 | GS006 | Lý, Hóa | để trống | 190.000 | 5 | Trực tuyến | T2-tối, T3-tối, T4-tối, T5-tối | 4,6 | Giả lập |
| 4 | GS020 | Lý, Hóa | để trống | 240.000 | 5 | Trực tuyến | T2-tối, T3-tối, T4-tối, T5-tối | 4,6 | Giả lập |
| 5 | GS-G01 | Toán | Bình Thạnh | 180.000 | 6 | Cả hai | T2-tối, T4-tối, T7-sáng | 5,0 | Giả lập |
| 6 | GS-G02 | Toán | Bình Thạnh | 300.000 | 3 | Cả hai | T2-tối, T4-tối, T7-sáng | 3,0 | Giả lập |
| 7 | GS-G03 | Anh Văn | Gò Vấp | 200.000 | 4 | Trực tuyến | T3-sáng, T5-sáng | 4,5 | Giả lập |
| 8 | GS-G04 | Văn | Quận 1, Quận 3 | 170.000 | 7 | Trực tiếp | T2-chiều, T5-chiều | 4,3 | Giả lập |
| 9 | GS-G05 | Sinh | Thủ Đức, Quận 9 | 190.000 | 4 | Cả hai | T3-tối, T6-tối | 4,0 | Giả lập |
| 10 | GS-G06 | Hóa | Quận 10, Quận 11 | 210.000 | 8 | Trực tiếp | T4-sáng, T7-sáng | 4,7 | Giả lập |
| 11 | GS-G07 | Tin học | Bình Thạnh, Thủ Đức | 220.000 | 5 | Trực tuyến | T2-tối, T4-tối, T6-tối | 4,4 | Giả lập |
| 12 | GS-G08 | Tiếng Nhật | Phú Nhuận, Tân Bình | 260.000 | 6 | Cả hai | T3-chiều, T5-chiều | 4,8 | Giả lập |
| 13 | GS-G09 | Toán | Quận 7 | 350.000 | 2 | Trực tiếp | T2-tối, T4-tối | 3,5 | Giả lập |
| 14 | GS-G10 | Toán | Quận 7 | 130.000 | 12 | Trực tiếp | T2-tối, T4-tối | 4,9 | Giả lập |
| 15 | GS-G11 | Anh Văn | Quận 2, Bình Thạnh | 200.000 | 5 | Trực tiếp | T3-sáng, T6-sáng | 4,5 | Giả lập |
| 16 | GS-G12 | Anh Văn | Quận 2, Thủ Đức | 200.000 | 5 | Trực tiếp | T3-sáng, T6-sáng | 4,5 | Giả lập |

*Bảng A.1 - Danh sách 16 hồ sơ gia sư mẫu*  
*Ghi chú: (*) Học phí và lịch rảnh của gia sư GS-T06 và GS-T07 là số liệu ước tính của nhóm nghiên cứu; môn dạy, khu vực và số năm kinh nghiệm là dữ liệu thu thập thực tế từ nguồn công khai đã được ẩn danh hóa. Điểm đánh giá để trống được thuật toán tự động xử lý bằng giá trị trung tính 0,5.*  
*Nguồn: `data/processed/tutors.json` và `data/processed/tutors.csv`.*

### 3. Danh mục khu vực quy ước trong hệ thống

Tập hợp danh mục khu vực địa lý sử dụng trong hệ thống được trích xuất từ các khu vực xuất hiện trong `data/processed/tutors.json` và đối chiếu với danh mục lựa chọn `DISTRICT_OPTIONS` trong mã nguồn frontend `frontend/src/services/api.js`:
- **Danh sách 16 quận/huyện quy ước:** Bình Chánh, Bình Thạnh, Gò Vấp, Nhà Bè, Phú Nhuận, Quận 1, Quận 2, Quận 3, Quận 7, Quận 8, Quận 9, Quận 10, Quận 11, Tân Bình, Tân Phú, Thủ Đức.
- **Đối chiếu:** Hai tập hợp trong cơ sở dữ liệu `data/processed/tutors.json` và cấu hình giao diện `DISTRICT_OPTIONS` trùng khớp hoàn toàn 16/16 khu vực (độ sai lệch bằng 0).
- **Khác biệt so với thực tế hành chính hiện hành:** Nhóm ghi nhận danh mục quy ước này không bám sát đơn vị hành chính hiện hành của Thành phố Hồ Chí Minh. Cụ thể, hệ thống vẫn duy trì tách biệt "Quận 2", "Quận 9" và "Thủ Đức" (trong khi các đơn vị này đã sáp nhập thành Thành phố Thủ Đức từ ngày 01/01/2021); đồng thời danh mục chưa bao quát đầy đủ 22 đơn vị hành chính cấp huyện của thành phố (thiếu Quận 4, Quận 5, Quận 6, Quận 12, Bình Tân, Hóc Môn, Củ Chi, Cần Giờ). Đây là danh mục quy ước đóng cục bộ phục vụ cho phạm vi thử nghiệm của đồ án.

### 4. Kết quả kiểm tra tính toàn vẹn của bộ dữ liệu

Tính toàn vẹn, hợp lệ kiểu dữ liệu và sự đồng bộ tuyệt đối giữa định dạng JSON và CSV của bộ dữ liệu 16 hồ sơ được xác minh thông qua lệnh chạy:

```powershell
python scripts/validate_tutors.py
```

Kết quả thực thi thực tế:

```text
ĐẠT: 16 bản ghi (2 public_collected, 14 simulated); id duy nhất; enum hợp lệ;
     đủ 9 trường; không có thông tin liên hệ; JSON và CSV khớp nhau từng ô.
```

---

## PHỤ LỤC B. MODULE TÍNH ĐIỂM VÀ XẾP HẠNG

Bảng dưới đây liệt kê danh mục các tệp mã nguồn, lớp và hàm chính hiện thực logic tính điểm và điều phối gợi ý trong gói `backend/app/`, được đối chiếu với các bước xử lý tương ứng tại Mục 3.6 của đề cương đồ án.

### Bảng B.1 - Danh mục tệp mã nguồn và hàm nghiệp vụ trong module gợi ý gia sư

| STT | Tệp mã nguồn | Lớp / Hàm chính | Vai trò kỹ thuật | Bước tương ứng trong Mục 3.6 |
|:---:|:---|:---|:---|:---|
| 1 | `backend/app/core/config.py` | Hằng số: `DELTA = 0.5`, `E_MAX = 8`, `RATING_DEFAULT = 0.5`, `PRIORITY_WEIGHTS`, `CRITERIA_KEYS` | Quản lý tham số thuật toán khởi tạo, bảng quy đổi mức ưu tiên sang trọng số nguyên và các khóa tiêu chí dùng chung. | Khởi tạo tham số và bảng quy đổi trọng số (Mục 3.6, Bảng 3.5, Bảng 3.6) |
| 2 | `backend/app/data/repository.py` | Lớp `TutorRepository` (hàm `get_all()`, `get_by_id()`), `TutorDataError` | Đọc dữ liệu từ `data/processed/tutors.json`, kiểm tra tính toàn vẹn và cung cấp danh sách hồ sơ gia sư cho pipeline trong bộ nhớ. | Cung cấp dữ liệu hồ sơ gia sư đầu vào |
| 3 | `backend/app/schemas/tutor.py` | Lớp Pydantic `TutorProfile` | Định nghĩa cấu trúc dữ liệu và kiểm thực kiểu dữ liệu cho 9 trường của hồ sơ gia sư (`extra="forbid"`). | Cấu trúc dữ liệu đặc trưng hồ sơ gia sư |
| 4 | `backend/app/schemas/search_request.py` | Lớp Pydantic `SearchRequest`, hàm `default_priorities()` | Định nghĩa cấu trúc truy vấn tìm kiếm của người học (7 trường), kiểm thực dữ liệu và gán mức ưu tiên mặc định. | Bước 1: Kiểm tra và chuẩn hóa yêu cầu tìm kiếm đầu vào |
| 5 | `backend/app/scoring/filters.py` | Hàm `filter_mandatory()`, `_matches_subject()`, `_matches_mode()`, `_matches_availability()` | Lọc danh sách gia sư theo các ràng buộc cứng: môn dạy, hình thức dạy/học và điều kiện trùng lịch tối thiểu ($|L \cap T| \ge 1$). | Bước 2: Lọc điều kiện bắt buộc (Bảng 3.2) |
| 6 | `backend/app/scoring/weights.py` | Lớp `EffectiveWeights`, hàm `compute_effective_weights()`, `priority_to_weight()`, `_applicable_criteria()` | Xác định số tiêu chí ưu tiên đang áp dụng ($n$) và tính bộ trọng số hiệu dụng $w_i$; tự động vô hiệu hóa ($w_i = 0$) các tiêu chí không áp dụng. | Xác định tiêu chí áp dụng và tính trọng số hiệu dụng |
| 7 | `backend/app/scoring/eligibility.py` | Hàm `filter_eligible_candidates()`, `check_tutor_eligibility()`, `count_available_criteria()`, `get_min_required_criteria()` | Đếm số tiêu chí ưu tiên có dữ liệu của gia sư và so khớp với bảng ngưỡng tối thiểu theo $n$; loại bỏ hồ sơ không đủ dữ liệu. | Điều kiện đủ dữ liệu để xếp hạng (ngưỡng tối thiểu giữa Bước 2 và Bước 3) |
| 8 | `backend/app/scoring/criteria.py` | Các hàm tính điểm: `score_fee()`, `score_location()`, `score_experience()`, `score_rating()`, `score_schedule()` | Hiện thực 5 công thức toán học tính điểm thành phần $s_i \in [0, 1]$ cho học phí, khu vực, kinh nghiệm, đánh giá và lịch rảnh. | Bước 3: Tính điểm thành phần $s_i$ cho các tiêu chí ưu tiên (Bảng 3.6) |
| 9 | `backend/app/scoring/ranker.py` | Hàm `score_and_rank()`, `_compute_single_criterion_score()`, `build_reason()`, `build_notes()` | Tổng hợp điểm Weighted Scoring $S = \sum (w_i \cdot s_i) / \sum w_i$, sắp xếp giảm dần, phá hòa tất định theo `tutor_id`, trích xuất điểm đóng góp và ghi chú giải thích. | Bước 4: Tổng hợp điểm Weighted Scoring và xếp hạng |
| 10 | `backend/app/schemas/recommendation.py` | Các lớp Pydantic: `RankedTutor`, `RecommendationSuccessResponse`, `NoMatchResponse`, `ZeroWeightResponse` | Định nghĩa cấu trúc phản hồi JSON cho các trường hợp nghiệp vụ: danh sách xếp hạng thành công, không có ứng viên và tổng trọng số bằng 0. | Định dạng cấu trúc dữ liệu phản hồi khuyến nghị |
| 11 | `backend/app/api/recommend.py` | Hàm endpoint `recommend_tutors()`, phụ trợ `get_tutor_repository()` | Tiếp nhận yêu cầu POST `/api/recommend`, điều phối luồng thực thi toàn bộ pipeline và trả về kết quả chuẩn hóa theo hợp đồng API. | Tích hợp toàn diện pipeline vào dịch vụ API FastAPI |

*Nguồn: Mã nguồn ứng dụng backend trong `backend/app/`.*

---

## PHỤ LỤC C. DANH MỤC HÌNH ẢNH GIAO DIỆN DEMO

### 1. Danh mục hình ảnh hiện có trong kho lưu trữ mã nguồn

Kho lưu trữ hiện lưu trữ 5 tệp hình ảnh chụp giao diện và kết quả kiểm thử tại thư mục `docs/thesis/assets/midterm/` (thư mục `docs/thesis/figures` hiện chỉ chứa `.gitkeep`):

### Bảng C.1 - Danh mục hình ảnh giao diện demo hiện có trong repo

| STT | Tệp hình ảnh trong repo | Nội dung thể hiện | Đánh giá hiện trạng kỹ thuật |
|:---:|:---|:---|:---|
| 1 | `docs/thesis/assets/midterm/hinh-1-cn01-nhap-nhu-cau.png` | Giao diện màn hình nhập nhu cầu học tập và bộ nút nạp nhanh 14 kịch bản thực nghiệm (CN01). | **Có thể lỗi thời:** Ảnh chụp tại thời điểm Sprint 5, chưa thể hiện ô lựa chọn "Mục tiêu học tập" (3 preset) được bổ sung tại US-41 (PR #85). |
| 2 | `docs/thesis/assets/midterm/hinh-2-cn02-ket-qua-top3.png` | Màn hình kết quả danh sách gợi ý Top-3, biểu đồ thanh xếp chồng điểm đóng góp và văn bản giải thích lý do gợi ý ở kịch bản KB01 (CN02). | Đầy đủ nội dung cơ bản; có thể cập nhật để đồng bộ định dạng trực quan mới nhất. |
| 3 | `docs/thesis/assets/midterm/hinh-3-cn03-dieu-chinh-uu-tien.png` | Bảng điều khiển tinh chỉnh mức ưu tiên trực tiếp trên màn hình kết quả và sự thay đổi thứ hạng gia sư tức thì (CN03). | **Có thể lỗi thời:** Nhãn mức ưu tiên 0 trong ảnh là "Không quan trọng" hoặc "Bỏ qua", chưa hiển thị rõ quy ước nhãn hiện hành "Bỏ qua (w = 0)". |
| 4 | `docs/thesis/assets/midterm/hinh-4-swagger-api-recommend.png` | Giao diện tài liệu tương tác OpenAPI (Swagger UI) của endpoint `POST /api/recommend` trên nền tảng FastAPI. | Thể hiện đúng giao diện Swagger UI của dịch vụ backend. |
| 5 | `docs/thesis/assets/midterm/hinh-5-pytest-190-passed.png` | Kết quả thực thi kiểm thử tự động trên terminal hiển thị mốc 190 bài kiểm thử vượt qua. | **Lỗi thời:** Ảnh chụp mốc 190 passed ở Sprint 5; hiện tại bộ kiểm thử đã đạt 200 passed (bổ sung 10 bài kiểm thử độ nhạy ở Sprint 6). |

*Nguồn: Thư mục `docs/thesis/assets/midterm/` trong kho lưu trữ mã nguồn.*

### 2. Danh sách hình ảnh đề xuất chụp lại cho bản báo cáo chính thức

Để đảm bảo tính đồng bộ tuyệt đối với phiên bản phần mềm nghiệm thu cuối cùng, các hình ảnh sau được đề xuất chụp mới để đưa vào bản thuyết minh chính thức (thay thế hoặc bổ sung vào `docs/thesis/figures`):
1. **Hình chụp CN01 mới:** Màn hình nhập nhu cầu hiển thị đầy đủ ô lựa chọn "Mục tiêu học tập" với 3 preset (Mặc định, Luyện thi điểm cao / học chuyên, Đậu tốt nghiệp / lấy lại căn bản).
2. **Hình chụp CN02 mới:** Màn hình kết quả Top-3 hiển thị thanh xếp chồng phân rã điểm thành phần ($w_i \cdot s_i / \sum w_i$) và văn bản giải thích rõ ràng.
3. **Hình chụp CN03 mới:** Màn hình điều chỉnh trực tiếp mức ưu tiên với nhãn chuẩn hóa "Bỏ qua (w = 0)".
4. **Hình chụp trạng thái tổng trọng số bằng 0:** Màn hình kết quả khi người học tắt toàn bộ các tiêu chí ưu tiên ($\sum w = 0$), hiển thị phản hồi hướng dẫn người học bật lại ít nhất một tiêu chí (`zero_weight`).
5. **Hình chụp Swagger UI tài liệu API:** Giao diện Swagger UI của FastAPI hiển thị đầy đủ schema của `SearchRequest` và `RecommendationSuccessResponse`.
6. **Hình chụp terminal kiểm thử 200 passed:** Kết quả chạy `pytest -q` đạt 200 passed và `pytest --cov=app` đạt độ bao phủ 97% trên môi trường Python 3.12.

---

## PHỤ LỤC D. KỊCH BẢN KIỂM THỬ THỰC NGHIỆM

Bảng D.1 đặc tả chi tiết toàn bộ tham số đầu vào và danh sách Top-3 kỳ vọng của 14 kịch bản tìm kiếm gia sư, được trích xuất trực tiếp từ tệp dữ liệu kịch bản `backend/tests/scenarios/scenarios.json`.

### Bảng D.1 - Yêu cầu đầy đủ của 14 kịch bản thực nghiệm

| Mã KB | Môn | Hình thức | Khu vực | Ngân sách (VNĐ/giờ) | Khung giờ | Mức ưu tiên khác mặc định | Top-3 kỳ vọng |
|:---:|:---|:---|:---|:---:|:---|:---|:---|
| KB01 | Toán | Trực tiếp | Bình Thạnh | 200.000 | Không nhập | Mặc định (đều w=2) | GS-G01, GS-G10, GS-T06 |
| KB02 | Anh Văn | Trực tiếp | Quận 2 | 220.000 | Không nhập | Mặc định (đều w=2) | GS-G11, GS-G12, GS-T07 |
| KB03 | Anh Văn | Trực tiếp | Thủ Đức | 220.000 | Không nhập | Mặc định (đều w=2) | GS-G12, GS-G11, GS-T07 |
| KB04 | Lý | Trực tuyến | Không nhập | 200.000 | T2-tối, T4-tối | Mặc định (đều w=2) | GS006, GS020 |
| KB05 | Tiếng Trung | any | Không nhập | Không nhập | Không nhập | Mặc định (đều w=2) | Không có (0 kết quả) |
| KB06 | Văn | Trực tiếp | Quận 1 | 180.000 | Không nhập | Mặc định (đều w=2) | GS-G04 |
| KB07 | Sinh | any | Thủ Đức | 200.000 | Không nhập | Mặc định (đều w=2) | GS-G05 |
| KB08 | Tin học | Trực tuyến | Không nhập | 250.000 | T2-tối, T6-tối | Mặc định (đều w=2) | GS-G07 |
| KB09 | Tiếng Nhật | any | Phú Nhuận | 280.000 | Không nhập | Mặc định (đều w=2) | GS-G08 |
| KB10 | Toán | Trực tiếp | Quận 7 | Không nhập | Không nhập | Kinh nghiệm: Cao (w=3) | GS-G10, GS-G01, GS-G09 |
| KB11 | Hóa | Trực tiếp | Quận 10 | 220.000 | Không nhập | Mặc định (đều w=2) | GS-G06, GS-T06 |
| KB12 | Anh Văn | Trực tiếp | Bình Chánh | 200.000 | Không nhập | Mặc định (đều w=2) | GS-T07, GS-G11, GS-G12 |
| KB13 | Toán | any | Không nhập | 150.000 | Không nhập | Mặc định (đều w=2) | GS-G10, GS-G01, GS-T06 |
| KB14 | Anh Văn | Trực tuyến | Không nhập | Không nhập | Không nhập | Mặc định (đều w=2) | GS-G03 |

*Bảng D.1 - Yêu cầu đầy đủ của 14 kịch bản thực nghiệm*  
*Ghi chú: Cột "Khung giờ" và "Khu vực" ghi nhận "Không nhập" khi người học không điền tiêu chí tùy chọn tương ứng; mức ưu tiên mặc định của cả 5 tiêu chí là Trung bình (w = 2). Kết quả Top-3 kỳ vọng được xác lập dựa trên suy luận logic nghiệp vụ để đối chiếu với thuật toán.*  
*Nguồn: `backend/tests/scenarios/scenarios.json`.*

### Dẫn chiếu kết quả thực nghiệm và kiểm thử ca biên

Nhằm đảm bảo tính súc tích và tránh trùng lặp số liệu trong toàn bộ báo cáo:
- **Kết quả xếp hạng thực tế của hệ thống đối với 14 kịch bản:** Kết quả chạy thật qua pipeline xếp hạng, đối chiếu số lượng trùng khớp (14/14 đạt 100%) và phân tích chi tiết bản chất kỹ thuật của các ca đặc biệt (KB04, KB09, KB02, KB12) đã được trình bày đầy đủ tại **Bảng 5.1 (Kết quả thực nghiệm 14 kịch bản tìm kiếm gia sư)** trong Chương 5 (`docs/thesis/report/chuong-05-thuc-nghiem-va-danh-gia.md`).
- **Kết quả kiểm thử ca biên của 5 hàm điểm:** Bảng ma trận kiểm thử các giá trị biên cực đoan và tính đơn điệu của các hàm điểm thành phần đã được trình bày chi tiết tại **Bảng 5.8 (Kết quả kiểm thử ca biên và tính đơn điệu của hàm điểm)** trong Chương 5.
- *Ghi chú đồng bộ:* Số hiệu Bảng 5.8 trong Chương 5 có thể được điều chỉnh và đồng bộ lại danh mục bảng trong giai đoạn đóng gói toàn văn báo cáo khóa luận (US-36).
