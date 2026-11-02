> [!NOTE]
> **Đề xuất, nhóm xác nhận**

# Sơ kết Sprint 5 (Sprint 5 Review)

- **Ngày họp:** *[Chờ nhóm điền]*
- **Người chủ trì:** Scrum Master (Trần Nguyễn Đức)
- **Thành phần tham dự:** *[Chờ nhóm điền]*

---

## 1. Kết quả thực hiện mục tiêu Sprint

- **Mục tiêu đặt ra:** Màn hình kết quả và tích hợp (Epic E5 & E6) — hoàn thiện màn hình hiển thị danh sách gia sư gợi ý `ResultPage` (CN02) kèm thẻ thông tin `TutorCard` và biểu đồ thanh xếp chồng phân rã điểm đóng góp `StackedBarScore`, hiện thực tính năng điều chỉnh mức ưu tiên tương tác trực tiếp trên màn hình kết quả (CN03), kết nối toàn diện luồng end-to-end từ `SearchPage` (CN01) sang `ResultPage` (CN02 + CN03) với API `POST /api/recommend`, đồng thời thực hiện kiểm thử các ca biên theo Mục 5.1 và điền đầy đủ cột **"Top-3 hệ thống"** vào **Bảng 5.1** để vượt qua **Cổng chất lượng 3 (Quality Gate 3)**.
- **Đánh giá mức độ hoàn thành:** *[Đạt / Chưa đạt]*

---

## 2. Rà soát chi tiết User Stories

| Mã US | Tên User Story | Điểm SP | Trạng thái | Ghi chú nghiệm thu |
|:---|:---|:---:|:---:|:---|
| US-25 | Xây dựng màn hình hiển thị danh sách kết quả gợi ý (`ResultPage` — CN02) | 3 | Xong (PR #71) | Xây dựng `frontend/src/data/tutorsCatalog.js` (tra cứu 16 hồ sơ chuẩn hóa theo `tutor_id` mà không sửa `api-contract.md`), `frontend/src/components/TutorCard.jsx` và `frontend/src/pages/ResultPage.jsx` theo Hình 3.5 đề cương; hiển thị đầy đủ trạng thái `success`, `no_match` (kèm `insufficient_data_candidates`) và `zero_weight` (kèm `unranked_candidates`) |
| US-26 | Trực quan hóa mức đóng góp của từng tiêu chí bằng biểu đồ thanh xếp chồng (`StackedBarScore`) | 2 | Xong (PR #71) | Cài đặt `frontend/src/components/StackedBarScore.jsx` vẽ thanh xếp chồng nhiều màu trên thang `[0, 1]` theo đúng tỷ trọng $C_i = w_i \cdot s_i / \sum w_i$, tự động ẩn tiêu chí bị loại (`contributions[i] === null`) và hiển thị tooltip chi tiết ($s_i$, $w_i$, $C_i$, tỷ lệ phần trăm) |
| US-27 | Tích hợp tính năng điều chỉnh mức ưu tiên trực tiếp trên màn hình kết quả (CN03) | 3 | Xong (PR #72) | Bảng điều khiển mức ưu tiên trực tiếp (CN03) ngay trên `ResultPage.jsx`, tự động gọi lại `POST /api/recommend` khi đổi mức ưu tiên (`none`, `low`, `medium`, `high`), hiển thị thời gian phản hồi thực tế (`ms`) và huy hiệu biến động thứ hạng (`rankDeltas`) |
| US-28 | Kết nối tích hợp Frontend – Backend và kiểm thử luồng nghiệp vụ end-to-end | 2 | Xong (PR #72) | Bổ sung bộ nạp nhanh 14 kịch bản thực nghiệm (`KB01`–`KB14`) tại `frontend/src/data/scenariosCatalog.js` và kết nối luồng điều hướng hai chiều `SearchPage.jsx` (CN01) $\leftrightarrow$ `ResultPage.jsx` (CN02 + CN03) trong `frontend/src/App.jsx` và `frontend/src/App.css` |
| US-29 | Kiểm thử chức năng, các ca biên Mục 5.1 và hoàn thiện kết quả Bảng 5.1 | 2 | Xong (PR #73) | Bổ sung 6 bài kiểm thử tự động các ca biên Mục 5.1, tính đơn điệu và luồng CN03 tại `backend/tests/api/test_boundary_muc_5_1.py`; lập báo cáo `docs/thesis/report/muc-5.1-bang-5.1-ket-qua.md` điền đầy đủ cột **"Top-3 hệ thống"** của **Bảng 5.1** cho 14/14 kịch bản (`KB01`–`KB14`) |

*Ghi chú về các PR đã merge trong Sprint 5 (đều do `tnduckhmt2411011-design` thực hiện):*
- **Biên bản Sprint 4 & kế hoạch Sprint 5:** PR #70 (`docs/sprint-04-review-sprint-05-planning`, merge `45e6882`, 2026-11-02).
- **US-25 (#27) + US-26 (#28):** PR #71 (`feat/27-28-man-hinh-ket-qua-va-stacked-bar`, merge `889006b`, 2026-11-02).
- **US-27 (#29) + US-28 (#30):** PR #72 (`feat/29-30-dieu-chinh-uu-tien-cn03-va-tich-hop-e2e`, merge `d1553ec`, 2026-11-02).
- **US-29 (#31):** PR #73 (`test/31-kiem-thu-ca-bien-muc-5-1-va-bang-5-1`, merge `dd58f52`, 2026-11-02).

---

## 3. Đánh giá Cổng chất lượng 3 (Quality Gate 3) & Kết quả kiểm thử nghiệm thu kỹ thuật

- [x] **Luồng end-to-end chạy trơn tru từ giao diện ReactJS (`SearchPage` $\rightarrow$ `ResultPage`) tới backend FastAPI (`POST /api/recommend`):** Người học có thể nhập nhu cầu tìm kiếm hoặc chọn nạp nhanh 1 trong 14 kịch bản thực nghiệm (`KB01`–`KB14`), gửi yêu cầu đến backend và nhận kết quả xếp hạng Top-$k$ kèm thanh xếp chồng phân rã điểm số, lý do gợi ý và ghi chú dữ liệu.
- [x] **Tính năng điều chỉnh mức ưu tiên trực tiếp (CN03) tự động gọi lại API và cập nhật thứ hạng kèm thanh xếp chồng dưới 1 giây:** Thời gian phản hồi trung bình của `POST /api/recommend` đạt `~4,75 ms` (`< 1000 ms`), giúp thứ hạng, điểm thành phần và huy hiệu biến động hạng cập nhật tức thì khi người học thay đổi mức ưu tiên trên `ResultPage.jsx`.
- [x] **Hoàn thành kiểm thử chức năng, các ca biên theo Mục 5.1 đề cương và điền đầy đủ cột "Top-3 hệ thống" vào Bảng 5.1:** Bộ kiểm thử `backend/tests/api/test_boundary_muc_5_1.py` xác nhận toàn bộ các điểm biên học phí ($P=B$, $P=1{,}25B$, $P=1{,}5B$, $P>1{,}5B$, $B=0$), kinh nghiệm ($E=0, 8, 20$), đánh giá (`None` và `5.0`), lịch rảnh ($1/k \dots k/k$), tính đơn điệu và luồng CN03; tài liệu `docs/thesis/report/muc-5.1-bang-5.1-ket-qua.md` đã điền đầy đủ cột **"Top-3 hệ thống"** của **Bảng 5.1** với tỷ lệ trùng khớp **14/14 kịch bản (100%)**.
- [x] **Chất lượng mã nguồn và độ bao phủ kiểm thử trên `origin/main` (`dd58f52`):**
  - **Backend (`backend/`):** `ruff check .` chạy sạch (`All checks passed!`); `pytest -v -rs` đạt **`190 passed, 0 skipped`**; độ bao phủ mã nguồn `backend/app/` đạt **96%** (`100%` trên `recommend.py`, `main.py`, `schemas/*`, `repository.py`, `filters.py`, `weights.py`).
  - **Frontend (`frontend/`):** `npm run lint` (`oxlint`) đạt `Found 0 warnings and 0 errors` trên 10 tệp; `npm run build` (`vite build`) biên dịch thành công (`~257 ms`).
- **Kết luận:** *[Đủ điều kiện chuyển sang Sprint 6 / Cần bổ sung]*
