> [!NOTE]
> **Đề xuất, nhóm xác nhận**

# Kế hoạch Sprint 6 (Sprint 6 Planning)

- **Thời gian thực hiện:** Hạn: 2027-01-01 (theo Milestone Sprint 6); ngày bắt đầu: [Chờ nhóm điền]
- **Mục tiêu Sprint (Sprint Goal):** Đánh giá độ ổn định, hoàn thiện báo cáo khóa luận, tài liệu vận hành, slide demo và đóng gói bàn giao `v1.0` (Epic E6 & E7) — thực hiện kiểm thử độ nhạy tham số ($\delta$, $E_{\max}$), biến động ngân sách và đa bộ mức ưu tiên theo Mục 5.2, hoàn thiện toàn văn Chương 5 và Chương 6 kèm các Phụ lục A–D, cập nhật tài liệu hướng dẫn triển khai nhanh `README.md` trong 5 phút, thiết kế bộ slide thuyết trình và kịch bản phân vai demo bảo vệ CN01–CN03, đồng bộ mục lục/bảng biểu/hình ảnh và gắn tag phát hành chính thức `v1.0` để hoàn tất **Cổng chất lượng 4 (Quality Gate 4)**.
- **Giả định công suất nhóm:** 9 Story Points *(9 Must)*.

---

## 1. Danh sách User Stories cam kết trong Sprint

| Mã US | Tên User Story | Điểm SP | Mức ưu tiên | Mục đề cương | Issue | Phụ trách | Trạng thái |
|:---|:---|:---:|:---:|:---|:---:|:---:|:---:|
| **US-30** | Đánh giá chất lượng xếp hạng và phân tích độ ổn định | 2 | Must | Mục 5.2 | #32 | *[Chờ nhóm phân công]* | Chưa làm |
| **US-33** | Hoàn thiện toàn diện nội dung báo cáo Chương 5 và Chương 6 | 3 | Must | Chương 5, Chương 6 | #33 | *[Chờ nhóm phân công]* | Chưa làm |
| **US-34** | Soạn thảo tài liệu hướng dẫn cài đặt và vận hành hệ thống (`README`) | 1 | Must | Mục 4.1, Phụ lục B | #34 | *[Chờ nhóm phân công]* | Chưa làm |
| **US-35** | Thiết kế slide thuyết trình và chuẩn bị kịch bản demo bảo vệ | 2 | Must | Báo cáo đồ án & slide | #35 | *[Chờ nhóm phân công]* | Chưa làm |
| **US-36** | Cập nhật mục lục, đóng gói hồ sơ đồ án và gắn tag phát hành `v1.0` | 1 | Must | Mục lục, Toàn bộ báo cáo | #36 | *[Chờ nhóm phân công]* | Chưa làm |

- **Tổng điểm Story Points:** **9 SP** (9 Must).
- *Ghi chú về nhóm tính năng mở rộng (`Could Have`):* 3 User Stories dự phòng gồm `US-37` (#37 — SQLite, 2 SP), `US-38` (#38 — LocalStorage, 1 SP) và `US-39` (#39 — Xuất PDF, 1 SP) thuộc phạm vi `Could Have` chưa xếp sprint theo `docs/scrum/roadmap.md`; nhóm ưu tiên hoàn tất 100% các hạng mục `Must Have` và nghiệm thu Cổng chất lượng 4 trước.

---

## 2. Phân rã nhiệm vụ kỹ thuật (Tasks)

- **Phụ trách:** *[Chờ nhóm phân công]*
  - [ ] US-30 (#32) + US-33 (#33):
    - Xây dựng bộ kiểm thử thực nghiệm tự động `backend/tests/scenarios/test_sensitivity_muc_5_2.py` khảo sát độ nhạy của tham số $\delta \in \{0{,}25;\, 0{,}30;\, 0{,}50;\, 0{,}70;\, 0{,}75;\, 1{,}00\}$, kinh nghiệm trần $E_{\max} \in \{5,\, 6,\, 8,\, 10,\, 12\}$, biến động ngân sách $\{-20\%,\, -10\%,\, -5\%,\, +5\%,\, +10\%,\, +20\%\}$ và đối chiếu thứ hạng dưới nhiều bộ mức ưu tiên trên dữ liệu thực theo tinh thần Bảng 2.2 (tổng cộng 10 bài kiểm thử tự động, nâng tổng số test toàn hệ thống từ `190` lên `200 passed, 0 skipped`).
    - Lập báo cáo chuyên đề `docs/thesis/report/muc-5.2-danh-gia-do-on-dinh.md` tổng hợp số liệu thống kê độ trùng khớp Top-3 (14/14 = 100%), phân tích độ ổn định và khả năng giải thích của mô hình.
    - Soạn thảo báo cáo hoàn chỉnh Chương 5 tại `docs/thesis/report/chuong-05-thuc-nghiem-va-danh-gia.md` (tổng hợp Mục 5.1, Bảng 5.1, Mục 5.2 và phân tích 5 hạn chế thực tế tại Mục 5.3).
    - Soạn thảo báo cáo hoàn chỉnh Chương 6 và hệ thống Phụ lục tại `docs/thesis/report/chuong-06-ket-luan-va-huong-phat-trien.md` (Mục 6.1 đối chiếu 4 mục tiêu cụ thể ở Mục 1.4, Mục 6.2 ba hướng phát triển lên đồ án tốt nghiệp, Mục 6.3 tự đánh giá Bảng 6.1, cùng Phụ lục A, B, C, D) và cập nhật `docs/thesis/outline/muc-6.1-bang-6.1.md`.
  - [ ] US-34 (#34) + US-35 (#35):
    - Cập nhật toàn diện `README.md` tại thư mục gốc cùng `backend/README.md` và `frontend/README.md` để người chấm hoặc người dùng mới có thể cài đặt môi trường, khởi chạy backend (`uvicorn`), khởi chạy frontend (`vite`), chạy kiểm thử (`pytest`, `ruff`, `oxlint`) và trải nghiệm demo CN01–CN03 trong vòng 5 phút; bổ sung hình ảnh minh họa giao diện tại `docs/thesis/figures/`.
    - Thiết kế nội dung bộ slide thuyết trình bảo vệ đồ án tại `docs/thesis/slides/slide-bao-ve-do-an.md` và kịch bản phân vai demo trực tiếp 3 chức năng CN01–CN03 cho 3 thành viên kèm bộ câu hỏi/trả lời phản biện dự kiến tại `docs/thesis/slides/kich-ban-demo-bao-ve.md`.
  - [ ] US-36 (#36):
    - Lập tài liệu tổng hợp `docs/thesis/report/muc-luc-va-ho-so-ban-giao.md` đồng bộ Mục lục, Danh mục hình ảnh (Hình 3.1–3.5 và hình giao diện thực tế), Danh mục bảng biểu (Bảng 1.1–6.1) và bảng kiểm tra tính toàn vẹn của hồ sơ bàn giao `v1.0`.
    - Rà soát làm sạch các tệp `.gitkeep` dư thừa tại các thư mục đã có tệp thật và lập biên bản sơ kết/rút kinh nghiệm cuối khóa tại `docs/scrum/sprints/sprint-06/{review,retrospective}.md`.
    - Sau khi toàn bộ các PR của Sprint 6 được kiểm tra và hợp nhất vào `main`, tạo và đẩy git tag chính thức `v1.0` lên GitHub repository.

---

## 3. Tiêu chí nghiệm thu Cổng chất lượng 4 (Quality Gate 4)

- [ ] Toàn bộ bài kiểm thử tự động ở backend (`pytest`, `ruff check`) và kiểm tra chất lượng mã nguồn ở frontend (`npm run lint`, `npm run build`) đều vượt qua 100% không lỗi.
- [ ] Hoàn thiện báo cáo Chương 5 (Mục 5.1, Bảng 5.1, Mục 5.2, Mục 5.3), Chương 6 (Mục 6.1, 6.2, 6.3 - Bảng 6.1) và các Phụ lục A, B, C, D phản ánh trung thực kết quả thực nghiệm của hệ thống.
- [ ] Tài liệu `README.md` đầy đủ hướng dẫn cài đặt, chạy thử nghiệm trong 5 phút và có hình minh họa giao diện; bộ slide thuyết trình và kịch bản demo bảo vệ CN01–CN03 sẵn sàng tại `docs/thesis/slides/`.
- [ ] Mục lục, Danh mục hình ảnh, Danh mục bảng biểu đồng bộ; repository sạch sẽ không có tệp thừa/tạm; hoàn tất gắn tag phát hành chính thức `v1.0` trên nhánh `main`.

---

## 4. Rủi ro dự kiến và phương án xử lý

- *Rủi ro 1:* Trong Python, các hàm `score_fee(price, budget, delta=DELTA)` và `score_experience(years, e_max=E_MAX)` trong `backend/app/scoring/criteria.py` gắn giá trị mặc định ngay tại thời điểm nạp module (`import` time), nên nếu bài kiểm thử độ nhạy Mục 5.2 chỉ gán lại biến `config.DELTA` hoặc `config.E_MAX` thì kết quả tính điểm qua `ranker.py` sẽ không thay đổi. $\rightarrow$ *Phương án:* Sử dụng `unittest.mock.patch` tại tầng `app.scoring.ranker.{score_fee, score_experience}` trong `test_sensitivity_muc_5_2.py` để truyền trực tiếp tham số `delta` và `e_max` biến thiên vào hàm gốc mà không cần sửa đổi bất kỳ dòng mã nguồn nào trong `backend/app/`.
- *Rủi ro 2:* Bất đồng bộ số liệu giữa kết quả chạy kiểm thử tự động với nội dung văn bản trong Chương 5, Chương 6, `README.md` và Slide bảo vệ. $\rightarrow$ *Phương án:* Trích xuất trực tiếp toàn bộ bảng số liệu độ nhạy từ kết quả chạy `pytest` trên 16 hồ sơ chuẩn hóa và 14 kịch bản `scenarios.json`, đồng thời đối chiếu chéo với `docs/thesis/report/muc-5.1-bang-5.1-ket-qua.md` và `docs/thesis/report/discrepancy_analysis.md`.
- *Rủi ro 3:* Xung đột tệp khi mở và hợp nhất các Pull Request bằng `Squash and merge` trên GitHub. $\rightarrow$ *Phương án:* Phân tách các PR của Sprint 6 trên các tập tệp hoàn toàn rời nhau từ `origin/main`, và chỉ gắn tag `v1.0` sau khi tất cả các PR đã được người phụ trách GitHub kiểm tra và hợp nhất vào `main`.
