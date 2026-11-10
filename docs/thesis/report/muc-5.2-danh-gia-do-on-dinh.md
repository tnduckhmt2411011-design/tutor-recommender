# Mục 5.2. Đánh giá chất lượng xếp hạng

> [!NOTE]
> **Đề xuất, nhóm xác nhận**

**Phạm vi và nguồn số liệu.** Mục này đánh giá độ ổn định và độ nhạy của kết quả xếp hạng trên 16 hồ sơ gia sư trong `data/processed/tutors.json` và 14 kịch bản KB01–KB14 trong `backend/tests/scenarios/scenarios.json`. Trong 16 hồ sơ, 14 hồ sơ là `simulated`; 2 hồ sơ `public_collected` là GS-T06 và GS-T07, có học phí và lịch rảnh là ước tính của nhóm, `avg_rating = null` và được gán 0,5 khi tính điểm (`data/README.md`). Top-3 kỳ vọng của 14 kịch bản do nhóm tự xác định và được khóa bất biến trong `backend/tests/scenarios/scenarios.json`.

**Tham số và dữ liệu thô.** Baseline dùng δ = 0,50 và E_max = 8; trọng số theo Bảng 3.5 gồm Không quan tâm 0, Thấp 1, Trung bình 2, Cao 3. Các khảo sát độ nhạy lần lượt thay đổi δ ∈ {0,25; 0,30; 0,50; 0,70; 0,75; 1,00}, E_max ∈ {5; 6; 8; 10; 12}, ngân sách theo các mức −20%, −10%, −5%, 0%, +5%, +10%, +20% và bốn bộ mức ưu tiên. Số liệu thô lấy từ `docs/thesis/report/muc-5.2-ket-qua-tho.json`, sinh bởi `backend/tests/scenarios/test_sensitivity_muc_5_2.py`; trường `meta.git_commit` ghi commit gốc `f66f065`. Bản thảo này chưa có phản hồi của GVHD.

## 5.2.1. So khớp Top-3 với kỳ vọng

Bảng 5.2 đối chiếu Top-3 hệ thống với Top-3 kỳ vọng của 14 kịch bản. Quy ước chấm khớp theo `backend/tests/scenarios/README.md` mục 3: với $m$ kỳ vọng ($1 \le m \le 3$), độ khớp là $x/m$; KB05 là trường hợp `no_match` với danh sách rỗng và được tính là khớp 0/0.

**Bảng 5.2 - Đối chiếu Top-3 hệ thống với Top-3 kỳ vọng trên 14 kịch bản**

| Mã KB | Top-3 kỳ vọng | Top-3 hệ thống | Số trùng x/m |
|:---:|:---|:---|:---:|
| KB01 | `GS-G01 > GS-G10 > GS-T06` | `GS-G01 > GS-G10 > GS-T06` | 3/3 |
| KB02 | `GS-G11 > GS-G12 > GS-T07` | `GS-G11 > GS-G12 > GS-T07` | 3/3 |
| KB03 | `GS-G12 > GS-G11 > GS-T07` | `GS-G12 > GS-G11 > GS-T07` | 3/3 |
| KB04 | `GS006 > GS020` | `GS006 > GS020` | 2/2 |
| KB05 | `[]` (`no_match`) | `[]` (`no_match`) | 0/0 |
| KB06 | `GS-G04` | `GS-G04` | 1/1 |
| KB07 | `GS-G05` | `GS-G05` | 1/1 |
| KB08 | `GS-G07` | `GS-G07` | 1/1 |
| KB09 | `GS-G08` | `GS-G08` | 1/1 |
| KB10 | `GS-G10 > GS-G01 > GS-G09` | `GS-G10 > GS-G01 > GS-G09` | 3/3 |
| KB11 | `GS-G06 > GS-T06` | `GS-G06 > GS-T06` | 2/2 |
| KB12 | `GS-T07 > GS-G11 > GS-G12` | `GS-T07 > GS-G11 > GS-G12` | 3/3 |
| KB13 | `GS-G10 > GS-G01 > GS-T06` | `GS-G10 > GS-G01 > GS-T06` | 3/3 |
| KB14 | `GS-G03` | `GS-G03` | 1/1 |

*Nguồn: `docs/thesis/report/muc-5.2-ket-qua-tho.json`, khối `baseline`; quy ước chấm khớp tại `backend/tests/scenarios/README.md` mục 3.*

Tổng hợp: **14/14 kịch bản** có Top-3 trùng kỳ vọng; KB05 được tính là khớp theo quy ước `no_match` 0/0. Không có kịch bản nào đảo thứ hạng hoặc lọt ứng viên ngoài danh sách kỳ vọng. Ba trường hợp cần ghi chú:

- **KB04:** hệ thống cho điểm 0,88625 và 0,78625, trong khi bản tính tay của Bảng 5.1 là 0,848 và 0,715. Nguyên nhân là phép tính tay bỏ tiêu chí lịch rảnh; thứ hạng `GS006 > GS020` không đổi.
- **KB09:** điểm chính xác là 0,9275; Bảng 5.1 làm tròn thành 0,928. Chênh lệch 0,0005 chỉ do quy tắc làm tròn, không đổi thứ hạng 1/1.
- **KB02 và KB12:** `GS-G11` và `GS-G12` đồng điểm lần lượt 0,88125 và 0,63125; hệ thống phá hòa theo `tutor_id` tăng dần nên `GS-G11` đứng trước `GS-G12`.

Chi tiết toán học của ba trường hợp trên ở `docs/thesis/report/discrepancy_analysis.md` mục 3.1–3.3.

## 5.2.2. Thứ hạng bất hợp lý và điều chỉnh

Trong phạm vi đối chiếu 14 kịch bản baseline, không ghi nhận thứ hạng nào bất hợp lý: các kịch bản có một ứng viên đều trả về đúng ứng viên; các kịch bản có đồng điểm được phá hòa tất định; KB04 và KB09 chỉ khác ở số hiển thị, không khác thứ hạng. Vì vậy nhóm **không điều chỉnh hàm điểm, không đổi δ, E_max hay trọng số, và không sửa `expected_top3` hoặc `expected_raw`** để khớp kỳ vọng. Các khác biệt số học của KB04 và KB09 được giải thích bằng công thức và quy tắc làm tròn; KB02 và KB12 là đồng điểm thực sự nên chỉ cần quy tắc phá hòa. Trường hợp KB10 thay đổi Top-3 ở E_max = 10 và 12 được phân tích ở mục 5.2.3 là thay đổi do tham số, không phải lỗi xếp hạng của baseline.

## 5.2.3. Tính ổn định và độ nhạy

Ba bảng dưới ghi số kịch bản đổi Top-3 so với baseline (δ = 0,50; E_max = 8; ngân sách gốc). “Đổi Top-3” được hiểu là thay đổi tập hợp hoặc thứ tự so với baseline.

**Bảng 5.3 - Độ nhạy của Top-3 theo δ**

| δ | Số KB đổi Top-3 | KB đổi | Số KB trùng Top-3 baseline (x/m) |
|:---:|:---:|:---:|:---:|
| 0,25 | 0 | — | 14/14 |
| 0,30 | 0 | — | 14/14 |
| 0,50 (baseline) | 0 | — | 14/14 |
| 0,70 | 0 | — | 14/14 |
| 0,75 | 0 | — | 14/14 |
| 1,00 | 0 | — | 14/14 |

*Nguồn: `docs/thesis/report/muc-5.2-ket-qua-tho.json`, khối `delta`; baseline δ = 0,50.*

Kết quả là **0/14 kịch bản đổi Top-3** ở cả 6 mức δ. Điều này phù hợp với công thức học phí: khi $P \le B$, $s_{\text{fee}} = 1$; khi $P > B$, mẫu số $\delta B$ tăng làm mức phạt giảm, nên $s_{\text{fee}}$ không giảm khi δ tăng. Tuy nhiên, việc thứ hạng giữ nguyên trên tập 16 hồ sơ là quan sát thực nghiệm, không phải bảo đảm cho mọi tập dữ liệu.

**Bảng 5.4 - Độ nhạy của Top-3 theo E_max**

| E_max | Số KB đổi Top-3 | KB đổi | Top-3 của KB10 | Số KB trùng Top-3 baseline (x/m) |
|:---:|:---:|:---:|:---|:---:|
| 5 | 0 | — | `GS-G10 > GS-G01 > GS-G09` | 14/14 |
| 6 | 0 | — | `GS-G10 > GS-G01 > GS-G09` | 14/14 |
| 8 (baseline) | 0 | — | `GS-G10 > GS-G01 > GS-G09` | 14/14 |
| 10 | 1 | KB10 | `GS-G10 > GS-G09 > GS-T06` | 13/14 |
| 12 | 1 | KB10 | `GS-G10 > GS-T06 > GS-G09` | 13/14 |

*Nguồn: `docs/thesis/report/muc-5.2-ket-qua-tho.json`, khối `e_max`; baseline E_max = 8.*

Trong khảo sát E_max, KB10 là kịch bản duy nhất đổi Top-3, và chỉ ở E_max = 10 và 12; ở cả hai mức, KB10 chỉ trùng 2/3 thành viên Top-3 kỳ vọng. KB10 áp dụng ba tiêu chí: Khu vực ($w = 2$), Kinh nghiệm ($w = 3$) và Đánh giá ($w = 2$), tổng trọng số 7; Học phí và Lịch rảnh không áp dụng vì kịch bản không có ngân sách và không có `time_slots`. Điểm baseline của các ứng viên là `GS-G10` 0,99429; `GS-G01` 0,60714; `GS-G09` 0,59286; `GS-T06` 0,57143.

- **E_max = 10:** `GS-G09` có $(2 \times 1 + 3 \times 2/10 + 2 \times 0{,}7)/7 = 4/7$; `GS-T06` có $(2 \times 0 + 3 \times 1 + 2 \times 0{,}5)/7 = 4/7$. Hai gia sư hòa điểm; trường `total_score` trong JSON đều là 0,57143, tương ứng cùng một giá trị toán học 4/7. Khóa sắp xếp $(-total\_score, tutor\_id)$ đưa `GS-G09` lên hạng 2 và `GS-T06` xuống hạng 3. Vì vậy thay đổi Top-3 ở E_max = 10 là do **hòa điểm và phá hòa**, không phải do điểm của hai gia sư khác nhau.
- **E_max = 12:** `GS-G09` có $(2 \times 1 + 3 \times 2/12 + 2 \times 0{,}7)/7 = 3{,}9/7 = 0{,}55714$; `GS-T06` vẫn là $4/7 = 0{,}57143$. `GS-T06` vượt `GS-G09`, nên Top-3 thành `GS-G10 > GS-T06 > GS-G09`.

**Bảng 5.5 - Độ nhạy của Top-3 theo mức ngân sách**

| Mức ngân sách | Số KB áp dụng | Số KB đổi Top-3 | KB đổi | Số KB áp dụng trùng Top-3 baseline (x/m) |
|:---:|:---:|:---:|:---:|:---:|
| −20% | 11 | 0 | — | 11/11 |
| −10% | 11 | 0 | — | 11/11 |
| −5% | 11 | 0 | — | 11/11 |
| 0% (baseline) | 11 | 0 | — | 11/11 |
| +5% | 11 | 0 | — | 11/11 |
| +10% | 11 | 0 | — | 11/11 |
| +20% | 11 | 0 | — | 11/11 |

*Nguồn: `docs/thesis/report/muc-5.2-ket-qua-tho.json`, khối `budget`; KB05, KB10 và KB14 không có `max_budget_vnd` nên không áp dụng.*

Trong 11 kịch bản áp dụng, không có thay đổi Top-3 ở cả 7 mức ngân sách. KB05, KB10 và KB14 không có ngân sách nên không áp dụng; tệp JSON vẫn ghi đủ 14 dòng cho mỗi mức, với `applicable: false` ở ba dòng này.

**Tính chất đơn điệu.** Các bài kiểm thử T4, T6 và T7–T9 kiểm tra các tính chất sau trên các kịch bản áp dụng:

- **T4:** với mỗi ứng viên, $S$ không giảm khi δ tăng (các kịch bản có ngân sách và tiêu chí học phí khác `none`).
- **T6:** với mỗi ứng viên, $S$ không tăng khi E_max tăng (các kịch bản có tiêu chí kinh nghiệm khác `none`).
- **T7–T9:** khi ngân sách tăng, $S$ không giảm; tập ứng viên qua lọc và thứ tự ứng viên không đổi qua chuỗi 7 mức từ −20% đến +20%.

Các tính chất này là hệ quả của công thức Bảng 3.6: $s_{\text{fee}} = \max(0, 1 - (P - B)/(\delta B))$ khi $P > B$ nên tăng khi δ tăng hoặc $B$ tăng; $s_{\text{experience}} = \min(E/E_{\max}, 1)$ nên không tăng khi E_max tăng. Cần phân biệt hai mức độ: tính đơn điệu của $S$ chứng minh được từ công thức, còn việc Top-3 không đổi là quan sát thực nghiệm trên 16 hồ sơ và 14 kịch bản. Một hàm $S$ đơn điệu không bảo đảm thứ hạng không đổi, vì các ứng viên có thể dịch chuyển khác nhau; ngược lại, thứ hạng không đổi trên tập nhỏ không chứng minh tính đơn điệu cho mọi dữ liệu.

## 5.2.4. Ảnh hưởng của mức ưu tiên

Bốn bộ dưới đây là bộ của bài kiểm thử T10 trong `backend/tests/scenarios/test_sensitivity_muc_5_2.py`: `default`, `prioritize_district`, `prioritize_fee`, `prioritize_experience_rating`. Chúng khác ba preset `none`, `high_score`, `pass_basic` của tính năng US-41; kết quả 19 truy vấn của US-41 được trình bày riêng tại `docs/design/de-xuat-mo-rong-cap-lop-muc-tieu.md` và không dùng trong các bảng độ nhạy của mục này.

**Bảng 5.6 - Ảnh hưởng của bốn bộ mức ưu tiên đến Top-3**

| Bộ mức ưu tiên | Số KB đổi Top-3 | KB đổi Top-3 | Thay đổi Top-3 cụ thể |
|:---|:---:|:---:|:---|
| Mặc định (tất cả Trung bình) | 1 | KB10 | `GS-G10 > GS-G09 > GS-G01` thay cho `GS-G10 > GS-G01 > GS-G09`: đảo hạng 2–3, cùng tập 3/3 |
| Ưu tiên Khu vực (district Cao, còn lại Thấp) | 2 | KB01, KB10 | KB01: `GS-G01 > GS-T06 > GS-G02` thay cho `GS-G01 > GS-G10 > GS-T06`; `GS-G10` rơi khỏi Top-3, `GS-T06` lên hạng 2, `GS-G02` hạng 3 (trùng 2/3). KB10: `GS-G10 > GS-G09 > GS-G01` thay cho `GS-G10 > GS-G01 > GS-G09` (đảo hạng 2–3, cùng tập 3/3) |
| Ưu tiên Học phí (fee Cao, còn lại Thấp) | 1 | KB10 | `GS-G10 > GS-G09 > GS-G01` thay cho `GS-G10 > GS-G01 > GS-G09` (đảo hạng 2–3, cùng tập 3/3); KB01 giữ nguyên |
| Ưu tiên KN & Đánh giá (experience và rating Cao, còn lại Thấp) | 1 | KB10 | `GS-G10 > GS-G01 > GS-T06` thay cho `GS-G10 > GS-G01 > GS-G09`: `GS-T06` vào Top-3 thay `GS-G09` (trùng 2/3) |

*Nguồn: `docs/thesis/report/muc-5.2-ket-qua-tho.json`, khối `priority_sets`; baseline là bộ `priorities` gốc của từng kịch bản.*

Nhận xét:

- **KB01 ở bộ Ưu tiên Khu vực:** `GS-G10` không dạy Bình Thạnh nên bị đẩy khỏi Top-3; `GS-T06` và `GS-G02` đều dạy Bình Thạnh nên tăng hạng. Thay đổi này hợp lý theo dữ liệu hồ sơ, không phải lỗi xếp hạng.
- **KB10 ở bộ Mặc định:** baseline của KB10 có `experience = high`; bộ Mặc định đặt `experience = medium`, tức **ghi đè** thiết lập gốc. Trọng số kinh nghiệm giảm từ 3 xuống 2, trong khi Khu vực và Đánh giá đều bằng 2, nên `GS-G09` (khớp khu vực, 2 năm, 3,5/5) vượt `GS-G01` (không khớp khu vực, 6 năm, 5,0/5). Chênh lệch này là do cách so sánh với baseline, không phải mất ổn định.
- **KB10 ở bộ Ưu tiên Học phí:** KB10 không có ngân sách nên tiêu chí học phí không áp dụng; đặt `fee = high` không tạo tác dụng với học phí. Kết quả trùng bộ Mặc định vì các tiêu chí còn áp dụng có cùng trọng số.
- **KB10 ở bộ Ưu tiên KN & Đánh giá:** `GS-T06` (20 năm, đánh giá trung tính 0,5) vào Top-3 thay `GS-G09` (2 năm, 3,5/5); thay đổi này hợp lý khi tăng trọng số kinh nghiệm và đánh giá.
- **Không bộ nào đổi hạng 1:** KB01 vẫn `GS-G01`, KB10 vẫn `GS-G10`. KB10 là kịch bản duy nhất xuất hiện ở cả bốn bộ; KB01 chỉ xuất hiện ở bộ Ưu tiên Khu vực.

## 5.2.5. Khả năng giải thích

Phản hồi thật của `POST /api/recommend` cho KB01 (HTTP 200) có cấu trúc `status`, `total_candidates`, `qualified_candidates`, `insufficient_data_candidates` và `results[]`; mỗi kết quả gồm `rank`, `tutor_id`, `total_score`, `criteria_scores`, `contributions`, `reason`, `notes` (`docs/design/api-contract.md` mục 3). `criteria_scores` và `contributions` luôn đủ 5 khóa; tiêu chí không áp dụng có giá trị `null`.

**Bảng 5.7 - Thành phần điểm và đóng góp của ba gia sư Top-3 tại KB01**

| Hạng | Gia sư | $S$ | `criteria_scores` (fee; district; experience; rating; availability) | `contributions` (fee; district; experience; rating; availability) |
|:---:|:---|:---:|:---|:---|
| 1 | GS-G01 | 0,9375 | 1,0000; 1,0000; 0,7500; 1,0000; null | 0,2500; 0,2500; 0,1875; 0,2500; null |
| 2 | GS-G10 | 0,7450 | 1,0000; 0,0000; 1,0000; 0,9800; null | 0,2500; 0,0000; 0,2500; 0,2450; null |
| 3 | GS-T06 | 0,6250 | 0,0000; 1,0000; 1,0000; 0,5000; null | 0,0000; 0,2500; 0,2500; 0,1250; null |

*Nguồn: phản hồi thật của `POST /api/recommend` cho KB01 (HTTP 200), đối chiếu với khối `baseline` của `docs/thesis/report/muc-5.2-ket-qua-tho.json`.*

Lý do gợi ý và ghi chú trả về:

- **GS-G01:** `"Học phí trong ngân sách, khu vực khớp, đánh giá 5,0/5"`; `notes = []`.
- **GS-G10:** `"Học phí trong ngân sách, kinh nghiệm 12 năm, đánh giá 4,9/5"`; `notes = []`.
- **GS-T06:** `"Khu vực khớp, kinh nghiệm 20 năm, đánh giá trung tính (0,5)"`; `notes = ["chưa có đánh giá"]`.

Ví dụ này cho thấy bốn điểm: (i) điểm tổng là tổng có trọng số của các điểm thành phần; (ii) các `contributions` cộng lại bằng `total_score`; (iii) `reason` tóm tắt các điểm nổi bật; (iv) `notes` ghi cảnh báo dữ liệu. Với `GS-G10`, `reason` không nhắc khu vực không khớp, nhưng `criteria_scores.district = 0,0` và `contributions.district = 0,0` vẫn thể hiện rõ trong phản hồi; người đọc cần xem cả hai trường này, không chỉ `reason`. `availability = null` ở cả ba gia sư vì KB01 không nhập `time_slots`.

Các giá trị trong Bảng 5.7 được làm tròn 4 chữ số thập phân để hiển thị. Phản hồi API thô có sai số biểu diễn số thực ở một số trường, ví dụ `rating = 0.9800000000000001` và `contributions.rating = 0.24500000000000002` của `GS-G10`; giá trị dùng trong bảng là 0,9800 và 0,2450.

## 5.2.6. Hạn chế và kết luận ngắn

Kết quả chính: baseline trùng Top-3 kỳ vọng 14/14; δ không làm đổi Top-3 ở cả 6 mức; E_max chỉ làm đổi KB10 ở mức 10 và 12; ngân sách không làm đổi Top-3 trong 11 kịch bản áp dụng; bốn bộ mức ưu tiên chỉ làm đổi KB01 và KB10 và không đổi hạng 1. Các thay đổi của KB10 được giải thích bằng hòa điểm, phá hòa hoặc bằng việc bộ Mặc định ghi đè `experience = high`; không có thay đổi nào đòi hỏi sửa công thức.

Hạn chế:

- Tập dữ liệu nhỏ: 16 hồ sơ, trong đó 14 hồ sơ mô phỏng; hai hồ sơ `public_collected` là GS-T06 và GS-T07 có học phí và lịch rảnh ước tính, điểm đánh giá để trống và dùng giá trị trung tính 0,5.
- 14 kịch bản và Top-3 kỳ vọng do nhóm tự xác định, không phải dữ liệu đối chứng độc lập từ người học thật. Vì vậy 14/14 chỉ cho thấy hệ thống tính đúng công thức đã chốt, chưa phải bằng chứng độc lập về chất lượng gợi ý.
- δ, E_max và trọng số do nhóm đặt; kết quả độ nhạy gắn với các lựa chọn này và không khái quát cho tập dữ liệu khác hoặc cho người học thật.
- Kết quả không đủ để kết luận về độ bền vững tổng quát của phương pháp; cần thêm dữ liệu thật, kịch bản độc lập và đánh giá từ người dùng để kiểm chứng chất lượng gợi ý.

Kết luận ngắn: trên phạm vi 16 hồ sơ và 14 kịch bản, kết quả xếp hạng ổn định trước các thay đổi δ và ngân sách; chỉ KB10 thay đổi khi E_max = 10 hoặc 12, với bản chất hòa điểm và phá hòa đã giải thích. Đây là kết quả trên một tập dữ liệu nhỏ, không phải kết luận tổng quát về chất lượng gợi ý.

**Ghi chú.** Danh mục bảng của Chương 5 được đồng bộ ở US-36.
