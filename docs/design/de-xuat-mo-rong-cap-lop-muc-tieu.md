> [!NOTE]
> **Đề xuất, nhóm đã chọn Phương án 1 và hiện thực ở mức giao diện**

# Đề xuất mở rộng mô hình: tổ hợp Cấp lớp và Mục tiêu học tập

> PHƯƠNG ÁN 1 ĐÃ HIỆN THỰC Ở MỨC GIAO DIỆN (US-41, PR #85); PHƯƠNG ÁN 2 VÀ CẤP LỚP CHƯA HIỆN THỰC; CHƯA CÓ PHẢN HỒI CỦA GVHD

**Phạm vi:** tài liệu thiết kế để thảo luận với GVHD, ghi lại hiện trạng Phương án 1 đã hiện thực ở tầng giao diện và Phương án 2 chưa hiện thực. Phương án 1 không thay đổi backend, dữ liệu, 14 kịch bản hay bộ kiểm thử hiện có. Tài liệu dự kiến được trích vào Mục 6.2 của Chương 6 và dùng để chuẩn bị trả lời phản biện.

---

## 1. Bối cảnh và giới hạn dữ liệu hiện tại

### 1.1. Chỉ dẫn của GVHD

Báo cáo giữa kỳ ghi nhận chỉ dẫn của GVHD: nhu cầu của người học không nên dừng ở tên môn học, mà là tổ hợp ba chiều **(Môn học, Cấp lớp, Mục tiêu học tập)**. Cùng một môn học, hai người học có mục tiêu khác nhau sẽ cần những hồ sơ gia sư khác nhau. Báo cáo nêu hai ví dụ:

- **Học sinh A — Toán lớp 8, mục tiêu điểm 10 cuối kỳ hoặc luyện thi chuyên/học sinh giỏi:** ưu tiên gia sư có trình độ chuyên môn cao (giảng viên, thạc sĩ, thủ khoa), nhiều năm kinh nghiệm, đánh giá xuất sắc; chấp nhận học phí cao.
- **Học sinh B — Toán lớp 9, mục tiêu vừa đủ điểm đậu hoặc lấy lại kiến thức căn bản:** ưu tiên gia sư là sinh viên khá/giỏi, nhiệt tình, kiên nhẫn, học phí vừa phải và ở gần nhà.

Hai ví dụ cho thấy cùng một tiêu chí có thể có mức ưu tiên rất khác nhau tùy mục tiêu. Báo cáo đề xuất hai hướng kỹ thuật: (1) *Adaptive Weight Mapping* — mục tiêu học tập gợi ý bộ mức ưu tiên khởi tạo cho 5 tiêu chí hiện có, người học vẫn tinh chỉnh ở CN03; (2) bổ sung tiêu chí thành phần thứ 6 `s_6` *Goal Compatibility*. Nhóm đã chọn Phương án 1 và hiện thực ở mức giao diện; Phương án 2 chưa hiện thực. Tại thời điểm hiện thực, nhóm **chưa có phản hồi của GVHD**.

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

### 2.1. Cơ chế đã hiện thực

Mục tiêu học tập **chỉ sinh ra bộ mức ưu tiên khởi tạo ở tầng giao diện**. API, hợp đồng dữ liệu và lõi chấm điểm giữ nguyên:

1. Ô chọn **“Mục tiêu học tập (gợi ý mức ưu tiên)”** đặt ngay trên khối 5 tiêu chí ở màn hình nhập nhu cầu.
2. Khi người học chọn một mục tiêu, giao diện tra `GOAL_PRESETS` và điền 5 mức ưu tiên tương ứng.
3. Ô chọn **không có state riêng**: giá trị hiển thị được suy ra bằng cách so khớp 5 mức ưu tiên hiện tại với từng bộ điền sẵn; không khớp bộ nào thì hiện “Tùy chỉnh”.
4. Người học vẫn nhìn thấy và chỉnh được từng mức ưu tiên như CN03 hiện tại; khi chỉnh tay một tiêu chí, ô chọn chuyển thành “Tùy chỉnh”.
5. `buildRecommendationPayload` tiếp tục gửi đúng 7 trường và đúng 5 khóa `fee`, `district`, `experience`, `rating`, `availability`; **không gửi thêm trường mục tiêu** vì `SearchRequest` đang `extra="forbid"`.

Các tệp giao diện đã chạm tới trong PR #85 (đã kiểm tra tồn tại):

- `frontend/src/data/goalPresets.js` (mới): định nghĩa `GOAL_PRESETS` gồm 3 mục tiêu; mỗi mục tiêu có `key`, `label`, `description` và `priorities` đủ 5 khóa; dùng `DEFAULT_PRIORITIES` từ `frontend/src/services/api.js`, không định nghĩa lại nhãn mức ưu tiên.
- `frontend/src/pages/SearchPage.jsx`: thêm ô chọn mục tiêu và `handleGoalChange`; không thêm state/trường vào `searchForm`; đổi mục tiêu chỉ cập nhật `priorities` và đặt `scenarioMeta: null`.
- `frontend/src/App.css`: thêm lớp `.goal-preset-block`.
- `frontend/README.md`: mô tả tính năng và nêu rõ Cấp lớp chưa hiện thực vì hồ sơ gia sư thiếu dữ liệu cấp lớp.

Không sửa `frontend/src/App.jsx`, `frontend/src/pages/ResultPage.jsx`, backend, dữ liệu hay hợp đồng API. Khi nạp kịch bản KB01–KB14, giao diện giữ nguyên `priorities` của kịch bản; nhờ vậy 14 kịch bản không bị ảnh hưởng. Ví dụ, nạp KB01 hiện “Không nêu mục tiêu” (5 × Trung bình), còn nạp KB10 hiện “Tùy chỉnh” vì kịch bản có Kinh nghiệm = Cao.

### 2.2. Bảng ánh xạ Mục tiêu → mức ưu tiên

Mỗi ô ghi kèm thẻ nguồn. `[báo cáo giữa kỳ]` là giá trị báo cáo đã nêu; `[giả định nhóm, chờ GVHD xác nhận]` là giá trị nhóm tự đề xuất, **chưa được GVHD xác nhận**; `[Bảng 3.5 — mặc định hiện tại]` là bộ mặc định đang chạy trong hệ thống.

**Giá trị đang dùng trong code: `frontend/src/data/goalPresets.js`.**

| Mục tiêu | Học phí | Khu vực | Kinh nghiệm | Đánh giá | Lịch rảnh |
|:---|:---|:---|:---|:---|:---|
| **Không nêu mục tiêu** (`none`) | Trung bình<br>`[Bảng 3.5 — mặc định hiện tại]` | Trung bình<br>`[Bảng 3.5 — mặc định hiện tại]` | Trung bình<br>`[Bảng 3.5 — mặc định hiện tại]` | Trung bình<br>`[Bảng 3.5 — mặc định hiện tại]` | Trung bình<br>`[Bảng 3.5 — mặc định hiện tại]` |
| **Điểm cao / luyện thi chuyên – học sinh giỏi** (`high_score`) (học sinh A) | Trung bình<br>`[giả định nhóm, chờ GVHD xác nhận]` | Trung bình<br>`[giả định nhóm, chờ GVHD xác nhận]` | **Cao**<br>`[báo cáo giữa kỳ]` | **Cao**<br>`[báo cáo giữa kỳ]` | Trung bình<br>`[giả định nhóm, chờ GVHD xác nhận]` |
| **Đủ điểm đậu / lấy lại kiến thức căn bản** (`pass_basic`) (học sinh B) | **Cao**<br>`[báo cáo giữa kỳ]` | Trung bình<br>`[giả định nhóm, chờ GVHD xác nhận]` | Trung bình<br>`[giả định nhóm, chờ GVHD xác nhận]` | Trung bình<br>`[giả định nhóm, chờ GVHD xác nhận]` | Trung bình<br>`[giả định nhóm, chờ GVHD xác nhận]` |

**Gợi ý bổ sung của nhóm — để ngỏ, chưa hiện thực:**

- Với học sinh A, vì báo cáo nêu A **chấp nhận học phí cao**, nhóm từng đề xuất đặt Học phí = **Thấp** thay vì Trung bình để tránh đẩy học phí lên ngang các tiêu chí chuyên môn. Gợi ý này **không được dùng trong code**; code đang dùng Học phí = Trung bình theo bảng chốt ở trên.
- Với học sinh B, vì báo cáo nêu B ưu tiên gia sư **ở gần nhà**, nhóm từng đề xuất đặt Khu vực = **Cao** thay vì Trung bình. Gợi ý này **không được dùng trong code**; code đang dùng Khu vực = Trung bình theo bảng chốt ở trên.
- Các ô còn lại giữ Trung bình vì báo cáo không nêu mức cụ thể; nhóm không tự suy ra giá trị khác khi chưa có căn cứ. Hai gợi ý trên chỉ để thảo luận với GVHD, chưa hiện thực.

### 2.3. Ví dụ minh họa trên TQ1 và TQ2

Hai ca minh họa dưới đây được chọn **sau khi thử 19 truy vấn** (14 kịch bản KB01–KB14 và 5 truy vấn tự đặt), nên chỉ là ca minh họa cơ chế, không phải bằng chứng chất lượng gợi ý. KB01 được giữ làm **ca đối chiếu mặc định** vì là kịch bản đã đánh giá.

| Ca (hồ sơ) | Bộ ưu tiên | Hạng 1 | Hạng 2 | Hạng 3 |
|:---|:---|:---|:---|:---|
| **KB01** — Toán · trực tiếp · Bình Thạnh · 200.000đ<br>(ca đối chiếu mặc định) | Mặc định | GS-G01 — 0,938 | GS-G10 — 0,745 | GS-T06 — 0,625 |
| | `high_score` (A) | GS-G01 — 0,925 | GS-G10 — 0,794 | GS-T06 — 0,650 |
| | `pass_basic` (B) | GS-G01 — 0,944 | GS-G10 — 0,773 | GS-T06 — 0,556 |
| **TQ1** — Toán · trực tiếp · Bình Thạnh · 250.000đ<br>(học sinh A) | Mặc định | GS-G01 — 0,938 | GS-G10 — 0,745 | GS-G02 — 0,644 |
| | `high_score` (A) | GS-G01 — 0,925 | GS-G10 — 0,794 | **GS-T06 — 0,650** |
| | `pass_basic` (B) | GS-G01 — 0,944 | GS-G10 — 0,773 | GS-G02 — 0,639 |
| **TQ2** — Toán · trực tiếp · Gò Vấp · 150.000đ<br>(học sinh B) | Mặc định | GS-G10 — 0,745 | GS-T06 — 0,625 | GS-G01 — 0,588 |
| | `high_score` (A) | GS-G10 — 0,794 | GS-T06 — 0,650 | GS-G01 — 0,645 |
| | `pass_basic` (B) | GS-G10 — 0,773 | **GS-G01 — 0,589** | **GS-T06 — 0,556** |

- **KB01:** cả ba bộ giữ nguyên thứ hạng `GS-G01 > GS-G10 > GS-T06`; chỉ điểm tổng thay đổi.
- **TQ1:** bộ `high_score` thay `GS-G02` bằng `GS-T06` ở hạng 3; hạng 1 và 2 không đổi.
- **TQ2:** bộ `pass_basic` đảo hạng 2 và 3 (`GS-T06`/`GS-G01`); hạng 1 không đổi.

Đoạn mã dưới chỉ dùng `app.*` và `data/processed/tutors.json` (qua `TutorRepository`), không đọc `backend/tests/scenarios/scenarios.json`. Chạy khối mã từ thư mục `backend/` với `PYTHONPATH=.`:

```python
from app.data.repository import TutorRepository
from app.schemas.search_request import SearchRequest
from app.scoring.eligibility import filter_eligible_candidates
from app.scoring.filters import filter_mandatory
from app.scoring.ranker import score_and_rank
from app.scoring.weights import compute_effective_weights

PRESETS = {
    "default": dict(fee="medium", district="medium", experience="medium", rating="medium", availability="medium"),
    "high_score": dict(fee="medium", district="medium", experience="high", rating="high", availability="medium"),
    "pass_basic": dict(fee="high", district="medium", experience="medium", rating="medium", availability="medium"),
}
CASES = {"KB01": ("Bình Thạnh", 200000), "TQ1": ("Bình Thạnh", 250000), "TQ2": ("Gò Vấp", 150000)}

tutors = TutorRepository().get_all()
for case, (district, budget) in CASES.items():
    for name, priorities in PRESETS.items():
        query = SearchRequest(
            subject="Toán", learning_mode="in_person", preferred_district=district,
            max_budget_vnd=budget, priorities=priorities, top_k=3,
        )
        weights = compute_effective_weights(query)
        eligible, _ = filter_eligible_candidates(filter_mandatory(tutors, query), weights)
        top3 = score_and_rank(eligible, query, weights, top_k=3)
        print(case, name, " > ".join(f"{r.tutor_id} {r.total_score:.3f}" for r in top3))
```

Kết quả thật:

```text
KB01 default GS-G01 0.938 > GS-G10 0.745 > GS-T06 0.625
KB01 high_score GS-G01 0.925 > GS-G10 0.794 > GS-T06 0.650
KB01 pass_basic GS-G01 0.944 > GS-G10 0.773 > GS-T06 0.556
TQ1 default GS-G01 0.938 > GS-G10 0.745 > GS-G02 0.644
TQ1 high_score GS-G01 0.925 > GS-G10 0.794 > GS-T06 0.650
TQ1 pass_basic GS-G01 0.944 > GS-G10 0.773 > GS-G02 0.639
TQ2 default GS-G10 0.745 > GS-T06 0.625 > GS-G01 0.588
TQ2 high_score GS-G10 0.794 > GS-T06 0.650 > GS-G01 0.645
TQ2 pass_basic GS-G10 0.773 > GS-G01 0.589 > GS-T06 0.556
```

**Phạm vi khảo sát:** 19 truy vấn gồm 14 kịch bản KB01–KB14 và 5 truy vấn tự đặt (TQ1–TQ5). Mỗi truy vấn chạy với cả 3 bộ `default`, `high_score`, `pass_basic`. Kết quả: **trong 5 truy vấn tự đặt, 2 truy vấn có Top-3 khác giữa các bộ** (TQ1 đổi thành viên hạng 3; TQ2 đảo hạng 2 và 3); **trong 14 kịch bản chỉ KB10 khác**, và KB10 **không dùng làm bằng chứng** vì kịch bản vốn có Kinh nghiệm = Cao nên bộ `default` ghi đè thiết lập gốc; **không truy vấn nào đổi hạng 1**. KB05 không có gia sư thỏa điều kiện bắt buộc nên không xếp hạng. Script tái lập cả 19 truy vấn ở Phụ lục (Mục 7).

Đây chỉ là minh họa cơ chế trên 16 hồ sơ, không phải bằng chứng chất lượng gợi ý và không chứng minh rằng mục tiêu học tập luôn làm đổi thứ hạng.

### 2.4. Tác động

- **Tệp thay đổi thực tế (PR #85):** đúng 4 tệp frontend — `frontend/src/data/goalPresets.js` (mới), `frontend/src/pages/SearchPage.jsx`, `frontend/src/App.css`, `frontend/README.md`.
- **Không đổi hợp đồng API:** request vẫn 7 trường `subject`, `learning_mode`, `preferred_district`, `max_budget_vnd`, `time_slots`, `priorities`, `top_k`; `priorities` vẫn đúng 5 khóa; response vẫn đủ 5 khóa `criteria_scores` và `contributions`.
- **Không đổi `docs/design/scoring-spec.md`:** công thức $S = \sum w_i s_i / \sum w_i$, bảng quy đổi $0/1/2/3$ và các ngưỡng giữ nguyên.
- **Không đổi backend, dữ liệu, kịch bản:** không sửa `backend/`, `data/`, `backend/tests/scenarios/scenarios.json`; 16 hồ sơ và 14 kịch bản giữ nguyên.
- **Ô chọn là bộ điền sẵn:** giá trị ô được suy ra từ 5 mức ưu tiên hiện tại; không thêm state/trường vào `searchForm`; không gửi mục tiêu lên API.
- **Không đổi bộ kiểm thử:** backend vẫn nhận đúng 5 khóa; frontend chỉ thay cách khởi tạo `priorities`.
- **Cấp lớp KHÔNG tham gia lọc hay chấm điểm.** Hồ sơ gia sư không có trường cấp lớp, nên hệ thống không thể lọc “gia sư dạy lớp 8” hay “lớp 9”. Tương tự, trình độ học vấn và thế mạnh sư phạm cũng không tham gia trực tiếp; chúng chỉ được xấp xỉ gián tiếp qua kinh nghiệm, đánh giá, học phí và khu vực.
- **Đây là gợi ý ở tầng giao diện**, không phải quy tắc bắt buộc của hệ thống. Người dùng gọi API trực tiếp vẫn có thể gửi bất kỳ bộ ưu tiên hợp lệ nào; điều này là chấp nhận được vì mục tiêu chỉ nhằm giảm thao tác cho người dùng, không nhằm thay đổi lõi chấm điểm.

---

## 3. Phương án 2 — Bổ sung tiêu chí `s_6` Goal Compatibility

**Trạng thái: chưa hiện thực.** Phương án 2 thêm một tiêu chí thành phần thứ 6 vào công thức tổng hợp. Để `s_6` có ý nghĩa, cần đồng thời có: (a) mục tiêu học tập của người học trong `SearchRequest`; (b) thuộc tính của gia sư để so khớp mục tiêu (trình độ, cấp lớp, thế mạnh sư phạm); (c) dữ liệu cho 16 hồ sơ. Hiện repo **chưa có (b) và (c)**. Nếu chỉ tính `s_6` từ 5 trường hiện có thì `s_6` thực chất là một cách tổ hợp lại các tiêu chí cũ, trùng với Phương án 1 nhưng phức tạp hơn.

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

### 3.5. Giao diện — 7 tệp

- `frontend/src/data/goalPresets.js`: thêm khóa `s_6` vào cả 3 bộ điền sẵn để ô chọn mục tiêu vẫn khớp đủ 6 tiêu chí.
- `frontend/src/App.jsx`: thêm trạng thái mục tiêu/cấp lớp và đặt lại khi nạp kịch bản.
- `frontend/src/services/api.js`: thêm `s_6` vào `CRITERIA_LIST` và `DEFAULT_PRIORITIES`.
- `frontend/src/data/tutorsCatalog.js`: thêm `s_6` vào `CRITERIA_META` (nhãn, màu, mô tả).
- `frontend/src/components/StackedBarScore.jsx`: hiển thị 6 đoạn thay vì 5; xử lý `null`/`w = 0`.
- `frontend/src/pages/SearchPage.jsx`: thêm điều khiển mức ưu tiên thứ 6 và trường mục tiêu.
- `frontend/src/pages/ResultPage.jsx`: hiển thị tiêu chí thứ 6 trong bảng điểm/đóng góp và câu giải thích.

**Tổng kiểm kê:** **27 đường dẫn** được liệt kê — **26 tệp phải sửa** và **1 tệp khóa bất biến** (`backend/tests/scenarios/scenarios.json`) chỉ được rà soát, không được sửa. Hai tệp `backend/app/schemas/recommendation.py` và `frontend/src/App.jsx` được bổ sung khi rà mã nguồn: `backend/app/schemas/recommendation.py` chỉ cần sửa mô tả, `frontend/src/App.jsx` cần giữ trạng thái mục tiêu. `frontend/src/data/goalPresets.js` đã tồn tại từ Phương án 1 nhưng phải sửa nếu `priorities` có 6 khóa. Nhóm **chưa có nguồn dữ liệu** cho trường trình độ gia sư; không được tự bịa giá trị cho 16 hồ sơ.

---

## 4. So sánh hai phương án

| Tiêu chí so sánh | Phương án 1 — Adaptive Weight Mapping | Phương án 2 — `s_6` Goal Compatibility |
|:---|:---|:---|
| **Số tệp phải đổi** | Đã hiện thực: 4 tệp frontend — `frontend/src/data/goalPresets.js` (mới), `frontend/src/pages/SearchPage.jsx`, `frontend/src/App.css`, `frontend/README.md`. Không đổi backend, dữ liệu, hợp đồng API hay test. | 26 tệp: 7 dữ liệu/schema, 5 lõi chấm điểm, 2 hợp đồng/tài liệu, 5 test, 7 frontend; thêm `backend/tests/scenarios/scenarios.json` là tệp khóa không được sửa. |
| **Ảnh hưởng bộ kiểm thử** | Không đổi payload/response nên không phải sửa test; bộ kiểm thử backend vẫn giữ 200 bài. | Phải sửa các test khẳng định `CRITERIA_KEYS`, số khóa response và thứ hạng; một số test kịch bản/biên có thể hỏng. Chưa hiện thực nên **không khẳng định** số bài hỏng cụ thể. |
| **Ảnh hưởng 14 kịch bản** | Không đổi: khi nạp KB01–KB14, giao diện giữ nguyên `priorities` của kịch bản; mục tiêu chỉ là lựa chọn của người dùng. | Xung đột với `backend/tests/scenarios/scenarios.json` khóa bất biến: thêm `s_6` làm đổi mẫu số/tổng trọng số và có thể đổi thứ hạng, trong khi không được sửa `expected_top3`/`expected_raw`. |
| **Nguồn dữ liệu cần thêm** | Không cần dữ liệu mới. Bảng ánh xạ đã dùng trong code; các ô giả định vẫn chờ GVHD xác nhận. | Cần dữ liệu trình độ học vấn, cấp lớp và thế mạnh sư phạm của gia sư; hiện **chưa có nguồn** trong repo. Nếu không có dữ liệu, `s_6` chỉ là tổ hợp lại 5 tiêu chí cũ. |
| **Khả năng giải thích (XAI)** | Dùng đúng 5 tiêu chí và 5 khóa đóng góp hiện có; giao diện giải thích được “vì mục tiêu A nên Kinh nghiệm/Đánh giá được đặt Cao”. Minh bạch, dễ đối chiếu với `docs/design/scoring-spec.md`. | `s_6` cần định nghĩa và dữ liệu riêng để giải thích; nếu dữ liệu không có, lý do gợi ý dễ thành suy diễn hoặc trùng lặp tiêu chí cũ, khó bảo vệ trước phản biện. |
| **Rủi ro chính** | Bảng ánh xạ là giả định chưa được GVHD xác nhận; Cấp lớp không được dùng; người dùng có thể hiểu nhầm mục tiêu tham gia chấm điểm; API client gọi trực tiếp có thể bỏ qua gợi ý. | Phá vỡ `TutorProfile`/`SearchRequest` do `extra="forbid"`; phải bịa hoặc bổ sung dữ liệu mới; đổi hợp đồng API và `CRITERIA_KEYS`; ảnh hưởng 14 kịch bản và nhiều test; công sức sửa toàn chuỗi lớn hơn nhiều. |

---

## 5. Khuyến nghị

**Khuyến nghị: nhóm đã chọn Phương án 1 — Adaptive Weight Mapping và hiện thực ở mức giao diện.** Phương án 2 giữ nguyên, chưa hiện thực.

1. **Bảng ánh xạ vẫn là giả định của nhóm**, chưa được GVHD xác nhận; cần hỏi GVHD để chốt giá trị từng ô và nhãn “gợi ý”.
2. **Phạm vi đã hiện thực chỉ ở tầng giao diện**: không sửa `backend/app/schemas/tutor.py`, `backend/app/schemas/search_request.py`, `backend/app/core/config.py`, `scripts/validate_tutors.py`, hợp đồng API, dữ liệu hay 14 kịch bản.
3. Giao diện ghi rõ mục tiêu chỉ **gợi ý** mức ưu tiên; người học vẫn chỉnh được và nhìn thấy đủ 5 tiêu chí.
4. Khi nạp kịch bản, giữ nguyên bộ ưu tiên của kịch bản; không để bảng ánh xạ đè lên 14 kịch bản đã khóa.
5. Phương án 2 chỉ nên triển khai nếu GVHD yêu cầu và có nguồn dữ liệu cấp lớp/trình độ/thế mạnh sư phạm; hiện chưa có.

**Lộ trình:**

- **Giai đoạn 0 — Đã hiện thực (Phương án 1):** ô chọn mục tiêu và bộ điền sẵn ở frontend; không gửi mục tiêu lên API. Chưa có phản hồi của GVHD tại thời điểm hiện thực.
- **Giai đoạn 1 — Chờ GVHD góp ý:** xác nhận giá trị từng ô và nhãn “gợi ý”; nếu GVHD yêu cầu khác thì điều chỉnh bảng hoặc gỡ phần gợi ý.
- **Giai đoạn 2 — Nếu GVHD yêu cầu dùng Cấp lớp hoặc `s_6`:** lập đề xuất riêng về thu thập dữ liệu cấp lớp/trình độ; không gộp vào phạm vi tài liệu này.

---

## 6. Trạng thái và câu hỏi chờ GVHD

> PHƯƠNG ÁN 1 ĐÃ HIỆN THỰC Ở MỨC GIAO DIỆN (US-41, PR #85); PHƯƠNG ÁN 2 VÀ CẤP LỚP CHƯA HIỆN THỰC; CHƯA CÓ PHẢN HỒI CỦA GVHD

**Ba điểm chưa xác minh:**

- **(a)** Các ô `[giả định nhóm, chờ GVHD xác nhận]` trong bảng ánh xạ ở Mục 2.2 **chưa được GVHD xác nhận**; bảng là giá trị nhóm tự đặt, chưa kiểm chứng với người dùng.
- **(b)** Phương án 2 mới chỉ được **phân tích định tính**, chưa chạy prototype `s_6`.
- **(c)** **Chưa có phản hồi của GVHD tại thời điểm hiện thực**; nhóm chưa biết GVHD đánh giá Phương án 1 đã hiện thực như thế nào và có yêu cầu chuyển sang Phương án 2 hay không.

Ba câu hỏi dự kiến gửi GVHD (nhóm không tự trả lời):

1. Cô đánh giá thế nào về việc nhóm chọn và hiện thực **Phương án 1 — Adaptive Weight Mapping** ở mức giao diện? Có cần chuyển sang **Phương án 2 — bổ sung tiêu chí `s_6` Goal Compatibility** không?
2. Có cần bổ sung dữ liệu **trình độ học vấn, cấp lớp và thế mạnh sư phạm** của gia sư không? Nếu có, nguồn dữ liệu nào được phép sử dụng để tránh tự tạo dữ liệu?
3. Trong bảng ánh xạ, ngoài hai mục tiêu “Điểm cao / luyện thi chuyên – học sinh giỏi” và “Đủ điểm đậu / lấy lại kiến thức căn bản”, có cần thêm mục tiêu nào (ví dụ mất gốc, ôn thi chuyển cấp) và mức ưu tiên tương ứng không?

---

## 7. Phụ lục — script tái lập khảo sát 19 truy vấn

Phụ lục này không trích vào Chương 6. Script đọc 14 kịch bản từ `backend/tests/scenarios/scenarios.json` và khai báo trực tiếp TQ1–TQ5. Chạy khối mã dưới từ thư mục `backend/` với `PYTHONPATH=.`; stdout chỉ dùng ASCII.

```python
import json
from pathlib import Path

from app.data.repository import TutorRepository
from app.schemas.search_request import SearchRequest
from app.scoring.eligibility import filter_eligible_candidates
from app.scoring.filters import filter_mandatory
from app.scoring.ranker import score_and_rank
from app.scoring.weights import compute_effective_weights

PRESETS = {
    "default": dict(fee="medium", district="medium", experience="medium", rating="medium", availability="medium"),
    "high_score": dict(fee="medium", district="medium", experience="high", rating="high", availability="medium"),
    "pass_basic": dict(fee="high", district="medium", experience="medium", rating="medium", availability="medium"),
}
EXTRA = {
    "TQ1": dict(subject="Toán", learning_mode="in_person", preferred_district="Bình Thạnh", max_budget_vnd=250000),
    "TQ2": dict(subject="Toán", learning_mode="in_person", preferred_district="Gò Vấp", max_budget_vnd=150000),
    "TQ3": dict(subject="Toán", learning_mode="online", max_budget_vnd=300000, time_slots=["T2-tối", "T4-tối"]),
    "TQ4": dict(subject="Lý", learning_mode="in_person", preferred_district="Thủ Đức", max_budget_vnd=180000),
    "TQ5": dict(subject="Hóa", learning_mode="in_person", preferred_district="Quận 10", max_budget_vnd=220000, time_slots=["T7-sáng"]),
}


def top3(tutors, payload):
    query = SearchRequest(**payload)
    weights = compute_effective_weights(query)
    eligible, _ = filter_eligible_candidates(filter_mandatory(tutors, query), weights)
    return [r.tutor_id for r in score_and_rank(eligible, query, weights, top_k=3)]


scenarios = json.loads(Path("tests/scenarios/scenarios.json").read_text(encoding="utf-8"))
cases = {s["id"]: s["request"] for s in scenarios}
cases.update(EXTRA)

tutors = TutorRepository().get_all()
khac, doi_hang_1 = 0, 0
for case_id, request in cases.items():
    orders = {name: top3(tutors, {**request, "priorities": p}) for name, p in PRESETS.items()}
    is_khac = len({tuple(v) for v in orders.values()}) > 1
    if is_khac:
        khac += 1
    if len({v[0] for v in orders.values() if v}) > 1:
        doi_hang_1 += 1
    label = "KHAC" if is_khac else "giong"
    parts = []
    for name in ("default", "high_score", "pass_basic"):
        ids = ",".join(orders[name]) if orders[name] else "none"
        parts.append(f"{name}={ids}")
    print(f"{case_id} {label} " + " | ".join(parts))

print(f"TONG={len(cases)} SO_CA_KHAC={khac} SO_CA_DOI_HANG_1={doi_hang_1}")
```

Kết quả thật:

```text
KB01 giong default=GS-G01,GS-G10,GS-T06 | high_score=GS-G01,GS-G10,GS-T06 | pass_basic=GS-G01,GS-G10,GS-T06
KB02 giong default=GS-G11,GS-G12,GS-T07 | high_score=GS-G11,GS-G12,GS-T07 | pass_basic=GS-G11,GS-G12,GS-T07
KB03 giong default=GS-G12,GS-G11,GS-T07 | high_score=GS-G12,GS-G11,GS-T07 | pass_basic=GS-G12,GS-G11,GS-T07
KB04 giong default=GS006,GS020 | high_score=GS006,GS020 | pass_basic=GS006,GS020
KB05 giong default=none | high_score=none | pass_basic=none
KB06 giong default=GS-G04 | high_score=GS-G04 | pass_basic=GS-G04
KB07 giong default=GS-G05 | high_score=GS-G05 | pass_basic=GS-G05
KB08 giong default=GS-G07 | high_score=GS-G07 | pass_basic=GS-G07
KB09 giong default=GS-G08 | high_score=GS-G08 | pass_basic=GS-G08
KB10 KHAC default=GS-G10,GS-G09,GS-G01 | high_score=GS-G10,GS-G01,GS-G09 | pass_basic=GS-G10,GS-G09,GS-G01
KB11 giong default=GS-G06,GS-T06 | high_score=GS-G06,GS-T06 | pass_basic=GS-G06,GS-T06
KB12 giong default=GS-T07,GS-G11,GS-G12 | high_score=GS-T07,GS-G11,GS-G12 | pass_basic=GS-T07,GS-G11,GS-G12
KB13 giong default=GS-G10,GS-G01,GS-T06 | high_score=GS-G10,GS-G01,GS-T06 | pass_basic=GS-G10,GS-G01,GS-T06
KB14 giong default=GS-G03 | high_score=GS-G03 | pass_basic=GS-G03
TQ1 KHAC default=GS-G01,GS-G10,GS-G02 | high_score=GS-G01,GS-G10,GS-T06 | pass_basic=GS-G01,GS-G10,GS-G02
TQ2 KHAC default=GS-G10,GS-T06,GS-G01 | high_score=GS-G10,GS-T06,GS-G01 | pass_basic=GS-G10,GS-G01,GS-T06
TQ3 giong default=GS-G01,GS-G02 | high_score=GS-G01,GS-G02 | pass_basic=GS-G01,GS-G02
TQ4 giong default=GS-T06 | high_score=GS-T06 | pass_basic=GS-T06
TQ5 giong default=GS-G06 | high_score=GS-G06 | pass_basic=GS-G06
TONG=19 SO_CA_KHAC=3 SO_CA_DOI_HANG_1=0
```

Mỗi ca in một dòng `giong` hoặc `KHAC` kèm Top-3 của cả 3 bộ; KB05 in `none` vì không có gia sư thỏa điều kiện bắt buộc. Script chỉ dùng `app.*`, `data/processed/tutors.json` (qua `TutorRepository`) và đọc `backend/tests/scenarios/scenarios.json`.
