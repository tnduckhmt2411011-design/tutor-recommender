# Final UI Polish & Motion Retina Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Hoàn thiện đợt tinh chỉnh giao diện cuối cùng theo đánh giá chuyên môn của frontend developer: đồng bộ góc chụp vai–đầu và nền trung tính cho 16 ảnh chân dung WebP chuẩn Retina (240x240), kích hoạt chuyển động Spring Stagger mượt mà cho 3 thẻ kết quả Top-3, và hoàn thiện trải nghiệm Loading Shimmer chuẩn thuật toán MCDA.

**Architecture:**
1. **Chân dung Retina & Đồng bộ Style:** Nâng cấp độ phân giải từ 160x160 lên 240x240 WebP (mật độ 4,5x trên frame hiển thị 52px), đồng bộ chặt chẽ góc chụp vai–đầu (face crop ~65% khung hình) với ánh sáng mềm và phông nền studio/học đường trung tính, lưu tại `frontend/public/avatars/{tutor_id}.webp`.
2. **Motion Coordination & Stagger Top-3:** Khắc phục triệt để hiện tượng che khuất animation giữa `AnimatePresence` cấp trang trong `App.jsx` và danh sách thẻ trong `ResultPage.jsx`. Sử dụng Motion container `variants` với `staggerChildren: 0.15s` và `delayChildren: 0.1s`, thẻ con lướt lên với Spring (`stiffness: 260, damping: 20`), loại bỏ motion article lồng nhau trong `TutorCard.jsx` và bổ sung hover lift `whileHover={{ y: -3 }}`.
3. **Loading UX & Phản hồi tính toán MCDA:** Tăng thời gian hiển thị tính toán tối thiểu (`minDelayPromise`) trong `App.jsx` lên 650ms để người dùng cảm nhận rõ rệt bước chuẩn hóa dữ liệu & xếp hạng đa tiêu chí MCDA; nâng cấp `SkeletonLoader.jsx` và `App.css` với hiệu ứng shimmer ngọc lục bảo (emerald) tinh tế. Bổ sung loading pulse phản hồi tức thì khi click thay đổi trọng số CN03.
4. **Bảo toàn lõi & Cập nhật Báo cáo:** Giữ nguyên 100% công thức tính toán MCDA, 16 hồ sơ gia sư và 190 backend test cases. Cập nhật in-place 5 ảnh chụp giao diện mới vào tài liệu Word `BAO_CAO_TIEN_DO_GIUA_KY_DO_AN_KHMT1.docx` (bảo toàn toàn bộ in đậm và các dòng chữ ký đã xóa của người dùng), sau đó commit, push PR #77 và deploy Vercel Production.

**Tech Stack:** React 19, Vite 8, `motion/react` v14, Python Pillow 13.0, Playwright, Vercel CLI, python-docx & zipfile.

**Spec:** Đánh giá phản biện của Frontend Developer (Điểm hiện tại ~8.0–8.5/10; các điểm cần tinh chỉnh: 1. Đồng bộ style ảnh vai-đầu và nền trung tính; 2. Thêm Motion stagger nảy cho Top-3; 3. Skeleton loading rõ ràng khi tìm kiếm; 4. Bản ảnh 2x Retina sắc nét).

---

## Global Constraints

- **Bảo toàn lõi hệ thống (Zero Impact):** Giữ nguyên tuyệt đối thuật toán MCDA (chuẩn hóa Min-Max, trọng số $w_i \in [0, 3]$, tổng điểm $S(g)$, quy tắc phá hòa theo $tutor\_id$). 190 backend test cases phải PASS 100%.
- **Quy tắc cô lập Git:** Toàn bộ công việc thực hiện trên worktree cô lập `C:\Users\LENOVO\AppData\Local\Temp\wt-live-demo` tại nhánh `feat/hybrid-modern-studio-ui` (PR #77). Thư mục gốc `tutor-recommender` giữ sạch trên nhánh `chore/2-ci-github-actions`.
- **Bảo toàn tài liệu Word:** Không làm mất bất kỳ định dạng in đậm thủ công nào của người dùng và giữ nguyên các dòng chữ ký đã xóa trong `BAO_CAO_TIEN_DO_GIUA_KY_DO_AN_KHMT1.docx`.
- **Tiêu chuẩn Avatar:** Định dạng WebP, kích thước 240x240px, dung lượng < 25KB/ảnh, góc vai trở lên, biểu cảm thân thiện, nền trung tính sạch sẽ, hỗ trợ fallback Monogram Initials.

---

## Review Focus

1. **Hiển thị Retina & Tỷ lệ khuôn mặt:** 16 ảnh chân dung khi render ở kích thước 52px phải sắc nét hoàn hảo trên màn hình Retina/4K, không bị mờ nhòe hay vỡ hạt; khuôn mặt nằm cân đối ở trung tâm (vai–đầu).
2. **Đồng bộ chuyển động Stagger:** Khi chuyển sang trang kết quả Top-3, 3 thẻ gia sư phải lần lượt lướt vào từ dưới lên với độ trễ so le 0.15s giữa các thẻ, tạo cảm giác mượt mà và sinh động thay vì hiện cứng.
3. **Hiển thị Skeleton Loading:** Khi người dùng bấm "Tìm gia sư" hoặc chọn kịch bản mẫu, bộ khung xương Skeleton 3 thẻ phải xuất hiện rõ nét với hiệu ứng sóng ánh sáng trong khoảng 650ms trước khi bung kết quả thật.
4. **Tương tác trực tiếp CN03:** Khi click điều chỉnh mức ưu tiên các tiêu chí trên bảng trượt bên trái, thẻ kết quả phải mượt mà cập nhật vị trí kèm hiệu ứng nâng thẻ mà không bị giật lag.
5. **Fallback an toàn:** Nếu một tệp ảnh đại diện bị thiếu hoặc mạng ngắt quãng, avatar phải tự động fallback mượt mà sang Monogram Initials trên nền gradient sang trọng, không sinh lỗi console hay vỡ layout.

---

### Task 1: Nâng Cấp Bộ 16 Ảnh Chân Dung WebP Chuẩn Retina (240x240) & Đồng Bộ Style

**Files:**
- Create/Modify: `frontend/public/avatars/GS-T06.webp` ... `GS-G12.webp` (16 tệp)
- Script: `scratch/process_portraits_retina.py`
- Modify: `frontend/src/components/TutorAvatar.jsx`

**Interfaces:**
- Consumes: URL ảnh gốc độ phân giải cao Unsplash License, tham số crop mặt `crop=faces,top&w=600&h=600&q=90`.
- Produces: 16 tệp WebP 240x240px chất lượng cao (~14–18KB) với góc chụp vai–đầu cân đối và nền trung tính tại `frontend/public/avatars/`.
- Component `TutorAvatar.jsx` hiển thị `img` với thuộc tính kích thước tường minh và xử lý fallback tin cậy.

- [ ] **Step 1: Viết script tải và chuẩn hóa 16 chân dung Retina 240x240**
Tạo script `scratch/process_portraits_retina.py` lấy nguồn ảnh chân dung độ phân giải cao, crop căn giữa mặt theo tỷ lệ vai–đầu, resize Lanczos 240x240, xuất WebP quality=90.
- [ ] **Step 2: Chạy script xử lý ảnh và xác minh kích thước**
Chạy: `python scratch/process_portraits_retina.py`.
Xác minh: 16 tệp WebP tồn tại trong `frontend/public/avatars/`, kích thước đồng đều 240x240, dung lượng mỗi tệp từ 10KB đến 22KB.
- [ ] **Step 3: Cập nhật component `TutorAvatar.jsx`**
Cấu hình thẻ `<img>` với `width={size}`, `height={size}`, `decoding="async"` và style `objectFit: 'cover'`, duy trì viền bo tròn 12px và bóng đổ tinh tế.
- [ ] **Step 4: Commit thay đổi Task 1**
```bash
git add frontend/public/avatars/ frontend/src/components/TutorAvatar.jsx
git commit -m "feat(frontend): upgrade 16 portrait avatars to 240x240 WebP Retina with synchronized head-and-shoulders crop"
```

---

### Task 2: Triển Khai Motion Spring Stagger Hoàn Chỉnh Cho Top-3

**Files:**
- Modify: `frontend/src/pages/ResultPage.jsx`
- Modify: `frontend/src/components/TutorCard.jsx`
- Modify: `frontend/src/App.css`

**Interfaces:**
- Consumes: Thư viện `motion/react` v14, danh sách kết quả `results`.
- Produces: Hệ thống Animation Variants phân tầng (`listVariants` trên container cha, `cardVariants` trên từng thẻ con), loại bỏ motion lồng nhau xung đột, bổ sung hiệu ứng hover lift.

- [ ] **Step 1: Cấu hình Motion Variants trên `ResultPage.jsx`**
Định nghĩa `listVariants` (staggerChildren: 0.15, delayChildren: 0.08) và `cardVariants` (hidden: opacity 0, y 36, scale 0.95; visible: opacity 1, y 0, scale 1, spring stiffness 260, damping 20).
Gắn `variants={listVariants}` và `initial="hidden" animate="visible"` vào container danh sách thẻ.
- [ ] **Step 2: Tinh gọn và phối hợp animation trong `TutorCard.jsx`**
Thay thế thẻ bọc `motion.article` có `initial/animate` riêng bằng thẻ `<article className="tutor-card">` chuẩn, để motion container bên ngoài điều phối nhịp nhàng; bổ sung tương tác hover mượt mà.
- [ ] **Step 3: Bổ sung CSS hover elevation và transition mượt mà**
Trong `App.css`, tinh chỉnh transition cho `.tutor-card`: bổ sung đổ bóng nhẹ khi hover (`box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.45)`) và viền sáng tinh tế.
- [ ] **Step 4: Kiểm tra lint và build frontend**
Chạy: `npm run lint` và `npm run build` trong `frontend/`.
- [ ] **Step 5: Commit thay đổi Task 2**
```bash
git add frontend/src/pages/ResultPage.jsx frontend/src/components/TutorCard.jsx frontend/src/App.css
git commit -m "feat(frontend): implement canonical Motion variants stagger and hover elevation on Top-3 cards"
```

---

### Task 3: Hoàn Thiện Trải Nghiệm Skeleton Shimmer & Loading Feedback

**Files:**
- Modify: `frontend/src/App.jsx`
- Modify: `frontend/src/components/SkeletonLoader.jsx`
- Modify: `frontend/src/App.css`

**Interfaces:**
- Consumes: Cờ trạng thái `isCalculating` và `isUpdatingPriorities`.
- Produces: Thời gian hiển thị tính toán tối thiểu 650ms mượt mà, hiệu ứng shimmer gradient ngọc lục bảo (emerald) sống động, visual badge hiển thị tiến trình thuật toán MCDA.

- [ ] **Step 1: Điều chỉnh độ trễ tính toán tối thiểu trong `App.jsx`**
Đặt `minDelayPromise` thành 650ms khi `options.switchToResult` kích hoạt, đảm bảo hiệu ứng chuyển cảnh từ Form sang Skeleton diễn ra êm ái, người dùng nhìn rõ quá trình tính toán gợi ý.
- [ ] **Step 2: Nâng cấp `SkeletonLoader.jsx` và CSS Shimmer Wave**
Cập nhật `App.css` với dải màu shimmer hiện đại (shimmer wave lướt từ trái sang phải với ánh sáng ngọc lục bảo mờ dịu `rgba(16, 185, 129, 0.08)`).
- [ ] **Step 3: Bổ sung loading visual indicator khi điều chỉnh trọng số CN03**
Hiển thị thanh tiến trình hoặc spinner nhỏ trang nhã trên header của rail CN03 khi đang cập nhật lại thứ hạng (`isUpdatingPriorities`).
- [ ] **Step 4: Kiểm tra build frontend**
Chạy: `npm run build` trong `frontend/`.
- [ ] **Step 5: Commit thay đổi Task 3**
```bash
git add frontend/src/App.jsx frontend/src/components/SkeletonLoader.jsx frontend/src/App.css
git commit -m "feat(frontend): enhance MCDA calculation skeleton shimmer and live CN03 update feedback"
```

---

### Task 4: Kiểm Thử Toàn Diện, Chụp Ảnh Minh Họa & Cập Nhật Báo Cáo Word

**Files:**
- Test: `backend/tests/` (190 test cases)
- Script: `scratch/verify_polished_ui.py`
- Create: `docs/thesis/assets/midterm/hinh-1-cn01-nhap-nhu-cau.png` ... `hinh-3-cn03-dieu-chinh-uu-tien.png`
- Modify: `BAO_CAO_TIEN_DO_GIUA_KY_DO_AN_KHMT1.docx` (in-place zip replacement)

**Interfaces:**
- Consumes: Headless Chromium via Playwright, server Vite local `127.0.0.1:5173`, backend FastAPI `127.0.0.1:8000`.
- Produces: Báo cáo kiểm thử 100% pass, bộ 5 ảnh chụp độ nét cao giao diện đã tinh chỉnh, tệp docx được cập nhật hoàn hảo.

- [ ] **Step 1: Chạy toàn bộ backend test suite**
Chạy: `pytest` trên môi trường backend.
Kỳ vọng: 190 passed trong < 1.0s.
- [ ] **Step 2: Viết script Playwright kiểm chứng Motion, Skeleton và Retina**
Tạo script `scratch/verify_polished_ui.py`:
- Kiểm tra trạng thái Skeleton hiển thị khi bấm tìm kiếm.
- Kiểm tra 3 thẻ gia sư xuất hiện với ảnh WebP 240x240 và rank badge đè góc trên bên trái.
- Kiểm tra tính năng kéo trượt CN03 không bị đè che.
- [ ] **Step 3: Chụp 3 ảnh giao diện mới và cập nhật thư mục assets**
Lưu 3 ảnh độ phân giải cao (`hinh-1-cn01-nhap-nhu-cau.png`, `hinh-2-cn02-ket-qua-top3.png`, `hinh-3-cn03-dieu-chinh-uu-tien.png`) vào `docs/thesis/assets/midterm/`.
- [ ] **Step 4: Cập nhật tài liệu Word `BAO_CAO_TIEN_DO_GIUA_KY_DO_AN_KHMT1.docx` in-place**
Sử dụng script Python zipfile cập nhật trực tiếp `word/media/image1.png` ... `image3.png`, bảo toàn 100% cấu trúc XML, định dạng in đậm và các chữ ký đã xóa.
- [ ] **Step 5: Commit và Push PR #77, Deploy Vercel Production**
```bash
git add docs/thesis/assets/midterm/
git commit -m "docs(thesis): update polished UI screenshots with retina portraits and motion"
git push origin feat/hybrid-modern-studio-ui
```
Deploy lên Vercel production và xác minh trên URL live.
