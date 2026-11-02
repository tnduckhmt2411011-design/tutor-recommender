> [!NOTE]
> **Đề xuất, nhóm xác nhận**

# Báo cáo khóa thiết kế bài toán và công thức chấm điểm (Sprint 1 — US-05)

- **Đề tài:** Hệ thống khuyến nghị gia sư dựa trên mức độ phù hợp đa tiêu chí
- **Giảng viên hướng dẫn:** TS. Lê Anh Nhã Uyên
- **Nhóm sinh viên thực hiện:** Cao Khánh Ngọc (KHMT2411025 — PO), Trần Nguyễn Đức (KHMT2411011 — SM/Dev), Lê Thị Bích Chuyền (KHMT2411037 — SM/Dev)
- **Phạm vi khóa thiết kế:** Mục 1.4, Mục 1.5 và Chương 3 (Mục 3.1–3.6) trong đề cương đồ án

---

## 1. Phát biểu bài toán (Mục 3.1)

- **Tác nhân duy nhất:** “Người học” (học sinh hoặc phụ huynh thay mặt học sinh). Không có tác nhân quản trị hay tác nhân hệ thống ngoài.
- **Đầu vào:** Nhu cầu của người học gồm:
  - Môn học cần tìm (bắt buộc, mỗi lần tìm xử lý một môn học),
  - Hình thức học (`Trực tiếp` / `Trực tuyến` / `Không yêu cầu`),
  - Khu vực mong muốn (tùy chọn),
  - Ngân sách tối đa theo giờ (VNĐ, tùy chọn),
  - Tập khung thời gian rảnh trong tuần (tùy chọn),
  - Mức ưu tiên cho 5 tiêu chí (`Không quan tâm` = 0, `Thấp` = 1, `Trung bình` = 2, `Cao` = 3; mặc định `Trung bình`).
- **Đầu ra:** Danh sách Top-$k$ gia sư thỏa các điều kiện bắt buộc, xếp hạng giảm dần theo điểm phù hợp tổng hợp $S$ (đồng điểm xếp theo mã gia sư tăng dần), kèm điểm thành phần $s_i$, tỷ lệ đóng góp $C_i$ của từng tiêu chí và lý do gợi ý. Trường hợp không có gia sư nào thỏa điều kiện bắt buộc hoặc tổng trọng số bằng 0, hệ thống trả thông báo rõ ràng thay vì trả danh sách rỗng không giải thích.

---

## 2. Ba chức năng cốt lõi của hệ thống (Bảng 3.1)

| Mã | Tên chức năng | Mô tả |
|:---:|:---|:---|
| **CN01** | Nhập nhu cầu và mức ưu tiên | Người học nhập môn học, hình thức học, khu vực, ngân sách, khung thời gian rảnh và chọn mức ưu tiên cho từng tiêu chí. |
| **CN02** | Xem danh sách gợi ý kèm điểm | Hệ thống trả về Top-$k$ gia sư xếp hạng theo điểm phù hợp, kèm điểm từng tiêu chí thành phần và lý do gợi ý; thông báo rõ khi không có gia sư thỏa điều kiện bắt buộc. |
| **CN03** | Điều chỉnh mức ưu tiên minh họa | Người học thay đổi mức ưu tiên của từng tiêu chí và quan sát danh sách xếp hạng lại tương ứng — điểm nhấn thực nghiệm của đồ án. |

---

## 3. Phân loại tiêu chí và quy tắc xử lý (Bảng 3.2)

| Tiêu chí | Loại | Cách xử lý | Lý do |
|:---|:---|:---|:---|
| **Môn học** | Bắt buộc | Người học chọn một môn mỗi lần tìm; gia sư phải dạy môn đó (`subject in tutor.subjects`). | Sai môn thì không có giá trị, dù điểm khác cao. |
| **Hình thức học** | Bắt buộc có điều kiện | Nếu chọn `Trực tiếp` hoặc `Trực tuyến`: gia sư phải dạy hình thức đó (gia sư `Cả hai` thỏa cả hai). Nếu chọn `Không yêu cầu`: không lọc. | Hình thức không tương thích thì không học được. |
| **Khung giờ rảnh** | Bắt buộc có điều kiện + Ưu tiên | Nếu người học nhập khung giờ $L$: phải có ít nhất một khung giờ giao nhau ($\lvert L \cap T \rvert \ge 1$) ở bước lọc; số khung giờ giao càng nhiều điểm càng cao ở bước chấm điểm. | Không có giờ chung thì không thể học. |
| **Học phí** | Ưu tiên (ngân sách mềm) | Học phí không vượt ngân sách: điểm tối đa; vượt thì điểm giảm dần về 0 khi vượt 50% ngân sách, không loại ngay. | Cho phép chấp nhận vượt nhẹ nếu gia sư tốt (theo động lực Mục 1.1). |
| **Khu vực** | Ưu tiên | Chỉ áp dụng khi chọn `Trực tiếp` hoặc `Không yêu cầu` hình thức và có nhập khu vực; nếu học `Trực tuyến` hoặc không nhập khu vực thì không áp dụng. | Học trực tuyến không phụ thuộc vị trí địa lý. |
| **Kinh nghiệm** | Ưu tiên | Càng nhiều năm càng tốt, có mức trần $E_{\max} = 8$; người học không nhập yêu cầu tối thiểu. | Giữ đầu vào đơn giản. |
| **Điểm đánh giá** | Ưu tiên | Điểm trung bình càng cao càng tốt; nếu chưa có đánh giá thì dùng giá trị trung tính $0,5$. | Giữ đầu vào đơn giản, không phạt nặng gia sư mới. |

---

## 4. Công thức tính điểm thành phần $s_i \in [0, 1]$ (Bảng 3.6) và gộp trọng số (Bảng 3.5)

### 4.1. Bảng quy đổi mức ưu tiên sang trọng số (Bảng 3.5)

| Mức ưu tiên | Khóa hệ thống | Trọng số $w_i$ |
|:---|:---:|:---:|
| Không quan tâm | `none` | 0 |
| Thấp | `low` | 1 |
| Trung bình (mặc định) | `medium` | 2 |
| Cao | `high` | 3 |

### 4.2. Năm công thức điểm thành phần (Bảng 3.6)

| Tiêu chí | Đầu vào | Công thức điểm $s_i$ | Tham số | Ví dụ minh họa |
|:---|:---|:---|:---|:---|
| **Học phí** | $P$: học phí gia sư; $B$: ngân sách | $s = 1$ nếu $P \le B$; $s = \max\left(0, 1 - \frac{P - B}{\delta \times B}\right)$ nếu $P > B$ | $\delta = 0,5$ | Với $B = 200.000$: $P = 180.000 \rightarrow 1,00$; $P = 230.000 \rightarrow 0,70$; $P = 300.000 \rightarrow 0,00$ |
| **Khu vực** | $K$: khu vực người học; tập khu vực của gia sư | $s = 1$ nếu $K$ thuộc khu vực dạy của gia sư; ngược lại $s = 0$ | Bỏ qua nếu học `Trực tuyến` hoặc không nhập $K$ | Với $K = \text{KV1}$: dạy $\{\text{KV1}, \text{KV2}\} \rightarrow 1$; dạy $\{\text{KV3}\} \rightarrow 0$; chỉ trực tuyến $\rightarrow 0$ |
| **Kinh nghiệm** | $E$: số năm kinh nghiệm | $s = \min\left(\frac{E}{E_{\max}}, 1\right)$ | $E_{\max} = 8$ | $E = 0 \rightarrow 0,00$; $E = 4 \rightarrow 0,50$; $E = 10 \rightarrow 1,00$ |
| **Đánh giá** | $R$: điểm trung bình (thang 5) | $s = \frac{R}{5}$; nếu chưa có đánh giá thì $s = 0,5$ | Giá trị trung tính $0,5$ | $R = 5 \rightarrow 1,00$; $R = 4,5 \rightarrow 0,90$; $R = 3 \rightarrow 0,60$ |
| **Lịch rảnh** | $L$: khung giờ người học; $T$: khung giờ gia sư | $s = \frac{\lvert L \cap T \rvert}{\lvert L \rvert}$ (bước lọc đã đảm bảo $\lvert L \cap T \rvert \ge 1$) | Bỏ qua nếu không nhập $L$ | Giao $2/3 \rightarrow \approx 0,67$; giao $6/7 \rightarrow \approx 0,857$; giao $1/4 \rightarrow 0,25$ |

### 4.3. Công thức điểm tổng hợp và tỷ lệ đóng góp

$$S = \frac{\sum_{i=1}^{m} w_i \times s_i}{\sum_{i=1}^{m} w_i}, \qquad C_i = \frac{w_i \times s_i}{\sum_{i=1}^{m} w_i}$$

Trong đó chỉ tính các tiêu chí đang áp dụng và có $w_i > 0$.

---

## 5. Quy tắc ngưỡng dữ liệu tối thiểu để được xếp hạng (Mục 3.6)

Sau bước lọc điều kiện bắt buộc và trước bước tính điểm có trọng số, hệ thống đếm số tiêu chí ưu tiên mà gia sư có dữ liệu trong số $n$ tiêu chí ưu tiên đang áp dụng của truy vấn đó (tiêu chí **Đánh giá** không tính vào $n$ vì luôn dùng được nhờ giá trị trung tính $0,5$).

| Số tiêu chí ưu tiên đang áp dụng ($n$) | Ngưỡng tối thiểu phải có dữ liệu |
|:---:|:---:|
| 1 | 1 |
| 2 | 2 |
| 3 | 2 |
| 4 | 3 |
| 5 | 4 |

**Quyết định triển khai đã thống nhất bổ sung (xem `docs/design/scoring-spec.md` mục 7):**
1. Hàng $n = 5$ giữ nguyên như đề cương nhưng không bao giờ được kích hoạt trong thực tế vì Đánh giá không tính vào $n$, do đó $n \in \{0, 1, 2, 3, 4\}$.
2. Khi $n = 0$ (chỉ tiêu chí Đánh giá có trọng số $w > 0$), ngưỡng tối thiểu là $0$ (không loại gia sư nào vì thiếu dữ liệu).

---

## 6. Biên bản và minh chứng trao đổi với Giảng viên hướng dẫn

- **Giảng viên hướng dẫn:** TS. Lê Anh Nhã Uyên
- **Ngày báo cáo & thống nhất khóa thiết kế:** `2026-11-01` *(theo Đức báo)*
- **Kênh trao đổi:** Tin nhắn Zalo *(theo Đức báo)*
- **Nội dung đã được xác nhận *(theo Đức báo)*:**
  1. Thống nhất phát biểu bài toán (Mục 3.1), 3 chức năng cốt lõi CN01–CN03 (Bảng 3.1), phân loại tiêu chí (Bảng 3.2), công thức 5 tiêu chí (Bảng 3.6) và cơ chế tổng hợp điểm Weighted Scoring.
  2. Thống nhất quy tắc ngưỡng dữ liệu tối thiểu (Mục 3.6) kèm cách xử lý hai trường hợp $n = 5$ và $n = 0$ (đã ghi nhận tại PR #50 trong `docs/design/scoring-spec.md`).
  3. Thống nhất quy ước đánh giá 14 kịch bản Bảng 5.1 và hiệu chỉnh nhãn môn của hồ sơ `GS-G03` thành `"Anh Văn"` (đã ghi nhận tại PR #48 và PR #49).
- **Chỗ đính kèm ảnh chụp / đường dẫn minh chứng bổ sung (nhóm cập nhật thêm nếu cần):**
  - Ảnh chụp màn hình / trích xuất tin nhắn trao đổi: *[Chờ nhóm đính kèm tệp hoặc đường dẫn vào `docs/thesis/review/` nếu cần]*
