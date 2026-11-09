# Frontend - Giao diện người dùng gợi ý gia sư

Giao diện web dành cho người học để nhập các tiêu chí tìm kiếm và xem kết quả gia sư được gợi ý.

> **Trạng thái hiện tại:** Đã có màn hình nhập nhu cầu (CN01/CN03) và màn hình kết quả gợi ý (CN02) nối với API backend; giao diện dùng CSS thuần, không dùng TailwindCSS/Recharts.

## 1. Công nghệ dự kiến

- **Framework/Build tool:** ReactJS (Vite)
- **Ngôn ngữ:** JavaScript (JSX) - theo tên tệp `SearchPage.jsx`, `api.js` trong product backlog
- **Thư viện giao diện & biểu đồ:** CSS thuần; thanh xếp chồng (stacked bar) vẽ bằng HTML/CSS, không dùng TailwindCSS/Recharts

## 2. Các màn hình chính (theo Mục 3.8 và 4.5 của đề cương)

1. **Màn hình nhập nhu cầu:**
   - Chọn môn học (bắt buộc)
   - Chọn hình thức học (Trực tiếp, Trực tuyến, Không yêu cầu)
   - Chọn khu vực mong muốn (nếu học trực tiếp)
   - Nhập ngân sách tối đa theo giờ (VNĐ)
   - Chọn các khung giờ rảnh trong tuần (lưới ngày trong tuần × buổi)
   - Chọn **mục tiêu học tập** để hệ thống điền sẵn bộ mức ưu tiên cho 5 tiêu chí; người học vẫn chỉnh tay được, và khi chỉnh tay ô chọn chuyển thành "Tùy chỉnh"
   - Chọn mức ưu tiên cho từng tiêu chí (Bỏ qua, Thấp, Trung bình, Cao)

   > **Phạm vi:** ô chọn **Cấp lớp CHƯA hiện thực** vì hồ sơ gia sư trong `data/processed/tutors.json` không có trường cấp lớp; một ô chọn không tác dụng sẽ làm người dùng hiểu sai. Bộ mức ưu tiên điền sẵn chỉ là gợi ý khởi tạo do nhóm đặt, chưa kiểm chứng với người dùng, và không thêm trường nào vào payload gửi API.

2. **Màn hình kết quả gợi ý:**
   - Danh sách Top-k gia sư phù hợp nhất kèm điểm tổng hợp
   - Điểm thành phần từng tiêu chí
   - Biểu đồ thể hiện mức độ đóng góp của từng tiêu chí vào điểm số tổng
   - Khả năng tinh chỉnh nhanh mức ưu tiên để quan sát thứ hạng thay đổi trực tiếp (Mục 3.7.1)

## 3. Cấu trúc thư mục `src` dự kiến

```text
src/
├── components/   # Các thành phần UI dùng lại (Header, PrioritySelector, TutorCard...)
├── pages/        # Các màn hình chính (SearchPage, ResultPage)
├── services/     # Tầng gọi API kết nối đến Backend FastAPI
└── types/        # Định nghĩa kiểu dữ liệu (Tutor, SearchRequest, RecommendationResult)
```

> Ghi chú Sprint 1: đã tạo `src/components/`, `src/pages/`, `src/services/` (có `.gitkeep`); `src/types/` chưa tạo vì dự án dùng JavaScript.

## 4. Cài đặt và chạy

Yêu cầu Node.js 20.19+ (đã kiểm tra với Node 24.19.0) và npm. Đứng tại thư mục `frontend/`:

```powershell
npm install
npm run build
npm run dev
```

- `npm run build` đóng gói production vào `frontend/dist/` (đã nằm trong `.gitignore`).
- `npm run dev` mở dev server tại địa chỉ mặc định `http://localhost:5173`.
- `npm run lint` dùng `oxlint` đi kèm template Vite; chưa đấu nối vào CI ở Sprint 1.
