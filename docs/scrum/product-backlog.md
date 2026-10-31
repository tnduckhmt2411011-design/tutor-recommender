> [!NOTE]
> **Đề xuất, nhóm xác nhận**

# Danh mục yêu cầu sản phẩm (Product Backlog)

Tài liệu quản lý toàn bộ các hạng mục công việc (User Stories) của đồ án **"Hệ thống khuyến nghị gia sư dựa trên mức độ phù hợp đa tiêu chí"**, được cấu trúc theo 8 Epic (E0–E7), ước lượng điểm theo thang Fibonacci và phân bổ trong 6 Sprint.

## 1. Bảng tổng hợp Product Backlog

| Mã US | Epic | Câu tóm tắt Story | Điểm SP | Mức ưu tiên | Sprint | Mục đề cương | Issue GitHub |
|:---|:---|:---|:---:|:---:|:---:|:---|:---:|
| **US-01** | E0 Hạ tầng và quy trình | Là nhóm phát triển, tôi muốn thiết lập môi trường Python 3.12, file requirements.txt ghim chính xác p... | 1 | Must | Sprint 1 | Mục 4.1 | [#1](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/1) |
| **US-02** | E0 Hạ tầng và quy trình | Là nhóm phát triển, tôi muốn cấu hình GitHub Actions workflow tự động chạy ruff check và pytest mỗi k... | 1 | Should | Sprint 1 | Mục 4.1 | [#2](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/2) |
| **US-03** | E0 Hạ tầng và quy trình | Là nhóm phát triển, tôi muốn khởi tạo dự án ReactJS tối giản bằng công cụ Vite trong thư mục frontend... | 1 | Must | Sprint 1 | Mục 4.1, Mục 4.5 | [#3](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/3) |
| **US-04** | E0 Hạ tầng và quy trình | Là nhóm phát triển, tôi muốn hoàn thiện bộ tài liệu quy trình Scrum (vai trò PO/SM, working agreement... | 1 | Must | Sprint 1 | Mục 1.5, Bảng 6.1 | [#4](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/4) |
| **US-05** | E1 Thiết kế và dữ liệu | Là nhóm phát triển, tôi muốn tổng hợp và gửi báo cáo tiến độ phần khóa bài toán (Mục 1.4, 1.5, 3.1–3.... | 1 | Must | Sprint 1 | Mục 1.4, Mục 1.5, Chương 3 | [#5](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/5) |
| **US-06** | E1 Thiết kế và dữ liệu | Là nhóm phát triển, tôi muốn chuẩn hóa 16 hồ sơ gia sư từ Phụ lục A đề cương thành các tệp dữ liệu da... | 2 | Must | Sprint 1 | Mục 3.5, Mục 4.2, Phụ lục A | [#6](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/6) |
| **US-07** | E1 Thiết kế và dữ liệu | Là nhóm phát triển, tôi muốn số hóa 14 kịch bản thực nghiệm từ Bảng 5.1 thành file backend/tests/scen... | 2 | Must | Sprint 1 | Mục 5.1, Mục 5.2, Bảng 5.1 | [#7](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/7) |
| **US-08** | E1 Thiết kế và dữ liệu | Là nhóm phát triển, tôi muốn soạn thảo tài liệu đặc tả hợp đồng API docs/design/api-contract.md quy đ... | 1 | Must | Sprint 1 | Mục 3.7.2, Mục 4.4, Bảng 3.4 | [#8](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/8) |
| **US-31** | E7 Báo cáo và bảo vệ | Là nhóm phát triển, tôi muốn nghiên cứu chi tiết tài liệu tham khảo GS360 [3], bổ sung so sánh cụ thể... | 1 | Must | Sprint 1 | Mục 1.2, Mục 1.3, Tài liệu tham khảo [3] | [#9](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/9) |
| **US-32** | E7 Báo cáo và bảo vệ | Là nhóm phát triển, tôi muốn điền đầy đủ bảng phân công nhiệm vụ 3 thành viên (Bảng 6.1) và soạn thảo... | 1 | Must | Sprint 1 | Mục 6.1, Mục 6.3, Bảng 6.1 | [#10](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/10) |
| **US-09** | E2 Lõi chấm điểm | Là nhóm phát triển, tôi muốn xây dựng module backend/app/data/repository.py đọc tệp JSON/CSV dữ liệu ... | 2 | Must | Sprint 2 | Mục 3.5, Mục 4.2 | [#11](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/11) |
| **US-10** | E2 Lõi chấm điểm | Là nhóm phát triển, tôi muốn xây dựng hàm lọc kiểm tra các điều kiện cứng: đúng môn học, phù hợp hình... | 2 | Must | Sprint 2 | Mục 2.3, Mục 3.4, Mục 3.6 (Bước 2), Bảng 3.2 | [#12](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/12) |
| **US-11** | E2 Lõi chấm điểm | Là nhóm phát triển, tôi muốn hiện thực 5 hàm tính điểm thành phần s_i trong [0, 1] cho Học phí, Khu v... | 3 | Must | Sprint 2 | Mục 3.6 (Bước 3), Bảng 3.6 | [#13](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/13) |
| **US-12** | E2 Lõi chấm điểm | Là nhóm phát triển, tôi muốn hiện thực module backend/app/scoring/weights.py quy đổi 4 mức ưu tiên (K... | 1 | Must | Sprint 2 | Mục 3.4, Mục 3.6, Bảng 3.5 | [#14](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/14) |
| **US-13** | E2 Lõi chấm điểm | Là nhóm phát triển, tôi muốn xây dựng bộ unit test kiểm thử toàn bộ 5 hàm điểm với tối thiểu 3 ca thử... | 2 | Must | Sprint 2 | Mục 3.6, Mục 5.1, Bảng 3.6 | [#15](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/15) |
| **US-14** | E3 Xếp hạng và giải thích | Là nhóm phát triển, tôi muốn hiện thực cơ chế kiểm tra ngưỡng dữ liệu tối thiểu theo Bảng ngưỡng đề c... | 2 | Must | Sprint 3 | Mục 3.6 (Bảng ngưỡng dữ liệu tối thiểu) | [#16](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/16) |
| **US-15** | E3 Xếp hạng và giải thích | Là người học, tôi muốn nhận được danh sách gia sư được sắp xếp giảm dần theo điểm tổng hợp S(g)... | 2 | Must | Sprint 3 | Mục 2.3, Mục 3.6 (Bước 4), CN02 (CN02) | [#17](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/17) |
| **US-16** | E3 Xếp hạng và giải thích | Là người học, tôi muốn xem được mức đóng góp cụ thể của từng tiêu chí vào điểm tổng và lời giải... | 2 | Must | Sprint 3 | Mục 3.3, Mục 3.6 (Bước 4), CN02 (CN02) | [#18](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/18) |
| **US-17** | E3 Xếp hạng và giải thích | Là nhóm phát triển, tôi muốn viết kịch bản test tự động nạp 14 ca thử nghiệm từ scenarios.json, chạy ... | 2 | Must | Sprint 3 | Mục 5.1, Mục 5.2, Bảng 5.1 | [#19](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/19) |
| **US-18** | E3 Xếp hạng và giải thích | Là nhóm phát triển, tôi muốn phân tích chi tiết nguyên nhân toán học và dữ liệu tại các kịch bản có k... | 1 | Must | Sprint 3 | Mục 5.2, Bảng 5.1 | [#20](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/20) |
| **US-19** | E4 API | Là hệ thống giao diện, tôi muốn gửi yêu cầu tìm gia sư kèm bộ trọng số qua phương thức POST tới /api/rec... | 2 | Must | Sprint 4 | Mục 4.4, Bảng 3.4 | [#21](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/21) |
| **US-20** | E4 API | Là người dùng API, tôi muốn nhận được mã phản hồi và thông điệp rõ ràng khi dữ liệu không hợp lệ, kh... | 2 | Must | Sprint 4 | Mục 3.1, Mục 3.6, Mục 4.4 | [#22](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/22) |
| **US-21** | E4 API | Là nhóm phát triển, tôi muốn viết bộ kiểm thử tích hợp sử dụng TestClient của FastAPI để kiểm tra toà... | 2 | Must | Sprint 4 | Mục 4.4, Mục 5.1 | [#23](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/23) |
| **US-22** | E4 API | Là nhà phát triển frontend, tôi muốn backend được cấu hình CORS mở cho client ReactJS và tài liệu Swagger UI ... | 1 | Should | Sprint 4 | Mục 2.4, Mục 4.4 | [#24](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/24) |
| **US-23** | E5 Giao diện | Là người học, tôi muốn sử dụng biểu mẫu giao diện trực quan để chọn môn học, hình thức học, khu... | 3 | Must | Sprint 4 | Mục 3.2 (CN01), Mục 3.8 (Hình 3.4), Mục 4.5 (CN01) | [#25](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/25) |
| **US-24** | E5 Giao diện | Là lập trình viên frontend, tôi muốn xây dựng module frontend/src/services/api.js đóng gói các cuộc gọi HTTP ... | 1 | Must | Sprint 4 | Mục 4.5, Mục 4.6 | [#26](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/26) |
| **US-25** | E5 Giao diện | Là người học, tôi muốn xem danh sách Top-k gia sư được đề xuất dưới dạng thẻ thông tin trực qua... | 3 | Must | Sprint 5 | Mục 3.2 (CN02), Mục 3.8 (Hình 3.5), Mục 4.5 (CN02) | [#27](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/27) |
| **US-26** | E5 Giao diện | Là người học, tôi muốn quan sát biểu đồ thanh xếp chồng (stacked bar) thể hiện tỉ lệ đóng góp c... | 2 | Should | Sprint 5 | Mục 3.3, Mục 3.8 (Hình 3.5), Mục 4.5 | [#28](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/28) |
| **US-27** | E5 Giao diện | Là người học, tôi muốn thay đổi nhanh mức ưu tiên của các tiêu chí ngay trên màn hình kết quả v... | 3 | Should | Sprint 5 | Mục 3.2 (CN03), Mục 4.5, Mục 4.6 (CN03) | [#29](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/29) |
| **US-28** | E6 Kiểm thử và đánh giá | Là nhóm phát triển, tôi muốn kết nối toàn diện giao diện ReactJS với backend FastAPI và kiểm thử toàn... | 2 | Must | Sprint 5 | Mục 4.6 | [#30](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/30) |
| **US-29** | E6 Kiểm thử và đánh giá | Là nhóm phát triển, tôi muốn thực hiện kiểm thử chức năng và các ca biên theo đặc tả Mục 5.1 (học phí... | 2 | Must | Sprint 5 | Mục 5.1, Bảng 5.1 | [#31](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/31) |
| **US-30** | E6 Kiểm thử và đánh giá | Là nhóm phát triển, tôi muốn phân tích độ ổn định của hệ thống khi thay đổi nhẹ các tham số đầu vào v... | 2 | Must | Sprint 6 | Mục 5.2 | [#32](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/32) |
| **US-33** | E7 Báo cáo và bảo vệ | Là nhóm phát triển, tôi muốn tổng hợp toàn bộ kết quả thực nghiệm, phân tích hạn chế Mục 5.3, kết luậ... | 3 | Must | Sprint 6 | Chương 5, Chương 6 | [#33](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/33) |
| **US-34** | E7 Báo cáo và bảo vệ | Là người dùng hoặc người chấm đồ án, tôi muốn đọc tài liệu README.md với đầy đủ các bước cài đặt môi trường, nạp dữ li... | 1 | Must | Sprint 6 | Mục 4.1, Phụ lục B | [#34](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/34) |
| **US-35** | E7 Báo cáo và bảo vệ | Là nhóm sinh viên thực hiện, tôi muốn thiết kế bộ slide thuyết trình bảo vệ đồ án và chuẩn bị kịch bản demo ch... | 2 | Must | Sprint 6 | Báo cáo đồ án & slide | [#35](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/35) |
| **US-36** | E7 Báo cáo và bảo vệ | Là nhóm phát triển, tôi muốn rà soát đồng bộ số trang, danh mục hình ảnh, danh mục bảng biểu của tài ... | 1 | Must | Sprint 6 | Mục lục, Toàn bộ báo cáo | [#36](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/36) |
| **US-37** | E1 Thiết kế và dữ liệu | Là nhóm phát triển, tôi muốn chuyển đổi cơ chế lưu trữ từ tệp JSON sang bảng đơn trong cơ sở dữ liệu ... | 2 | Could | Chưa xếp | Mục 2.4, Mục 4.2 | [#37](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/37) |
| **US-38** | E5 Giao diện | Là người học, tôi muốn xem lại các cấu hình nhu cầu tìm kiếm trước đó được lưu trữ trong trình ... | 1 | Could | Chưa xếp | Tính năng mở rộng | [#38](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/38) |
| **US-39** | E5 Giao diện | Là người học, tôi muốn xuất danh sách Top-k gia sư kèm thông tin liên hệ và lý do gợi ý ra file... | 1 | Could | Chưa xếp | Tính năng mở rộng | [#39](https://github.com/tnduckhmt2411011-design/tutor-recommender/issues/39) |

## 2. Thống kê độ lớn Backlog

- **Tổng số User Stories:** 39 stories
- **Tổng điểm Story Points:** 67 SP
  - **Mức Must (Bắt buộc):** 56 SP (31 stories)
  - **Mức Should (Nên có):** 7 SP (5 stories: CI backend, Swagger/CORS, thanh xếp chồng, tương tác CN03)
  - **Mức Could (Có thể):** 4 SP (3 stories dự phòng: SQLite, lưu lịch sử LocalStorage, xuất PDF)
- **Phân bổ theo Sprint:**
  - **Sprint 1:** 12 SP (11 Must, 1 Should)
  - **Sprint 2:** 10 SP (10 Must)
  - **Sprint 3:** 9 SP (9 Must)
  - **Sprint 4:** 11 SP (10 Must, 1 Should)
  - **Sprint 5:** 12 SP (7 Must, 5 Should)
  - **Sprint 6:** 9 SP (9 Must)
  - **Chưa xếp sprint (Could):** 4 SP (3 stories dự phòng)
