> [!NOTE]
> **Đề xuất, nhóm xác nhận**

# Rút kinh nghiệm Sprint 6 (Sprint 6 Retrospective)

- **Ngày họp:** *[Chờ nhóm điền]*
- **Người điều phối:** Scrum Master (Trần Nguyễn Đức)
- **Thành viên tham gia:** *[Chờ nhóm điền]*

---

## 1. Dữ kiện lịch sử repo làm cơ sở thảo luận

- **Tiến độ so với Milestone:** Hạn Milestone của Sprint 6 là `2027-01-01`. Mười một PR của Sprint 6 (#80, #81, #84–#92) được hợp nhất từ `2026-11-09` đến `2026-11-16`, sớm hơn hạn Milestone khoảng 6 tuần. PR #93 (slide, hình Chương 3, front matter, thay nguồn tham khảo) đang mở với head `bfe0b9b`; tag `v1.0` chưa tạo.
- **Khối lượng bàn giao:** 12/13 Story Point hoàn tất (8/9 SP `Must` và 4/4 SP `Should`), 1 SP còn lại thuộc US-36 chờ thao tác phát hành; báo cáo hoàn chỉnh 6 chương với **31 bảng** và **9 hình**, toàn bộ bảng/hình đều được dẫn chiếu trong thân bài; bộ kiểm thử tăng từ `190` lên **`200 passed, 0 skipped`** với độ bao phủ **97%** (340/351 câu lệnh).
- **Hai story `Should` được làm trước một phần story `Must`:** US-40 (#79) và US-41 (#82) được hợp nhất ngày `2026-11-09`–`2026-11-10`, trong khi US-30 (#32) và US-33 (#33) hợp nhất ngày `2026-11-10`–`2026-11-11`. Việc này không ảnh hưởng Cổng chất lượng 4 nhưng làm thứ tự ưu tiên trong kế hoạch Sprint không còn phản ánh thứ tự thực thi.
- **Khác biệt giữa kế hoạch và hiện thực ở US-41:** Kế hoạch ghi “thêm `learningGoal` vào `searchForm`” và “hiển thị mục tiêu đã chọn ở `ResultPage`”; bản hiện thực đặt bảng ánh xạ tại `frontend/src/data/goalPresets.js`, suy ra giá trị ô chọn từ 5 mức ưu tiên hiện tại (không thêm state, không thêm trường vào payload) và không hiển thị lại mục tiêu ở `ResultPage`. Cách làm này giữ nguyên hợp đồng API nhưng làm mô tả nhiệm vụ trong `planning.md` không còn khớp mã nguồn.
- **Số liệu thời gian chạy kiểm thử không ổn định giữa các môi trường:** Báo cáo ghi `1,18 giây` cho 200 bài kiểm thử; lần chạy lại trên máy khác cho `1,90 giây`. Số lượng bài kiểm thử và tỷ lệ đạt không đổi, chỉ thời gian chạy thay đổi theo máy.
- **Biên bản Sprint 6 hoàn tất sau khi đã hợp nhất 11 PR:** `review.md` và `retrospective.md` của Sprint 6 được soạn ngày `2026-11-17`, tức sau thời điểm hợp nhất gần như toàn bộ PR của sprint; dòng khai báo tệp biên bản trong `planning.md` đã được đánh dấu hoàn thành từ trước khi tệp tồn tại.
- **Thay nguồn tham khảo thiếu tính học thuật:** Sáu mục trong `tai-lieu-tham-khao.md` vốn trỏ tới Wikipedia; PR #93 thay bằng 6 ấn phẩm có DOI (Bray & Kwok 2003; Triantaphyllou 2000; Su & Khoshgoftaar 2009; Adomavicius & Tuzhilin 2005; Manning và cộng sự 2008; Fishburn 1967), đồng thời chỉnh lại câu dẫn ở Chương 1 và Chương 2 cho khớp nội dung nguồn mới.

---

## 2. Những điểm đã làm tốt (What went well?)

- **Bàn giao đúng hạn và vượt phạm vi `Must Have`:** Toàn bộ 9 SP `Must` đều có sản phẩm nghiệm thu được (8 SP hoàn tất, 1 SP của US-36 chờ thao tác phát hành), cộng thêm 4 SP `Should` (US-40, US-41) hoàn tất trước hạn Milestone khoảng 6 tuần.
- **Số liệu trong báo cáo bám sát lần chạy thật:** Bộ kiểm thử tự động tăng từ `190` lên `200` bài, độ bao phủ 97%, 14/14 kịch bản trùng Top-3; các số liệu này được dùng thống nhất ở Chương 5, Chương 6, `README.md`, slide và kịch bản demo thay vì mỗi nơi một con số.
- **Kiểm chứng nguồn thay vì tin vào cảm nhận:** Sáu nguồn Wikipedia được thay bằng ấn phẩm có DOI và metadata đối chiếu qua cơ sở dữ liệu trích dẫn; câu dẫn trong thân bài cũng được sửa lại để không nói quá nội dung nguồn.
- **Hồ sơ bàn giao có thể kiểm tra chéo:** Mục lục, danh mục 31 bảng, danh mục 9 hình và hồ sơ bàn giao nằm trong một tệp duy nhất, cho phép đối chiếu ký hiệu bảng/hình với thân bài mà không phải mở từng chương.
- **Cổng chất lượng có bằng chứng chạy được:** Mỗi điều kiện của Cổng chất lượng 4 gắn với một lệnh hoặc một tệp cụ thể (`pytest`, `oxlint`, `vite build`, `README.md`, `docs/thesis/slides/`), không dừng ở mô tả định tính.

---

## 3. Những điểm cần cải thiện (What could be improved?)

- **Biên bản sprint đi sau sản phẩm:** `review.md` và `retrospective.md` được soạn sau khi đã hợp nhất 11 PR, trong khi `planning.md` đã đánh dấu hoàn thành từ trước. Biên bản mất giá trị như một công cụ điều phối trong sprint và trở thành thủ tục ghi nhớ hậu kỳ.
- **Kế hoạch nhiệm vụ không được cập nhật khi thiết kế thay đổi:** Trường hợp US-41 cho thấy mô tả trong `planning.md` (thêm `learningGoal`, hiển thị ở `ResultPage`) khác bản hiện thực (`goalPresets.js`, giá trị suy ra). Người đọc sau phải mở mã nguồn mới hiểu đúng phạm vi đã làm.
- **Thứ tự thực thi lệch mức ưu tiên:** Hai story `Should` (US-40, US-41, 4 SP) được hợp nhất trước US-30 và US-33 (5 SP `Must`). Với sprint cuối khóa, thứ tự này tạo rủi ro nếu tiến độ căng, vì hạng mục `Should` có thể cắt được còn `Must` thì không.
- **Số liệu thời gian chạy thiếu môi trường đo:** Báo cáo ghi `1,18 giây` nhưng lần chạy lại cho `1,90 giây`; cùng một bộ kiểm thử nhưng khác máy. Số liệu thời gian nên kèm cấu hình máy hoặc chỉ nêu ngưỡng, tránh gây tranh luận không cần thiết khi bảo vệ.
- **Bước phát hành chưa được đóng thành checklist:** Việc gắn tag `v1.0` phụ thuộc vào một PR còn mở và vào chỉ định của nhóm trưởng, nhưng không có danh sách kiểm tra phát hành (hợp nhất PR nào, xác nhận CI nào, tag ở commit nào). Đây là lý do Cổng chất lượng 4 dừng ở 4/5 điều kiện.

---

## 4. Hành động cải tiến cho giai đoạn sau (Action Items)

- **Chốt checklist phát hành `v1.0` trước khi hợp nhất PR #93:** xác nhận CI xanh, xác nhận đủ 31 bảng và 9 hình trong bản Word cuối, rồi mới hợp nhất và tạo tag trên đúng commit của `main`.
- **Đưa biên bản sprint vào Definition of Done của sprint, không phải của story:** `review.md` và `retrospective.md` phải tồn tại trước khi đóng sprint; không đánh dấu hoàn thành nhiệm vụ soạn biên bản khi tệp chưa được tạo.
- **Cập nhật `planning.md` ngay khi thiết kế thay đổi:** mọi khác biệt giữa kế hoạch và mã nguồn (như US-41) phải được ghi lại trong cùng PR với thay đổi kỹ thuật, kèm một dòng lý do.
- **Giữ thứ tự `Must` trước `Should` khi sprint cuối khóa:** chỉ bắt đầu hạng mục `Should` sau khi các hạng mục `Must` đã có bản chạy được và đã qua kiểm thử.
- **Ghi rõ môi trường đo khi công bố số liệu thời gian:** nêu cấu hình máy hoặc dùng ngưỡng thay vì một con số tuyệt đối, và chỉ công bố một lần cho mỗi phép đo.
- **Duy trì quy tắc kiểm chứng nguồn:** không dùng nguồn bách khoa mở trong danh mục tham khảo; mọi nguồn mới phải có DOI hoặc số hiệu xuất bản tra được, và câu dẫn phải khớp nội dung nguồn.
