> [!NOTE]
> **Đề xuất, nhóm xác nhận**

# Báo cáo tiến độ giữa kỳ và nghiệm thu thực nghiệm Bảng 5.1 (Kết thúc Sprint 5 — Cổng chất lượng 3)

- **Đề tài:** Hệ thống khuyến nghị gia sư dựa trên mức độ phù hợp đa tiêu chí
- **Học phần:** Đồ án Khoa học máy tính 1 — Khoa Công nghệ thông tin, Trường Đại học Kỹ thuật Công nghệ Cần Thơ
- **Giảng viên hướng dẫn:** TS. Lê Anh Nhã Uyên
- **Nhóm sinh viên thực hiện:**
  - Cao Khánh Ngọc (`KHMT2411025` — Nhóm trưởng / Product Owner kiêm Developer)
  - Trần Nguyễn Đức (`KHMT2411011` — Scrum Master các Sprint 1, 3, 5 kiêm Developer)
  - Lê Thị Bích Chuyền (`KHMT2411037` — Scrum Master các Sprint 2, 4, 6 kiêm Developer)
- **Mốc báo cáo:** Giữa kỳ — hoàn tất **Sprint 1 đến hết Sprint 5** (đã vượt qua **3 Cổng chất lượng 1, 2, 3** trên nhánh `main` tại commit `de0ceb9`) và chuyển sang **Sprint 6** (hoàn thiện báo cáo cuối kỳ).

---

## 1. Tổng quan tiến độ theo Cấu trúc Đề cương (Bảng 1.2) và 4 Mục tiêu cụ thể (Mục 1.4)

### 1.1. Tiến độ thực hiện theo các chương của đề cương (Bảng 1.2)

| Hạng mục trong Đề cương (Bảng 1.2) | Thời lượng dự kiến | Trạng thái hiện tại (Giữa kỳ) | Minh chứng trong Repository (`origin/main`) |
|:---|:---:|:---:|:---|
| **Chương 1 — Tổng quan về đề tài** | 8 giờ (8%) | **Đã hoàn thành (100%)** | Phát biểu lý do chọn đề tài, khảo sát 3 nền tảng thực tế (Bảng 1.1), bổ sung đối sánh chi tiết với đồ án tham khảo GS360 [3] tại `docs/thesis/outline/muc-1.3-gs360.md` (PR #47) và khóa phạm vi tại `docs/thesis/review/sprint-01-problem-lock-report.md` (PR #51). |
| **Chương 2 — Cơ sở lý thuyết và công nghệ** | 10 giờ (10%) | **Đã hoàn thành (100%)** | Cơ sở khuyến nghị dựa trên đặc trưng hồ sơ, lọc điều kiện bắt buộc kết hợp Weighted Scoring (Bảng 2.1, Bảng 2.2) và lựa chọn công nghệ FastAPI + ReactJS. |
| **Chương 3 — Phân tích và thiết kế hệ thống** | 30 giờ (30%) | **Đã hoàn thành (100%)** | Khóa toàn bộ công thức Bảng 3.2, Bảng 3.5, Bảng 3.6 và bảng ngưỡng dữ liệu tối thiểu tại `docs/design/scoring-spec.md` (PR #50); khóa từ điển dữ liệu Bảng 3.3–3.4 tại `docs/design/data-dictionary.md`; khóa hợp đồng API tại `docs/design/api-contract.md` (PR #46). |
| **Chương 4 — Xây dựng hệ thống** | 30 giờ (30%) | **Đã hoàn thành (100%)** | Hoàn thiện toàn bộ dữ liệu mẫu 16 hồ sơ (`data/processed/tutors.{json,csv}`), module lõi chấm điểm độc lập (`backend/app/scoring/`), API `POST /api/recommend` (`backend/app/api/recommend.py`) và giao diện ReactJS 2 màn hình tích hợp đầy đủ 3 chức năng **CN01, CN02, CN03** (`frontend/src/`). |
| **Chương 5 — Kiểm thử và đánh giá** | 16 giờ (16%) | **Đã hoàn thành Mục 5.1 & Bảng 5.1 (~75%)** | Hoàn tất kiểm thử đơn vị, kiểm thử ca biên Mục 5.1 (`test_boundary_muc_5_1.py`), tự động hóa 14 kịch bản (`test_scenarios.py`), điền đầy đủ cột **"Top-3 hệ thống"** của **Bảng 5.1** (`muc-5.1-bang-5.1-ket-qua.md`) và phân tích toán học (`discrepancy_analysis.md`). Phần khảo sát độ nhạy tham số Mục 5.2 và tổng hợp văn bản Chương 5 thực hiện ở Sprint 6. |
| **Chương 6 — Kết luận và hướng phát triển** | 6 giờ (6%) | **Đã có khung đối chiếu (~40%)** | Đã khởi tạo khung đối chiếu Mục 6.1 và bảng phân công Bảng 6.1 tại `docs/thesis/outline/muc-6.1-bang-6.1.md` (PR #47); sẽ hoàn thiện toàn văn Chương 6, Phụ lục A–D và slide bảo vệ ở Sprint 6. |

### 1.2. Đối chiếu với 4 mục tiêu cụ thể của đề tài (Mục 1.4)

1. **Mục tiêu (a) — Mô hình hóa mức độ phù hợp và xây dựng module lọc – tính điểm có trọng số:**
   - **Trạng thái:** **Hoàn thành 100%** (Sprint 1–3).
   - **Kết quả:** Hiện thực đầy đủ quy trình 4 bước độc lập với tầng API tại `backend/app/scoring/`: lọc điều kiện bắt buộc (`filters.py`), quy đổi 4 mức ưu tiên sang trọng số và xử lý tiêu chí không áp dụng (`weights.py`), kiểm tra ngưỡng dữ liệu tối thiểu $n \in \{0..5\}$ (`eligibility.py`), 5 hàm chuẩn hóa điểm thành phần $s_i \in [0, 1]$ theo Bảng 3.6 (`criteria.py`), và tổng hợp điểm Weighted Scoring $S(g) = \sum (w_i \cdot s_i) / \sum w_i$ kèm tỷ lệ đóng góp $C_i$, phá hòa tất định theo `tutor_id` tăng dần và sinh lời giải thích tiếng Việt (`ranker.py`).
2. **Mục tiêu (b) — Xây dựng dịch vụ API gợi ý bằng FastAPI:**
   - **Trạng thái:** **Hoàn thành 100%** (Sprint 4, `PR #68`).
   - **Kết quả:** Endpoint `POST /api/recommend` tuân thủ nghiêm ngặt thứ tự xử lý 5 bước của `docs/design/api-contract.md`, kiểm tra hợp lệ đầu vào bằng Pydantic v2 (`422 Unprocessable Entity`), phân biệt chính xác 3 trạng thái phản hồi nghiệp vụ (`success`, `no_match` kèm `insufficient_data_candidates`, `zero_weight` kèm `unranked_candidates`), cấu hình CORS và tài liệu OpenAPI/Swagger UI (`/docs`). Thời gian phản hồi thực tế đạt trung bình **`~4,75 ms`** (thấp hơn rất nhiều so với ngưỡng yêu cầu phi chức năng `< 1000 ms`).
3. **Mục tiêu (c) — Xây dựng giao diện demo bằng ReactJS:**
   - **Trạng thái:** **Hoàn thành 100%** (Sprint 4–5, `PR #69`, `PR #71`, `PR #72`).
   - **Kết quả:** Hiện thực đầy đủ hai màn hình theo Hình 3.4 và Hình 3.5 đề cương, đáp ứng trọn vẹn 3 chức năng cốt lõi **CN01**, **CN02**, **CN03** (Bảng 3.1).
4. **Mục tiêu (d) — Đánh giá chất lượng xếp hạng bằng bộ kịch bản có kỳ vọng xác định trước và minh họa ảnh hưởng của mức ưu tiên:**
   - **Trạng thái:** **Đã hoàn thành thực nghiệm 14/14 kịch bản Bảng 5.1 và luồng tương tác CN03; còn bước khảo sát độ nhạy tham số Mục 5.2 ở Sprint 6.**
   - **Kết quả:** Toàn bộ **14/14 kịch bản (`KB01`–`KB14`)** có danh sách Top-3 của hệ thống trùng khớp **100%** với Top-3 kỳ vọng đã khóa từ đầu kỳ.

---

## 2. Tổng kết tiến độ 5 Sprint đầu và 3 Cổng chất lượng (Quality Gates 1, 2, 3)

Tính đến commit `de0ceb9` trên nhánh `main`, nhóm đã hoàn thành **5/6 Sprint** (**31/36 User Stories** đã xếp sprint = **86,1%**, tương ứng **54/63 Story Points = 85,7%**):

| Sprint | Mục tiêu trọng tâm | Khối lượng | Các PR đã hợp nhất vào `main` | Cổng chất lượng (Quality Gate) |
|:---|:---|:---:|:---|:---|
| **Sprint 1** | Khóa thiết kế công thức, chuẩn hóa 16 hồ sơ & 14 kịch bản, dựng khung dự án & CI | 10 US (12 SP) | `PR #40`–`#52` | **Đạt Cổng chất lượng 1:** Dữ liệu mẫu & 14 kịch bản đã khóa bất biến trước khi viết code tính điểm; GVHD đã xác nhận phần khóa bài toán (`sprint-01-problem-lock-report.md`). |
| **Sprint 2** | Cài đặt tầng nạp dữ liệu (`repository.py`), lọc cứng (`filters.py`), 5 hàm điểm (`criteria.py`), trọng số (`weights.py`) & unit test | 5 US (10 SP) | `PR #54`–`#57`, `PR #62` | 100% unit test cho bộ lọc, trọng số và 5 hàm điểm thành phần Bảng 3.6 vượt qua thành công. |
| **Sprint 3** | Cài đặt ngưỡng dữ liệu tối thiểu (`eligibility.py`), xếp hạng Weighted Scoring (`ranker.py`), tự động hóa 14 kịch bản & phân tích sai lệch | 5 US (9 SP) | `PR #63`–`#67` | **Đạt Cổng chất lượng 2:** `test_scenarios.py` chạy tự động 14/14 kịch bản khớp `expected_top3` 100%; giải trình toán học tại `discrepancy_analysis.md`. |
| **Sprint 4** | Xây dựng API `POST /api/recommend`, kiểm thử tích hợp `TestClient` và màn hình nhập nhu cầu `SearchPage` (CN01) | 6 US (11 SP) | `PR #68`–`#70` | 35 bài kiểm thử tích hợp HTTP API xanh 100%; độ trễ trung bình `~4,75 ms < 1000 ms`. |
| **Sprint 5** | Xây dựng `ResultPage`, `TutorCard`, `StackedBarScore` (CN02), điều chỉnh ưu tiên trực tiếp (CN03), kiểm thử ca biên Mục 5.1 & điền Bảng 5.1 | 5 US (12 SP) | `PR #71`–`#74` | **Đạt Cổng chất lượng 3:** Hoàn chỉnh luồng E2E `CN01 <-> CN02 + CN03`; hoàn tất kiểm thử ca biên Mục 5.1 và điền cột "Top-3 hệ thống" vào Bảng 5.1. |

### Chỉ số chất lượng mã nguồn thực tế trên `origin/main` (`de0ceb9`)

- **Backend (`backend/`):**
  - Kiểm tra chuẩn mã nguồn (`ruff check .`): `All checks passed!` (0 lỗi, 0 cảnh báo).
  - Bộ kiểm thử tự động (`pytest -v -rs`): **`190 passed, 0 skipped`** (thời gian chạy `~0,85s`), gồm:
    - `132` bài kiểm thử đơn vị (`tests/unit/` và `tests/test_environment.py`) cho cấu hình, repository, bộ lọc, 5 hàm điểm, trọng số, ngưỡng dữ liệu tối thiểu và bộ xếp hạng.
    - `17` bài kiểm thử kịch bản thực nghiệm (`tests/scenarios/test_scenarios.py`) đối chiếu 14 kịch bản `KB01`–`KB14`.
    - `41` bài kiểm thử tích hợp API và ca biên Mục 5.1 (`tests/api/test_recommend_api.py` và `tests/api/test_boundary_muc_5_1.py`).
  - Độ bao phủ mã nguồn (`pytest --cov=app`): Đạt **96%** trên toàn bộ `backend/app/` (`100%` tại `api/recommend.py`, `main.py`, `schemas/*`, `data/repository.py`, `scoring/filters.py`, `scoring/weights.py`).
- **Frontend (`frontend/`):**
  - Kiểm tra tĩnh (`npm run lint` với `oxlint`): `Found 0 warnings and 0 errors` trên toàn bộ 10 tệp mã nguồn.
  - Đóng gói sản phẩm (`npm run build` với `vite build`): Biên dịch thành công (`~257 ms`).

---

## 3. Minh chứng vận hành End-to-End 3 chức năng cốt lõi (CN01 – CN02 – CN03)

### 3.1. Luồng hoạt động thực tế của 3 chức năng (Bảng 3.1)

1. **CN01 — Nhập nhu cầu và mức ưu tiên (`frontend/src/pages/SearchPage.jsx`):**
   - Cho phép người học chọn môn học (bắt buộc), hình thức học (`Trực tiếp`, `Trực tuyến`, `Không yêu cầu`), khu vực mong muốn (tự động khóa/vô hiệu hóa khi chọn học `Trực tuyến` theo đúng Mục 3.6), ngân sách tối đa theo giờ (VNĐ), lưới 21 khung giờ rảnh trong tuần (Thứ 2 – Chủ nhật × Sáng/Chiều/Tối) và mức ưu tiên 4 nấc (`Không quan tâm`, `Thấp`, `Trung bình`, `Cao`) cho 5 tiêu chí.
   - Tích hợp sẵn thanh **"Nạp nhanh kịch bản thực nghiệm (Bảng 5.1)"** (`scenariosCatalog.js`) giúp giảng viên hoặc người chấm chọn bất kỳ kịch bản nào từ `KB01` đến `KB14` chỉ bằng 1 cú nhấp chuột.
2. **CN02 — Xem danh sách gợi ý kèm điểm và thanh xếp chồng (`ResultPage.jsx`, `TutorCard.jsx`, `StackedBarScore.jsx`):**
   - Hiển thị danh sách Top-$k$ gia sư theo thẻ trực quan (Hình 3.5 đề cương) gồm: hạng, mã gia sư, nhãn nguồn dữ liệu (`Thu thập công khai (*)` cho `GS-T06`, `GS-T07` hoặc `Giả lập`), môn dạy, hình thức, khu vực, học phí, số năm kinh nghiệm, điểm đánh giá, khung giờ rảnh, điểm phù hợp tổng hợp $S(g)$, bảng điểm thành phần $s_i$, biểu đồ thanh xếp chồng nhiều màu thể hiện tỷ lệ đóng góp $C_i = w_i \cdot s_i / \sum w_i$ và lời giải thích tiếng Việt (`reason`) kèm ghi chú (`notes`: `"chưa có đánh giá"`).
   - Hiển thị thông báo tường minh cho các trạng thái đặc biệt: không có gia sư thỏa điều kiện (`no_match` kèm danh sách ứng viên bị loại do thiếu dữ liệu `insufficient_data_candidates`) hoặc tổng trọng số bằng 0 (`zero_weight` kèm danh sách ứng viên vượt qua lọc bắt buộc `unranked_candidates`).
3. **CN03 — Điều chỉnh mức ưu tiên trực tiếp trên màn hình kết quả (`ResultPage.jsx` — điểm nhấn thực nghiệm):**
   - Ngay trên màn hình kết quả, người học có thể đổi mức ưu tiên của từng tiêu chí hoặc bấm các nút cấu hình nhanh (*Mặc định cân bằng*, *Ưu tiên Học phí*, *Ưu tiên Kinh nghiệm & Đánh giá*, *Ưu tiên Khu vực*).
   - Mỗi lần thay đổi, giao diện tự động gọi lại `POST /api/recommend`, hiển thị thời gian phản hồi thực tế (`~4–6 ms < 1000 ms`), cập nhật lại thanh xếp chồng và gắn huy hiệu biến động thứ hạng (`▲ Tăng hạng` / `▼ Giảm hạng` / `Mới vào Top-k`).
   - **Ví dụ thực nghiệm trực tiếp trên dữ liệu mẫu (nhu cầu Toán, Trực tiếp, Bình Thạnh, ngân sách 200.000đ, lịch rảnh `T2-tối, T4-tối, T7-sáng`):**
     - *Khi đặt `fee = Cao (3)`, `experience = Thấp (1)`, `rating = Thấp (1)` (`KB01`):* Hệ thống xếp **`1. GS-G01 (0,899) > 2. GS-G02 (0,836) > 3. GS-T06 (0,833)`** vì `GS-G01` có học phí 180.000đ nằm trong ngân sách ($s_{\text{fee}} = 1{,}00$).
     - *Khi đổi trực tiếp trên bảng CN03 sang `fee = Thấp (1)`, `experience = Cao (3)`, `rating = Cao (3)` (`KB02`):* Thứ hạng lập tức đảo chiều thành **`1. GS-G02 (0,889) > 2. GS-G01 (0,771) = 3. GS-T06 (0,771)`** vì điểm kinh nghiệm (6 năm) và đánh giá (4,9/5) của `GS-G02` bù đắp vượt trội cho mức học phí 240.000đ (vượt nhẹ 20% ngân sách).

### 3.2. Các lệnh khởi chạy và kiểm chứng nhanh (dành cho buổi kiểm tra giữa kỳ)

```powershell
# 1. Chạy bộ 190 bài kiểm thử tự động & kiểm tra chuẩn code Backend (tại thư mục backend/)
.\.venv\Scripts\ruff.exe check .
.\.venv\Scripts\python.exe -m pytest -v -rs

# 2. Khởi động máy chủ API FastAPI tại http://localhost:8000 (Swagger UI tại http://localhost:8000/docs)
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000

# 3. Khởi động giao diện ReactJS tại http://localhost:5173 (tại thư mục frontend/)
npm run dev
```

---

## 4. Kết quả kiểm thử ca biên (Mục 5.1) và Bảng 5.1 hoàn chỉnh (14/14 kịch bản)

### 4.1. Tổng hợp kết quả thực nghiệm Bảng 5.1 (tích hợp từ `docs/thesis/report/muc-5.1-bang-5.1-ket-qua.md`)

Tất cả **14/14 kịch bản (`KB01`–`KB14`)** đều được kiểm thử tự động tại `backend/tests/scenarios/test_scenarios.py` và `backend/tests/api/test_recommend_api.py`, đạt tỷ lệ trùng khớp **14/14 (100%)** so với `expected_top3` đã khóa từ Sprint 1:

| Mã KB | Tóm tắt nhu cầu tìm kiếm & mức ưu tiên | Top-3 kỳ vọng (Đề cương gốc) | Top-3 hệ thống (Thực chạy API) | Số trùng | Nhận xét đối chiếu |
|:---:|:---|:---|:---|:---:|:---|
| **KB01** | Toán \| Trực tiếp \| Bình Thạnh \| 200.000đ \| `fee=Cao`, `exp=Thấp`, `rating=Thấp` | `1. GS-G01 (0,899)`<br/>`2. GS-G02 (0,836)`<br/>`3. GS-T06 (0,833)` | `1. GS-G01 (0,899)`<br/>`2. GS-G02 (0,836)`<br/>`3. GS-T06 (0,833)` | **3/3** | Khớp tuyệt đối cả thứ hạng và điểm số đến 3 chữ số thập phân. |
| **KB02** | Toán \| Trực tiếp \| Bình Thạnh \| 200.000đ \| `fee=Thấp`, `exp=Cao`, `rating=Cao` | `1. GS-G02 (0,889)`<br/>`2–3. GS-G01 = GS-T06 (0,771, đồng hạng)` | `1. GS-G02 (0,889)`<br/>`2. GS-G01 (0,771)`<br/>`3. GS-T06 (0,771)` | **3/3** | Khớp tuyệt đối; minh họa đảo thứ hạng khi đổi ưu tiên từ Học phí sang Kinh nghiệm & Đánh giá; phá hòa tất định `GS-G01` trước `GS-T06`. |
| **KB03** | Vật Lý \| Trực tiếp \| Quận 3 \| 250.000đ \| Tất cả Trung bình ($w=2$) | `1. GS-G04 (0,829)`<br/>`2. GS-G05 (0,795)` | `1. GS-G04 (0,829)`<br/>`2. GS-G05 (0,795)` | **2/2** | Khớp tuyệt đối cả thứ hạng và điểm số. |
| **KB04** | Anh Văn \| Trực tuyến \| 220.000đ \| `T2-tối, T4-tối` \| Tất cả Trung bình ($w=2$) | `1. GS-G03 (0,848)`<br/>`2. GS-G13 (0,715)` | `1. GS-G03 (0,886)`<br/>`2. GS-G13 (0,786)` | **2/2** | Khớp thứ hạng 2/2 (`GS-G03 > GS-G13`). Điểm hệ thống tính đủ 4 tiêu chí đang áp dụng (có `availability`); xem giải trình ở Mục 4.2. |
| **KB05** | Tin học \| Trực tiếp \| Quận 1 \| 200.000đ \| `CN-tối` | `Không có gia sư thỏa điều kiện` | `status = "no_match"` (`total_After_filter = 0`) | **Đạt** | Hệ thống trả về đúng thông báo không có gia sư thỏa điều kiện bắt buộc. |
| **KB06** | Ngữ Văn \| Không yêu cầu \| Quận 3 \| 200.000đ \| Tất cả Trung bình ($w=2$) | `1. GS-G14 (0,931)` | `1. GS-G14 (0,931)` | **1/1** | Khớp tuyệt đối cả thứ hạng và điểm số. |
| **KB07** | Sinh \| Trực tiếp \| Gò Vấp \| 180.000đ \| Tất cả Trung bình ($w=2$) | `1. GS-G07 (0,948)` | `1. GS-G07 (0,948)` | **1/1** | Khớp tuyệt đối cả thứ hạng và điểm số. |
| **KB08** | Tin học \| Không yêu cầu \| Quận 1 \| 250.000đ \| Tất cả Trung bình ($w=2$) | `1. GS-G07 (0,876)` | `1. GS-G07 (0,876)` | **1/1** | Khớp tuyệt đối cả thứ hạng và điểm số (`0,87625`). |
| **KB09** | Tiếng Nhật \| Không yêu cầu \| Phú Nhuận \| 280.000đ \| Tất cả Trung bình ($w=2$) | `1. GS-G08 (0,928)` | `1. GS-G08 (0,9275)` | **1/1** | Khớp thứ hạng 1/1; giá trị chính xác $3{,}71 / 4 = 0{,}9275$ (làm tròn thập phân thông thường thành `0,928`). |
| **KB10** | Toán \| Trực tiếp \| Quận 7 \| `exp=Cao`, còn lại Trung bình | `1. GS-G10 (0,994)`<br/>`2. GS-G01 (0,607)`<br/>`3. GS-G09 (0,593)` | `1. GS-G10 (0,994)`<br/>`2. GS-G01 (0,607)`<br/>`3. GS-G09 (0,593)` | **3/3** | Khớp tuyệt đối; `GS-T06` (`0,571`) đứng hạng 4 ngoài Top-3 đúng như phân tích đề cương. |
| **KB11** | Hóa \| Trực tiếp \| Quận 10 \| 220.000đ \| Tất cả Trung bình ($w=2$) | `1. GS-G06 (0,985)`<br/>`2. GS-T06 (0,375)` | `1. GS-G06 (0,985)`<br/>`2. GS-T06 (0,375)` | **2/2** | Khớp tuyệt đối cả thứ hạng và điểm số. |
| **KB12** | Anh Văn \| Trực tiếp \| Bình Chánh \| 200.000đ \| Tất cả Trung bình ($w=2$) | `1. GS-T07 (0,8125)`<br/>`2–3. GS-G11 = GS-G12 (0,631, đồng hạng)` | `1. GS-T07 (0,8125)`<br/>`2. GS-G11 (0,631)`<br/>`3. GS-G12 (0,631)` | **3/3** | Khớp tuyệt đối; hồ sơ thu thập công khai `GS-T07` đứng hạng 1 nhờ đúng khu vực Bình Chánh và học phí trong ngân sách. |
| **KB13** | Toán \| Không yêu cầu \| 150.000đ \| Tất cả Trung bình ($w=2$) | `1. GS-G10 (0,993)`<br/>`2. GS-G01 (0,783)`<br/>`3. GS-T06 (0,50)` | `1. GS-G10 (0,993)`<br/>`2. GS-G01 (0,783)`<br/>`3. GS-T06 (0,500)` | **3/3** | Khớp tuyệt đối cả thứ hạng và điểm số. |
| **KB14** | Anh Văn \| Trực tuyến \| Tất cả Trung bình ($w=2$) | `1. GS-G03 (0,70)` | `1. GS-G03 (0,700)` | **1/1** | Khớp tuyệt đối cả thứ hạng và điểm số. |

### 4.2. Giải trình trung thực các phát hiện số học (chi tiết tại `docs/thesis/report/discrepancy_analysis.md`)

Tuân thủ nguyên tắc tại Mục 5.2 của đề cương (*"tránh chỉnh cho khớp mà không giải thích"*), nhóm giữ nguyên bất biến tệp `scenarios.json` và ghi nhận minh bạch:
1. **Sự khác biệt phần thập phân tại `KB04` (`0,886 / 0,786` so với `0,848 / 0,715`):**
   - Truy vấn `KB04` chọn học `Trực tuyến` (loại `district`), không nhập khu vực, có nhập ngân sách `220.000đ` và khung giờ `L = {T2-tối, T4-tối}`. Do đó có **4 tiêu chí ưu tiên đang áp dụng**: `fee`, `experience`, `rating` và `availability` (cùng $w = 2$).
   - Cả hai ứng viên `GS-G03` (mã đề cương `GS006`) và `GS-G13` (mã đề cương `GS020`) đều khớp toàn bộ $2/2$ khung giờ ($s_{\text{avail}} = 1{,}00$). Khi tính đủ 4 tiêu chí, điểm tổng là $S(\text{GS-G03}) = (1{,}00 + 0{,}625 + 0{,}92 + 1{,}00)/4 = 0{,}88625 \approx 0{,}886$ và $S(\text{GS-G13}) = (1{,}00 + 0{,}50 + 0{,}645 + 1{,}00)/4 \approx 0{,}786$.
   - Con số `0,848` và `0,715` trong bản tính tay ban đầu ở đề cương là trung bình cộng của 3 tiêu chí (`fee`, `experience`, `rating`) khi sơ suất quên cộng $s_{\text{avail}} = 1{,}00$. Vì cả hai ứng viên đều có cùng $s_{\text{avail}} = 1{,}00$, thứ hạng **`1. GS-G03 > 2. GS-G13` hoàn toàn không thay đổi**.
2. **Quy tắc làm tròn tại `KB09` (`0,9275`):** Điểm chính xác của `GS-G08` là $3{,}71 / 4 = 0{,}9275$ (làm tròn half-up 3 chữ số là `0,928` như đề cương; làm tròn half-to-even IEEE-754 là `0,927`).
3. **Vai trò của 2 hồ sơ thu thập công khai (`GS-T06`, `GS-T07`):** Xuất hiện trực tiếp trong Top-3 của 5 kịch bản (`KB01`, `KB02`, `KB11`, `KB12`, `KB13`), trong đó `GS-T07` xếp hạng 1 tại `KB12` và luôn gắn ghi chú `"chưa có đánh giá"` (sử dụng điểm trung tính $0{,}5$) đúng như thiết kế.

---

## 5. Kế hoạch công việc giai đoạn cuối kỳ (Sprint 6 — 9 SP Must, hướng tới Cổng chất lượng 4 & `v1.0`)

Trong giai đoạn cuối kỳ (Milestone Sprint 6, hạn `2027-01-01`, đã lập kế hoạch tại `docs/scrum/sprints/sprint-06/planning.md`), nhóm tập trung hoàn thành 5 User Stories bắt buộc còn lại (`#32`–`#36`):

1. **`US-30` (#32 — 2 SP Must, Mục 5.2):** Viết bộ kiểm thử thực nghiệm tự động khảo sát độ nhạy của tham số phạt học phí $\delta$, kinh nghiệm trần $E_{\max}$, biến động ngân sách ($\pm 5\%, \pm 10\%, \pm 20\%$) và lập bảng so sánh thứ hạng dưới nhiều bộ mức ưu tiên trên dữ liệu thực theo tinh thần Bảng 2.2; xuất báo cáo `docs/thesis/report/muc-5.2-danh-gia-do-on-dinh.md`.
2. **`US-33` (#33 — 3 SP Must, Chương 5 & Chương 6):** Soạn thảo hoàn chỉnh toàn văn Chương 5 (`chuong-05-thuc-nghiem-va-danh-gia.md`, gồm Mục 5.1, Bảng 5.1, Mục 5.2, Mục 5.3 hạn chế thực tế) và Chương 6 (`chuong-06-ket-luan-va-huong-phat-trien.md`, gồm Mục 6.1 kết quả đạt được, Mục 6.2 ba hướng phát triển, Mục 6.3 tự đánh giá Bảng 6.1, cùng Phụ lục A, B, C, D).
3. **`US-34` (#34 — 1 SP Must, Mục 4.1 & Phụ lục B):** Cập nhật toàn diện tài liệu `README.md` gốc và các `README.md` thành phần kèm hình ảnh minh họa giao diện để người chấm có thể cài đặt và chạy thử nghiệm trong 5 phút.
4. **`US-35` (#35 — 2 SP Must):** Thiết kế bộ slide thuyết trình bảo vệ đồ án và kịch bản phân vai demo trực tiếp 3 chức năng CN01–CN03 cho 3 thành viên tại `docs/thesis/slides/`.
5. **`US-36` (#36 — 1 SP Must):** Đồng bộ Mục lục, Danh mục hình ảnh, Danh mục bảng biểu, làm sạch repository và gắn git tag phát hành chính thức `v1.0` trên GitHub.

---

## 6. Các nội dung xin ý kiến chỉ đạo của Giảng viên hướng dẫn

Nhóm kính mong Cô xem xét kết quả thực hiện giữa kỳ và cho nhóm ý kiến chỉ đạo về **3 nội dung** để nhóm hoàn thiện báo cáo cuối kỳ ở Sprint 6:

1. **Về cách trình bày số liệu của kịch bản `KB04` trong Bảng 5.1 của cuốn báo cáo chính thức:**
   - Nhóm đề xuất giữ nguyên cột *"Top-3 kỳ vọng"* theo đề cương gốc (`1. GS006 (0,848); 2. GS020 (0,715)`), ghi giá trị thực chạy 4 tiêu chí ở cột *"Top-3 hệ thống"* (`1. GS-G03 / GS006 (0,886); 2. GS-G13 / GS020 (0,786)`), và đặt chú thích giải trình rõ nguyên nhân toán học (tính đủ tiêu chí `availability`) ngay bên dưới Bảng 5.1 để đảm bảo tính trung thực thực nghiệm.
2. **Về phạm vi khảo sát độ nhạy tham số tại Mục 5.2 (`US-30`):**
   - Nhóm dự kiến thực hiện 3 phép thử độ nhạy trên tập dữ liệu thật: *(a)* Biến thiên hệ số dung sai học phí $\delta \in \{0{,}25;\, 0{,}30;\, 0{,}50;\, 0{,}70;\, 0{,}75;\, 1{,}00\}$; *(b)* Biến thiên mức trần kinh nghiệm $E_{\max} \in \{5,\, 6,\, 8,\, 10,\, 12\}$; *(c)* Biến thiên ngân sách $\{-20\%,\, -10\%,\, -5\%,\, +5\%,\, +10\%,\, +20\%\}$ và bảng đối chiếu thứ hạng dưới 3–4 bộ mức ưu tiên khác nhau theo mẫu Bảng 2.2. Kính xin ý kiến Cô xem phạm vi thực nghiệm này đã phù hợp với yêu cầu của Mục 5.2 chưa.
3. **Về mốc thời gian gửi bản thảo toàn văn Chương 5 – Chương 6 và buổi duyệt demo:**
   - Nhóm xin ý kiến Cô về lịch nộp bản thảo báo cáo cuối kỳ để Cô đọc duyệt trước khi nhóm đóng gói hồ sơ `v1.0`.

---

## 7. Biên bản ghi nhận ý kiến phản hồi của Giảng viên hướng dẫn

- **Giảng viên hướng dẫn:** TS. Lê Anh Nhã Uyên
- **Ngày báo cáo tiến độ giữa kỳ:** *[Chờ nhóm điền]*
- **Kênh trao đổi:** *[Tin nhắn Zalo / Email / Gặp trực tiếp — chờ nhóm điền]*
- **Ý kiến nhận xét và chỉ đạo của Giảng viên hướng dẫn:**
  1. Về tiến độ thực hiện giữa kỳ (Chương 4, Mục 5.1 và Bảng 5.1): *[Chờ nhóm cập nhật sau khi nhận phản hồi của Cô]*
  2. Về cách trình bày Bảng 5.1 và phạm vi khảo sát độ nhạy Mục 5.2: *[Chờ nhóm cập nhật sau khi nhận phản hồi của Cô]*
  3. Các yêu cầu bổ sung hoặc điều chỉnh cho giai đoạn cuối kỳ (Sprint 6): *[Chờ nhóm cập nhật sau khi nhận phản hồi của Cô]*
- **Minh chứng trao đổi:** *[Chờ nhóm đính kèm ảnh chụp hoặc trích xuất tin nhắn xác nhận nếu cần]*
