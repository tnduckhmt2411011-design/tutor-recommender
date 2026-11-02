> [!NOTE]
> **Đề xuất, nhóm xác nhận**

# Sơ kết Sprint 1 (Sprint 1 Review)

- **Ngày họp:** *[Chờ nhóm điền]*
- **Người chủ trì:** Scrum Master (Trần Nguyễn Đức)
- **Thành phần tham dự:** *[Chờ nhóm điền]*

---

## 1. Kết quả thực hiện mục tiêu Sprint

- **Mục tiêu đặt ra:** Khóa thiết kế bài toán và công thức tính điểm với GVHD; số hóa dữ liệu 16 hồ sơ gia sư và 14 kịch bản kiểm thử vào repo; thiết lập API contract; dựng khung môi trường backend và frontend; hoàn thiện các mục còn treo trong đề cương.
- **Đánh giá mức độ hoàn thành:** *[Đạt / Chưa đạt]*

---

## 2. Rà soát chi tiết User Stories

| Mã US | Tên User Story | Điểm SP | Trạng thái | Ghi chú nghiệm thu |
|:---|:---|:---:|:---:|:---|
| US-01 | Khởi tạo môi trường ảo backend | 1 | Xong (PR #41) | |
| US-02 | Quy trình CI GitHub Actions | 1 | Xong (PR #44) | |
| US-03 | Khung frontend ReactJS Vite | 1 | Xong (PR #45) | |
| US-04 | Quy trình Scrum & DoR | 1 | Xong (PR #40) | |
| US-05 | Báo cáo chốt bài toán với GVHD | 1 | Đang chờ merge (PR #58) | |
| US-06 | Dữ liệu 16 hồ sơ Phụ lục A | 2 | Xong (PR #42) | |
| US-07 | 14 kịch bản scenarios.json | 2 | Xong (PR #43) | |
| US-08 | Hợp đồng API Contract | 1 | Xong (PR #46) | |
| US-31 | Tài liệu tham khảo GS360 | 1 | Đang chờ merge (PR #59) | |
| US-32 | Điền Bảng 6.1 & mục 6.1 | 1 | Đang chờ merge (PR #60) | |

*Ghi chú về các PR đã merge và PR bổ sung/hiệu chỉnh (đều do `tnduckhmt2411011-design` thực hiện):*
- **US-01 (#1):** PR #41 (merge 2026-11-01).
- **US-02 (#2):** PR #44 (merge 2026-11-01).
- **US-03 (#3):** PR #45 (merge 2026-11-01).
- **US-04 (#4):** PR #40 (merge 2026-10-31), bổ sung PR #47 và PR #51 (merge 2026-11-02).
- **US-05 (#5):** PR #58 (`docs/thesis/review/sprint-01-problem-lock-report.md`).
- **US-06 (#6):** PR #42 (merge 2026-11-01), sửa nhãn môn `GS-G03` tại PR #48 (merge 2026-11-02).
- **US-07 (#7):** PR #43 (merge 2026-11-01), ghi quyết định cho KB04, KB09, KB14 tại PR #49 (merge 2026-11-02).
- **US-08 (#8):** PR #46 (merge 2026-11-02).
- **US-31 (#9):** PR #59 (`docs/thesis/outline/muc-1.3-gs360.md`).
- **US-32 (#10):** PR #60 (`docs/thesis/outline/muc-6.1-bang-6.1.md`).

---

## 3. Đánh giá Cổng chất lượng 1 (Quality Gate 1)

- [x] Công thức tính điểm Bảng 3.6 và dữ liệu 16 hồ sơ nằm trong repo (đã kiểm chứng: `docs/design/scoring-spec.md`, `data/processed/tutors.json`, `data/processed/tutors.csv`).
- [x] 14 kịch bản kiểm thử với Top-3 kỳ vọng nguyên văn nằm trong repo (đã kiểm chứng: `backend/tests/scenarios/scenarios.json`).
- [x] Tài liệu API Contract được phê duyệt (tài liệu `docs/design/api-contract.md` đã merge qua PR #46; phê duyệt của PO theo Đức báo).
- [x] GVHD đã nhận báo cáo khóa bài toán (theo Đức báo; biên bản lưu tại `docs/thesis/review/sprint-01-problem-lock-report.md` — PR #58).
- **Kết luận:** *[Đủ điều kiện chuyển sang Sprint 2 / Cần bổ sung]*
