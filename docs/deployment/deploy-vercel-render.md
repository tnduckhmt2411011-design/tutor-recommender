# Cẩm nang Triển khai Hệ thống Lên Cloud (Vercel + Render)

Tài liệu này hướng dẫn chi tiết từng bước đưa hệ thống **Khuyến nghị Gia sư Đa tiêu chí (Tutor Recommender)** lên môi trường Cloud công cộng để phục vụ chấm điểm đồ án, gửi link cho GVHD (TS. Lê Anh Nhã Uyên) và trình chiếu demo bảo vệ.

Toàn bộ quá trình sử dụng các gói **Free Tier trọn đời ($0)** của Render và Vercel.


> [!IMPORTANT]
> **Hệ thống đã được triển khai trực tiếp và đang hoạt động 24/7:**
> - **Ứng dụng Web trực tuyến (Frontend Live):** https://tutor-recommender.vercel.app *(Hoặc alias: https://frontend-ochre-six-11.vercel.app)*
> - **Máy chủ API Backend (FastAPI Live):** https://tutor-recommender-api.onrender.com
> - **Tài liệu API tương tác (Swagger UI):** https://tutor-recommender-api.onrender.com/docs
> - **Kiểm tra trạng thái máy chủ (Health Check):** https://tutor-recommender-api.onrender.com/health

---

## 1. Kiến trúc Triển khai (Deployment Architecture)

```
┌───────────────────────────────────────┐
│     Người dùng / GVHD / Hội đồng      │
│ (Trình duyệt máy tính hoặc điện thoại)│
└──────────────────┬────────────────────┘
                   │ HTTPS
                   ▼
┌────────────────────────────────────────────────────────┐
│              FRONTEND (Vercel Edge Network)            │
│  • Domain: https://tutor-recommender.vercel.app        │
│  • Công nghệ: React 19 + Vite 8 SPA                    │
│  • Biến môi trường: VITE_API_URL = <Backend Render URL>│
└──────────────────┬─────────────────────────────────────┘
                   │ REST API (HTTPS)
                   ▼
┌────────────────────────────────────────────────────────┐
│             BACKEND (Render.com Web Service)           │
│  • Domain: https://tutor-recommender-api.onrender.com  │
│  • Công nghệ: FastAPI (Python 3.12) + Uvicorn          │
│  • Dữ liệu: 16 hồ sơ gia sư in-memory (tutors.json)    │
│  • CORS: allow_origins=["*"] mở an toàn cho Frontend   │
└────────────────────────────────────────────────────────┘
```

---

## 2. Phần A: Triển khai Backend FastAPI lên Render.com (Làm trước)

Backend cần được triển khai trước để lấy URL API cấp cho Frontend.

### Bước A1: Đăng ký / Đăng nhập Render.com
1. Truy cập [https://render.com/](https://render.com/).
2. Chọn **Sign in with GitHub** để tự động liên kết với tài khoản GitHub của bạn.

### Bước A2: Tạo Web Service mới
1. Tại Render Dashboard, bấm nút **New +** ở góc trên cùng bên phải $\rightarrow$ Chọn **Web Service**.
2. Chọn tùy chọn **Build and deploy from a Git repository**.
3. Chọn kho mã nguồn: `tnduckhmt2411011-design/tutor-recommender` (hoặc repository fork của bạn).
4. Điền các thông số cấu hình như sau:

| Trường cấu hình | Giá trị thiết lập | Ghi chú |
| :--- | :--- | :--- |
| **Name** | `tutor-recommender-api` *(hoặc tên tùy chọn)* | Tạo domain dạng `tutor-recommender-api.onrender.com` |
| **Region** | `Singapore (Southeast Asia)` | Vùng địa lý gần Việt Nam nhất, độ trễ thấp |
| **Branch** | `main` *(hoặc nhánh PR đang chạy)* | Nhánh mã nguồn cần deploy |
| **Root Directory** | `backend` | **Bắt buộc:** để Render trỏ đúng vào thư mục backend |
| **Runtime** | `Python 3` | Môi trường Python |
| **Build Command** | `pip install -r requirements.txt` | Cài đặt FastAPI, Uvicorn, Pydantic |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` | Khởi chạy máy chủ FastAPI trên cổng động |
| **Instance Type** | `Free` (0.1 CPU, 512 MB RAM) | Hoàn toàn miễn phí trọn đời |

> [!TIP]
> **Tùy chọn nâng cao (Render Blueprint):** Repository đã có sẵn tệp cấu hình [render.yaml](file:///render.yaml). Bạn cũng có thể chọn **New + $\rightarrow$ Blueprint** và chọn repo để Render tự động điền toàn bộ cấu hình trên mà không cần nhập thủ công.

### Bước A3: Khởi chạy và lấy URL Backend
1. Bấm nút **Create Web Service** (hoặc **Apply Blueprint**).
2. Chờ 1–2 phút để Render tiến hành build và khởi động. Khi thấy dòng chữ log `Application startup complete.` và trạng thái chuyển sang **Live**, copy đường dẫn URL ở phía trên (Ví dụ: `https://tutor-recommender-api.onrender.com`).
3. **Kiểm tra sức khỏe (Health Check):** Mở trình duyệt vào `https://tutor-recommender-api.onrender.com/health`, nếu thấy `{"status": "ok"}` và vào `/docs` thấy giao diện Swagger UI là backend đã hoạt động 100%!

---

## 3. Phần B: Triển khai Frontend React lên Vercel (Làm sau)

### Bước B1: Đăng ký / Đăng nhập Vercel
1. Truy cập [https://vercel.com/](https://vercel.com/).
2. Chọn **Continue with GitHub**.

### Bước B2: Import Project
1. Tại Vercel Dashboard, bấm **Add New... $\rightarrow$ Project**.
2. Tìm repository `tutor-recommender` và bấm **Import**.
3. Cấu hình các mục triển khai:

| Mục cấu hình | Giá trị thiết lập | Ghi chú |
| :--- | :--- | :--- |
| **Project Name** | `tutor-recommender` *(hoặc tên nhóm thích)* | Sẽ tạo domain `https://tutor-recommender.vercel.app` |
| **Framework Preset** | `Vite` | Vercel tự động nhận diện Vite |
| **Root Directory** | Bấm **Edit** $\rightarrow$ chọn thư mục `frontend` | **Bắt buộc:** để Vercel build đúng frontend |
| **Build Command** | `npm run build` *(Mặc định)* | Biên dịch React sang thư mục `dist` |
| **Output Directory**| `dist` *(Mặc định)* | Vercel tự động nhận diện |

### Bước B3: Cấu hình biến môi trường (Environment Variables)
1. Mở rộng mục **Environment Variables**.
2. Thêm biến kết nối Backend:
   * **Key:** `VITE_API_URL`
   * **Value:** URL của Render đã lấy ở Phần A (Ví dụ: `https://tutor-recommender-api.onrender.com` — *Lưu ý không có dấu `/` ở cuối*).
3. Bấm nút **Add**.

### Bước B4: Deploy
1. Bấm nút **Deploy**.
2. Chờ khoảng 30–45 giây để Vercel build. Khi hoàn thành, pháo hoa sẽ xuất hiện kèm đường link chính thức:  
   👉 `https://tutor-recommender.vercel.app`

---

## 4. Phần C: Nghiệm thu Toàn trình & Xử lý Cold Start

1. **Thử nghiệm Kịch bản KB01:** Mở link Vercel, chọn chip **KB01** $\rightarrow$ Kiểm tra Top-3 gợi ý có hiển thị đầy đủ và biểu đồ phân rã $C_i$ có sáng đèn khi rê chuột hay không.
2. **Thử nghiệm Điều chỉnh Ưu tiên (CN03):** Thay đổi các mức ưu tiên trên rail bên trái $\rightarrow$ Kiểm tra thứ hạng và điểm số có cập nhật tức thì dưới 1 giây hay không.
3. **Lưu ý về Hiện tượng "Cold Start" (Khởi động nguội) trên Render Free Tier:**
   * Gói miễn phí của Render sẽ tạm đưa backend về trạng thái ngủ nếu sau 15 phút không có ai truy cập.
   * Khi bạn (hoặc cô giáo) truy cập lần đầu sau thời gian nghỉ, request đầu tiên sẽ mất khoảng **30–40 giây** để Render đánh thức server dậy.
   * **Mẹo khi đi báo cáo / demo:** Trước buổi báo cáo khoảng 5 phút, hãy mở sẵn link web và bấm thử một kịch bản bất kỳ để server Render "thức giấc" sẵn sàng, khi cô giáo thao tác sẽ có phản hồi siêu tốc (< 200ms).

---

## 5. Phần D: Cập nhật vào Báo cáo & Hồ sơ Đồ án

Sau khi có 2 link hoạt động, nhóm bổ sung vào Báo cáo giữa kỳ / Báo cáo đồ án:

```markdown
- **Đường dẫn ứng dụng trực tuyến (Demo Link):** https://tutor-recommender.vercel.app
- **Tài liệu API tương tác (Swagger UI):** https://tutor-recommender-api.onrender.com/docs
- **Mã nguồn dự án (GitHub):** https://github.com/tnduckhmt2411011-design/tutor-recommender
```
