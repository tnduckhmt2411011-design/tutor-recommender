# Quy ước đóng góp và làm việc nhóm

Tài liệu này quy định quy trình làm việc trên repository cho các thành viên trong nhóm đồ án.

## 1. Nguyên tắc làm việc trên nhánh

- Nhánh `main` là nhánh ổn định, chỉ nhận thay đổi thông qua Pull Request (PR), không commit trực tiếp.
- Quy ước đặt tên nhánh công việc:
  - `feat/<số-issue>-<tên-ngắn>`: Phát triển tính năng mới.
  - `fix/<số-issue>-<tên-ngắn>`: Sửa lỗi hoặc điều chỉnh hành vi sai.
  - `docs/<số-issue>-<tên-ngắn>`: Cập nhật tài liệu thiết kế, đồ án hoặc scrum.
  - `test/<số-issue>-<tên-ngắn>`: Bổ sung ca kiểm thử, kịch bản dữ liệu.
  - `chore/<số-issue>-<tên-ngắn>`: Cấu hình môi trường, dependencies, tooling.

## 2. Quy ước thông điệp commit

- Mỗi commit có tiền tố tương ứng (`feat`, `fix`, `docs`, `test`, `chore`).
- Nội dung viết bằng tiếng Việt có dấu, gói gọn trong một dòng ngắn tự nhiên, không dùng văn mẫu hay sáo rỗng.
- Ví dụ:
  - `feat: thêm hàm tính điểm tiêu chí học phí`
  - `fix: xử lý trường hợp chia cho 0 khi tổng trọng số bằng không`
  - `docs: cập nhật công thức bảng 3.6 vào scoring-spec`
  - `test: bổ sung ca biên khi học phí vượt 50 phần trăm ngân sách`
  - `chore: khởi tạo cấu trúc repo`

## 3. Quy trình Pull Request và Review

- Mỗi PR phải được liên kết với ít nhất một Issue liên quan.
- Mỗi PR bắt buộc phải được ít nhất một thành viên khác trong nhóm xem xét (review) và phê duyệt trước khi merge.
- Phương thức hợp nhất: Chỉ sử dụng **Squash and merge** để giữ lịch sử commit trên nhánh `main` gọn gàng.
- Nhánh tính năng sẽ tự động được xóa sau khi merge thành công.
