> [!NOTE]
> **Đề xuất, nhóm xác nhận**

# Thỏa thuận làm việc nhóm (Working Agreement)

Tài liệu quy định các nguyên tắc giao tiếp, lịch trình nghi thức Scrum và quy chuẩn kỹ thuật mà toàn bộ thành viên cam kết tuân thủ trong suốt quá trình thực hiện đồ án.

---

## 1. Kênh liên lạc và trao đổi

- **Kênh liên lạc chính thức của nhóm:** `Zalo` và `Discord`.
- **Kênh lưu trữ mã nguồn và tài liệu:** GitHub Repository `https://github.com/tnduckhmt2411011-design/tutor-recommender`.
- **Thời gian phản hồi:** Thành viên phản hồi tin nhắn công việc trong vòng tối đa 6–12 giờ vào các ngày trong tuần (trừ trường hợp khẩn cấp có thông báo trước).

---

## 2. Các nghi thức Scrum tinh gọn (Lightweight Ceremonies)

Nhằm tối ưu hóa thời gian và tránh lãng phí công sức, các nghi thức Scrum được tổ chức tinh gọn với mục tiêu chi phí thời gian họp **chiếm dưới 10–15% tổng giờ sprint**:

1. **Sprint Planning (Lập kế hoạch Sprint):**
   - *Thời lượng:* 45 phút vào đầu ngày thứ Hai của tuần đầu tiên trong Sprint.
   - *Mục tiêu:* PO trình bày mục tiêu sprint; nhóm chọn các User Story từ Backlog, làm rõ tiêu chí chấp nhận và phân công công việc.
2. **Async Daily Standup (Họp báo cáo hằng ngày bất đồng bộ):**
   - *Hình thức:* Bất đồng bộ trên kênh chat của nhóm vào các ngày **thứ Hai, thứ Tư, thứ Sáu**.
   - *Nội dung:* Mỗi thành viên gửi đúng 3 dòng ngắn gọn:
     1. *Hôm qua tôi đã hoàn thành việc gì?*
     2. *Hôm nay tôi sẽ làm việc gì?*
     3. *Tôi có gặp khó khăn hay vướng mắc (blocker) nào không?*
3. **Backlog Refinement (Làm mịn Backlog):**
   - *Thời lượng:* 20 phút vào giữa sprint (thứ Sáu tuần 1).
   - *Mục tiêu:* Rà soát các story của sprint tiếp theo, bổ sung chi tiết tiêu chí chấp nhận theo Definition of Ready.
4. **Sprint Review & Retrospective gộp (Sơ kết và Rút kinh nghiệm):**
   - *Thời lượng:* 45–60 phút vào ngày thứ Bảy cuối tuần thứ hai của Sprint.
   - *Mục tiêu:* Demo các tính năng đã hoàn thành theo Definition of Done; đánh giá tiến độ so với Lộ trình; thảo luận 1–2 điểm cần cải tiến trong quy trình làm việc sprint sau.

---

## 3. Quy chuẩn làm việc trên GitHub và Quản lý mã nguồn

1. **Quy tắc nhánh (Branching Convention):**
   - Nhánh `main` là nhánh ổn định, chỉ nhận mã nguồn thông qua Pull Request, tuyệt đối không push trực tiếp lên `main`.
   - Nhánh tính năng: `feat/<số-issue>-<tên-ngắn>` (ví dụ: `feat/11-criteria-scoring`).
   - Nhánh tài liệu: `docs/<tên-ngắn>` (ví dụ: `docs/scrum-roadmap`).
   - Nhánh sửa lỗi: `fix/<số-issue>-<tên-ngắn>` (ví dụ: `fix/15-tie-breaker`).
2. **Quy chuẩn thông điệp Commit (Commit Convention):**
   - Tiếng Việt có dấu, một dòng ngắn gọn, mang tính mô tả rõ hành động.
   - Bắt buộc có tiền tố chuẩn: `feat:`, `fix:`, `docs:`, `test:`, `chore:`.
   - Ví dụ: `feat: cài đặt 5 hàm chuẩn hóa điểm thành phần Bảng 3.6`.
3. **Quy trình Pull Request và Merge:**
   - Mỗi PR phải mô tả ngắn gọn nội dung thay đổi và liên kết với Issue tương ứng (ví dụ: `Closes #11`).
   - Bắt buộc kiểm tra tự động (CI pytest, ruff) báo xanh (pass 100%).
   - Cần tối thiểu **1 thành viên khác trong nhóm review và phê duyệt (Approve)**.
   - Luôn sử dụng hình thức **Squash and merge** để giữ lịch sử git trên `main` gọn gàng.
