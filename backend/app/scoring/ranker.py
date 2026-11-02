"""Tổng hợp điểm bằng Weighted Scoring, xếp hạng và trích xuất Top-k gia sư.

Trách nhiệm:
- Hiện thực Bước 4 trong quy trình tính điểm mục 3.6
- Tính điểm tổng hợp: S = sum(w_i * s_i) / sum(w_i)
- Tính mức đóng góp từng tiêu chí: w_i * s_i / sum(w_i)
- Sắp xếp giảm dần theo S; trường hợp đồng điểm sắp xếp theo mã gia sư (tutor_id) để kết quả ổn định
- Trích xuất Top-k kết quả phù hợp nhất

Mục tương ứng trong đề cương:
- Mục 3.6. Thiết kế thuật toán (Bước 4: Tổng hợp và xếp hạng)
- Mục 4.3. Cài đặt module tính điểm
"""

from app.core.config import CRITERIA_KEYS, RATING_DEFAULT
from app.schemas.recommendation import RankedTutor
from app.schemas.search_request import SearchRequest
from app.schemas.tutor import TutorProfile
from app.scoring.criteria import (
    score_experience,
    score_fee,
    score_location,
    score_rating,
    score_schedule,
)
from app.scoring.weights import EffectiveWeights


def _compute_single_criterion_score(
    criterion_key: str,
    tutor: TutorProfile,
    query: SearchRequest,
) -> float:
    """Tính điểm thành phần `s_i` trong `[0, 1]` cho một tiêu chí đang áp dụng."""
    if criterion_key == "fee":
        if tutor.hourly_fee_vnd is None or query.max_budget_vnd is None:
            return 0.0
        return score_fee(tutor.hourly_fee_vnd, query.max_budget_vnd)

    if criterion_key == "district":
        if not query.preferred_district or not tutor.districts:
            return 0.0
        return score_location(query.preferred_district, tutor.districts)

    if criterion_key == "experience":
        if tutor.years_experience is None:
            return 0.0
        return score_experience(tutor.years_experience)

    if criterion_key == "rating":
        return score_rating(tutor.avg_rating)

    if criterion_key == "availability":
        if not query.time_slots or not tutor.availability:
            return 0.0
        return score_schedule(query.time_slots, tutor.availability)

    return 0.0


def _describe_criterion_highlight(
    criterion_key: str,
    tutor: TutorProfile,
    query: SearchRequest,
    score: float,
) -> str:
    """Sinh cụm mô tả ngắn gọn tiếng Việt cho một tiêu chí dựa trên dữ liệu đã tính."""
    if criterion_key == "fee":
        if (
            tutor.hourly_fee_vnd is not None
            and query.max_budget_vnd is not None
            and query.max_budget_vnd > 0
        ):
            if tutor.hourly_fee_vnd <= query.max_budget_vnd:
                return "học phí trong ngân sách"
            over_pct = round(
                (tutor.hourly_fee_vnd - query.max_budget_vnd)
                * 100
                / query.max_budget_vnd
            )
            return f"học phí vượt ngân sách {over_pct}%"
        return f"điểm học phí {score:.2f}".replace(".", ",")

    if criterion_key == "district":
        if score >= 1.0:
            return "khu vực khớp"
        return "khu vực khác quận mong muốn"

    if criterion_key == "experience":
        if tutor.years_experience is not None:
            years_val = (
                int(tutor.years_experience)
                if float(tutor.years_experience).is_integer()
                else tutor.years_experience
            )
            years_str = str(years_val).replace(".", ",")
            return f"kinh nghiệm {years_str} năm"
        return f"điểm kinh nghiệm {score:.2f}".replace(".", ",")

    if criterion_key == "rating":
        if tutor.avg_rating is not None:
            rating_str = f"{tutor.avg_rating:.1f}".replace(".", ",")
            return f"đánh giá {rating_str}/5"
        default_str = f"{RATING_DEFAULT:.1f}".replace(".", ",")
        return f"đánh giá trung tính ({default_str})"

    if criterion_key == "availability":
        if score >= 1.0:
            return "lịch rảnh khớp toàn bộ khung giờ mong muốn"
        if query.time_slots:
            matched = len(set(query.time_slots) & set(tutor.availability))
            return f"lịch rảnh khớp {matched}/{len(query.time_slots)} khung giờ"
        return f"điểm lịch rảnh {score:.2f}".replace(".", ",")

    return criterion_key


def build_notes(tutor: TutorProfile) -> list[str]:
    """Sinh danh sách ghi chú dữ liệu (ví dụ: `"chưa có đánh giá"`)."""
    if tutor.avg_rating is None:
        return ["chưa có đánh giá"]
    return []


def build_reason(
    tutor: TutorProfile,
    query: SearchRequest,
    criteria_scores: dict[str, float | None],
    contributions: dict[str, float | None],
) -> str:
    """Sinh lý do gợi ý tiếng Việt tất định dựa trên các tiêu chí đóng góp cao nhất."""
    order_index = {key: idx for idx, key in enumerate(CRITERIA_KEYS)}
    active_items = [
        (key, contrib)
        for key, contrib in contributions.items()
        if contrib is not None
    ]
    active_items.sort(key=lambda item: (-item[1], order_index[item[0]]))

    top_keys = [key for key, _ in active_items[:3]]
    phrases = [
        _describe_criterion_highlight(
            key,
            tutor,
            query,
            criteria_scores[key] or 0.0,
        )
        for key in top_keys
    ]
    if not phrases:
        return "Phù hợp điều kiện bắt buộc"

    joined = ", ".join(phrases)
    return joined[0].upper() + joined[1:]


def score_and_rank(
    tutors: list[TutorProfile],
    query: SearchRequest,
    effective_weights: EffectiveWeights,
    top_k: int = 3,
) -> list[RankedTutor]:
    """Tính điểm tổng hợp Weighted Scoring, sắp xếp giảm dần (phá hòa theo `tutor_id`) và lấy Top-k."""
    if effective_weights.total <= 0:
        raise ValueError("Tổng trọng số phải lớn hơn 0 để tiến hành xếp hạng.")
    if top_k < 1:
        raise ValueError("Tham số top_k phải lớn hơn hoặc bằng 1.")

    scored_candidates: list[tuple[float, str, dict[str, float | None], dict[str, float | None], str, list[str]]] = []

    for tutor in tutors:
        criteria_scores: dict[str, float | None] = {}
        contributions: dict[str, float | None] = {}
        total_score = 0.0

        for key in CRITERIA_KEYS:
            weight = effective_weights.weights.get(key)
            if weight is None or weight <= 0:
                criteria_scores[key] = None
                contributions[key] = None
            else:
                s_i = _compute_single_criterion_score(key, tutor, query)
                c_i = (weight * s_i) / effective_weights.total
                criteria_scores[key] = s_i
                contributions[key] = c_i
                total_score += c_i

        reason = build_reason(tutor, query, criteria_scores, contributions)
        notes = build_notes(tutor)
        scored_candidates.append(
            (total_score, tutor.tutor_id, criteria_scores, contributions, reason, notes)
        )

    scored_candidates.sort(key=lambda item: (-item[0], item[1]))

    ranked_results: list[RankedTutor] = []
    for idx, (
        total_score,
        tutor_id,
        criteria_scores,
        contributions,
        reason,
        notes,
    ) in enumerate(scored_candidates[:top_k], start=1):
        ranked_results.append(
            RankedTutor(
                rank=idx,
                tutor_id=tutor_id,
                total_score=total_score,
                criteria_scores=criteria_scores,
                contributions=contributions,
                reason=reason,
                notes=notes,
            )
        )

    return ranked_results
