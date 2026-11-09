> [!NOTE]
> **Đề xuất, nhóm xác nhận**

# Đề xuất mở rộng mô hình: tổ hợp Cấp lớp và Mục tiêu học tập

> ĐỀ XUẤT, CHƯA HIỆN THỰC, CHƯA CÓ PHẢN HỒI CỦA GVHD

**Phạm vi:** tài liệu thiết kế để thảo luận với GVHD; không thay đổi mã nguồn, dữ liệu, 14 kịch bản hay bộ kiểm thử hiện có. Tài liệu dự kiến được trích vào Mục 6.2 của Chương 6 và dùng để chuẩn bị trả lời phản biện.

---

## 1. Bối cảnh và giới hạn dữ liệu hiện tại

### 1.1. Chỉ dẫn của GVHD

Báo cáo giữa kỳ ghi nhận chỉ dẫn của GVHD: nhu cầu của người học không nên dừng ở tên môn học, mà là tổ hợp ba chiều **(Môn học, Cấp lớp, Mục tiêu học tập)**. Cùng một môn học, hai người học có mục tiêu khác nhau sẽ cần những hồ sơ gia sư khác nhau. Báo cáo nêu hai ví dụ:

- **Học sinh A — Toán lớp 8, mục tiêu điểm 10 cuối kỳ hoặc luyện thi chuyên/học sinh giỏi:** ưu tiên gia sư có trình độ chuyên môn cao (giảng viên, thạc sĩ, thủ khoa), nhiều năm kinh nghiệm, đánh giá xuất sắc; chấp nhận học phí cao.
- **Học sinh B — Toán lớp 9, mục tiêu vừa đủ điểm đậu hoặc lấy lại kiến thức căn bản:** ưu tiên gia sư là sinh viên khá/giỏi, nhiệt tình, kiên nhẫn, học phí vừa phải và ở gần nhà.

Hai ví dụ cho thấy cùng một tiêu chí có thể có mức ưu tiên rất khác nhau tùy mục tiêu. Báo cáo đề xuất hai hướng kỹ thuật: (1) *Adaptive Weight Mapping* — mục tiêu học tập gợi ý bộ mức ưu tiên khởi tạo cho 5 tiêu chí hiện có, người học vẫn tinh chỉnh ở CN03; (2) bổ sung tiêu chí thành phần thứ 6 `s_6` *Goal Compatibility*. Đến thời điểm soạn tài liệu này, nhóm **chưa có phản hồi của GVHD** về việc chọn hướng nào.

### 1.2. Giới hạn dữ liệu và mô hình hiện tại

Đối chiếu trực tiếp với mã nguồn và dữ liệu trong repo:

- `backend/app/schemas/tutor.py`: `TutorProfile` có đúng **9 trường** — `tutor_id`, `subjects`, `districts`, `hourly_fee_vnd`, `years_experience`, `teaching_mode`, `availability`, `avg_rating`, `data_source` — và đặt `extra="forbid"`. **Không có** trường cấp lớp, trình độ học vấn (giảng viên/thạc sĩ/cử nhân/sinh viên) hay thế mạnh sư phạm (kiên nhẫn, nhiệt tình, chuyên sâu học thuật).
- `data/processed/tutors.json` và `data/processed/tutors.csv`: **16 hồ sơ** (2 `public_collected`, 14 `simulated`), chỉ chứa 9 trường nêu trên.
- `backend/app/schemas/search_request.py`: `SearchRequest` có 7 trường — `subject`, `learning_mode`, `preferred_district`, `max_budget_vnd`, `time_slots`, `priorities`, `top_k` — và cũng đặt `extra="forbid"`. **Không có** trường cấp lớp hay mục tiêu học tập.
- `backend/app/core/config.py`: `CRITERIA_KEYS = ("fee", "district", "experience", "rating", "availability")` — đúng **5 tiêu chí**; bốn mức ưu tiên `none/low/medium/high` quy đổi thành `0/1/2/3`; mặc định `medium`.
- `docs/design/api-contract.md`: phản hồi `criteria_scores` và `contributions` **luôn đủ 5 khóa**; tiêu chí không áp dụng hoặc có `w = 0` nhận giá trị `null`.

Hệ quả: các mô tả như “giảng viên/thạc sĩ/thủ khoa” hay “sinh viên khá/giỏi” **không thể so khớp trực tiếp** vì hồ sơ gia sư không có dữ liệu tương ứng. Với dữ liệu hiện tại, nhóm chỉ có thể **xấp xỉ gián tiếp** qua `years_experience`, `avg_rating`, `hourly_fee_vnd` và `districts`; cách xấp xỉ này phải được ghi rõ là giả định, không được trình bày như dữ liệu thật. Cấp lớp của người học cũng chưa có trường để lưu, nên chưa thể dùng để lọc hay chấm điểm.

---

## 2. Phương án 1 — Adaptive Weight Mapping

### 2.1. Cơ chế đề xuất

Mục tiêu học tập **chỉ sinh ra bộ mức ưu tiên khởi tạo ở tầng giao diện**. API, hợp đồng dữ liệu và lõi chấm điểm giữ nguyên:

1. Người học chọn mục tiêu ở CN01 (hoặc một bộ chọn mục tiêu đặt cạnh phần mức ưu tiên).
2. Giao diện tra bảng ánh xạ ở Mục 2.2 và đặt 5 mức ưu tiên tương ứng.
3. Người học vẫn nhìn thấy và chỉnh được từng mức ưu tiên như CN03 hiện tại.
4. `buildRecommendationPayload` tiếp tục gửi đúng 5 khóa `fee`, `district`, `experience`, `rating`, `availability`; **không gửi thêm trường mục tiêu** vì `SearchRequest` đang `extra="forbid"`.

Các tệp giao diện dự kiến chạm tới (đã kiểm tra tồn tại):

- `frontend/src/App.jsx`: thêm `learningGoal` vào trạng thái `searchForm`; đặt lại về “Không nêu mục tiêu” khi nạp kịch bản để không đè lên bộ ưu tiên của 14 kịch bản.
- `frontend/src/services/api.js`: thêm hằng số danh sách mục tiêu và bảng ánh xạ mục tiêu → mức ưu tiên; giữ nguyên `CRITERIA_LIST`, `DEFAULT_PRIORITIES` và `buildRecommendationPayload`.
- `frontend/src/pages/SearchPage.jsx`: thêm bộ chọn mục tiêu; khi đổi mục tiêu thì cập nhật 5 mức ưu tiên; khi người học tự đổi một mức ưu tiên thì giữ nguyên lựa chọn thủ công đó.
- `frontend/src/pages/ResultPage.jsx`: hiển thị mục tiêu đã chọn và ghi chú “mức ưu tiên chỉ là gợi ý, có thể chỉnh ở CN03”.

Không cần sửa backend, không cần endpoint mới, không cần thêm trường vào request. Khi nạp kịch bản KB01–KB14, giao diện giữ nguyên `priorities` của kịch bản và đặt mục tiêu về “Không nêu”; nhờ vậy 14 kịch bản không bị ảnh hưởng.

### 2.2. Bảng ánh xạ Mục tiêu → mức ưu tiên

Mỗi ô ghi kèm thẻ nguồn. `[báo cáo giữa kỳ]` là giá trị báo cáo đã nêu; `[giả định nhóm, chờ GVHD xác nhận]` là giá trị nhóm tự đề xuất, **chưa được GVHD xác nhận**; `[Bảng 3.5 — mặc định hiện tại]` là bộ mặc định đang chạy trong hệ thống.

| Mục tiêu | Học phí | Khu vực | Kinh nghiệm | Đánh giá | Lịch rảnh |
|:---|:---|:---|:---|:---|:---|
| **Điểm cao / luyện thi chuyên – học sinh giỏi** (học sinh A) | Trung bình<br>`[giả định nhóm, chờ GVHD xác nhận]` | Trung bình<br>`[giả định nhóm, chờ GVHD xác nhận]` | **Cao**<br>`[báo cáo giữa kỳ]` | **Cao**<br>`[báo cáo giữa kỳ]` | Trung bình<br>`[giả định nhóm, chờ GVHD xác nhận]` |
| **Đủ điểm đậu / lấy lại căn bản** (học sinh B) | **Cao**<br>`[báo cáo giữa kỳ]` | Trung bình<br>`[giả định nhóm, chờ GVHD xác nhận]` | Trung bình<br>`[giả định nhóm, chờ GVHD xác nhận]` | Trung bình<br>`[giả định nhóm, chờ GVHD xác nhận]` | Trung bình<br>`[giả định nhóm, chờ GVHD xác nhận]` |
| **Không nêu mục tiêu** | Trung bình<br>`[Bảng 3.5 — mặc định hiện tại]` | Trung bình<br>`[Bảng 3.5 — mặc định hiện tại]` | Trung bình<br>`[Bảng 3.5 — mặc định hiện tại]` | Trung bình<br>`[Bảng 3.5 — mặc định hiện tại]` | Trung bình<br>`[Bảng 3.5 — mặc định hiện tại]` |

**Gợi ý bổ sung của nhóm (ghi riêng, chưa đưa vào bảng chính):**

- Với học sinh A, vì báo cáo nêu A **chấp nhận học phí cao**, nhóm đề xuất đặt Học phí = **Thấp** thay vì Trung bình để tránh đẩy học phí lên ngang các tiêu chí chuyên môn. Đây là `[giả định nhóm, chờ GVHD xác nhận]`.
- Với học sinh B, vì báo cáo nêu B ưu tiên gia sư **ở gần nhà**, nhóm đề xuất đặt Khu vực = **Cao** thay vì Trung bình. Đây là `[giả định nhóm, chờ GVHD xác nhận]`.
- Các ô còn lại giữ Trung bình vì báo cáo không nêu mức cụ thể; nhóm không tự suy ra giá trị khác khi chưa có căn cứ.

### 2.3. Ví dụ minh họa trên KB01

Chạy từ thư mục `backend/`, dùng script tạm đặt ngoài repo; kết quả ghi ra `%TEMP%\kb01-adaptive-weight-example.json` bằng UTF-8, stdout chỉ in ký tự ASCII:

```powershell
# Từ thư mục backend/ của worktree
$env:PYTHONDONTWRITEBYTECODE = "1"
$env:PYTHONIOENCODING = "utf-8"
& "<đường-dẫn-venv>\Scripts\python.exe" "$env:TEMP\opencode\kb01_adaptive_example.py"
```

Script đọc `KB01` từ `backend/tests/scenarios/scenarios.json`, gọi `POST /api/recommend` qua `TestClient` với ba bộ ưu tiên: mặc định (5 × Trung bình), học sinh A (Kinh nghiệm Cao, Đánh giá Cao, còn lại Trung bình), học sinh B (Học phí Cao, còn lại Trung bình). Kết quả thật:

```text
WROTE C:\Users\LENOVO\AppData\Local\Temp\kb01-adaptive-weight-example.json
default -> GS-G01=0.938, GS-G10=0.745, GS-T06=0.625
student_a -> GS-G01=0.925, GS-G10=0.794, GS-T06=0.650
student_b -> GS-G01=0.944, GS-G10=0.773, GS-T06=0.556
```

| Bộ ưu tiên | Hạng 1 | Hạng 2 | Hạng 3 |
|:---|:---|:---|:---|
| Mặc định (5 × Trung bình) | GS-G01 — 0,938 | GS-G10 — 0,745 | GS-T06 — 0,625 |
| Học sinh A (Kinh nghiệm Cao, Đánh giá Cao) | GS-G01 — 0,925 | GS-G10 — 0,794 | GS-T06 — 0,650 |
| Học sinh B (Học phí Cao) | GS-G01 — 0,944 | GS-G10 — 0,773 | GS-T06 — 0,556 |

Với KB01, **thứ hạng Top-3 không đổi**; chỉ điểm tổng và mức đóng góp thay đổi. Ví dụ ở bộ ưu tiên A, đóng góp của GS-G01 là Học phí 0,200; Khu vực 0,200; Kinh nghiệm 0,225; Đánh giá 0,300; Lịch rảnh `null` (KB01 không có `time_slots`, nên tiêu chí này không áp dụng). Đây chỉ là **minh họa cơ chế trên 16 hồ sơ**, không phải bằng chứng chất lượng gợi ý và không chứng minh rằng mục tiêu học tập luôn làm đổi thứ hạng.

### 2.4. Tác động

- **Không đổi hợp đồng API:** request vẫn 7 trường, `priorities` vẫn đúng 5 khóa; response vẫn đủ 5 khóa `criteria_scores` và `contributions`.
- **Không đổi `scoring-spec.md`:** công thức $S = \sum w_i s_i / \sum w_i$, bảng quy đổi $0/1/2/3$ và các ngưỡng giữ nguyên.
- **Không đổi dữ liệu:** 16 hồ sơ, 14 kịch bản và `tutors.json`/`tutors.csv` giữ nguyên.
- **Không đổi các test hiện có:** backend vẫn nhận đúng 5 khóa; frontend chỉ thay cách khởi tạo `priorities`. Cần chạy lại kiểm thử để xác nhận, không được chỉ suy luận.
- **Cấp lớp KHÔNG tham gia lọc hay chấm điểm.** Hồ sơ gia sư không có trường cấp lớp, nên hệ thống không thể lọc “gia sư dạy lớp 8” hay “lớp 9”. Tương tự, trình độ học vấn và thế mạnh sư phạm cũng không tham gia trực tiếp; chúng chỉ được xấp xỉ gián tiếp qua kinh nghiệm, đánh giá, học phí và khu vực.
- **Đây là gợi ý ở tầng giao diện**, không phải quy tắc bắt buộc của hệ thống. Người dùng gọi API trực tiếp vẫn có thể gửi bất kỳ bộ ưu tiên hợp lệ nào; điều này là chấp nhận được vì mục tiêu chỉ nhằm giảm thao tác cho người dùng, không nhằm thay đổi lõi chấm điểm.

---

## 3. Phương án 2 — Bổ sung tiêu chí `s_6` Goal Compatibility

Phương án 2 thêm một tiêu chí thành phần thứ 6 vào công thức tổng hợp. Để `s_6` có ý nghĩa, cần đồng thời có: (a) mục tiêu học tập của người học trong `SearchRequest`; (b) thuộc tính của gia sư để so khớp mục tiêu (trình độ, cấp lớp, thế mạnh sư phạm); (c) dữ liệu cho 16 hồ sơ. Hiện repo **chưa có (b) và (c)**. Nếu chỉ tính `s_6` từ 5 trường hiện có thì `s_6` thực chất là một cách tổ hợp lại các tiêu chí cũ, trùng với Phương án 1 nhưng phức tạp hơn.

Các nhóm tệp và hạng mục phải đổi nếu chọn Phương án 2 (mọi đường dẫn đã kiểm tra tồn tại):

### 3.1. Dữ liệu và schema — 7 tệp

- `data/processed/tutors.json`: thêm trường cấp lớp/trình độ/thế mạnh sư phạm cho 16 hồ sơ. Hiện **không có nguồn dữ liệu** cho các trường này; không được tự bịa.
- `data/processed/tutors.csv`: thêm cột tương ứng và giữ khớp từng ô với JSON.
- `backend/app/schemas/tutor.py`: mở rộng `TutorProfile`; vì đang `extra="forbid"`, dữ liệu cũ sẽ không còn hợp lệ cho đến khi cập nhật đồng bộ.
- `backend/app/schemas/search_request.py`: thêm trường mục tiêu học tập (và cấp lớp nếu dùng); cập nhật validator `priorities` cho khóa thứ 6; vì `extra="forbid"`, client cũ gửi trường lạ sẽ bị từ chối.
- `backend/app/schemas/recommendation.py`: cập nhật mô tả “5 tiêu chí” thành 6; kiểu `dict[str, ...]` không cần đổi cấu trúc.
- `scripts/validate_tutors.py`: thêm trường vào `FIELDS`, kiểm tra kiểu/enum và kiểm tra JSON–CSV khớp nhau.
- `docs/design/data-dictionary.md`: bổ sung định nghĩa trường mới và quy ước giá trị.

### 3.2. Lõi chấm điểm — 5 tệp

- `backend/app/core/config.py`: thêm `s_6` vào `CRITERIA_KEYS`; quyết định mức ưu tiên mặc định và cách quy đổi của tiêu chí mới.
- `backend/app/scoring/criteria.py`: thêm hàm tính `s_6` và quy tắc chuẩn hóa về $[0, 1]$.
- `backend/app/scoring/weights.py`: duyệt 6 khóa; xử lý trường hợp `s_6` không áp dụng hoặc dữ liệu thiếu.
- `backend/app/scoring/eligibility.py`: mở rộng bảng ngưỡng `MIN_DATA_THRESHOLD` cho `n = 6`; đếm dữ liệu của tiêu chí mới; cập nhật ghi chú “không đủ dữ liệu để xếp hạng”.
- `backend/app/scoring/ranker.py`: tính `s_6`, đưa vào tổng điểm và `contributions`; cập nhật thứ tự khóa và câu giải thích.

### 3.3. Hợp đồng và tài liệu — 2 tệp

- `docs/design/api-contract.md`: thêm khóa `s_6` vào `priorities` và response; sửa cam kết “luôn đủ 5 khóa” thành 6; cập nhật ví dụ và các trường hợp lỗi.
- `docs/design/scoring-spec.md`: thêm hàng `s_6` vào Bảng 3.6, sửa công thức/tổng trọng số và bảng ngưỡng dữ liệu tối thiểu.

### 3.4. Kiểm thử — 6 tệp

- `backend/tests/unit/test_config.py`: cập nhật kỳ vọng `CRITERIA_KEYS` (6 khóa).
- `backend/tests/api/test_recommend_api.py`: rà lại các khẳng định về khóa `criteria_scores`/`contributions` (test đang so với hằng `CRITERIA_KEYS`) và cập nhật các kỳ vọng thứ hạng/điểm có thể đổi.
- `backend/tests/unit/test_ranker.py`: cập nhật điểm, đóng góp và thứ tự khóa.
- `backend/tests/unit/test_eligibility.py`: cập nhật ngưỡng cho `n = 6`.
- `backend/tests/unit/test_weights.py`: cập nhật vòng lặp và tổng trọng số.
- `backend/tests/scenarios/scenarios.json`: **khóa bất biến, không được sửa**. Nếu `s_6` tham gia tính điểm cho 14 kịch bản thì `expected_top3`/`expected_raw` có thể không còn đúng; đây là xung đột trực tiếp với bất biến, phải xử lý ở tầng thiết kế chứ không được chỉnh tệp.

Ngoài danh sách trên, các tệp kiểm thử phụ thuộc thứ hạng như `backend/tests/scenarios/test_scenarios.py`, `backend/tests/api/test_boundary_muc_5_1.py` và `backend/tests/scenarios/test_sensitivity_muc_5_2.py` cũng có thể phải rà soát. Chưa chạy thử nên nhóm **không khẳng định** con số bài kiểm thử sẽ hỏng.

### 3.5. Giao diện — 6 tệp

- `frontend/src/App.jsx`: thêm trạng thái mục tiêu/cấp lớp và đặt lại khi nạp kịch bản.
- `frontend/src/services/api.js`: thêm `s_6` vào `CRITERIA_LIST` và `DEFAULT_PRIORITIES`.
- `frontend/src/data/tutorsCatalog.js`: thêm `s_6` vào `CRITERIA_META` (nhãn, màu, mô tả).
- `frontend/src/components/StackedBarScore.jsx`: hiển thị 6 đoạn thay vì 5; xử lý `null`/`w = 0`.
- `frontend/src/pages/SearchPage.jsx`: thêm điều khiển mức ưu tiên thứ 6 và trường mục tiêu.
- `frontend/src/pages/ResultPage.jsx`: hiển thị tiêu chí thứ 6 trong bảng điểm/đóng góp và câu giải thích.

**Tổng kiểm kê:** **26 đường dẫn** được liệt kê — **25 tệp phải sửa** và **1 tệp khóa bất biến** (`scenarios.json`) chỉ được rà soát, không được sửa. Hai tệp `recommendation.py` và `App.jsx` không nằm trong danh sách gợi ý ban đầu nhưng bị ảnh hưởng khi rà mã nguồn: `recommendation.py` chỉ cần sửa mô tả, `App.jsx` cần giữ trạng thái mục tiêu. Nhóm **chưa có nguồn dữ liệu** cho trường trình độ gia sư; không được tự bịa giá trị cho 16 hồ sơ.

---

## 4. So sánh hai phương án

| Tiêu chí so sánh | Phương án 1 — Adaptive Weight Mapping | Phương án 2 — `s_6` Goal Compatibility |
|:---|:---|:---|
| **Số tệp phải đổi** | 4 tệp frontend: `App.jsx`, `api.js`, `SearchPage.jsx`, `ResultPage.jsx`. Không đổi backend, dữ liệu, hợp đồng API hay test. | 25 tệp: 7 dữ liệu/schema, 5 lõi chấm điểm, 2 hợp đồng/tài liệu, 5 test, 6 frontend; thêm `scenarios.json` là tệp khóa không được sửa. |
| **Ảnh hưởng 190/200 bài kiểm thử** | Không đổi payload/response nên không phải sửa test. Báo cáo giữa kỳ ghi 190 bài; bản hiện tại đã thu 200 bài (10 test độ nhạy Mục 5.2 bổ sung). Cần chạy lại để xác nhận, không suy luận. | Phải sửa các test khẳng định `CRITERIA_KEYS`, số khóa response và thứ hạng; một số test kịch bản/biên có thể hỏng. Chưa hiện thực nên **không khẳng định** số bài hỏng cụ thể. |
| **Ảnh hưởng 14 kịch bản** | Không đổi: khi nạp KB01–KB14, giao diện giữ nguyên `priorities` của kịch bản; mục tiêu chỉ là lựa chọn của người dùng. | Xung đột với `scenarios.json` khóa bất biến: thêm `s_6` làm đổi mẫu số/tổng trọng số và có thể đổi thứ hạng, trong khi không được sửa `expected_top3`/`expected_raw`. |
| **Nguồn dữ liệu cần thêm** | Không cần dữ liệu mới. Chỉ cần bảng ánh xạ do nhóm đề xuất, phải ghi rõ là giả định và chờ GVHD xác nhận. | Cần dữ liệu trình độ học vấn, cấp lớp và thế mạnh sư phạm của gia sư; hiện **chưa có nguồn** trong repo. Nếu không có dữ liệu, `s_6` chỉ là tổ hợp lại 5 tiêu chí cũ. |
| **Khả năng giải thích (XAI)** | Dùng đúng 5 tiêu chí và 5 khóa đóng góp hiện có; giao diện giải thích được “vì mục tiêu A nên Kinh nghiệm/Đánh giá được đặt Cao”. Minh bạch, dễ đối chiếu với scoring-spec. | `s_6` cần định nghĩa và dữ liệu riêng để giải thích; nếu dữ liệu không có, lý do gợi ý dễ thành suy diễn hoặc trùng lặp tiêu chí cũ, khó bảo vệ trước phản biện. |
| **Rủi ro chính** | Bảng ánh xạ là giả định chưa được GVHD xác nhận; Cấp lớp không được dùng; người dùng có thể hiểu nhầm mục tiêu tham gia chấm điểm; API client gọi trực tiếp có thể bỏ qua gợi ý. | Phá vỡ `TutorProfile`/`SearchRequest` do `extra="forbid"`; phải bịa hoặc bổ sung dữ liệu mới; đổi hợp đồng API và `CRITERIA_KEYS`; ảnh hưởng 14 kịch bản và nhiều test; công sức sửa toàn chuỗi lớn hơn nhiều. |

---

## 5. Khuyến nghị

**Khuyến nghị: chọn Phương án 1 — Adaptive Weight Mapping**, với các điều kiện sau:

1. **Chỉ triển khai khi GVHD đồng ý** với hướng tiếp cận và bảng ánh xạ ở Mục 2.2. Hiện trạng thái là **chờ GVHD xác nhận**.
2. **Chưa nằm trong phạm vi bắt buộc của `v1.0`.** Đây là hạng mục `Should`; nếu GVHD chưa phản hồi hoặc tiến độ căng, nhóm có thể cắt mà không ảnh hưởng Cổng chất lượng 4.
3. Chỉ thay đổi tầng giao diện/khởi tạo mức ưu tiên; **không** sửa `TutorProfile`, `SearchRequest`, `CRITERIA_KEYS`, `validate_tutors.py`, hợp đồng API, dữ liệu hay 14 kịch bản.
4. Giao diện phải ghi rõ mục tiêu chỉ **gợi ý** mức ưu tiên; người học vẫn chỉnh được và nhìn thấy đủ 5 tiêu chí.
5. Khi nạp kịch bản, giữ nguyên bộ ưu tiên của kịch bản; không để bảng ánh xạ đè lên 14 kịch bản đã khóa.

**Lộ trình theo giai đoạn nếu được duyệt:**

- **Giai đoạn 0 — Chờ GVHD chốt:** gửi 3 câu hỏi ở Mục 6; chưa viết mã.
- **Giai đoạn 1 — Chốt bảng ánh xạ:** xác nhận giá trị từng ô và nhãn “gợi ý”; không thay đổi dữ liệu.
- **Giai đoạn 2 — Giao diện:** thêm mục tiêu và bảng ánh xạ vào 4 tệp frontend đã nêu; không gửi mục tiêu lên API.
- **Giai đoạn 3 — Kiểm thử hồi quy:** chạy lại toàn bộ test backend (200 bài hiện tại), lint/build frontend; kiểm tra payload vẫn đúng 5 khóa; nạp thử 14 kịch bản và đối chiếu `expected_top3`.
- **Giai đoạn 4 — Chỉ khi GVHD yêu cầu dùng Cấp lớp:** lập đề xuất riêng về thu thập dữ liệu cấp lớp/trình độ; không gộp vào phạm vi tài liệu này.

---

## 6. Trạng thái và câu hỏi chờ GVHD

> ĐỀ XUẤT, CHƯA HIỆN THỰC, CHƯA CÓ PHẢN HỒI CỦA GVHD

**Ba điểm chưa xác minh:**

- Các ô `[giả định nhóm, chờ GVHD xác nhận]` trong bảng ánh xạ ở Mục 2.2 **chưa được GVHD xác nhận**.
- Phương án 2 mới chỉ được **phân tích định tính**, chưa chạy prototype `s_6`.
- Nhóm **chưa biết GVHD chọn phương án nào**.

Ba câu hỏi dự kiến gửi GVHD (nhóm không tự trả lời):

1. Cô chọn **Phương án 1 — Adaptive Weight Mapping** hay **Phương án 2 — bổ sung tiêu chí `s_6` Goal Compatibility**?
2. Có cần bổ sung dữ liệu **trình độ học vấn, cấp lớp và thế mạnh sư phạm** của gia sư không? Nếu có, nguồn dữ liệu nào được phép sử dụng để tránh tự tạo dữ liệu?
3. Trong bảng ánh xạ, ngoài hai mục tiêu “Điểm cao / luyện thi chuyên – học sinh giỏi” và “Đủ điểm đậu / lấy lại căn bản”, có cần thêm mục tiêu nào (ví dụ mất gốc, ôn thi chuyển cấp) và mức ưu tiên tương ứng không?
