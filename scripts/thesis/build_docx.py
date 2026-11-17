"""Chuyển đổi và ghép toàn bộ báo cáo Markdown thành tệp Word (.docx) hoàn chỉnh."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import docx
import pypandoc
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Cm, Emu, Mm, Pt, RGBColor

REPO_ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = REPO_ROOT / "docs" / "thesis" / "report"

ORDER: tuple[str, ...] = (
    "muc-luc-va-ho-so-ban-giao.md",
    "chuong-01-tong-quan.md",
    "chuong-02-co-so-ly-thuyet-va-cong-nghe.md",
    "chuong-03-phan-tich-thiet-ke.md",
    "chuong-04-xay-dung-he-thong.md",
    "chuong-05-thuc-nghiem-va-danh-gia.md",
    "chuong-06-ket-luan-va-huong-phat-trien.md",
    "tai-lieu-tham-khao.md",
)

SENTINEL_MAIN_START = "[[THESIS_MAIN_SECTION_START]]"
SENTINEL_TOC_SLOT = "[[THESIS_TOC_SLOT]]"
SENTINEL_LOT_SLOT = "[[THESIS_LOT_SLOT]]"
SENTINEL_LOF_SLOT = "[[THESIS_LOF_SLOT]]"

ALERT_LABELS = {
    "NOTE": "Lưu ý:",
    "IMPORTANT": "Quan trọng:",
    "WARNING": "Cảnh báo:",
}

PRINTABLE_WIDTH_TWIPS = 9072  # 16.0 cm (21.0 - 3.0 - 2.0 cm)
MAX_IMAGE_WIDTH_EMU = int(Cm(15.5))
MAX_IMAGE_HEIGHT_EMU = int(Cm(19.0))


def preprocess_markdown(md_text: str, base_dir: Path | None = None) -> str:
    """Chuẩn hóa Markdown: chuyển alert GitHub thành văn xuôi, bỏ dòng '---' và chuẩn hóa đường dẫn ảnh."""
    lines = md_text.splitlines()
    out: list[str] = []
    in_code = False
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code = not in_code
            out.append(line)
            i += 1
            continue

        if in_code:
            out.append(line)
            i += 1
            continue

        # Bỏ dòng kẻ ngang Markdown ngoài khối mã
        if re.fullmatch(r"-{3,}", stripped):
            i += 1
            continue

        # Chuyển khối GitHub Alert: > [!NOTE] ...
        if m_alert := re.match(r"^>\s*\[!(NOTE|IMPORTANT|WARNING)\]\s*$", stripped):
            label = ALERT_LABELS[m_alert.group(1)]
            i += 1
            quote_lines: list[str] = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                qtext = re.sub(r"^>\s?", "", lines[i].lstrip()).strip()
                if qtext:
                    quote_lines.append(qtext)
                i += 1
            if quote_lines:
                out.append(f"**{label}** " + " ".join(quote_lines))
            continue

        # Chuẩn hóa đường dẫn ảnh tương đối nếu truyền base_dir
        if base_dir is not None and "![" in line:

            def _resolve_img(match: re.Match[str]) -> str:
                alt = match.group(1)
                raw_path = match.group(2).strip()
                candidate = (base_dir / raw_path).resolve()
                if candidate.exists():
                    return f"![{alt}]({candidate.as_posix()})"
                return match.group(0)

            line = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", _resolve_img, line)

        out.append(line)
        i += 1

    return "\n".join(out)


def split_appendix(ch6_md: str) -> tuple[str, str]:
    """Tách Chương 6 và phần Phụ lục A–D từ tệp chuong-06-ket-luan-va-huong-phat-trien.md."""
    lines = ch6_md.splitlines()
    split_idx: int | None = None
    for idx, line in enumerate(lines):
        if re.match(r"^#\s+PHỤ LỤC\s+A\b", line.strip()):
            split_idx = idx
            break
    if split_idx is None:
        raise ValueError("Không tìm thấy tiêu đề '# PHỤ LỤC A' trong Chương 6.")

    ch6_body = "\n".join(lines[:split_idx]).rstrip()
    # Bỏ dòng --- ngay trước Phụ lục A nếu còn
    ch6_body = re.sub(r"\n-{3,}\s*$", "", ch6_body).rstrip()
    appendix_md = "\n".join(lines[split_idx:]).strip()
    return ch6_body, appendix_md


def _extract_h2_sections(md_text: str) -> dict[str, str]:
    """Tách nội dung theo các đề mục cấp 2 (`## ...`)."""
    sections: dict[str, str] = {}
    current_key: str | None = None
    buf: list[str] = []
    in_code = False

    for line in md_text.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
        if not in_code and (m := re.match(r"^##\s+(\d+)\.\s+", line.strip())):
            if current_key is not None:
                sections[current_key] = "\n".join(buf).strip()
            current_key = m.group(1)
            buf = []
            continue
        if current_key is not None:
            buf.append(line)

    if current_key is not None:
        sections[current_key] = "\n".join(buf).strip()
    return sections


def split_front_matter(front_matter_md: str) -> dict[str, Any]:
    """Tách dữ liệu Bìa và 7 mục phần mở đầu hợp lệ (bỏ qua mục nội bộ 1, 2, 11 và bảng '…')."""
    sections = _extract_h2_sections(front_matter_md)

    # Mục 3: trích khối code bìa chính
    sec3 = sections.get("3", "")
    m_code = re.search(r"```[^\n]*\n(.*?)\n```", sec3, re.S)
    if not m_code:
        raise ValueError("Không tìm thấy khối nội dung trang bìa trong Mục 3.")
    cover_lines = [ln.rstrip() for ln in m_code.group(1).splitlines()]

    # Mục 6: tách Tóm tắt tiếng Việt (6.1) và Abstract tiếng Anh (6.2)
    sec6 = sections.get("6", "")
    m_abs = re.search(r"^###\s+6\.2\.\s+.*$", sec6, re.M)
    if m_abs:
        tom_tat_raw = sec6[: m_abs.start()]
        abstract_raw = sec6[m_abs.end() :]
    else:
        tom_tat_raw = sec6
        abstract_raw = ""
    tom_tat_vi = re.sub(r"^###\s+6\.1\.[^\n]*\n?", "", tom_tat_raw, flags=re.M).strip()
    abstract_en = abstract_raw.strip()

    # Mục 9 & 10: Danh mục bảng (31) và Danh mục hình (9)
    tables_list: list[tuple[str, str]] = []
    tables_note = ""
    for line in sections.get("9", "").splitlines():
        s = line.strip()
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if len(cells) >= 2 and re.match(r"^Bảng\s+[A-D0-9]+\.\d+$", cells[0]):
                tables_list.append((cells[0], cells[1]))
        elif s.startswith("**Tổng:"):
            tables_note = s

    figures_list: list[tuple[str, str]] = []
    figures_note = ""
    for line in sections.get("10", "").splitlines():
        s = line.strip()
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if len(cells) >= 2 and re.match(r"^Hình\s+[A-D0-9]+\.\d+$", cells[0]):
                figures_list.append((cells[0], cells[1]))
        elif s.startswith("**Tổng:"):
            figures_note = s

    return {
        "cover_lines": cover_lines,
        "loi_cam_on": preprocess_markdown(sections.get("4", "")),
        "loi_cam_doan": preprocess_markdown(sections.get("5", "")),
        "tom_tat_vi": preprocess_markdown(tom_tat_vi),
        "abstract_en": preprocess_markdown(abstract_en),
        "ky_hieu_viet_tat": preprocess_markdown(sections.get("8", "")),
        "tables_list": tables_list,
        "tables_note": tables_note,
        "figures_list": figures_list,
        "figures_note": figures_note,
    }


def _strip_theme_fonts_and_set(rpr_parent: Any, font_name: str, size_pt: float | None = None) -> None:
    """Gán font cố định vào XML và xóa thuộc tính Theme Font mặc định của Word/Pandoc."""
    rpr = rpr_parent.find(qn("w:rPr"))
    if rpr is None:
        rpr = OxmlElement("w:rPr")
        rpr_parent.insert(0, rpr)
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)

    for attr in ("asciiTheme", "hAnsiTheme", "cstheme", "eastAsiaTheme"):
        rfonts.attrib.pop(qn(f"w:{attr}"), None)
    for attr in ("ascii", "hAnsi", "cs", "eastAsia"):
        rfonts.set(qn(f"w:{attr}"), font_name)

    if size_pt is not None:
        half_pts = str(int(round(size_pt * 2)))
        for tag in ("w:sz", "w:szCs"):
            el = rpr.find(qn(tag))
            if el is None:
                el = OxmlElement(tag)
                rpr.append(el)
            el.set(qn("w:val"), half_pts)


def create_reference_docx(out_path: Path) -> Path:
    """Tạo tệp reference.docx chuẩn A4, lề luận văn và phông Times New Roman từ mẫu gốc Pandoc."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pandoc_exe = pypandoc.get_pandoc_path()
    proc = subprocess.run(
        [pandoc_exe, "--print-default-data-file=reference.docx"],
        capture_output=True,
        check=True,
    )
    out_path.write_bytes(proc.stdout)

    doc = docx.Document(str(out_path))
    sec = doc.sections[0]
    sec.page_width = Mm(210)
    sec.page_height = Mm(297)
    sec.top_margin = Cm(2.5)
    sec.bottom_margin = Cm(2.0)
    sec.left_margin = Cm(3.0)
    sec.right_margin = Cm(2.0)
    sec.header_distance = Cm(1.25)
    sec.footer_distance = Cm(1.25)

    # Thiết lập docDefaults về Times New Roman 13 pt
    styles_el = doc.styles.element
    for rpr_def in styles_el.xpath(".//w:docDefaults/w:rPrDefault"):
        _strip_theme_fonts_and_set(rpr_def, "Times New Roman", size_pt=13)

    black = RGBColor(0x00, 0x00, 0x00)
    style_specs: list[tuple[str, float, bool, bool, Any, float, float, float, float]] = [
        # name, size, bold, italic, align, line_spacing, before, after, first_indent_cm
        ("Normal", 13.0, False, False, WD_ALIGN_PARAGRAPH.LEFT, 1.3, 3.0, 4.0, 0.0),
        ("Body Text", 13.0, False, False, WD_ALIGN_PARAGRAPH.JUSTIFY, 1.3, 3.0, 4.0, 1.0),
        ("First Paragraph", 13.0, False, False, WD_ALIGN_PARAGRAPH.JUSTIFY, 1.3, 3.0, 4.0, 1.0),
        ("Compact", 13.0, False, False, WD_ALIGN_PARAGRAPH.LEFT, 1.25, 2.0, 2.0, 0.0),
        ("Block Text", 12.5, False, False, WD_ALIGN_PARAGRAPH.JUSTIFY, 1.25, 3.0, 4.0, 0.0),
        ("Heading 1", 15.0, True, False, WD_ALIGN_PARAGRAPH.CENTER, 1.2, 6.0, 12.0, 0.0),
        ("Heading 2", 14.0, True, False, WD_ALIGN_PARAGRAPH.LEFT, 1.25, 10.0, 4.0, 0.0),
        ("Heading 3", 13.0, True, True, WD_ALIGN_PARAGRAPH.LEFT, 1.25, 8.0, 3.0, 0.0),
        ("Heading 4", 13.0, False, True, WD_ALIGN_PARAGRAPH.LEFT, 1.25, 6.0, 2.0, 0.0),
        ("Caption", 11.0, True, False, WD_ALIGN_PARAGRAPH.CENTER, 1.15, 4.0, 4.0, 0.0),
        ("Image Caption", 11.0, True, False, WD_ALIGN_PARAGRAPH.CENTER, 1.15, 4.0, 6.0, 0.0),
        ("Title", 16.0, True, False, WD_ALIGN_PARAGRAPH.CENTER, 1.2, 6.0, 10.0, 0.0),
    ]

    for (
        sname,
        size,
        bold,
        italic,
        align,
        lsp,
        sbefore,
        safter,
        findent_cm,
    ) in style_specs:
        if sname not in doc.styles:
            continue
        st = doc.styles[sname]
        st.font.name = "Times New Roman"
        st.font.size = Pt(size)
        st.font.bold = bold
        st.font.italic = italic
        st.font.color.rgb = black
        _strip_theme_fonts_and_set(st._element, "Times New Roman", size_pt=size)
        pf = st.paragraph_format
        pf.alignment = align
        pf.line_spacing = lsp
        pf.space_before = Pt(sbefore)
        pf.space_after = Pt(safter)
        pf.first_line_indent = Cm(findent_cm)
        if sname.startswith("Heading"):
            pf.keep_with_next = True

    if "Verbatim Char" in doc.styles:
        vc = doc.styles["Verbatim Char"]
        vc.font.name = "Times New Roman"
        _strip_theme_fonts_and_set(vc._element, "Times New Roman")
    if "Source Code" in doc.styles:
        sc = doc.styles["Source Code"]
        sc.font.name = "Consolas"
        sc.font.size = Pt(10)
        _strip_theme_fonts_and_set(sc._element, "Consolas", size_pt=10)
        sc.paragraph_format.first_line_indent = Cm(0)
        sc.paragraph_format.line_spacing = 1.15
        sc.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

    for i in range(1, 5):
        tname = f"TOC {i}"
        if tname in doc.styles:
            tst = doc.styles[tname]
            tst.font.name = "Times New Roman"
            tst.font.size = Pt(13 if i == 1 else 12)
            _strip_theme_fonts_and_set(tst._element, "Times New Roman", size_pt=(13 if i == 1 else 12))

    doc.save(str(out_path))
    return out_path


def _add_field_to_paragraph(
    paragraph: docx.text.paragraph.Paragraph,
    instr: str,
    default_text: str = "",
    *,
    bold: bool = False,
    font_size: float = 13.0,
) -> None:
    """Chèn trường động Word (PAGE, TOC, PAGEREF) vào một đoạn."""
    def _mk_run(text: str | None = None) -> Any:
        r = paragraph.add_run(text or "")
        r.font.name = "Times New Roman"
        r.font.size = Pt(font_size)
        r.font.bold = bold
        _strip_theme_fonts_and_set(r._element, "Times New Roman", size_pt=font_size)
        return r

    r_begin = _mk_run()
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    r_begin._r.append(fld_begin)

    r_instr = _mk_run()
    instr_el = OxmlElement("w:instrText")
    instr_el.set(qn("xml:space"), "preserve")
    instr_el.text = f" {instr} "
    r_instr._r.append(instr_el)

    r_sep = _mk_run()
    fld_sep = OxmlElement("w:fldChar")
    fld_sep.set(qn("w:fldCharType"), "separate")
    r_sep._r.append(fld_sep)

    if default_text:
        _mk_run(default_text)

    r_end = _mk_run()
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    r_end._r.append(fld_end)


def _configure_section_page_layout(
    sec: docx.section.Section,
    *,
    page_num_fmt: str | None,
    start_num: int | None = None,
    first_page_border: bool = False,
) -> None:
    """Cấu hình khổ A4, lề, số trang chân trang và viền trang bìa cho một Section."""
    sec.page_width = Mm(210)
    sec.page_height = Mm(297)
    sec.top_margin = Cm(2.5)
    sec.bottom_margin = Cm(2.0)
    sec.left_margin = Cm(3.0)
    sec.right_margin = Cm(2.0)
    sec.header_distance = Cm(1.25)
    sec.footer_distance = Cm(1.25)

    sect_pr = sec._sectPr
    for old in sect_pr.findall(qn("w:pgNumType")):
        sect_pr.remove(old)
    if page_num_fmt is not None:
        pg_num = OxmlElement("w:pgNumType")
        pg_num.set(qn("w:fmt"), page_num_fmt)
        if start_num is not None:
            pg_num.set(qn("w:start"), str(start_num))
        sect_pr.append(pg_num)

    for old in sect_pr.findall(qn("w:pgBorders")):
        sect_pr.remove(old)
    if first_page_border:
        pg_borders = parse_xml(
            f'<w:pgBorders {nsdecls("w")} w:offsetFrom="page" w:display="firstPage">'
            '<w:top w:val="double" w:sz="6" w:space="24" w:color="1F4E79"/>'
            '<w:left w:val="double" w:sz="6" w:space="24" w:color="1F4E79"/>'
            '<w:bottom w:val="double" w:sz="6" w:space="24" w:color="1F4E79"/>'
            '<w:right w:val="double" w:sz="6" w:space="24" w:color="1F4E79"/>'
            "</w:pgBorders>"
        )
        sect_pr.append(pg_borders)

    sec.footer.is_linked_to_previous = False
    sec.header.is_linked_to_previous = False
    footer_p = sec.footer.paragraphs[0]
    footer_p.text = ""
    footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer_p.paragraph_format.first_line_indent = Cm(0)
    if page_num_fmt is not None:
        _add_field_to_paragraph(footer_p, "PAGE", "", font_size=11.0)


def _format_cover_paragraph(
    p: docx.text.paragraph.Paragraph,
    text: str,
    *,
    size: float,
    bold: bool = False,
    italic: bool = False,
    align: Any = WD_ALIGN_PARAGRAPH.CENTER,
    space_before: float = 0.0,
    space_after: float = 4.0,
    left_indent_cm: float = 0.0,
) -> None:
    p.alignment = align
    pf = p.paragraph_format
    pf.first_line_indent = Cm(0)
    pf.left_indent = Cm(left_indent_cm)
    pf.line_spacing = 1.25
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    _strip_theme_fonts_and_set(run._element, "Times New Roman", size_pt=size)


def _insert_cover_pages_before_first_paragraph(
    doc: docx.document.Document,
    anchor_p: docx.text.paragraph.Paragraph,
    cover_lines: list[str],
) -> None:
    """Chèn Trang bìa chính và Trang bìa phụ (cùng bố cục) + ngắt Section trước phần mở đầu."""
    non_empty = [ln.strip() for ln in cover_lines if ln.strip()]
    # Tách cấu trúc thông tin từ khối văn bản bìa trong muc-luc-va-ho-so-ban-giao.md
    org_top = non_empty[0] if len(non_empty) > 0 else ""
    school = non_empty[1] if len(non_empty) > 1 else ""
    faculty = non_empty[2] if len(non_empty) > 2 else ""
    sep_line = non_empty[3] if len(non_empty) > 3 else "----***----"
    report_type = non_empty[4] if len(non_empty) > 4 else ""
    title_lines = [ln for ln in non_empty[5:7]]
    advisor = non_empty[7] if len(non_empty) > 7 else ""
    student_header = non_empty[8] if len(non_empty) > 8 else ""
    student_lines = [re.sub(r"\s{2,}", "  —  ", ln) for ln in non_empty[9:-2]]
    class_line = non_empty[-2] if len(non_empty) >= 2 else ""
    place_date = non_empty[-1] if non_empty else ""

    def _emit_single_cover(page_break_after: bool, is_last: bool) -> None:
        _format_cover_paragraph(anchor_p.insert_paragraph_before(""), org_top, size=13, space_after=2)
        _format_cover_paragraph(anchor_p.insert_paragraph_before(""), school, size=13, bold=True, space_after=2)
        _format_cover_paragraph(anchor_p.insert_paragraph_before(""), faculty, size=13, bold=True, space_after=2)
        _format_cover_paragraph(anchor_p.insert_paragraph_before(""), sep_line, size=12, space_after=36)
        _format_cover_paragraph(anchor_p.insert_paragraph_before(""), report_type, size=14, bold=True, space_before=18, space_after=14)
        for idx, tline in enumerate(title_lines):
            _format_cover_paragraph(
                anchor_p.insert_paragraph_before(""),
                tline,
                size=16.5,
                bold=True,
                space_before=(6 if idx == 0 else 0),
                space_after=(48 if idx == len(title_lines) - 1 else 4),
            )
        _format_cover_paragraph(anchor_p.insert_paragraph_before(""), advisor, size=13, bold=True, space_before=24, space_after=24)
        _format_cover_paragraph(anchor_p.insert_paragraph_before(""), student_header, size=13, bold=True, space_after=6)
        for sline in student_lines:
            _format_cover_paragraph(
                anchor_p.insert_paragraph_before(""),
                sline,
                size=13,
                align=WD_ALIGN_PARAGRAPH.LEFT,
                left_indent_cm=2.2,
                space_after=4,
            )
        _format_cover_paragraph(anchor_p.insert_paragraph_before(""), class_line, size=13, space_before=18, space_after=60)
        last_p = anchor_p.insert_paragraph_before("")
        _format_cover_paragraph(last_p, place_date, size=13, bold=True, space_before=18, space_after=0)
        if page_break_after:
            last_p.add_run().add_break(docx.enum.text.WD_BREAK.PAGE)
        if is_last:
            # Gắn section break (nextPage) từ Section 1 -> Section 2
            ppr = last_p._p.get_or_add_pPr()
            sect_pr = parse_xml(f'<w:sectPr {nsdecls("w")}><w:type w:val="nextPage"/></w:sectPr>')
            ppr.append(sect_pr)

    # Trang bìa chính (ngắt trang sang bìa phụ) + Trang bìa phụ (ngắt section sang phần mở đầu)
    _emit_single_cover(page_break_after=True, is_last=False)
    _emit_single_cover(page_break_after=False, is_last=True)


def _slug_bookmark(caption_label: str) -> str:
    """Chuyển 'Bảng 1.1' / 'Hình 3.2' / 'Bảng A.1' thành tên bookmark Word hợp lệ."""
    clean = caption_label.lower().replace("ả", "a").replace("ì", "i").replace(".", "_")
    clean = re.sub(r"[^a-z0-9_]+", "_", clean).strip("_")
    return f"bm_{clean}"[:39]


def _bookmark_caption_paragraphs(doc: docx.document.Document) -> dict[str, str]:
    """Đánh bookmark cho toàn bộ caption Bảng X.Y và Hình X.Y trong phần nội dung."""
    existing_ids = [
        int(el.get(qn("w:id"), "0"))
        for el in doc.element.body.xpath(".//w:bookmarkStart")
        if (el.get(qn("w:id")) or "").isdigit()
    ]
    next_id = (max(existing_ids) + 1) if existing_ids else 100

    label_to_bm: dict[str, str] = {}
    in_main = False
    for p in doc.paragraphs:
        txt = p.text.strip()
        if txt.startswith("CHƯƠNG 1"):
            in_main = True
        if not in_main:
            continue

        m = re.match(r"^((?:Bảng|Hình)\s+[A-D0-9]+\.\d+)\s*[-–:]", txt)
        if not m:
            continue
        label = re.sub(r"\s+", " ", m.group(1).strip())
        bm_name = _slug_bookmark(label)
        if label in label_to_bm:
            continue
        label_to_bm[label] = bm_name

        b_start = OxmlElement("w:bookmarkStart")
        b_start.set(qn("w:id"), str(next_id))
        b_start.set(qn("w:name"), bm_name)
        b_end = OxmlElement("w:bookmarkEnd")
        b_end.set(qn("w:id"), str(next_id))
        next_id += 1

        # Đặt bookmarkStart trước nội dung run đầu và bookmarkEnd cuối đoạn
        p._p.insert(1 if p._p.pPr is not None else 0, b_start)
        p._p.append(b_end)

    return label_to_bm


def _insert_toc_at_sentinel(
    doc: docx.document.Document,
    sentinel_p: docx.text.paragraph.Paragraph,
    label_to_bm: dict[str, str],
) -> None:
    """Chèn trường TOC động Word tại vị trí MỤC LỤC và xóa đoạn sentinel."""
    # Không đưa chữ 'MỤC LỤC' vào cấp outline 1 để mục lục không tự liệt kê chính mình
    title_p = sentinel_p.insert_paragraph_before("")
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = title_p.paragraph_format
    pf.page_break_before = True
    pf.first_line_indent = Cm(0)
    pf.space_before = Pt(6)
    pf.space_after = Pt(12)
    pf.keep_with_next = True
    r = title_p.add_run("MỤC LỤC")
    r.font.name = "Times New Roman"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    _strip_theme_fonts_and_set(r._element, "Times New Roman", size_pt=15)

    toc_p = sentinel_p.insert_paragraph_before("")
    toc_p.paragraph_format.first_line_indent = Cm(0)
    toc_p.paragraph_format.space_before = Pt(2)
    toc_p.paragraph_format.space_after = Pt(6)
    _add_field_to_paragraph(
        toc_p,
        'TOC \\o "1-3" \\h \\z \\u',
        default_text=(
            "Mục lục tự động (mở bằng Microsoft Word hoặc WPS Writer và chọn "
            "Update Field / nhấn Ctrl+A rồi F9 để cập nhật số trang mới nhất)."
        ),
        font_size=12.0,
    )
    sentinel_p._element.getparent().remove(sentinel_p._element)


def _insert_ref_list_table_at_sentinel(
    doc: docx.document.Document,
    sentinel_p: docx.text.paragraph.Paragraph,
    entries: list[tuple[str, str]],
    summary_note: str,
    label_to_bm: dict[str, str],
    col_header_id: str,
    col_header_title: str,
) -> None:
    """Thay thế sentinel bằng bảng Danh mục bảng/hình có trường PAGEREF trỏ tới từng caption."""
    parent = sentinel_p._element.getparent()
    idx_in_parent = list(parent).index(sentinel_p._element)

    table = doc.add_table(rows=1 + len(entries), cols=3)
    table.style = "Table Grid" if "Table Grid" in doc.styles else table.style
    # Di chuyển bảng từ cuối tài liệu lên ngay trước sentinel
    parent.remove(table._tbl)
    parent.insert(idx_in_parent, table._tbl)

    headers = [col_header_id, col_header_title, "Trang"]
    for ci, htext in enumerate(headers):
        cell = table.rows[0].cells[ci]
        p = cell.paragraphs[0]
        p.text = ""
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if ci != 1 else WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(htext)
        run.font.bold = True
        run.font.name = "Times New Roman"
        run.font.size = Pt(11)
        _strip_theme_fonts_and_set(run._element, "Times New Roman", size_pt=11)

    for ri, (label, title) in enumerate(entries, start=1):
        row = table.rows[ri]
        # Cột 0: Số hiệu
        p0 = row.cells[0].paragraphs[0]
        p0.text = ""
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r0 = p0.add_run(label)
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(11)
        _strip_theme_fonts_and_set(r0._element, "Times New Roman", size_pt=11)

        # Cột 1: Tên bảng / hình (giữ công thức toán inline dạng chữ sạch nếu có)
        p1 = row.cells[1].paragraphs[0]
        p1.text = ""
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        clean_title = (
            title.replace("$\\delta$", "δ")
            .replace("$E_{\\max}$", "E_max")
            .replace("$\\sum w_i = 0$", "∑w_i = 0")
            .replace("`", "")
        )
        r1 = p1.add_run(clean_title)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        _strip_theme_fonts_and_set(r1._element, "Times New Roman", size_pt=11)

        # Cột 2: Trường PAGEREF trỏ tới bookmark caption
        p2 = row.cells[2].paragraphs[0]
        p2.text = ""
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        bm_name = label_to_bm.get(label)
        if bm_name:
            _add_field_to_paragraph(p2, f"PAGEREF {bm_name} \\h", default_text="-", font_size=11.0)
        else:
            r2 = p2.add_run("-")
            r2.font.name = "Times New Roman"
            r2.font.size = Pt(11)
            _strip_theme_fonts_and_set(r2._element, "Times New Roman", size_pt=11)

    # Ghi dòng Tổng dưới bảng
    if summary_note:
        note_p = sentinel_p.insert_paragraph_before("")
        note_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        note_p.paragraph_format.first_line_indent = Cm(0)
        note_p.paragraph_format.space_before = Pt(4)
        note_p.paragraph_format.space_after = Pt(6)
        clean_note = summary_note.replace("**", "")
        rn = note_p.add_run(clean_note)
        rn.font.name = "Times New Roman"
        rn.font.size = Pt(12)
        rn.font.bold = True
        _strip_theme_fonts_and_set(rn._element, "Times New Roman", size_pt=12)

    parent.remove(sentinel_p._element)


def _format_all_tables(doc: docx.document.Document) -> None:
    """Định dạng khung viền, tiêu đề lặp trang, ngắt dòng và kích thước cho mọi bảng."""
    border_xml = (
        f'<w:tblBorders {nsdecls("w")}>'
        '<w:top w:val="single" w:sz="6" w:space="0" w:color="404040"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        '<w:bottom w:val="single" w:sz="6" w:space="0" w:color="404040"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="B0B0B0"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="C8C8C8"/>'
        "</w:tblBorders>"
    )
    cell_mar_xml = (
        f'<w:tblCellMar {nsdecls("w")}>'
        '<w:top w:w="60" w:type="dxa"/>'
        '<w:left w:w="90" w:type="dxa"/>'
        '<w:bottom w:w="60" w:type="dxa"/>'
        '<w:right w:w="90" w:type="dxa"/>'
        "</w:tblCellMar>"
    )

    for tbl in doc.tables:
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl_pr = tbl._tbl.tblPr
        for tag in ("w:tblBorders", "w:tblCellMar", "w:tblW"):
            for old in tbl_pr.findall(qn(tag)):
                tbl_pr.remove(old)

        tbl_w = OxmlElement("w:tblW")
        tbl_w.set(qn("w:w"), str(PRINTABLE_WIDTH_TWIPS))
        tbl_w.set(qn("w:type"), "dxa")
        tbl_pr.append(tbl_w)
        tbl_pr.append(parse_xml(border_xml))
        tbl_pr.append(parse_xml(cell_mar_xml))

        # Căn tỷ lệ độ rộng cột cho vừa khít PRINTABLE_WIDTH_TWIPS
        grid_cols = tbl._tbl.xpath("./w:tblGrid/w:gridCol")
        if grid_cols:
            widths = [
                int(col.get(qn("w:w"))) if (col.get(qn("w:w")) or "").isdigit() else 1000
                for col in grid_cols
            ]
            total_w = sum(widths) or len(grid_cols) * 1000
            scaled_widths = [max(450, round(w * PRINTABLE_WIDTH_TWIPS / total_w)) for w in widths]
            # Chỉnh sai số làm tròn ở cột dài nhất
            diff = PRINTABLE_WIDTH_TWIPS - sum(scaled_widths)
            max_idx = max(range(len(scaled_widths)), key=lambda idx: scaled_widths[idx])
            scaled_widths[max_idx] = max(450, scaled_widths[max_idx] + diff)
            for col, sw in zip(grid_cols, scaled_widths):
                col.set(qn("w:w"), str(sw))
        else:
            scaled_widths = []

        for r_idx, row in enumerate(tbl.rows):
            tr_pr = row._tr.get_or_add_trPr()
            if tr_pr.find(qn("w:cantSplit")) is None:
                tr_pr.append(OxmlElement("w:cantSplit"))
            if r_idx == 0 and tr_pr.find(qn("w:tblHeader")) is None:
                tr_pr.append(OxmlElement("w:tblHeader"))

            for c_idx, cell in enumerate(row.cells):
                tc_pr = cell._tc.get_or_add_tcPr()
                if c_idx < len(scaled_widths):
                    for old_w in tc_pr.findall(qn("w:tcW")):
                        tc_pr.remove(old_w)
                    tc_w = OxmlElement("w:tcW")
                    tc_w.set(qn("w:w"), str(scaled_widths[c_idx]))
                    tc_w.set(qn("w:type"), "dxa")
                    tc_pr.append(tc_w)

                if r_idx == 0:
                    for old_shd in tc_pr.findall(qn("w:shd")):
                        tc_pr.remove(old_shd)
                    tc_pr.append(
                        parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="D9E1F2"/>')
                    )

                for p in cell.paragraphs:
                    pf = p.paragraph_format
                    pf.first_line_indent = Cm(0)
                    pf.line_spacing = 1.15
                    pf.space_before = Pt(1)
                    pf.space_after = Pt(1)
                    if r_idx == 0:
                        pf.keep_with_next = True
                    for run in p.runs:
                        run.font.name = "Times New Roman"
                        run.font.size = Pt(10.5)
                        run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
                        if r_idx == 0:
                            run.font.bold = True
                        _strip_theme_fonts_and_set(run._element, "Times New Roman", size_pt=10.5)


def _scale_images_and_style_paragraphs(doc: docx.document.Document) -> None:
    """Chuẩn hóa phông, ngắt trang H1, kích thước ảnh, caption bảng/hình và tài liệu tham khảo."""
    in_references = False
    seen_main_h1 = False
    paras = doc.paragraphs

    for idx, p in enumerate(paras):
        txt = p.text.strip()
        sname = p.style.name if p.style else ""

        if txt == "TÀI LIỆU THAM KHẢO":
            in_references = True
        elif txt.startswith("PHỤ LỤC A"):
            in_references = False

        # Bỏ thụt đầu dòng trong các đoạn danh sách có numPr
        has_numpr = p._p.pPr is not None and p._p.pPr.find(qn("w:numPr")) is not None
        if has_numpr:
            p.paragraph_format.first_line_indent = Cm(0)

        # Heading 1: ngắt trang sạch cho Chương 1..6, Tài liệu tham khảo, Phụ lục A..D và Front Matter
        if sname == "Heading 1":
            p.paragraph_format.keep_with_next = True
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if txt.startswith("CHƯƠNG 1"):
                # Chương 1 đã nằm ngay sau Section Break -> không cần page_break_before
                seen_main_h1 = True
                p.paragraph_format.page_break_before = False
            elif txt == "LỜI CẢM ƠN":
                # Lời cảm ơn nằm ngay sau Section Break từ Bìa -> không cần page_break_before
                p.paragraph_format.page_break_before = False
            else:
                p.paragraph_format.page_break_before = True

        # Caption Bảng X.Y -> căn trái/giữa rõ ràng và keep_with_next với bảng phía dưới
        if re.match(r"^Bảng\s+[A-D0-9]+\.\d+\s*[-–:]", txt):
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.keep_with_next = True
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(3)
            for run in p.runs:
                run.font.bold = True
                run.font.size = Pt(11.5)
                _strip_theme_fonts_and_set(run._element, "Times New Roman", size_pt=11.5)

        # Caption Hình X.Y -> căn giữa bên dưới hình
        if re.match(r"^Hình\s+[A-D0-9]+\.\d+\s*[-–:]", txt):
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            for run in p.runs:
                run.font.bold = True
                run.font.size = Pt(11.0)
                _strip_theme_fonts_and_set(run._element, "Times New Roman", size_pt=11.0)

        # Dòng Nguồn / Ghi chú bên dưới bảng hoặc hình
        if txt.startswith(("Nguồn:", "Ghi chú:")):
            prev_txt = paras[idx - 1].text.strip() if idx > 0 else ""
            is_fig_note = bool(re.match(r"^Hình\s+[A-D0-9]+\.\d+", prev_txt))
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if is_fig_note else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(6)
            for run in p.runs:
                run.font.size = Pt(11.0)
                _strip_theme_fonts_and_set(run._element, "Times New Roman", size_pt=11.0)

        # Đoạn chứa hình ảnh (<w:drawing>)
        drawings = p._p.xpath(".//w:drawing")
        if drawings:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.keep_with_next = True
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(3)
            for drw in drawings:
                for ext in drw.xpath(".//wp:extent | .//a:xfrm/a:ext"):
                    cx_raw = ext.get("cx")
                    cy_raw = ext.get("cy")
                    if cx_raw and cy_raw and cx_raw.isdigit() and cy_raw.isdigit():
                        cx = int(cx_raw)
                        cy = int(cy_raw)
                        scale = min(1.0, MAX_IMAGE_WIDTH_EMU / max(cx, 1), MAX_IMAGE_HEIGHT_EMU / max(cy, 1))
                        # Phóng ảnh UI chụp màn hình nhỏ hơn khung 15.5 cm lên vừa khung chuẩn
                        if cx > int(Cm(8)):
                            scale = min(MAX_IMAGE_WIDTH_EMU / cx, MAX_IMAGE_HEIGHT_EMU / cy)
                        ext.set("cx", str(int(cx * scale)))
                        ext.set("cy", str(int(cy * scale)))

        # Tài liệu tham khảo [1]..[11]: hanging indent
        if in_references and re.match(r"^\[\d+\]\s+", txt):
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.left_indent = Cm(0.9)
            p.paragraph_format.first_line_indent = Cm(-0.9)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(4)

        # Bảo đảm toàn bộ run ngoài khối mã nguồn đều mang Times New Roman, màu đen
        if sname != "Source Code":
            for run in p.runs:
                run.font.name = "Times New Roman"
                if run.font.color and run.font.color.rgb not in (None, RGBColor(0x00, 0x00, 0x00)):
                    run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
                _strip_theme_fonts_and_set(run._element, "Times New Roman")
        # Làm sạch OMML font về Cambria Math mặc định (chuẩn Word/WPS) — không ép Times New Roman lên m:r

        _ = seen_main_h1


def _split_sections_at_main_sentinel(doc: docx.document.Document) -> None:
    """Chèn Section Break giữa Section 2 (Front Matter) và Section 3 (Nội dung chính) tại sentinel."""
    for p in doc.paragraphs:
        if p.text.strip() == SENTINEL_MAIN_START:
            p.text = ""
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            ppr = p._p.get_or_add_pPr()
            sect_pr = parse_xml(f'<w:sectPr {nsdecls("w")}><w:type w:val="nextPage"/></w:sectPr>')
            ppr.append(sect_pr)
            return
    raise RuntimeError("Không tìm thấy sentinel phân tách Section 2 và Section 3.")


def _enable_auto_update_fields(doc: docx.document.Document) -> None:
    settings_el = doc.settings.element
    for old in settings_el.findall(qn("w:updateFields")):
        settings_el.remove(old)
    upd = OxmlElement("w:updateFields")
    upd.set(qn("w:val"), "true")
    settings_el.append(upd)


def _try_update_fields_with_wps(docx_path: Path) -> bool:
    """Thử cập nhật số trang TOC/PAGEREF qua WPS Writer COM (timeout 15s, an toàn nếu bị chặn)."""
    ps_script = f"""
$ErrorActionPreference = 'Stop'
$wps = $null
try {{
    $wps = New-Object -ComObject Kwps.Application
    $wps.Visible = $false
    $wps.DisplayAlerts = 0
    $doc = $wps.Documents.Open('{str(docx_path).replace("'", "''")}', $false, $false)
    foreach ($toc in $doc.TablesOfContents) {{ $toc.Update() }}
    $doc.Fields.Update() | Out-Null
    $doc.Save()
    $doc.Close($false)
    Write-Output 'WPS_COM_OK'
}} finally {{
    if ($wps -ne $null) {{
        try {{ $wps.Quit() }} catch {{}}
    }}
}}
"""
    try:
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        return proc.returncode == 0 and "WPS_COM_OK" in proc.stdout
    except Exception:
        return False


def build(
    repo_root: Path = REPO_ROOT,
    output_path: Path | None = None,
    mirror_output_path: Path | None = None,
    try_wps_com: bool = False,
) -> Path:
    """Ghép toàn bộ báo cáo Markdown và xuất tệp .docx hoàn chỉnh."""
    report_dir = repo_root / "docs" / "thesis" / "report"
    out_file = (
        output_path
        if output_path is not None
        else repo_root.parent / "BAO_CAO_DO_AN_KHMT1_HOAN_CHINH.docx"
    )
    ref_docx = repo_root / "scripts" / "thesis" / "reference.docx"
    create_reference_docx(ref_docx)

    fm_md = (report_dir / "muc-luc-va-ho-so-ban-giao.md").read_text(encoding="utf-8")
    fm_parts = split_front_matter(fm_md)

    chapters_md: list[str] = []
    for fname in ORDER[1:-1]:
        raw = (report_dir / fname).read_text(encoding="utf-8")
        if fname.startswith("chuong-06"):
            ch6_body, appendix_md = split_appendix(raw)
            chapters_md.append(preprocess_markdown(ch6_body, base_dir=report_dir))
        else:
            chapters_md.append(preprocess_markdown(raw, base_dir=report_dir))

    refs_md = preprocess_markdown(
        (report_dir / "tai-lieu-tham-khao.md").read_text(encoding="utf-8"),
        base_dir=report_dir,
    )
    appendix_clean = preprocess_markdown(appendix_md, base_dir=report_dir)

    combined_md_sections = [
        "# LỜI CẢM ƠN",
        fm_parts["loi_cam_on"],
        "# LỜI CAM ĐOAN LIÊM CHÍNH HỌC THUẬT",
        fm_parts["loi_cam_doan"],
        "# TÓM TẮT",
        fm_parts["tom_tat_vi"],
        "# ABSTRACT",
        fm_parts["abstract_en"],
        SENTINEL_TOC_SLOT,
        "# DANH MỤC KÝ HIỆU VÀ CHỮ VIẾT TẮT",
        fm_parts["ky_hieu_viet_tat"],
        "# DANH MỤC BẢNG BIỂU",
        SENTINEL_LOT_SLOT,
        "# DANH MỤC HÌNH VẼ, SƠ ĐỒ, BIỂU ĐỒ",
        SENTINEL_LOF_SLOT,
        SENTINEL_MAIN_START,
        *chapters_md,
        refs_md,
        appendix_clean,
    ]
    combined_md = "\n\n".join(combined_md_sections)

    resource_paths = os.pathsep.join(
        [
            str(report_dir),
            str(repo_root / "docs" / "thesis" / "figures"),
            str(repo_root / "docs" / "thesis" / "assets" / "midterm"),
        ]
    )

    out_file.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
        tmp_docx = Path(tmp.name)

    try:
        pypandoc.convert_text(
            combined_md,
            to="docx",
            format="markdown+tex_math_dollars+pipe_tables+raw_tex-implicit_figures",
            outputfile=str(tmp_docx),
            extra_args=[
                f"--reference-doc={ref_docx}",
                f"--resource-path={resource_paths}",
            ],
        )

        doc = docx.Document(str(tmp_docx))
        if not doc.paragraphs:
            raise RuntimeError("Tài liệu DOCX sinh ra từ Pandoc bị rỗng.")

        anchor_first = doc.paragraphs[0]
        _insert_cover_pages_before_first_paragraph(doc, anchor_first, fm_parts["cover_lines"])
        _split_sections_at_main_sentinel(doc)

        label_to_bm = _bookmark_caption_paragraphs(doc)

        for p in list(doc.paragraphs):
            t = p.text.strip()
            if t == SENTINEL_TOC_SLOT:
                _insert_toc_at_sentinel(doc, p, label_to_bm)
            elif t == SENTINEL_LOT_SLOT:
                _insert_ref_list_table_at_sentinel(
                    doc,
                    p,
                    fm_parts["tables_list"],
                    fm_parts["tables_note"],
                    label_to_bm,
                    "Số hiệu",
                    "Tên bảng",
                )
            elif t == SENTINEL_LOF_SLOT:
                _insert_ref_list_table_at_sentinel(
                    doc,
                    p,
                    fm_parts["figures_list"],
                    fm_parts["figures_note"],
                    label_to_bm,
                    "Số hiệu",
                    "Tên hình",
                )

        _format_all_tables(doc)
        _scale_images_and_style_paragraphs(doc)

        if len(doc.sections) != 3:
            raise RuntimeError(f"Kỳ vọng 3 Section nhưng thu được {len(doc.sections)} Section.")

        _configure_section_page_layout(
            doc.sections[0], page_num_fmt=None, first_page_border=True
        )
        _configure_section_page_layout(
            doc.sections[1], page_num_fmt="lowerRoman", start_num=1, first_page_border=False
        )
        _configure_section_page_layout(
            doc.sections[2], page_num_fmt="decimal", start_num=1, first_page_border=False
        )

        _enable_auto_update_fields(doc)
        doc.save(str(out_file))
    finally:
        if tmp_docx.exists():
            tmp_docx.unlink()

    if try_wps_com:
        _try_update_fields_with_wps(out_file)

    if mirror_output_path is not None:
        mirror_output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(out_file, mirror_output_path)

    return out_file


def main() -> int:
    default_out = REPO_ROOT.parent / "BAO_CAO_DO_AN_KHMT1_HOAN_CHINH.docx"
    mirror_out = REPO_ROOT / "docs" / "thesis" / "BAO_CAO_DO_AN_KHMT1_HOAN_CHINH.docx"
    result = build(REPO_ROOT, output_path=default_out, mirror_output_path=mirror_out, try_wps_com=False)
    print(f"Built DOCX: {result} ({result.stat().st_size:,} bytes)")
    print(f"Mirror DOCX: {mirror_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
