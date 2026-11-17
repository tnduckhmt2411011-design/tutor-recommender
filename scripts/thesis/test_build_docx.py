"""Unit test TDD cho quy trình chuẩn hóa Markdown, dựng reference.docx, ghép và kiểm định DOCX."""

from __future__ import annotations

from pathlib import Path

import docx
import pytest

from build_docx import (
    ORDER,
    create_reference_docx,
    preprocess_markdown,
    split_appendix,
    split_front_matter,
)
from verify_docx import verify_docx


def test_order_contains_all_expected_report_files() -> None:
    expected = [
        "muc-luc-va-ho-so-ban-giao.md",
        "chuong-01-tong-quan.md",
        "chuong-02-co-so-ly-thuyet-va-cong-nghe.md",
        "chuong-03-phan-tich-thiet-ke.md",
        "chuong-04-xay-dung-he-thong.md",
        "chuong-05-thuc-nghiem-va-danh-gia.md",
        "chuong-06-ket-luan-va-huong-phat-trien.md",
        "tai-lieu-tham-khao.md",
    ]
    assert list(ORDER) == expected


def test_preprocess_markdown_removes_github_alerts_and_horizontal_rules() -> None:
    raw = (
        "Đoạn dẫn.\n\n"
        "---\n\n"
        "> [!NOTE]\n"
        "> Nội dung ghi chú $s_1 = 1$.\n\n"
        "> [!IMPORTANT]\n"
        "> Nội dung quan trọng.\n\n"
        "```markdown\n"
        "---\n"
        "```\n"
    )
    cleaned = preprocess_markdown(raw)
    assert "[!NOTE]" not in cleaned
    assert "[!IMPORTANT]" not in cleaned
    assert "**Lưu ý:** Nội dung ghi chú $s_1 = 1$." in cleaned
    assert "**Quan trọng:** Nội dung quan trọng." in cleaned
    # Horizontal rule bên ngoài code block bị loại bỏ, bên trong code block được giữ nguyên
    lines = cleaned.splitlines()
    assert "---" in lines
    assert lines.count("---") == 1


def test_split_appendix_separates_chapter6_from_appendices() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    ch6_text = (
        repo_root / "docs" / "thesis" / "report" / "chuong-06-ket-luan-va-huong-phat-trien.md"
    ).read_text(encoding="utf-8")
    ch6_body, appendix_md = split_appendix(ch6_text)

    assert "# CHƯƠNG 6. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN" in ch6_body
    assert "PHỤ LỤC A" not in ch6_body
    assert appendix_md.lstrip().startswith("# PHỤ LỤC A.")
    for label in ("# PHỤ LỤC A.", "# PHỤ LỤC B.", "# PHỤ LỤC C.", "# PHỤ LỤC D."):
        assert label in appendix_md


def test_split_front_matter_extracts_cover_and_front_sections_without_handover_notes() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    fm_text = (
        repo_root / "docs" / "thesis" / "report" / "muc-luc-va-ho-so-ban-giao.md"
    ).read_text(encoding="utf-8")
    parts = split_front_matter(fm_text)

    cover = "\n".join(parts["cover_lines"])
    assert "TRƯỜNG ĐẠI HỌC KỸ THUẬT CÔNG NGHỆ CẦN THƠ" in cover
    assert "CONTENT-BASE FILTERING" in cover
    assert "TS. LÊ ANH NHÃ UYÊN" in cover

    assert "TS. Lê Anh Nhã Uyên" in parts["loi_cam_on"]
    assert "Nhóm cam đoan:" in parts["loi_cam_doan"]
    assert "Abstract (English)" in parts["abstract_en"] or "Choosing a tutor" in parts["abstract_en"]
    assert "Choosing a tutor" in parts["abstract_en"]
    assert len(parts["tables_list"]) == 31
    assert len(parts["figures_list"]) == 9
    # Không đưa các mục nội bộ (1, 2, 11) hay dấu … còn sót vào phần mở đầu
    for key in ("loi_cam_on", "loi_cam_doan", "tom_tat_vi", "abstract_en", "ky_hieu_viet_tat"):
        assert "Cần Thơ" in parts["loi_cam_on"] or key != "loi_cam_on"
        assert "Hồ sơ bàn giao" not in parts[key]
        assert "…" not in parts[key]


def test_create_reference_docx_configures_a4_margins_and_times_new_roman(tmp_path: Path) -> None:
    ref_path = tmp_path / "reference.docx"
    result_path = create_reference_docx(ref_path)
    assert result_path.exists()

    doc = docx.Document(str(result_path))
    sec = doc.sections[0]
    assert round(sec.page_width.mm) == 210
    assert round(sec.page_height.mm) == 297
    assert pytest.approx(sec.top_margin.cm, abs=0.05) == 2.5
    assert pytest.approx(sec.bottom_margin.cm, abs=0.05) == 2.0
    assert pytest.approx(sec.left_margin.cm, abs=0.05) == 3.0
    assert pytest.approx(sec.right_margin.cm, abs=0.05) == 2.0

    for style_name in (
        "Normal",
        "Heading 1",
        "Heading 2",
        "Heading 3",
        "Body Text",
        "First Paragraph",
        "Compact",
        "Block Text",
        "Caption",
    ):
        if style_name in doc.styles:
            assert doc.styles[style_name].font.name == "Times New Roman"

    assert doc.styles["Normal"].font.size.pt == 13
    assert doc.styles["Heading 1"].font.bold is True
    assert doc.styles["Heading 2"].font.bold is True
    assert doc.styles["Heading 3"].font.bold is True
    assert doc.styles["Heading 3"].font.italic is True


def test_verify_docx_reports_missing_file(tmp_path: Path) -> None:
    issues, _stats = verify_docx(tmp_path / "does_not_exist.docx")
    assert issues and "Không tìm thấy" in issues[0]


def test_verify_docx_passes_on_generated_report() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    out_docx = repo_root.parent / "BAO_CAO_DO_AN_KHMT1_HOAN_CHINH.docx"
    assert out_docx.exists(), "Cần chạy build_docx.py trước khi kiểm định tệp đích."
    issues, stats = verify_docx(out_docx, repo_root)
    assert issues == []
    assert stats["sections"] == 3
    assert stats["media_count"] == 9
    assert stats["body_tables"] == 31
    assert stats["body_figures"] == 9
    assert int(stats["omath_count"]) > 100
    assert float(stats["word_diff_pct"]) < 3.0
