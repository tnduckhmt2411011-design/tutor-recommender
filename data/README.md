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

## 3. Ghi chú về hai hồ sơ thu thập công khai (Phụ lục A)

- Tập dữ liệu chuẩn hóa gồm **16 hồ sơ**: `processed/tutors.json` và `processed/tutors.csv`, đúng theo Bảng 3.3 (bản cuối) trong Phụ lục A của đề cương.
- **Học phí và lịch rảnh của GS-T06, GS-T07 là ước tính của nhóm** (ký hiệu `(*)` ở Phụ lục A), không phải số liệu thu thập trực tiếp. Học phí được nội suy theo số năm kinh nghiệm từ khoảng giá quan sát được khi khảo sát thị trường tại daythem.com (130.000–400.000 VNĐ/giờ); lịch rảnh là giả định chung dựa trên các khung giờ phổ biến, không suy ra từ nguồn cụ thể nào.
- Môn dạy, khu vực và số năm kinh nghiệm của GS-T06, GS-T07 là số liệu thu thập thật. Điểm đánh giá trung bình của hai hồ sơ này để trống và dùng giá trị trung tính 0,5 khi tính điểm.
- Theo đúng Phụ lục A, `data_source` của GS-T06 và GS-T07 vẫn ghi `public_collected`; nhãn `estimated` trong quy ước ở mục 2 chưa được dùng cho hai hồ sơ này. Điểm lệch này đang chờ nhóm quyết định.
