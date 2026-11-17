"""Đo hiệu năng xử lý nội tại (in-process) của endpoint POST /api/recommend qua TestClient."""

from __future__ import annotations

import json
import statistics
import sys
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = REPO_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

# Phiên đo chuẩn được ghi nhận trong Báo cáo (Chương 5, Mục 5.1.2)
RECORDED_SESSION: dict[str, float] = {
    "mean_140_ms": 3.54,
    "max_140_ms": 7.97,
    "mean_700_ms": 3.72,
    "max_700_ms": 26.64,
    "sla_limit_ms": 1000.0,
}


def _measure_rounds(
    client: TestClient,
    scenarios: list[dict[str, Any]],
    rounds: int,
) -> dict[str, float]:
    latencies_ms: list[float] = []
    for _ in range(rounds):
        for sc in scenarios:
            t0 = time.perf_counter()
            resp = client.post("/api/recommend", json=sc["request"])
            dt_ms = (time.perf_counter() - t0) * 1000.0
            if resp.status_code != 200:
                raise RuntimeError(
                    f"Kịch bản {sc['id']} trả về HTTP {resp.status_code} khi benchmark."
                )
            latencies_ms.append(dt_ms)

    sorted_vals = sorted(latencies_ms)
    p95_idx = max(0, int(0.95 * len(sorted_vals)) - 1)
    return {
        "calls": float(len(latencies_ms)),
        "mean_ms": round(statistics.mean(latencies_ms), 2),
        "median_ms": round(statistics.median(latencies_ms), 2),
        "p95_ms": round(sorted_vals[p95_idx], 2),
        "max_ms": round(max(latencies_ms), 2),
    }


def run_benchmark(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    """Thực thi warm-up, đo 140 lượt (10x14) và 700 lượt (50x14) qua TestClient."""
    scenarios_path = repo_root / "backend" / "tests" / "scenarios" / "scenarios.json"
    scenarios = json.loads(scenarios_path.read_text(encoding="utf-8"))

    with TestClient(app) as client:
        # Khởi động warm-up 1 vòng để loại trừ trễ nạp lần đầu
        _measure_rounds(client, scenarios, rounds=1)
        stats_140 = _measure_rounds(client, scenarios, rounds=10)
        stats_700 = _measure_rounds(client, scenarios, rounds=50)

    sla_limit = RECORDED_SESSION["sla_limit_ms"]
    sla_passed = stats_140["max_ms"] < sla_limit and stats_700["max_ms"] < sla_limit
    return {
        "mean_140_ms": stats_140["mean_ms"],
        "max_140_ms": stats_140["max_ms"],
        "p95_140_ms": stats_140["p95_ms"],
        "mean_700_ms": stats_700["mean_ms"],
        "max_700_ms": stats_700["max_ms"],
        "p95_700_ms": stats_700["p95_ms"],
        "recorded_session": dict(RECORDED_SESSION),
        "sla_passed": sla_passed,
    }


def main() -> int:
    result = run_benchmark()
    print(
        f"140 calls: mean={result['mean_140_ms']} ms, p95={result['p95_140_ms']} ms, max={result['max_140_ms']} ms"
    )
    print(
        f"700 calls: mean={result['mean_700_ms']} ms, p95={result['p95_700_ms']} ms, max={result['max_700_ms']} ms"
    )
    print(f"SLA (< {RECORDED_SESSION['sla_limit_ms']} ms): {'PASS' if result['sla_passed'] else 'FAIL'}")
    return 0 if result["sla_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
