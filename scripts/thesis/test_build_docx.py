"""Unit test TDD cho quy trình chuẩn hóa Markdown, dựng reference.docx, ghép và kiểm định DOCX."""

from __future__ import annotations

from pathlib import Path
import struct
import xml.etree.ElementTree as ET
import zipfile

import docx
import pypandoc
import pytest
from docx.oxml.ns import qn

import build_docx
import verify_docx as verify_docx_mod
from build_docx import (
    EQ_NUM_MARKER_PREFIX,
    ORDER,
    PRINTABLE_WIDTH_TWIPS,
    _compute_smart_col_widths,
    create_reference_docx,
    preprocess_markdown,
    split_appendix,
    split_front_matter,
)
from verify_docx import (
    _load_style_bold_map,
    _load_style_id_map,
    _toc_run_bold_flags,
    verify_docx,
)


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


def test_preprocess_markdown_handles_alerts_rules_and_equation_numbers() -> None:
    raw = (
        "Đoạn dẫn.\n\n"
        "---\n\n"
        "$$S(g) = \\frac{1}{2} \\qquad (2.1)$$\n\n"
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
    assert f"{EQ_NUM_MARKER_PREFIX}(2.1)]]" in cleaned
    assert "$$S(g) = \\frac{1}{2}$$" in cleaned
    lines = cleaned.splitlines()
    assert "---" in lines
    assert lines.count("---") == 1


def test_preprocess_markdown_separates_lead_in_prose_from_lists() -> None:
    raw = (
        "Hệ thống gồm ba thành phần:\n"
        "- Thành phần 1.\n"
        "- Thành phần 2.\n\n"
        "Quy trình hai bước:\n"
        "1. Bước một.\n"
        "2. Bước hai.\n"
    )
    cleaned = preprocess_markdown(raw)
    assert "Hệ thống gồm ba thành phần:\n\n- Thành phần 1.\n- Thành phần 2." in cleaned
    assert "Quy trình hai bước:\n\n1. Bước một.\n2. Bước hai." in cleaned


def test_compute_smart_col_widths_balances_content_and_sums_to_printable_width() -> None:
    d = docx.Document()
    tbl = d.add_table(rows=3, cols=3)
    rows_data = [
        ("Ký hiệu", "Tên gọi", "Ý nghĩa trong báo cáo"),
        ("k", "Số gợi ý", "Số lượng gia sư hàng đầu được trả về cho mỗi truy vấn người học"),
        ("S(g)", "Điểm tổng hợp", "Tổng trọng số chuẩn hóa của bốn thành phần hàm đánh giá đa tiêu chí"),
    ]
    for r_idx, row_vals in enumerate(rows_data):
        for c_idx, val in enumerate(row_vals):
            tbl.rows[r_idx].cells[c_idx].text = val
    widths = _compute_smart_col_widths(tbl, PRINTABLE_WIDTH_TWIPS)
    assert len(widths) == 3
    assert sum(widths) == PRINTABLE_WIDTH_TWIPS
    assert widths[2] > widths[1] > widths[0]


def test_split_appendix_separates_chapter6_from_unified_appendix() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    ch6_text = (
        repo_root / "docs" / "thesis" / "report" / "chuong-06-ket-luan-va-huong-phat-trien.md"
    ).read_text(encoding="utf-8")
    ch6_body, appendix_md = split_appendix(ch6_text)

    assert "# CHƯƠNG 6. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN" in ch6_body
    assert "Phụ lục A." not in ch6_body
    assert appendix_md.lstrip().startswith("# PHỤ LỤC")
    for label in (
        "## Phụ lục A.",
        "## Phụ lục B.",
        "## Phụ lục C.",
        "## Phụ lục D.",
    ):
        assert label in appendix_md


def test_split_front_matter_extracts_covers_and_front_sections_per_ml_standard() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    fm_text = (
        repo_root / "docs" / "thesis" / "report" / "muc-luc-va-ho-so-ban-giao.md"
    ).read_text(encoding="utf-8")
    parts = split_front_matter(fm_text)

    cover = "\n".join(parts["cover_lines"])
    assert "TRƯỜNG ĐẠI HỌC KỸ THUẬT - CÔNG NGHỆ CẦN THƠ" in cover
    assert "CONTENT-BASE FILTERING" in cover
    assert "TS. Lê Anh Nhã Uyên" in cover
    assert len(parts["cover_main_blocks"]) == 5
    assert len(parts["cover_sub_blocks"]) >= 1

    assert "TS. Lê Anh Nhã Uyên" in parts["loi_cam_on"]
    assert "cam đoan về báo cáo này như sau:" in parts["loi_cam_doan"]
    assert "Từ khóa:" not in parts["tom_tat_vi"]
    assert "Keywords:" not in parts["abstract_en"]
    assert "Choosing a tutor" in parts["abstract_en"]
    assert "### 1. Chữ viết tắt" in parts["ky_hieu_viet_tat"]
    assert "### 2. Ký hiệu toán học" in parts["ky_hieu_viet_tat"]
    assert len(parts["tables_list"]) == 31
    assert len(parts["figures_list"]) == 9
    for key in ("loi_cam_on", "loi_cam_doan", "tom_tat_vi", "abstract_en", "ky_hieu_viet_tat"):
        assert "Hồ sơ bàn giao" not in parts[key]
        assert "…" not in parts[key]


def test_create_reference_docx_configures_ml_margins_styles_and_times_new_roman(
    tmp_path: Path,
) -> None:
    ref_path = tmp_path / "reference.docx"
    result_path = create_reference_docx(ref_path)
    assert result_path.exists()

    doc = docx.Document(str(result_path))
    sec = doc.sections[0]
    assert round(sec.page_width.mm) == 210
    assert round(sec.page_height.mm) == 297
    assert pytest.approx(sec.top_margin.cm, abs=0.05) == 2.0
    assert pytest.approx(sec.bottom_margin.cm, abs=0.05) == 2.0
    assert pytest.approx(sec.left_margin.cm, abs=0.05) == 3.0
    assert pytest.approx(sec.right_margin.cm, abs=0.05) == 2.0

    for style_name in (
        "Normal",
        "Heading 1",
        "Heading 2",
        "Heading 3",
        "Front Title",
        "Front Heading 2",
        "Caption Table",
        "Caption Figure",
        "Source Code",
    ):
        assert style_name in doc.styles
        assert doc.styles[style_name].font.name == "Times New Roman"

    assert doc.styles["Normal"].font.size.pt == 13
    assert doc.styles["Heading 1"].font.size.pt == 15
    assert doc.styles["Heading 1"].font.bold is True
    assert doc.styles["Heading 2"].font.size.pt == 13.5
    assert doc.styles["Heading 2"].font.bold is True
    assert doc.styles["Heading 3"].font.size.pt == 13
    assert doc.styles["Heading 3"].font.bold is True
    assert doc.styles["Heading 3"].font.italic is True
    assert doc.styles["Caption Table"].font.size.pt == 11
    assert doc.styles["Caption Figure"].font.size.pt == 11
    assert doc.styles["Source Code"].font.size.pt == 10.0


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
    assert stats["media_count"] == 11
    assert stats["body_tables"] == 31
    assert stats["body_figures"] == 9
    assert int(stats["toc_level1_count"]) == 16
    assert int(stats["data_tables"]) == 33
    assert int(stats["omath_count"]) > 100
    assert float(stats["word_diff_pct"]) < 3.0


def test_generated_report_uses_dash_lists_standard_spacing_and_no_list_totals() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    out_docx = repo_root.parent / "BAO_CAO_DO_AN_KHMT1_HOAN_CHINH.docx"
    assert out_docx.exists(), "Cần chạy build_docx.py trước khi kiểm định tệp đích."

    doc = docx.Document(str(out_docx))
    all_texts = [p.text for p in doc.paragraphs]
    assert not any("Tổng: 31 bảng" in t for t in all_texts)
    assert not any("Tổng: 9 hình" in t for t in all_texts)

    with zipfile.ZipFile(out_docx) as zf:
        numbering_xml = ET.fromstring(zf.read("word/numbering.xml"))
    w_ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    for lvl in numbering_xml.findall(f".//{w_ns}lvl"):
        nf = lvl.find(f"{w_ns}numFmt")
        lt = lvl.find(f"{w_ns}lvlText")
        if nf is not None and nf.attrib.get(f"{w_ns}val") == "bullet" and lt is not None:
            lt_val = lt.attrib.get(f"{w_ns}val", "")
            if lt_val.strip() != "":
                assert lt_val == "-"
                rf = lvl.find(f"{w_ns}rPr/{w_ns}rFonts")
                assert rf is not None
                assert rf.attrib.get(f"{w_ns}ascii") == "Times New Roman"
                assert rf.attrib.get(f"{w_ns}hAnsi") == "Times New Roman"

    level0_list_paras = []
    for p in doc.paragraphs:
        ppr = p._p.pPr
        num_pr = ppr.find(qn("w:numPr")) if ppr is not None else None
        if num_pr is not None:
            ilvl = num_pr.find(qn("w:ilvl"))
            depth = int(ilvl.get(qn("w:val"), "0")) if ilvl is not None else 0
            if depth == 0:
                level0_list_paras.append(p)
    assert level0_list_paras
    for p in level0_list_paras:
        pf = p.paragraph_format
        assert pf.line_spacing == pytest.approx(1.3, abs=0.01)
        assert pf.space_before is not None and pf.space_before.pt == pytest.approx(3.0, abs=0.1)
        assert pf.space_after is not None and pf.space_after.pt == pytest.approx(3.0, abs=0.1)
        assert pf.left_indent is not None and pf.left_indent.cm == pytest.approx(1.30, abs=0.05)
        assert pf.first_line_indent is not None and pf.first_line_indent.cm == pytest.approx(-0.45, abs=0.05)


def test_chapter3_drawio_sources_and_rendered_pngs_are_valid() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    figures_dir = repo_root / "docs" / "thesis" / "figures"
    src_dir = figures_dir / "src"

    stems = (
        "hinh-3-1-luong-xu-ly-khuyen-nghi",
        "hinh-3-2-kien-truc-ba-lop",
        "hinh-3-3-so-do-trinh-tu",
        "hinh-3-5-phac-thao-ket-qua",
    )
    parsed_xmls: dict[str, ET.Element] = {}
    for stem in stems:
        drawio_path = src_dir / f"{stem}.drawio"
        png_path = figures_dir / f"{stem}.png"
        assert drawio_path.exists(), f"Thiếu tệp nguồn draw.io: {drawio_path}"
        assert png_path.exists(), f"Thiếu tệp ảnh xuất PNG: {png_path}"

        root = ET.fromstring(drawio_path.read_text(encoding="utf-8"))
        assert root.tag == "mxfile"
        assert root.find(".//mxGraphModel/root") is not None
        parsed_xmls[stem] = root

        png_header = png_path.read_bytes()[:24]
        assert png_header[:8] == b"\x89PNG\r\n\x1a\n"
        width, height = struct.unpack(">II", png_header[16:24])
        assert width >= 1600 and height >= 1200

    # Hình 3.3: chuẩn UML 2.5 và đúng thứ tự thực thi của recommend.py
    h33_xml = ET.tostring(parsed_xmls["hinh-3-3-so-do-trinh-tu"], encoding="unicode")
    for token in (
        "umlActor",
        "umlFrame",
        "filter_mandatory",
        "compute_effective_weights",
        "filter_eligible_candidates",
        "score_and_rank",
    ):
        assert token in h33_xml

    def _msg_y(root: ET.Element, needle: str) -> float:
        for cell in root.findall(".//mxCell"):
            if needle in cell.get("value", ""):
                pt = cell.find(".//mxGeometry/mxPoint[@as='sourcePoint']")
                if pt is not None:
                    return float(pt.get("y", "0"))
                geom = cell.find("mxGeometry")
                if geom is not None and geom.get("y") is not None:
                    return float(geom.get("y", "0"))
        raise AssertionError(f"Không tìm thấy phần tử '{needle}'")

    h33_root = parsed_xmls["hinh-3-3-so-do-trinh-tu"]
    y_get_all = _msg_y(h33_root, "get_all()")
    y_mandatory = _msg_y(h33_root, "filter_mandatory")
    y_weights = _msg_y(h33_root, "compute_effective_weights")
    y_eligible = _msg_y(h33_root, "filter_eligible_candidates")
    y_rank = _msg_y(h33_root, "score_and_rank")
    assert y_get_all < y_mandatory < y_weights < y_eligible < y_rank

    # Hình 3.1: đúng chuẩn ISO 5807 (rhombus) và zero_weight đứng trước ngưỡng Bảng 3.7
    h31_root = parsed_xmls["hinh-3-1-luong-xu-ly-khuyen-nghi"]
    diamonds = [c for c in h31_root.findall(".//mxCell") if "rhombus" in c.get("style", "")]
    assert len(diamonds) == 5
    y_zero = _msg_y(h31_root, "zero_weight")
    y_thresh = _msg_y(h31_root, "Bảng 3.7")
    assert y_zero < y_thresh


def test_generated_report_bolds_only_level1_toc_entries() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    out_docx = repo_root.parent / "BAO_CAO_DO_AN_KHMT1_HOAN_CHINH.docx"
    assert out_docx.exists(), "Cần chạy build_docx.py trước khi kiểm định tệp đích."

    w_ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    with zipfile.ZipFile(out_docx) as zf:
        doc_xml = ET.fromstring(zf.read("word/document.xml"))
        styles_xml = ET.fromstring(zf.read("word/styles.xml"))

    style_id_to_canon = _load_style_id_map(styles_xml, w_ns)
    style_id_to_bold = _load_style_bold_map(styles_xml, w_ns)

    body_el = doc_xml.find(f"{w_ns}body")
    assert body_el is not None

    front_section = ""
    bold_lvl1_titles: list[str] = []
    expected_lvl1_titles = [
        "LỜI CẢM ƠN",
        "LỜI CAM ĐOAN",
        "TÓM TẮT",
        "ABSTRACT",
        "MỤC LỤC",
        "DANH MỤC KÝ HIỆU VÀ CHỮ VIẾT TẮT",
        "DANH MỤC BẢNG BIỂU",
        "DANH MỤC HÌNH ẢNH",
        "CHƯƠNG 1. TỔNG QUAN VỀ ĐỀ TÀI",
        "CHƯƠNG 2. CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ",
        "CHƯƠNG 3. PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG",
        "CHƯƠNG 4. XÂY DỰNG HỆ THỐNG",
        "CHƯƠNG 5. KIỂM THỬ VÀ ĐÁNH GIÁ",
        "CHƯƠNG 6. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN",
        "TÀI LIỆU THAM KHẢO",
        "PHỤ LỤC",
    ]

    for p_el in body_el.findall(f"{w_ns}p"):
        p_style_el = p_el.find(f"{w_ns}pPr/{w_ns}pStyle")
        sid = p_style_el.attrib.get(f"{w_ns}val", "") if p_style_el is not None else ""
        canon = style_id_to_canon.get(sid, sid.lower())
        txt = "".join(t.text for t in p_el.iter(f"{w_ns}t") if t.text).strip()
        if canon in ("heading 1", "heading1") and txt.startswith("CHƯƠNG 1."):
            break
        if canon in ("front title", "fronttitle") and txt:
            front_section = txt
            continue
        if canon not in ("toc 1", "toc1", "toc 2", "toc2", "toc 3", "toc3") or not txt:
            continue

        flags = _toc_run_bold_flags(p_el, sid, style_id_to_bold, w_ns)
        assert flags, f"Dòng mục lục thiếu run hiển thị trong '{front_section}'."
        if front_section == "MỤC LỤC" and canon in ("toc 1", "toc1"):
            assert all(flags), f"Mục cấp 1 chưa được in đậm: {txt}"
            title_only = "".join(
                t.text
                for r_el in p_el.iter(f"{w_ns}r")
                if r_el.find(f"{w_ns}instrText") is None
                for t in r_el.findall(f"{w_ns}t")
                if t.text
            )
            for exp in expected_lvl1_titles:
                if exp in title_only:
                    bold_lvl1_titles.append(exp)
                    break
        else:
            assert not any(flags), f"Dòng không phải cấp 1 trong '{front_section}' bị in đậm: {txt}"

    assert bold_lvl1_titles == expected_lvl1_titles


def test_table_br_tags_render_as_word_linebreaks_without_smashing(tmp_path: Path) -> None:
    raw = (
        "| Mã | Điểm `criteria_scores`<br/>(`fee`; `district`) |\n"
        "|---|---|\n"
        "| KB01 | 1. GS-G01 (0,938)<br/>2. GS-G10 (0,745) |\n"
    )
    cleaned = preprocess_markdown(raw)
    assert "XTHESISBRX" in cleaned

    out = tmp_path / "br_test.docx"
    pypandoc.convert_text(
        cleaned,
        to="docx",
        format="markdown+tex_math_dollars+pipe_tables+raw_tex-implicit_figures",
        outputfile=str(out),
    )
    doc = docx.Document(str(out))
    build_docx._format_all_tables(doc)

    w_ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    hdr_xml = ET.fromstring(doc.tables[0].rows[0].cells[1]._tc.xml)
    assert len(hdr_xml.findall(f".//{w_ns}br")) >= 1
    hdr_p = hdr_xml.find(f".//{w_ns}p")
    assert hdr_p is not None
    hdr_txt = verify_docx_mod._paragraph_text_xml(hdr_p)
    assert "XTHESISBRX" not in hdr_txt
    assert "THESIS_BR" not in hdr_txt

    cell_xml = ET.fromstring(doc.tables[0].rows[1].cells[1]._tc.xml)
    assert len(cell_xml.findall(f".//{w_ns}br")) >= 1
    p_el = cell_xml.find(f".//{w_ns}p")
    assert p_el is not None
    txt = verify_docx_mod._paragraph_text_xml(p_el)
    assert "XTHESISBRX" not in txt
    assert ")2." not in txt
    assert txt.splitlines() == ["1. GS-G01 (0,938)", "2. GS-G10 (0,745)"]


def test_table_cells_unwrap_centered_omathpara(tmp_path: Path) -> None:
    raw = "| Tham số | Công thức |\n|---|---|\n| KN | $E_{\\max} = 8$ |\n"
    out = tmp_path / "math_test.docx"
    pypandoc.convert_text(
        raw,
        to="docx",
        format="markdown+tex_math_dollars+pipe_tables+raw_tex-implicit_figures",
        outputfile=str(out),
    )
    doc = docx.Document(str(out))
    # Wrap inline oMath into <m:oMathPara> (simulating WPS Writer promoting lone cell math)
    p_el = doc.tables[0].rows[1].cells[1].paragraphs[0]._p
    om_ns = "http://schemas.openxmlformats.org/officeDocument/2006/math"
    omath = p_el.find(f"{{{om_ns}}}oMath")
    assert omath is not None
    omp = docx.oxml.OxmlElement("m:oMathPara")
    pos = list(p_el).index(omath)
    p_el.remove(omath)
    omp.append(omath)
    p_el.insert(pos, omp)

    build_docx._format_all_tables(doc)

    tbl_xml = ET.fromstring(doc.tables[0]._tbl.xml)
    m_ns = f"{{{om_ns}}}"
    assert len(tbl_xml.findall(f".//{m_ns}oMathPara")) == 0
    assert len(tbl_xml.findall(f".//{m_ns}oMath")) >= 1


def test_verify_docx_rejects_smashed_table_text_and_nhom_truong() -> None:
    assert "XTHESISBRX" in verify_docx_mod.FORBIDDEN_STRINGS
    assert "THESIS_BR" in verify_docx_mod.FORBIDDEN_STRINGS
    assert "Nhóm trưởng" in verify_docx_mod.FORBIDDEN_STRINGS
    assert "nhóm em" in verify_docx_mod.FORBIDDEN_STRINGS
    assert "Nhóm em" in verify_docx_mod.FORBIDDEN_STRINGS

    w_ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    bad_tbl = ET.fromstring(
        '<w:tbl xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
        '<w:tblPr><w:tblBorders>'
        '<w:top w:val="single" w:sz="12"/><w:bottom w:val="single" w:sz="12"/><w:insideV w:val="none"/>'
        '</w:tblBorders></w:tblPr>'
        '<w:tr><w:trPr><w:tblHeader/><w:cantSplit/></w:trPr>'
        '<w:tc><w:tcPr><w:tcBorders><w:bottom w:val="single" w:sz="6"/></w:tcBorders></w:tcPr>'
        '<w:p><w:r><w:t>H</w:t></w:r></w:p></w:tc></w:tr>'
        '<w:tr><w:trPr><w:cantSplit/></w:trPr><w:tc><w:p>'
        '<w:r><w:t>1. A (0,9)2. B (0,8)</w:t></w:r>'
        '<m:oMathPara><m:oMath><m:r><m:t>x</m:t></m:r></m:oMath></m:oMathPara>'
        '</w:p></w:tc></w:tr>'
        '</w:tbl>'
    )
    errs = verify_docx_mod._verify_booktabs_table(bad_tbl, 1, w_ns)
    joined = " | ".join(errs)
    assert "oMathPara" in joined
    assert ")2." in joined or "dính" in joined


def test_smart_col_widths_splits_tokens_at_word_br(tmp_path: Path) -> None:
    fmt = "markdown+tex_math_dollars+pipe_tables+raw_tex-implicit_figures"
    raw_br = (
        "| Cột 1 | Cột 2 |\n"
        "|---|---|\n"
        "| alphatokenten<br/>betatokenten | ngắn gọn |\n"
    )
    raw_sp = (
        "| Cột 1 | Cột 2 |\n"
        "|---|---|\n"
        "| alphatokenten betatokenten | ngắn gọn |\n"
    )
    p_br = tmp_path / "t_br.docx"
    p_sp = tmp_path / "t_sp.docx"
    pypandoc.convert_text(preprocess_markdown(raw_br), to="docx", format=fmt, outputfile=str(p_br))
    pypandoc.convert_text(preprocess_markdown(raw_sp), to="docx", format=fmt, outputfile=str(p_sp))

    d_br = docx.Document(str(p_br))
    d_sp = docx.Document(str(p_sp))
    build_docx._expand_table_linebreaks(d_br)
    w_br = build_docx._compute_smart_col_widths(d_br.tables[0], build_docx.PRINTABLE_WIDTH_TWIPS)
    w_sp = build_docx._compute_smart_col_widths(d_sp.tables[0], build_docx.PRINTABLE_WIDTH_TWIPS)
    assert w_br == w_sp


def test_split_student_rows_accepts_hyphen_and_em_dash() -> None:
    rows, next_idx = build_docx._split_student_rows(
        [
            "Lê Thị Bích Chuyền - KHMT2411037",
            "Trần Nguyễn Đức — KHMT2411011",
            "Cao Khánh Ngọc - KHMT2411025",
            "**Lớp:** Khoa học máy tính 2024",
        ],
        0,
    )
    assert next_idx == 3
    assert rows == [
        ("Lê Thị Bích Chuyền", "KHMT2411037"),
        ("Trần Nguyễn Đức", "KHMT2411011"),
        ("Cao Khánh Ngọc", "KHMT2411025"),
    ]
