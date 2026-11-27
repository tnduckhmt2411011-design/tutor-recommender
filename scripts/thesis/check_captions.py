"""Kiểm tra tính nhất quán của caption bảng, hình, hình ảnh và trích dẫn trong báo cáo."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

TABLE_CAP_RE = re.compile(
    r"^\*{0,2}Bảng\s+([A-D0-9]+\.\d+)\s*[-–:]\s*(.+?)\*{0,2}\s*$"
)
FIG_CAP_RE = re.compile(
    r"^\*{0,2}Hình\s+([A-D0-9]+\.\d+)\s*[-–:]\s*(.+?)\*{0,2}\s*$"
)
IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
TABLE_REF_RE = re.compile(r"\bBảng\s+([A-D0-9]+\.\d+)\b")
FIG_REF_RE = re.compile(r"\bHình\s+([A-D0-9]+\.\d+)\b")
CITE_GROUP_RE = re.compile(r"\[(\d+(?:\s*[-–,]\s*\d+)*)\]")
CITE_RANGE_RE = re.compile(r"(\d+)\s*[-–]\s*(\d+)")
REF_ENTRY_RE = re.compile(r"^\[(\d+)\]\s+", re.MULTILINE)


@dataclass(frozen=True)
class AuditIssue:
    """Một vấn đề phát hiện khi kiểm tra caption, hình ảnh hoặc trích dẫn."""

    code: str
    location: str
    message: str


def extract_captions(markdown: str) -> tuple[list[tuple[str, str, int]], list[tuple[str, str, int]]]:
    """Trích xuất caption bảng và hình (mã hiệu, tiêu đề, số dòng) từ nội dung Markdown."""
    tables: list[tuple[str, str, int]] = []
    figures: list[tuple[str, str, int]] = []
    in_code_block = False

    for line_no, raw_line in enumerate(markdown.splitlines(), start=1):
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block or stripped.startswith("|") or stripped.startswith("!["):
            continue

        if match := TABLE_CAP_RE.match(stripped):
            title = match.group(2).strip().rstrip("*").strip()
            tables.append((match.group(1), title, line_no))
        elif match := FIG_CAP_RE.match(stripped):
            title = match.group(2).strip().rstrip("*").strip()
            figures.append((match.group(1), title, line_no))

    return tables, figures


def extract_front_matter_lists(
    front_matter_md: str,
) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """Trích danh mục bảng biểu (Mục 9) và danh mục hình vẽ (Mục 10)."""
    tables: list[tuple[str, str]] = []
    figures: list[tuple[str, str]] = []
    section: str | None = None

    for raw_line in front_matter_md.splitlines():
        line = raw_line.strip()
        if line.startswith("## 9."):
            section = "tables"
            continue
        if line.startswith("## 10."):
            section = "figures"
            continue
        if line.startswith("## "):
            section = None
            continue
        if not line.startswith("|"):
            continue

        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        if section == "tables":
            if match := re.match(r"^Bảng\s+([A-D0-9]+\.\d+)\s*[-–:]?$", cells[0]):
                tables.append((match.group(1), cells[1]))
        elif section == "figures":
            if match := re.match(r"^Hình\s+([A-D0-9]+\.\d+)\s*[-–:]?$", cells[0]):
                figures.append((match.group(1), cells[1]))

    return tables, figures


def extract_citations(text: str) -> list[int]:
    """Trích danh sách các chỉ số trích dẫn IEEE dạng `[1]`, `[2, 3]`, `[4]-[6]`, bỏ qua code và công thức."""
    cleaned = re.sub(r"`[^`]+`", "", text)
    cleaned = re.sub(r"\$\$[^$]+\$\$|\$[^$]+\$", "", cleaned)
    cleaned = re.sub(r"\[0\s*,[^\]]*\]", "", cleaned)
    found: list[int] = []
    # Xử lý dạng dải liên kết giữa các ngoặc: [4]-[6]
    normalized = re.sub(r"\]\s*[-–]\s*\[", "-", cleaned)
    for match in CITE_GROUP_RE.finditer(normalized):
        group = match.group(1)
        for part in re.split(r"\s*,\s*", group):
            if range_match := CITE_RANGE_RE.fullmatch(part.strip()):
                start, end = int(range_match.group(1)), int(range_match.group(2))
                if 1 <= start <= end and (end - start) <= 50:
                    found.extend(range(start, end + 1))
            elif part.strip().isdigit() and int(part.strip()) >= 1:
                found.append(int(part.strip()))
    return found


def check_section_structure(report_dir: Path) -> list[AuditIssue]:
    """Kiểm tra dẫn chiếu Mục X.Y / mục N và cấu trúc đề mục con đơn độc."""
    issues: list[AuditIssue] = []
    chapter_files = sorted(report_dir.glob("chuong-*.md"))
    valid_sections: set[str] = set()
    child_groups: dict[str, list[tuple[str, str]]] = {}

    for ch_path in chapter_files:
        for line_no, raw_line in enumerate(ch_path.read_text(encoding="utf-8").splitlines(), start=1):
            if match := re.match(r"^#{2,4}\s+(\d+(?:\.\d+)+)\.\s+", raw_line):
                sec_id = match.group(1)
                valid_sections.add(sec_id)
                parts = sec_id.split(".")
                if len(parts) == 3:
                    parent = ".".join(parts[:2])
                    child_groups.setdefault(parent, []).append((sec_id, f"{ch_path.name}:{line_no}"))

    for parent, children in sorted(child_groups.items()):
        if len(children) == 1:
            issues.append(
                AuditIssue(
                    "SINGLE_CHILD_HEADING",
                    children[0][1],
                    f"Mục {parent} chỉ có duy nhất một tiểu mục con ({children[0][0]}).",
                )
            )

    for ch_path in chapter_files:
        in_code = False
        for line_no, raw_line in enumerate(ch_path.read_text(encoding="utf-8").splitlines(), start=1):
            stripped = raw_line.strip()
            if stripped.startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            # Bỏ qua các dòng trích dẫn cấu trúc của đồ án tham khảo GS360
            is_gs360_line = "GS360" in raw_line
            for m in re.finditer(r"[Mm]ục\s+(\d+(?:\.\d+)+)", raw_line):
                sid = m.group(1)
                if sid not in valid_sections:
                    if is_gs360_line or "tr." in raw_line:
                        continue
                    issues.append(
                        AuditIssue(
                            "BROKEN_SECTION_REF",
                            f"{ch_path.name}:{line_no}",
                            f"Dẫn chiếu tới '{m.group(0)}' không tồn tại trong báo cáo.",
                        )
                    )
            for m in re.finditer(r"[Mm]ục\s+(\d+)(?!\.\d)", raw_line):
                before = raw_line[max(0, m.start() - 60) : m.start()]
                after = raw_line[m.end() : m.end() + 40]
                if (
                    ".md" in before
                    or "README" in before
                    or "Hướng dẫn" in before
                    or "phụ lục" in before.lower()
                    or "Phụ lục" in before
                    or "scoring-spec" in before
                    or "api-contract" in before
                    or re.search(r"tiêu chí|bước", after, re.I)
                    or is_gs360_line
                    or "tr." in raw_line
                    or "mục 3 và 7" in raw_line
                ):
                    continue
                if m.group(1) in {"1", "2", "3", "4", "5", "6"}:
                    issues.append(
                        AuditIssue(
                            "BROKEN_SECTION_REF",
                            f"{ch_path.name}:{line_no}",
                            f"Dẫn chiếu '{m.group(0)}' có thể là cấp Chương chứ không phải Mục.",
                        )
                    )

    return issues


def _check_sequence(
    items: list[tuple[str, str, int, str]],
    kind: str,
    seq_code: str,
    dup_code: str,
) -> list[AuditIssue]:
    issues: list[AuditIssue] = []
    seen: dict[str, str] = {}
    by_prefix: dict[str, list[tuple[int, int, str]]] = {}

    for item_id, _title, line_no, fname in items:
        if item_id in seen:
            issues.append(
                AuditIssue(
                    dup_code,
                    f"{fname}:{line_no}",
                    f"Trùng mã {kind} {item_id} (đã xuất hiện ở {seen[item_id]}).",
                )
            )
        seen[item_id] = f"{fname}:{line_no}"
        prefix, num_str = item_id.split(".", 1)
        by_prefix.setdefault(prefix, []).append((int(num_str), line_no, fname))

    for prefix, entries in by_prefix.items():
        nums = [num for num, _, _ in entries]
        expected = list(range(1, len(nums) + 1))
        if nums != expected:
            loc = f"{entries[-1][2]}:{entries[-1][1]}"
            issues.append(
                AuditIssue(
                    seq_code,
                    loc,
                    f"Số thứ tự {kind} nhóm {prefix} không liên tục: {nums} (kỳ vọng {expected}).",
                )
            )
    return issues


def audit_report(report_dir: Path) -> list[AuditIssue]:
    """Thực hiện kiểm tra toàn diện caption, dẫn chiếu, ảnh và trích dẫn."""
    issues: list[AuditIssue] = []
    chapter_files = sorted(report_dir.glob("chuong-*.md"))
    if not chapter_files:
        return [AuditIssue("NO_CHAPTERS", str(report_dir), "Không tìm thấy tệp chuong-*.md.")]

    all_tables: list[tuple[str, str, int, str]] = []
    all_figures: list[tuple[str, str, int, str]] = []
    table_refs: dict[str, list[str]] = {}
    figure_refs: dict[str, list[str]] = {}
    citation_order: list[tuple[int, str]] = []
    image_count = 0

    for ch_path in chapter_files:
        text = ch_path.read_text(encoding="utf-8")
        tables, figures = extract_captions(text)
        caption_lines = {line_no for _, _, line_no in tables} | {
            line_no for _, _, line_no in figures
        }

        for tid, title, line_no in tables:
            all_tables.append((tid, title, line_no, ch_path.name))
        for fid, title, line_no in figures:
            all_figures.append((fid, title, line_no, ch_path.name))

        in_code_block = False
        for line_no, raw_line in enumerate(text.splitlines(), start=1):
            stripped = raw_line.strip()
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue

            for img_match in IMG_RE.finditer(raw_line):
                image_count += 1
                rel_path = img_match.group(2).strip()
                resolved = (ch_path.parent / rel_path).resolve()
                if not resolved.exists():
                    issues.append(
                        AuditIssue(
                            "BROKEN_IMAGE",
                            f"{ch_path.name}:{line_no}",
                            f"Không tìm thấy tệp ảnh '{rel_path}' ({resolved}).",
                        )
                    )

            if line_no in caption_lines or stripped.startswith("!["):
                continue

            for m in TABLE_REF_RE.finditer(raw_line):
                table_refs.setdefault(m.group(1), []).append(f"{ch_path.name}:{line_no}")
            for m in FIG_REF_RE.finditer(raw_line):
                figure_refs.setdefault(m.group(1), []).append(f"{ch_path.name}:{line_no}")
            for cid in extract_citations(raw_line):
                citation_order.append((cid, f"{ch_path.name}:{line_no}"))

    issues.extend(_check_sequence(all_tables, "Bảng", "TABLE_SEQUENCE", "TABLE_DUPLICATE"))
    issues.extend(_check_sequence(all_figures, "Hình", "FIGURE_SEQUENCE", "FIGURE_DUPLICATE"))

    table_ids = {tid for tid, _, _, _ in all_tables}
    figure_ids = {fid for fid, _, _, _ in all_figures}

    for ref_id, locs in sorted(table_refs.items()):
        if ref_id not in table_ids:
            issues.append(
                AuditIssue(
                    "BROKEN_TABLE_REF",
                    locs[0],
                    f"Dẫn chiếu tới 'Bảng {ref_id}' không tồn tại trong báo cáo (xuất hiện {len(locs)} lần).",
                )
            )
    for ref_id, locs in sorted(figure_refs.items()):
        if ref_id not in figure_ids:
            issues.append(
                AuditIssue(
                    "BROKEN_FIGURE_REF",
                    locs[0],
                    f"Dẫn chiếu tới 'Hình {ref_id}' không tồn tại trong báo cáo (xuất hiện {len(locs)} lần).",
                )
            )

    for tid, _title, line_no, fname in all_tables:
        if tid not in table_refs:
            issues.append(
                AuditIssue(
                    "UNREFERENCED_TABLE",
                    f"{fname}:{line_no}",
                    f"Bảng {tid} chưa được dẫn chiếu trực tiếp trong văn bản.",
                )
            )
    for fid, _title, line_no, fname in all_figures:
        if fid not in figure_refs:
            issues.append(
                AuditIssue(
                    "UNREFERENCED_FIGURE",
                    f"{fname}:{line_no}",
                    f"Hình {fid} chưa được dẫn chiếu trực tiếp trong văn bản.",
                )
            )

    if image_count != len(all_figures):
        issues.append(
            AuditIssue(
                "IMAGE_CAPTION_MISMATCH",
                "docs/thesis/report",
                f"Số ảnh nhúng ({image_count}) khác số caption hình ({len(all_figures)}).",
            )
        )

    fm_path = report_dir / "muc-luc-va-ho-so-ban-giao.md"
    if fm_path.exists():
        fm_text = fm_path.read_text(encoding="utf-8")
        in_prose_fm = False
        in_fm_code = False
        for line_no, raw_line in enumerate(fm_text.splitlines(), start=1):
            stripped = raw_line.strip()
            if stripped.startswith("```"):
                in_fm_code = not in_fm_code
                continue
            if in_fm_code:
                continue
            if re.match(r"^##\s+", stripped) or re.match(r"^#\s+", stripped):
                sec_match = re.match(r"^##\s+(\d+)\.", stripped)
                in_prose_fm = bool(sec_match and sec_match.group(1) in {"4", "5", "6"})
                continue
            if in_prose_fm:
                for cid in extract_citations(raw_line):
                    issues.append(
                        AuditIssue(
                            "FRONT_MATTER_CITATION",
                            f"{fm_path.name}:{line_no}",
                            f"Trích dẫn [{cid}] xuất hiện ở phần mở đầu trước thân bài, phá vỡ thứ tự IEEE.",
                        )
                    )

        fm_tables, fm_figures = extract_front_matter_lists(fm_text)
        body_table_pairs = [(tid, title) for tid, title, _, _ in all_tables]
        body_figure_pairs = [(fid, title) for fid, title, _, _ in all_figures]

        body_t_ids = [tid for tid, _ in body_table_pairs]
        fm_t_ids = [tid for tid, _ in fm_tables]
        if body_t_ids != fm_t_ids:
            issues.append(
                AuditIssue(
                    "FRONT_MATTER_TABLE_MISMATCH",
                    fm_path.name,
                    f"Danh mục bảng ({len(fm_t_ids)}) khác thân bài ({len(body_t_ids)}): "
                    f"chỉ có ở thân={sorted(set(body_t_ids) - set(fm_t_ids))}, "
                    f"chỉ có ở danh mục={sorted(set(fm_t_ids) - set(body_t_ids))}.",
                )
            )
        else:
            for (tid, b_title), (_, f_title) in zip(body_table_pairs, fm_tables):
                if b_title != f_title:
                    issues.append(
                        AuditIssue(
                            "FRONT_MATTER_TABLE_TITLE_DIFF",
                            fm_path.name,
                            f"Tên Bảng {tid} khác giữa thân bài ('{b_title}') và danh mục ('{f_title}').",
                        )
                    )

        body_f_ids = [fid for fid, _ in body_figure_pairs]
        fm_f_ids = [fid for fid, _ in fm_figures]
        if body_f_ids != fm_f_ids:
            issues.append(
                AuditIssue(
                    "FRONT_MATTER_FIGURE_MISMATCH",
                    fm_path.name,
                    f"Danh mục hình ({len(fm_f_ids)}) khác thân bài ({len(body_f_ids)}).",
                )
            )
        else:
            for (fid, b_title), (_, f_title) in zip(body_figure_pairs, fm_figures):
                if b_title != f_title:
                    issues.append(
                        AuditIssue(
                            "FRONT_MATTER_FIGURE_TITLE_DIFF",
                            fm_path.name,
                            f"Tên Hình {fid} khác giữa thân bài ('{b_title}') và danh mục ('{f_title}').",
                        )
                    )

    refs_path = report_dir / "tai-lieu-tham-khao.md"
    if refs_path.exists():
        ref_ids = [int(m.group(1)) for m in REF_ENTRY_RE.finditer(refs_path.read_text(encoding="utf-8"))]
        cited_ids = {cid for cid, _ in citation_order}
        for cid, loc in citation_order:
            if cid not in ref_ids:
                issues.append(
                    AuditIssue(
                        "MISSING_REFERENCE_ENTRY",
                        loc,
                        f"Trích dẫn [{cid}] không có trong tai-lieu-tham-khao.md.",
                    )
                )
        for rid in ref_ids:
            if rid not in cited_ids:
                issues.append(
                    AuditIssue(
                        "UNCITED_REFERENCE",
                        refs_path.name,
                        f"Tài liệu tham khảo [{rid}] chưa được trích dẫn trong thân bài.",
                    )
                )
        seen_cites: list[int] = []
        for cid, _loc in citation_order:
            if cid not in seen_cites:
                seen_cites.append(cid)
        if seen_cites != sorted(seen_cites) or (
            seen_cites and seen_cites != list(range(1, len(seen_cites) + 1))
        ):
            issues.append(
                AuditIssue(
                    "CITATION_ORDER",
                    "docs/thesis/report",
                    f"Thứ tự xuất hiện trích dẫn lần đầu chưa tăng dần từ 1: {seen_cites}.",
                )
            )

    issues.extend(check_section_structure(report_dir))
    return issues


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    report_dir = repo_root / "docs" / "thesis" / "report"
    issues = audit_report(report_dir)

    tables_total = 0
    figures_total = 0
    for ch_path in sorted(report_dir.glob("chuong-*.md")):
        t, f = extract_captions(ch_path.read_text(encoding="utf-8"))
        tables_total += len(t)
        figures_total += len(f)

    if not issues:
        print(f"OK {tables_total} tables, {figures_total} figures, 0 broken refs")
        return 0

    print(f"FOUND {len(issues)} issues ({tables_total} tables, {figures_total} figures):")
    for iss in issues:
        print(f"  [{iss.code}] {iss.location}: {iss.message}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
