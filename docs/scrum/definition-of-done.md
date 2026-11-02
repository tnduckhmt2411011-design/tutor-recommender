# Định nghĩa hoàn thành (Definition of Done - DoD)

Một User Story, Task hoặc Pull Request chỉ được coi là hoàn thành (Done) khi thỏa mãn đầy đủ các tiêu chí sau:

1. **Kiểm tra mã nguồn:** Đã được người phụ trách GitHub kiểm tra qua Pull Request; thay đổi về công thức, API contract và dữ liệu đã được Product Owner xác nhận.
2. **Kiểm thử tự động:** Tất cả các bài kiểm thử liên quan chạy qua thành công; mọi thay đổi ở module tính điểm (`scoring`) phải có ca kiểm thử lấy từ ví dụ Bảng 3.6 hoặc ca biên (mục 5.1).
3. **Đồng bộ tài liệu & đề cương:** Đã cập nhật tài liệu trong thư mục `docs/design` nếu thay đổi công thức, trường dữ liệu hoặc API, đồng thời ghi rõ tác động lên đề cương đồ án trong phần mô tả của PR.
4. **An toàn dữ liệu:** Dữ liệu mẫu thêm vào hệ thống phải có gắn nhãn nguồn dữ liệu (`data_source`), được ẩn danh hoàn toàn bằng mã gia sư, không chứa họ tên hay thông tin liên hệ cá nhân.
5. **Tính trung thực trong đánh giá:** Tuyệt đối không được chỉnh sửa kết quả Top-3 kỳ vọng trong kịch bản kiểm thử để làm khớp với kết quả thực tế của hệ thống.
