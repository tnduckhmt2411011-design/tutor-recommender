# Frontend - Giao diện người dùng gợi ý gia sư (React 19 + Vite)

Ứng dụng web Single Page Application cho phép người học nhập nhu cầu, chọn mức ưu tiên, xem kết quả Top-k gia sư kèm biểu đồ thanh xếp chồng điểm đóng góp và ghi chú giải thích.

## 1. Công nghệ sử dụng

- **Thư viện giao diện chính:** React 19 (`react` ^19.3.1, `react-dom` ^19.3.1)
- **Công cụ đóng gói & Máy chủ phát triển:** Vite 8 (`vite` ^8.3.5, `@vitejs/plugin-react` ^6.1.2)
- **Hiệu ứng & Avatar:** `motion` ^14.9.0 (hoạt họa chuyển cảnh), `boring-avatars` ^2.0.4 (tạo avatar tất định cho gia sư)
- **Kiểm tra mã nguồn (Linter):** `oxlint` ^1.89.0
- **Ngôn ngữ:** JavaScript (JSX)
- **Định kiểu (Styling):** CSS thuần (`App.css`, `index.css`). Hệ thống **hoàn toàn không sử dụng TailwindCSS hay Recharts**; biểu đồ thanh xếp chồng phân rã điểm đóng góp (Stacked Bar Score) được tự dựng hoàn toàn bằng HTML và CSS thuần trong component `StackedBarScore.jsx`.

## 2. Cấu trúc thư mục `src/` thực tế

```text
frontend/src/
├── assets/                  # Hình ảnh và biểu tượng tĩnh (hero.png, react.svg, vite.svg)
├── components/              # Các thành phần giao diện tái sử dụng
│   ├── CriteriaIcon.jsx     # Biểu tượng đại diện cho từng tiêu chí ưu tiên
│   ├── SkeletonLoader.jsx   # Khung tải trang (skeleton loader) khi chờ kết quả API
│   ├── StackedBarScore.jsx  # Biểu đồ thanh xếp chồng phân rã tỷ lệ đóng góp của từng tiêu chí
│   ├── SubjectIcon.jsx      # Biểu tượng đại diện các môn học
│   ├── TutorAvatar.jsx      # Hiển thị avatar đại diện gia sư
│   └── TutorCard.jsx        # Thẻ thông tin chi tiết gia sư, điểm tổng, lý do và biểu đồ
├── data/                    # Dữ liệu tĩnh và cấu hình nạp sẵn
│   ├── goalPresets.js       # Danh mục 3 preset mục tiêu học tập (US-41)
│   ├── scenariosCatalog.js  # Danh mục 14 kịch bản thực nghiệm nạp nhanh
│   └── tutorsCatalog.js     # Bản sao dữ liệu 16 hồ sơ gia sư phục vụ hiển thị
├── pages/                   # Các màn hình nghiệp vụ chính
│   ├── SearchPage.jsx       # Màn hình nhập nhu cầu học tập (CN01)
│   └── ResultPage.jsx       # Màn hình kết quả Top-k và tinh chỉnh mức ưu tiên (CN02, CN03)
├── services/                # Tầng kết nối mạng
│   └── api.js               # Cấu hình endpoint, chuẩn hóa payload và gọi API backend
├── App.css                  # Định kiểu phong cách giao diện và hiệu ứng tương tác
├── App.jsx                  # Component gốc điều phối trạng thái và chuyển trang
├── index.css                # Reset CSS và thiết lập phông chữ toàn cục
└── main.jsx                 # Điểm khởi chạy ứng dụng React với Vite
```

*(Lưu ý: Dự án sử dụng JavaScript thuần, không có thư mục `src/types/`).*

## 3. Các tính năng và màn hình nghiệp vụ

### 3.1. Màn hình nhập nhu cầu học tập (CN01 - `SearchPage.jsx`)
- **Chọn môn học:** Trường bắt buộc (Toán, Lý, Hóa, Sinh, Văn, Anh Văn, Anh Văn GT, Tin học, Tiếng Nhật, Tiếng Trung).
- **Chọn hình thức học:** Trực tiếp (`in_person`), Trực tuyến (`online`), hoặc Không yêu cầu (`any`).
- **Chọn khu vực mong muốn:** Hiển thị khi chọn hình thức Trực tiếp, hỗ trợ danh mục 16 quận/huyện quy ước.
- **Nhập ngân sách tối đa theo giờ:** Đơn vị VNĐ/giờ (tùy chọn).
- **Chọn lưới khung giờ rảnh:** Bảng ma trận 7 ngày trong tuần $\times$ 3 buổi (Sáng, Chiều, Tối).
- **Tính năng mở rộng - Mục tiêu học tập (US-41):** Hộp chọn với 3 preset định sẵn gợi ý bộ mức ưu tiên ban đầu:
  1. *Mặc định:* Tất cả 5 tiêu chí ở mức Trung bình ($w=2$).
  2. *Luyện thi điểm cao / học chuyên:* Ưu tiên Kinh nghiệm và Đánh giá ở mức Cao ($w=3$).
  3. *Đậu tốt nghiệp / lấy lại căn bản:* Ưu tiên Học phí ở mức Cao ($w=3$).
  *(Khi người học chỉnh tay bất kỳ tiêu chí nào, ô chọn chuyển sang trạng thái "Tùy chỉnh").*
- **Chọn mức ưu tiên từng tiêu chí:** 4 mức rõ ràng gồm Bỏ qua ($w=0$), Thấp ($w=1$), Trung bình ($w=2$), Cao ($w=3$).
- **Thanh nạp nhanh 14 kịch bản thực nghiệm:** Nạp sẵn các tham số kiểm thử từ KB01 đến KB14 để kiểm chứng nhanh hệ thống.

> **Phạm vi kỹ thuật:** Ô chọn **Cấp lớp CHƯA hiện thực** do cơ sở dữ liệu hồ sơ gia sư hiện tại không có dữ liệu tương ứng; đề xuất mở rộng này hiện chưa có phản hồi chính thức của GVHD.

### 3.2. Màn hình kết quả gợi ý & Tinh chỉnh ưu tiên (CN02 & CN03 - `ResultPage.jsx`)
- **Danh sách gợi ý Top-k:** Hiển thị thẻ gia sư kèm thứ hạng (Top 1, 2, 3), điểm tổng hợp $S \in [0, 1]$, mức học phí, số năm kinh nghiệm, hình thức dạy và điểm đánh giá.
- **Biểu đồ thanh xếp chồng (Stacked Bar):** Trực quan hóa phần trăm đóng góp của từng tiêu chí vào điểm tổng: $\frac{w_i \cdot s_i}{\sum w_i}$.
- **Ghi chú giải thích:** Hiển thị lý do gợi ý nổi bật và cảnh báo khi điểm đánh giá sử dụng giá trị trung tính $0,5$.
- **Điều chỉnh ưu tiên trực tiếp (CN03):** Cho phép người học thay đổi mức ưu tiên ngay tại thanh điều khiển trên màn hình kết quả để quan sát danh sách xếp hạng tính toán lại tức thì.
- **Nút "Thử $\sum w_i = 0$":** Đưa tất cả tiêu chí về mức 0 để kiểm tra trạng thái biên (`zero_weight`), hiển thị giao diện hướng dẫn người dùng bật lại ít nhất một tiêu chí.

## 4. Cơ chế chọn URL API Backend (`src/services/api.js`)

Logic xác định URL backend diễn ra tự động và an toàn theo độ ưu tiên:
1. **Biến môi trường:** Nếu có khai báo `VITE_API_URL` (hoặc `VITE_API_BASE_URL`) trong tệp `.env`, hệ thống sử dụng địa chỉ này.
2. **Tự động theo hostname:**
   - Khi chạy trên trình duyệt có hostname là `localhost` hoặc `127.0.0.1`: Mặc định kết nối tới Backend cục bộ tại `http://localhost:8000`.
   - Khi chạy trên domain khác (ví dụ triển khai trên Vercel tại `tutor-recommender.vercel.app`): Mặc định kết nối tới Backend đám mây tại `https://tutor-recommender-api.onrender.com`.

## 5. Cài đặt và khởi chạy

Yêu cầu môi trường: Node.js tương thích `^20.19.0 || >=22.12.0` (đã kiểm chứng với Node.js v24.19.0 và npm 11.17.0). Đứng tại thư mục `frontend/`:

### Cài đặt dependencies:
```powershell
npm ci
```

### Kiểm tra tĩnh mã nguồn (Linter):
```powershell
npm run lint
```
*(Sử dụng `oxlint` quét toàn bộ mã nguồn JavaScript/JSX).*

### Đóng gói ứng dụng (Production Build):
```powershell
npm run build
```
*(Đóng gói mã nguồn production vào thư mục `frontend/dist/`).*

### Khởi chạy máy chủ phát triển (Vite Dev Server):
```powershell
npm run dev
```
- Ứng dụng sẵn sàng tại: `http://localhost:5173`
- *Ghi chú về kiểm thử:* Frontend hiện không có khung kiểm thử tự động (unit test / component test); toàn bộ logic gợi ý và kịch bản nghiệp vụ được kiểm thử tự động 100% ở phía Backend (200 test passed).
