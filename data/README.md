# Dữ liệu hệ thống gợi ý gia sư

Thư mục quản lý tập dữ liệu phục vụ phát triển, thử nghiệm và đánh giá thuật toán gợi ý.

## 1. Cấu trúc thư mục

- `raw/`: Chứa dữ liệu gốc thu thập từ các nguồn công khai hoặc kịch bản giả lập thô.
- `processed/`: Chứa tập dữ liệu mẫu đã được làm sạch, chuẩn hóa và gán nhãn, sẵn sàng nạp vào hệ thống để demo và kiểm thử.

## 2. Quy ước nhãn và tính ẩn danh (theo Mục 3.5 của đề cương)

- **Ẩn danh hóa thông tin:** Tất cả hồ sơ gia sư được định danh duy nhất bằng mã gia sư (ví dụ: `GS001`, `GS002`...). Tuyệt đối không lưu trữ họ tên, số điện thoại, địa chỉ nhà, tài khoản mạng xã hội hay bất kỳ thông tin liên hệ cá nhân nào.
- **Gán nhãn nguồn dữ liệu (`data_source`):**
  - `Thu thập công khai` (`public_collected`): Dữ liệu thu thập từ các bài đăng tìm gia sư hoặc website gia sư công khai.
  - `Giả lập` (`simulated`): Dữ liệu được nhóm tự tạo ra để kiểm thử các ca biên, ca xung đột tiêu chí hoặc ca thiếu dữ liệu.
  - `Ước tính` (`estimated`): Dữ liệu được bổ sung hoặc ước lượng phục vụ mục đích kiểm chứng.
