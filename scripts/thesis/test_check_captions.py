"""Kiểm thử cho script rà soát caption, dẫn chiếu, hình ảnh và trích dẫn."""

from __future__ import annotations

from pathlib import Path

import pytest

from check_captions import (
    audit_report,
    check_section_structure,
    extract_captions,
    extract_citations,
    extract_front_matter_lists,
)


def _write_sample_repo(tmp_path: Path, *, break_table_seq: bool = False) -> Path:
    report_dir = tmp_path / "docs" / "thesis" / "report"
    figures_dir = tmp_path / "docs" / "thesis" / "figures"
    report_dir.mkdir(parents=True)
    figures_dir.mkdir(parents=True)
    (figures_dir / "fig1.png").write_bytes(b"png")

    (report_dir / "chuong-01-tong-quan.md").write_text(
        "# CHƯƠNG 1. TỔNG QUAN\n\n"
        "Xem Bảng 1.1 và Hình 1.1 cùng trích dẫn [1].\n\n"
        "**Bảng 1.1 - Bảng đầu tiên**\n\n"
        "| A |\n|---|\n| 1 |\n\n"
        + ("**Bảng 1.3 - Bị nhảy số**\n\n| B |\n|---|\n| 2 |\n\n" if break_table_seq else "")
        + "![Hình 1.1 - Sơ đồ](../figures/fig1.png)\n\n"
        "**Hình 1.1 - Sơ đồ**\n",
        encoding="utf-8",
    )
    (report_dir / "tai-lieu-tham-khao.md").write_text(
        "# TÀI LIỆU THAM KHẢO\n\n[1] Tác giả, \"Tiêu đề,\" 2024.\n",
        encoding="utf-8",
    )
    (report_dir / "muc-luc-va-ho-so-ban-giao.md").write_text(
        "## 9. Danh mục bảng biểu\n\n"
        "| Số hiệu | Tên bảng | Trang |\n|---|---|---|\n"
        "| Bảng 1.1 | Bảng đầu tiên | … |\n\n"
        "## 10. Danh mục hình vẽ\n\n"
        "| Số hiệu | Tên hình | Trang |\n|---|---|---|\n"
        "| Hình 1.1 | Sơ đồ | … |\n",
        encoding="utf-8",
    )
    return report_dir


def test_extract_captions_distinguishes_caption_from_reference(tmp_path: Path) -> None:
    md = (
        "Theo Bảng 1.1 và Hình 1.1 cho thấy kết quả.\n\n"
        "**Bảng 1.1 - Bảng đầu tiên**\n\n"
        "| Cột |\n|---|\n| 1 |\n\n"
        "**Hình 1.1 - Sơ đồ**\n"
    )
    tables, figures = extract_captions(md)
    assert tables == [("1.1", "Bảng đầu tiên", 3)]
    assert figures == [("1.1", "Sơ đồ", 9)]


def test_extract_front_matter_lists_reads_tables_and_figures(tmp_path: Path) -> None:
    report_dir = _write_sample_repo(tmp_path)
    tables, figures = extract_front_matter_lists(
        (report_dir / "muc-luc-va-ho-so-ban-giao.md").read_text(encoding="utf-8")
    )
    assert tables == [("1.1", "Bảng đầu tiên")]
    assert figures == [("1.1", "Sơ đồ")]


def test_extract_citations_ignores_decimal_brackets() -> None:
    text = (
        "Khoảng giá trị $s_i \\in [0, 1]$ hoặc `arr[0, 5]` và đoạn [0, 1] "
        "theo tài liệu [1] và [2, 3] hoặc [4]-[6]."
    )
    assert extract_citations(text) == [1, 2, 3, 4, 5, 6]


def test_audit_report_passes_on_clean_sample(tmp_path: Path) -> None:
    report_dir = _write_sample_repo(tmp_path, break_table_seq=False)
    issues = audit_report(report_dir)
    assert issues == []


def test_audit_report_flags_sequence_gap_and_front_matter_mismatch(tmp_path: Path) -> None:
    report_dir = _write_sample_repo(tmp_path, break_table_seq=True)
    issues = audit_report(report_dir)
    codes = {issue.code for issue in issues}
    assert "TABLE_SEQUENCE" in codes
    assert "FRONT_MATTER_TABLE_MISMATCH" in codes


def test_check_section_structure_flags_broken_muc_ref_and_single_child(tmp_path: Path) -> None:
    report_dir = tmp_path / "docs" / "thesis" / "report"
    report_dir.mkdir(parents=True)
    (report_dir / "chuong-01-tong-quan.md").write_text(
        "# CHƯƠNG 1. TỔNG QUAN\n\n"
        "## 1.1. Mở đầu\n\n"
        "### 1.1.1. Mục con duy nhất\n\n"
        "Xem Mục 9.9 và dữ liệu ở mục 5.\n",
        encoding="utf-8",
    )
    issues = check_section_structure(report_dir)
    codes = {i.code for i in issues}
    assert "BROKEN_SECTION_REF" in codes
    assert "SINGLE_CHILD_HEADING" in codes
