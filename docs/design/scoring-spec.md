# Đặc tả thuật toán tính điểm và xếp hạng gia sư

Tài liệu này trích dẫn nguyên văn công thức và quy tắc tính điểm từ **Mục 3.6 (Thiết kế thuật toán)** trong đề cương đồ án.

## 1. Quy trình tính điểm tổng quát (4 bước)

- **Bước 1. Kiểm tra và chuẩn hóa đầu vào:** Ví dụ ngân sách không âm, bắt buộc có môn học.
- **Bước 2. Lọc điều kiện bắt buộc theo Bảng 3.2:** Nếu không còn gia sư nào, trả thông báo *"không có gia sư thỏa điều kiện"*.
- **Bước 3. Tính điểm thành phần $s_i \in [0, 1]$ cho các tiêu chí ưu tiên theo Bảng 3.6.**
- **Bước 4. Gộp bằng công thức Weighted Scoring ở mục 2.3:** Sắp xếp giảm dần theo $S$ (đồng điểm thì xếp theo mã gia sư để kết quả ổn định), lấy Top-$k$ và trả kèm điểm thành phần cùng đóng góp $w_i \times s_i \div \sum w_i$ của từng tiêu chí.

---

## 2. Lọc bắt buộc (Ràng buộc cứng - Bảng 3.2)

- **Môn học:** Gia sư phải dạy môn học người học cần (`subject in tutor.subjects`).
- **Hình thức dạy/học:**
  - Nếu người học chọn `in_person`: Gia sư phải có hình thức `in_person` hoặc `both`.
  - Nếu người học chọn `online`: Gia sư phải có hình thức `online` hoặc `both`.
  - Nếu người học chọn `any`: Mọi gia sư đều thỏa mãn.
- **Lịch rảnh (ràng buộc tối thiểu):** Nếu người học có nhập lịch rảnh $L$, gia sư phải có ít nhất 1 khung giờ trùng khớp ($|L \cap T| \ge 1$).

---

## 3. Điều kiện đủ dữ liệu để được xếp hạng

> Trích nguyên văn Mục 3.6:
> "Sau bước lọc điều kiện bắt buộc và trước bước tính điểm có trọng số, hệ thống đếm số tiêu chí ưu tiên mà gia sư có dữ liệu, trong số các tiêu chí ưu tiên đang áp dụng của truy vấn đó ($n$; tiêu chí Đánh giá không tính vào $n$ vì luôn dùng được nhờ giá trị trung tính 0,5). Nếu số tiêu chí có dữ liệu nhỏ hơn ngưỡng tối thiểu tương ứng với $n$ (bảng dưới), gia sư bị loại khỏi kết quả xếp hạng của truy vấn này, ghi chú *'Không đủ dữ liệu để xếp hạng'* - không tính điểm trên phần dữ liệu ít ỏi còn lại. Công thức tính điểm của từng tiêu chí giữ nguyên, không đổi."

| Số tiêu chí ưu tiên đang áp dụng ($n$) | Ngưỡng tối thiểu phải có dữ liệu |
|:---:|:---:|
| 1 | 1 |
| 2 | 2 |
| 3 | 2 |
| 4 | 3 |
| 5 | 4 |

---

## 4. Công thức điểm từng tiêu chí ($s_i \in [0, 1]$ - Bảng 3.6)

### 4.1. Học phí
- **Đầu vào:** $P$: học phí gia sư; $B$: ngân sách người học; Tham số $\delta = 0,5$ (vượt 50% ngân sách thì điểm về 0).
- **Công thức:**
  $$s = 1 \quad \text{nếu } P \le B$$
  $$s = \max\left(0, 1 - \frac{P - B}{\delta \times B}\right) \quad \text{nếu } P > B$$
- **Ví dụ:** $B = 200.000$:
  - $P = 180.000 \rightarrow 1,00$
  - $P = 230.000 \rightarrow 0,70$
  - $P = 300.000 \rightarrow 0,00$

### 4.2. Khu vực
- **Đầu vào:** $K$: khu vực người học; tập khu vực dạy của gia sư.
- **Công thức:**
  $$s = 1 \quad \text{nếu } K \text{ thuộc khu vực dạy của gia sư; ngược lại } s = 0$$
- **Ghi chú:** Không áp dụng nếu học Trực tuyến hoặc người học không nhập $K$.
- **Ví dụ:** $K = \text{KV1}$:
  - Gia sư dạy $\{\text{KV1}, \text{KV2}\} \rightarrow 1$
  - Gia sư dạy $\{\text{KV3}\} \rightarrow 0$
  - Gia sư chỉ dạy trực tuyến $\rightarrow 0$

### 4.3. Kinh nghiệm
- **Đầu vào:** $E$: số năm kinh nghiệm; Tham số $E_{\max} = 8$.
- **Công thức:**
  $$s = \min\left(\frac{E}{E_{\max}}, 1\right)$$
- **Ví dụ:**
  - $E = 0 \rightarrow 0,00$
  - $E = 4 \rightarrow 0,50$
  - $E = 10 \rightarrow 1,00$

### 4.4. Đánh giá
- **Đầu vào:** $R$: điểm trung bình (thang 5). Giá trị trung tính: 0,5.
- **Công thức:**
  $$s = \frac{R}{5}; \quad \text{nếu chưa có đánh giá thì } s = 0,5$$
- **Ví dụ:**
  - $R = 5 \rightarrow 1,00$
  - $R = 4,5 \rightarrow 0,90$
  - $R = 3 \rightarrow 0,60$

### 4.5. Lịch rảnh
- **Đầu vào:** $L$: khung giờ người học; $T$: khung giờ gia sư (bước 2 đã đảm bảo $|L \cap T| \ge 1$).
- **Công thức:**
  $$s = \frac{|L \cap T|}{|L|}$$
- **Ghi chú:** Không áp dụng nếu người học không nhập $L$.
- **Ví dụ:**
  - $L = \{\text{T2-tối}, \text{T4-tối}, \text{T7-sáng}\}$, $T$ chứa T2-tối và T7-sáng $\rightarrow 2/3 \approx 0,67$.
  - $L$ có 7 khung, $T$ chứa 6 khung $\rightarrow 6/7 \approx 0,857$.
  - $L$ có 4 khung, $T$ chỉ chứa 1 khung $\rightarrow 1/4 = 0,25$.

---

## 5. Tổng hợp điểm và xếp hạng

- **Bảng quy đổi trọng số (Bảng 3.5):**
  - Không quan tâm: $w = 0$
  - Thấp: $w = 1$
  - Trung bình (mặc định): $w = 2$
  - Cao: $w = 3$
- **Công thức điểm tổng hợp Weighted Scoring:**
  $$S = \frac{\sum_{i=1}^m w_i \times s_i}{\sum_{i=1}^m w_i}$$
- **Tỷ lệ đóng góp của tiêu chí $i$:**
  $$C_i = \frac{w_i \times s_i}{\sum_{i=1}^m w_i}$$
- **Quy tắc xếp hạng:** Sắp xếp giảm dần theo $S$. Khi đồng điểm, sắp xếp theo mã gia sư (`tutor_id`) tăng dần để đảm bảo tính tất định và ổn định.

---

## 6. Các trường hợp đặc biệt

1. **Người học chọn học Trực tuyến:** Tiêu chí khu vực không áp dụng, bị loại khỏi cả tử số và mẫu số của công thức tổng hợp.
2. **Người học không nhập ngân sách, khu vực hoặc khung giờ:** Tiêu chí tương ứng không áp dụng, xử lý như trên.
3. **Tiêu chí có mức “Không quan tâm” ($w = 0$):** Không được tính.
4. **Tổng trọng số của các tiêu chí đang áp dụng bằng 0 ($\sum w_i = 0$):** Không thể xếp hạng; hệ thống hiển thị danh sách gia sư thỏa điều kiện bắt buộc kèm thông báo cho người học chọn ít nhất một tiêu chí ưu tiên.
5. **Gia sư chưa có điểm đánh giá:** Dùng giá trị trung tính 0,5 và ghi chú *“chưa có đánh giá”* trên giao diện.
