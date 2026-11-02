> [!NOTE]
> **Đề xuất, nhóm xác nhận**

# Kế hoạch Sprint 5 (Sprint 5 Planning)

- **Thời gian thực hiện:** Hạn: 2026-12-18 (theo Milestone Sprint 5); ngày bắt đầu: [Chờ nhóm điền]
- **Mục tiêu Sprint (Sprint Goal):** Màn hình kết quả và tích hợp (E5 & E6) — hoàn thiện màn hình hiển thị danh sách gia sư gợi ý `ResultPage` (CN02) kèm thẻ thông tin `TutorCard` và biểu đồ thanh xếp chồng phân rã điểm đóng góp `StackedBarScore`, hiện thực tính năng điều chỉnh mức ưu tiên tương tác trực tiếp trên trang kết quả (CN03) với thời gian phản hồi dưới 1 giây, kết nối luồng hoạt động end-to-end từ nhập nhu cầu đến xem/điều chỉnh kết quả, kiểm thử đầy đủ các ca biên theo Mục 5.1 và điền hoàn chỉnh cột "Top-3 hệ thống" của Bảng 5.1 để vượt qua **Cổng chất lượng 3 (Quality Gate 3)**.
- **Giả định công suất nhóm:** 12 Story Points *(7 Must, 5 Should)*.

---

## 1. Danh sách User Stories cam kết trong Sprint

| Mã US | Tên User Story | Điểm SP | Mức ưu tiên | Mục đề cương | Issue | Phụ trách | Trạng thái |
|:---|:---|:---:|:---:|:---|:---:|:---:|:---:|
| **US-25** | Xây dựng màn hình hiển thị danh sách gia sư gợi ý (`ResultPage` — CN02) | 3 | Must | Mục 3.2 (CN02), Mục 3.8 (Hình 3.5), Mục 4.5 | #27 | *[Chờ nhóm phân công]* | Chưa làm |
| **US-26** | Hiển thị thanh xếp chồng phân rã điểm đóng góp của từng tiêu chí (`StackedBarScore`) | 2 | Should | Mục 3.3, Mục 3.8 (Hình 3.5), Mục 4.5 | #28 | *[Chờ nhóm phân công]* | Chưa làm |
| **US-27** | Hiện thực tính năng điều chỉnh mức ưu tiên tương tác trực tiếp (CN03) | 3 | Should | Mục 3.2 (CN03), Mục 4.5, Mục 4.6 | #29 | *[Chờ nhóm phân công]* | Chưa làm |
| **US-28** | Tích hợp giao diện với API và kiểm tra luồng hoạt động end-to-end | 2 | Must | Mục 4.6 | #30 | *[Chờ nhóm phân công]* | Chưa làm |
| **US-29** | Kiểm thử chức năng và kiểm thử ca biên trên toàn hệ thống, điền cột Top-3 hệ thống Bảng 5.1 | 2 | Must | Mục 5.1, Bảng 5.1 | #31 | *[Chờ nhóm phân công]* | Chưa làm |

- **Tổng điểm Story Points:** **12 SP** (7 Must, 5 Should).

---

## 2. Phân rã nhiệm vụ kỹ thuật (Tasks)

- **Phụ trách:** *[Chờ nhóm phân công]*
  - [ ] US-25 (#27) + US-26 (#28):
    - Xây dựng danh mục tra cứu tĩnh `frontend/src/data/tutorsCatalog.js` chứa 16 hồ sơ chuẩn hóa từ `data/processed/tutors.json` (môn dạy, khu vực, hình thức, học phí, kinh nghiệm, điểm đánh giá, khung giờ rảnh) để bổ sung thông tin hiển thị trên thẻ gia sư theo Hình 3.5 đề cương mà không cần thay đổi `docs/design/api-contract.md`.
    - Xây dựng component `frontend/src/components/StackedBarScore.jsx` vẽ thanh xếp chồng nhiều màu trên thang `[0, 1]`, trong đó chiều rộng mỗi phân đoạn của tiêu chí đang áp dụng bằng `contributions[i] * 100%` ($C_i = w_i \cdot s_i / \sum w_i$), tự động ẩn tiêu chí có `contributions[i] === null` và hiển thị tooltip chi tiết ($s_i$, $w_i$, $C_i$, tỷ trọng phần trăm) khi di chuột hoặc focus bàn phím.
    - Xây dựng component `frontend/src/components/TutorCard.jsx` và màn hình `frontend/src/pages/ResultPage.jsx` hiển thị danh sách Top-$k$ gia sư giảm dần theo `total_score`, lý do gợi ý (`reason`), ghi chú dữ liệu (`notes`), kèm thông báo thân thiện cho 2 trạng thái `no_match` (hiển thị cả `insufficient_data_candidates` nếu có) và `zero_weight` (hiển thị `unranked_candidates`).
  - [ ] US-27 (#29) + US-28 (#30):
    - Bổ sung bảng điều khiển mức ưu tiên trực tiếp (CN03) ngay trên `ResultPage.jsx`, cho phép đổi nhanh mức ưu tiên (`none`, `low`, `medium`, `high`) của 5 tiêu chí, tự động gọi lại `POST /api/recommend`, đo thời gian phản hồi thực tế (`< 1s`) và cập nhật mượt mà thứ hạng cùng thanh xếp chồng.
    - Bổ sung bộ nạp nhanh 14 kịch bản thực nghiệm (`KB01`–`KB14`) tại `frontend/src/data/scenariosCatalog.js` và kết nối luồng điều hướng hai chiều `SearchPage.jsx` (CN01) $\leftrightarrow$ `ResultPage.jsx` (CN02 + CN03) trong `frontend/src/App.jsx` và `frontend/src/App.css`, kèm xử lý lỗi mất kết nối backend hoặc lỗi `422`.
  - [ ] US-29 (#31):
    - Viết bộ kiểm thử tự động các ca biên và luồng CN03 theo đặc tả Mục 5.1 tại `backend/tests/api/test_boundary_muc_5_1.py` (kiểm tra học phí biên $P=B$, $P=1{,}25B$, $P=1{,}5B$, $P>1{,}5B$, $B=0$; kinh nghiệm biên $E=0$, $E=8$, $E>8$; đánh giá biên `None` và $5{,}0$; lịch rảnh biên $1/k$, $k/k$; tính đơn điệu và cập nhật thứ hạng khi đổi ưu tiên CN03).
    - Lập tài liệu báo cáo kết quả kiểm thử ca biên Mục 5.1 và điền đầy đủ cột **"Top-3 hệ thống"** của **Bảng 5.1** cho toàn bộ 14 kịch bản (`KB01`–`KB14`) tại `docs/thesis/report/muc-5.1-bang-5.1-ket-qua.md`.

---

## 3. Tiêu chí nghiệm thu Cổng chất lượng 3 (Quality Gate 3)

- [ ] Luồng end-to-end chạy trơn tru từ giao diện ReactJS (`SearchPage` $\rightarrow$ `ResultPage`) tới backend FastAPI (`POST /api/recommend`).
- [ ] Tính năng điều chỉnh mức ưu tiên trực tiếp (CN03) tự động gọi lại API và cập nhật thứ hạng kèm thanh xếp chồng dưới 1 giây.
- [ ] Hoàn thành kiểm thử chức năng và các ca biên theo Mục 5.1 đề cương; điền đầy đủ cột **"Top-3 hệ thống"** vào **Bảng 5.1** trong tài liệu báo cáo.

---

## 4. Rủi ro dự kiến và phương án xử lý

- *Rủi ro 1:* Phản hồi của `POST /api/recommend` trong `docs/design/api-contract.md` chỉ trả về `tutor_id`, `full_name`, điểm số và lời giải thích, chưa kèm các thuộc tính tĩnh của hồ sơ (môn dạy, học phí, năm kinh nghiệm, điểm đánh giá, khu vực, khung giờ) để hiển thị đầy đủ thẻ gia sư theo Hình 3.5. $\rightarrow$ *Phương án:* Giữ nguyên tuyệt đối `docs/design/api-contract.md` (không tự ý thêm endpoint ngoài hợp đồng); sử dụng danh mục tĩnh `frontend/src/data/tutorsCatalog.js` đồng bộ từ 16 hồ sơ chuẩn hóa `data/processed/tutors.json` để tra cứu thông tin hồ sơ theo `tutor_id`, còn toàn bộ kết quả lọc, xếp hạng, điểm số và giải thích lấy trực tiếp từ phản hồi API.
- *Rủi ro 2:* Người dùng bấm đổi mức ưu tiên liên tiếp trên bảng CN03 làm nhiều request chồng lấn. $\rightarrow$ *Phương án:* Quản lý bộ đếm yêu cầu hiện hành (`requestId`) và trạng thái đang cập nhật trên `ResultPage.jsx` để chỉ áp dụng kết quả của lần thay đổi mới nhất và hiển thị rõ độ trễ phản hồi (ms).
- *Rủi ro 3:* Sai lệch tỷ lệ hiển thị trên thanh xếp chồng khi có tiêu chí bị loại (`contributions[i] === null`). $\rightarrow$ *Phương án:* Tính chiều rộng từng đoạn trực tiếp theo `contributions[i] * 100%` trên thang `[0, 1]` và chỉ dựng các tiêu chí có `contributions[i] !== null`, đảm bảo tổng chiều rộng các đoạn màu luôn bằng đúng `total_score * 100%`.
