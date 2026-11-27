> [!NOTE]
> **Đề xuất, nhóm xác nhận**

# Sơ kết Sprint 6 (Sprint 6 Review)

- **Ngày họp:** *[Chờ nhóm điền]*
- **Người chủ trì:** Scrum Master (Lê Thị Bích Chuyền)
- **Thành phần tham dự:** *[Chờ nhóm điền]*

---

## 1. Kết quả thực hiện mục tiêu Sprint

- **Mục tiêu đặt ra:** Đánh giá độ ổn định, hoàn thiện báo cáo khóa luận, tài liệu vận hành, slide demo và đóng gói bàn giao `v1.0` (Epic E6 & E7) — khảo sát độ nhạy tham số theo Mục 5.2, hoàn thiện toàn văn Chương 5 và Chương 6 kèm Phụ lục A–D, cập nhật `README.md`, thiết kế bộ slide và kịch bản demo bảo vệ CN01–CN03, soạn tài liệu đề xuất mở rộng mô hình (US-40) và ô chọn mục tiêu học tập ở màn hình nhập nhu cầu (US-41), đồng bộ mục lục/danh mục bảng biểu/danh mục hình ảnh rồi gắn tag phát hành `v1.0` để hoàn tất **Cổng chất lượng 4 (Quality Gate 4)**.
- **Đánh giá mức độ hoàn thành:** **Đạt** đối với toàn bộ hạng mục `Must Have` và `Should Have` về sản phẩm; **chưa hoàn tất** bước phát hành cuối cùng (gắn tag `v1.0`), do PR #93 còn đang mở và nhóm chủ động chờ chỉ định hợp nhất.
- **Tổng hợp theo Story Point:** **12/13 SP** hoàn tất trọn vẹn (US-30, US-33, US-34, US-35, US-40, US-41); **1 SP** còn lại của US-36 đã có sản phẩm (mục lục, danh mục, hồ sơ bàn giao, biên bản sprint) nhưng chưa đóng vì thao tác gắn tag `v1.0` chưa thực hiện.

---

## 2. Rà soát chi tiết User Stories

| Mã US | Tên User Story | Điểm SP | Trạng thái | Ghi chú nghiệm thu |
|:---|:---|:---:|:---:|:---|
| US-30 | Đánh giá chất lượng xếp hạng và phân tích độ ổn định | 2 | Xong (PR #87) | Bổ sung `backend/tests/scenarios/test_sensitivity_muc_5_2.py` (10 bài kiểm thử) khảo sát độ nhạy của dung sai học phí $\delta$, mốc kinh nghiệm bão hòa $E_{\max}$, biến động ngân sách và đa bộ mức ưu tiên, nâng tổng số bài kiểm thử từ `190` lên `200 passed, 0 skipped`; báo cáo chuyên đề tại `docs/thesis/report/muc-5.2-danh-gia-do-on-dinh.md` |
| US-33 | Hoàn thiện toàn diện nội dung báo cáo Chương 5 và Chương 6 | 3 | Xong (PR #88, #89, #92) | Chương 5 hoàn chỉnh (Mục 5.1, Bảng 5.1, Mục 5.2, Mục 5.3) tại `chuong-05-thuc-nghiem-va-danh-gia.md`; Chương 6 và Phụ lục A–D tại `chuong-06-ket-luan-va-huong-phat-trien.md`; Chương 1–3 được rà lại theo quy chuẩn trình bày trong PR #92. Toàn bộ báo cáo hiện có **31 bảng** và **9 hình**, mọi bảng/hình đều được dẫn chiếu trong thân bài |
| US-34 | Soạn thảo tài liệu hướng dẫn cài đặt và vận hành hệ thống (`README`) | 1 | Xong (PR #90) | `README.md` tại thư mục gốc cùng `backend/README.md`, `frontend/README.md` mô tả cài đặt môi trường, chạy `uvicorn`/`vite`, chạy `pytest`/`ruff`/`oxlint` và trải nghiệm CN01–CN03 trong 5 phút, kèm 4 ảnh giao diện tại `docs/thesis/figures/` |
| US-35 | Thiết kế slide thuyết trình và chuẩn bị kịch bản demo bảo vệ | 2 | Xong, chờ hợp nhất (PR #93) | `docs/thesis/slides/slide-bao-ve-do-an.md` gồm **16 slide** có phân bổ thời gian; `docs/thesis/slides/kich-ban-demo-bao-ve.md` gồm kịch bản demo **4 phút** chia 6 bước (KB01 $\rightarrow$ đọc kết quả $\rightarrow$ đổi mức ưu tiên $\rightarrow$ trạng thái $\sum w_i = 0$ $\rightarrow$ trạng thái `no_match` $\rightarrow$ kết thúc), **10 câu hỏi phản biện** kèm câu trả lời và bảng phương án dự phòng khi máy chiếu/mạng gặp sự cố |
| US-36 | Cập nhật mục lục, đóng gói hồ sơ đồ án và gắn tag phát hành `v1.0` | 1 | Đang làm (còn tag `v1.0`) | `docs/thesis/report/muc-luc-va-ho-so-ban-giao.md` đã đồng bộ 9 mục phần mở đầu, danh mục 31 bảng, danh mục 9 hình và hồ sơ bàn giao; 9 tệp `.gitkeep` dư thừa đã xóa (giữ `data/raw/.gitkeep`); biên bản `docs/scrum/sprints/sprint-06/{review,retrospective}.md` đã soạn. Chưa gắn tag vì PR #93 chưa hợp nhất |
| US-40 | Đề xuất mở rộng mô hình: Tổ hợp Cấp lớp và Mục tiêu học tập | 2 | Xong (PR #80, #81) | `docs/design/de-xuat-mo-rong-cap-lop-muc-tieu.md` phân tích nhu cầu ba chiều (Môn học, Cấp lớp, Mục tiêu học tập), so sánh *Adaptive Weight Mapping* và *Goal Compatibility* ($s_6$), khuyến nghị Phương án 1 kèm lộ trình và rủi ro; không sửa mã nguồn, dữ liệu hay kịch bản |
| US-41 | Thêm gợi ý mức ưu tiên theo mục tiêu học tập ở màn hình nhập nhu cầu | 2 | Xong (PR #85, #84, #86) | `frontend/src/data/goalPresets.js` định nghĩa 3 bộ điền sẵn (*Không nêu mục tiêu*, *Điểm cao/luyện thi chuyên*, *Đủ điểm đậu/lấy lại căn bản*); ô chọn tại `SearchPage.jsx` điền sẵn 5 mức ưu tiên và có trạng thái *Tùy chỉnh* khi người học sửa tay. Payload gửi `POST /api/recommend` giữ nguyên 7 trường, backend và `scenarios.json` không đổi |

*Ghi chú về các PR đã merge trong Sprint 6 (đều do `tnduckhmt2411011-design` thực hiện):*
- **US-40 (#79) — khung story:** PR #80 (`docs/79-de-xuat-mo-rong-cap-lop-muc-tieu`, merge `a517159`, 2026-11-09).
- **US-40 (#79) — tài liệu đề xuất:** PR #81 (`docs/79-tai-lieu-de-xuat-cap-lop-muc-tieu`, merge `7be429d`, 2026-11-09).
- **US-41 (#82) — đồng bộ kế hoạch:** PR #84 (`docs/82-dong-bo-us-41`, merge `c5bed51`, 2026-11-09).
- **US-41 (#82) — giao diện:** PR #85 (`feat/82-chon-muc-tieu-hoc-tap`, merge `f331dd6`, 2026-11-10).
- **US-41 (#82) — cập nhật tài liệu:** PR #86 (`docs/82-cap-nhat-tai-lieu-de-xuat`, merge `c771209`, 2026-11-10).
- **US-30 (#32):** PR #87 (`docs/32-muc-5-2-danh-gia-do-on-dinh`, merge `d9548ce`, 2026-11-10).
- **US-33 (#33):** PR #88 (`docs/33-chuong-5-thuc-nghiem-danh-gia`, merge `000cf55`, 2026-11-10); PR #89 (`docs/33-chuong-6-ket-luan-phu-luc`, merge `7c3b785`, 2026-11-11); PR #92 (`docs/chuong-1-3-hoan-thien`, merge `d7073de`, 2026-11-16).
- **US-34 (#34):** PR #90 (`docs/34-readme-huong-dan`, merge `0ca15fd`, 2026-11-11).
- **Chương 4:** PR #91 (`docs/chuong-4-xay-dung-he-thong`, merge `c17269f`, 2026-11-11).
- **US-35 (#35) + US-36 (#36):** PR #93 (`docs/doi-chieu-gs360`, head `bfe0b9b`, **đang mở**, chưa hợp nhất).

*Ghi chú về nhóm `Could Have`:* `US-37` (#37 — SQLite), `US-38` (#38 — LocalStorage), `US-39` (#39 — xuất PDF) **không** được kéo vào Sprint 6; cả ba vẫn mở trong backlog và không phải điều kiện của Cổng chất lượng 4.

---

## 3. Đánh giá Cổng chất lượng 4 (Quality Gate 4) & Kết quả kiểm thử nghiệm thu kỹ thuật

- [x] **Toàn bộ bài kiểm thử tự động và kiểm tra chất lượng mã nguồn đều vượt qua:** Workflow CI `Ruff và Pytest` xanh trên PR #93; chạy cục bộ tại `backend/` đạt **`200 passed, 0 failed, 0 skipped`** (thời gian chạy cỡ 1–2 giây tùy máy); độ bao phủ `backend/app/` đạt **97%** (340/351 câu lệnh), trong đó 7 module cốt lõi đạt 100%. Phía `frontend/`: `npm run lint` (`oxlint`) không báo lỗi/cảnh báo (mã thoát `0`) và `npm run build` (`vite build`) biên dịch thành công trong `259 ms`.
- [x] **Báo cáo Chương 5, Chương 6 và Phụ lục A–D phản ánh trung thực kết quả thực nghiệm:** Chương 5 trình bày Mục 5.1 (Bảng 5.1 với 14/14 kịch bản trùng Top-3), Mục 5.2 (độ nhạy tham số) và Mục 5.3 (6 hạn chế); Chương 6 gồm Mục 6.1 đối chiếu 4 mục tiêu, Mục 6.2 ba hướng phát triển, Mục 6.3 tự đánh giá (Bảng 6.1) cùng Phụ lục A (16 hồ sơ), B (danh mục mã nguồn), C (hình ảnh), D (kịch bản). Số liệu trong báo cáo khớp với lần chạy kiểm thử thật: 200/200 bài đạt, độ bao phủ 97%, thời gian xử lý nội tại trung bình 3,54 ms.
- [x] **`README.md`, slide và kịch bản demo sẵn sàng:** `README.md` hướng dẫn cài đặt và chạy thử trong 5 phút kèm 4 ảnh giao diện; `docs/thesis/slides/slide-bao-ve-do-an.md` (16 slide) và `docs/thesis/slides/kich-ban-demo-bao-ve.md` (kịch bản 4 phút cho CN01–CN03, 10 câu hỏi phản biện, phương án dự phòng) đã hoàn tất.
- [x] **Mục lục, danh mục hình ảnh, danh mục bảng biểu đồng bộ; repository sạch:** `muc-luc-va-ho-so-ban-giao.md` liệt kê đủ 31 bảng và 9 hình, khớp với ký hiệu trong Chương 1–6 và Phụ lục; 9 tệp `.gitkeep` dư thừa đã được xóa, không còn tệp tạm trong cây làm việc.
- [ ] **Gắn tag phát hành chính thức `v1.0` trên nhánh `main`:** chưa thực hiện — PR #93 đang mở, và nhóm chủ động chờ chỉ định hợp nhất trước khi tạo tag (xem Mục 5).

> **Kết luận Cổng chất lượng 4:** đạt **4/5 điều kiện** tại thời điểm `2026-11-17`. Điều kiện còn lại là thao tác phát hành (hợp nhất PR #93 rồi gắn tag `v1.0`), không phải hạng mục kỹ thuật hay nội dung báo cáo.

---

## 4. Bản demo sản phẩm

- **Nội dung demo:** luồng CN01 $\rightarrow$ CN02 $\rightarrow$ CN03 trên giao diện ReactJS gọi `POST /api/recommend` của backend FastAPI. Kịch bản 4 phút đi qua 6 bước: nộp KB01, đọc kết quả và lý do gợi ý, đổi mức ưu tiên để thấy thứ hạng thay đổi, thử trạng thái $\sum w_i = 0$, thử trạng thái `no_match` bằng KB05, rồi đưa giao diện về trạng thái ban đầu.
- **Số liệu dùng khi demo:** KB01 cho GS-G01 = 0,9375; GS-G10 = 0,7450; GS-T06 = 0,6250. KB05 trả `no_match`; KB04 chỉ có 2 ứng viên; KB09 chỉ có 1 ứng viên.
- **Phương án dự phòng:** bộ 4 ảnh `docs/thesis/figures/` đã mở sẵn để dùng khi máy chiếu hoặc mạng gặp sự cố; demo cục bộ không phụ thuộc mạng.
- **Điểm cần nói trước hội đồng:** tên đề tài trong văn bản đăng ký ghi “Content-Base” (thiếu chữ “d”), thân bài dùng “Content-Based Filtering”; phần này đã ghi trong kịch bản Q&A để tránh bị hiểu là sai lệch giữa bìa và nội dung.

---

## 5. Việc còn lại sau Sprint 6

| # | Việc | Người phụ trách | Trạng thái |
| :-: | :--- | :--- | :--- |
| 1 | Rà và hợp nhất PR #93 vào `main` (đóng Issue #35) | Nhóm trưởng | Chờ chỉ định |
| 2 | Tạo và đẩy tag `v1.0` sau khi hợp nhất (đóng Issue #36) | Nhóm trưởng | Chờ chỉ định |
| 3 | Diễn tập bảo vệ thử với bộ slide và kịch bản demo | Cả nhóm | Chưa làm |
| 4 | Ghép 6 chương + tài liệu tham khảo + phụ lục thành một tệp Word theo mẫu, điền số trang mục lục | Nhóm | Chưa làm (thao tác Word, ngoài kho mã) |
| 5 | Ba story `Could Have` (US-37, US-38, US-39) | — | Giữ trong backlog, ngoài phạm vi đồ án |
