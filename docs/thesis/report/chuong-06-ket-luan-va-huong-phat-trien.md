# CHƯƠNG 6. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

Chương này tổng kết kết quả thực hiện của đồ án “Hệ thống khuyến nghị gia sư dựa trên phương pháp Content-Base Filtering” theo bốn mục tiêu cụ thể đã đăng ký trong đề cương. Chương cũng trình bày các hạn chế hiện hữu, hướng phát triển mở rộng, phân công và tự đánh giá của nhóm, cùng bốn phụ lục kỹ thuật (Phụ lục A–D) gồm bộ dữ liệu mẫu, module tính điểm, danh mục hình ảnh giao diện và đặc tả 14 kịch bản thực nghiệm.

---

## 6.1. Kết quả đạt được

Hệ thống khuyến nghị gia sư đã hoàn thiện các thành phần cốt lõi từ thuật toán tính điểm, dịch vụ API backend, giao diện người dùng frontend cho đến bộ kiểm thử tự động và tài liệu thiết kế. Kết quả thực tế được đối chiếu trực tiếp với bốn mục tiêu cụ thể tại Mục 1.4 trong Khung đối chiếu dưới đây.

### 6.1.1. Khung đối chiếu kết quả thực hiện với bốn mục tiêu cụ thể (Mục 1.4 đề cương)

| Mục tiêu cụ thể (Mục 1.4) | Kết quả đạt được | Bằng chứng thực tế trong kho lưu trữ | Mức độ và giới hạn cụ thể |
|:---|:---|:---|:---|
| **(a) Mô hình hóa mức độ phù hợp và module lọc – tính điểm:** Phân loại tiêu chí (bắt buộc/ưu tiên/tùy chọn), công thức điểm cho từng tiêu chí, ngưỡng dữ liệu tối thiểu, module lọc – tính điểm có trọng số (Weighted Scoring). | Đã hiện thực đầy đủ pipeline lọc và tính điểm: (1) lọc điều kiện bắt buộc theo Bảng 3.2 (môn học, hình thức dạy, lịch rảnh tối thiểu); (2) kiểm tra ngưỡng dữ liệu tối thiểu tương ứng với số tiêu chí áp dụng $n$; (3) tính điểm thành phần $s_i \in [0, 1]$ cho 5 tiêu chí ưu tiên theo Bảng 3.6; (4) tổng hợp bằng Weighted Scoring, phá hòa tất định theo mã gia sư (`tutor_id`) và trích xuất điểm đóng góp cùng lý do gợi ý. | `backend/app/scoring/filters.py`, `eligibility.py`, `criteria.py`, `weights.py`, `ranker.py`, `backend/app/core/config.py`, `docs/design/scoring-spec.md`, 132 bài kiểm thử đơn vị tại `backend/tests/unit/` và `test_environment.py`, Bảng 5.2 (Chương 5). | **Đã hiện thực, có giới hạn:** Pipeline tính đúng theo đặc tả; tuy nhiên các tham số ($\delta = 0{,}5$, $E_{\max} = 8$, điểm trung tính $0{,}5$) và bộ trọng số nguyên $\{0, 1, 2, 3\}$ do nhóm ấn định theo giả định nghiệp vụ, chưa được ước lượng từ dữ liệu hành vi người dùng. |
| **(b) Dịch vụ API gợi ý bằng FastAPI:** Tiếp nhận nhu cầu tìm kiếm của người học và trả về danh sách gia sư đã xếp hạng kèm điểm thành phần và điểm đóng góp. | Đã xây dựng endpoint `POST /api/recommend` trên nền tảng FastAPI (Python 3.12). Dịch vụ kiểm tra hợp lệ dữ liệu đầu vào theo Pydantic schema và phân luồng đủ bốn trạng thái phản hồi: `success` (HTTP 200), `no_match` (HTTP 200 khi không có ứng viên thỏa lọc), `zero_weight` (HTTP 200 khi tổng trọng số bằng 0) và lỗi dữ liệu không hợp lệ `422 Unprocessable Entity`. | `backend/app/api/recommend.py`, `backend/app/schemas/search_request.py`, `recommendation.py`, `docs/design/api-contract.md`, 41 bài kiểm thử API tại `backend/tests/api/`, số liệu đo `TestClient` trong Chương 5 (trung bình 3,54 ms, tối đa 7,97 ms). | **Đã hiện thực, có giới hạn:** API xử lý đúng trong môi trường kiểm thử bộ nhớ và đã triển khai trên Render; tuy nhiên gói Render miễn phí có hiện tượng *cold start* khoảng 30–40 giây sau thời gian không hoạt động, và độ trễ truyền tải qua Internet chưa được đo đạc định lượng. |
| **(c) Giao diện demo bằng ReactJS:** Cho phép người học nhập nhu cầu, chọn mức ưu tiên và xem kết quả xếp hạng kèm giải thích. | Đã xây dựng giao diện Single Page Application bằng React 19 và Vite: màn hình nhập nhu cầu `SearchPage` (CN01) kèm bộ nạp nhanh 14 kịch bản; màn hình kết quả `ResultPage` (CN02) hiển thị Top-$k$ gia sư với thanh xếp chồng điểm đóng góp và lý do gợi ý; rail điều chỉnh mức ưu tiên (CN03) cập nhật thứ hạng trực tiếp trên màn hình kết quả. | `frontend/src/App.jsx`, `pages/SearchPage.jsx`, `pages/ResultPage.jsx`, `components/TutorCard.jsx`, `components/StackedBarScore.jsx`, `data/goalPresets.js`, `services/api.js`, triển khai trực tuyến trên Vercel. | **Đã hiện thực, có giới hạn:** Giao diện đáp ứng luồng minh họa thủ công ba chức năng CN01–CN03; tuy nhiên hệ thống dừng ở phạm vi demo tra cứu một chiều, chưa có kiểm thử tự động frontend, chưa có xác thực người dùng, đăng ký học hay đánh giá gia sư sau buổi học. |
| **(d) Đánh giá chất lượng xếp hạng qua kịch bản thực nghiệm:** Đánh giá chất lượng xếp hạng bằng các kịch bản có kỳ vọng xác định trước, minh họa ảnh hưởng của mức ưu tiên. | Đã số hóa và kiểm thử tự động 14 kịch bản tại Bảng 5.3, đạt tỷ lệ trùng khớp 14/14 (100%) với Top-3 kỳ vọng; phân tích các ca đặc thù (`KB04`, `KB09`, `KB02`, `KB12`); khảo sát độ nhạy trên 4 yếu tố tại Mục 5.2 (biên dung sai $\delta$, mốc bão hòa $E_{\max}$, biến động ngân sách và bộ mức ưu tiên tại Bảng 5.5–5.8), cho thấy tính ổn định thứ hạng và tác động điều hướng của trọng số. | `backend/tests/scenarios/scenarios.json`, `test_scenarios.py`, `test_sensitivity_muc_5_2.py` (27 bài kiểm thử), kết quả tại Chương 5 và tệp số liệu thô `docs/thesis/report/muc-5.2-ket-qua-tho.json`. | **Đã hiện thực, có giới hạn:** Top-3 kỳ vọng do nhóm tự xác định theo suy luận nghiệp vụ; do đó kết quả 14/14 chỉ chứng minh hệ thống tính đúng và nhất quán theo công thức đã chọn, chưa phản ánh mức độ hài lòng của người học thực tế. |

*Nguồn: Đối chiếu giữa Mục 1.4 đề cương đồ án với mã nguồn và kết quả thực nghiệm trong kho lưu trữ.*

### 6.1.2. Mở rộng ngoài đề cương: Hỗ trợ Mục tiêu học tập tại giao diện người dùng

Xuất phát từ góp ý chuyên môn của Giảng viên hướng dẫn (TS. Lê Anh Nhã Uyên) trong đợt báo cáo tiến độ giữa kỳ — gợi ý mở rộng nhu cầu người học theo bộ ba *(Môn học, Cấp lớp, Mục tiêu học tập)* thay vì chỉ dừng ở tên môn học — nhóm đã khảo sát khả năng mở rộng tại tài liệu thiết kế `docs/design/de-xuat-mo-rong-cap-lop-muc-tieu.md`. Hiện trạng triển khai cụ thể như sau:

- **Phương án 1 (Adaptive Weight Mapping) đã hiện thực ở tầng giao diện:** Tại màn hình nhập nhu cầu `SearchPage` (`frontend/src/pages/SearchPage.jsx` và `frontend/src/data/goalPresets.js`), hệ thống bổ sung ô lựa chọn “Mục tiêu học tập (gợi ý mức ưu tiên)” với ba thiết lập sẵn:
  1. *Không nêu mục tiêu:* giữ bộ mặc định cả năm tiêu chí ở mức Trung bình ($w = 2$).
  2. *Điểm cao / luyện thi chuyên – học sinh giỏi:* đặt Kinh nghiệm và Đánh giá ở mức Cao ($w = 3$), ba tiêu chí còn lại Trung bình ($w = 2$).
  3. *Đủ điểm đậu / lấy lại kiến thức căn bản:* đặt Học phí ở mức Cao ($w = 3$), bốn tiêu chí còn lại Trung bình ($w = 2$).
  Sau khi chọn preset, người học vẫn có thể chỉnh từng tiêu chí theo nhu cầu riêng (ô mục tiêu khi đó chuyển về hiển thị “Tùy chỉnh”).
- **Phương án 2 (bổ sung tiêu chí thứ sáu $s_6$ — *Goal Compatibility*) và trường Cấp lớp chưa hiện thực:** Hồ sơ gia sư hiện tại (`TutorProfile`) chỉ có 9 trường cơ bản, chưa có dữ liệu về cấp lớp nhận dạy, trình độ học vấn hay thế mạnh sư phạm.
- **Minh họa cơ chế trên 19 truy vấn:** Chạy thử ba bộ preset trên 19 truy vấn (14 kịch bản KB01–KB14 và 5 truy vấn tự đặt TQ1–TQ5) ghi nhận có 3/19 ca thay đổi thứ hạng ở vị trí 2–3 và 0/19 ca thay đổi hạng 1. Trong đó, `KB10` bị ghi đè mức ưu tiên gốc khi áp dụng `default`, còn trong 5 truy vấn tự đặt có 2/5 ca (`TQ1`, `TQ2`) đổi hạng 2–3 giữa các bộ preset. Các ca này được chọn sau khi thử 19 truy vấn nhằm minh họa cơ chế ánh xạ trọng số trên 16 hồ sơ, không dùng làm bằng chứng đánh giá chất lượng gợi ý. Đề xuất mở rộng hiện chờ phản hồi chính thức từ GVHD.

### 6.1.3. Môi trường triển khai thực tế

Hệ thống đã được triển khai trực tuyến trên hạ tầng đám mây theo `docs/deployment/deploy-vercel-render.md`:
- **Giao diện người dùng (Frontend):** triển khai trên Vercel tại `https://tutor-recommender.vercel.app`.
- **Dịch vụ khuyến nghị (Backend API):** triển khai trên Render tại `https://tutor-recommender-api.onrender.com`, kèm tài liệu tương tác Swagger UI tại `https://tutor-recommender-api.onrender.com/docs` và endpoint kiểm tra sức khỏe tại `/health`.

Kiểm chứng thực tế ngày 10/11/2026 ghi nhận cả hai địa chỉ (trang chủ frontend và `/health` của backend) đều phản hồi HTTP 200 OK. Nhóm lưu ý chỉ số thời gian xử lý bằng `TestClient` ở Chương 5 (trung bình 3,54 ms, lớn nhất 7,97 ms) là tốc độ xử lý trong bộ nhớ máy cục bộ, tách biệt với độ trễ truyền tải qua Internet và thời gian khởi động lại (*cold start* khoảng 30–40 giây) trên gói Render miễn phí.

---

## 6.2. Hạn chế và hướng phát triển

### 6.2.1. Tổng hợp các hạn chế kỹ thuật hiện hữu

Các hạn chế của hệ thống đã được phân tích chi tiết tại Mục 5.3 (Chương 5), tập trung vào bốn nhóm chính:
1. **Dữ liệu và kịch bản thử nghiệm quy mô nhỏ:** tập dữ liệu chỉ có 16 hồ sơ (14 hồ sơ mô phỏng, 2 hồ sơ thật có học phí và lịch rảnh ước tính); 14 kịch bản đánh giá do nhóm tự xây dựng nên chỉ kiểm chứng được tính đúng của công thức cài đặt.
2. **Tham số và cơ chế xử lý thiếu dữ liệu mang tính giả định:** các tham số $\delta = 0{,}5$, $E_{\max} = 8$, giá trị trung tính $0{,}5$ và trọng số $\{0, 1, 2, 3\}$ được thiết lập thủ công; bộ preset mục tiêu học tập cũng là giả định ban đầu.
3. **Chưa có dữ liệu tương tác và phản hồi người dùng thật:** hệ thống chưa ghi nhận hành vi chọn hồ sơ, lượt kết nối hay đánh giá sau buổi học để kiểm chứng mức độ hài lòng ngoài thực tế.
4. **Đơn giản hóa không gian tìm kiếm và thiếu đo đạc độ trễ mạng:** tiêu chí khu vực mới so khớp nhị phân theo tên quận/huyện quy ước; mỗi truy vấn mới hỗ trợ một môn học; độ trễ mạng đầu-cuối và *cold start* chưa được đo đạc có hệ thống.

### 6.2.2. Hướng phát triển theo đề cương đồ án

Để hoàn thiện giải pháp và nâng cao khả năng ứng dụng thực tế khi phát triển thành đồ án tốt nghiệp, đề cương định hướng ba bước tiếp theo:

1. **Tích hợp làm module khuyến nghị lõi cho nền tảng gia sư hoàn chỉnh:** kết nối module lọc – tính điểm với cơ sở dữ liệu quan hệ quản lý tài khoản người học, hồ sơ gia sư xác minh danh tính, đăng ký học thử, xếp lịch dạy và quản lý học phí.
2. **Nâng cấp mô hình Hybrid kết hợp Collaborative Filtering:** khi nền tảng tích lũy đủ người học và lịch sử tương tác, hệ thống có thể xây dựng ma trận tương tác người dùng – gia sư (*User-Item Interaction Matrix*) để kết hợp lọc cộng tác với lọc theo đặc trưng hồ sơ, vừa giữ khả năng xử lý *cold-start* cho gia sư mới vừa khai thác được xu hướng lựa chọn từ dữ liệu tương tác cộng đồng.
3. **Ứng dụng học máy xếp hạng (*Learning-to-Rank*):** thay thế bảng quy đổi trọng số thủ công bằng các mô hình học máy xếp hạng có giám sát, tự động học và tinh chỉnh trọng số dựa trên phản hồi ngầm định (lượt bấm, lưu hồ sơ) và phản hồi tường minh (điểm đánh giá sau khóa học).

### 6.2.3. Đề xuất mở rộng mô hình: Cấp lớp, Mục tiêu học tập và tiêu chí $s_6$

Tiếp nối phương án đã trình bày tại Mục 6.1.2 (theo `docs/design/de-xuat-mo-rong-cap-lop-muc-tieu.md`), hướng mở rộng dữ liệu và thuật toán gồm hai bước:
- Mở rộng cấu trúc `TutorProfile` để lưu trữ các trường cấp lớp nhận dạy (Tiểu học, THCS, THPT, Luyện thi), trình độ chuyên môn (Giảng viên, Thạc sĩ, Cử nhân, Sinh viên sư phạm) và thế mạnh sư phạm (luyện thi chuyên sâu, lấy lại căn bản, kiên nhẫn, nhiệt tình).
- Khi có đủ nguồn dữ liệu thật cho các trường trên, hiện thực Phương án 2 bằng cách bổ sung tiêu chí thành phần thứ sáu $s_6$ (*Goal Compatibility*) vào backend và cập nhật công thức Weighted Scoring (đề xuất này hiện chờ ý kiến chuyên môn của GVHD trước khi sửa hợp đồng API và bộ dữ liệu chuẩn).

---

## 6.3. Tự đánh giá và phân công công việc

### 6.3.1. Phân công công việc

**Bảng 6.1 - Phân công công việc và mức độ hoàn thành của các thành viên trong nhóm**

| STT | Thành viên | Mã sinh viên | Công việc phụ trách | Mức độ hoàn thành |
|:---:|:---|:---:|:---|:---:|
| 1 | **Lê Thị Bích Chuyền** | KHMT2411037 | **Scrum Master các Sprint 2, 4, 6 kiêm Developer:** Điều phối nghi thức Scrum ở các Sprint chẵn; phát triển giao diện ReactJS (Vite), kết nối API và kiểm thử trải nghiệm người dùng; tham gia thiết kế dữ liệu và kiểm thử hệ thống. | Hoàn thành |
| 2 | **Trần Nguyễn Đức** | KHMT2411011 | **Scrum Master các Sprint 1, 3, 5 kiêm Developer:** Điều phối nghi thức Scrum ở các Sprint lẻ và phụ trách quản lý nhánh/PR trên GitHub; phát triển lõi chấm điểm backend FastAPI, thuật toán xếp hạng và kiểm thử tự động. | Hoàn thành |
| 3 | **Cao Khánh Ngọc** *(Nhóm trưởng)* | KHMT2411025 | **Product Owner kiêm Developer:** Đại diện yêu cầu đề tài và làm việc với GVHD (TS. Lê Anh Nhã Uyên), quản lý và ưu tiên Product Backlog, nghiệm thu sản phẩm theo *Definition of Done*; tham gia phát triển tài liệu, thiết kế dữ liệu và kiểm thử. | Hoàn thành |

*Ghi chú: Phân công thực tế do nhóm xác nhận. Toàn bộ mã nguồn và tài liệu trên GitHub được hợp nhất qua tài khoản điều phối kỹ thuật, nên số lượng commit hay Pull Request không đại diện cho tỷ lệ đóng góp từng cá nhân. Mức độ hoàn thành trong Bảng 6.1 là tự đánh giá của nhóm; kết luận chính thức do GVHD và hội đồng đánh giá tại buổi bảo vệ đồ án.*  
*Nguồn: `docs/scrum/roles.md` và `docs/thesis/outline/muc-6.1-bang-6.1.md`.*

### 6.3.2. Tự đánh giá kết quả thực hiện

Nhóm tự đánh giá quá trình thực hiện đồ án dựa trên các bằng chứng kiểm chứng được trong kho lưu trữ mã nguồn:
- **Tính đầy đủ của sản phẩm:** Hoàn thành các thành phần phần mềm theo phạm vi đề cương: module thuật toán tính điểm backend, dịch vụ RESTful API, giao diện web frontend hai màn hình và hạ tầng triển khai trực tuyến.
- **Chất lượng kiểm thử và độ tin cậy:** Bộ kiểm thử tự động đạt 200/200 bài (tỷ lệ đạt 100%) bằng `pytest` với độ bao phủ 97% (340/351 câu lệnh theo `pytest --cov=app`); 14/14 kịch bản thực nghiệm khớp thứ tự kỳ vọng tại Bảng 5.3.
- **Tính toàn vẹn dữ liệu:** 16 hồ sơ gia sư trong `data/processed/tutors.json` và `data/processed/tutors.csv` đạt kiểm tra định dạng và khớp từng ô theo `scripts/validate_tutors.py` (Mục 4.2.4).
- **Kỷ luật kỹ thuật và tài liệu hóa:** Quá trình phát triển được tổ chức theo mô hình Scrum qua 6 Sprint; tài liệu kiến trúc, đặc tả thuật toán, hợp đồng API, biên bản sprint và báo cáo thực nghiệm được cập nhật đồng bộ cùng mã nguồn trên Git.

---

# PHỤ LỤC A. BỘ DỮ LIỆU MẪU

## 1. Mô tả nguồn gốc và quy trình xử lý dữ liệu gia sư

Nhóm đã khảo sát và thu thập thủ công 15 hồ sơ gia sư ban đầu từ hai nền tảng công khai tại Việt Nam là `giasudatviet.com` và `giasudantri.vn`. Sau bước xác minh sơ bộ, nhóm lọc được 11 hồ sơ hoạt động trên địa bàn Thành phố Hồ Chí Minh.

Khảo sát thực tế cho thấy cả hai nền tảng đều không công khai đồng thời học phí theo giờ, khung giờ rảnh cụ thể trong tuần và điểm đánh giá trung bình theo từng hồ sơ. Để phục vụ thử nghiệm của đồ án mà vẫn bảo vệ quyền riêng tư cá nhân:
- Nhóm giữ lại 2 hồ sơ thu thập thực tế (`GS-T06` và `GS-T07`) làm đại diện cho quy trình khảo sát từ nguồn công khai; môn dạy, danh sách khu vực và số năm kinh nghiệm là số liệu thực tế đã ẩn danh hóa.
- Học phí của hai hồ sơ này được nhóm ước tính trong khoảng 130.000–400.000 VNĐ/giờ dựa trên khảo sát thị trường tại `daythem.com` và nội suy theo số năm kinh nghiệm; khung giờ rảnh giả định theo các ca học phổ biến. Hai trường ước tính được đánh dấu `(*)` trong Bảng A.1; điểm đánh giá để trống (`null`) và nhận giá trị trung tính $0{,}5$ khi tính toán.
- 14 hồ sơ còn lại (`GS006`, `GS020`, `GS-G01` đến `GS-G12`) là dữ liệu mô phỏng do nhóm xây dựng nhằm bao phủ các ca biên, tình huống `no_match`, hình thức học trực tuyến và các trường hợp đồng điểm.
- **Lưu trữ dữ liệu thô:** Trong kho mã nguồn, thư mục `data/raw` chỉ chứa tệp `.gitkeep` giữ chỗ thư mục; các bản ghi thô thu thập thủ công không lưu lại trong kho lưu trữ.
- **Chuẩn hóa nhãn môn học hồ sơ `GS-G03`:** Nhãn môn học của `GS-G03` được sửa từ “Tiếng Anh” thành “Anh Văn” theo `data/README.md` (mục 4) để đồng bộ với danh mục môn học của toàn hệ thống.
- **Nhãn nguồn dữ liệu:** Trường `data_source` của `GS-T06` và `GS-T07` giữ nguyên giá trị `public_collected` trong các tệp dữ liệu của hệ thống (`data/processed/tutors.json`, `data/processed/tutors.csv`, `frontend/src/data/tutorsCatalog.js`) theo quyết định thống nhất của nhóm.

## 2. Danh sách 16 hồ sơ gia sư mẫu

Bảng A.1 liệt kê đầy đủ 16 hồ sơ theo đúng thứ tự mã, kèm nhãn nguồn dữ liệu và dấu `(*)` cho hai trường ước tính của `GS-T06`, `GS-T07`.

**Bảng A.1 - Danh sách 16 hồ sơ gia sư mẫu**

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

*Ghi chú: (*) Học phí và lịch rảnh của `GS-T06` và `GS-T07` là số liệu ước tính của nhóm; môn dạy, khu vực và số năm kinh nghiệm là dữ liệu thu thập thực tế đã ẩn danh hóa. Điểm đánh giá để trống nhận giá trị trung tính $0{,}5$.*  
*Nguồn: `data/processed/tutors.json` và `data/processed/tutors.csv`.*

## 3. Danh mục khu vực quy ước trong hệ thống

Tập hợp danh mục khu vực địa lý được trích xuất từ `data/processed/tutors.json` và đối chiếu với danh sách `DISTRICT_OPTIONS` trong `frontend/src/services/api.js`:
- **Danh sách 16 quận/huyện quy ước:** Bình Chánh, Bình Thạnh, Gò Vấp, Nhà Bè, Phú Nhuận, Quận 1, Quận 2, Quận 3, Quận 7, Quận 8, Quận 9, Quận 10, Quận 11, Tân Bình, Tân Phú, Thủ Đức.
- **Đối chiếu:** Hai tập hợp trong `data/processed/tutors.json` và `DISTRICT_OPTIONS` trùng khớp 16/16 khu vực.
- **Khác biệt so với thực tế hành chính hiện hành:** Danh mục quy ước vẫn tách riêng “Quận 2”, “Quận 9” và “Thủ Đức” (các đơn vị này đã sáp nhập thành Thành phố Thủ Đức từ 01/01/2021) và chưa bao phủ đủ 22 đơn vị cấp huyện của Thành phố Hồ Chí Minh (thiếu Quận 4, Quận 5, Quận 6, Quận 12, Bình Tân, Hóc Môn, Củ Chi, Cần Giờ). Đây là danh mục quy ước cố định chỉ dùng cho phạm vi thử nghiệm của đồ án.

## 4. Kết quả kiểm tra tính toàn vẹn của bộ dữ liệu

Tính toàn vẹn kiểu dữ liệu và sự khớp nhau từng ô giữa tệp JSON và CSV của 16 hồ sơ được xác minh qua lệnh:

```powershell
python scripts/validate_tutors.py
```

Kết quả thực thi:

```text
ĐẠT: 16 bản ghi (2 public_collected, 14 simulated); id duy nhất; enum hợp lệ;
     đủ 9 trường; không có thông tin liên hệ; JSON và CSV khớp nhau từng ô.
```

---

# PHỤ LỤC B. MODULE TÍNH ĐIỂM VÀ XẾP HẠNG

Bảng B.1 liệt kê danh mục tệp mã nguồn, lớp và hàm chính hiện thực logic tính điểm và điều phối gợi ý trong gói `backend/app/`, đối chiếu với các bước xử lý tại Mục 3.6.

**Bảng B.1 - Danh mục tệp mã nguồn và hàm nghiệp vụ trong module gợi ý gia sư**

| STT | Tệp mã nguồn | Lớp / Hàm chính | Vai trò kỹ thuật | Bước tương ứng trong Mục 3.6 |
|:---:|:---|:---|:---|:---|
| 1 | `backend/app/core/config.py` | Hằng số: `DELTA = 0.5`, `E_MAX = 8`, `RATING_DEFAULT = 0.5`, `PRIORITY_WEIGHTS`, `CRITERIA_KEYS` | Quản lý tham số thuật toán khởi tạo, bảng quy đổi mức ưu tiên sang trọng số nguyên và các khóa tiêu chí dùng chung. | Khởi tạo tham số và bảng quy đổi trọng số (Mục 3.6, Bảng 3.5, Bảng 3.6) |
| 2 | `backend/app/data/repository.py` | Lớp `TutorRepository` (`get_all()`, `get_by_id()`), `TutorDataError` | Đọc dữ liệu từ `data/processed/tutors.json`, kiểm tra toàn vẹn và cung cấp danh sách hồ sơ cho pipeline. | Cung cấp dữ liệu hồ sơ gia sư đầu vào |
| 3 | `backend/app/schemas/tutor.py` | Lớp Pydantic `TutorProfile` | Định nghĩa cấu trúc và kiểm tra hợp lệ kiểu dữ liệu cho 9 trường hồ sơ gia sư (`extra="forbid"`). | Cấu trúc dữ liệu đặc trưng hồ sơ gia sư |
| 4 | `backend/app/schemas/search_request.py` | Lớp Pydantic `SearchRequest`, hàm `default_priorities()` | Định nghĩa cấu trúc truy vấn tìm kiếm của người học (7 trường), xác thực dữ liệu đầu vào và gán mức ưu tiên mặc định. | Bước 1: Kiểm tra và chuẩn hóa yêu cầu tìm kiếm đầu vào |
| 5 | `backend/app/scoring/filters.py` | Hàm `filter_mandatory()`, `_matches_subject()`, `_matches_mode()`, `_matches_availability()` | Lọc danh sách gia sư theo các ràng buộc cứng: môn dạy, hình thức dạy/học và điều kiện trùng lịch tối thiểu ($\lvert L \cap T \rvert \ge 1$). | Bước 2: Lọc điều kiện bắt buộc (Bảng 3.2) |
| 6 | `backend/app/scoring/weights.py` | Lớp `EffectiveWeights`, hàm `compute_effective_weights()`, `priority_to_weight()`, `_applicable_criteria()` | Xác định số tiêu chí ưu tiên đang áp dụng ($n$) và tính bộ trọng số hiệu dụng $w_i$; vô hiệu hóa ($w_i = 0$) các tiêu chí không áp dụng. | Xác định tiêu chí áp dụng và tính trọng số hiệu dụng |
| 7 | `backend/app/scoring/eligibility.py` | Hàm `filter_eligible_candidates()`, `check_tutor_eligibility()`, `count_available_criteria()`, `get_min_required_criteria()` | Đếm số tiêu chí ưu tiên có dữ liệu của gia sư và so khớp bảng ngưỡng tối thiểu theo $n$; loại bỏ hồ sơ thiếu dữ liệu. | Điều kiện đủ dữ liệu để xếp hạng (giữa Bước 2 và Bước 3) |
| 8 | `backend/app/scoring/criteria.py` | `score_fee()`, `score_location()`, `score_experience()`, `score_rating()`, `score_schedule()` | Hiện thực 5 công thức tính điểm thành phần $s_i \in [0, 1]$ cho học phí, khu vực, kinh nghiệm, đánh giá và lịch rảnh. | Bước 3: Tính điểm thành phần $s_i$ (Bảng 3.6) |
| 9 | `backend/app/scoring/ranker.py` | `score_and_rank()`, `_compute_single_criterion_score()`, `build_reason()`, `build_notes()` | Tổng hợp điểm Weighted Scoring $S = \sum (w_i \cdot s_i) / \sum w_i$, sắp xếp giảm dần, phá hòa tất định theo `tutor_id`, trích xuất điểm đóng góp và lý do gợi ý. | Bước 4: Tổng hợp điểm Weighted Scoring và xếp hạng |
| 10 | `backend/app/schemas/recommendation.py` | `RankedTutor`, `RecommendationSuccessResponse`, `NoMatchResponse`, `ZeroWeightResponse` | Định nghĩa cấu trúc phản hồi JSON cho các trạng thái `success`, `no_match` và `zero_weight`. | Định dạng cấu trúc dữ liệu phản hồi |
| 11 | `backend/app/api/recommend.py` | Endpoint `recommend_tutors()`, phụ trợ `get_tutor_repository()` | Tiếp nhận yêu cầu `POST /api/recommend`, điều phối pipeline và trả kết quả chuẩn hóa theo hợp đồng API. | Điều phối toàn bộ pipeline qua dịch vụ API FastAPI |

*Nguồn: Mã nguồn ứng dụng backend trong `backend/app/`.*

---

# PHỤ LỤC C. DANH MỤC HÌNH ẢNH GIAO DIỆN DEMO

## 1. Danh mục hình ảnh lưu trữ theo giai đoạn

Kho mã nguồn hiện lưu 5 tệp ảnh chụp từ đợt báo cáo giữa kỳ tại `docs/thesis/assets/midterm/` (Bảng C.1) và 9 hình vẽ, ảnh chụp chính thức tại `docs/thesis/figures/` dùng trực tiếp trong Chương 3 (Hình 3.1–3.5) và Chương 4 (Hình 4.1–4.4).

**Bảng C.1 - Danh mục hình ảnh giao diện demo hiện có trong kho lưu trữ**

| STT | Tệp hình ảnh | Nội dung thể hiện | Trạng thái đối chiếu với bản cuối |
|:---:|:---|:---|:---|
| 1 | `docs/thesis/assets/midterm/hinh-1-cn01-nhap-nhu-cau.png` | Giao diện màn hình nhập nhu cầu và thanh nạp nhanh 14 kịch bản ở đợt giữa kỳ (CN01). | Đã thay bằng Hình 4.1 (bản cuối bổ sung ô “Mục tiêu học tập”). |
| 2 | `docs/thesis/assets/midterm/hinh-2-cn02-ket-qua-top3.png` | Màn hình kết quả gợi ý Top-3, thanh xếp chồng điểm đóng góp và lý do gợi ý ở kịch bản KB01 (CN02). | Đã thay bằng Hình 4.2 để đồng bộ giao diện cuối kỳ. |
| 3 | `docs/thesis/assets/midterm/hinh-3-cn03-dieu-chinh-uu-tien.png` | Bảng điều khiển tinh chỉnh mức ưu tiên trên màn hình kết quả (CN03); nhãn mức ưu tiên 0 hiển thị là “Bỏ qua” ($w = 0$). | Đã thay bằng Hình 4.3 (bổ sung nhãn rõ ràng và trường hợp đối chứng mới). |
| 4 | `docs/thesis/assets/midterm/hinh-4-swagger-api-recommend.png` | Giao diện tài liệu tương tác OpenAPI (Swagger UI) của endpoint `POST /api/recommend`. | Minh họa giao diện Swagger UI; báo cáo dẫn trực tiếp URL `/docs` tại Mục 4.4.1, Mục 4.6.3 và Mục 6.1.3. |
| 5 | `docs/thesis/assets/midterm/hinh-5-pytest-190-passed.png` | Ảnh chụp terminal kiểm thử ở mốc 190 bài đạt tại đợt báo cáo giữa kỳ. | Lỗi thời (bộ kiểm thử cuối kỳ đạt 200 bài, tổng hợp bằng Bảng 5.1). |

*Nguồn: Thư mục `docs/thesis/assets/midterm/` trong kho lưu trữ mã nguồn.*

## 2. Tổng hợp hình ảnh giao diện chính thức trong báo cáo

Bốn ảnh giao diện phiên bản nghiệm thu cuối cùng đã được chụp và chèn tại Chương 4:
1. **Hình 4.1 (CN01):** Màn hình nhập nhu cầu hiển thị đầy đủ ô “Mục tiêu học tập (gợi ý mức ưu tiên)” với ba preset (“Không nêu mục tiêu”, “Điểm cao / luyện thi chuyên – học sinh giỏi”, “Đủ điểm đậu / lấy lại kiến thức căn bản”).
2. **Hình 4.2 (CN02):** Màn hình kết quả Top-3 kịch bản KB01 kèm thanh xếp chồng phân rã đóng góp ($w_i \cdot s_i / \sum w_i$) và chuỗi lý do gợi ý.
3. **Hình 4.3 (CN03):** Màn hình điều chỉnh mức ưu tiên trực tiếp với nhãn “Bỏ qua ($w = 0$)” làm thay đổi thứ hạng.
4. **Hình 4.4 (Trạng thái `zero_weight`):** Màn hình kết quả khi tổng trọng số bằng $0$ ($\sum w_i = 0$), hiển thị cảnh báo và nút khôi phục trọng số mặc định.

Hai hạng mục tài liệu bổ trợ là Swagger UI và terminal kiểm thử 200 bài đạt (lệnh `pytest -q` và `pytest --cov=app`, độ bao phủ 97%) được trình bày qua liên kết triển khai tại Mục 6.1.3 và Bảng 5.1 thay vì chèn thêm ảnh chụp.

---

# PHỤ LỤC D. KỊCH BẢN KIỂM THỬ THỰC NGHIỆM

## 1. Bảng yêu cầu đầy đủ của 14 kịch bản thực nghiệm

Bảng D.1 đặc tả toàn bộ tham số đầu vào và danh sách Top-3 kỳ vọng của 14 kịch bản tìm kiếm gia sư, trích xuất trực tiếp từ tệp `backend/tests/scenarios/scenarios.json`.

**Bảng D.1 - Yêu cầu đầy đủ của 14 kịch bản thực nghiệm**

| Mã KB | Môn | Hình thức | Khu vực | Ngân sách (VNĐ/giờ) | Khung giờ | Mức ưu tiên khác mặc định | Top-3 kỳ vọng |
|:---:|:---|:---|:---|:---:|:---|:---|:---|
| KB01 | Toán | Trực tiếp | Bình Thạnh | 200.000 | Không nhập | Mặc định (đều $w = 2$) | GS-G01, GS-G10, GS-T06 |
| KB02 | Anh Văn | Trực tiếp | Quận 2 | 220.000 | Không nhập | Mặc định (đều $w = 2$) | GS-G11, GS-G12, GS-T07 |
| KB03 | Anh Văn | Trực tiếp | Thủ Đức | 220.000 | Không nhập | Mặc định (đều $w = 2$) | GS-G12, GS-G11, GS-T07 |
| KB04 | Lý | Trực tuyến | Không nhập | 200.000 | T2-tối, T4-tối | Mặc định (đều $w = 2$) | GS006, GS020 |
| KB05 | Tiếng Trung | Bất kỳ (`any`) | Không nhập | Không nhập | Không nhập | Mặc định (đều $w = 2$) | Không có (0 kết quả) |
| KB06 | Văn | Trực tiếp | Quận 1 | 180.000 | Không nhập | Mặc định (đều $w = 2$) | GS-G04 |
| KB07 | Sinh | Bất kỳ (`any`) | Thủ Đức | 200.000 | Không nhập | Mặc định (đều $w = 2$) | GS-G05 |
| KB08 | Tin học | Trực tuyến | Không nhập | 250.000 | T2-tối, T6-tối | Mặc định (đều $w = 2$) | GS-G07 |
| KB09 | Tiếng Nhật | Bất kỳ (`any`) | Phú Nhuận | 280.000 | Không nhập | Mặc định (đều $w = 2$) | GS-G08 |
| KB10 | Toán | Trực tiếp | Quận 7 | Không nhập | Không nhập | Kinh nghiệm: Cao ($w = 3$) | GS-G10, GS-G01, GS-G09 |
| KB11 | Hóa | Trực tiếp | Quận 10 | 220.000 | Không nhập | Mặc định (đều $w = 2$) | GS-G06, GS-T06 |
| KB12 | Anh Văn | Trực tiếp | Bình Chánh | 200.000 | Không nhập | Mặc định (đều $w = 2$) | GS-T07, GS-G11, GS-G12 |
| KB13 | Toán | Bất kỳ (`any`) | Không nhập | 150.000 | Không nhập | Mặc định (đều $w = 2$) | GS-G10, GS-G01, GS-T06 |
| KB14 | Anh Văn | Trực tuyến | Không nhập | Không nhập | Không nhập | Mặc định (đều $w = 2$) | GS-G03 |

*Ghi chú: Cột “Khung giờ” và “Khu vực” ghi nhận “Không nhập” khi người học không điền tiêu chí tùy chọn tương ứng; mức ưu tiên mặc định của cả 5 tiêu chí là Trung bình ($w = 2$). Kết quả Top-3 kỳ vọng được xác lập dựa trên suy luận logic nghiệp vụ để đối chiếu với thuật toán.*  
*Nguồn: `backend/tests/scenarios/scenarios.json`.*

## 2. Dẫn chiếu kết quả thực nghiệm và kiểm thử ca biên

Nhằm tránh trùng lặp số liệu trong báo cáo:
- **Kết quả xếp hạng thực tế đối với 14 kịch bản:** Kết quả chạy qua pipeline xếp hạng, tỷ lệ trùng khớp (14/14 đạt 100%) và phân tích các ca đặc thù (`KB04`, `KB09`, `KB02`, `KB12`) được trình bày tại **Bảng 5.3** trong Chương 5.
- **Kết quả kiểm thử ca biên của 5 hàm điểm:** Bảng ma trận kiểm thử các giá trị biên và tính đơn điệu của các hàm điểm thành phần được trình bày tại **Bảng 5.2** trong Chương 5.
