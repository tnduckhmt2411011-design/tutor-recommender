"""Kiểm thử tích hợp cho API gợi ý gia sư (POST /api/recommend).

Trách nhiệm:
- Kiểm tra tính đúng đắn của dữ liệu trả về theo hợp đồng API
- Kiểm tra mã phản hồi HTTP cho các ca hợp lệ và ca biên (không có gia sư, tổng trọng số 0)
- Kiểm tra thời gian phản hồi theo mục 5.1 (< 1s)

Mục tương ứng trong đề cương: Mục 4.4, Mục 5.1.
"""

import json
from pathlib import Path
from time import perf_counter
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.api.recommend import get_tutor_repository
from app.core.config import CRITERIA_KEYS
from app.main import app
from app.schemas.tutor import TutorProfile

SCENARIOS_JSON_PATH = (
    Path(__file__).resolve().parent.parent / "scenarios" / "scenarios.json"
)


class _DummyRepository:
    """Repository giả lập phục vụ kiểm thử biến thể thiếu dữ liệu (Mục 4.4)."""

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


class TestRecommendSuccessResponses:
    """Kiểm thử phản hồi 200 OK (status='success') theo Mục 3 và Mục 5 của API Contract."""

    def test_recommend_success_structure_and_latency(
        self, client: TestClient
    ) -> None:
        payload = {
            "subject": "Toán",
            "learning_mode": "in_person",
            "preferred_district": "Bình Thạnh",
            "max_budget_vnd": 200000,
            "time_slots": ["T2-tối", "T4-tối"],
            "priorities": {
                "fee": "medium",
                "district": "medium",
                "experience": "medium",
                "rating": "medium",
                "availability": "medium",
            },
            "top_k": 3,
        }

        start = perf_counter()
        response = client.post("/api/recommend", json=payload)
        elapsed = perf_counter() - start

        assert response.status_code == 200
        assert elapsed < 1.0

        body = response.json()
        assert body["status"] == "success"
        assert "message" not in body
        assert body["total_candidates"] == 16
        assert body["qualified_candidates"] >= 1
        assert body["insufficient_data_candidates"] == []
        assert 1 <= len(body["results"]) <= 3

        first = body["results"][0]
        assert first["rank"] == 1
        assert isinstance(first["tutor_id"], str)
        assert isinstance(first["total_score"], float)
        assert tuple(first["criteria_scores"].keys()) == CRITERIA_KEYS
        assert tuple(first["contributions"].keys()) == CRITERIA_KEYS
        assert isinstance(first["reason"], str) and len(first["reason"].strip()) > 0
        assert isinstance(first["notes"], list)

    def test_recommend_respects_custom_top_k(self, client: TestClient) -> None:
        base_payload = {
            "subject": "Toán",
            "learning_mode": "in_person",
            "preferred_district": "Bình Thạnh",
            "max_budget_vnd": 200000,
        }

        resp_top1 = client.post(
            "/api/recommend", json={**base_payload, "top_k": 1}
        )
        assert resp_top1.status_code == 200
        assert len(resp_top1.json()["results"]) == 1

        resp_top10 = client.post(
            "/api/recommend", json={**base_payload, "top_k": 10}
        )
        assert resp_top10.status_code == 200
        # Có 5 gia sư Toán trực tiếp trong kho dữ liệu -> trả hết 5, không lỗi
        assert len(resp_top10.json()["results"]) == 5
        assert [r["rank"] for r in resp_top10.json()["results"]] == [1, 2, 3, 4, 5]

    @pytest.mark.parametrize(
        "scenario_id",
        [f"KB{i:02d}" for i in range(1, 15)],
    )
    def test_all_14_scenarios_via_http_endpoint(
        self, client: TestClient, scenario_id: str
    ) -> None:
        scenarios: list[dict[str, Any]] = json.loads(
            SCENARIOS_JSON_PATH.read_text(encoding="utf-8")
        )
        scenario = next(s for s in scenarios if s["id"] == scenario_id)

        response = client.post("/api/recommend", json=scenario["request"])
        assert response.status_code == 200
        body = response.json()

        if scenario_id == "KB05":
            assert body["status"] == "no_match"
            assert body["results"] == []
        else:
            assert body["status"] == "success"
            system_top3 = [item["tutor_id"] for item in body["results"]]
            assert system_top3 == scenario["expected_top3"]


class TestRecommendSpecialBusinessStatuses:
    """Kiểm thử các phản hồi nghiệp vụ đặc biệt (Mục 4.1, 4.2, 4.4)."""

    def test_no_match_when_mandatory_filter_empty(self, client: TestClient) -> None:
        response = client.post(
            "/api/recommend",
            json={
                "subject": "Tiếng Trung",
                "learning_mode": "any",
            },
        )
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "no_match"
        assert body["message"] == "Không có gia sư thỏa điều kiện bắt buộc"
        assert body["results"] == []
        assert body["insufficient_data_candidates"] == []
        assert body["total_candidates"] == 16
        assert body["qualified_candidates"] == 0

    def test_zero_weight_when_all_priorities_are_none(
        self, client: TestClient
    ) -> None:
        response = client.post(
            "/api/recommend",
            json={
                "subject": "Toán",
                "learning_mode": "in_person",
                "preferred_district": "Bình Thạnh",
                "max_budget_vnd": 200000,
                "priorities": dict.fromkeys(CRITERIA_KEYS, "none"),
            },
        )
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "zero_weight"
        assert (
            body["message"]
            == "Vui lòng chọn mức ưu tiên cho ít nhất một tiêu chí để tiến hành xếp hạng"
        )
        assert len(body["unranked_candidates"]) == 5
        assert "GS-G01" in body["unranked_candidates"]
        assert "results" not in body

    def test_no_match_variant_when_all_qualified_fail_data_threshold(
        self, client: TestClient
    ) -> None:
        incomplete_tutors = [
            TutorProfile(
                tutor_id="GS-INC-1",
                subjects=["Toán"],
                districts=[],
                hourly_fee_vnd=None,
                years_experience=None,
                teaching_mode="in_person",
                availability=["T2-tối"],
                avg_rating=4.5,
                data_source="simulated",
            ),
            TutorProfile(
                tutor_id="GS-INC-2",
                subjects=["Toán"],
                districts=[],
                hourly_fee_vnd=200000,
                years_experience=None,
                teaching_mode="both",
                availability=["T2-tối"],
                avg_rating=None,
                data_source="simulated",
            ),
        ]
        app.dependency_overrides[get_tutor_repository] = lambda: _DummyRepository(
            incomplete_tutors
        )

        # Với 4 tiêu chí áp dụng (fee, district, experience, availability) -> ngưỡng tối thiểu là 3
        # GS-INC-1 chỉ có 1/4 tiêu chí, GS-INC-2 chỉ có 2/4 tiêu chí -> cả hai đều bị loại
        response = client.post(
            "/api/recommend",
            json={
                "subject": "Toán",
                "learning_mode": "in_person",
                "preferred_district": "Quận 1",
                "max_budget_vnd": 200000,
                "time_slots": ["T2-tối"],
            },
        )
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "no_match"
        assert (
            body["message"]
            == "Có gia sư thỏa điều kiện bắt buộc nhưng không đủ dữ liệu để xếp hạng"
        )
        assert body["results"] == []
        assert body["insufficient_data_candidates"] == ["GS-INC-1", "GS-INC-2"]
        assert body["total_candidates"] == 2
        assert body["qualified_candidates"] == 2


class TestRecommendValidationErrors422:
    """Kiểm thử các trường hợp đầu vào không hợp lệ trả về HTTP 422 (Mục 4.3)."""

    @pytest.mark.parametrize(
        "invalid_payload",
        [
            {"learning_mode": "in_person"},  # Thiếu subject
            {"subject": "", "learning_mode": "in_person"},  # subject rỗng
            {"subject": "   ", "learning_mode": "in_person"},  # subject chỉ khoảng trắng
            {"subject": "Toán", "learning_mode": "hybrid"},  # learning_mode ngoài enum
            {"subject": "Toán", "learning_mode": "online", "max_budget_vnd": -1},  # ngân sách âm
            {"subject": "Toán", "learning_mode": "online", "max_budget_vnd": 200000.5},  # ngân sách số thực
            {"subject": "Toán", "learning_mode": "online", "top_k": 0},  # top_k < 1
            {"subject": "Toán", "learning_mode": "online", "top_k": 21},  # top_k > 20
            {"subject": "Toán", "learning_mode": "online", "top_k": 3.5},  # top_k số thực
            {"subject": "Toán", "learning_mode": "online", "top_k": "3"},  # top_k chuỗi
            {"subject": "Toán", "learning_mode": "online", "top_k": True},  # top_k boolean
            {
                "subject": "Toán",
                "learning_mode": "online",
                "priorities": {"fee": "urgent"},
            },  # mức ưu tiên ngoài enum
            {
                "subject": "Toán",
                "learning_mode": "online",
                "priorities": {"unknown_criterion": "high"},
            },  # khóa tiêu chí lạ
            {
                "subject": "Toán",
                "learning_mode": "online",
                "extra_field": 123,
            },  # trường lạ ngoài hợp đồng
        ],
    )
    def test_invalid_inputs_return_422(
        self, client: TestClient, invalid_payload: dict[str, Any]
    ) -> None:
        response = client.post("/api/recommend", json=invalid_payload)
        assert response.status_code == 422


class TestCorsAndOpenApiDocs:
    """Kiểm thử cấu hình CORS và tài liệu Swagger UI (/docs, /openapi.json — Issue #24)."""

    def test_cors_preflight_allows_frontend_origin(self, client: TestClient) -> None:
        response = client.options(
            "/api/recommend",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type",
            },
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers

    def test_openapi_schema_and_swagger_ui_available(self, client: TestClient) -> None:
        health_resp = client.get("/health")
        assert health_resp.status_code == 200
        assert health_resp.json() == {"status": "ok"}

        docs_resp = client.get("/docs")
        assert docs_resp.status_code == 200

        openapi_resp = client.get("/openapi.json")
        assert openapi_resp.status_code == 200
        schema = openapi_resp.json()
        assert "/api/recommend" in schema["paths"]
        assert "post" in schema["paths"]["/api/recommend"]
