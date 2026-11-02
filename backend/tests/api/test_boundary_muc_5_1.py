"""Kiểm thử chức năng, kiểm thử ca biên (Mục 5.1), tính đơn điệu và luồng CN03
trên toàn hệ thống tích hợp qua endpoint POST /api/recommend (Issue #31 - US-29).

Mục tương ứng trong đề cương:
- Mục 3.2 (CN01, CN02, CN03)
- Mục 3.5 & Bảng 3.6 (5 hàm chuẩn hóa điểm thành phần và biên dung sai)
- Mục 5.1 & Bảng 5.1 (Kiểm thử chức năng, kiểm thử ca biên và 14 kịch bản thực nghiệm)
"""

from time import perf_counter

import pytest
from fastapi.testclient import TestClient

from app.api.recommend import get_tutor_repository
from app.main import app
from app.schemas.tutor import TutorProfile


class _BoundaryRepository:
    """Repository phục vụ kiểm thử chính xác các điểm biên toán học qua HTTP API."""

    def __init__(self, tutors: list[TutorProfile]) -> None:
        self._tutors = tutors

    def get_all(self) -> list[TutorProfile]:
        return list(self._tutors)


@pytest.fixture
def client() -> TestClient:
    app.dependency_overrides.clear()
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


class TestBoundaryCasesMuc51:
    """Kiểm thử toàn diện các ca biên theo đặc tả Mục 5.1 đề cương."""

    def test_fee_boundary_exact_equal_25pct_50pct_and_over_50pct(
        self, client: TestClient
    ) -> None:
        """Kiểm tra biên học phí với ngân sách B = 200.000 VNĐ (delta = 0,5 -> trần phạt 300.000):
        - P = 200.000 (= B)        -> s_fee = 1,00 (reason chứa 'học phí trong ngân sách')
        - P = 250.000 (= 1,25 B)   -> s_fee = 0,50 (reason chứa 'học phí vượt ngân sách 25%')
        - P = 300.000 (= 1,50 B)   -> s_fee = 0,00 (biên chạm ngưỡng 50%: 'học phí vượt ngân sách 50%')
        - P = 400.000 (> 1,50 B)   -> s_fee = 0,00 (ngoài vùng dung sai: 'học phí vượt ngân sách 100%')
        """
        boundary_tutors = [
            TutorProfile(
                tutor_id="GS-FEE-100",
                subjects=["Toán"],
                districts=["Quận 1"],
                hourly_fee_vnd=200000,
                years_experience=4,
                teaching_mode="in_person",
                availability=["T2-tối"],
                avg_rating=4.0,
                data_source="simulated",
            ),
            TutorProfile(
                tutor_id="GS-FEE-125",
                subjects=["Toán"],
                districts=["Quận 1"],
                hourly_fee_vnd=250000,
                years_experience=4,
                teaching_mode="in_person",
                availability=["T2-tối"],
                avg_rating=4.0,
                data_source="simulated",
            ),
            TutorProfile(
                tutor_id="GS-FEE-150",
                subjects=["Toán"],
                districts=["Quận 1"],
                hourly_fee_vnd=300000,
                years_experience=4,
                teaching_mode="in_person",
                availability=["T2-tối"],
                avg_rating=4.0,
                data_source="simulated",
            ),
            TutorProfile(
                tutor_id="GS-FEE-200",
                subjects=["Toán"],
                districts=["Quận 1"],
                hourly_fee_vnd=400000,
                years_experience=4,
                teaching_mode="in_person",
                availability=["T2-tối"],
                avg_rating=None,
                data_source="public_collected",
            ),
        ]
        app.dependency_overrides[get_tutor_repository] = lambda: _BoundaryRepository(
            boundary_tutors
        )

        # Chỉ bật 3 tiêu chí (fee, district, experience) để fee luôn nằm trong top-3 cụm lý do
        resp = client.post(
            "/api/recommend",
            json={
                "subject": "Toán",
                "learning_mode": "in_person",
                "preferred_district": "Quận 1",
                "max_budget_vnd": 200000,
                "priorities": {
                    "fee": "high",
                    "district": "medium",
                    "experience": "medium",
                    "rating": "none",
                    "availability": "none",
                },
                "top_k": 10,
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "success"
        by_id = {item["tutor_id"]: item for item in body["results"]}

        assert by_id["GS-FEE-100"]["criteria_scores"]["fee"] == pytest.approx(1.0)
        assert "học phí trong ngân sách" in by_id["GS-FEE-100"]["reason"].lower()
        assert by_id["GS-FEE-100"]["notes"] == []

        assert by_id["GS-FEE-125"]["criteria_scores"]["fee"] == pytest.approx(0.5)
        assert "học phí vượt ngân sách 25%" in by_id["GS-FEE-125"]["reason"].lower()

        assert by_id["GS-FEE-150"]["criteria_scores"]["fee"] == pytest.approx(0.0)
        assert "học phí vượt ngân sách 50%" in by_id["GS-FEE-150"]["reason"].lower()

        assert by_id["GS-FEE-200"]["criteria_scores"]["fee"] == pytest.approx(0.0)
        assert "học phí vượt ngân sách 100%" in by_id["GS-FEE-200"]["reason"].lower()
        assert by_id["GS-FEE-200"]["notes"] == ["chưa có đánh giá"]

    def test_fee_boundary_when_budget_is_zero(self, client: TestClient) -> None:
        """Kiểm tra ca biên max_budget_vnd = 0 không gây lỗi chia cho 0."""
        resp = client.post(
            "/api/recommend",
            json={
                "subject": "Toán",
                "learning_mode": "in_person",
                "preferred_district": "Bình Thạnh",
                "max_budget_vnd": 0,
                "top_k": 5,
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "success"
        for item in body["results"]:
            assert item["criteria_scores"]["fee"] == pytest.approx(0.0)

    def test_experience_boundary_zero_eight_and_above_eight_years(
        self, client: TestClient
    ) -> None:
        """Kiểm tra ca biên số năm kinh nghiệm (mốc bão hòa 8 năm):
        - E = 0 năm  -> s_experience = 0,000
        - E = 8 năm  -> s_experience = 1,000
        - E = 20 năm -> s_experience = 1,000 (không vượt quá 1,0)
        """
        exp_tutors = [
            TutorProfile(
                tutor_id="GS-EXP-0",
                subjects=["Hóa"],
                districts=["Quận 10"],
                hourly_fee_vnd=200000,
                years_experience=0,
                teaching_mode="in_person",
                availability=["T4-sáng"],
                avg_rating=4.5,
                data_source="simulated",
            ),
            TutorProfile(
                tutor_id="GS-EXP-8",
                subjects=["Hóa"],
                districts=["Quận 10"],
                hourly_fee_vnd=200000,
                years_experience=8,
                teaching_mode="in_person",
                availability=["T4-sáng"],
                avg_rating=4.5,
                data_source="simulated",
            ),
            TutorProfile(
                tutor_id="GS-EXP-20",
                subjects=["Hóa"],
                districts=["Quận 10"],
                hourly_fee_vnd=200000,
                years_experience=20,
                teaching_mode="in_person",
                availability=["T4-sáng"],
                avg_rating=4.5,
                data_source="simulated",
            ),
        ]
        app.dependency_overrides[get_tutor_repository] = lambda: _BoundaryRepository(
            exp_tutors
        )

        resp = client.post(
            "/api/recommend",
            json={
                "subject": "Hóa",
                "learning_mode": "in_person",
                "preferred_district": "Quận 10",
                "max_budget_vnd": 200000,
                "top_k": 5,
            },
        )
        assert resp.status_code == 200
        by_id = {item["tutor_id"]: item for item in resp.json()["results"]}

        assert by_id["GS-EXP-0"]["criteria_scores"]["experience"] == pytest.approx(0.0)
        assert by_id["GS-EXP-8"]["criteria_scores"]["experience"] == pytest.approx(1.0)
        assert by_id["GS-EXP-20"]["criteria_scores"]["experience"] == pytest.approx(1.0)
        # GS-EXP-8 và GS-EXP-20 có cùng điểm tổng hợp tuyệt đối
        assert by_id["GS-EXP-8"]["total_score"] == pytest.approx(
            by_id["GS-EXP-20"]["total_score"]
        )

    def test_schedule_overlap_boundary_partial_and_full(
        self, client: TestClient
    ) -> None:
        """Kiểm tra ca biên lịch rảnh trên dữ liệu thực tế:
        Truy vấn môn Toán với 3 khung giờ ['T2-tối', 'T4-tối', 'T6-tối']:
        - GS-T06 rảnh cả 3/3 khung giờ -> s_availability = 1,000
        - GS-G01 và GS-G10 rảnh 2/3 khung giờ ('T2-tối', 'T4-tối') -> s_availability = 2/3
        """
        resp = client.post(
            "/api/recommend",
            json={
                "subject": "Toán",
                "learning_mode": "in_person",
                "preferred_district": "Bình Thạnh",
                "max_budget_vnd": 200000,
                "time_slots": ["T2-tối", "T4-tối", "T6-tối"],
                "top_k": 5,
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "success"
        by_id = {item["tutor_id"]: item for item in body["results"]}

        assert by_id["GS-T06"]["criteria_scores"]["availability"] == pytest.approx(1.0)
        assert by_id["GS-G01"]["criteria_scores"]["availability"] == pytest.approx(
            2.0 / 3.0
        )
        assert by_id["GS-G10"]["criteria_scores"]["availability"] == pytest.approx(
            2.0 / 3.0
        )


class TestMonotonicityAndLivePriorityCN03:
    """Kiểm thử tính đơn điệu của mô hình điểm và tính năng điều chỉnh ưu tiên CN03."""

    def test_monotonicity_with_increasing_budget(self, client: TestClient) -> None:
        """Khi ngân sách tối đa tăng từ 150.000 -> 200.000 -> 350.000 VNĐ,
        điểm học phí s_fee và tổng điểm S(g) của mọi ứng viên không bao giờ giảm.
        """
        budgets = [150000, 200000, 350000]
        scores_by_budget: dict[int, dict[str, float]] = {}

        for budget in budgets:
            resp = client.post(
                "/api/recommend",
                json={
                    "subject": "Toán",
                    "learning_mode": "in_person",
                    "preferred_district": "Bình Thạnh",
                    "max_budget_vnd": budget,
                    "top_k": 10,
                },
            )
            assert resp.status_code == 200
            data = resp.json()
            scores_by_budget[budget] = {
                item["tutor_id"]: item["total_score"] for item in data["results"]
            }

        for tutor_id in scores_by_budget[150000]:
            s_150 = scores_by_budget[150000][tutor_id]
            s_200 = scores_by_budget[200000][tutor_id]
            s_350 = scores_by_budget[350000][tutor_id]
            assert s_150 <= s_200 + 1e-9
            assert s_200 <= s_350 + 1e-9

    def test_cn03_live_priority_adjustment_reranks_under_one_second(
        self, client: TestClient
    ) -> None:
        """Mô phỏng thao tác CN03 trên trang kết quả:
        - Bước 1: Truy vấn KB01 mặc định (mọi mức ưu tiên = medium) -> GS-G01 hạng 1, GS-T06 hạng 3.
        - Bước 2 (CN03): Người học tắt ưu tiên Học phí & Đánh giá ('none'), nâng Kinh nghiệm lên 'high'
          -> GS-T06 (20 năm kinh nghiệm, khớp Bình Thạnh) vươn lên hạng 1 (S = 1,000), vượt qua GS-G01.
        - Bước 3 (CN03): Người học chuyển toàn bộ về 'none' -> trạng thái zero_weight thân thiện.
        Mỗi bước cập nhật đều phản hồi dưới 1 giây.
        """
        base_query = {
            "subject": "Toán",
            "learning_mode": "in_person",
            "preferred_district": "Bình Thạnh",
            "max_budget_vnd": 200000,
            "top_k": 5,
        }

        # Bước 1: Mặc định (tất cả medium)
        t0 = perf_counter()
        resp_default = client.post(
            "/api/recommend",
            json={
                **base_query,
                "priorities": {
                    "fee": "medium",
                    "district": "medium",
                    "experience": "medium",
                    "rating": "medium",
                    "availability": "medium",
                },
            },
        )
        elapsed_1 = perf_counter() - t0
        assert resp_default.status_code == 200
        assert elapsed_1 < 1.0
        top3_default = [r["tutor_id"] for r in resp_default.json()["results"][:3]]
        assert top3_default == ["GS-G01", "GS-G10", "GS-T06"]

        # Bước 2 (CN03): Ưu tiên Kinh nghiệm = Cao, Khu vực = Trung bình, bỏ qua Học phí & Đánh giá
        t1 = perf_counter()
        resp_exp_focus = client.post(
            "/api/recommend",
            json={
                **base_query,
                "priorities": {
                    "fee": "none",
                    "district": "medium",
                    "experience": "high",
                    "rating": "none",
                    "availability": "medium",
                },
            },
        )
        elapsed_2 = perf_counter() - t1
        assert resp_exp_focus.status_code == 200
        assert elapsed_2 < 1.0
        results_exp = resp_exp_focus.json()["results"]
        # GS-T06 có s_district = 1.0, s_experience = 1.0 -> S = 1.0 đứng hạng 1
        assert results_exp[0]["tutor_id"] == "GS-T06"
        assert results_exp[0]["total_score"] == pytest.approx(1.0)
        assert results_exp[0]["contributions"]["fee"] is None
        assert results_exp[0]["contributions"]["rating"] is None

        # Bước 3 (CN03): Chuyển toàn bộ về 'none' -> nhận trạng thái zero_weight thân thiện
        t2 = perf_counter()
        resp_zero = client.post(
            "/api/recommend",
            json={
                **base_query,
                "priorities": {
                    "fee": "none",
                    "district": "none",
                    "experience": "none",
                    "rating": "none",
                    "availability": "none",
                },
            },
        )
        elapsed_3 = perf_counter() - t2
        assert resp_zero.status_code == 200
        assert elapsed_3 < 1.0
        assert resp_zero.json()["status"] == "zero_weight"
        assert len(resp_zero.json()["unranked_candidates"]) == 5
