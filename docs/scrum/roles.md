> [!NOTE]
> **Đề xuất, nhóm xác nhận**

# Cơ cấu vai trò Scrum (Scrum Roles)

Tài liệu định nghĩa vai trò, trách nhiệm và nguyên tắc phối hợp của các thành viên trong nhóm đồ án **"Hệ thống khuyến nghị gia sư dựa trên mức độ phù hợp đa tiêu chí"**.

---

## 1. Phân bổ vai trò trong nhóm

| Thành viên | Mã sinh viên | Vai trò Scrum chính | Trách nhiệm trọng tâm |
|:---|:---:|:---|:---|
| **Cao Khánh Ngọc** | KHMT2411025 | **Product Owner (PO)**<br/>*Kiêm Developer* | - Đại diện yêu cầu đề tài, làm việc trực tiếp với Giảng viên hướng dẫn (TS. Lê Anh Nhã Uyên).<br/>- Quản lý và làm mịn Product Backlog, ưu tiên hóa các User Stories.<br/>- Nghiệm thu sản phẩm cuối mỗi Sprint dựa trên Definition of Done.<br/>- Tham gia phát triển phần tài liệu, thiết kế dữ liệu và kiểm thử hệ thống. |
| **Trần Nguyễn Đức** | KHMT2411011 | **Scrum Master (SM)**<br/>*(Sprint 1, 3, 5)*<br/>*Kiêm Developer* | - Điều phối các nghi thức Scrum trong các sprint lẻ (Planning, Daily, Review, Retro).<br/>- Tháo gỡ các trở ngại kỹ thuật và theo dõi tiến độ nhánh làm việc trên GitHub.<br/>- Trực tiếp phát triển lõi chấm điểm backend FastAPI, thuật toán xếp hạng và kiểm thử tự động. |
| **Lê Thị Bích Chuyền** | KHMT2411037 | **Scrum Master (SM)**<br/>*(Sprint 2, 4, 6)*<br/>*Kiêm Developer* | - Điều phối các nghi thức Scrum trong các sprint chẵn (Planning, Daily, Review, Retro).<br/>- Đảm bảo tuân thủ thỏa thuận làm việc và cập nhật tài liệu sprint.<br/>- Trực tiếp phát triển giao diện ReactJS Vite, kết nối API và kiểm thử trải nghiệm người dùng. |

---

## 2. Cơ chế luân phiên Scrum Master

- Vai trò **Scrum Master được luân phiên theo Sprint** giữa hai thành viên Trần Nguyễn Đức và Lê Thị Bích Chuyền:
  - **Sprint 1, 3, 5:** Trần Nguyễn Đức đảm nhiệm vai trò Scrum Master.
  - **Sprint 2, 4, 6:** Lê Thị Bích Chuyền đảm nhiệm vai trò Scrum Master.
- **Mục đích:** Giúp các thành viên đều có trải nghiệm điều phối dự án thực tế, đồng thời san sẻ áp lực quản lý quy trình để tập trung lập trình.

---

## 3. Nguyên tắc kỷ luật bắt buộc

1. **Tách biệt vai trò PO và SM:** Product Owner (Cao Khánh Ngọc) tuyệt đối không kiêm nhiệm Scrum Master trong bất kỳ sprint nào để duy trì tính khách quan giữa việc định hướng yêu cầu (PO) và hỗ trợ quy trình (SM).
2. **Không tự duyệt Pull Request:** Tuyệt đối không thành viên nào được tự merge hoặc tự phê duyệt (Approve) Pull Request do chính mình tạo ra trên GitHub.
3. **Review chéo bắt buộc:** Mỗi Pull Request bắt buộc phải được ít nhất một thành viên khác trong nhóm kiểm tra mã nguồn, xác nhận CI pass và chính thức Approve trên GitHub trước khi thực hiện squash merge vào nhánh `main`.
