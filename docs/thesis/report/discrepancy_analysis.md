# Phân tích đối chiếu kết quả thực nghiệm 14 kịch bản (KB01–KB14)

- **Mục tương ứng trong đề cương:** Mục 5.1 (Kịch bản kiểm thử), Mục 5.2 (Phân tích kết quả thực nghiệm), Bảng 5.1.
- **Thuộc User Story:** US-18 (Issue #20) — Phân tích và điều tra nguyên nhân các trường hợp lệch giữa kết quả hệ thống và kỳ vọng thủ công.
- **Dữ liệu đầu vào:** `data/processed/tutors.json` (16 hồ sơ chuẩn hóa từ Phụ lục A) và `backend/tests/scenarios/scenarios.json` (14 kịch bản `KB01`–`KB14` từ Bảng 5.1, khóa bất biến).

---

## 1. Bảng tổng hợp đối chiếu 14 kịch bản thực nghiệm

Quy ước chấm khớp theo `backend/tests/scenarios/README.md`:
- Khi Top-3 kỳ vọng có $m$ gia sư ($1 \le m \le 3$), tỷ lệ trùng khớp được tính theo dạng $x/m$.
- Kịch bản `KB05` kiểm tra trường hợp không có ứng viên thỏa điều kiện bắt buộc (`no_match`, danh sách rỗng `[]`).
- Các ứng viên đồng hạng trong kỳ vọng (`KB02`, `KB12`) được xem là hoán đổi được; hệ thống phá hòa tất định theo mã hồ sơ `tutor_id` tăng dần.

| Mã KB | Mục tiêu kiểm thử (theo `scenarios.json`) | Số ứng viên qua lọc | `expected_top3` (Bảng 5.1) | Top-3 hệ thống | Điểm hệ thống $S(g)$ | `expected_raw` trong Bảng 5.1 | Độ khớp | Ghi chú đối chiếu |
|:---:|:---|:---:|:---|:---|:---|:---|:---:|:---|
| **KB01** | Toán, trực tiếp, Bình Thạnh, ngân sách 200.000đ (có `GS-T06` chưa có đánh giá) | 5 | `GS-G01`, `GS-G10`, `GS-T06` | `GS-G01`, `GS-G10`, `GS-T06` | `0,938`; `0,745`; `0,625` | `1. GS-G01 (0,938) 2. GS-G10 (0,745) 3. GS-T06 (0,625)` | **3/3** | Khớp tuyệt đối thứ hạng và điểm; `GS-T06` nhận `s_rating = 0,5` |
| **KB02** | Anh Văn, trực tiếp, Quận 2, ngân sách 220.000đ (đồng hạng 1–2 `GS-G11` và `GS-G12`) | 3 | `GS-G11`, `GS-G12`, `GS-T07` | `GS-G11`, `GS-G12`, `GS-T07` | `0,881`; `0,881`; `0,5625` | `1–2. GS-G11 = GS-G12 (0,881, đồng hạng) 3. GS-T07 (0,5625)` | **3/3** | Đồng điểm `7,05/8 = 0,88125`; phá hòa `GS-G11` trước `GS-G12` |
| **KB03** | Anh Văn, trực tiếp, Thủ Đức, ngân sách 220.000đ (tách đồng hạng `GS-G12` và `GS-G11`) | 3 | `GS-G12`, `GS-G11`, `GS-T07` | `GS-G12`, `GS-G11`, `GS-T07` | `0,881`; `0,631`; `0,5625` | `1. GS-G12 (0,881) 2. GS-G11 (0,631) 3. GS-T07 (0,5625)` | **3/3** | Khớp tuyệt đối thứ hạng và điểm |
| **KB04** | Lý, trực tuyến (`online`), ngân sách 200.000đ, khung giờ `T2-tối`, `T4-tối` | 2 | `GS006`, `GS020` | `GS006`, `GS020` | `0,886`; `0,786` | `1. GS006 (0,848) 2. GS020 (0,715)` | **2/2** | **Khớp thứ hạng 2/2; lệch giá trị điểm số** (xem Mục 3.1) |
| **KB05** | Tiếng Trung, hình thức `any` — không có ứng viên thỏa điều kiện bắt buộc | 0 | `[]` | `[]` (`no_match`) | *(không có)* | `(không có)` | **Đạt** | Bộ lọc bắt buộc trả về `[]` đúng kỳ vọng |
| **KB06** | Văn, trực tiếp, Quận 1, ngân sách 180.000đ (môn hiếm 1 ứng viên) | 1 | `GS-G04` | `GS-G04` | `0,934` | `1. GS-G04 (0,934)` | **1/1** | Khớp tuyệt đối (`7,475 / 8 = 0,934375`) |
| **KB07** | Sinh, hình thức `any`, Thủ Đức, ngân sách 200.000đ (môn hiếm 1 ứng viên) | 1 | `GS-G05` | `GS-G05` | `0,825` | `1. GS-G05 (0,825)` | **1/1** | Khớp tuyệt đối (`6,60 / 8 = 0,825`) |
| **KB08** | Tin học, trực tuyến (`online`), ngân sách 250.000đ, khung giờ `T2-tối`, `T6-tối` | 1 | `GS-G07` | `GS-G07` | `0,876` | `1. GS-G07 (0,876)` | **1/1** | Khớp tuyệt đối (`7,01 / 8 = 0,87625`) |
| **KB09** | Tiếng Nhật, hình thức `any`, Phú Nhuận, ngân sách 280.000đ | 1 | `GS-G08` | `GS-G08` | `0,9275` | `1. GS-G08 (0,928)` | **1/1** | Khớp thứ hạng 1/1; chênh `0,0005` do quy tắc làm tròn (xem Mục 3.2) |
| **KB10** | Toán, trực tiếp, Quận 7, không nhập ngân sách, ưu tiên Kinh nghiệm Cao | 5 | `GS-G10`, `GS-G01`, `GS-G09` | `GS-G10`, `GS-G01`, `GS-G09` | `0,994`; `0,607`; `0,593` | `1. GS-G10 (0,994) 2. GS-G01 (0,607) 3. GS-G09 (0,593)` | **3/3** | Khớp tuyệt đối thứ hạng và điểm |
| **KB11** | Hóa, trực tiếp, Quận 10, ngân sách 220.000đ (2 ứng viên `GS-G06` và `GS-T06`) | 2 | `GS-G06`, `GS-T06` | `GS-G06`, `GS-T06` | `0,985`; `0,375` | `1. GS-G06 (0,985) 2. GS-T06 (0,375)` | **2/2** | Khớp tuyệt đối thứ hạng và điểm (`s_fee(GS-T06) = 0`) |
| **KB12** | Anh Văn, trực tiếp, Bình Chánh, ngân sách 200.000đ (`GS-T07` hạng 1, đồng hạng 2–3) | 3 | `GS-T07`, `GS-G11`, `GS-G12` | `GS-T07`, `GS-G11`, `GS-G12` | `0,8125`; `0,631`; `0,631` | `1. GS-T07 (0,8125) 2–3. GS-G11 = GS-G12 (0,631, đồng hạng)` | **3/3** | Đồng điểm hạng 2–3 (`5,05/8 = 0,63125`); phá hòa `GS-G11` trước `GS-G12` |
| **KB13** | Toán, hình thức `any`, ngân sách 150.000đ, không nhập khu vực và khung giờ | 5 | `GS-G10`, `GS-G01`, `GS-T06` | `GS-G10`, `GS-G01`, `GS-T06` | `0,993`; `0,783`; `0,500` | `1. GS-G10 (0,993) 2. GS-G01 (0,783) 3. GS-T06 (0,50)` | **3/3** | Khớp tuyệt đối thứ hạng và điểm |
| **KB14** | Anh Văn, trực tuyến (`online`), không nhập ngân sách/khu vực/khung giờ | 1 | `GS-G03` | `GS-G03` | `0,700` | `1. GS-G03 (0,70)` | **1/1** | Khớp tuyệt đối sau khi đồng bộ nhãn môn `GS-G03` ở PR #48 |

---

## 2. Đánh giá tổng quan độ trùng khớp

- **Về thứ hạng gợi ý (`expected_top3`):** Hệ thống đạt độ trùng khớp **14/14 kịch bản (100%)** so với `expected_top3` trong `scenarios.json`. Không có bất kỳ kịch bản nào bị đảo thứ hạng hoặc lọt ứng viên ngoài danh sách kỳ vọng.
- **Về kiểm tra ngưỡng dữ liệu tối thiểu (Mục 3.6):** Cả 16 hồ sơ trong `data/processed/tutors.json` đều có dữ liệu đầy đủ cho các tiêu chí đang áp dụng trong từng kịch bản, do đó không có ứng viên nào qua lọc bắt buộc bị loại ở bước kiểm tra ngưỡng dữ liệu (`insufficient_data_candidates = []` trên cả 14 kịch bản). Hai hồ sơ thu thập công khai (`GS-T06`, `GS-T07`) có `avg_rating = null` được gán điểm đánh giá trung tính `0,5` kèm ghi chú `"chưa có đánh giá"` đúng theo Mục 6.5 của `scoring-spec.md`.
- **Về điểm số chi tiết (`expected_raw`):** Có **2 kịch bản** xuất hiện khác biệt nhỏ về con số thập phân giữa kết quả hệ thống và chuỗi `expected_raw` tính tay trong Bảng 5.1 (`KB04` và `KB09`), nhưng **không làm thay đổi thứ hạng**. Nguyên nhân toán học được phân tích chi tiết ở Mục 3 dưới đây.

---

## 3. Phân tích toán học chi tiết các trường hợp khác biệt số liệu

### 3.1. Kịch bản KB04 — Học trực tuyến (`online`), loại bỏ tiêu chí Khu vực

- **Cấu hình truy vấn `KB04` trong `scenarios.json`:**
  - `subject = "Lý"`, `learning_mode = "online"`, `max_budget_vnd = 200000`, `time_slots = ["T2-tối", "T4-tối"]`.
  - Mức ưu tiên: cả 5 tiêu chí đều là `"medium"` ($w = 2$).
- **Ứng viên vượt qua lọc bắt buộc:** `GS006` và `GS020` (đều dạy môn Lý, hình thức `online`, và có lịch rảnh chứa cả `["T2-tối", "T4-tối"]`).
- **Điểm thành phần $s_i$ của hai ứng viên:**
  - `GS006` (`hourly_fee_vnd = 190000`, `years_experience = 5`, `avg_rating = 4.6`, `availability = ["T2-tối", "T3-tối", "T4-tối", "T5-tối"]`):
    - $s_{\text{fee}} = 1{,}000$ (vì $190\,000 \le 200\,000$)
    - $s_{\text{experience}} = \min(5 / 8, 1) = 0{,}625$
    - $s_{\text{rating}} = 4{,}6 / 5 = 0{,}920$
    - $s_{\text{availability}} = 2 / 2 = 1{,}000$
  - `GS020` (`hourly_fee_vnd = 240000`, `years_experience = 5`, `avg_rating = 4.6`, `availability = ["T2-tối", "T3-tối", "T4-tối", "T5-tối"]`):
    - $s_{\text{fee}} = 1 - \frac{240\,000 - 200\,000}{0{,}5 \times 200\,000} = 1 - 0{,}4 = 0{,}600$
    - $s_{\text{experience}} = 5 / 8 = 0{,}625$
    - $s_{\text{rating}} = 4{,}6 / 5 = 0{,}920$
    - $s_{\text{availability}} = 2 / 2 = 1{,}000$

- **Nguyên nhân lệch điểm giữa hệ thống và `expected_raw`:**
  1. **Cách tính của hệ thống (áp dụng đúng Mục 6.1 của `scoring-spec.md`):** Khi `learning_mode = "online"`, chỉ riêng tiêu chí `district` bị loại. Vì truy vấn `KB04` có truyền `time_slots = ["T2-tối", "T4-tối"]`, có **4 tiêu chí áp dụng** gồm `fee`, `experience`, `rating`, `availability` với tổng trọng số $\sum w_i = 2 + 2 + 2 + 2 = 8$:
     $$S(\text{GS006}) = \frac{2 \times 1{,}0 + 2 \times 0{,}625 + 2 \times 0{,}92 + 2 \times 1{,}0}{8} = \frac{7{,}09}{8} = 0{,}88625 \approx 0{,}886$$
     $$S(\text{GS020}) = \frac{2 \times 0{,}6 + 2 \times 0{,}625 + 2 \times 0{,}92 + 2 \times 1{,}0}{8} = \frac{6{,}29}{8} = 0{,}78625 \approx 0{,}786$$
  2. **Cách tính tay trong `expected_raw` của Bảng 5.1 (`0,848` và `0,715`):** Khi tính nháp thủ công cho Bảng 5.1, người tính chỉ cộng 3 tiêu chí (`fee`, `experience`, `rating`) với tổng trọng số $\sum w_i = 6$ (bỏ sót tiêu chí `availability` trong công thức tổng hợp dù đã dùng `time_slots` để lọc ứng viên):
     $$S_{\text{tính tay}}(\text{GS006}) = \frac{2 \times 1{,}0 + 2 \times 0{,}625 + 2 \times 0{,}92}{6} = \frac{5{,}09}{6} = 0{,}848333\ldots \approx 0{,}848$$
     $$S_{\text{tính tay}}(\text{GS020}) = \frac{2 \times 0{,}6 + 2 \times 0{,}625 + 2 \times 0{,}92}{6} = \frac{4{,}29}{6} = 0{,}715000 = 0{,}715$$
  3. **Tác động lên kết quả xếp hạng:** Vì cả hai ứng viên đều có $s_{\text{availability}} = 1{,}0$, việc tính đủ 4 tiêu chí chỉ dịch chuyển đồng thời điểm của cả hai ứng viên về phía $1{,}0$ mà **giữ nguyên hoàn toàn thứ tự xếp hạng** (`1. GS006`, `2. GS020`). Theo quy ước tại PR #49 và `backend/tests/scenarios/README.md`, nhóm giữ nguyên `expected_raw` trong `scenarios.json` và ghi nhận giải thích toán học này vào báo cáo thực nghiệm.

### 3.2. Kịch bản KB09 — Không nhập khung giờ (`time_slots` để trống)

- **Phân tích điểm của `GS-G08` (`hourly_fee_vnd = 260000 <= 280000`, `districts = ["Phú Nhuận", "Tân Bình"]`, `years_experience = 6`, `avg_rating = 4.8`):**
  - 4 tiêu chí áp dụng (`fee`, `district`, `experience`, `rating`), mỗi tiêu chí có $w_i = 2 \Rightarrow \sum w_i = 8$.
  - Điểm thành phần: $s_{\text{fee}} = 1{,}0$; $s_{\text{district}} = 1{,}0$; $s_{\text{experience}} = 6/8 = 0{,}75$; $s_{\text{rating}} = 4{,}8/5 = 0{,}96$.
  - Điểm tổng hợp chính xác:
    $$S(\text{GS-G08}) = \frac{2 \times (1{,}0 + 1{,}0 + 0{,}75 + 0{,}96)}{8} = \frac{3{,}71}{4} = 0{,}9275$$
- **Nguyên nhân khác biệt chữ số thập phân thứ 3 (`0,927` vs `0,928`):**
  - Giá trị chính xác $0{,}9275$ nằm đúng chính giữa $0{,}927$ và $0{,}928$.
  - Khi tính tay trong Bảng 5.1 theo quy tắc làm tròn nửa lên (*round half up*), $0{,}9275 \to 0{,}928$.
  - Trong chuẩn số thực dấu phẩy động IEEE-754 và hàm `round(x, 3)` của Python (*round half to even*), biểu diễn nhị phân của `0.9275` xấp xỉ `0.927499999999999991118...` nên làm tròn thành `0.927`. Hệ thống giữ nguyên số thực `0.9275` không làm tròn trung gian đúng theo QĐ-E và `api-contract.md` mục 5.2.

### 3.3. Kịch bản đồng điểm KB02 và KB12 — Xác minh cơ chế phá hòa (Tie-breaker)

- **Tại KB02 (`preferred_district = "Quận 2"`, `max_budget_vnd = 220000`, không truyền `time_slots`):**
  - 4 tiêu chí áp dụng (`fee`, `district`, `experience`, `rating`), mỗi tiêu chí có $w_i = 2 \Rightarrow \sum w_i = 8$.
  - `GS-G11` (`districts = ["Quận 2", "Bình Thạnh"]`) và `GS-G12` (`districts = ["Quận 2", "Thủ Đức"]`) đều có `hourly_fee_vnd = 200000 <= 220000` ($s_{\text{fee}} = 1{,}0$), đều khớp `Quận 2` ($s_{\text{district}} = 1{,}0$), cùng `years_experience = 5` ($s_{\text{experience}} = 0{,}625$) và cùng `avg_rating = 4.5` ($s_{\text{rating}} = 0{,}90$).
  - Điểm tổng của cả hai bằng nhau tuyệt đối:
    $$S(\text{GS-G11}) = S(\text{GS-G12}) = \frac{2 \times (1{,}0 + 1{,}0 + 0{,}625 + 0{,}90)}{8} = \frac{7{,}05}{8} = 0{,}88125 \approx 0{,}881$$
  - Bộ xếp hạng `score_and_rank` sắp xếp theo khóa `(-total_score, tutor_id)`, đưa `"GS-G11"` đứng hạng 1 và `"GS-G12"` đứng hạng 2 một cách tất định.
- **Tại KB12 (`preferred_district = "Bình Chánh"`, `max_budget_vnd = 200000`, không truyền `time_slots`):**
  - `GS-T07` khớp `Bình Chánh` ($s_{\text{district}} = 1{,}0$), học phí `190000 <= 200000` ($s_{\text{fee}} = 1{,}0$), kinh nghiệm 6 năm ($s_{\text{experience}} = 0{,}75$), chưa có đánh giá ($s_{\text{rating}} = 0{,}5$), đạt điểm hạng 1 là $\frac{2 \times (1{,}0 + 1{,}0 + 0{,}75 + 0{,}5)}{8} = 0{,}8125$.
  - `GS-G11` và `GS-G12` đều không khớp `Bình Chánh` ($s_{\text{district}} = 0{,}0$), đạt cùng điểm:
    $$S(\text{GS-G11}) = S(\text{GS-G12}) = \frac{2 \times (1{,}0 + 0{,}0 + 0{,}625 + 0{,}90)}{8} = \frac{5{,}05}{8} = 0{,}63125 \approx 0{,}631$$
  - Hai ứng viên đồng điểm hạng 2–3 được phá hòa ổn định theo thứ tự từ điển `"GS-G11"` trước `"GS-G12"`.

---

## 4. Kết luận phục vụ Chương 5 khóa luận

1. Thuật toán lọc bắt buộc, quy đổi trọng số, kiểm tra ngưỡng dữ liệu và xếp hạng Weighted Scoring hoạt động chính xác trên toàn bộ 14 kịch bản thực nghiệm Bảng 5.1, đạt tỷ lệ trùng khớp Top-3 là **14/14 (100%)**.
2. Không có sự đánh đổi hay mâu thuẫn nào giữa công thức chuẩn hóa Bảng 3.6 và kết quả xếp hạng thực tế trên tập 16 hồ sơ chuẩn hóa.
3. Hai điểm khác biệt nhỏ về con số hiển thị tại `KB04` (do phép tính tay trong đề cương lược bỏ tiêu chí `availability`) và `KB09` (do quy tắc làm tròn tại chữ số thập phân thứ 4 là `5`) đã được chứng minh tường minh bằng công thức toán học mà **không chỉnh sửa ngược dữ liệu kỳ vọng trong `scenarios.json`**.
