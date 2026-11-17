# CHƯƠNG 4. XÂY DỰNG HỆ THỐNG

Chương này trình bày quá trình hiện thực hệ thống khuyến nghị gia sư thuộc đề tài “Hệ thống khuyến nghị gia sư dựa trên phương pháp Content-Base Filtering” theo sáu mục của kế hoạch hiện thực trong đề cương: chuẩn bị môi trường phát triển (Mục 4.1), xây dựng tập dữ liệu mẫu (Mục 4.2), cài đặt module tính điểm (Mục 4.3), xây dựng API khuyến nghị (Mục 4.4), xây dựng giao diện demo (Mục 4.5) và tích hợp giao diện với API cùng kiểm tra luồng end-to-end (Mục 4.6). Mô tả trong chương phản ánh đúng phần mềm đã hiện thực trong kho mã nguồn. Mọi tên tệp, tên hàm và phiên bản phần mềm nêu dưới đây đều truy ngược được về tệp cấu hình hoặc kết quả kiểm chứng trực tiếp. Những điểm mà hiện thực khác với kế hoạch dự kiến trong đề cương (ví dụ cơ sở dữ liệu SQLite) được nêu thẳng tại từng mục. Số liệu kiểm thử định lượng không lặp lại trong chương này mà trình bày tại Chương 5.

---

## 4.1. Chuẩn bị môi trường phát triển

Nhóm tách hệ thống thành hai thư mục độc lập: `backend/` (dịch vụ API) và `frontend/` (giao diện), cùng thư mục dữ liệu dùng chung `data/processed/`. Phiên bản các thư viện được ghim tĩnh: phía Python bằng tệp `backend/requirements.txt` và `backend/requirements-dev.txt` (phiên bản ghim từ `pip freeze` của môi trường Python 3.12), phía JavaScript bằng `frontend/package.json` và `frontend/package-lock.json`.

Bảng 4.1 tóm tắt thành phần và phiên bản của từng công nghệ tại thời điểm hiện thực.

**Bảng 4.1 - Thành phần và công nghệ của hệ thống tại thời điểm hiện thực**

| Thành phần | Công nghệ (phiên bản) | Vai trò |
|:---|:---|:---|
| Nền tảng backend | Python 3.12.7 (môi trường ảo `.venv`; đo bằng `python --version`) | Nền tảng chạy dịch vụ và kiểm thử |
| Khung API | FastAPI 0.162.0 | Định nghĩa endpoint, sinh tài liệu OpenAPI |
| Xác thực dữ liệu | Pydantic 2.14.2 | Mô hình hóa hồ sơ, yêu cầu và phản hồi; kiểm tra ràng buộc đầu vào |
| Máy chủ ASGI | Uvicorn 0.54.0 (gói `uvicorn[standard]`) | Khởi chạy dịch vụ HTTP |
| Nền tảng frontend | Node.js (yêu cầu `^20.19.0 \|\| >=22.12.0` theo README; máy nhóm chạy Node v24.19.0, npm 11.17.0) | Môi trường dựng và đóng gói |
| Thư viện giao diện | React 19.3.1, React DOM 19.3.1 | Giao diện Single Page Application hai màn hình |
| Công cụ dựng | Vite 8.3.5, `@vitejs/plugin-react` 6.1.2 | Build và phát triển cục bộ (sinh thư mục `dist/`) |
| Hiệu ứng chuyển cảnh | motion 14.9.0 | Chuyển động giữa hai màn hình, thanh xếp chồng, huy hiệu biến động hạng |
| Lưu trữ dữ liệu | Tệp `data/processed/tutors.json` và `tutors.csv` | 16 hồ sơ gia sư chuẩn hóa (không dùng cơ sở dữ liệu, xem Mục 4.2) |

*Ghi chú:* `frontend/package.json` còn khai báo thư viện `boring-avatars` 2.0.4 nhưng trong mã nguồn `frontend/src/` không có tệp nào import thư viện này; thành phần avatar `TutorAvatar.jsx` tự dựng ảnh chân dung WebP kèm fallback (Mục 4.5).

*Nguồn: `backend/requirements.txt`, `backend/requirements-dev.txt`, `frontend/package.json`, `frontend/package-lock.json` (`lockfileVersion` 3; `react` 19.3.1, `vite` 8.3.5, `@vitejs/plugin-react` 6.1.2, `motion` 14.9.0, `oxlint` 1.90.0); đo lường môi trường bằng lệnh `python --version`, `node --version`, `npm --version`.*

Về công cụ chất lượng, phía backend dùng `pytest` 9.2.0 (cấu hình tại `backend/pytest.ini` với `testpaths = tests` và `pythonpath = .`) và `pytest-cov` 7.1.0 để đo độ bao phủ. Backend cũng dùng `httpx` 0.28.1 (cung cấp `TestClient` cho kiểm thử tích hợp API) và `ruff` 0.17.3 để kiểm tra định dạng mã nguồn. Phía frontend dùng `oxlint` 1.90.0 với cấu hình `frontend/.oxlintrc.json` (kích hoạt quy tắc `react/rules-of-hooks` ở mức error) và hai script `npm run lint`, `npm run build`.

Trình tự kiểm tra chất lượng được tự động hóa bằng GitHub Actions tại `.github/workflows/ci.yml` (workflow `CI backend`) cho mỗi `push` vào nhánh `main` và mỗi pull request. Workflow dựng môi trường `ubuntu-latest`, cài Python 3.12 (có cache pip theo hai tệp requirements), cài phụ thuộc, rồi chạy `ruff check .` và `pytest` trong thư mục `backend/`. Giới hạn hiện tại là CI chỉ bao phủ backend; frontend chưa có job riêng trong CI (`oxlint` và `vite build` chạy từ terminal theo `README.md` mục 7). Cấu trúc thư mục chi tiết và ánh xạ vào đề cương đã trình bày ở `README.md` mục 3 nên chương này không lặp lại.

## 4.2. Xây dựng tập dữ liệu mẫu

### 4.2.1. Định dạng lưu trữ

Dữ liệu được lưu bằng hai tệp đồng bộ: `data/processed/tutors.json` (nạp cho chương trình) và `data/processed/tutors.csv` (đối chiếu bằng mắt, phục vụ Phụ lục A). Đề cương thiết kế cho phép lưu bằng “JSON/CSV hoặc SQLite”; hiện thực cuối cùng chỉ dùng JSON và CSV vì bộ dữ liệu gồm bản ghi phẳng 9 trường theo Bảng 3.3, không có quan hệ nhiều bảng cần cơ sở dữ liệu quan hệ (theo Mục 3.5). Phương án chuyển sang “bảng SQLite đơn” được xếp ở mức ưu tiên thấp (*Could Have*) trong lộ trình dự án nên chưa triển khai; hai docstring ở `backend/app/data/repository.py` và `backend/app/core/config.py` vẫn nhắc tên SQLite như phương án dự kiến, còn lớp `TutorRepository` mới đọc tệp JSON.

### 4.2.2. Cấu trúc dữ liệu

Cấu trúc bản ghi được mã hóa thành các mô hình Pydantic tại `backend/app/schemas/`, ánh xạ từ Bảng 3.3 và Bảng 3.4 của đề cương theo `docs/design/data-dictionary.md`. Từ điển dữ liệu này chuyển tên trường tiếng Việt sang định danh tiếng Anh thống nhất trong toàn bộ hệ thống.

Bảng 4.2 trích rút gọn các ánh xạ chính; từ điển đầy đủ nằm tại `docs/design/data-dictionary.md`.

**Bảng 4.2 - Ánh xạ trường dữ liệu đề cương sang định danh trong code (rút gọn từ data-dictionary.md)**

| Nhóm | Trường trong đề cương | Định danh trong code | Kiểu trong code |
|:---|:---|:---|:---|
| Hồ sơ gia sư (Bảng 3.3) | `id` | `tutor_id` | `string` |
| | `môn_dạy` | `subjects` | `list[string]` |
| | `khu_vực` | `districts` | `list[string]` (rỗng nếu chỉ dạy trực tuyến) |
| | `học_phí_giờ` | `hourly_fee_vnd` | `int \| None` |
| | `số_năm_kinh_nghiệm` | `years_experience` | `float \| None` |
| | `hình_thức_dạy` | `teaching_mode` | enum `in_person`, `online`, `both` |
| | `lịch_rảnh` | `availability` | `list[string]` |
| | `điểm_đánh_giá_tb` | `avg_rating` | `float \| None` (`null` nếu chưa có đánh giá) |
| | `nguồn_dữ_liệu` | `data_source` | enum `public_collected`, `simulated`, `estimated` |
| Nhu cầu người học (Bảng 3.4) | `môn_học` | `subject` | `string` (bắt buộc, không chỉ khoảng trắng) |
| | `hình_thức_học` | `learning_mode` | enum `in_person`, `online`, `any` |
| | `khu_vực_mong_muốn` | `preferred_district` | `string \| None` |
| | `ngân_sách_tối_đa` | `max_budget_vnd` | `StrictInt \| None` (`ge = 0`) |
| | `khung_thời_gian` | `time_slots` | `list[string] \| None` |
| | `mức_ưu_tiên` | `priorities` | `dict[enum tiêu chí, enum none/low/medium/high]` |
| | (thêm so với đề cương) | `top_k` | `StrictInt`, mặc định 3, ràng buộc $1 \le \text{top\_k} \le 20$ |

Hai mô hình đều đặt `extra="forbid"` — bản ghi chứa trường thừa sẽ bị từ chối, giúp phát hiện sớm sai lệch cấu trúc dữ liệu. Trường `top_k` là bổ sung so với Bảng 3.4, thuộc hợp đồng API (giới hạn 1–20, trả về mã HTTP 422 khi vi phạm).

*Nguồn: `docs/design/data-dictionary.md`; `backend/app/schemas/tutor.py`, `backend/app/schemas/search_request.py` (các ràng buộc `Field`, `StrictInt`, `field_validator`).*

### 4.2.3. Nguồn và nhãn dữ liệu

Tập dữ liệu gồm đúng 16 hồ sơ: 2 hồ sơ thu thập công khai `GS-T06`, `GS-T07` (nhãn `public_collected`) và 14 hồ sơ mô phỏng `GS006`, `GS020`, `GS-G01` đến `GS-G12` (nhãn `simulated`). Theo `data/README.md` mục 3, môn dạy, khu vực và số năm kinh nghiệm của hai hồ sơ thu thập là số liệu thật đã ẩn danh. Học phí và lịch rảnh là ước tính của nhóm (nội suy theo số năm kinh nghiệm từ khoảng giá khảo sát tại daythem.com 130.000–400.000 VNĐ/giờ; lịch rảnh giả định theo các khung giờ phổ biến), được đánh dấu hoa thị `(*)` ở Phụ lục A. Điểm đánh giá trung bình của hai hồ sơ này để trống và nhận giá trị trung tính $0{,}5$ khi tính điểm. Tài liệu `data/README.md` mục 3 cũng ghi nhận rằng nhãn `estimated` chưa được áp dụng cho hai hồ sơ ước tính; trường `data_source` giữ nguyên `public_collected` theo Phụ lục A.

Tài liệu `data/README.md` mục 4 ghi nhận một hiệu chỉnh dữ liệu ngày 01/11/2026: nhãn môn dạy của `GS-G03` sửa từ “Tiếng Anh” thành “Anh Văn” để đồng nhất với các hồ sơ tiếng Anh khác và giúp kịch bản KB14 có ứng viên. Kiểm tra trực tiếp tệp `tutors.json` xác nhận `GS-G03` mang giá trị `subjects: ["Anh Văn"]`.

### 4.2.4. Kiểm tra toàn vẹn dữ liệu

Script `scripts/validate_tutors.py` (chỉ đọc, không chứa công thức tính điểm) kiểm tra năm nhóm điều kiện trên bộ dữ liệu mẫu:
- Số lượng bản ghi và tỷ lệ nguồn dữ liệu.
- Tính duy nhất của `tutor_id` trong cả JSON và CSV.
- Đủ 9 trường với kiểu dữ liệu và enum hợp lệ.
- Không chứa thông tin định danh cá nhân (số điện thoại, email, từ khóa liên hệ) theo nguyên tắc ẩn danh ở Mục 3.5.
- Khớp từng ô giữa tệp JSON và CSV.

Kết quả chạy kiểm tra (Python 3.12.7):

```text
ĐẠT: 16 bản ghi (2 public_collected, 14 simulated); id duy nhất; enum hợp lệ;
     đủ 9 trường; không có thông tin liên hệ; JSON và CSV khớp nhau từng ô.
```

### 4.2.5. Nguyên tắc thiết kế dữ liệu và minh chứng trong 16 hồ sơ

Bốn nguyên tắc thiết kế dữ liệu được thể hiện cụ thể qua 16 hồ sơ trong `data/processed/tutors.json`:

1. **Tạo xung đột tiêu chí:** cặp `GS-G09` (học phí 350.000, kinh nghiệm 2 năm, đánh giá 3,5) và `GS-G10` (130.000, 12 năm, 4,9) cùng dạy Toán, nhận Quận 7 và rảnh T2-tối, T4-tối. Người học ưu tiên học phí và người ưu tiên kinh nghiệm sẽ chọn khác nhau; cặp `GS-G01` (180.000, 6 năm, 5,0) và `GS-G02` (300.000, 3 năm, 3,0) tại Bình Thạnh có cấu trúc tương tự.
2. **Cặp chỉ khác một tiêu chí:** `GS006` và `GS020` giống nhau ở mọi trường, chỉ khác học phí (190.000 so với 240.000). Cặp `GS-G11` và `GS-G12` cũng chỉ khác nhau ở khu vực (Quận 2 + Bình Thạnh so với Quận 2 + Thủ Đức), được dùng trực tiếp trong KB02 (đồng điểm, phá hòa theo `tutor_id`) và KB03 (tách hạng nhờ khớp khu vực Thủ Đức).
3. **Tình huống không ai thỏa điều kiện bắt buộc:** không hồ sơ nào dạy môn Tiếng Trung trong khi danh sách môn trên giao diện có lựa chọn này. Khi gọi API thật với `subject = "Tiếng Trung"`, hệ thống trả về trạng thái `no_match` (Mục 4.4), tương ứng kịch bản KB05.
4. **Gia sư chưa có đánh giá:** `GS-T06` và `GS-T07` có `avg_rating = null`, được gán điểm trung tính $0{,}5$ kèm ghi chú “chưa có đánh giá” trong phản hồi API (xác nhận trong output ở Mục 4.3 và Mục 4.4).

## 4.3. Cài đặt module tính điểm

Module tính điểm nằm trong gói `backend/app/scoring/` và được thiết kế tách rời khỏi tầng API. Bảng 4.3 ánh xạ từng tệp với hàm/lớp chính và bước tương ứng trong quy trình tính điểm 4 bước của Mục 3.6.

**Bảng 4.3 - Tệp, hàm/lớp chính và bước quy trình tương ứng (Mục 3.6)**

| Tệp | Hàm / lớp chính | Vai trò trong quy trình Mục 3.6 |
|:---|:---|:---|
| `app/data/repository.py` | `TutorRepository.get_all`, `_parse_record`, ngoại lệ `TutorDataError` | Truy xuất 16 hồ sơ JSON, xác thực từng bản ghi theo `TutorProfile` |
| `app/scoring/filters.py` | `filter_mandatory`, `_matches_subject`, `_matches_mode`, `_matches_availability` | Bước 2 — lọc điều kiện bắt buộc (môn học, hình thức, $\lvert L \cap T \rvert \ge 1$) |
| `app/scoring/weights.py` | `compute_effective_weights`, `priority_to_weight`, `_applicable_criteria`, `EffectiveWeights` | Quy đổi mức ưu tiên sang trọng số theo Bảng 3.5; xác định tiêu chí áp dụng (loại tiêu chí không nhập dữ liệu và $w = 0$) |
| `app/scoring/eligibility.py` | `check_tutor_eligibility`, `count_available_criteria`, `filter_eligible_candidates`, `MIN_DATA_THRESHOLD` | Kiểm tra ngưỡng dữ liệu tối thiểu để xếp hạng (bảng ngưỡng theo $n = 1\text{–}5$), giữa Bước 2 và Bước 4 |
| `app/scoring/criteria.py` | `score_fee`, `score_location`, `score_experience`, `score_rating`, `score_schedule` | Bước 3 — năm hàm thuần tính điểm thành phần $s_i \in [0, 1]$ theo Bảng 3.6 |
| `app/scoring/ranker.py` | `score_and_rank`, `_compute_single_criterion_score`, `build_reason`, `build_notes` | Bước 4 — tổng hợp $S = \sum w_i \cdot s_i / \sum w_i$, đóng góp $C_i$, sắp xếp giảm dần (phá hòa theo `tutor_id`), trích Top-$k$ |
| `app/core/config.py` | `DELTA = 0.5`, `E_MAX = 8`, `RATING_DEFAULT = 0.5`, `PRIORITY_WEIGHTS = {"none": 0, "low": 1, "medium": 2, "high": 3}`, `DEFAULT_PRIORITY = "medium"`, `CRITERIA_KEYS` | Tham số thuật toán theo Mục 3.6 và Bảng 3.5 |

Ba bước trong quy trình (Bước 2, Bước 3, Bước 4) được gọi bằng đúng hàm của module scoring. Bước 1 (kiểm tra và chuẩn hóa đầu vào) do mô hình `SearchRequest` của Pydantic đảm nhận, kèm các ngoại lệ `ValueError` trong hàm thuần (quyết định QĐ-B dưới đây); lớp `repository.py` cung cấp dữ liệu đầu vào cho Bước 2.

*Nguồn: docstring đầu mỗi tệp trong `backend/app/scoring/`, `backend/app/core/config.py`, `backend/app/data/repository.py`; đối chiếu quy trình 4 bước tại `docs/design/scoring-spec.md` mục 1.*

### 4.3.1. Các quyết định triển khai QĐ-A đến QĐ-E

Năm quyết định triển khai phát sinh khi Bảng 3.6 chưa nêu tường minh các trường hợp biên; nội dung năm quyết định này được ghi nhận trong docstring, bộ kiểm thử và biên bản sprint như sau:

- **QĐ-A — Ngân sách bằng 0:** khi $B = 0$, học phí $P = 0$ nhận điểm $1$, $P > 0$ nhận điểm $0$, tránh phép chia cho $\delta \times B = 0$. Nguồn: docstring `score_fee` (`criteria.py` dòng 24), `backend/tests/unit/test_criteria.py` (hai test QĐ-A với $B = 0$), `docs/scrum/sprints/sprint-02/planning.md`.
- **QĐ-B — Kiểm tra miền đầu vào bằng ngoại lệ `ValueError`:** `score_fee` ném lỗi khi $P < 0$ hoặc $B < 0$, còn `score_experience` ném lỗi khi $E < 0$. Tương tự, `score_rating` chặn $R$ ngoài đoạn $[0, 5]$ và `score_schedule` chặn tập khung giờ người học rỗng. Nguồn: docstring và thân hàm trong `criteria.py`, nhóm test “Đầu vào ngoài miền hợp lệ (QĐ-B)” trong `test_criteria.py`.
- **QĐ-C — Loại bỏ tiêu chí khu vực khi học trực tuyến tại `weights.py`:** `score_location` chỉ chấm $1$ hoặc $0$. Tiêu chí khu vực bị loại khỏi tập áp dụng do `_applicable_criteria` trong `weights.py` (khi `learning_mode = "online"` hoặc không nhập khu vực). Nguồn: docstring `score_location` (`criteria.py` dòng 40–41) và thân `weights.py`.
- **QĐ-D — So khớp chuỗi chính xác, phân biệt hoa/thường:** so khớp môn học, khu vực và khung giờ dùng phép so chuỗi chính xác (`subject in tutor.subjects`, phép giao tập khung giờ), không chuẩn hóa hoa/thường. Nguồn: docstring `score_location`, `test_criteria.py` (test QĐ-D “không chuẩn hóa hoa/thường”), `test_filters.py`.
- **QĐ-E — Không làm tròn trung gian:** phép tính giữ giá trị số thực đầy đủ; làm tròn chỉ thực hiện khi hiển thị (3 chữ số thập phân). Nguồn: `docs/design/api-contract.md` mục 5.2, `docs/thesis/report/discrepancy_analysis.md`, `docs/scrum/sprints/sprint-02/retrospective.md` (nhóm quyết định QĐ-A–QĐ-E).

### 4.3.2. Tính tách rời khỏi tầng API

Module scoring không phụ thuộc khung web: tra cứu từ khóa (`fastapi|starlette|uvicorn`) trên toàn bộ `backend/app/scoring/` trả về rỗng. Toàn bộ khối `import` trong năm tệp của gói này chỉ gồm thư viện chuẩn (`collections.abc`, `dataclasses`) và các mô-đun nội bộ (`app.core.config`, `app.schemas.*`, `app.scoring.*`), nhờ đó module tính điểm chạy được độc lập qua lời gọi hàm trực tiếp mà không cần HTTP.

### 4.3.3. Ví dụ chạy thật: kịch bản KB01

Chạy kiểm chứng trực tiếp pipeline tính điểm (gọi lần lượt `filter_mandatory` → `compute_effective_weights` → `filter_eligible_candidates` → `score_and_rank` trên 16 hồ sơ) cho kịch bản KB01 (Toán, trực tiếp, Bình Thạnh, ngân sách 200.000 VNĐ/giờ, mọi mức ưu tiên Trung bình, `top_k = 3`), kết quả rút gọn như sau:

```text
total_candidates: 16
qualified_candidates: 5  [GS-T06, GS-G01, GS-G02, GS-G09, GS-G10]
insufficient_data_candidates: []
effective weights: {'fee': 2, 'district': 2, 'experience': 2, 'rating': 2}  total: 8
rank=1 tutor_id=GS-G01 total_score=0.9375
  criteria_scores: fee 1.0 | district 1.0 | experience 0.75 | rating 1.0 | availability None
  contributions:   fee 0.25 | district 0.25 | experience 0.1875 | rating 0.25 | availability None
  reason: "Học phí trong ngân sách, khu vực khớp, đánh giá 5,0/5"
rank=2 tutor_id=GS-G10 total_score=0.745
  criteria_scores: fee 1.0 | district 0.0 | experience 1.0 | rating 0.98 | availability None
rank=3 tutor_id=GS-T06 total_score=0.625
  criteria_scores: fee 0.0 | district 1.0 | experience 1.0 | rating 0.5 | availability None
  notes: ['chưa có đánh giá']
```

Kết quả minh họa các cơ chế đã cài đặt: tiêu chí lịch rảnh không áp dụng vì KB01 không nhập khung giờ (giá trị `null`). Hồ sơ `GS-T06` có học phí ước tính 400.000 nên `s_fee = 0` nhưng không bị loại cứng; việc thiếu đánh giá nhận điểm trung tính $0{,}5$ kèm ghi chú. Dãy điểm này khớp đúng với Bảng 5.9 của Chương 5.

## 4.4. Xây dựng API khuyến nghị

### 4.4.1. Endpoint và cấu trúc ứng dụng

Dịch vụ được khai báo trong `backend/app/main.py`: khởi tạo ứng dụng FastAPI, đăng ký `CORSMiddleware` (mở mọi origin và phương thức cho frontend từ Vercel) và gắn router từ `backend/app/api/recommend.py`. Dịch vụ kèm endpoint kiểm tra sức khỏe `GET /health` trả về `{"status": "ok"}`, cùng tài liệu tương tác Swagger UI tự sinh tại `/docs`.

Endpoint chính `POST /api/recommend` (hàm `recommend_tutors`) nhận `SearchRequest` và trả về `RecommendationResponse` — kiểu hợp (*union*) của ba mô hình `RecommendationSuccessResponse`, `NoMatchResponse`, `ZeroWeightResponse` trong `backend/app/schemas/recommendation.py`. Quy trình xử lý theo đúng thứ tự 5 bước của `docs/design/api-contract.md` mục 6:

1. Kiểm tra đầu vào bằng ràng buộc Pydantic trên `SearchRequest` (môn học không chỉ gồm khoảng trắng, `max_budget_vnd` nguyên không âm, `top_k` từ 1 đến 20, giá trị enum hợp lệ, từ chối khóa `priorities` lạ và trường thừa) — vi phạm trả về mã HTTP 422.
2. Lọc bắt buộc qua `filter_mandatory`; nếu rỗng trả về trạng thái `no_match` với thông báo “Không có gia sư thỏa điều kiện bắt buộc”.
3. Kiểm tra tổng trọng số qua `compute_effective_weights`; nếu tổng bằng $0$ trả về trạng thái `zero_weight` kèm `unranked_candidates`.
4. Áp ngưỡng dữ liệu qua `filter_eligible_candidates`; nếu mọi ứng viên bị loại trả về biến thể `no_match` với thông báo “Có gia sư thỏa điều kiện bắt buộc nhưng không đủ dữ liệu để xếp hạng” kèm `insufficient_data_candidates`.
5. Tính điểm, xếp hạng, lấy Top-$k$ bằng `score_and_rank` với `top_k` của yêu cầu.

Lớp truy xuất dữ liệu được cấp qua cơ chế *dependency injection* của FastAPI: hàm `get_tutor_repository()` trả về `TutorRepository()`, gắn vào endpoint bằng `Annotated[TutorRepository, Depends(get_tutor_repository)]`. Cách làm này cho phép thay thế nguồn dữ liệu bằng dependency override trong bộ test API mà không sửa mã endpoint.

Bốn trạng thái phản hồi cùng điều kiện phát sinh tương ứng được tổng hợp ở Bảng 4.4.

**Bảng 4.4 - Các trạng thái phản hồi của `POST /api/recommend`**

| Trạng thái | Điều kiện phát sinh | Mã HTTP |
|:---|:---|:---:|
| `success` | Có ít nhất một gia sư qua lọc, đủ ngưỡng dữ liệu và xếp hạng được | 200 |
| `no_match` (biến thể 1) | Không có gia sư nào thỏa điều kiện bắt buộc | 200 |
| `no_match` (biến thể 2) | Có gia sư qua lọc bắt buộc nhưng tất cả bị loại do thiếu dữ liệu (kèm `insufficient_data_candidates` không rỗng) | 200 |
| `zero_weight` | Tổng trọng số các tiêu chí đang áp dụng bằng 0 (kèm `unranked_candidates`) | 200 |
| Lỗi xác thực dữ liệu | Vi phạm ràng buộc `SearchRequest` (thiếu `subject`, ngân sách âm, `top_k` ngoài khoảng, enum sai, khóa lạ, trường thừa) | 422 |

*Nguồn: `backend/app/api/recommend.py` (4 nhánh trả về trong hàm `recommend_tutors`); `docs/design/api-contract.md` mục 4–6; `backend/app/schemas/recommendation.py`, `backend/app/schemas/search_request.py`.*

### 4.4.2. Ví dụ request/response thật

Khởi chạy dịch vụ cục bộ bằng `python -m uvicorn app.main:app` (Python 3.12.7) và gọi `POST /api/recommend` với thân yêu cầu KB01 (Mục 4.3.3); phần phản hồi thực tế nhận được cho hạng 1 (HTTP 200, các hạng 2–3 rút gọn trường chi tiết) như sau:

```json
{
  "status": "success",
  "total_candidates": 16,
  "qualified_candidates": 5,
  "insufficient_data_candidates": [],
  "results": [
    {
      "rank": 1,
      "tutor_id": "GS-G01",
      "total_score": 0.9375,
      "criteria_scores": {"fee": 1.0, "district": 1.0, "experience": 0.75, "rating": 1.0, "availability": null},
      "contributions":  {"fee": 0.25, "district": 0.25, "experience": 0.1875, "rating": 0.25, "availability": null},
      "reason": "Học phí trong ngân sách, khu vực khớp, đánh giá 5,0/5",
      "notes": []
    }
  ]
}
```

Trong cùng lần kiểm chứng đó, hai phần tử tiếp theo trong `results` là `GS-G10` (`total_score: 0.745`, `notes: []`) và `GS-T06` (`total_score: 0.625`, `notes: ["chưa có đánh giá"]`). Các ca biên trả về đúng thiết kế:
- Thiếu `subject` trả về HTTP 422 với chi tiết lỗi `missing` tại `["body", "subject"]` (`"Field required"`).
- `max_budget_vnd = -5` trả về HTTP 422 (`greater_than_equal`).
- Môn Tiếng Trung trả về trạng thái `no_match` (HTTP 200).
- Toàn bộ mức ưu tiên `none` trả về trạng thái `zero_weight` (HTTP 200) với 5 mã gia sư qua lọc trong `unranked_candidates`.

Số liệu hiệu năng và kết quả bộ kiểm thử tự động được trình bày tại Chương 5; chương này không lặp lại.

## 4.5. Xây dựng giao diện demo

Giao diện là một Single Page Application React 19 (Vite), CSS thuần trong `frontend/src/App.css` (2.089 dòng) và `index.css` — không dùng TailwindCSS và không dùng thư viện biểu đồ; thanh xếp chồng được tự dựng bằng HTML/CSS. Quản lý trạng thái dùng các hook chuẩn React trong `App.jsx`.

Bảng 4.5 liệt kê các tệp giao diện theo từng chức năng CN01–CN03.

**Bảng 4.5 - Thành phần giao diện và chức năng theo CN01–CN03**

| Tệp | Vai trò | Chức năng |
|:---|:---|:---|
| `src/App.jsx` | Điều phối trung tâm | Điều hướng 2 bước (tab CN01 và tab CN02+CN03); lưu trạng thái chung (`searchForm`, `recommendationResult`, `isLoading`, `apiError`, `latencyMs`, `rankDeltas`); `executeRecommendationRequest` gọi API; chống chồng lấn request bằng `requestSeqRef` (Mục 4.6) |
| `src/pages/SearchPage.jsx` | Màn hình nhập nhu cầu (CN01) | Biểu mẫu theo Bảng 3.4 (môn học, hình thức, khu vực, ngân sách kèm dòng quy đổi bằng chữ, Top-$k$); bảng chọn lịch 7 ngày × 3 buổi và 3 mẫu chọn nhanh; kiểm tra hợp lệ phía client (môn học, khu vực bắt buộc khi học Trực tiếp, ngân sách không âm); thanh chip “Nạp nhanh” 14 kịch bản KB01–KB14 (nhãn giao diện “Kịch bản thực nghiệm (Bảng 5.1 · KB01 - KB14)”, tương ứng Bảng 5.3 của báo cáo) kèm tùy chọn “Tự động chuyển kết quả” |
| `src/pages/ResultPage.jsx` | Màn hình kết quả (CN02 + CN03) | Dải KPI (kịch bản, môn, hình thức, khu vực, ngân sách, lịch) và phễu “Kho → Hợp lệ → Top-$k$”; rail CN03 với 5 tiêu chí và 4 nút “Nạp nhanh trọng số” (“Mặc định (w=2)”, “Ưu tiên Học phí”, “Ưu tiên KN & Đánh giá”, “Thử ∑w_i = 0”); hiển thị 3 trạng thái `success`/`no_match`/`zero_weight`; chip độ trễ đo tại trình duyệt |
| `src/components/TutorCard.jsx` | Thẻ gia sư | Avatar, huy hiệu hạng, huy hiệu “Khuyến nghị tốt nhất” cho hạng 1, nhãn nguồn dữ liệu (“Dữ liệu thực tế” cho `public_collected`, “Dữ liệu đối chứng” cho `simulated`), lưới thuộc tính 4 ô và hàng lịch rảnh, lý do gợi ý và ghi chú dữ liệu |
| `src/components/StackedBarScore.jsx` | Thanh xếp chồng tự dựng | Vẽ phân đoạn theo đóng góp $C_i = w_i \cdot s_i / \sum w_i$; tooltip hiển thị `s_i`, `w_i`, `C_i` và tỷ trọng; chú giải đếm cả tiêu chí “Không áp dụng” (`null` bị ẩn khỏi thanh) |
| `src/components/TutorAvatar.jsx` | Ảnh đại diện | Ảnh chân dung `/avatars/{tutor_id}.webp` (16 tệp WebP trong `frontend/public/avatars/`), fallback sang monogram gradient khi ảnh thiếu |
| `src/components/CriteriaIcon.jsx`, `SubjectIcon.jsx`, `SkeletonLoader.jsx` | Phụ trợ | Biểu tượng tiêu chí/môn học; khung xương chờ khi đang tính điểm |
| `src/services/api.js` | Dịch vụ gọi API | Chọn `API_BASE_URL` theo tên miền và biến `VITE_API_URL`; `buildRecommendationPayload` chuẩn hóa biểu mẫu theo hợp đồng API; `fetchRecommendations` xử lý lỗi mạng/HTTP |
| `src/data/scenariosCatalog.js` | Dữ liệu kịch bản | 14 kịch bản KB01–KB14 đồng bộ từ `backend/tests/scenarios/scenarios.json` (kèm `expected_raw` để hiển thị kỳ vọng) |
| `src/data/goalPresets.js` | Mục tiêu học tập (US-41) | 3 preset điền sẵn 5 mức ưu tiên: “Không nêu mục tiêu” (mặc định), “Điểm cao / luyện thi chuyên – học sinh giỏi” (Kinh nghiệm và Đánh giá mức Cao), “Đủ điểm đậu / lấy lại kiến thức căn bản” (Học phí mức Cao) |
| `src/data/tutorsCatalog.js` | Tra cứu hồ sơ | Bản sao chuẩn hóa 16 hồ sơ theo `tutor_id` để hiển thị thẻ mà không đổi hợp đồng API; bảng màu 5 tiêu chí; các hàm định dạng số dùng dấu phẩy (`formatScoreVi`) |

*Nguồn: các tệp `frontend/src/` liệt kê trong bảng; `frontend/src/App.css`; `frontend/package.json`.*

Ô “Mục tiêu học tập” được đặt trên khối 5 tiêu chí ở CN01 (theo `docs/design/de-xuat-mo-rong-cap-lop-muc-tieu.md`). Preset chỉ sinh bộ mức ưu tiên khởi tạo ở tầng giao diện; ô không có state riêng mà suy ra giá trị hiển thị từ 5 mức ưu tiên hiện tại (không khớp preset nào thì hiện “Tùy chỉnh”). Payload gửi API giữ nguyên 7 trường và 5 khóa ưu tiên; cấp lớp nhận dạy chưa hiện thực vì `TutorProfile` chỉ có 9 trường, không có dữ liệu cấp lớp.

Bốn ảnh giao diện sau minh họa lần lượt bốn trạng thái của luồng sử dụng: nhập nhu cầu (Hình 4.1), kết quả Top-3 của KB01 (Hình 4.2), xếp hạng lại sau khi đổi mức ưu tiên (Hình 4.3) và trạng thái biên khi tổng trọng số bằng 0 (Hình 4.4). Các ảnh được chụp trực tiếp từ hệ thống chạy cục bộ và lưu tại `docs/thesis/figures/`.

![Hình 4.1 - Màn hình nhập nhu cầu học tập (CN01)](../figures/hinh-ui-01-cn01-nhap-nhu-cau.png)

**Hình 4.1 - Màn hình nhập nhu cầu học tập (CN01)**

Hình 4.1 minh họa giao diện chế độ tối với thanh chip 14 kịch bản KB01–KB14 (KB01 đang được chọn) và biểu mẫu “Thông tin nhu cầu học tập (Bảng 3.4)”. Các trường đã điền gồm môn Toán, hình thức Trực tiếp, khu vực Bình Thạnh, ngân sách `200000` (200.000 VNĐ/giờ kèm dòng quy đổi bằng chữ). Cột phải “Mức độ ưu tiên cho 5 tiêu chí (Bảng 3.5)” hiển thị ô “Mục tiêu học tập (gợi ý mức ưu tiên)” ở giá trị “Không nêu mục tiêu” cùng bốn nút mức ưu tiên $w = 0, 1, 2, 3$ (mặc định Trung bình, $w = 2$).

![Hình 4.2 - Màn hình kết quả gợi ý Top-3 kịch bản KB01 (CN02)](../figures/hinh-ui-02-cn02-ket-qua-kb01.png)

**Hình 4.2 - Màn hình kết quả gợi ý Top-3 kịch bản KB01 (CN02)**

Trên Hình 4.2, dải KPI hiển thị đúng kỳ vọng “1. GS-G01 (0,938) 2. GS-G10 (0,745) 3. GS-T06 (0,625)”, kèm phễu “Kho: 16 hồ sơ → Hợp lệ: 5 ứng viên → Top-3: 3 gợi ý” và rail CN03 bên trái. Thẻ hạng 1 `GS-G01` hiển thị huy hiệu `#1`, “Khuyến nghị tốt nhất”, nhãn “Dữ liệu đối chứng”, điểm tổng hợp $S(g) = 0{,}938$ (93,8%) và thanh xếp chồng bốn phân đoạn `0,25 / 0,25 / 0,19 / 0,25` (riêng Lịch rảnh không áp dụng) cùng dòng “Lý do gợi ý: Học phí trong ngân sách, khu vực khớp, đánh giá 5,0/5”. Chip `651,5 ms` là độ trễ đo tại trình duyệt ở lần chụp ảnh, không phải số liệu benchmark có hệ thống để so sánh với Chương 5.

![Hình 4.3 - Điều chỉnh mức ưu tiên trực tiếp (CN03) làm đổi hạng](../figures/hinh-ui-03-cn03-dieu-chinh-uu-tien.png)

**Hình 4.3 - Điều chỉnh mức ưu tiên trực tiếp (CN03) làm đổi hạng**

Hình 4.3 cho thấy trạng thái sau khi đưa Học phí và Khu vực về “Bỏ qua (w=0)”, đồng thời tăng Kinh nghiệm và Đánh giá lên “Cao (w=3)”. Gia sư `GS-G10` (130.000 VNĐ/giờ, 12 năm, 4,9/5) lên hạng 1 với điểm $0{,}990$ (99,0%) kèm huy hiệu “↑ Tăng 1 bậc sau khi điều chỉnh mức ưu tiên (CN03)”, trong khi thẻ tụt hạng phía dưới gắn huy hiệu “↓ Giảm 1 bậc sau khi điều chỉnh mức ưu tiên (CN03)”. Thanh xếp chồng lúc này chỉ còn hai phân đoạn Kinh nghiệm ($0{,}50$) và Đánh giá ($0{,}49$), ba tiêu chí còn lại hiển thị “Không áp dụng”.

![Hình 4.4 - Trạng thái biên tổng trọng số bằng 0 ($\sum w_i = 0$)](../figures/hinh-ui-04-zero-weight.png)

**Hình 4.4 - Trạng thái biên tổng trọng số bằng 0 ($\sum w_i = 0$)**

Hình 4.4 trình bày trạng thái biên khi đặt cả 5 tiêu chí về “Bỏ qua (w=0)”: chip kịch bản chuyển thành “KB01 (Tùy chỉnh: ∑w=0)”, phễu kết quả ghi “Top-3: 0 gợi ý” và rail CN03 hiện cảnh báo “Tổng trọng số ∑w_i = 0”. Giữa trang hiển thị thẻ trạng thái “Không thể xếp hạng do tổng trọng số bằng 0” kèm nút “Khôi phục trọng số mặc định (w = 2)”.

## 4.6. Tích hợp giao diện với API và kiểm tra luồng end-to-end

### 4.6.1. Luồng xử lý end-to-end

Luồng xử lý chính từ giao diện đến API diễn ra theo bốn bước:
1. Người học nhập nhu cầu tại `SearchPage` (CN01) hoặc nạp nhanh một kịch bản, kích hoạt `App.jsx` gọi `executeRecommendationRequest` và `buildRecommendationPayload` để chuẩn hóa dữ liệu gửi đi.
2. `fetchRecommendations` gửi `POST /api/recommend` đến backend; kết quả (thuộc một trong ba trạng thái) được `ResultPage` (CN02) hiển thị kèm thanh xếp chồng và lý do gợi ý.
3. Khi người học đổi mức ưu tiên trên rail CN03, `onUpdatePriorities` gọi lại API với `trackDeltaFrom` là kết quả trước đó, đối chiếu thứ hạng cũ và mới để tạo dữ liệu `rankDeltas` cho huy hiệu “Tăng/Giảm $n$ bậc”.
4. Nút “Thử ∑w_i = 0” trên rail đưa cả 5 tiêu chí về `none` và kích hoạt hiển thị trạng thái `zero_weight` của backend (Hình 4.4).

Trong `frontend/src/services/api.js`, `API_BASE_URL` nhận lần lượt biến môi trường `VITE_API_URL` rồi `VITE_API_BASE_URL`; nếu không đặt cả hai, mô-đun chọn URL theo tên miền hiện hành rồi cắt dấu gạch chéo cuối. Khi hostname khác `localhost`/`127.0.0.1` (triển khai trên Vercel), URL mặc định là `https://tutor-recommender-api.onrender.com`; khi chạy cục bộ là `http://localhost:8000`. Kho mã nguồn không lưu tệp `.env*` của frontend, nên việc đặt biến `VITE_API_URL` trên bảng điều khiển Vercel theo `docs/deployment/deploy-vercel-render.md` (phần B3) nằm ngoài phạm vi kiểm chứng trực tiếp từ tệp mã nguồn; hành vi mặc định khi không có biến môi trường do cơ chế chọn URL theo tên miền trong `api.js` đảm nhiệm.

### 4.6.2. Xử lý lỗi cơ bản ở cả hai phía

Bảng 4.6 tổng hợp các tình huống lỗi đã gặp và nơi xử lý tương ứng ở cả hai phía.

**Bảng 4.6 - Các tình huống lỗi và nơi xử lý**

| Tình huống | Nơi xử lý (tệp) | Hành vi quan sát được |
|:---|:---|:---|
| Thiếu môn học | `frontend/src/pages/SearchPage.jsx` (chặn trước khi gửi); `backend/app/schemas/search_request.py` (chặn lần hai) | Client hiển thị “Vui lòng chọn môn học mong muốn.”; nếu gọi API trực tiếp, backend trả về HTTP 422 với thông báo “Môn học (subject) không được để trống.” |
| Ngân sách âm hoặc không nguyên | `SearchPage.jsx`; `api.js` (`parseInt`); `search_request.py` (`StrictInt`, `ge = 0`) | Client hiển thị “Ngân sách tối đa phải là một số không âm hợp lệ.”; yêu cầu vượt qua client (gọi trực tiếp) trả về HTTP 422 `greater_than_equal` |
| Không có gia sư thỏa điều kiện bắt buộc | `backend/app/api/recommend.py`; `frontend/src/pages/ResultPage.jsx` | Backend trả về `no_match`; giao diện hiển thị thẻ “Không tìm thấy gia sư thỏa mãn điều kiện” kèm danh sách ứng viên qua lọc nhưng thiếu dữ liệu (nếu có) |
| Tổng trọng số bằng 0 | `recommend.py`; `ResultPage.jsx`; `App.jsx` (tính `totalActiveWeight` hiển thị cảnh báo ở rail) | Backend trả về `zero_weight` kèm `unranked_candidates`; giao diện hiển thị thẻ cảnh báo và nút khôi phục trọng số mặc định (Hình 4.4) |
| Backend không phản hồi | `frontend/src/services/api.js` | Bắt lỗi `fetch` và hiển thị “Không thể kết nối tới máy chủ gợi ý gia sư. Vui lòng kiểm tra dịch vụ Backend đang chạy.” trên cả hai màn hình |
| Phản hồi HTTP lỗi / không phải JSON | `frontend/src/services/api.js` | Hiển thị “Phản hồi từ máy chủ không hợp lệ (HTTP `<mã trạng thái>`).”; khi backend trả về 422, dùng chuỗi `detail` nếu là chuỗi, ngược lại hiển thị “Dữ liệu đầu vào không hợp lệ (HTTP 422). Vui lòng kiểm tra lại các trường đã nhập.” |
| Đổi mức ưu tiên liên tiếp (CN03) | `frontend/src/App.jsx` (`requestSeqRef`) | Mỗi yêu cầu nhận một số thứ tự; phản hồi của yêu cầu không còn là yêu cầu mới nhất bị bỏ qua, không ghi đè kết quả hiển thị |

*Nguồn: `frontend/src/App.jsx` (`executeRecommendationRequest`, `requestSeqRef` tại dòng 52, kiểm tra `seq !== requestSeqRef.current` tại dòng 77, 104, 113), `frontend/src/pages/SearchPage.jsx` (`handleSubmit`, dòng 231, 241, 248), `frontend/src/pages/ResultPage.jsx` (dòng 216, 442, 459), `frontend/src/services/api.js` (`fetchRecommendations`, dòng 164, 172, 179), `backend/app/schemas/search_request.py` (dòng 90), `backend/app/api/recommend.py`.*

Luồng end-to-end được kiểm tra theo hai lớp: kiểm thử tự động phía backend (41 bài test API và ca biên trong `backend/tests/api/`, gồm cả luồng đổi ưu tiên CN03) và kiểm tra thủ công trên giao diện khi demo. Phía frontend chưa có bộ kiểm thử tự động — `frontend/package.json` chỉ định nghĩa bốn script `dev`, `build`, `lint`, `preview`.

### 4.6.3. Triển khai công khai

Hệ thống được triển khai lên nền tảng đám mây theo `docs/deployment/deploy-vercel-render.md`. Frontend (thư mục `frontend`, build `npm run build`, định tuyến SPA qua `vercel.json`) chạy trên Vercel tại `https://tutor-recommender.vercel.app`. Backend chạy trên Render Web Service (cấu hình trong `render.yaml`: runtime Python 3.12.7, `rootDir: backend`, lệnh khởi chạy `uvicorn app.main:app --host 0.0.0.0 --port $PORT`, kiểm tra sức khỏe tại `/health`) tại `https://tutor-recommender-api.onrender.com`, kèm Swagger UI tại `/docs`.

Tài liệu triển khai mô tả hiện tượng khởi động nguội (*cold start*) khoảng 30–40 giây trên gói miễn phí của Render sau thời gian không có lưu lượng; đây là thông số kỹ thuật từ tài liệu triển khai và chưa được đo đạc độc lập. Độ trễ mạng toàn trình giữa trình duyệt và hai dịch vụ đám mây cũng chưa được đo đạc; kết quả kiểm thử định lượng của hệ thống được trình bày tại Chương 5.

---

## 4.7. Giới hạn của việc hiện thực

- **Cơ sở dữ liệu chưa hiện thực:** lưu trữ chỉ dùng JSON/CSV; phương án SQLite xếp mức ưu tiên thấp (*Could Have*), chưa đưa vào sprint nào.
- **CI chỉ bao phủ backend:** frontend chưa có job trong GitHub Actions và chưa có bộ kiểm thử tự động riêng (chỉ chạy `oxlint` và `vite build` từ terminal).

Các giới hạn còn lại được trình bày tại Mục 5.3 (Chương 5) và Mục 6.2 (Chương 6) để tránh lặp, bao gồm quy mô bộ dữ liệu 16 hồ sơ, tham số ấn định thủ công, phạm vi hiện thực Phương án 1 cho “Mục tiêu học tập”, cùng việc chưa đo độ trễ mạng toàn trình.
