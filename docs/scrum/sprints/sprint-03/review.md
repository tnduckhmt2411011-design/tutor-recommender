> [!NOTE]
> **Đề xuất, nhóm xác nhận**

# Sơ kết Sprint 3 (Sprint 3 Review)

- **Ngày họp:** *[Chờ nhóm điền]*
- **Người chủ trì:** Scrum Master (Trần Nguyễn Đức)
- **Thành phần tham dự:** *[Chờ nhóm điền]*

---

## 1. Kết quả thực hiện mục tiêu Sprint

- **Mục tiêu đặt ra:** Hoàn thiện tầng xếp hạng và giải thích (Epic E3) — gồm cơ chế kiểm tra ngưỡng dữ liệu tối thiểu (`eligibility.py`), thuật toán tính điểm tổng hợp Weighted Scoring và sắp xếp Top-$k$ kèm mức đóng góp từng tiêu chí, lý do gợi ý và ghi chú dữ liệu (`ranker.py`), tự động hóa bộ kiểm thử hồi quy 14 kịch bản thực nghiệm (`test_scenarios.py`) và lập báo cáo phân tích đối chiếu kết quả (`discrepancy_analysis.md`) để vượt qua Cổng chất lượng 2 (Quality Gate 2).
- **Đánh giá mức độ hoàn thành:** *[Đạt / Chưa đạt]*

---

## 2. Rà soát chi tiết User Stories

| Mã US | Tên User Story | Điểm SP | Trạng thái | Ghi chú nghiệm thu |
|:---|:---|:---:|:---:|:---|
| US-14 | Hiện thực cơ chế kiểm tra ngưỡng dữ liệu tối thiểu theo Bảng ngưỡng đề cương | 2 | Xong (PR #63) | 17 unit test tại `test_eligibility.py` (bao phủ bảng ngưỡng $n=0..5$ và loại trừ `rating`) |
| US-15 | Tính điểm tổng hợp $S(g)$, sắp xếp giảm dần (phá hòa theo mã hồ sơ) và lấy Top-$k$ | 2 | Xong (PR #64) | Cài đặt tại `app/scoring/ranker.py` và mô hình `RankedTutor` tại `app/schemas/recommendation.py` |
| US-16 | Tính mức đóng góp của từng tiêu chí vào điểm tổng và sinh lời giải thích kèm ghi chú | 2 | Xong (PR #64) | 8 unit test tại `test_ranker.py` (gồm ví dụ Mục 3.6 $S = 113/150 \approx 0{,}753$ và Ví dụ 2 của `api-contract.md`) |
| US-17 | Tự động hóa kiểm thử hồi quy 14 kịch bản đánh giá từ `scenarios.json` | 2 | Xong (PR #66) | 17 bài kiểm thử tại `tests/scenarios/test_scenarios.py`, khớp 14/14 kịch bản (`KB01`–`KB14`) |
| US-18 | Phân tích chi tiết nguyên nhân toán học và dữ liệu tại các kịch bản có sai lệch so với `expected_raw` | 1 | Xong (PR #65) | Báo cáo `docs/thesis/report/discrepancy_analysis.md` phân tích `KB04`, `KB09` và đồng điểm `KB02`, `KB12` |

*Ghi chú về các PR đã merge trong Sprint 3 (đều do `tnduckhmt2411011-design` thực hiện):*
- **Biên bản Sprint 2 & kế hoạch Sprint 3:** PR #62 (`docs/sprint-02-review-sprint-03-planning`, merge `4e03439`, 2026-11-02).
- **US-14 (#16):** PR #63 (`feat/16-nguong-du-lieu`, merge `461cb84`, 2026-11-02).
- **US-15 (#17) + US-16 (#18):** PR #64 (`feat/17-18-xep-hang-va-giai-thich`, merge `835f950`, 2026-11-02).
- **US-18 (#20):** PR #65 (`docs/20-phan-tich-sai-lech-kich-ban`, merge `edff048`, 2026-11-02).
- **US-17 (#19):** PR #66 (`test/19-kiem-thu-14-kich-ban`, merge `fe2b265`, 2026-11-02).

---

## 3. Đánh giá Cổng chất lượng 2 (Quality Gate 2)

- [x] **100% unit test của 5 hàm chuẩn hóa điểm (Bảng 3.6) và module xếp hạng vượt qua thành công:** Đã kiểm chứng trên `origin/main` (`fe2b265`) với `ruff check .` (`All checks passed!`) và `pytest -rs` đạt `149 passed, 1 skipped` (chỉ còn duy nhất `tests/api/test_recommend_api.py` thuộc Sprint 4); độ bao phủ toàn bộ `backend/app/` đạt **95%**.
- [x] **14 kịch bản thực nghiệm (`KB01`–`KB14`) chạy tự động qua bộ máy xếp hạng và xuất bảng tổng hợp đối sánh:** `tests/scenarios/test_scenarios.py` thực thi tự động toàn bộ 14 kịch bản từ `scenarios.json` trên tập 16 hồ sơ chuẩn hóa `data/processed/tutors.json`, đạt tỷ lệ trùng khớp `expected_top3` là **14/14 (100%)**.
- [x] **Mọi khác biệt số liệu giữa hệ thống và `expected_raw` được điều tra và lập biên bản, tuyệt đối không sửa kỳ vọng:** Đã ghi nhận tại `docs/thesis/report/discrepancy_analysis.md` (giải thích nguyên nhân tính đủ 4 tiêu chí tại `KB04` cho `0,886 / 0,786` so với phép tính tay 3 tiêu chí `0,848 / 0,715` mà không đổi thứ hạng `GS006 > GS020`, quy tắc làm tròn `0,9275` tại `KB09` và cơ chế phá hòa theo `tutor_id` tại `KB02`, `KB12`); tệp `backend/tests/scenarios/scenarios.json` được giữ nguyên bất biến.
- **Kết luận:** *[Đủ điều kiện chuyển sang Sprint 4 / Cần bổ sung]*
