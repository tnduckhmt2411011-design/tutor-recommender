# Nâng cấp Giao diện Hybrid Modern Studio (Dark Mode Mặc định + Rank #1 Hero Glow) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Chuyển đổi giao diện sang phong cách **Hybrid Modern Studio** (Shadcn Slate Dark + Tremor Vibrant Analytics + Linear Hero Glow) giúp triệt tiêu 100% hiện tượng chói mắt, tạo điểm nhấn đẳng cấp cho Quán quân Rank #1, bổ sung nút chuyển đổi chế độ ☀️ Sáng / 🌙 Tối, đồng thời đảm bảo 100% không ảnh hưởng tới logic tính toán backend và hợp đồng API.

**Architecture:**
- **Theme Engine (CSS Variables & Data Attribute):**
  - Cấu hình mặc định `theme = 'dark'` trên thẻ `<html>` hoặc `#root` với bảng màu Slate than chì sâu (`#0b0f19` / `#111827` / `#1f2937`), chữ sáng dịu (`#f9fafb`), viền mờ cao cấp (`#374151`).
  - Hỗ trợ chế độ Warm Light qua `[data-theme="light"]` (nền giấy ngà ấm dịu `#f8fafc`, không dùng trắng gắt).
  - Lưu lựa chọn vào `localStorage.getItem('tutor_theme')`.
- **Hero Elevation & Visual Hierarchy:**
  - Thẻ Quán quân (Rank #1) sở hữu hiệu ứng viền Emerald (`#10b981`), vầng sáng dịu nhẹ (`rgba(16, 185, 129, 0.12)`), và huy hiệu *"Khuyến nghị tốt nhất"*.
  - Thẻ Rank #2 và Rank #3 giữ tông màu Slate trầm tạo bậc thang thị giác rõ rệt.
- **Bảng màu Tiêu chí Rực rỡ (Tremor Palette):**
  - Cập nhật 5 mã màu trong `frontend/src/data/tutorsCatalog.js`: Học phí (Emerald `#10b981`), Khu vực (Sky `#0ea5e9`), Kinh nghiệm (Violet `#8b5cf6`), Đánh giá (Amber `#f59e0b`), Lịch rảnh (Rose `#f43f5e`).

**Tech Stack:** React 19, CSS Variables, Vite 8, Vercel, Render.

**Spec:** `docs/design/scoring-spec.md`, `docs/design/api-contract.md`.

---

## Global Constraints

- **Tuyệt đối không chạm vào Backend:** 190 tests backend, công thức toán học, 16 gia sư và 14 kịch bản giữ nguyên 100%.
- **Working Tree Isolation:** Main repo giữ sạch 100% trên `chore/2-ci-github-actions`. Mọi chỉnh sửa chỉ thực hiện trong worktree `$env:TEMP\wt-live-demo`.
- **Bảo toàn Văn bản Word:** Giữ nguyên các định dạng in đậm và chỉnh sửa tay của người dùng trong `BAO_CAO_TIEN_DO_GIUA_KY_DO_AN_KHMT1.docx`.

---

## Tasks

- [ ] **Task 1: Cấu hình Tokens CSS Dark / Light Mode (`frontend/src/index.css`)**
  - [ ] Thiết lập bảng màu Dark Mode mặc định (Slate 900 `#0b0f19`, Card `#111827`, Raised `#1f2937`, Border `#374151`, Text `#f9fafb`, Muted `#9ca3af`).
  - [ ] Thiết lập bảng màu Warm Light `[data-theme="light"]`.
  - [ ] Tinh chỉnh style scrollbar và selection đồng bộ theo Dark Mode.

- [ ] **Task 2: Đồng bộ Bảng màu 5 Tiêu chí Tremor (`frontend/src/data/tutorsCatalog.js`)**
  - [ ] Cập nhật mã màu trong `CRITERIA_META` sang bảng màu Tremor tương phản cao.

- [ ] **Task 3: Nâng cấp Theme Switcher & Navbar (`frontend/src/App.jsx`)**
  - [ ] Thêm state `theme` ('dark' | 'light') đọc từ `localStorage`, đồng bộ lên `document.documentElement.setAttribute('data-theme', theme)`.
  - [ ] Bổ sung nút bấm chuyển đổi theme ☀️ / 🌙 trên thanh điều hướng `workflow-nav`.

- [ ] **Task 4: Thiết kế Thẻ Quán quân Rank #1 & Tối ưu Giao diện (`frontend/src/App.css` & `TutorCard.jsx`)**
  - [ ] Bổ sung badge *"Khuyến nghị tốt nhất"* và class `rank-1-hero` cho thẻ Top-1 trong `TutorCard.jsx`.
  - [ ] Thiết lập style viền Emerald, elevation glow và thứ bậc phân tầng trong `App.css`.
  - [ ] Căn chỉnh độ tương phản của SearchPage, ma trận lịch và rail điều chỉnh CN03 trên nền tối.

- [ ] **Task 5: Kiểm thử, Nghiệm thu & Chụp ảnh Mới**
  - [ ] Chạy `npm run lint` (`oxlint`) và `npm run build` (0 lỗi).
  - [ ] Chạy `pytest tests -q` backend (190 passed).
  - [ ] Dùng Playwright chụp lại trọn bộ 5 ảnh demo thực tế trên nền giao diện mới.
  - [ ] Cập nhật 5 ảnh mới vào file Word `BAO_CAO_TIEN_DO_GIUA_KY_DO_AN_KHMT1.docx` (giữ nguyên in đậm của người dùng).
  - [ ] Commit & Đẩy lên PR #76, tự động deploy lên Vercel (`https://tutor-recommender.vercel.app`).
