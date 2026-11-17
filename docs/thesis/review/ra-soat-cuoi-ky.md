# Báo cáo rà soát cuối kỳ — Văn phong, Logic và Số liệu

- **Nhánh gốc đối chiếu:** `origin/main` tại commit `9ba3db7` (*"docs: hoàn thiện hình Chương 3, front matter và slide bảo vệ (#93)"*).
- **Nhánh rà soát & sửa lỗi:** `docs/ra-soat-ghep-bao-cao` (worktree `_thesis-main`).
- **Quy chuẩn áp dụng:** `D:\Use Antigravity\Medical Vision\docs\report_standards.md` (Mục 2–3), `academic_writing_guide.md` (văn phong, từ cấm), và đối chiếu trực tiếp với mã nguồn `backend/`, `frontend/`, `data/processed/`, `Input\ĐỀ CƯƠNG HỆ THỐNG KHUYẾN NGHỊ_DU-THAO_v3.docx`.
- **Công cụ kiểm chứng tự động:**
  - `pytest -q` (tại `backend/`): **200 passed, 1 warning in 1.32s** (và `--cov=app`: **340/351 statements, 97%**).
  - `scripts/thesis/check_captions.py`: kiểm tra 31 bảng, 9 hình, ảnh nhúng, dẫn chiếu mục/bảng/hình, trích dẫn `[1]`–`[11]`.
  - `scripts/thesis/recompute_numbers.py`: kiểm tra 74 claim số liệu và xuất bảng đối chiếu `docs/thesis/review/so-lieu-doi-chieu.csv`.

---

## 1. Phần A — Rà soát Văn phong (`VP`)

Toàn bộ các tệp thuộc báo cáo (`muc-luc-va-ho-so-ban-giao.md`, `chuong-01` đến `chuong-06` kể cả Phụ lục A–D, `tai-lieu-tham-khao.md`, kèm đối chiếu `muc-5.1-bang-5.1-ket-qua.md` và `muc-5.2-danh-gia-do-on-dinh.md`) đã được đọc toàn văn bởi 5 phiên rà soát độc lập và quét tự động.

**Xác nhận đã đọc toàn văn:**
- `muc-luc-va-ho-so-ban-giao.md` (274 dòng): 19 vấn đề.
- `chuong-01-tong-quan.md` (84 dòng): 17 vấn đề.
- `chuong-02-co-so-ly-thuyet-va-cong-nghe.md` (57 dòng): 10 vấn đề.
- `chuong-03-phan-tich-thiet-ke.md` (200 dòng): 19 vấn đề.
- `chuong-04-xay-dung-he-thong.md` (302 dòng): 28 vấn đề.
- `chuong-05-thuc-nghiem-va-danh-gia.md` (298 dòng): 37 vấn đề (+3 vấn đề kế thừa từ `muc-5.1`/`muc-5.2`).
- `chuong-06-ket-luan-va-huong-phat-trien.md` (249 dòng): 38 vấn đề.
- `tai-lieu-tham-khao.md` (23 dòng): 9 vấn đề.

### Danh mục lỗi văn phong trọng yếu cần xử lý (gộp các mục tiêu biểu; bản chi tiết từng dòng được xử lý trong các commit tương ứng)

| ID | Tệp:dòng | Loại | Mức | Trích nguyên văn | Đề xuất sửa | Trạng thái |
|:---|:---|:---|:---:|:---|:---|:---|
| VP-001 | `chuong-01:3–4`, `02:3–4`, `03:3–4`, `04:3–4`, `05:3–4`, `06:3–4`, `05:297–298`, `muc-luc:1,3–4` | Dấu vết nháp nội bộ | Blocker | `> [!NOTE] > **Đề xuất, nhóm xác nhận**` và ghi chú `User Story US-36` | Xóa khỏi các chương báo cáo (phần `muc-luc` dùng bộ tách `split_front_matter` chỉ lấy Mục 3–10 khi xuất DOCX). | Sửa khách quan |
| VP-002 | `muc-luc:8` | Lộ đường dẫn máy cá nhân | Blocker | `` `D:\Use Antigravity\Medical Vision\docs\report_standards.md` `` | Thay bằng mô tả quy chuẩn chung trong phần tài liệu quy trình (và không đưa Mục 1–2 vào bản Word). | Sửa khách quan |
| VP-003 | `chuong-05:288, 291` | Lộ ghi chú bảo vệ / tiến độ | Blocker | `chuẩn bị sẵn phương án giải trình khi bảo vệ đồ án...`; `tại thời điểm soạn thảo báo cáo, nhóm chưa nhận được ý kiến... từ GVHD` | Xóa khỏi Mục 5.3 Hạn chế của hệ thống (nêu ngắn gọn việc chưa thử nghiệm với người học thật). | Sửa khách quan |
| VP-004 | `chuong-05:74,121,162,170,232,254,280` | Dấu vết file làm việc | Blocker | Dẫn chiếu ngược ra `muc-5.1`, `muc-5.2`, `discrepancy_analysis.md` | Xóa các dòng dẫn chiếu ra file làm việc nội bộ (nội dung đã tích hợp vào Chương 5). | Sửa khách quan |
| VP-005 | `chuong-01:84`, `chuong-05:6` | Lộ metadata Git / Scrum | Major | `(Mô hình A, docs/scrum/roadmap.md)`; `commit gốc f66f065 ... commit d9548ce trên nhánh chính origin/main` | Bỏ mã commit/tên nhánh/đường dẫn kế hoạch Scrum khỏi văn xuôi chính thức. | Sửa khách quan |
| VP-006 | `chuong-05:20,66,106–119,289`, `chuong-06:150` | Từ cấm / AI slop (`tuyệt đối`) | Major | 12/15 lần dùng `tuyệt đối` ở Ch5 (`độ bao phủ tuyệt đối 100%`, `Điểm đánh giá tuyệt đối`, `Trùng khớp tuyệt đối`, `tuân thủ tuyệt đối`) và `đồng bộ tuyệt đối` ở Ch6 | Sửa thành `100%`, `tối đa`, `Khớp thứ hạng và điểm số`, `tính đúng theo`, `khớp từng ô` (giữ 3 chỗ `đồng điểm tuyệt đối` / `hòa điểm tuyệt đối` mang nghĩa toán học). | Sửa khách quan |
| VP-007 | `chuong-05:17,18,42,44,258,278,286`, `chuong-06:18,20,21,49,54,62,94,183` | AI slop / Từ tâng bốc / Sáo rỗng | Major | `chuyên sâu`, `tức thời`, `cảnh báo thân thiện`, `minh chứng tính minh bạch`, `Trên tinh thần học thuật khách quan và trung thực`, `trọn vẹn`, `toàn diện`, `Thiếu vắng`, `bài bản`, `minh bạch` | Thay bằng từ ngữ kỹ thuật trung tính, bỏ mở đầu rập khuôn và tính từ tự khen. | Sửa khách quan |
| VP-008 | `chuong-04:6,209` | Chính tả tiếng Việt | Major | `không lập lại` | Sửa thành `không lặp lại`. | Sửa khách quan |
| VP-009 | `chuong-04:181`, `chuong-06:19,175,176` | Dùng từ thiếu chuẩn | Major | `kiểm thực` (`kiểm thực dữ liệu`, `lỗi kiểm thực`) | Thống nhất dùng `kiểm tra hợp lệ` / `xác thực dữ liệu`. | Sửa khách quan |
| VP-010 | `chuong-05:168,286,288,293`, `chuong-06:6,103,111,138`, `muc-luc:71` | Đại từ nhân xưng không nhất quán | Major | `nhóm nghiên cứu` (lẫn với `nhóm`), `Nhóm chúng em cam đoan` (lẫn với `Nhóm chịu trách nhiệm`) | Thống nhất dùng `nhóm` / `Nhóm` (giữ `Nhóm chúng em` riêng trong Lời cảm ơn). | Sửa khách quan |
| VP-011 | `chuong-05:57–71` | Dấu thập phân trong bảng & văn | Major | `s_fee = 1.0`, `0.5`, `avg_rating = 5.0`, `s_availability = 0.6667`, `S = 1.0` | Chuyển về dấu phẩy thập phân tiếng Việt (`1,0`, `0,5`, `5,0`, `0,6667`) khi viết dạng biểu thức tiếng Việt. | Sửa khách quan |
| VP-012 | `chuong-04:110,203,204,209,255` | Dấu `…` sót & lặp khẩu ngữ | Major | `n = 1…5`; `"…": "…"`; `"↓ Giảm 1 bậc…"`; lặp 4 lần `Mở ảnh thấy`; `200000` | Sửa `1–5`; bỏ cặp `"…": "…"` giả trong JSON; trích đủ nhãn `"↓ Giảm 1 bậc sau khi điều chỉnh mức ưu tiên (CN03)"`; đa dạng hóa mở đoạn Hình 4.1–4.4; sửa `200.000`. | Sửa khách quan |
| VP-013 | `chuong-06:32` | Câu cụt ý / văn phong nháp | Blocker | `Trích dẫn nguyên văn kết quả thử nghiệm... (tổng 19 ca có 3 ca biến động thứ hạng 2–3; ca được chọn sau khi thử 19 truy vấn).` | Viết lại thành văn xuôi học thuật hoàn chỉnh, giải thích rõ ca minh họa chọn sau 19 truy vấn và vai trò `KB10`. | Sửa khách quan |
| VP-014 | `chuong-06:191–215` | Văn phong checklist nháp (Phụ lục C) | Major | `Có thể lỗi thời`, `danh sách dưới đây ghi lại các ảnh cần chụp... Bốn mục đầu đã hoàn tất...`, `"Không quan trọng" hoặc "Bỏ qua"` | Biên tập lại thành danh mục lưu trữ lịch sử + hình ảnh chính thức; kiểm tra trực tiếp ảnh `hinh-3-cn03` xác nhận nhãn thật là `"Bỏ qua"` (`w = 0`). | Sửa khách quan |
| VP-015 | `chuong-01`–`06`, `muc-luc` | Câu >40 từ, dấu câu, nhất quán `khuyến nghị`/`gợi ý`, `Mục` viết hoa, `Tỉ lệ`/`Tỷ lệ`, công thức LaTeX `Ch2`/`Ch3`/`Ch4` | Minor | Câu ghép 60–110 từ (`chuong-01:46`, `chuong-03:105,160`, `chuong-04:243,249,267`, `chuong-05:290`); công thức thuần văn bản ở `chuong-02:37,39,53`; `Mục`/`mục` viết hoa không đều; `trong code`/`trong repo` | Tách câu dài xuống ≤35–40 từ, chuyển công thức Chương 2–4 sang LaTeX chuẩn `$...$`, thống nhất viết hoa `Mục`, `Phụ lục`, `Tỷ lệ`, đổi `trong code`/`repo` sang `trong mã nguồn`/`kho lưu trữ`. | Sửa khách quan |

---

## 2. Phần B — Rà soát Logic và Cấu trúc (`LG`)

### 2.1. Danh mục lỗi Logic & Cấu trúc

| ID | Vị trí | Loại | Mức | Mô tả vấn đề & chứng cứ | Hướng xử lý | Trạng thái |
|:---|:---|:---|:---:|:---|:---|:---|
| LG-001 | Toàn bộ báo cáo & `chuong-02:31` vs Đề cương v3 | Mâu thuẫn tên đề tài & phương pháp | Blocker | Đề cương v3 ghi `"dựa trên mức độ phù hợp đa tiêu chí"`; báo cáo ghi `"Content-Base Filtering"` (thiếu `-d`). Đặc biệt `chuong-02:31` viết *"đề tài không gọi phương pháp là Content-Based Filtering thuần túy"* — mâu thuẫn trực tiếp với tên đề tài trên bìa và Chương 1, 4, 5, 6. | **Cần người dùng chốt** (3 phương án ở Mục 4). | Chờ quyết định |
| LG-002 | `chuong-05:123–144` & `muc-luc:210–211` | Lặp toàn bộ bảng dữ liệu | Blocker | **Bảng 5.4** lặp nguyên xi 14 dòng Top-3 kỳ vọng, Top-3 hệ thống và `x/m` đã có trong **Bảng 5.3**, kèm câu dẫn thừa dấu ghép nối `"theo cấu trúc của Mục 5.2"`. Nếu bỏ Bảng 5.4, tổng số bảng toàn quyển đổi từ 31 thành 30. | **Cần người dùng chốt**: bỏ Bảng 5.4 (sửa thành 30 bảng) hay giữ Bảng 5.4 (chỉnh câu dẫn). | Chờ quyết định |
| LG-003 | `chuong-05:225` | Sai thuật ngữ toán học | Blocker | Viết `tính chất đơn điệu chặt chẽ` cho các hàm điểm có đoạn phẳng ($s_{\text{fee}} = 1$ khi $P \le B$, $s_{\text{exp}} = 1$ khi $E \ge E_{\max}$). | Sửa thành `tính đơn điệu (không giảm theo B, δ và không tăng theo E_max)`. | Sửa khách quan |
| LG-004 | `chuong-06:85` | Mâu thuẫn đánh giá & sai tên học phần | Blocker | Ghi `khóa luận` (đúng là `đồ án`) và `mức độ hoàn thành sẽ được tập thể nhóm và GVHD đánh giá` — mâu thuẫn với cột `Hoàn thành` trong Bảng 6.1 và dòng 95. | Sửa thành `đồ án` và ghi rõ mức độ hoàn thành là tự đánh giá của nhóm, chờ GVHD/hội đồng kết luận khi bảo vệ. | Sửa khách quan |
| LG-005 | `chuong-06:177` | Lỗi cú pháp bảng Markdown | Blocker | Dòng `backend/app/scoring/filters.py` chứa `$|L \cap T| \ge 1$` với ký tự `|` chưa thoát làm vỡ cột bảng B.1. | Sửa thành `$\lvert L \cap T \rvert \ge 1$`. | Sửa khách quan |
| LG-006 | `chuong-06:214` | Sai dẫn chiếu nội bộ | Blocker | Phụ lục C ghi `báo cáo dẫn liên kết tài liệu tương tác ở Mục 6.1.3`, nhưng Mục 6.1.3 chỉ có trang chủ frontend và `/health`, thiếu `/docs`. | Bổ sung đường dẫn `/docs` tại Mục 6.1.3 và dẫn chiếu chính xác về Mục 4.4.1, 4.6.3, 6.1.3. | Sửa khách quan |
| LG-007 | `chuong-06:215` | Sai cờ lệnh kiểm thử | Blocker | Ghi `pytest --coverage` (không tồn tại ở plugin `pytest-cov`). | Sửa thành `pytest --cov=app` khớp Chương 5 và `backend/requirements-dev.txt`. | Sửa khách quan |
| LG-008 | `chuong-06:20` | Phát biểu vượt chứng cứ (frontend) | Major | Khẳng định `đáp ứng trọn vẹn kịch bản kiểm thử trải nghiệm` trong khi Chương 4 (4.6.2, 4.7) xác nhận frontend chưa có kiểm thử tự động và chưa thử nghiệm người học thật. | Sửa thành `đáp ứng luồng minh họa thủ công ba chức năng CN01–CN03`. | Sửa khách quan |
| LG-009 | `chuong-05:250` | Phát biểu vượt chứng cứ | Major | Viết `chứng minh trọng số người dùng đã tác động chính xác` từ duy nhất một kịch bản KB01. | Hạ mức quy kết thành `minh họa tác động của trọng số đến thứ hạng đúng theo thiết kế`. | Sửa khách quan |
| LG-010 | `chuong-03:176` | Sai dẫn chiếu mục trong chú thích hình | Major | Chú thích Hình 3.2 ghi `(Mục 3.7.1)` trong khi Hình 3.2 thuộc `Mục 3.7.2. Kiến trúc ba lớp`. | Sửa thành `(Mục 3.7.2)`. | Sửa khách quan |
| LG-011 | `chuong-02:41` | Sai dẫn chiếu cấp chương/mục | Major | Viết `dữ liệu thực được dùng ở mục 5.` (Chương 2 không có mục 5). | Sửa thành `Chương 5`. | Sửa khách quan |
| LG-012 | `chuong-05:104,109,114,154` | Dẫn chiếu `Bảng 5.1` gây nhầm lẫn | Major | Gọi `Đề cương Bảng 5.1` bên trong Chương 5 nơi đã có `Bảng 5.1 - Phân bổ bộ kiểm thử tự động theo nhóm`. | Sửa thành `kỳ vọng trong đề cương (tương ứng tệp scenarios.json)` hoặc `kỳ vọng ban đầu của kịch bản`. | Sửa khách quan |
| LG-013 | `muc-luc:203–204` | Lệch tên bảng giữa danh mục và thân bài | Major | Tên Bảng 4.2 và 4.3 ở `muc-luc` bị rút ngắn khác với caption trong Chương 4. | Đồng bộ tên caption trong Mục 9 của `muc-luc` khớp nguyên văn thân bài. | Sửa khách quan |
| LG-014 | `chuong-06:88` | Đề mục con đơn độc | Major | `## 6.3` chỉ có duy nhất một mục con `### 6.3.1. Tự đánh giá kết quả thực hiện`. | Thêm `### 6.3.1. Phân công công việc` trước Bảng 6.1 và đổi mục tự đánh giá thành `### 6.3.2`. | Sửa khách quan |
| LG-015 | `tai-lieu-tham-khao.md:3–23` | Vi phạm quy chuẩn IEEE | Major | Thiếu in nghiêng tạp chí/sách/web; thiếu `, USA`; dấu `-` thay cho `–` ở dải trang; lẫn Title Case/Sentence case; lẫn `(truy cập ...)` tiếng Việt vào mục tiếng Anh; lẫn biệt danh `(Tiangolo)`; `[5]` dùng `and` trong tài liệu tiếng Việt. | Chuẩn hóa toàn bộ 11 mục theo đúng quy chuẩn IEEE. (Đã kiểm chứng trực tiếp qua Crossref/arXiv/URL: 11/11 nguồn có thật, thông tin khớp). | Sửa khách quan |
| LG-016 | `chuong-06:231,233,235,239` | Thuật ngữ tiếng Anh thô trong bảng | Minor | Bảng D.1 cột Hình thức ghi `any` xen lẫn `Trực tiếp`, `Trực tuyến`. | Đổi thành `Bất kỳ (any)` đồng nhất với Bảng 5.3. | Sửa khách quan |
| LG-017 | `muc-luc:174,177,181` | Thuật ngữ quy trình Scrum/Git trong danh mục viết tắt | Minor | Đưa `PR`, `SP`, `US` vào Danh mục viết tắt khi thân bài báo cáo chính thức không dùng các viết tắt này. | Loại bỏ `PR`, `SP`, `US` khỏi Danh mục viết tắt và sắp lại thứ tự chữ cái. | Sửa khách quan |

### 2.2. Bảng truy vết Mục tiêu (Ch1) ↔ Thiết kế/Hiện thực (Ch3–4) ↔ Kiểm chứng (Ch5) ↔ Kết luận (Ch6)

| Mục tiêu (Mục 1.4) | Thiết kế & Hiện thực (Ch3–Ch4) | Kiểm chứng (Ch5) | Kết luận (Ch6) | Tình trạng chuỗi logic |
|:---|:---|:---|:---|:---|
| Mục tiêu tổng quát: lọc bắt buộc + tổng hợp điểm có trọng số + giải thích | Mục 3.4, 3.6–3.8; Mục 4.3–4.6 | 200 bài test, 14/14 kịch bản, phân rã KB01 (Bảng 5.9) | Mục 6.1.1 & 6.3 | Đầy đủ |
| (a) Mô hình hóa mức độ phù hợp & module lọc – tính điểm | Bảng 3.2, 3.5–3.7; `backend/app/scoring/*.py` (Mục 4.3) | 132 unit test (84% cov đơn lẻ), Bảng 5.2 ca biên & đơn điệu | Mục 6.1.1(a) | Đạt sau khi sửa 97% → 84% ở Bảng 5.1 |
| (b) Dịch vụ API gợi ý FastAPI | Mục 3.7.2, Hình 3.2–3.3; `POST /api/recommend`, Bảng 4.4 (Mục 4.4) | 41 API test (93% cov đơn lẻ, 100% tầng API/Schemas); đo trễ TestClient | Mục 6.1.1(b), 6.1.3 | Số đo `3,54 ms` thiếu script benchmark tái lập (chờ chốt) |
| (c) Giao diện demo ReactJS | Mục 3.8, Hình 3.4–3.5; `SearchPage`, `ResultPage`, Hình 4.1–4.4 (Mục 4.5–4.6) | Chỉ kiểm tra thủ công + `oxlint`/`vite build` (không có test tự động frontend) | Mục 6.1.1(c) | Đạt sau khi sửa `React 18`→`19` và bỏ phóng đại kiểm thử trải nghiệm |
| (d) Đánh giá chất lượng & ảnh hưởng mức ưu tiên | `scenarios.json` (14 KB) + CN03 (Mục 4.5) | 27 scenario/sensitivity test; Bảng 5.3–5.9; khảo sát 4 yếu tố | Mục 6.1.1(d) | Đạt sau khi sửa `"5 nhóm tham số"` → `"4 yếu tố"` và xử lý Bảng 5.4 |
| Kiểm tra đủ 4 hạn chế bắt buộc | Đã nêu dữ liệu hỗn hợp & giới hạn hiện thực ở Mục 4.2.3, 4.7 | Mục 5.3 nêu đủ: mẫu nhỏ 16 hồ sơ, chưa có đánh giá thật, nhãn `public_collected` và 2 trường ước tính `(*)` của `GS-T06/T07` | Mục 6.2.1 tổng hợp lại (rút gọn để tránh lặp) | Đầy đủ |

### 2.3. Kiểm chứng Tài liệu tham khảo (`tai-lieu-tham-khao.md`)
- Cả 11 mục `[1]`–`[11]` đều được trích dẫn trong Chương 1–2 theo đúng thứ tự tăng dần từ `1` đến `11`; không có mục dư, không có trích dẫn gãy.
- Xác minh thực tế qua Crossref API, arXiv và HTTP trực tiếp: `[1]` (Elsevier 2003, Bray & Kwok), `[2]` (Springer 2000, Triantaphyllou), `[3]` (Hindawi 2009, Su & Khoshgoftaar), `[4]` (arXiv:1804.11192, Zhang & Chen), `[5]` (Scribd GS360, HTTP 200), `[6]` (IEEE TKDE 2005, Adomavicius & Tuzhilin), `[7]` (arXiv:1812.08947, Qin et al.), `[8]` (Cambridge 2008, Manning et al.), `[9]` (Operations Research 1967, Fishburn), `[10]` (FastAPI docs, HTTP 200), `[11]` (React docs, HTTP 200) — **11/11 nguồn xác thực, đúng tác giả và năm xuất bản**.

---

## 3. Phần C — Rà soát Số liệu bằng Chứng cứ Chạy được (`SL`)

Bảng đối chiếu đầy đủ **74 claim** được lưu tại `docs/thesis/review/so-lieu-doi-chieu.csv`. Tổng hợp kết quả chạy lại trực tiếp trên mã nguồn: **67/74 claim khớp 100%** (bao gồm toàn bộ Top-3 và điểm số 14 kịch bản KB01–KB14, độ nhạy $\delta$, $E_{\max}$, ngân sách, 4 bộ ưu tiên, phân rã KB01, 16 hồ sơ Phụ lục A, 16 quận/huyện, 13 phiên bản thư viện Bảng 4.1, 200 bài test theo từng tệp, độ bao phủ tổng 340/351 = 97%, và khảo sát 19 truy vấn Chương 6).

**7 claim phát hiện sai lệch (`LỆCH`):**

| ID | Vị trí | Giá trị trong báo cáo | Giá trị tính lại từ mã nguồn / dữ liệu | Mức | Xử lý |
|:---|:---|:---|:---|:---:|:---|
| SL-001 | `chuong-06:20` | `React 18` | `React 19.3.1` (`frontend/package-lock.json`, Chương 4) | Blocker | Sửa khách quan → `React 19` |
| SL-002 | `chuong-05:26` | Bảng 5.1 hàng Unit Tests ghi độ bao phủ `97%` | Chạy `pytest tests/unit tests/test_environment.py --cov=app`: **84%** (294/351 câu lệnh, 57 chưa phủ). `97%` là độ bao phủ tổng hợp cả 200 bài. | Blocker | Sửa khách quan → `84% (riêng unit)` và `97% (340/351)` ở tổng |
| SL-003 | `chuong-05:86` | `time_slots = []` xuất hiện ở `11/14 kịch bản` | Đếm trực tiếp trong `scenarios.json`: **12/14 kịch bản** (`KB01–03, KB05–07, KB09–14`; chỉ `KB04, KB08` có lịch rảnh). | Blocker | Sửa khách quan → `12/14 kịch bản` |
| SL-004 | `chuong-06:21` | `5 nhóm tham số tại Mục 5.2 (Bảng 5.4–5.9)` | Mục 5.2 khảo sát **4 yếu tố** (`\delta`, `E_max`, ngân sách, bộ mức ưu tiên) tại Bảng 5.5–5.8. | Blocker | Sửa khách quan → `4 yếu tố` |
| SL-005 | `chuong-06:30, 210` | Tên 3 preset: `Mặc định`, `Luyện thi điểm cao / học chuyên`, `Đậu tốt nghiệp / lấy lại căn bản` | `frontend/src/data/goalPresets.js`: `Không nêu mục tiêu`, `Điểm cao / luyện thi chuyên – học sinh giỏi`, `Đủ điểm đậu / lấy lại kiến thức căn bản`. | Blocker | Sửa khách quan theo `goalPresets.js` |
| SL-006 | `muc-5.1:49`, `discrepancy_analysis.md:23` | Điểm `GS-G04` (KB06) ghi `0,934375` (`7,475 / 8`) | Tính lại từ pipeline & công thức: $2 \times (1 + 1 + 0{,}875 + 0{,}86) / 8 = 7{,}47 / 8 = \mathbf{0{,}93375}$ (Chương 5 dòng 111 đã đúng). | Major | Sửa khách quan trong tài liệu trung gian |
| SL-007 | `chuong-05:44`, `chuong-06:19,41`, `muc-luc:93,103` | `3,54 ms` (max `7,97 ms`, 140 lượt) và `3,72 ms` (max `26,64 ms`, 700 lượt) | **Không có script benchmark lưu trong repo** để tái lập chính xác cùng phần cứng. Đo kiểm chứng bằng `TestClient` trên máy hiện tại cho kết quả cùng bậc độ lớn: 140 lượt TB `4,06 ms` (max `15,67 ms`); 700 lượt TB `3,69 ms` (max `27,82 ms`). | Major | **Chờ người dùng chốt** (bổ sung script benchmark mới hay giữ số phiên đo gốc kèm ghi chú) |

---

## 4. Kết luận cổng chất lượng (Task 5)

1. **Các lỗi khách quan có chứng cứ** (`VP-001`–`VP-015`, `LG-003`–`LG-017`, `SL-001`–`SL-006`) **đã được sửa trực tiếp** trên nhánh `docs/ra-soat-ghep-bao-cao` (các commit `cc0b918`..HEAD). Kiểm chứng lại bằng `check_captions.py` cho kết quả `OK 31 tables, 9 figures, 0 broken refs`; `recompute_numbers.py` đạt **73/74 claim khớp 100%** (duy nhất `SL-CH5-LATENCY` chờ quyết định); bộ test `backend/` đạt **200/200 passed**.
2. **Các điểm cần phán đoán (DỪNG VÀ HỎI NGƯỜI DÙNG trước khi sang Giai đoạn B convert DOCX):**
   - **Q1 — Tên đề tài & Chương 2 (Blocker `LG-001`):** Đề cương v3 ghi *"dựa trên mức độ phù hợp đa tiêu chí"*; báo cáo ghi *"Content-Base Filtering"* (thiếu `-d`), trong khi Chương 2 dòng 31 lại viết *"đề tài không gọi phương pháp là Content-Based Filtering thuần túy"*. Bạn chọn: **(a)** giữ `"Content-Base Filtering"` theo đăng ký và viết lại Chương 2 dòng 31 cho khớp, **(b)** sửa thành `"Content-Based Filtering"` ở cả bìa và toàn bài, hay **(c)** quay về tên Đề cương v3?
   - **Q2 — Bảng 5.4 trùng lặp Bảng 5.3 (Blocker `LG-002`):** Bạn muốn **gộp bỏ Bảng 5.4** (đánh số lại thành Bảng 5.4–5.8, tổng toàn quyển còn 30 bảng) hay **giữ nguyên 31 bảng** (chỉnh lại lời dẫn ở Bảng 5.4)?
   - **Q3 — Số liệu độ trễ `3,54 ms` không có script benchmark tái lập (Major `SL-007`):** Bạn muốn **giữ số liệu phiên đo gốc** (`3,54 ms` / `3,72 ms`) và ghi chú rõ đây là kết quả chạy `TestClient` thủ công (hoặc bổ sung script benchmark tái lập và cập nhật theo số đo tái lập trên máy)?
   - **Q4 — Chuẩn bị Giai đoạn B (DOCX):** (a) Xác nhận cài `pypandoc_binary` vào môi trường Python; (b) Dòng bìa giữ `"BÁO CÁO ĐỒ ÁN KHOA HỌC MÁY TÍNH 1"` hay đổi `"BÁO CÁO ĐỒ ÁN TỐT NGHIỆP"`; (c) Thân bài Chương 4–6 giữ nguyên đường dẫn tệp mã nguồn để hội đồng tra cứu hay chuyển bớt vào ghi chú?
