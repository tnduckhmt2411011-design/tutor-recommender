> [!NOTE]
> **Đề xuất, nhóm xác nhận**

# Tổng hợp tài liệu tham khảo GS360 [3] và bổ sung Mục 1.3 (Sprint 1 — US-31)

Tài liệu này lưu trữ nội dung nghiên cứu tài liệu tham khảo `[3]` (đồ án GS360) và đoạn văn cập nhật vào **Mục 1.3.2** cùng **Danh mục tài liệu tham khảo** của đề cương đồ án *(trích từ bản dự thảo `ĐỀ CƯƠNG HỆ THỐNG KHUYẾN NGHỊ_DU-THAO_v3.docx`)*.

---

## 1. Tóm tắt luận điểm và phạm vi của đồ án GS360 [3]

- **Thông tin tài liệu [3]:** Lê Thị Hoài Thương, Lê Nguyễn Quang Minh, *"GS360 - Xây dựng website hỗ trợ tìm kiếm gia sư"*, Đồ án cơ sở, Trường Đại học Công nghệ thông tin và Truyền thông Việt - Hàn (VKU), tháng 11/2024. *(Ghi chú: trong mô tả ban đầu của Issue #9 từng ghi tạm là ĐH FPT 2023; thông tin chuẩn theo tệp tài liệu gốc `[3]` trong đề cương là ĐH CNTT&TT Việt - Hàn, 2024).*
- **Phạm vi hệ thống GS360:**
  - Xây dựng một website hỗ trợ tìm kiếm và kết nối gia sư hoàn chỉnh theo quy trình nghiệp vụ hai vai trò (Gia sư — Phụ huynh/Học viên) và Quản trị viên (Mục 2.2.2, tr.13–14).
  - Các nhóm chức năng chính (Use case 2.2.6.1–2.2.6.19, tr.30–44; giao diện Mục 3.4, tr.60–69): đăng ký/đăng nhập, quản lý hồ sơ và suất dạy của gia sư, đăng bài tìm gia sư của phụ huynh, đặt lịch, thanh toán và hoàn tiền, đánh giá gia sư, hỏi đáp và thống kê doanh thu.
- **Cơ chế tìm kiếm trong GS360:**
  - Mục 2.1 (tr.11) mô tả GS360 cho phép tìm gia sư thông qua từ khóa tên môn học, cấp học và địa điểm.
  - Giao diện “Tìm gia sư” ở Mục 3.4.6 (tr.64) là biểu mẫu đăng bài tìm gia sư, sau đó bài đăng được hiển thị ở trang suất dạy.
  - Toàn văn báo cáo GS360 không mô tả cơ chế xếp hạng tổng hợp nhiều tiêu chí có trọng số, không tính điểm thành phần và không sinh lý do gợi ý (không xuất hiện các cụm “xếp hạng”, “trọng số”, “thuật toán”).

---

## 2. Bảng đối chiếu GS360 [3] và đề tài của nhóm

| Tiêu chí đối chiếu | Đồ án cơ sở GS360 [3] | Đề tài của nhóm (`tutor-recommender`) |
|:---|:---|:---|
| **Trọng tâm đề tài** | Website quản lý và kết nối gia sư đầu-cuối (đăng ký, đăng bài, nhận lớp, thanh toán, hoàn tiền, thống kê). | Bộ máy khuyến nghị (recommendation engine) đa tiêu chí có giải thích kèm giao diện demo tối giản. |
| **Cơ chế tìm kiếm & lọc** | Tìm theo từ khóa môn học, cấp học, địa điểm hoặc đăng bài tìm gia sư lên danh sách suất dạy. | Lọc điều kiện bắt buộc 3 ràng buộc cứng (Môn học, Hình thức học, Giao khung giờ rảnh $\lvert L \cap T \rvert \ge 1$ — Bảng 3.2). |
| **Cơ chế chấm điểm & xếp hạng** | Không có công thức chấm điểm thành phần hay tổng hợp trọng số đa tiêu chí. | Chuẩn hóa 5 hàm điểm thành phần $s_i \in [0, 1]$ (Bảng 3.6), kiểm tra ngưỡng dữ liệu tối thiểu và gộp bằng Weighted Scoring theo 4 mức ưu tiên (Bảng 3.5). |
| **Khả năng giải thích (Explainability)** | Không hiển thị điểm phù hợp hoặc đóng góp tiêu chí. | Trả về Top-$k$ kèm điểm từng tiêu chí $s_i$, tỷ lệ đóng góp $C_i$ (thanh xếp chồng) và chuỗi lý do gợi ý tất định. |
| **Vai trò trong đề cương** | Mốc tham chiếu về phạm vi chức năng của một website gia sư hoàn chỉnh. | Giải quyết khoảng trống giữa bước “lọc theo tiêu chí” và “chọn gia sư” ở Mục 1.3.1; đánh giá qua 14 kịch bản Bảng 5.1. |

---

## 3. Đoạn văn cập nhật vào Mục 1.3.2 của Đề cương

> Nhóm có tham khảo đồ án GS360 [3] như một ví dụ về hướng xây dựng website hỗ trợ tìm kiếm gia sư. Đồ án này không kế thừa khung tính năng của GS360 mà chỉ tập trung vào phần khuyến nghị.
>
> *(Dự thảo bổ sung — chờ nhóm xác nhận đối chiếu lần cuối với tài liệu gốc)* GS360 (Lê Thị Hoài Thương, Lê Nguyễn Quang Minh; Trường Đại học Công nghệ thông tin và Truyền thông Việt - Hàn, tháng 11/2024) là một website hỗ trợ tìm kiếm gia sư hoàn chỉnh: người dùng đăng ký/đăng nhập theo hai vai trò, gia sư quản lý hồ sơ và suất dạy, phụ huynh đăng bài tìm gia sư, đặt lịch, thanh toán và hoàn tiền, đánh giá gia sư, hỏi đáp và quản trị thống kê doanh thu (Mục 2.2.2, tr.13–14; các use case 2.2.6.1–2.2.6.19, tr.30–44; giao diện Mục 3.4, tr.60–69).
>
> Về tìm kiếm, Mục 2.1 (tr.11) mô tả GS360 cho phép tìm gia sư thông qua từ khóa tên môn học, cấp học và địa điểm; giao diện "tìm gia sư" ở Mục 3.4.6 (tr.64) là biểu mẫu đăng bài tìm gia sư, sau đó bài đăng được hiển thị ở trang suất dạy. Toàn văn tài liệu không mô tả cơ chế xếp hạng tổng hợp nhiều tiêu chí có trọng số, điểm thành phần hay lý do gợi ý (không xuất hiện các cụm "xếp hạng", "trọng số", "thuật toán").
>
> Khác với GS360, đồ án này không xây dựng nền tảng gia sư đầy đủ mà tập trung vào bộ máy khuyến nghị: lọc điều kiện bắt buộc (môn học, hình thức học, khung giờ giao nhau), chấm điểm năm tiêu chí ưu tiên theo Bảng 3.6, gộp bằng Weighted Scoring (Mục 2.3, 3.6) và trả Top-$k$ kèm điểm thành phần, đóng góp từng tiêu chí (Mục 3.1, 4.4). Vì vậy GS360 là mốc tham chiếu về phạm vi chức năng của một website gia sư, không phải baseline để so sánh độ chính xác xếp hạng; các kịch bản ở Bảng 5.1 mới là công cụ đánh giá của đồ án.

---

## 4. Mục Tài liệu tham khảo cập nhật

1. `[1]` S. Ramírez (Tiangolo), *FastAPI Documentation*. [Online]. Available: https://fastapi.tiangolo.com/
2. `[2]` Meta Platforms, Inc., *React Documentation*. [Online]. Available: https://react.dev/
3. `[3]` L. T. H. Thương, L. N. Q. Minh, *"GS360 - Xây dựng website hỗ trợ tìm kiếm gia sư"* (Đồ án cơ sở, Trường Đại học Công nghệ thông tin và Truyền thông Việt - Hàn, năm 2024). Available: https://fr.scribd.com/document/834112051/BAI-BAO-CAO-%C4%90%E1%BB%92-AN-C%C6%A0-S%E1%BB%9E-2
