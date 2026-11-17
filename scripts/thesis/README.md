# Công cụ kiểm định và xuất báo cáo đồ án (`scripts/thesis/`)

Thư mục này chứa bộ script tự động phục vụ rà soát văn phong – logic – số liệu, đo hiệu năng nội tại và chuyển đổi toàn bộ báo cáo Markdown trong `docs/thesis/report/` thành tệp Word (`.docx`) hoàn chỉnh.

## 1. Yêu cầu môi trường

Kích hoạt hoặc dùng trực tiếp Python trong môi trường ảo `backend/.venv` (Python 3.12+ đã cài `pypandoc_binary`, `python-docx`, `pytest`, `pytest-cov`).

## 2. Danh mục script

| Tệp | Chức năng | Lệnh chạy mẫu (từ gốc kho mã nguồn) |
| :--- | :--- | :--- |
| `check_captions.py` | Kiểm tra toàn bộ 31 chú thích bảng, 9 chú thích hình, đường dẫn ảnh nhúng, dẫn chiếu mục/bảng/hình, tiểu mục con đơn độc và trích dẫn `[1]`–`[5]`. | `backend\.venv\Scripts\python.exe scripts\thesis\check_captions.py` |
| `benchmark_latency.py` | Thực hiện warm-up và đo thời gian phản hồi nội tại qua FastAPI `TestClient` (140 lượt và 700 lượt) trên 14 kịch bản `KB01–KB14`, đối chiếu ngưỡng SLA `< 1.000 ms`. | `backend\.venv\Scripts\python.exe scripts\thesis\benchmark_latency.py` |
| `recompute_numbers.py` | Tính lại và đối chiếu 74 mệnh đề số liệu xuyên suốt Chương 1–6 với dữ liệu gốc và mã nguồn, xuất báo cáo đối chiếu `docs/thesis/review/so-lieu-doi-chieu.csv`. | `backend\.venv\Scripts\python.exe scripts\thesis\recompute_numbers.py` |
| `build_docx.py` | Chuẩn hóa Markdown, dựng mẫu `reference.docx` (A4, lề chuẩn, Times New Roman), chuyển đổi công thức LaTeX sang OMML qua `pypandoc_binary`, nhúng 9 hình, chia 3 Section đánh số trang (`none` / `lowerRoman` / `decimal`) và ghép thành tệp `BAO_CAO_DO_AN_KHMT1_HOAN_CHINH.docx`. | `backend\.venv\Scripts\python.exe scripts\thesis\build_docx.py` |
| `verify_docx.py` | Kiểm định cấu trúc `.docx` đầu ra: 3 Section, khổ A4, lề, phông chữ, thứ tự Chương/Phụ lục, 31 bảng, 9 hình, số lượng OMML, không sót ký tự cấm (`…`, `[!NOTE]`, `TODO`, `$` thô) và đối chiếu tổng số từ (< 3%). | `backend\.venv\Scripts\python.exe scripts\thesis\verify_docx.py` |

## 3. Chạy kiểm thử đơn vị cho bộ công cụ

```powershell
backend\.venv\Scripts\pytest.exe backend\tests scripts\thesis -q
```
