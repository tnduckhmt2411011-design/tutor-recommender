> [!NOTE]
> **Đề xuất, nhóm xác nhận**

# Tiêu chuẩn sẵn sàng (Definition of Ready - DoR)

Tài liệu quy định các tiêu chí chất lượng bắt buộc mà một hạng mục công việc (User Story) phải thỏa mãn trước khi được Product Owner và nhóm phát triển chấp thuận đưa vào kế hoạch của bất kỳ Sprint nào.

---

## 4 Tiêu chuẩn sẵn sàng bắt buộc

Một User Story chỉ được xem là **Sẵn sàng (Ready)** khi đáp ứng đồng thời 4 điều kiện sau:

1. **Tiêu chí chấp nhận rõ ràng và kiểm tra được (Testable Acceptance Criteria):**
   - Story phải có danh sách tiêu chí nghiệm thu cụ thể, đo lường được bằng kết quả thực tế (ví dụ: "chạy qua 15 ca test từ Bảng 3.6", "thời gian phản hồi dưới 1 giây").
   - Tuyệt đối không sử dụng các từ ngữ định tính, mơ hồ như "hoạt động tốt", "chạy ổn định", "giao diện đẹp".
2. **Ước lượng độ lớn khả thi (Sized & Estimable):**
   - Story đã được nhóm thảo luận và thống nhất gắn điểm Story Points theo dãy số Fibonacci: 1, 2, 3, 5, 8.
   - **Ràng buộc:** Điểm ước lượng không được vượt quá 8 SP. Nếu một story lớn hơn 8 SP, bắt buộc phải phân rã thành các story nhỏ hơn trước khi đưa vào Sprint Planning.
3. **Nguồn gốc đề cương minh bạch (Traceable to Thesis Outline):**
   - Mọi story phải dẫn xuất trực tiếp từ một mục, bảng biểu cụ thể trong Đề cương đồ án hoặc yêu cầu của GVHD (ví dụ: Mục 3.6, Mục 4.4, Bảng 3.2, Bảng 5.1, CN01...).
   - Không tự ý đưa vào backlog các tính năng nằm ngoài phạm vi đề tài đã được duyệt.
4. **Không bị chặn bởi phụ thuộc kỹ thuật (No Blocking Dependencies):**
   - Các điều kiện tiên quyết về mặt thiết kế, công thức toán học hoặc interface kỹ thuật liên quan đã được giải quyết hoặc hoàn tất ở các sprint trước.
   - Story sẵn sàng để lập trình viên bắt tay vào làm ngay mà không phải chờ đợi quyết định kỹ thuật chưa rõ ràng.
