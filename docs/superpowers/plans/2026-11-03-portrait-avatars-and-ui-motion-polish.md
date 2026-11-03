# Portrait Avatars & UI Motion Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Triển khai bộ 16 ảnh chân dung gia sư người thật chuẩn học đường (WebP 160x160), tích hợp vào `TutorAvatar.jsx` với fallback monogram/boring-avatars, đè rank badge góc ảnh, bổ sung Skeleton shimmer loading khi bấm "Tìm gia sư" và làm rõ nét hiệu ứng chuyển động Spring Stagger của Motion.

**Architecture:** 
1. Thu thập và chuẩn hóa 16 ảnh chân dung sinh viên/giảng viên Đông Nam Á / Châu Á độ tuổi 20–30 từ nguồn ảnh mở bản quyền tự do (Unsplash License). Dùng Python Pillow tự động crop 1:1, resize 160x160, nén WebP chất lượng cao (~12–15KB/ảnh) đặt tại `frontend/public/avatars/{tutor_id}.webp`.
2. Nâng cấp `TutorAvatar.jsx` ưu tiên tải ảnh WebP cục bộ, có thuộc tính `alt="Gia sư {tutor_id}"`, nhãn minh họa và fallback tự động sang Monogram Initials / Boring Avatars nếu tệp không tồn tại hoặc lỗi tải.
3. Cập nhật `TutorCard.jsx` và `App.css` để huy hiệu thứ hạng (Rank badge #1, #2, #3...) đè nổi góc trên của ảnh chân dung theo đúng yêu cầu UI.
4. Nâng cấp `ResultPage.jsx` và `App.jsx` bổ sung trạng thái Skeleton loading 3 thẻ khi bấm "Tìm gia sư" hoặc chọn kịch bản mẫu, kết hợp hiệu ứng Spring Stagger lướt thẻ rõ nét và chuyển step mượt mà.

**Tech Stack:** React 19, Vite 8, `motiondivision/motion` v14, Python Pillow 13.0, Playwright, Vercel CLI.

**Spec:** Yêu cầu người dùng (Phương án 2: Chân dung người thật chọn lọc, tiêu chí 20-30 tuổi, góc vai trở lên, nền sạch, biểu cảm thân thiện, WebP 1:1, rank badge đè góc ảnh, fallback initials).

## Global Constraints

- **Bảo toàn lõi hệ thống (Zero Impact):** Không thay đổi công thức tính điểm MCDA, không sửa dữ liệu `tutors.json`, giữ nguyên 190 test case backend pass 100%.
- **Quy tắc cô lập Git:** Thực hiện toàn bộ công việc trên worktree cô lập `wt-live-demo` nhánh `feat/hybrid-modern-studio-ui` (PR #77), không chạm vào main repository.
- **Tiêu chuẩn ảnh chân dung:** Độ tuổi 20–30, góc chụp vai trở lên, ánh sáng mềm, nền studio/học đường trang nhã, biểu cảm nhẹ nhàng thân thiện, định dạng WebP 160x160px.
- **Bảo toàn văn bản Word:** Giữ nguyên 100% in đậm và xóa dòng chữ ký thủ công trong `BAO_CAO_TIEN_DO_GIUA_KY_DO_AN_KHMT1.docx`.

## Review Focus

1. **Thiếu file ảnh hoặc sai đường dẫn:** `TutorAvatar` phải tự động fallback sang Monogram Initials mang mã số gia sư kèm màu gradient mà không làm vỡ layout hay báo lỗi console.
2. **Kích thước ảnh và hiệu năng:** 16 ảnh WebP phải dưới 25KB/ảnh, load tức thì từ `public/avatars/` không gây trễ mạng.
3. **Hiển thị Rank badge đè góc:** Badge hạng `#1`, `#2`, `#3` phải nằm đè chính xác ở góc trên bên trái của ảnh đại diện (overlap) trên cả màn hình lớn và nhỏ.
4. **Trạng thái Skeleton Loading:** Khi bấm "Tìm gia sư", giao diện phải hiển thị rõ Skeleton 3 thẻ trong ~350-400ms trước khi bung kết quả, giúp người dùng cảm nhận được phản hồi tương tác rõ rệt.
5. **Hiệu ứng Motion Stagger:** 3 thẻ gia sư Top-3 phải lần lượt bay vào so le rõ rệt theo trục Y và scale với đường cong spring nảy êm ái.

---

### Task 1: Thu thập, Chuẩn hóa & Xuất 16 Ảnh Chân Dung WebP (160x160)

**Files:**
- Create: `frontend/public/avatars/GS-T06.webp` ... `GS-G12.webp` (16 tệp)
- Script: `scratch/process_portraits.py`

**Interfaces:**
- Input: 16 ảnh chân dung người thật độ tuổi 20–30 phong cách học đường châu Á từ Unsplash License.
- Output: 16 tệp WebP chuẩn kích thước 160x160px, dung lượng ~12–18KB mỗi ảnh tại `frontend/public/avatars/`.

- [ ] **Step 1: Viết script tải và chuẩn hóa 16 ảnh chân dung**
Viết `scratch/process_portraits.py` sử dụng thư viện `Pillow` và `urllib`: tải 16 chân dung phù hợp tiêu chí (sinh viên/giảng viên trẻ châu Á, góc vai trở lên, nền sạch, cười nhẹ), crop center 1:1, resize `160x160`, nén WebP với `quality=85`.

- [ ] **Step 2: Chạy script xử lý ảnh và kiểm tra kết quả**
Chạy: `python scratch/process_portraits.py`
Xác minh: Thư mục `frontend/public/avatars/` có đủ 16 file WebP đúng tên mã gia sư (`GS-T06.webp`, `GS-T07.webp`, `GS006.webp`, `GS020.webp`, `GS-G01.webp` ... `GS-G12.webp`).

- [ ] **Step 3: Kiểm tra dung lượng và kích thước từng tệp ảnh**
Chạy lệnh kiểm tra kích thước: Đảm bảo 100% tệp có kích thước 160x160 và dung lượng < 25KB.

- [ ] **Step 4: Commit bộ ảnh static**
```bash
git add frontend/public/avatars/
git commit -m "feat(frontend): add 16 curated high-quality student portrait WebP avatars"
```

---

### Task 2: Nâng Cấp Component `TutorAvatar.jsx` với Chân Dung WebP & Fallback Initials

**Files:**
- Modify: `frontend/src/components/TutorAvatar.jsx`

**Interfaces:**
- Consumes: `tutorId`, `fullName`, `size`, `className`
- Produces: JSX hiển thị `<img src="/avatars/{tutorId}.webp" alt="Gia sư {tutorId}" />` kèm `onError` fallback sang monogram chữ cái đầu / `boring-avatars`.

- [ ] **Step 1: Viết mã nâng cấp cho `TutorAvatar.jsx`**
Cập nhật logic:
1. Đường dẫn ảnh: `/avatars/${tutorId}.webp`
2. Thuộc tính `alt={`Gia sư ${tutorId}`}`
3. Xử lý sự kiện `onError`: nếu không tải được ảnh, chuyển sang fallback hiển thị Monogram Initials chữ cái lớn (ví dụ `G01`, `T06`, `020`) trên nền gradient màu sắc tương ứng hoặc `boring-avatars`.
4. Bổ sung `title={`Gia sư ${fullName || tutorId} (Ảnh minh họa hồ sơ)`}`.

- [ ] **Step 2: Kiểm tra Lint và Build**
Chạy: `npm run lint` và `npm run build` trong `frontend/`.
Xác minh: Build thành công 0 lỗi.

- [ ] **Step 3: Commit component TutorAvatar**
```bash
git add frontend/src/components/TutorAvatar.jsx
git commit -m "feat(frontend): update TutorAvatar to support portrait WebP with initial fallback"
```

---

### Task 3: Cập Nhật Layout Thẻ `TutorCard.jsx` & `App.css` (Rank Badge Đè Góc Ảnh)

**Files:**
- Modify: `frontend/src/components/TutorCard.jsx`
- Modify: `frontend/src/App.css`

**Interfaces:**
- Consumes: Cấu trúc thẻ gia sư trong `TutorCard.jsx`
- Produces: Huy hiệu thứ hạng (#1, #2, #3...) đè nổi ở góc trên ảnh đại diện (`position: absolute; top: -6px; left: -6px; z-index: 2`).

- [ ] **Step 1: Điều chỉnh CSS cho `.tutor-rank-group` và `.rank-mark` trong `App.css`**
Đặt `.tutor-avatar-wrap` trong wrapper `position: relative`, đưa `.rank-mark` lên vị trí đè góc ảnh đại diện với `position: absolute; top: -6px; left: -6px; z-index: 2; box-shadow: 0 2px 6px rgba(0,0,0,0.3)`.

- [ ] **Step 2: Tinh chỉnh khoảng cách tiêu đề tên gia sư**
Điều chỉnh margin/padding của `.tutor-identity` để tên gia sư, mã ID và các badge không bị che khuất bởi rank badge đè góc.

- [ ] **Step 3: Kiểm tra hiển thị qua Vite HMR**
Xác minh trên trình duyệt: Thẻ gia sư hiển thị avatar chân dung 160x160 sắc nét, góc trên có huy hiệu #1, #2, #3 đè nổi bật, viền bo tròn 12px tinh tế.

- [ ] **Step 4: Commit thay đổi CSS và Card**
```bash
git add frontend/src/components/TutorCard.jsx frontend/src/App.css
git commit -m "feat(frontend): overlay rank badge on avatar corner per UI design"
```

---

### Task 4: Nâng Cấp Skeleton Loading & Motion Spring Stagger Rõ Nét

**Files:**
- Modify: `frontend/src/App.jsx`
- Modify: `frontend/src/pages/ResultPage.jsx`
- Modify: `frontend/src/App.css`

**Interfaces:**
- Consumes: `isLoading` từ `App.jsx`, kết quả gợi ý `recommendationResult`
- Produces:
  1. Khi đang tính toán (sau khi click "Tìm gia sư" hoặc chọn kịch bản): Chuyển tab sang `ResultPage` hiển thị 3 thẻ Skeleton Pulse với animation ánh sáng quét nhẹ trong ~350ms.
  2. Khi kết quả sẵn sàng: 3 thẻ gia sư bay vào so le rõ rệt (`initial={{ opacity: 0, y: 32, scale: 0.96 }}`, `delay: index * 0.1s`, `stiffness: 240, damping: 20`).
  3. Thẻ Rank #1 có viền ánh sáng thở (subtle glowing border).

- [ ] **Step 1: Tích hợp Skeleton State vào `ResultPage.jsx`**
Cập nhật `ResultPage.jsx`: Nếu `isUpdatingPriorities` hoặc đang tính toán, hiển thị 3 thẻ Skeleton mô phỏng cấu trúc hồ sơ gia sư (avatar tròn, tên, biểu đồ stacked bar, tiêu chí).

- [ ] **Step 2: Nâng cấp Spring Stagger cho danh sách kết quả**
Tăng biên độ dịch chuyển lên `y: 32px`, kết hợp `scale: 0.96 -> 1` và spring physics rõ nét để người dùng cảm nhận rõ chuyển động.

- [ ] **Step 3: Kiểm tra chuyển step mượt mà từ `SearchPage` sang `ResultPage`**
Đảm bảo khi click kịch bản mẫu (KB01–KB14), trang không bị khựng mà chuyển tiếp mượt mà qua Skeleton rồi hiện Top-3 kết quả.

- [ ] **Step 4: Commit cải tiến Motion và Skeleton**
```bash
git add frontend/src/App.jsx frontend/src/pages/ResultPage.jsx frontend/src/App.css
git commit -m "feat(frontend): enhance skeleton loading feedback and pronounced spring stagger motion"
```

---

### Task 5: Kiểm Thử Nghiệm Thu Toàn Trình, Chụp Ảnh Demo & Deploy Vercel Production

**Files:**
- Test: Backend pytest suite (`190 passed`)
- Test: Playwright live test script
- Update: `BAO_CAO_TIEN_DO_GIUA_KY_DO_AN_KHMT1.docx`
- Deploy: Vercel Production (`https://tutor-recommender.vercel.app`)

- [ ] **Step 1: Chạy kiểm thử tự động Backend & Frontend**
Chạy:
`pytest -q` trong `backend/` $\rightarrow$ Đảm bảo **190 passed 100%**.
`npm run lint` & `npm run build` trong `frontend/` $\rightarrow$ Đảm bảo **0 warning, 0 error**.

- [ ] **Step 2: Dùng Playwright chụp lại trọn bộ 5 ảnh demo mới nhất**
Chụp màn hình:
1. `hinh-1-cn01-nhap-nhu-cau.png`: Form tìm kiếm và thanh kịch bản.
2. `hinh-2-cn02-ket-qua-top3.png`: Kết quả Top-3 với ảnh chân dung WebP và rank badge đè góc.
3. `hinh-3-cn03-dieu-chinh-uu-tien.png`: Bảng điều chỉnh CN03 và thẻ gia sư xếp hạng lại.
4. Cập nhật đè vào `docs/thesis/assets/midterm/` và file Word `BAO_CAO_TIEN_DO_GIUA_KY_DO_AN_KHMT1.docx`.

- [ ] **Step 3: Push commit lên PR #77 trên GitHub**
Push nhánh `feat/hybrid-modern-studio-ui` lên `origin`.

- [ ] **Step 4: Triển khai lên Vercel Production và nghiệm thu Playwright**
Chạy: `npx vercel deploy --prod` với biến môi trường API.
Dùng Playwright kiểm tra trực tiếp trên `https://tutor-recommender.vercel.app` để xác nhận ảnh chân dung, skeleton và motion hoạt động hoàn hảo.
