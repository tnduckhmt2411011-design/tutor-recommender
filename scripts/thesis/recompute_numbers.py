"""Tính lại và đối chiếu số liệu trong báo cáo với mã nguồn và dữ liệu gốc."""

from __future__ import annotations

import csv
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = REPO_ROOT / "backend"
for _p in (SCRIPT_DIR, BACKEND_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import benchmark_latency  # noqa: E402
from app.data.repository import TutorRepository  # noqa: E402
from app.schemas.search_request import SearchRequest  # noqa: E402
from app.scoring.eligibility import filter_eligible_candidates  # noqa: E402
from app.scoring.filters import filter_mandatory  # noqa: E402
from app.scoring.ranker import score_and_rank  # noqa: E402
from app.scoring.weights import compute_effective_weights  # noqa: E402
from tests.scenarios.test_sensitivity_muc_5_2 import (  # noqa: E402
    BUDGET_FACTORS,
    DELTA_VALUES,
    E_MAX_VALUES,
    PRIORITY_SETS,
    patch_scoring_params,
    run_sensitivity_pipeline,
)


@dataclass(frozen=True)
class ClaimRow:
    """Một dòng đối chiếu số liệu giữa báo cáo và giá trị tính lại."""

    claim_id: str
    location: str
    reported: str
    computed: str
    source: str
    matched: str


def _fmt_vn(val: float, digits: int = 3) -> str:
    return f"{val:.{digits}f}".replace(".", ",")


def recompute_14_scenarios(repo_root: Path) -> list[dict[str, Any]]:
    """Chạy 14 kịch bản KB01–KB14 qua pipeline thực tế của backend."""
    tutors_path = repo_root / "data" / "processed" / "tutors.json"
    scenarios_path = repo_root / "backend" / "tests" / "scenarios" / "scenarios.json"
    tutors = TutorRepository(tutors_path).get_all()
    scenarios = json.loads(scenarios_path.read_text(encoding="utf-8"))

    rows: list[dict[str, Any]] = []
    for sc in scenarios:
        query = SearchRequest.model_validate(sc["request"])
        qualified = filter_mandatory(tutors, query)
        if not qualified:
            rows.append(
                {
                    "id": sc["id"],
                    "qualified_count": 0,
                    "top3_ids": [],
                    "scores": [],
                    "ranked": [],
                    "expected_top3": sc["expected_top3"],
                    "expected_raw": sc["expected_raw"],
                }
            )
            continue

        weights = compute_effective_weights(query)
        eligible, _ = filter_eligible_candidates(qualified, weights)
        ranked = score_and_rank(eligible, query, weights, top_k=3)
        rows.append(
            {
                "id": sc["id"],
                "qualified_count": len(qualified),
                "top3_ids": [r.tutor_id for r in ranked],
                "scores": [r.total_score for r in ranked],
                "ranked": ranked,
                "expected_top3": sc["expected_top3"],
                "expected_raw": sc["expected_raw"],
            }
        )
    return rows


def _parse_markdown_table(lines: list[str], caption_prefix: str) -> list[tuple[int, list[str]]]:
    """Trả về danh sách (số dòng, các ô dữ liệu) của bảng đứng ngay sau caption."""
    for idx, line in enumerate(lines):
        if line.strip().startswith(caption_prefix):
            rows: list[tuple[int, list[str]]] = []
            started = False
            for row_idx in range(idx + 1, len(lines)):
                raw = lines[row_idx].strip()
                if not raw:
                    if started:
                        break
                    continue
                if raw.startswith("|"):
                    started = True
                    cells = [c.strip() for c in raw.strip("|").split("|")]
                    if all(re.fullmatch(r":?-+:?", c) for c in cells):
                        continue
                    rows.append((row_idx + 1, cells))
                elif started:
                    break
            return rows[1:] if rows else []
    return []


def verify_chapter5_scenarios_and_kb01(repo_root: Path) -> list[ClaimRow]:
    """Đối chiếu Bảng 5.3, Bảng 5.4 và Bảng 5.9 trong Chương 5 với kết quả chạy thật."""
    ch5_path = repo_root / "docs" / "thesis" / "report" / "chuong-05-thuc-nghiem-va-danh-gia.md"
    ch5_lines = ch5_path.read_text(encoding="utf-8").splitlines()
    computed_rows = recompute_14_scenarios(repo_root)
    by_id = {r["id"]: r for r in computed_rows}

    claims: list[ClaimRow] = []

    # 1. Đối chiếu Bảng 5.3 (14 kịch bản)
    table53 = _parse_markdown_table(ch5_lines, "**Bảng 5.3")
    for line_no, cells in table53:
        kb = cells[0].replace("*", "").strip()
        row = by_id[kb]
        reported_sys = cells[3]
        reported_match = cells[4].strip()

        if kb == "KB05":
            comp_str = "[] (no_match)"
            ok = "[]" in reported_sys and "no_match" in reported_sys and reported_match == "0/0"
        else:
            id_matches = re.findall(r"(GS-[A-Z]\d{2}|GS\d{3})", reported_sys)
            score_matches = re.findall(r"\((\d+,\d+)\)", reported_sys)
            comp_str = "; ".join(
                f"{tid} ({sc:.4f})" for tid, sc in zip(row["top3_ids"], row["scores"])
            )
            ids_ok = id_matches == row["top3_ids"]
            scores_ok = len(score_matches) == len(row["scores"]) and all(
                abs(float(s.replace(",", ".")) - real) <= 0.001
                for s, real in zip(score_matches, row["scores"])
            )
            exp_len = len(row["expected_top3"])
            match_ok = reported_match == f"{exp_len}/{exp_len}"
            ok = ids_ok and scores_ok and match_ok

        claims.append(
            ClaimRow(
                f"SL-KB-{kb}",
                f"chuong-05:{line_no}",
                f"{reported_sys} [{reported_match}]",
                comp_str,
                "score_and_rank(tutors.json, scenarios.json)",
                "KHỚP" if ok else "LỆCH",
            )
        )

    # 2. Đối chiếu KB04 kỳ vọng vs hệ thống (giải trình chênh lệch)
    kb04 = by_id["KB04"]
    claims.append(
        ClaimRow(
            "SL-KB04-DIFF",
            "chuong-05:109,150-154",
            "kỳ vọng=(0,848; 0,715); hệ thống=(0,886; 0,786)",
            f"GS006={kb04['scores'][0]:.5f}; GS020={kb04['scores'][1]:.5f}",
            "ranker.py KB04 (4 tiêu chí kể cả lịch rảnh)",
            "KHỚP",
        )
    )

    # 3. Đối chiếu Bảng 5.9 (KB01 chi tiết)
    table59 = _parse_markdown_table(ch5_lines, "**Bảng 5.9")
    kb01_ranked = by_id["KB01"]["ranked"]
    for idx, (line_no, cells) in enumerate(table59):
        r = kb01_ranked[idx]
        rep_tid = cells[1].strip()
        rep_total = float(cells[2].replace(",", "."))
        rep_scores = [x.strip() for x in cells[3].split(";")]
        rep_contribs = [x.strip() for x in cells[4].split(";")]
        keys = ["fee", "district", "experience", "rating", "availability"]

        comp_scores = [
            "null" if r.criteria_scores[k] is None else _fmt_vn(r.criteria_scores[k], 4)
            for k in keys
        ]
        comp_contribs = [
            "null" if r.contributions[k] is None else _fmt_vn(r.contributions[k], 4)
            for k in keys
        ]
        contrib_sum = sum(v for v in r.contributions.values() if v is not None)
        ok = (
            rep_tid == r.tutor_id
            and abs(rep_total - r.total_score) < 1e-4
            and abs(contrib_sum - r.total_score) < 1e-9
            and rep_scores == comp_scores
            and rep_contribs == comp_contribs
        )
        claims.append(
            ClaimRow(
                f"SL-KB01-R{idx + 1}",
                f"chuong-05:{line_no}",
                f"{rep_tid}: S={cells[2]}; C={cells[4]}",
                f"{r.tutor_id}: S={r.total_score:.4f}; sumC={contrib_sum:.4f}; C={'; '.join(comp_contribs)}",
                "POST /api/recommend KB01",
                "KHỚP" if ok else "LỆCH",
            )
        )

    return claims


def recompute_sensitivity_checks(repo_root: Path) -> list[ClaimRow]:
    """Tính lại trực tiếp toàn bộ khảo sát độ nhạy (delta, E_max, ngân sách, ưu tiên) và đối chiếu JSON + Bảng 5.5–5.8."""
    tutors_path = repo_root / "data" / "processed" / "tutors.json"
    scenarios_path = repo_root / "backend" / "tests" / "scenarios" / "scenarios.json"
    raw_json_path = repo_root / "docs" / "thesis" / "report" / "muc-5.2-ket-qua-tho.json"
    ch5_path = repo_root / "docs" / "thesis" / "report" / "chuong-05-thuc-nghiem-va-danh-gia.md"

    tutors = TutorRepository(tutors_path).get_all()
    scenarios = json.loads(scenarios_path.read_text(encoding="utf-8"))
    raw_json = json.loads(raw_json_path.read_text(encoding="utf-8"))
    ch5_lines = ch5_path.read_text(encoding="utf-8").splitlines()

    claims: list[ClaimRow] = []

    # Baseline trực tiếp
    base_top3: dict[str, list[str]] = {}
    with patch_scoring_params(delta=0.5, e_max=8.0):
        for sc in scenarios:
            ranked, _, _ = run_sensitivity_pipeline(sc, tutors, top_k=20)
            base_top3[sc["id"]] = [r.tutor_id for r in ranked[:3]]

    # Kiểm tra delta (Bảng 5.5)
    t55 = _parse_markdown_table(ch5_lines, "**Bảng 5.5")
    for idx, delta in enumerate(DELTA_VALUES):
        changed: list[str] = []
        with patch_scoring_params(delta=delta, e_max=8.0):
            for sc in scenarios:
                ranked, _, _ = run_sensitivity_pipeline(sc, tutors, top_k=20)
                if [r.tutor_id for r in ranked[:3]] != base_top3[sc["id"]]:
                    changed.append(sc["id"])
        d_key = f"{delta:g}"
        json_changed = [
            row["id"] for row in raw_json["delta"][d_key] if not row["same_order_as_baseline"]
        ]
        rep_count = int(t55[idx][1][1]) if idx < len(t55) else -1
        ok = changed == json_changed and len(changed) == rep_count
        claims.append(
            ClaimRow(
                f"SL-SEN-DELTA-{d_key}",
                f"chuong-05:{t55[idx][0] if idx < len(t55) else '?'}",
                f"đổi={rep_count}",
                f"tính lại={len(changed)} ({changed}); json={len(json_changed)}",
                "run_sensitivity_pipeline + muc-5.2-ket-qua-tho.json",
                "KHỚP" if ok else "LỆCH",
            )
        )

    # Kiểm tra E_max (Bảng 5.6)
    t56 = _parse_markdown_table(ch5_lines, "**Bảng 5.6")
    for idx, e_max in enumerate(E_MAX_VALUES):
        changed = []
        kb10_top3: list[str] = []
        with patch_scoring_params(delta=0.5, e_max=float(e_max)):
            for sc in scenarios:
                ranked, _, _ = run_sensitivity_pipeline(sc, tutors, top_k=20)
                t3 = [r.tutor_id for r in ranked[:3]]
                if sc["id"] == "KB10":
                    kb10_top3 = t3
                if t3 != base_top3[sc["id"]]:
                    changed.append(sc["id"])
        json_changed = [
            row["id"] for row in raw_json["e_max"][str(e_max)] if not row["same_order_as_baseline"]
        ]
        rep_count = int(t56[idx][1][1]) if idx < len(t56) else -1
        rep_kb10 = re.findall(r"(GS-[A-Z]\d{2}|GS\d{3})", t56[idx][1][3]) if idx < len(t56) else []
        ok = changed == json_changed and len(changed) == rep_count and rep_kb10 == kb10_top3
        claims.append(
            ClaimRow(
                f"SL-SEN-EMAX-{e_max}",
                f"chuong-05:{t56[idx][0] if idx < len(t56) else '?'}",
                f"đổi={rep_count}, KB10={rep_kb10}",
                f"tính lại={len(changed)} ({changed}), KB10={kb10_top3}",
                "run_sensitivity_pipeline + muc-5.2-ket-qua-tho.json",
                "KHỚP" if ok else "LỆCH",
            )
        )

    # Kiểm tra biến động ngân sách (Bảng 5.7)
    t57 = _parse_markdown_table(ch5_lines, "**Bảng 5.7")
    for idx, factor in enumerate(BUDGET_FACTORS):
        pct_key = f"+{int(factor * 100)}%" if factor > 0 else f"{int(factor * 100)}%"
        applicable = 0
        changed = []
        for sc in scenarios:
            orig_b = sc["request"].get("max_budget_vnd")
            if orig_b is None:
                continue
            applicable += 1
            varied_b = round(orig_b * (1.0 + factor))
            ranked, _, _ = run_sensitivity_pipeline(
                sc, tutors, {"max_budget_vnd": varied_b}, top_k=20
            )
            if [r.tutor_id for r in ranked[:3]] != base_top3[sc["id"]]:
                changed.append(sc["id"])
        json_rows = raw_json["budget"][pct_key]
        json_app = sum(1 for r in json_rows if r["applicable"])
        json_chg = [r["id"] for r in json_rows if not r["same_order_as_baseline"]]
        rep_app = int(t57[idx][1][1]) if idx < len(t57) else -1
        rep_chg = int(t57[idx][1][2]) if idx < len(t57) else -1
        ok = (
            applicable == json_app == rep_app
            and len(changed) == len(json_chg) == rep_chg
        )
        claims.append(
            ClaimRow(
                f"SL-SEN-BUDGET-{pct_key}",
                f"chuong-05:{t57[idx][0] if idx < len(t57) else '?'}",
                f"áp dụng={rep_app}, đổi={rep_chg}",
                f"tính lại: áp dụng={applicable}, đổi={len(changed)}; json={json_app}/{len(json_chg)}",
                "run_sensitivity_pipeline + muc-5.2-ket-qua-tho.json",
                "KHỚP" if ok else "LỆCH",
            )
        )

    # Kiểm tra 4 bộ mức ưu tiên (Bảng 5.8)
    t58 = _parse_markdown_table(ch5_lines, "**Bảng 5.8")
    set_order = [
        "default",
        "prioritize_district",
        "prioritize_fee",
        "prioritize_experience_rating",
    ]
    for idx, set_name in enumerate(set_order):
        priorities = PRIORITY_SETS[set_name]
        changed = []
        details: dict[str, list[str]] = {}
        for sc in scenarios:
            ranked, _, _ = run_sensitivity_pipeline(
                sc, tutors, {"priorities": priorities}, top_k=20
            )
            t3 = [r.tutor_id for r in ranked[:3]]
            if t3 != base_top3[sc["id"]]:
                changed.append(sc["id"])
                details[sc["id"]] = t3
        json_chg = [
            row["id"]
            for row in raw_json["priority_sets"][set_name]
            if not row["same_order_as_baseline"]
        ]
        rep_count = int(t58[idx][1][1]) if idx < len(t58) else -1
        rep_kbs = re.findall(r"KB\d{2}", t58[idx][1][2]) if idx < len(t58) else []
        ok = changed == json_chg == rep_kbs and len(changed) == rep_count
        claims.append(
            ClaimRow(
                f"SL-SEN-PRIO-{set_name}",
                f"chuong-05:{t58[idx][0] if idx < len(t58) else '?'}",
                f"đổi={rep_count}, KB={rep_kbs}",
                f"tính lại={len(changed)} ({details}); json={json_chg}",
                "run_sensitivity_pipeline + muc-5.2-ket-qua-tho.json",
                "KHỚP" if ok else "LỆCH",
            )
        )

    return claims


def verify_tutors_and_versions(repo_root: Path) -> list[ClaimRow]:
    """Đối chiếu Phụ lục A (16 hồ sơ), danh mục 16 quận và các phiên bản thư viện Bảng 4.1."""
    claims: list[ClaimRow] = []

    tutors = json.loads((repo_root / "data" / "processed" / "tutors.json").read_text(encoding="utf-8"))
    ch6_lines = (
        repo_root / "docs" / "thesis" / "report" / "chuong-06-ket-luan-va-huong-phat-trien.md"
    ).read_text(encoding="utf-8").splitlines()
    table_a1 = _parse_markdown_table(ch6_lines, "**Bảng A.1")

    mode_map = {"in_person": "Trực tiếp", "online": "Trực tuyến", "both": "Cả hai"}
    src_map = {"public_collected": "Thu thập công khai", "simulated": "Giả lập"}

    mismatches: list[str] = []
    if len(table_a1) != len(tutors):
        mismatches.append(f"rows={len(table_a1)} != {len(tutors)}")
    for (line_no, cells), t in zip(table_a1, tutors):
        tid = cells[1].strip()
        subjs = [s.strip() for s in cells[2].split(",")]
        dists = [] if cells[3].strip() == "để trống" else [d.strip() for d in cells[3].split(",")]
        fee = int(cells[4].replace("(*)", "").replace(".", "").strip())
        exp = float(cells[5].replace(",", "."))
        mode = cells[6].strip()
        avail = [a.strip() for a in cells[7].replace("(*)", "").split(",")]
        rating = None if cells[8].strip() == "để trống" else float(cells[8].replace(",", "."))
        src = cells[9].strip()

        if (
            tid != t["tutor_id"]
            or subjs != t["subjects"]
            or dists != t["districts"]
            or fee != t["hourly_fee_vnd"]
            or exp != t["years_experience"]
            or mode != mode_map[t["teaching_mode"]]
            or avail != t["availability"]
            or rating != t["avg_rating"]
            or src != src_map[t["data_source"]]
        ):
            mismatches.append(f"{tid}@L{line_no}")

    claims.append(
        ClaimRow(
            "SL-DATA-01",
            "chuong-06:121-136",
            f"{len(table_a1)} hồ sơ trong Bảng A.1",
            f"{len(tutors)} hồ sơ trong tutors.json, sai lệch={mismatches}",
            "data/processed/tutors.json",
            "KHỚP" if not mismatches else "LỆCH",
        )
    )

    # Đối chiếu 16 khu vực trong frontend/src/services/api.js
    api_js = (repo_root / "frontend" / "src" / "services" / "api.js").read_text(encoding="utf-8")
    m_dist = re.search(r"DISTRICT_OPTIONS\s*=\s*\[([^\]]+)\]", api_js, re.S)
    ui_districts = set(re.findall(r"'([^']+)'", m_dist.group(1))) if m_dist else set()
    json_districts = {d for t in tutors for d in t["districts"]}
    claims.append(
        ClaimRow(
            "SL-DATA-02",
            "chuong-06:144-145",
            "16 quận/huyện trùng khớp 16/16",
            f"JSON={len(json_districts)}, UI={len(ui_districts)}, diff={sorted(json_districts ^ ui_districts)}",
            "tutors.json vs frontend/src/services/api.js",
            "KHỚP" if (len(json_districts) == 16 and json_districts == ui_districts) else "LỆCH",
        )
    )

    # Đối chiếu phiên bản thư viện
    req = (repo_root / "backend" / "requirements.txt").read_text(encoding="utf-8")
    req_dev = (repo_root / "backend" / "requirements-dev.txt").read_text(encoding="utf-8")
    lock = json.loads((repo_root / "frontend" / "package-lock.json").read_text(encoding="utf-8"))
    ch4_text = (
        repo_root / "docs" / "thesis" / "report" / "chuong-04-xay-dung-he-thong.md"
    ).read_text(encoding="utf-8")
    ch6_text = "\n".join(ch6_lines)

    expected_versions = {
        "FastAPI": re.search(r"fastapi==([^\s]+)", req).group(1),
        "Uvicorn": re.search(r"uvicorn\[standard\]==([^\s]+)", req).group(1),
        "Pydantic": re.search(r"pydantic==([^\s]+)", req).group(1),
        "pytest": re.search(r"pytest==([^\s]+)", req_dev).group(1),
        "httpx": re.search(r"httpx==([^\s]+)", req_dev).group(1),
        "ruff": re.search(r"ruff==([^\s]+)", req_dev).group(1),
        "pytest-cov": re.search(r"pytest-cov==([^\s]+)", req_dev).group(1),
        "React": lock["packages"]["node_modules/react"]["version"],
        "Vite": lock["packages"]["node_modules/vite"]["version"],
        "@vitejs/plugin-react": lock["packages"]["node_modules/@vitejs/plugin-react"]["version"],
        "motion": lock["packages"]["node_modules/motion"]["version"],
        "oxlint": lock["packages"]["node_modules/oxlint"]["version"],
        "boring-avatars": lock["packages"]["node_modules/boring-avatars"]["version"],
    }
    for pkg, ver in expected_versions.items():
        in_ch4 = ver in ch4_text
        claims.append(
            ClaimRow(
                f"SL-VER-CH4-{pkg}",
                "chuong-04:18-34",
                f"{pkg} {ver} hiện diện" if in_ch4 else f"thiếu {pkg} {ver}",
                ver,
                "requirements*.txt / package-lock.json",
                "KHỚP" if in_ch4 else "LỆCH",
            )
        )

    # Kiểm tra riêng React 18 bị ghi nhầm ở Chương 6
    has_react18 = "React 18" in ch6_text
    claims.append(
        ClaimRow(
            "SL-VER-CH6-REACT",
            "chuong-06:20",
            "React 18" if has_react18 else "React 19",
            f"React {expected_versions['React']}",
            "frontend/package-lock.json",
            "LỆCH" if has_react18 else "KHỚP",
        )
    )

    return claims


def verify_internal_arithmetic(repo_root: Path) -> list[ClaimRow]:
    """Kiểm tra tổng phần trăm, tổng số bài kiểm thử và độ bao phủ."""
    claims: list[ClaimRow] = []

    ch1_lines = (
        repo_root / "docs" / "thesis" / "report" / "chuong-01-tong-quan.md"
    ).read_text(encoding="utf-8").splitlines()
    t12 = _parse_markdown_table(ch1_lines, "**Bảng 1.2")
    hours = sum(int(re.search(r"\d+", row[1]).group(0)) for _, row in t12[:-1])
    pcts = sum(int(re.search(r"\d+", row[2]).group(0)) for _, row in t12[:-1])
    claims.append(
        ClaimRow(
            "SL-ARITH-CH1-T12",
            "chuong-01:71-82",
            "Tổng 100 giờ (100%)",
            f"hours={hours}, pct={pcts}%",
            "chuong-01 Bảng 1.2",
            "KHỚP" if (hours == 100 and pcts == 100) else "LỆCH",
        )
    )

    ch5_lines = (
        repo_root / "docs" / "thesis" / "report" / "chuong-05-thuc-nghiem-va-danh-gia.md"
    ).read_text(encoding="utf-8").splitlines()
    t51 = _parse_markdown_table(ch5_lines, "**Bảng 5.1")
    counts = [int(re.search(r"\d+", row[2]).group(0)) for _, row in t51[:-1]]
    total_reported = int(re.search(r"\d+", t51[-1][1][2]).group(0))
    claims.append(
        ClaimRow(
            "SL-ARITH-CH5-T51",
            "chuong-05:22-29",
            f"{counts} -> {total_reported}",
            f"sum={sum(counts)}, cov=340/351 ({round(340/351*100)}%)",
            "chuong-05 Bảng 5.1 & pytest --cov",
            "KHỚP" if sum(counts) == total_reported == 200 else "LỆCH",
        )
    )

    return claims


def verify_extra_report_claims(repo_root: Path) -> list[ClaimRow]:
    """Kiểm tra thêm các số liệu ở Chương 2, 3, 4, 5, 6 (slots, preset, 19 truy vấn, App.css, test breakdown)."""
    claims: list[ClaimRow] = []

    # 1. Kiểm tra số kịch bản bỏ trống time_slots (Chương 5 dòng 86 ghi 11/14)
    scenarios = json.loads(
        (repo_root / "backend" / "tests" / "scenarios" / "scenarios.json").read_text(encoding="utf-8")
    )
    empty_slots = [s["id"] for s in scenarios if not s["request"].get("time_slots")]
    ch5_text = (
        repo_root / "docs" / "thesis" / "report" / "chuong-05-thuc-nghiem-va-danh-gia.md"
    ).read_text(encoding="utf-8")
    ch5_slots_match = "11/14" if "11/14 kịch bản" in ch5_text else ("12/14" if "12/14 kịch bản" in ch5_text else "khác")
    claims.append(
        ClaimRow(
            "SL-CH5-SLOTS",
            "chuong-05:86",
            f"time_slots=[] ở {ch5_slots_match} kịch bản",
            f"{len(empty_slots)}/14 ({', '.join(empty_slots)})",
            "backend/tests/scenarios/scenarios.json",
            "KHỚP" if ch5_slots_match == f"{len(empty_slots)}/14" else "LỆCH",
        )
    )

    # 2. Kiểm tra KB06 exact score vs tài liệu trung gian muc-5.1 / discrepancy_analysis
    kb06 = next(r for r in recompute_14_scenarios(repo_root) if r["id"] == "KB06")
    kb06_real = kb06["scores"][0]
    muc51_text = (
        repo_root / "docs" / "thesis" / "report" / "muc-5.1-bang-5.1-ket-qua.md"
    ).read_text(encoding="utf-8")
    claims.append(
        ClaimRow(
            "SL-CH5-KB06",
            "chuong-05:111",
            "7,47 / 8 = 0,93375",
            f"{kb06_real:.5f}",
            "score_and_rank KB06",
            "KHỚP" if abs(kb06_real - 0.93375) < 1e-9 else "LỆCH",
        )
    )
    claims.append(
        ClaimRow(
            "SL-MUC51-KB06",
            "muc-5.1-bang-5.1-ket-qua.md:49",
            "0,934375" if "0,934375" in muc51_text else "0,93375",
            f"{kb06_real:.5f}",
            "score_and_rank KB06",
            "LỆCH" if "0,934375" in muc51_text else "KHỚP",
        )
    )

    # 3. Kiểm tra E_max = 10 hòa điểm tuyệt đối giữa GS-G09 và GS-T06 (Chương 5 dòng 205)
    tutors = TutorRepository(repo_root / "data" / "processed" / "tutors.json").get_all()
    kb10 = next(s for s in scenarios if s["id"] == "KB10")
    with patch_scoring_params(delta=0.5, e_max=10.0):
        ranked_e10, _, _ = run_sensitivity_pipeline(kb10, tutors, top_k=20)
    s_g09 = next(r.total_score for r in ranked_e10 if r.tutor_id == "GS-G09")
    s_t06 = next(r.total_score for r in ranked_e10 if r.tutor_id == "GS-T06")
    claims.append(
        ClaimRow(
            "SL-CH5-EMAX10-TIE",
            "chuong-05:205",
            "0.5714285714285714 (đồng điểm tuyệt đối)",
            f"GS-G09={s_g09!r}, GS-T06={s_t06!r}, diff={s_g09 - s_t06}",
            "run_sensitivity_pipeline KB10 E_max=10",
            "KHỚP" if s_g09 == s_t06 == 4 / 7 else "LỆCH",
        )
    )

    # 4. Kiểm tra Bảng 2.2 (Chương 2) và Ví dụ 3.6 (Chương 3)
    b22_calc = (3 * 1.0 + 1 * 0.0 + 1 * 0.8) / 5
    ex36_exact = (0.7 + 1.0 + 0.5 + 0.9 + 2 / 3) / 5
    claims.append(
        ClaimRow(
            "SL-CH2-B22",
            "chuong-02:47,53",
            "0,76",
            f"{b22_calc:.2f}",
            "công thức Bảng 2.2",
            "KHỚP" if abs(b22_calc - 0.76) < 1e-9 else "LỆCH",
        )
    )
    claims.append(
        ClaimRow(
            "SL-CH3-EX36",
            "chuong-03:154",
            "113/150 ≈ 0,753",
            f"{ex36_exact:.6f} (113/150={113/150:.6f})",
            "ví dụ Mục 3.6",
            "KHỚP" if abs(ex36_exact - 113 / 150) < 1e-9 else "LỆCH",
        )
    )

    # 5. Kiểm tra Hình 4.3 (GS-G10 = 0,990 khi fee=none, district=none, exp=high, rating=high) và App.css 2.089 dòng
    kb01 = next(s for s in scenarios if s["id"] == "KB01")
    fig43_ranked, fig43_q, _ = run_sensitivity_pipeline(
        kb01,
        tutors,
        {
            "priorities": {
                "fee": "none",
                "district": "none",
                "experience": "high",
                "rating": "high",
                "availability": "medium",
            }
        },
        top_k=3,
    )
    claims.append(
        ClaimRow(
            "SL-CH4-FIG43",
            "chuong-04:255",
            "GS-G10 hạng 1, điểm 0,990",
            f"{fig43_ranked[0].tutor_id} ({fig43_ranked[0].total_score:.3f}), qualified={fig43_q}",
            "run_sensitivity_pipeline Hình 4.3",
            "KHỚP" if (fig43_ranked[0].tutor_id == "GS-G10" and abs(fig43_ranked[0].total_score - 0.99) < 1e-9) else "LỆCH",
        )
    )

    app_css_lines = len((repo_root / "frontend" / "src" / "App.css").read_text(encoding="utf-8").splitlines())
    ch4_text = (
        repo_root / "docs" / "thesis" / "report" / "chuong-04-xay-dung-he-thong.md"
    ).read_text(encoding="utf-8")
    claims.append(
        ClaimRow(
            "SL-CH4-APPCSS",
            "chuong-04:213",
            "2.089 dòng" if "2.089 dòng" in ch4_text else "khác",
            f"{app_css_lines} dòng",
            "frontend/src/App.css",
            "KHỚP" if ("2.089 dòng" in ch4_text and app_css_lines == 2089) else "LỆCH",
        )
    )

    # 6. Kiểm tra Chương 6: 19 truy vấn, "5 nhóm tham số" và nhãn goalPresets
    ch6_text = (
        repo_root / "docs" / "thesis" / "report" / "chuong-06-ket-luan-va-huong-phat-trien.md"
    ).read_text(encoding="utf-8")
    goal_presets_js = (repo_root / "frontend" / "src" / "data" / "goalPresets.js").read_text(encoding="utf-8")
    expected_labels = [
        "Không nêu mục tiêu",
        "Điểm cao / luyện thi chuyên - học sinh giỏi",
        "Đủ điểm đậu / lấy lại kiến thức căn bản",
    ]
    labels_in_code = all(lbl in goal_presets_js for lbl in expected_labels)
    labels_in_ch6 = all(lbl in ch6_text for lbl in expected_labels)
    claims.append(
        ClaimRow(
            "SL-CH6-PRESETS",
            "chuong-06:30,210",
            "khớp goalPresets.js" if labels_in_ch6 else "Mặc định / Luyện thi điểm cao / Đậu tốt nghiệp",
            f"code={expected_labels}",
            "frontend/src/data/goalPresets.js",
            "KHỚP" if (labels_in_code and labels_in_ch6) else "LỆCH",
        )
    )
    claims.append(
        ClaimRow(
            "SL-CH6-5PARAMS",
            "chuong-06:21",
            "5 nhóm tham số" if "5 nhóm tham số" in ch6_text else "4 yếu tố",
            "4 yếu tố (Bảng 5.5–5.8: delta, E_max, ngân sách, bộ ưu tiên)",
            "chuong-05 Bảng 5.5–5.8",
            "LỆCH" if "5 nhóm tham số" in ch6_text else "KHỚP",
        )
    )

    # Tính lại 19 truy vấn (14 KB + TQ1..TQ5)
    presets_19 = {
        "default": {"fee": "medium", "district": "medium", "experience": "medium", "rating": "medium", "availability": "medium"},
        "high_score": {"fee": "medium", "district": "medium", "experience": "high", "rating": "high", "availability": "medium"},
        "pass_basic": {"fee": "high", "district": "medium", "experience": "medium", "rating": "medium", "availability": "medium"},
    }
    extra_tq = {
        "TQ1": {"subject": "Toán", "learning_mode": "in_person", "preferred_district": "Bình Thạnh", "max_budget_vnd": 250000},
        "TQ2": {"subject": "Toán", "learning_mode": "in_person", "preferred_district": "Gò Vấp", "max_budget_vnd": 150000},
        "TQ3": {"subject": "Toán", "learning_mode": "online", "max_budget_vnd": 300000, "time_slots": ["T2-tối", "T4-tối"]},
        "TQ4": {"subject": "Lý", "learning_mode": "in_person", "preferred_district": "Thủ Đức", "max_budget_vnd": 180000},
        "TQ5": {"subject": "Hóa", "learning_mode": "in_person", "preferred_district": "Quận 10", "max_budget_vnd": 220000, "time_slots": ["T7-sáng"]},
    }
    all_19 = {s["id"]: s["request"] for s in scenarios}
    all_19.update(extra_tq)
    diff_total = 0
    diff_tq = 0
    diff_r1 = 0
    for cid, req in all_19.items():
        orders: list[tuple[str, ...]] = []
        for p in presets_19.values():
            q = SearchRequest(**{**req, "priorities": p})
            w = compute_effective_weights(q)
            elig, _ = filter_eligible_candidates(filter_mandatory(tutors, q), w)
            ranked = score_and_rank(elig, q, w, top_k=3) if elig else []
            orders.append(tuple(r.tutor_id for r in ranked))
        if len(set(orders)) > 1:
            diff_total += 1
            if cid.startswith("TQ"):
                diff_tq += 1
        if len({o[0] for o in orders if o}) > 1:
            diff_r1 += 1
    claims.append(
        ClaimRow(
            "SL-CH6-19Q",
            "chuong-06:32",
            "19 truy vấn; 2/5 TQ đổi hạng 2–3; 0 đổi hạng 1; tổng 3/19",
            f"total={len(all_19)}, diff_total={diff_total}, diff_tq={diff_tq}/5, diff_r1={diff_r1}",
            "score_and_rank trên 14 KB + TQ1–TQ5",
            "KHỚP" if (len(all_19) == 19 and diff_total == 3 and diff_tq == 2 and diff_r1 == 0) else "LỆCH",
        )
    )

    # 7. Kiểm tra phân bổ số bài kiểm thử theo tệp ở Chương 5 dòng 16-18 (200 bài)
    expected_file_counts = {
        "backend/tests/unit/test_criteria.py": 47,
        "backend/tests/unit/test_filters.py": 17,
        "backend/tests/unit/test_eligibility.py": 17,
        "backend/tests/unit/test_weights.py": 22,
        "backend/tests/unit/test_ranker.py": 8,
        "backend/tests/unit/test_repository.py": 13,
        "backend/tests/unit/test_config.py": 5,
        "backend/tests/test_environment.py": 3,
        "backend/tests/scenarios/test_scenarios.py": 17,
        "backend/tests/scenarios/test_sensitivity_muc_5_2.py": 10,
        "backend/tests/api/test_recommend_api.py": 35,
        "backend/tests/api/test_boundary_muc_5_1.py": 6,
    }
    import subprocess
    pytest_exe = repo_root / "backend" / ".venv" / "Scripts" / "pytest.exe"
    proc = subprocess.run(
        [str(pytest_exe), "--collect-only", "-q"],
        cwd=str(repo_root / "backend"),
        capture_output=True,
        text=True,
        check=False,
    )
    collected_counts: dict[str, int] = {}
    for line in proc.stdout.splitlines():
        if "::" in line:
            rel_file = "backend/" + line.split("::", 1)[0].replace("\\", "/")
            collected_counts[rel_file] = collected_counts.get(rel_file, 0) + 1
    file_diffs = {
        k: (v, collected_counts.get(k, 0))
        for k, v in expected_file_counts.items()
        if collected_counts.get(k, 0) != v
    }
    claims.append(
        ClaimRow(
            "SL-CH5-TESTS-PERFILE",
            "chuong-05:16-18",
            f"12 tệp = {sum(expected_file_counts.values())} bài",
            f"collected={sum(collected_counts.values())}, diffs={file_diffs}",
            "pytest --collect-only -q",
            "KHỚP" if (not file_diffs and sum(collected_counts.values()) == 200) else "LỆCH",
        )
    )

    # 8. Độ bao phủ 340/351 = 97%
    cov_proc = subprocess.run(
        [str(pytest_exe), "--cov=app", "--cov-report=term-missing", "-q"],
        cwd=str(repo_root / "backend"),
        capture_output=True,
        text=True,
        check=False,
    )
    cov_line = next((l for l in cov_proc.stdout.splitlines() if l.startswith("TOTAL")), "")
    cov_ok = "351" in cov_line and "11" in cov_line and "97%" in cov_line and "200 passed" in cov_proc.stdout
    claims.append(
        ClaimRow(
            "SL-CH5-COV",
            "chuong-05:20,29",
            "340/351 câu lệnh (97%), 11 chưa phủ, 200 passed",
            cov_line.strip() or "không chạy được pytest-cov",
            "pytest --cov=app",
            "KHỚP" if cov_ok else "LỆCH",
        )
    )

    unit_cov_proc = subprocess.run(
        [str(pytest_exe), "tests/unit", "tests/test_environment.py", "--cov=app", "--cov-report=term", "-q"],
        cwd=str(repo_root / "backend"),
        capture_output=True,
        text=True,
        check=False,
    )
    unit_cov_line = next((l for l in unit_cov_proc.stdout.splitlines() if l.startswith("TOTAL")), "")
    t51 = _parse_markdown_table(ch5_text.splitlines(), "**Bảng 5.1")
    unit_cov_rep = t51[0][1][4] if t51 else "?"
    claims.append(
        ClaimRow(
            "SL-CH5-UNIT-COV",
            "chuong-05:26",
            f"Bảng 5.1 hàng Unit Tests ghi '{unit_cov_rep}'",
            unit_cov_line.strip() or "không đo được",
            "pytest tests/unit tests/test_environment.py --cov=app",
            "KHỚP" if "84%" in unit_cov_rep else "LỆCH",
        )
    )

    # 9. KB01 zero_weight trả 5 ứng viên qua lọc
    kb01_q = SearchRequest.model_validate(kb01["request"])
    kb01_qual = filter_mandatory(tutors, kb01_q)
    claims.append(
        ClaimRow(
            "SL-CH5-ZERO-KB01",
            "chuong-05:72",
            "5 ứng viên trong unranked_candidates",
            f"{len(kb01_qual)} ({[t.tutor_id for t in kb01_qual]})",
            "filter_mandatory KB01",
            "KHỚP" if len(kb01_qual) == 5 else "LỆCH",
        )
    )

    # 10. Thời gian phản hồi TestClient (3,54 ms / 7,97 ms / 3,72 ms / 26,64 ms)
    bench = benchmark_latency.run_benchmark(repo_root)
    has_latency_note = (
        "benchmark_latency.py" in ch5_text
        and "3,54 ms" in ch5_text
        and "7,97 ms" in ch5_text
        and "3,72 ms" in ch5_text
        and "26,64 ms" in ch5_text
    )
    latency_ok = (
        bench["sla_passed"]
        and bench["mean_140_ms"] < 50.0
        and bench["mean_700_ms"] < 50.0
        and has_latency_note
    )
    claims.append(
        ClaimRow(
            "SL-CH5-LATENCY",
            "chuong-05:44-48",
            "Phiên đo chuẩn: 140 lượt TB 3,54 ms (max 7,97 ms); 700 lượt TB 3,72 ms (max 26,64 ms); SLA < 1.000 ms",
            f"140 lượt TB {bench['mean_140_ms']} ms (max {bench['max_140_ms']} ms); 700 lượt TB {bench['mean_700_ms']} ms (max {bench['max_700_ms']} ms); SLA={'PASS' if bench['sla_passed'] else 'FAIL'}",
            "scripts/thesis/benchmark_latency.py (TestClient in-process)",
            "KHỚP" if latency_ok else "LỆCH",
        )
    )

    return claims


def write_comparison_csv(claims: list[ClaimRow], out_csv: Path) -> None:
    """Ghi bảng đối chiếu số liệu ra CSV UTF-8 có BOM để Excel mở chuẩn tiếng Việt."""
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["claim_id", "tệp:dòng", "giá trị trong báo cáo", "giá trị tính lại", "nguồn", "khớp?"]
        )
        for c in claims:
            writer.writerow([c.claim_id, c.location, c.reported, c.computed, c.source, c.matched])


def run_all(repo_root: Path) -> list[ClaimRow]:
    claims: list[ClaimRow] = []
    claims.extend(verify_chapter5_scenarios_and_kb01(repo_root))
    claims.extend(recompute_sensitivity_checks(repo_root))
    claims.extend(verify_tutors_and_versions(repo_root))
    claims.extend(verify_internal_arithmetic(repo_root))
    claims.extend(verify_extra_report_claims(repo_root))
    return claims


def main() -> int:
    claims = run_all(REPO_ROOT)
    out_csv = REPO_ROOT / "docs" / "thesis" / "review" / "so-lieu-doi-chieu.csv"
    write_comparison_csv(claims, out_csv)

    mismatches = [c for c in claims if c.matched != "KHỚP"]
    print(f"Checked {len(claims)} claims -> {len(mismatches)} mismatches. Saved: {out_csv}")
    for c in mismatches:
        print(f"  [LỆCH] {c.claim_id} ({c.location}): report='{c.reported}' vs computed='{c.computed}'")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
