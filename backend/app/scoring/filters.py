"""Lọc danh sách gia sư theo các điều kiện bắt buộc (ràng buộc cứng).

Trách nhiệm:
- Hiện thực Bước 2 trong quy trình tính điểm mục 3.6
- Lọc theo điều kiện môn học: gia sư phải đảm nhận môn học được yêu cầu
- Lọc theo hình thức học: khớp hình thức Trực tiếp/Trực tuyến/Cả hai (theo Bảng 3.2)
- Lọc theo lịch rảnh: phải có ít nhất 1 khung giờ giao nhau (|L ∩ T| >= 1) nếu người học có nhập lịch rảnh

Mục tương ứng trong đề cương:
- Mục 3.6. Thiết kế thuật toán (Bước 2: Lọc điều kiện bắt buộc)
- Bảng 3.2. Phân loại tiêu chí
"""

from app.schemas.search_request import SearchRequest
from app.schemas.tutor import TutorProfile


def _matches_subject(tutor: TutorProfile, query: SearchRequest) -> bool:
    return query.subject in tutor.subjects


def _matches_mode(tutor: TutorProfile, query: SearchRequest) -> bool:
    if query.learning_mode == "any":
        return True
    return tutor.teaching_mode in (query.learning_mode, "both")


def _matches_availability(tutor: TutorProfile, query: SearchRequest) -> bool:
    if not query.time_slots:
        return True
    return len(set(query.time_slots) & set(tutor.availability)) >= 1


def filter_mandatory(
    tutors: list[TutorProfile], query: SearchRequest
) -> list[TutorProfile]:
    """Giữ lại gia sư thỏa mọi điều kiện bắt buộc của Bảng 3.2.

    Danh sách rỗng là tín hiệu "không có gia sư thỏa điều kiện"; trạng thái
    `no_match` do API (Sprint 4) sinh ra. Thứ tự đầu vào được giữ nguyên.
    """
    return [
        tutor
        for tutor in tutors
        if _matches_subject(tutor, query)
        and _matches_mode(tutor, query)
        and _matches_availability(tutor, query)
    ]
