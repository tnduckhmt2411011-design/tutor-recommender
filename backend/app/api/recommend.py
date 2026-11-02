"""Endpoint tiếp nhận yêu cầu tìm kiếm gia sư và trả về danh sách gợi ý.

Trách nhiệm:
- Endpoint POST /api/recommend nhận dữ liệu nhu cầu người học (Bảng 3.4)
- Gọi repository để lấy tập ứng viên, gọi luồng scoring thực thi 4 bước
- Trả về danh sách Top-k gia sư kèm điểm tổng và mức đóng góp tiêu chí
- Xử lý các tình huống biên: không có gia sư thỏa điều kiện, tổng trọng số bằng 0

Mục tương ứng trong đề cương:
- Mục 4.4. Xây dựng API gợi ý
"""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.data.repository import TutorRepository
from app.schemas.recommendation import (
    NoMatchResponse,
    RecommendationResponse,
    RecommendationSuccessResponse,
    ZeroWeightResponse,
)
from app.schemas.search_request import SearchRequest
from app.scoring.eligibility import filter_eligible_candidates
from app.scoring.filters import filter_mandatory
from app.scoring.ranker import score_and_rank
from app.scoring.weights import compute_effective_weights

router = APIRouter(prefix="/api", tags=["Recommendations"])


def get_tutor_repository() -> TutorRepository:
    """Khởi tạo đối tượng truy xuất dữ liệu hồ sơ gia sư."""
    return TutorRepository()


@router.post(
    "/recommend",
    response_model=RecommendationResponse,
    summary="Gợi ý danh sách Top-k gia sư theo mức độ phù hợp đa tiêu chí",
    description=(
        "Tiếp nhận nhu cầu của người học và mức ưu tiên 5 tiêu chí, thực hiện lọc điều kiện bắt buộc, "
        "kiểm tra tổng trọng số, áp ngưỡng dữ liệu tối thiểu và xếp hạng theo công thức Weighted Scoring."
    ),
)
def recommend_tutors(
    request: SearchRequest,
    repository: Annotated[TutorRepository, Depends(get_tutor_repository)],
) -> RecommendationResponse:
    """Xử lý yêu cầu khuyến nghị gia sư theo trình tự 5 bước tại Mục 6 của API Contract."""
    all_tutors = repository.get_all()
    total_candidates = len(all_tutors)

    # Bước 2: Lọc bắt buộc theo Bảng 3.2
    qualified = filter_mandatory(all_tutors, request)
    qualified_count = len(qualified)
    if not qualified:
        return NoMatchResponse(
            status="no_match",
            message="Không có gia sư thỏa điều kiện bắt buộc",
            total_candidates=total_candidates,
            qualified_candidates=0,
            insufficient_data_candidates=[],
            results=[],
        )

    # Bước 3: Kiểm tra tổng trọng số các tiêu chí đang áp dụng
    effective_weights = compute_effective_weights(request)
    if effective_weights.total == 0:
        return ZeroWeightResponse(
            status="zero_weight",
            message="Vui lòng chọn mức ưu tiên cho ít nhất một tiêu chí để tiến hành xếp hạng",
            total_candidates=total_candidates,
            qualified_candidates=qualified_count,
            unranked_candidates=[tutor.tutor_id for tutor in qualified],
        )

    # Bước 4: Áp ngưỡng dữ liệu tối thiểu (Mục 3.6)
    eligible, insufficient_ids = filter_eligible_candidates(
        qualified, effective_weights
    )
    if not eligible:
        return NoMatchResponse(
            status="no_match",
            message="Có gia sư thỏa điều kiện bắt buộc nhưng không đủ dữ liệu để xếp hạng",
            total_candidates=total_candidates,
            qualified_candidates=qualified_count,
            insufficient_data_candidates=insufficient_ids,
            results=[],
        )

    # Bước 5: Tính điểm, xếp hạng và lấy Top-k
    ranked_results = score_and_rank(
        eligible,
        request,
        effective_weights,
        top_k=request.top_k,
    )
    return RecommendationSuccessResponse(
        status="success",
        total_candidates=total_candidates,
        qualified_candidates=qualified_count,
        insufficient_data_candidates=insufficient_ids,
        results=ranked_results,
    )
