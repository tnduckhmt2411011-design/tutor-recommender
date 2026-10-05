# Từ điển dữ liệu (Data Dictionary)

Tài liệu này định nghĩa bảng ánh xạ giữa các trường dữ liệu tiếng Việt được mô tả trong đề cương đồ án (Bảng 3.3 và Bảng 3.4) với các định danh tiếng Anh tương ứng sử dụng trong mã nguồn và cơ sở dữ liệu.

## 1. Bản ghi hồ sơ gia sư (Tutor Profile - Bảng 3.3)

| Trường trong đề cương (Bảng 3.3) | Định danh đề xuất trong code | Kiểu dữ liệu | Mô tả & Quy ước giá trị | Ghi chú so khớp với đề cương |
|---|---|---|---|---|
| `id` | `tutor_id` | `string` | Mã định danh gia sư duy nhất (ví dụ: `GS001`, `GS002`). | Đề cương dùng `id`; code đề xuất đổi thành `tutor_id` để tường minh hơn. |
| `môn_dạy` | `subjects` | `List[string]` | Danh sách môn học gia sư có thể giảng dạy (ví dụ: `["Toán", "Lý"]`). | Khớp với Bảng 3.3. |
| `khu_vực` | `districts` | `List[string]` | Danh sách khu vực nhận dạy trực tiếp; rỗng nếu chỉ dạy trực tuyến. | Khớp với Bảng 3.3. |
| `học_phí_giờ` | `hourly_fee_vnd` | `int` | Đơn giá học phí mỗi giờ theo VNĐ (ví dụ: `200000`). | Khớp với Bảng 3.3. |
| `số_năm_kinh_nghiệm` | `years_experience` | `float` / `int` | Số năm kinh nghiệm giảng dạy (ví dụ: `4`). | Khớp với Bảng 3.3. |
| `hình_thức_dạy` | `teaching_mode` | `string` (enum) | Giá trị: `in_person` (Trực tiếp), `online` (Trực tuyến), `both` (Cả hai). | Khớp với 3 giá trị trong Bảng 3.3. |
| `lịch_rảnh` | `availability` | `List[string]` | Tập khung giờ rảnh trong tuần (ví dụ: `["T2-tối", "T4-tối", "T7-sáng"]`). | Khớp với Bảng 3.3. |
| `điểm_đánh_giá_tb` | `avg_rating` | `Optional[float]` | Điểm trung bình thang 5. Để `null` (None) nếu chưa có đánh giá. | Khớp với Bảng 3.3. |
| `nguồn_dữ_liệu` | `data_source` | `string` (enum) | Giá trị: `public_collected` (Thu thập công khai), `simulated` (Giả lập), `estimated` (Ước tính). | Đề cương nêu 2 giá trị; code đề xuất bổ sung thêm `estimated` cho ngoại suy. |

---

## 2. Bản ghi nhu cầu của người học (Search Request - Bảng 3.4)

| Trường trong đề cương (Bảng 3.4) | Định danh đề xuất trong code | Kiểu dữ liệu | Mô tả & Quy ước giá trị | Ghi chú so khớp với đề cương |
|---|---|---|---|---|
| `môn_học` | `subject` | `string` | Môn học cần tìm gia sư (chọn đúng một môn, bắt buộc). | Khớp với Bảng 3.4. |
| `hình_thức_học` | `learning_mode` | `string` (enum) | Giá trị: `in_person` (Trực tiếp), `online` (Trực tuyến), `any` (Không yêu cầu). | Bổ sung `any` cho lựa chọn 'Không yêu cầu' trong đề cương. |
| `khu_vực_mong_muốn` | `preferred_district` | `Optional[string]` | Tên khu vực cần học trực tiếp (ví dụ: `"KV1"`), hoặc bỏ trống nếu học online. | Khớp với Bảng 3.4. |
| `ngân_sách_tối_đa` | `max_budget_vnd` | `Optional[int]` | Ngân sách tối đa mỗi giờ (VNĐ), hoặc bỏ trống nếu không giới hạn. | Khớp với Bảng 3.4. |
| `khung_thời_gian` | `time_slots` | `Optional[List[string]]` | Tập khung giờ rảnh của người học (ví dụ: `["T2-tối", "T4-tối"]`), hoặc bỏ trống. | Khớp với Bảng 3.4. |
| `mức_ưu_tiên` | `priorities` | `dict` / `PriorityConfig` | Mức ưu tiên của 5 tiêu chí: `fee`, `district`, `experience`, `rating`, `availability`. Giá trị mỗi tiêu chí: `none` (Không quan tâm, w=0), `low` (Thấp, w=1), `medium` (Trung bình, w=2), `high` (Cao, w=3). | Khớp với Bảng 3.4 và Bảng 3.5. Mặc định `medium` cho tất cả tiêu chí. |
