"""Chuyển đổi và ghép toàn bộ báo cáo Markdown thành tệp Word (.docx) theo chuẩn báo cáo đồ án CTUT (KHMT 1)."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any

import docx
import pypandoc
from lxml import etree
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Cm, Mm, Pt, RGBColor

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
EQ_NUM_MARKER_PREFIX = "[[THESIS_EQ_NUM:"
LINEBREAK_MARKER = "XTHESISBRX"

ALERT_LABELS = {
    "NOTE": "Lưu ý:",
    "IMPORTANT": "Quan trọng:",
    "WARNING": "Cảnh báo:",
}

FRONT_TITLE_TEXTS: tuple[str, ...] = (
    "LỜI CẢM ƠN",
    "LỜI CAM ĐOAN",
    "TÓM TẮT",
    "ABSTRACT",
    "MỤC LỤC",
    "DANH MỤC KÝ HIỆU VÀ CHỮ VIẾT TẮT",
    "DANH MỤC BẢNG BIỂU",
    "DANH MỤC HÌNH ẢNH",
)

FONT_NAME = "Times New Roman"
PRINTABLE_WIDTH_TWIPS = 9072  # 16.0 cm (21.0 - 3.0 - 2.0 cm)
CENTER_TAB_TWIPS = 4536  # 8.0 cm
MAX_IMAGE_WIDTH_EMU = int(Cm(15.2))
MAX_IMAGE_HEIGHT_EMU = int(Cm(19.0))
LIST_LEFT_BASE_CM = 1.30
LIST_HANGING_CM = 0.45
LIST_DEPTH_STEP_CM = 0.45
LIST_LINE_SPACING = 1.3
LIST_SPACE_BEFORE_PT = 3.0
LIST_SPACE_AFTER_PT = 3.0


def preprocess_markdown(md_text: str, base_dir: Path | None = None) -> str:
    """Chuẩn hóa Markdown: bỏ '---', chuyển alert GitHub, tách số công thức khối, chèn dòng trống trước danh sách và chuẩn hóa đường dẫn ảnh."""
    lines = md_text.splitlines()
    out: list[str] = []
    in_code = False
    in_math = False
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

        if stripped == "$$":
            in_math = not in_math
            out.append(line)
            i += 1
            continue

        if in_math:
            out.append(line)
            i += 1
            continue

        # Bỏ dòng kẻ ngang Markdown ngoài khối mã
        if re.fullmatch(r"-{3,}", stripped):
            i += 1
            continue

        # Đảm bảo danh sách theo sau ngay đoạn văn dẫn không bị Pandoc gộp thành một đoạn liền
        if (
            re.match(r"^(?:[-*]|\d+\.)\s+", line)
            and out
            and out[-1].strip() != ""
            and not out[-1].lstrip().startswith(("#", "|", ">", "```", "$$", "[["))
            and not re.match(r"^\s*(?:[-*+]|\d+\.)\s+", out[-1])
        ):
            out.append("")

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

        # Tách số công thức (X.Y) khỏi công thức khối $$...$$ để căn giữa công thức và căn phải số
        if m_eq := re.match(r"^(\s*)\$\$(.+?)\s*(?:\\qquad|\\quad)\s*(\(\d+\.\d+\))\s*\$\$\s*$", line):
            indent, expr, eq_num = m_eq.group(1), m_eq.group(2).strip(), m_eq.group(3)
            out.append(f"{indent}$${expr}$$")
            out.append("")
            out.append(f"{indent}{EQ_NUM_MARKER_PREFIX}{eq_num}]]")
            i += 1
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

        # Bảo toàn thẻ xuống dòng <br/> trong bảng Markdown để chuyển thành <w:br/> ở bước hậu xử lý
        if stripped.startswith("|") and "<br" in line.lower():
            line = re.sub(r"<br\s*/?>", LINEBREAK_MARKER, line, flags=re.IGNORECASE)

        out.append(line)
        i += 1

    return "\n".join(out)


def split_appendix(ch6_md: str) -> tuple[str, str]:
    """Tách Chương 6 và phần Phụ lục (`# PHỤ LỤC`) từ tệp chuong-06-ket-luan-va-huong-phat-trien.md."""
    lines = ch6_md.splitlines()
    split_idx: int | None = None
    for idx, line in enumerate(lines):
        if re.match(r"^#\s+PHỤ LỤC\b", line.strip()):
            split_idx = idx
            break
    if split_idx is None:
        raise ValueError("Không tìm thấy tiêu đề '# PHỤ LỤC' trong Chương 6.")

    ch6_body = "\n".join(lines[:split_idx]).rstrip()
    ch6_body = re.sub(r"\n-{3,}\s*$", "", ch6_body).rstrip()
    appendix_md = "\n".join(lines[split_idx:]).strip()
    return ch6_body, appendix_md


def _extract_h2_sections(md_text: str) -> dict[str, str]:
    """Tách nội dung theo các đề mục cấp 2 (`## N. ...`)."""
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


def _extract_cover_quote_blocks(sec3_md: str, heading_prefix: str) -> list[list[str]]:
    """Trích các khối quote `>` dưới tiểu mục `### 3.1.` hoặc `### 3.2.` của trang bìa."""
    in_sub = False
    blocks: list[list[str]] = []
    cur: list[str] = []
    for raw in sec3_md.splitlines():
        s = raw.strip()
        if s.startswith("### "):
            if in_sub:
                break
            in_sub = s.startswith(heading_prefix)
            continue
        if not in_sub:
            continue
        if s.startswith(">"):
            cur.append(s.lstrip(">").strip())
        elif cur:
            blocks.append(cur)
            cur = []
    if cur:
        blocks.append(cur)
    return blocks


def split_front_matter(front_matter_md: str) -> dict[str, Any]:
    """Tách dữ liệu Trang bìa chính/phụ và phần mở đầu hợp lệ từ muc-luc-va-ho-so-ban-giao.md."""
    sections = _extract_h2_sections(front_matter_md)

    sec3 = sections.get("3", "")
    cover_main_blocks = _extract_cover_quote_blocks(sec3, "### 3.1.")
    cover_sub_blocks = _extract_cover_quote_blocks(sec3, "### 3.2.")
    if not cover_main_blocks or not cover_sub_blocks:
        raise ValueError("Không tìm thấy đầy đủ khối trang bìa chính (3.1) và bìa phụ (3.2) trong Mục 3.")
    cover_lines = [ln for blk in cover_main_blocks for ln in blk if ln.strip()]

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

    # Chuẩn hóa tiêu đề con của Mục 8 sang 1. Chữ viết tắt và 2. Ký hiệu toán học
    sec8_raw = sections.get("8", "")
    sec8_clean = re.sub(r"^###\s+8\.1\.\s+", "### 1. ", sec8_raw, flags=re.M)
    sec8_clean = re.sub(r"^###\s+8\.2\.\s+", "### 2. ", sec8_clean, flags=re.M)

    tables_list: list[tuple[str, str]] = []
    for line in sections.get("9", "").splitlines():
        s = line.strip()
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if len(cells) >= 2 and (m := re.match(r"^(Bảng\s+[A-D0-9]+\.\d+)\s*[-–:]?$", cells[0])):
                tables_list.append((m.group(1), cells[1]))

    figures_list: list[tuple[str, str]] = []
    for line in sections.get("10", "").splitlines():
        s = line.strip()
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if len(cells) >= 2 and (m := re.match(r"^(Hình\s+[A-D0-9]+\.\d+)\s*[-–:]?$", cells[0])):
                figures_list.append((m.group(1), cells[1]))

    return {
        "cover_main_blocks": cover_main_blocks,
        "cover_sub_blocks": cover_sub_blocks,
        "cover_lines": cover_lines,
        "loi_cam_on": preprocess_markdown(sections.get("4", "")),
        "loi_cam_doan": preprocess_markdown(sections.get("5", "")),
        "tom_tat_vi": preprocess_markdown(tom_tat_vi),
        "abstract_en": preprocess_markdown(abstract_en),
        "ky_hieu_viet_tat": preprocess_markdown(sec8_clean),
        "tables_list": tables_list,
        "figures_list": figures_list,
    }


def _strip_theme_fonts_and_set(
    rpr_parent: Any,
    font_name: str = FONT_NAME,
    size_pt: float | None = None,
) -> None:
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


def _ensure_paragraph_style(
    doc: docx.document.Document,
    name: str,
    *,
    base_style_name: str | None = "Normal",
    size_pt: float,
    bold: bool = False,
    italic: bool = False,
    all_caps: bool = False,
    align: Any = WD_ALIGN_PARAGRAPH.LEFT,
    line_spacing: float = 1.25,
    space_before_pt: float = 4.0,
    space_after_pt: float = 4.0,
    first_indent_cm: float = 0.0,
    left_indent_cm: float = 0.0,
    keep_with_next: bool = False,
    page_break_before: bool = False,
    shading_fill: str | None = None,
) -> Any:
    """Khởi tạo hoặc cập nhật đầy đủ thuộc tính của một paragraph style."""
    if name in doc.styles:
        st = doc.styles[name]
    else:
        st = doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        if base_style_name and base_style_name in doc.styles:
            st.base_style = doc.styles[base_style_name]

    st.font.name = FONT_NAME
    st.font.size = Pt(size_pt)
    st.font.bold = bold
    st.font.italic = italic
    st.font.all_caps = all_caps
    st.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    _strip_theme_fonts_and_set(st._element, FONT_NAME, size_pt=size_pt)

    pf = st.paragraph_format
    pf.alignment = align
    pf.line_spacing = line_spacing
    pf.space_before = Pt(space_before_pt)
    pf.space_after = Pt(space_after_pt)
    pf.first_line_indent = Cm(first_indent_cm)
    pf.left_indent = Cm(left_indent_cm)
    pf.keep_with_next = keep_with_next
    pf.page_break_before = page_break_before

    if shading_fill:
        ppr = st._element.get_or_add_pPr()
        for old_shd in ppr.findall(qn("w:shd")):
            ppr.remove(old_shd)
        ppr.append(
            parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="{shading_fill}"/>')
        )
    return st


def _apply_standard_styles(doc: docx.document.Document) -> None:
    """Thiết lập đồng bộ toàn bộ hệ thống style chuẩn báo cáo đồ án CTUT (KHMT 1) trên Document."""
    styles_el = doc.styles.element
    for rpr_def in styles_el.xpath(".//w:docDefaults/w:rPrDefault"):
        _strip_theme_fonts_and_set(rpr_def, FONT_NAME, size_pt=13)

    _ensure_paragraph_style(
        doc,
        "Normal",
        base_style_name=None,
        size_pt=13.0,
        align=WD_ALIGN_PARAGRAPH.JUSTIFY,
        line_spacing=1.3,
        space_before_pt=4.0,
        space_after_pt=4.0,
        first_indent_cm=1.0,
    )
    for prose_name in ("Body Text", "First Paragraph"):
        if prose_name in doc.styles:
            _ensure_paragraph_style(
                doc,
                prose_name,
                base_style_name="Normal",
                size_pt=13.0,
                align=WD_ALIGN_PARAGRAPH.JUSTIFY,
                line_spacing=1.3,
                space_before_pt=4.0,
                space_after_pt=4.0,
                first_indent_cm=1.0,
            )

    if "Compact" in doc.styles:
        _ensure_paragraph_style(
            doc,
            "Compact",
            base_style_name="Normal",
            size_pt=13.0,
            align=WD_ALIGN_PARAGRAPH.JUSTIFY,
            line_spacing=LIST_LINE_SPACING,
            space_before_pt=LIST_SPACE_BEFORE_PT,
            space_after_pt=LIST_SPACE_AFTER_PT,
            first_indent_cm=0.0,
        )
    if "Block Text" in doc.styles:
        _ensure_paragraph_style(
            doc,
            "Block Text",
            base_style_name="Normal",
            size_pt=13.0,
            align=WD_ALIGN_PARAGRAPH.JUSTIFY,
            line_spacing=1.25,
            space_before_pt=3.0,
            space_after_pt=4.0,
            first_indent_cm=0.0,
        )

    _ensure_paragraph_style(
        doc,
        "Heading 1",
        base_style_name="Normal",
        size_pt=15.0,
        bold=True,
        all_caps=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        line_spacing=1.2,
        space_before_pt=12.0,
        space_after_pt=8.0,
        first_indent_cm=0.0,
        keep_with_next=True,
        page_break_before=True,
    )
    _ensure_paragraph_style(
        doc,
        "Heading 2",
        base_style_name="Normal",
        size_pt=13.5,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.LEFT,
        line_spacing=1.25,
        space_before_pt=10.0,
        space_after_pt=4.0,
        first_indent_cm=0.0,
        keep_with_next=True,
    )
    _ensure_paragraph_style(
        doc,
        "Heading 3",
        base_style_name="Normal",
        size_pt=13.0,
        bold=True,
        italic=True,
        align=WD_ALIGN_PARAGRAPH.LEFT,
        line_spacing=1.25,
        space_before_pt=6.0,
        space_after_pt=4.0,
        first_indent_cm=0.0,
        keep_with_next=True,
    )
    if "Heading 4" in doc.styles:
        _ensure_paragraph_style(
            doc,
            "Heading 4",
            base_style_name="Normal",
            size_pt=13.0,
            italic=True,
            align=WD_ALIGN_PARAGRAPH.LEFT,
            line_spacing=1.25,
            space_before_pt=6.0,
            space_after_pt=2.0,
            first_indent_cm=0.0,
            keep_with_next=True,
        )

    _ensure_paragraph_style(
        doc,
        "Front Title",
        base_style_name="Normal",
        size_pt=15.0,
        bold=True,
        all_caps=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        line_spacing=1.2,
        space_before_pt=12.0,
        space_after_pt=8.0,
        first_indent_cm=0.0,
        keep_with_next=True,
        page_break_before=True,
    )
    _ensure_paragraph_style(
        doc,
        "Front Heading 2",
        base_style_name="Normal",
        size_pt=13.5,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.LEFT,
        line_spacing=1.25,
        space_before_pt=10.0,
        space_after_pt=4.0,
        first_indent_cm=0.0,
        keep_with_next=True,
    )
    _ensure_paragraph_style(
        doc,
        "Caption Table",
        base_style_name="Normal",
        size_pt=11.0,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.LEFT,
        line_spacing=1.15,
        space_before_pt=6.0,
        space_after_pt=4.0,
        first_indent_cm=0.0,
        keep_with_next=True,
    )
    _ensure_paragraph_style(
        doc,
        "Caption Figure",
        base_style_name="Normal",
        size_pt=11.0,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        line_spacing=1.15,
        space_before_pt=6.0,
        space_after_pt=4.0,
        first_indent_cm=0.0,
        keep_with_next=False,
    )

    for cap_legacy in ("Caption", "Image Caption"):
        if cap_legacy in doc.styles:
            _ensure_paragraph_style(
                doc,
                cap_legacy,
                base_style_name="Normal",
                size_pt=11.0,
                bold=True,
                align=WD_ALIGN_PARAGRAPH.CENTER,
                line_spacing=1.15,
                space_before_pt=4.0,
                space_after_pt=4.0,
                first_indent_cm=0.0,
            )

    _ensure_paragraph_style(
        doc,
        "Source Code",
        base_style_name="Normal",
        size_pt=10.0,
        align=WD_ALIGN_PARAGRAPH.LEFT,
        line_spacing=1.15,
        space_before_pt=1.0,
        space_after_pt=1.0,
        first_indent_cm=0.0,
        left_indent_cm=0.35,
        shading_fill="F5F5F5",
    )

    for st in doc.styles:
        if st.type == WD_STYLE_TYPE.CHARACTER:
            st.font.name = FONT_NAME
            if st.font.color and st.font.color.rgb not in (None, RGBColor(0x00, 0x00, 0x00)):
                st.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
            _strip_theme_fonts_and_set(st._element, FONT_NAME)

    for lvl in (1, 2, 3):
        toc_name = next(
            (s.name for s in doc.styles if s.name.lower() == f"toc {lvl}"),
            f"toc {lvl}",
        )
        _ensure_paragraph_style(
            doc,
            toc_name,
            base_style_name="Normal",
            size_pt=12.0 if lvl == 1 else (11.5 if lvl == 2 else 11.0),
            bold=(lvl == 1),
            align=WD_ALIGN_PARAGRAPH.LEFT,
            line_spacing=1.15,
            space_before_pt=2.0 if lvl == 1 else 1.0,
            space_after_pt=2.0 if lvl == 1 else 1.0,
            first_indent_cm=0.0,
            left_indent_cm=0.0 if lvl == 1 else (0.5 * (lvl - 1)),
        )


def create_reference_docx(out_path: Path) -> Path:
    """Tạo tệp reference.docx chuẩn A4 (lề 2/2/3/2 cm, Times New Roman) từ mẫu Pandoc."""
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
    sec.top_margin = Cm(2.0)
    sec.bottom_margin = Cm(2.0)
    sec.left_margin = Cm(3.0)
    sec.right_margin = Cm(2.0)
    sec.header_distance = Cm(1.25)
    sec.footer_distance = Cm(1.25)

    _apply_standard_styles(doc)
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
    """Chèn trường động Word (PAGE, PAGEREF) vào một đoạn."""

    def _mk_run(text: str | None = None) -> Any:
        r = paragraph.add_run(text or "")
        r.font.name = FONT_NAME
        r.font.size = Pt(font_size)
        r.font.bold = bold
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        _strip_theme_fonts_and_set(r._element, FONT_NAME, size_pt=font_size)
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


def _install_cover_border_behind_text(section: docx.section.Section, border_png: Path) -> None:
    """Chèn ảnh khung viền A4 toàn trang vào header của section bìa ở lớp Behind Text."""
    if section.header._element.findall(f".//{qn('wp:anchor')}"):
        return
    hp = section.header.paragraphs[0]
    hp.paragraph_format.first_line_indent = Cm(0)
    hp.paragraph_format.space_before = Pt(0)
    hp.paragraph_format.space_after = Pt(0)
    run = hp.add_run()
    shape = run.add_picture(str(border_png), width=Cm(21.0), height=Cm(29.7))
    inline = shape._inline
    extent = inline.find(qn("wp:extent"))
    doc_pr = inline.find(qn("wp:docPr"))
    graphic = inline.find(qn("a:graphic"))
    cx = extent.get("cx") if extent is not None else str(int(Cm(21.0)))
    cy = extent.get("cy") if extent is not None else str(int(Cm(29.7)))
    doc_id = doc_pr.get("id") if doc_pr is not None else "1"
    doc_name = doc_pr.get("name") if doc_pr is not None else "CoverBorder"

    anchor_xml = (
        f'<wp:anchor {nsdecls("wp", "a", "r")} '
        'distT="0" distB="0" distL="0" distR="0" simplePos="0" '
        'relativeHeight="0" behindDoc="1" locked="0" layoutInCell="1" allowOverlap="1">'
        '<wp:simplePos x="0" y="0"/>'
        '<wp:positionH relativeFrom="page"><wp:posOffset>0</wp:posOffset></wp:positionH>'
        '<wp:positionV relativeFrom="page"><wp:posOffset>0</wp:posOffset></wp:positionV>'
        f'<wp:extent cx="{cx}" cy="{cy}"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        '<wp:wrapNone/>'
        f'<wp:docPr id="{doc_id}" name="{doc_name}"/>'
        '<wp:cNvGraphicFramePr/>'
        "</wp:anchor>"
    )
    anchor = parse_xml(anchor_xml)
    if graphic is not None:
        anchor.append(graphic)
    parent = inline.getparent()
    parent.replace(inline, anchor)


def _configure_section_page_layout(
    sec: docx.section.Section,
    *,
    page_num_fmt: str | None,
    start_num: int | None = None,
    border_png: Path | None = None,
) -> None:
    """Cấu hình khổ A4 (2/2/3/2 cm), số trang chân trang và khung viền trang bìa."""
    sec.page_width = Mm(210)
    sec.page_height = Mm(297)
    sec.top_margin = Cm(2.0)
    sec.bottom_margin = Cm(2.0)
    sec.left_margin = Cm(3.0)
    sec.right_margin = Cm(2.0)
    sec.header_distance = Cm(1.25)
    sec.footer_distance = Cm(1.25)

    sect_pr = sec._sectPr
    for old in sect_pr.findall(qn("w:pgNumType")):
        sect_pr.remove(old)
    for old in sect_pr.findall(qn("w:pgBorders")):
        sect_pr.remove(old)

    if page_num_fmt is not None:
        pg_num = OxmlElement("w:pgNumType")
        pg_num.set(qn("w:fmt"), page_num_fmt)
        if start_num is not None:
            pg_num.set(qn("w:start"), str(start_num))
        sect_pr.append(pg_num)

    sec.header.is_linked_to_previous = False
    sec.footer.is_linked_to_previous = False
    for p in list(sec.header.paragraphs):
        p.clear()
    footer_p = sec.footer.paragraphs[0]
    footer_p.text = ""
    footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer_p.paragraph_format.first_line_indent = Cm(0)
    footer_p.paragraph_format.space_before = Pt(0)
    footer_p.paragraph_format.space_after = Pt(0)
    if page_num_fmt is not None:
        _add_field_to_paragraph(footer_p, "PAGE", "", font_size=11.0)

    if border_png is not None and border_png.exists():
        _install_cover_border_behind_text(sec, border_png)


def _add_cover_line(
    anchor_p: docx.text.paragraph.Paragraph,
    raw_line: str,
    *,
    size_pt: float = 13.0,
    space_before: float = 0.0,
    space_after: float = 4.0,
) -> docx.text.paragraph.Paragraph:
    """Chèn một dòng căn giữa cân đối trên trang bìa ngay trước anchor_p."""
    p = anchor_p.insert_paragraph_before("")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.first_line_indent = Cm(0)
    # Bù lệch lề trái 3,0 cm / phải 2,0 cm (trục giữa x = 10,5 cm, vùng chữ rộng 15,8 cm trong khung bìa)
    pf.left_indent = Cm(-0.4)
    pf.right_indent = Cm(0.6)
    pf.line_spacing = 1.25
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)

    if not raw_line:
        return p

    for part in re.split(r"(\*\*[^*]+\*\*)", raw_line):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            r = p.add_run(part[2:-2])
            r.bold = True
        else:
            r = p.add_run(part)
        r.font.name = FONT_NAME
        r.font.size = Pt(size_pt)
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        _strip_theme_fonts_and_set(r._element, FONT_NAME, size_pt=size_pt)
    return p


def _add_cover_student_table_before(
    doc: docx.document.Document,
    anchor_p: docx.text.paragraph.Paragraph,
    students: list[tuple[str, str]],
) -> None:
    """Chèn bảng 2 cột không viền cho danh sách sinh viên thực hiện, cân giữa khung bìa."""
    table = doc.add_table(rows=len(students), cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    table.autofit = False

    # Đánh dấu thuộc tính riêng và di chuyển bảng vào trước anchor_p
    col_widths_dxa = (3742, 1984)  # 6,6 cm + 3,5 cm = 10,1 cm (5726 dxa)
    total_w_dxa = sum(col_widths_dxa)
    tbl_pr = table._tbl.tblPr
    for tag, attrs in (
        ("w:tblW", {"w:w": str(total_w_dxa), "w:type": "dxa"}),
        ("w:tblInd", {"w:w": "1389", "w:type": "dxa"}),
        ("w:tblLayout", {"w:type": "fixed"}),
    ):
        old = tbl_pr.find(qn(tag))
        if old is not None:
            tbl_pr.remove(old)
        el = OxmlElement(tag)
        for k, v in attrs.items():
            el.set(qn(k), v)
        tbl_pr.append(el)

    tbl_borders = tbl_pr.find(qn("w:tblBorders"))
    if tbl_borders is None:
        tbl_borders = OxmlElement("w:tblBorders")
        tbl_pr.append(tbl_borders)
    for edge in ("top", "bottom", "left", "right", "insideH", "insideV"):
        old = tbl_borders.find(qn(f"w:{edge}"))
        if old is not None:
            tbl_borders.remove(old)
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "none")
        tbl_borders.append(el)

    tbl_cell_mar = tbl_pr.find(qn("w:tblCellMar"))
    if tbl_cell_mar is None:
        tbl_cell_mar = OxmlElement("w:tblCellMar")
        tbl_pr.append(tbl_cell_mar)
    for side, w in (("top", "20"), ("bottom", "20"), ("left", "40"), ("right", "40")):
        old = tbl_cell_mar.find(qn(f"w:{side}"))
        if old is not None:
            tbl_cell_mar.remove(old)
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:w"), w)
        el.set(qn("w:type"), "dxa")
        tbl_cell_mar.append(el)

    col_specs = (
        (Cm(6.6), col_widths_dxa[0], WD_ALIGN_PARAGRAPH.LEFT),
        (Cm(3.5), col_widths_dxa[1], WD_ALIGN_PARAGRAPH.RIGHT),
    )
    tbl_grid = table._tbl.find(qn("w:tblGrid"))
    if tbl_grid is not None:
        for gc, w_dxa in zip(tbl_grid.findall(qn("w:gridCol")), col_widths_dxa):
            gc.set(qn("w:w"), str(w_dxa))
    for col, (col_cm, _, _) in zip(table.columns, col_specs):
        col.width = col_cm

    for row, (name, code) in zip(table.rows, students):
        row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        for cell, val, (width_cm, width_dxa, align) in zip(row.cells, (name, code), col_specs):
            cell.width = width_cm
            tc_pr = cell._tc.get_or_add_tcPr()
            for old_tc_w in tc_pr.findall(qn("w:tcW")):
                tc_pr.remove(old_tc_w)
            tc_w = OxmlElement("w:tcW")
            tc_w.set(qn("w:w"), str(width_dxa))
            tc_w.set(qn("w:type"), "dxa")
            tc_pr.insert(0, tc_w)
            p = cell.paragraphs[0]
            p.alignment = align
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.space_before = Pt(1.0)
            p.paragraph_format.space_after = Pt(1.0)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(val)
            r.font.name = FONT_NAME
            r.font.size = Pt(13.0)
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
            _strip_theme_fonts_and_set(r._element, FONT_NAME, size_pt=13.0)

    parent = anchor_p._p.getparent()
    parent.remove(table._tbl)
    idx_in_parent = list(parent).index(anchor_p._p)
    parent.insert(idx_in_parent, table._tbl)


def _split_student_rows(lines: list[str], start_idx: int) -> tuple[list[tuple[str, str]], int]:
    """Đọc các dòng `Họ tên - MSSV` (hoặc `—`) liên tiếp bắt đầu tại start_idx."""
    pat = re.compile(r"^(.*?)\s+[—-]\s+([A-Z0-9]+)\s*$")
    rows: list[tuple[str, str]] = []
    pos = start_idx
    while pos < len(lines):
        m = pat.match(lines[pos].strip())
        if not m:
            break
        rows.append((m.group(1).strip(), m.group(2).strip()))
        pos += 1
    return rows, pos


def _insert_cover_pages_before_first_paragraph(
    doc: docx.document.Document,
    anchor_p: docx.text.paragraph.Paragraph,
    main_blocks: list[list[str]],
    sub_blocks: list[list[str]],
    logo_png: Path,
) -> None:
    """Dựng Trang bìa chính + ngắt trang + Trang bìa phụ + ngắt section sang Phần mở đầu."""
    # 1. Trang bìa chính: [0] Trường/Khoa -> Logo -> [1] Loại báo cáo -> [2] Đề tài -> [3] GVHD & SV -> [4] Ngày tháng
    for idx, blk in enumerate(main_blocks):
        if idx == 0:
            for j, line in enumerate(blk):
                _add_cover_line(
                    anchor_p,
                    line,
                    size_pt=14.0,
                    space_before=66.0 if j == 0 else 0.0,
                    space_after=12.0 if j == len(blk) - 1 else 4.0,
                )
            p_logo = anchor_p.insert_paragraph_before("")
            p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_logo.paragraph_format.first_line_indent = Cm(0)
            p_logo.paragraph_format.left_indent = Cm(-0.4)
            p_logo.paragraph_format.right_indent = Cm(0.6)
            p_logo.paragraph_format.space_before = Pt(12)
            p_logo.paragraph_format.space_after = Pt(12)
            if logo_png.exists():
                p_logo.add_run().add_picture(str(logo_png), width=Cm(3.0))
        elif idx == 1:
            for j, line in enumerate(blk):
                _add_cover_line(
                    anchor_p,
                    line,
                    size_pt=15.0,
                    space_after=18.0 if j == len(blk) - 1 else 4.0,
                )
        elif idx == 2:
            for j, line in enumerate(blk):
                sz = 14.0 if j == 0 else 15.5
                _add_cover_line(
                    anchor_p,
                    line,
                    size_pt=sz,
                    space_after=20.0 if j == len(blk) - 1 else 6.0,
                )
        elif idx == 3:
            j = 0
            while j < len(blk):
                line = blk[j]
                s_strip = line.strip()
                if s_strip == "**Sinh viên thực hiện:**":
                    _add_cover_line(anchor_p, line, size_pt=13.0, space_after=4.0)
                    students, next_j = _split_student_rows(blk, j + 1)
                    if students:
                        _add_cover_student_table_before(doc, anchor_p, students)
                        j = next_j
                        continue
                if s_strip.startswith("**GVHD:"):
                    _add_cover_line(anchor_p, line, size_pt=13.0, space_after=10.0)
                elif s_strip.startswith(("**LỚP:", "**Lớp:")):
                    _add_cover_line(anchor_p, line, size_pt=13.0, space_before=10.0, space_after=36.0)
                elif s_strip:
                    _add_cover_line(anchor_p, line, size_pt=13.0, space_after=3.0)
                j += 1
        else:
            for j, line in enumerate(blk):
                p_last_main = _add_cover_line(anchor_p, line, size_pt=13.0, space_after=0.0)
                if j == len(blk) - 1:
                    p_last_main.add_run().add_break(WD_BREAK.PAGE)

    # 2. Trang bìa phụ (dùng dòng đệm line_spacing=64pt tránh Word/WPS bỏ space_before sau ngắt trang)
    p_top = anchor_p.insert_paragraph_before("")
    p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_top.paragraph_format.first_line_indent = Cm(0)
    p_top.paragraph_format.left_indent = Cm(-0.4)
    p_top.paragraph_format.right_indent = Cm(0.6)
    p_top.paragraph_format.space_before = Pt(0)
    p_top.paragraph_format.space_after = Pt(0)
    p_top.paragraph_format.line_spacing = Pt(64)
    r_top = p_top.add_run("\u00a0")
    r_top.font.name = FONT_NAME
    r_top.font.size = Pt(1.0)
    _strip_theme_fonts_and_set(r_top._element, FONT_NAME, size_pt=1.0)

    last_sub_p: docx.text.paragraph.Paragraph = p_top
    for blk in sub_blocks:
        lines = [ln for ln in blk]
        j = 0
        while j < len(lines):
            s_strip = lines[j].strip()
            if not s_strip:
                j += 1
                continue
            if s_strip == "**Sinh viên thực hiện:**":
                _add_cover_line(anchor_p, lines[j], size_pt=13.0, space_after=4.0)
                students, next_j = _split_student_rows(lines, j + 1)
                if students:
                    _add_cover_student_table_before(doc, anchor_p, students)
                    j = next_j
                    continue
            if j == 0:
                last_sub_p = _add_cover_line(anchor_p, lines[j], size_pt=14.0, space_after=10.0)
            elif j in (1, 2) and "**Môn:" not in s_strip:
                last_sub_p = _add_cover_line(
                    anchor_p,
                    lines[j],
                    size_pt=15.5,
                    space_after=16.0 if j == 2 else 4.0,
                )
            elif s_strip.startswith("Cần Thơ"):
                last_sub_p = _add_cover_line(
                    anchor_p,
                    lines[j],
                    size_pt=13.0,
                    space_before=110.0,
                    space_after=0.0,
                )
            elif s_strip.startswith("**GVHD:"):
                last_sub_p = _add_cover_line(anchor_p, lines[j], size_pt=13.0, space_after=10.0)
            else:
                last_sub_p = _add_cover_line(anchor_p, lines[j], size_pt=13.0, space_after=4.0)
            j += 1

    # Chèn ngắt Section (nextPage) sau Trang bìa phụ sang Phần mở đầu (Section 1)
    ppr = last_sub_p._p.get_or_add_pPr()
    sect_pr = parse_xml(f'<w:sectPr {nsdecls("w")}><w:type w:val="nextPage"/></w:sectPr>')
    ppr.append(sect_pr)


def _attach_bookmark(p: docx.text.paragraph.Paragraph, bm_id: int, bm_name: str) -> None:
    """Gắn cặp <w:bookmarkStart>/<w:bookmarkEnd> bao quanh nội dung của đoạn."""
    b_start = OxmlElement("w:bookmarkStart")
    b_start.set(qn("w:id"), str(bm_id))
    b_start.set(qn("w:name"), bm_name)
    b_end = OxmlElement("w:bookmarkEnd")
    b_end.set(qn("w:id"), str(bm_id))
    insert_pos = 1 if p._p.pPr is not None else 0
    p._p.insert(insert_pos, b_start)
    p._p.append(b_end)


def _slug_bookmark(caption_label: str) -> str:
    """Chuyển 'Bảng 1.1' / 'Hình 3.2' / 'Bảng A.1' thành tên bookmark Word hợp lệ."""
    clean = caption_label.lower().replace("ả", "a").replace("ì", "i").replace(".", "_")
    clean = re.sub(r"[^a-z0-9_]+", "_", clean).strip("_")
    return f"bm_{clean}"[:39]


def _bookmark_headings_and_captions(
    doc: docx.document.Document,
) -> tuple[list[tuple[int, str, str]], dict[str, str]]:
    """Gắn bookmark cho toàn bộ Front Title, Heading 1–3, Caption Table và Caption Figure."""
    existing_ids = [
        int(el.get(qn("w:id"), "0"))
        for el in doc.element.body.xpath(".//w:bookmarkStart")
        if (el.get(qn("w:id")) or "").isdigit()
    ]
    next_id = (max(existing_ids) + 1) if existing_ids else 100
    toc_counter = 1

    toc_entries: list[tuple[int, str, str]] = []
    label_to_bm: dict[str, str] = {}
    in_main = False

    for p in doc.paragraphs:
        txt = re.sub(r"\s+", " ", p.text.strip())
        if not txt:
            continue
        sname = p.style.name if p.style else ""

        if txt.startswith("CHƯƠNG 1"):
            in_main = True

        if sname == "Front Title":
            bm_name = f"_Toc{toc_counter:05d}"
            toc_counter += 1
            _attach_bookmark(p, next_id, bm_name)
            next_id += 1
            toc_entries.append((1, txt, bm_name))
            continue

        if sname in ("Heading 1", "Heading 2", "Heading 3"):
            level = int(sname.split()[-1])
            bm_name = f"_Toc{toc_counter:05d}"
            toc_counter += 1
            _attach_bookmark(p, next_id, bm_name)
            next_id += 1
            toc_entries.append((level, txt, bm_name))
            continue

        if in_main and (m := re.match(r"^((?:Bảng|Hình)\s+[A-D0-9]+\.\d+)\s*[-–:]", txt)):
            label = re.sub(r"\s+", " ", m.group(1).strip())
            if label not in label_to_bm:
                bm_name = _slug_bookmark(label)
                _attach_bookmark(p, next_id, bm_name)
                next_id += 1
                label_to_bm[label] = bm_name

    return toc_entries, label_to_bm


def _emit_dotted_toc_field(
    doc: docx.document.Document,
    anchor_p: docx.text.paragraph.Paragraph,
    instruction: str,
    entries: list[tuple[int, str, str]],
) -> None:
    """Chèn trường Word `TOC` đa đoạn với dòng chấm dẫn và `PAGEREF` bên trong kết quả."""
    if not entries:
        p = anchor_p.insert_paragraph_before("")
        p.paragraph_format.first_line_indent = Cm(0)
        _add_field_to_paragraph(p, instruction, default_text="", font_size=12.0)
        return

    for idx, (level, title, bm_name) in enumerate(entries):
        is_first = idx == 0
        is_last = idx == len(entries) - 1
        lvl = min(max(level, 1), 3)
        toc_style = next(
            (s.name for s in doc.styles if s.name.lower() == f"toc {lvl}"),
            None,
        )
        p = anchor_p.insert_paragraph_before("", style=doc.styles[toc_style] if toc_style else None)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf = p.paragraph_format
        pf.first_line_indent = Cm(0)
        pf.left_indent = Cm(0.0 if level == 1 else (0.55 if level == 2 else 1.1))
        pf.right_indent = Cm(1.3)
        pf.space_before = Pt(2.0 if level == 1 else 1.0)
        pf.space_after = Pt(2.0 if level == 1 else 1.0)
        pf.line_spacing = 1.15

        pPr = p._p.get_or_add_pPr()
        for old_tabs in pPr.findall(qn("w:tabs")):
            pPr.remove(old_tabs)
        tabs = OxmlElement("w:tabs")
        tab = OxmlElement("w:tab")
        tab.set(qn("w:val"), "right")
        tab.set(qn("w:leader"), "dot")
        tab.set(qn("w:pos"), str(PRINTABLE_WIDTH_TWIPS))
        tabs.append(tab)
        pPr.append(tabs)

        is_caption_list = title.startswith(("Bảng ", "Hình "))
        font_pt = 11.0 if is_caption_list else (11.5 if level > 1 else 12.0)
        is_bold = level == 1 and not is_caption_list

        def _mk_fld_run(fld_type: str) -> None:
            r = p.add_run()
            r.font.name = FONT_NAME
            r.font.size = Pt(font_pt)
            _strip_theme_fonts_and_set(r._element, FONT_NAME, size_pt=font_pt)
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), fld_type)
            r._r.append(el)

        if is_first:
            _mk_fld_run("begin")
            r_instr = p.add_run()
            r_instr.font.name = FONT_NAME
            r_instr.font.size = Pt(font_pt)
            _strip_theme_fonts_and_set(r_instr._element, FONT_NAME, size_pt=font_pt)
            instr_el = OxmlElement("w:instrText")
            instr_el.set(qn("xml:space"), "preserve")
            instr_el.text = f" {instruction} "
            r_instr._r.append(instr_el)
            _mk_fld_run("separate")

        # Chèn hyperlink tới bookmark để Word/WPS nhảy trang khi nhấn Ctrl+Click
        hlink = OxmlElement("w:hyperlink")
        hlink.set(qn("w:anchor"), bm_name)

        def _append_hlink_run(text: str | None = None, *, is_tab: bool = False) -> OxmlElement:
            r = OxmlElement("w:r")
            rPr = OxmlElement("w:rPr")
            rf = OxmlElement("w:rFonts")
            for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
                rf.set(qn(attr), FONT_NAME)
            rPr.append(rf)
            sz_val = str(int(round(font_pt * 2)))
            for sz_tag in ("w:sz", "w:szCs"):
                sz_el = OxmlElement(sz_tag)
                sz_el.set(qn("w:val"), sz_val)
                rPr.append(sz_el)
            col = OxmlElement("w:color")
            col.set(qn("w:val"), "000000")
            rPr.append(col)
            b_el = OxmlElement("w:b")
            b_cs_el = OxmlElement("w:bCs")
            if not is_bold:
                b_el.set(qn("w:val"), "0")
                b_cs_el.set(qn("w:val"), "0")
            rPr.append(b_el)
            rPr.append(b_cs_el)
            r.append(rPr)
            if is_tab:
                r.append(OxmlElement("w:tab"))
            elif text is not None:
                t = OxmlElement("w:t")
                t.set(qn("xml:space"), "preserve")
                t.text = text
                r.append(t)
            hlink.append(r)
            return r

        _append_hlink_run(title)
        _append_hlink_run(is_tab=True)

        for child in ("begin", "instr", "separate", "placeholder", "end"):
            r_pg = _append_hlink_run(None)
            if child in ("begin", "separate", "end"):
                fc = OxmlElement("w:fldChar")
                fc.set(qn("w:fldCharType"), child)
                r_pg.append(fc)
            elif child == "instr":
                it = OxmlElement("w:instrText")
                it.set(qn("xml:space"), "preserve")
                it.text = f" PAGEREF {bm_name} \\h "
                r_pg.append(it)
            else:
                tp = OxmlElement("w:t")
                tp.text = "-"
                r_pg.append(tp)

        p._p.append(hlink)
        if is_last:
            _mk_fld_run("end")


def _clean_inline_caption_title(raw_title: str) -> str:
    """Làm sạch công thức nhỏ trong tiêu đề danh mục bảng/hình."""
    return (
        raw_title.replace("$\\delta$", "δ")
        .replace("$E_{\\max}$", "E_max")
        .replace("$\\sum w_i = 0$", "∑w_i = 0")
        .replace("`", "")
    )


def _style_front_matter_headings(doc: docx.document.Document) -> None:
    """Chuyển tiêu đề Phần mở đầu sang `Front Title` và tiểu mục Ký hiệu sang `Front Heading 2`."""
    for p in doc.paragraphs:
        txt = p.text.strip()
        sname = p.style.name if p.style else ""
        if sname == "Heading 1" and txt.upper() in FRONT_TITLE_TEXTS:
            p.style = doc.styles["Front Title"]
            p.paragraph_format.page_break_before = txt.upper() != "LỜI CẢM ƠN"
        elif txt == SENTINEL_TOC_SLOT:
            pass
        elif sname == "Heading 3" and txt in ("1. Chữ viết tắt", "2. Ký hiệu toán học"):
            p.style = doc.styles["Front Heading 2"]


def _populate_toc_and_lists(doc: docx.document.Document, fm_parts: dict[str, Any]) -> None:
    """Chèn mục lục chấm dẫn, danh mục bảng biểu và danh mục hình ảnh tại các vị trí sentinel."""
    # Trước tiên tạo đoạn tiêu đề Front Title "MỤC LỤC" ngay tại SENTINEL_TOC_SLOT để đưa vào chính Mục lục nếu cần hoặc xuất trước TOC
    toc_sentinel = next((p for p in doc.paragraphs if p.text.strip() == SENTINEL_TOC_SLOT), None)
    if toc_sentinel is not None:
        title_p = toc_sentinel.insert_paragraph_before("MỤC LỤC", style=doc.styles["Front Title"])
        title_p.paragraph_format.page_break_before = True
        for r in title_p.runs:
            r.font.name = FONT_NAME
            _strip_theme_fonts_and_set(r._element, FONT_NAME, size_pt=15.0)

    toc_entries, label_to_bm = _bookmark_headings_and_captions(doc)

    # Xây dựng danh mục bảng và hình dạng dòng chấm dẫn: "Bảng 1.1: Tên bảng\t<PAGEREF>"
    lot_entries = [
        (1, f"{label}: {_clean_inline_caption_title(title)}", label_to_bm[label])
        for label, title in fm_parts["tables_list"]
        if label in label_to_bm
    ]
    lof_entries = [
        (1, f"{label}: {_clean_inline_caption_title(title)}", label_to_bm[label])
        for label, title in fm_parts["figures_list"]
        if label in label_to_bm
    ]

    for p in list(doc.paragraphs):
        t = p.text.strip()
        if t == SENTINEL_TOC_SLOT:
            _emit_dotted_toc_field(doc, p, 'TOC \\o "1-3" \\h \\z \\u \\t "Front Title,1"', toc_entries)
            p._element.getparent().remove(p._element)
        elif t == SENTINEL_LOT_SLOT:
            _emit_dotted_toc_field(doc, p, 'TOC \\h \\z \\t "Caption Table,1"', lot_entries)
            p._element.getparent().remove(p._element)
        elif t == SENTINEL_LOF_SLOT:
            _emit_dotted_toc_field(doc, p, 'TOC \\h \\z \\t "Caption Figure,1"', lof_entries)
            p._element.getparent().remove(p._element)


def _is_cover_student_table(tbl: Any) -> bool:
    """Nhận diện bảng ẩn viền 2 cột dùng trên trang bìa chính/phụ."""
    tbl_pr = tbl._tbl.tblPr
    tbl_ind = tbl_pr.find(qn("w:tblInd"))
    return tbl_ind is not None and tbl_ind.get(qn("w:w")) == "1389"


def _set_cell_border(cell: Any, side: str, sz: str, color: str = "000000") -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_borders = tc_pr.find(qn("w:tcBorders"))
    if tc_borders is None:
        tc_borders = OxmlElement("w:tcBorders")
        tc_pr.append(tc_borders)
    for old in tc_borders.findall(qn(f"w:{side}")):
        tc_borders.remove(old)
    edge = OxmlElement(f"w:{side}")
    edge.set(qn("w:val"), "single")
    edge.set(qn("w:sz"), sz)
    edge.set(qn("w:space"), "0")
    edge.set(qn("w:color"), color)
    tc_borders.append(edge)


def _compute_smart_col_widths(tbl: Any, total_twips: int) -> list[int]:
    """Tính độ rộng cột cân đối theo nội dung thực tế (header + phân vị P85 + token dài) trên tổng 9072 dxa."""
    ncols = len(tbl.columns)
    if ncols <= 0:
        return []
    nrows = len(tbl.rows)
    floors: list[int] = []
    weights: list[float] = []
    min_abs_col = 540 if ncols >= 8 else 580
    pad_budget = 145 if ncols >= 8 else 190

    for c_idx in range(ncols):
        cell_texts: list[str] = []
        max_tok = 2
        for r_idx in range(nrows):
            if c_idx >= len(tbl.rows[r_idx].cells):
                continue
            cell = tbl.rows[r_idx].cells[c_idx]
            p_texts: list[str] = []
            for p_el in cell._tc.findall(qn("w:p")):
                pieces: list[str] = []
                for el in p_el.iter():
                    if not isinstance(el.tag, str):
                        continue
                    if el.tag.endswith("}br"):
                        pieces.append("\n")
                    elif el.tag.endswith("}t") and el.text:
                        pieces.append(el.text)
                p_texts.append("".join(pieces))
            raw = "\n".join(p_texts).replace(LINEBREAK_MARKER, "\n").strip().replace("\\|", "|")
            cell_texts.append(raw)
            for tok in re.split(r"\s+", raw):
                if tok:
                    max_tok = max(max_tok, len(tok))
        if not cell_texts:
            floors.append(min_abs_col)
            weights.append(5.0)
            continue

        hdr_len = len(cell_texts[0])
        lengths = sorted(len(t) for t in cell_texts)
        p85_len = lengths[min(len(lengths) - 1, int(0.85 * len(lengths)))]
        tok_cap = min(max_tok, 28)
        eff_chars = max(hdr_len, p85_len, min(max_tok, 24), 4)
        weights.append((float(eff_chars) ** 0.78) + 0.35 * tok_cap)
        floors.append(max(min_abs_col, min(max_tok, 16) * 118 + pad_budget))

    floor_sum = sum(floors)
    max_floor_budget = int(0.78 * total_twips)
    if floor_sum > max_floor_budget and floor_sum > 0:
        scale = max_floor_budget / floor_sum
        floors = [max(min_abs_col if ncols <= 6 else 520, int(round(f * scale))) for f in floors]

    rem = max(0, total_twips - sum(floors))
    w_sum = sum(weights) or float(ncols)
    widths = [floors[idx] + round(rem * weights[idx] / w_sum) for idx in range(ncols)]
    diff = total_twips - sum(widths)
    if widths:
        max_idx = max(range(ncols), key=lambda idx: widths[idx])
        widths[max_idx] = max(480, widths[max_idx] + diff)
    return widths


def _unwrap_table_omath_para_xml(root: Any) -> None:
    """Hạ `<m:oMathPara>` trong ô bảng xuống `<m:oMath>` nội tuyến để tránh bị căn giữa lệch cột."""
    m_ns = "http://schemas.openxmlformats.org/officeDocument/2006/math"
    w_ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    for p_el in root.findall(f".//{{{w_ns}}}tc//{{{w_ns}}}p"):
        for omp in list(p_el.findall(f"{{{m_ns}}}oMathPara")):
            pos = list(p_el).index(omp)
            omaths = list(omp.findall(f"{{{m_ns}}}oMath"))
            p_el.remove(omp)
            for off, om in enumerate(omaths):
                p_el.insert(pos + off, om)


def _expand_table_linebreaks(doc: docx.document.Document) -> None:
    """Chuyển marker `XTHESISBRX` trong các ô bảng thành ngắt dòng thật `<w:br/>` của Word."""
    w_ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    for tbl in doc.tables:
        if _is_cover_student_table(tbl):
            continue
        for row in tbl.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for r_el in list(p._p.findall(f"{{{w_ns}}}r")):
                        t_nodes = list(r_el.findall(f"{{{w_ns}}}t"))
                        if not t_nodes:
                            continue
                        full_text = "".join(tn.text or "" for tn in t_nodes)
                        if LINEBREAK_MARKER not in full_text:
                            continue
                        parts = full_text.split(LINEBREAK_MARKER)
                        for child in list(r_el):
                            if child.tag in (f"{{{w_ns}}}t", f"{{{w_ns}}}br"):
                                r_el.remove(child)
                        for part_idx, part in enumerate(parts):
                            if part_idx > 0:
                                r_el.append(OxmlElement("w:br"))
                            if part or part_idx == 0:
                                t_new = OxmlElement("w:t")
                                t_new.set(qn("xml:space"), "preserve")
                                t_new.text = part
                                r_el.append(t_new)


def _format_all_tables(doc: docx.document.Document) -> None:
    """Định dạng toàn bộ bảng dữ liệu theo chuẩn Booktabs (nền trắng, không viền dọc, hàng tổng in đậm)."""
    _expand_table_linebreaks(doc)
    _unwrap_table_omath_para_xml(doc.element.body)
    border_xml = (
        f'<w:tblBorders {nsdecls("w")}>'
        '<w:top w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
        '<w:left w:val="none"/>'
        '<w:bottom w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
        '<w:right w:val="none"/>'
        '<w:insideH w:val="none"/>'
        '<w:insideV w:val="none"/>'
        "</w:tblBorders>"
    )

    for tbl in doc.tables:
        if _is_cover_student_table(tbl):
            continue

        ncols = len(tbl.columns)
        h_mar = "55" if ncols >= 8 else "75"
        cell_mar_xml = (
            f'<w:tblCellMar {nsdecls("w")}>'
            '<w:top w:w="34" w:type="dxa"/>'
            f'<w:left w:w="{h_mar}" w:type="dxa"/>'
            '<w:bottom w:w="34" w:type="dxa"/>'
            f'<w:right w:w="{h_mar}" w:type="dxa"/>'
            "</w:tblCellMar>"
        )

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

        grid_cols = tbl._tbl.xpath("./w:tblGrid/w:gridCol")
        scaled_widths = _compute_smart_col_widths(tbl, PRINTABLE_WIDTH_TWIPS)
        if grid_cols and len(grid_cols) == len(scaled_widths):
            for col, sw in zip(grid_cols, scaled_widths):
                col.set(qn("w:w"), str(sw))

        cell_pt = 10.0 if ncols >= 6 else 10.5
        nrows = len(tbl.rows)
        first_last_row_text = (
            tbl.rows[-1].cells[0].text.strip() if nrows > 1 and len(tbl.rows[-1].cells) > 0 else ""
        )
        has_summary_row = first_last_row_text.startswith(("Tổng cộng", "Tổng hợp", "Tổng:"))

        for r_idx, row in enumerate(tbl.rows):
            is_header = r_idx == 0
            is_summary = has_summary_row and (r_idx == nrows - 1)
            tr_pr = row._tr.get_or_add_trPr()
            if tr_pr.find(qn("w:cantSplit")) is None:
                tr_pr.append(OxmlElement("w:cantSplit"))
            if is_header and tr_pr.find(qn("w:tblHeader")) is None:
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

                # Xóa tô nền xám kế thừa từ table style Pandoc để giữ nền trắng Booktabs
                for old_shd in tc_pr.findall(qn("w:shd")):
                    tc_pr.remove(old_shd)
                for old_bdr in tc_pr.findall(qn("w:tcBorders")):
                    tc_pr.remove(old_bdr)

                if is_header:
                    _set_cell_border(cell, "bottom", "6", "000000")
                if is_summary:
                    _set_cell_border(cell, "top", "4", "000000")

                for p in cell.paragraphs:
                    if p.alignment in (None, WD_ALIGN_PARAGRAPH.JUSTIFY):
                        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    pf = p.paragraph_format
                    pf.first_line_indent = Cm(0)
                    pf.line_spacing = 1.15
                    pf.space_before = Pt(1)
                    pf.space_after = Pt(1)
                    if (is_header or nrows <= 5) and (r_idx < nrows - 1):
                        pf.keep_with_next = True
                    for run in p.runs:
                        if "\\|" in run.text:
                            run.text = run.text.replace("\\|", "|")
                        run.font.name = FONT_NAME
                        run.font.size = Pt(cell_pt)
                        run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
                        if is_header or is_summary:
                            run.font.bold = True
                        _strip_theme_fonts_and_set(run._element, FONT_NAME, size_pt=cell_pt)


def _strip_syntax_token_rstyle(p: docx.text.paragraph.Paragraph) -> None:
    """Chuẩn hóa toàn bộ run trong khối mã hoặc code inline về Times New Roman màu đen."""
    sname = p.style.name if p.style else ""
    target_size = 10.0 if sname == "Source Code" else None
    for run in p.runs:
        rpr = run._r.find(qn("w:rPr"))
        if rpr is not None:
            rstyle = rpr.find(qn("w:rStyle"))
            if rstyle is not None and rstyle.get(qn("w:val")) in (
                "NormalTok",
                "StringTok",
                "KeywordTok",
                "AlertTok",
                "DataTypeTok",
                "DecValTok",
                "FloatTok",
                "CommentTok",
                "OperatorTok",
                "FunctionTok",
                "BuiltInTok",
                "AttributeTok",
                "ExtensionTok",
                "ConstantTok",
                "VerbatimChar",
            ):
                rpr.remove(rstyle)
            for col in rpr.findall(qn("w:color")):
                rpr.remove(col)
        run.font.name = FONT_NAME
        run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        if target_size is not None:
            run.font.size = Pt(target_size)
        _strip_theme_fonts_and_set(run._element, FONT_NAME, size_pt=target_size)


def _apply_display_equation_tabs(doc: docx.document.Document) -> None:
    """Ghép marker số công thức [[THESIS_EQ_NUM:(X.Y)]] vào đoạn công thức khối và căn tab 4536/9072."""
    eq_pat = re.compile(re.escape(EQ_NUM_MARKER_PREFIX) + r"(\(\d+\.\d+\))\]\]")
    m_ns = "http://schemas.openxmlformats.org/officeDocument/2006/math"
    paras = list(doc.paragraphs)

    for idx, p in enumerate(paras):
        txt = p.text.strip()
        if not (m := eq_pat.fullmatch(txt)):
            continue
        eq_num = m.group(1)
        if idx == 0:
            continue
        prev_p = paras[idx - 1]
        # Chèn tab căn giữa (4536 dxa) và tab căn phải (9072 dxa) cho đoạn chứa oMathPara/oMath
        prev_p.style = doc.styles["Normal"]
        prev_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        prev_p.paragraph_format.first_line_indent = Cm(0)
        prev_p.paragraph_format.space_before = Pt(6)
        prev_p.paragraph_format.space_after = Pt(6)

        pPr = prev_p._p.get_or_add_pPr()
        for old_tabs in pPr.findall(qn("w:tabs")):
            pPr.remove(old_tabs)
        tabs = OxmlElement("w:tabs")
        for val, pos in (("center", str(CENTER_TAB_TWIPS)), ("right", str(PRINTABLE_WIDTH_TWIPS))):
            tb = OxmlElement("w:tab")
            tb.set(qn("w:val"), val)
            tb.set(qn("w:pos"), pos)
            tabs.append(tb)
        pPr.append(tabs)

        # Lấy phần tử m:oMath ra khỏi m:oMathPara để dùng chung trên một dòng có tab
        omath_paras = prev_p._p.findall(f"{{{m_ns}}}oMathPara")
        for omp in omath_paras:
            omaths = omp.findall(f"{{{m_ns}}}oMath")
            pos_in_prev = list(prev_p._p).index(omp)
            prev_p._p.remove(omp)
            for offset, om in enumerate(omaths):
                prev_p._p.insert(pos_in_prev + offset, om)

        r_lead = OxmlElement("w:r")
        rPr_l = OxmlElement("w:rPr")
        r_lead.append(rPr_l)
        r_lead.append(OxmlElement("w:tab"))
        _strip_theme_fonts_and_set(r_lead, FONT_NAME, size_pt=13.0)
        insert_pos = 1 if prev_p._p.pPr is not None else 0
        prev_p._p.insert(insert_pos, r_lead)

        r_end_tab = prev_p.add_run()
        r_end_tab.font.name = FONT_NAME
        _strip_theme_fonts_and_set(r_end_tab._element, FONT_NAME, size_pt=13.0)
        r_end_tab.add_tab()

        r_num = prev_p.add_run(eq_num)
        r_num.font.name = FONT_NAME
        r_num.font.size = Pt(13.0)
        r_num.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        _strip_theme_fonts_and_set(r_num._element, FONT_NAME, size_pt=13.0)

        p._element.getparent().remove(p._element)


def _cm_to_twips(cm_val: float) -> int:
    """Quy đổi khoảng cách theo cm sang đơn vị twips (1 inch = 1440 twips)."""
    return round(cm_val * 1440.0 / 2.54)


def _normalize_list_numbering(doc: docx.document.Document) -> None:
    """Chuyển danh sách bullet sang dấu '-' (Times New Roman 13 pt) và đồng bộ thụt lề trong numbering.xml."""
    try:
        numbering_root = doc.part.numbering_part.numbering_definitions._numbering
    except (AttributeError, NotImplementedError):
        return

    for lvl in numbering_root.findall(f".//{qn('w:lvl')}"):
        depth = int(lvl.get(qn("w:ilvl"), "0"))
        left_twips = _cm_to_twips(LIST_LEFT_BASE_CM + LIST_DEPTH_STEP_CM * depth)
        hanging_twips = _cm_to_twips(LIST_HANGING_CM)

        num_fmt = lvl.find(qn("w:numFmt"))
        lvl_text = lvl.find(qn("w:lvlText"))
        if (
            num_fmt is not None
            and num_fmt.get(qn("w:val")) == "bullet"
            and lvl_text is not None
            and (lvl_text.get(qn("w:val")) or "").strip() != ""
        ):
            lvl_text.set(qn("w:val"), "-")

        suff = lvl.find(qn("w:suff"))
        if suff is None:
            suff = OxmlElement("w:suff")
            suff.set(qn("w:val"), "tab")
            if lvl_text is not None:
                lvl.insert(list(lvl).index(lvl_text), suff)
            else:
                lvl.insert(0, suff)
        elif suff.get(qn("w:val")) != "tab":
            suff.set(qn("w:val"), "tab")

        ppr = lvl.find(qn("w:pPr"))
        if ppr is None:
            ppr = OxmlElement("w:pPr")
            rpr_existing = lvl.find(qn("w:rPr"))
            if rpr_existing is not None:
                lvl.insert(list(lvl).index(rpr_existing), ppr)
            else:
                lvl.append(ppr)
        for old_tabs in ppr.findall(qn("w:tabs")):
            ppr.remove(old_tabs)
        ind = ppr.find(qn("w:ind"))
        if ind is None:
            ind = OxmlElement("w:ind")
            ppr.append(ind)
        for stale_attr in ("w:leftChars", "w:hangingChars", "w:firstLine"):
            ind.attrib.pop(qn(stale_attr), None)
        ind.set(qn("w:left"), str(left_twips))
        ind.set(qn("w:hanging"), str(hanging_twips))

        rpr = lvl.find(qn("w:rPr"))
        if rpr is None:
            rpr = OxmlElement("w:rPr")
            lvl.append(rpr)
        color_el = rpr.find(qn("w:color"))
        if color_el is None:
            color_el = OxmlElement("w:color")
            sz_el = rpr.find(qn("w:sz"))
            if sz_el is not None:
                rpr.insert(list(rpr).index(sz_el), color_el)
            else:
                rpr.append(color_el)
        color_el.set(qn("w:val"), "000000")
        _strip_theme_fonts_and_set(lvl, FONT_NAME, size_pt=13.0)
        rfonts = rpr.find(qn("w:rFonts"))
        if rfonts is not None:
            rfonts.attrib.pop(qn("w:hint"), None)


def _scale_images_and_style_paragraphs(doc: docx.document.Document) -> None:
    """Chuẩn hóa phông Times New Roman, caption Bảng/Hình, chú thích bảng, ảnh và danh sách."""
    _apply_display_equation_tabs(doc)
    _normalize_list_numbering(doc)

    in_references = False
    paras = doc.paragraphs

    for idx, p in enumerate(paras):
        txt = p.text.strip()
        sname = p.style.name if p.style else ""

        if txt == "TÀI LIỆU THAM KHẢO":
            in_references = True
        elif txt == "PHỤ LỤC":
            in_references = False

        # Chuẩn hóa thụt lề, giãn dòng và khoảng cách các đoạn danh sách có numPr
        ppr = p._p.pPr
        num_pr = ppr.find(qn("w:numPr")) if ppr is not None else None
        if num_pr is not None:
            ilvl_el = num_pr.find(qn("w:ilvl"))
            depth = int(ilvl_el.get(qn("w:val"), "0")) if ilvl_el is not None else 0
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.left_indent = Cm(LIST_LEFT_BASE_CM + LIST_DEPTH_STEP_CM * depth)
            p.paragraph_format.first_line_indent = Cm(-LIST_HANGING_CM)
            p.paragraph_format.line_spacing = LIST_LINE_SPACING
            p.paragraph_format.space_before = Pt(LIST_SPACE_BEFORE_PT)
            p.paragraph_format.space_after = Pt(LIST_SPACE_AFTER_PT)

        # Heading 1 / Heading 2 / Heading 3: đồng bộ khoảng cách và giữ trang
        if sname == "Heading 1":
            p.paragraph_format.keep_with_next = True
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.page_break_before = not txt.startswith("CHƯƠNG 1")
            for r in p.runs:
                if r.text:
                    r.text = r.text.upper()

        # Caption Bảng X.Y: -> Style Caption Table (11 pt Bold, căn trái, keep_with_next=True)
        if re.match(r"^Bảng\s+[A-D0-9]+\.\d+\s*[-–:]", txt):
            p.style = doc.styles["Caption Table"]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.keep_with_next = True
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(4)
            for run in p.runs:
                run.font.bold = True
                run.font.size = Pt(11.0)
                _strip_theme_fonts_and_set(run._element, FONT_NAME, size_pt=11.0)

        # Caption Hình X.Y: -> Style Caption Figure (11 pt Bold, căn giữa)
        elif re.match(r"^Hình\s+[A-D0-9]+\.\d+\s*[-–:]", txt):
            p.style = doc.styles["Caption Figure"]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.keep_with_next = False
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(4)
            for run in p.runs:
                run.font.bold = True
                run.font.size = Pt(11.0)
                _strip_theme_fonts_and_set(run._element, FONT_NAME, size_pt=11.0)

        # Chú thích nghiêng trong ngoặc đơn *(...)* ngay dưới bảng
        elif txt.startswith("(") and txt.endswith(")") and p.runs and all(
            (r.italic or not r.text.strip()) for r in p.runs
        ):
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = 1.15
            for run in p.runs:
                run.font.italic = True
                run.font.size = Pt(10.5)
                _strip_theme_fonts_and_set(run._element, FONT_NAME, size_pt=10.5)

        # Khối mã nguồn fenced code
        elif sname == "Source Code":
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.left_indent = Cm(0.35)
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)

        # Đoạn chứa hình ảnh (<w:drawing>)
        drawings = p._p.xpath(".//w:drawing")
        if drawings:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.keep_with_next = True
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(4)
            for drw in drawings:
                for ext in drw.xpath(".//wp:extent | .//a:xfrm/a:ext"):
                    cx_raw = ext.get("cx")
                    cy_raw = ext.get("cy")
                    if cx_raw and cy_raw and cx_raw.isdigit() and cy_raw.isdigit():
                        cx = int(cx_raw)
                        cy = int(cy_raw)
                        scale = min(1.0, MAX_IMAGE_WIDTH_EMU / max(cx, 1), MAX_IMAGE_HEIGHT_EMU / max(cy, 1))
                        if cx > int(Cm(8)):
                            scale = min(MAX_IMAGE_WIDTH_EMU / cx, MAX_IMAGE_HEIGHT_EMU / cy)
                        ext.set("cx", str(int(cx * scale)))
                        ext.set("cy", str(int(cy * scale)))

        # Tài liệu tham khảo [1]..[5]: hanging indent 0,9 cm
        if in_references and re.match(r"^\[\d+\]\s+", txt):
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.left_indent = Cm(0.9)
            p.paragraph_format.first_line_indent = Cm(-0.9)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(4)

        _strip_syntax_token_rstyle(p)
        _ = idx


def _split_sections_at_main_sentinel(doc: docx.document.Document) -> None:
    """Chèn Section Break giữa Section 1 (Mở đầu) và Section 2 (Thân bài) tại sentinel."""
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
    raise RuntimeError("Không tìm thấy sentinel phân tách Section Mở đầu và Section Thân bài.")


def _enable_auto_update_fields(doc: docx.document.Document) -> None:
    settings_el = doc.settings.element
    for old in settings_el.findall(qn("w:updateFields")):
        settings_el.remove(old)
    upd = OxmlElement("w:updateFields")
    upd.set(qn("w:val"), "true")
    settings_el.append(upd)


def _reinject_update_fields_in_docx(src_docx: Path, dst_docx: Path | None = None) -> None:
    """Khôi phục cờ <w:updateFields w:val="true"/> trong word/settings.xml và ghi ra dst_docx."""
    import time

    target = dst_docx if dst_docx is not None else src_docx
    tmp_path = target.with_suffix(".tmp.docx")
    with zipfile.ZipFile(src_docx, "r") as zin, zipfile.ZipFile(
        tmp_path, "w", compression=zipfile.ZIP_DEFLATED
    ) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/settings.xml":
                root = etree.fromstring(data)
                for old in root.findall(qn("w:updateFields")):
                    root.remove(old)
                upd = etree.Element(qn("w:updateFields"))
                upd.set(qn("w:val"), "true")
                root.append(upd)
                data = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone="yes")
            elif item.filename == "word/document.xml":
                doc_root = etree.fromstring(data)
                _unwrap_table_omath_para_xml(doc_root)
                data = etree.tostring(doc_root, xml_declaration=True, encoding="UTF-8", standalone="yes")
            zout.writestr(item, data)
    for attempt in range(5):
        try:
            os.replace(tmp_path, target)
            return
        except PermissionError:
            if attempt == 4:
                raise
            time.sleep(0.4)


def _try_update_fields_with_wps(docx_path: Path, export_pdf_path: Path | None = None) -> bool:
    """Cập nhật số trang TOC/PAGEREF qua WPS Writer COM trên bản sao tạm (tránh khóa tệp đích)."""
    work_fd, work_name = tempfile.mkstemp(prefix="wps_work_", suffix=".docx")
    os.close(work_fd)
    work_docx = Path(work_name)
    shutil.copy2(docx_path, work_docx)

    pdf_cmd = ""
    if export_pdf_path is not None:
        export_pdf_path.parent.mkdir(parents=True, exist_ok=True)
        pdf_escaped = str(export_pdf_path.resolve()).replace("'", "''")
        pdf_cmd = f"$doc.ExportAsFixedFormat('{pdf_escaped}', 17)"

    ps_script = f"""
$ErrorActionPreference = 'Stop'
$wps = $null
$doc = $null
try {{
    $wps = New-Object -ComObject Kwps.Application
    $wps.Visible = $false
    $wps.DisplayAlerts = 0
    $doc = $wps.Documents.Open('{str(work_docx.resolve()).replace("'", "''")}', $false, $false)
    foreach ($sid in @(-20, -21, -22)) {{
        try {{
            $st = $doc.Styles.Item($sid)
            $st.Font.Name = 'Times New Roman'
            $st.Font.Size = 12
            $st.Font.Bold = $(if ($sid -eq -20) {{ 1 }} else {{ 0 }})
            $st.ParagraphFormat.RightIndent = 36.85
        }} catch {{}}
    }}
    foreach ($toc in $doc.TablesOfContents) {{ $toc.UpdatePageNumbers() }}
    $doc.Fields.Update() | Out-Null
    $doc.Repaginate()
    $doc.Fields.Update() | Out-Null
    for ($i = 2; $i -le $doc.TablesOfContents.Count; $i++) {{
        $r = $doc.TablesOfContents.Item($i).Range
        $r.Font.Name = 'Times New Roman'
        $r.Font.Size = 11
        $r.Font.Bold = 0
        $r.ParagraphFormat.RightIndent = 36.85
    }}
    $doc.Repaginate()
    foreach ($toc in $doc.TablesOfContents) {{ $toc.UpdatePageNumbers() }}
    if ($doc.TablesOfContents.Count -ge 1) {{
        foreach ($p in $doc.TablesOfContents.Item(1).Range.Paragraphs) {{
            $sname = [string]$p.Style.NameLocal
            $isLvl1 = ($sname -match '(^|\\s)1$')
            $p.Range.Font.Name = 'Times New Roman'
            $p.Range.Font.Size = 12
            $p.Range.Font.Bold = $(if ($isLvl1) {{ 1 }} else {{ 0 }})
        }}
    }}
    for ($i = 2; $i -le $doc.TablesOfContents.Count; $i++) {{
        $r = $doc.TablesOfContents.Item($i).Range
        $r.Font.Name = 'Times New Roman'
        $r.Font.Size = 11
        $r.Font.Bold = 0
        $r.ParagraphFormat.RightIndent = 36.85
    }}
    $doc.Repaginate()
    $doc.Save()
    {pdf_cmd}
    $doc.Close($false)
    [System.Runtime.Interopservices.Marshal]::FinalReleaseComObject($doc) | Out-Null
    $doc = $null
    Write-Output 'WPS_COM_OK'
}} finally {{
    if ($doc -ne $null) {{
        try {{ $doc.Close($false) }} catch {{}}
        try {{ [System.Runtime.Interopservices.Marshal]::FinalReleaseComObject($doc) | Out-Null }} catch {{}}
    }}
    if ($wps -ne $null) {{
        try {{ $wps.Quit(0) }} catch {{}}
        try {{ [System.Runtime.Interopservices.Marshal]::FinalReleaseComObject($wps) | Out-Null }} catch {{}}
    }}
}}
"""
    try:
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )
        ok = proc.returncode == 0 and "WPS_COM_OK" in proc.stdout
        if ok:
            _reinject_update_fields_in_docx(work_docx, docx_path)
        else:
            print(
                f"[WPS COM] Thất bại (returncode={proc.returncode}): {proc.stderr.strip()}",
                file=sys.stderr,
            )
        return ok
    except subprocess.TimeoutExpired as exc:
        print(f"[WPS COM] Quá thời gian chờ ({exc.timeout}s).", file=sys.stderr)
        return False
    except Exception as exc:
        print(f"[WPS COM] Lỗi không mong đợi: {exc}", file=sys.stderr)
        return False
    finally:
        try:
            if work_docx.exists():
                work_docx.unlink()
        except OSError:
            pass


def build(
    repo_root: Path = REPO_ROOT,
    output_path: Path | None = None,
    mirror_output_path: Path | None = None,
    try_wps_com: bool = False,
    export_pdf_path: Path | None = None,
) -> Path:
    """Ghép toàn bộ báo cáo Markdown và xuất tệp .docx hoàn chỉnh chuẩn báo cáo đồ án CTUT (KHMT 1)."""
    report_dir = repo_root / "docs" / "thesis" / "report"
    figures_dir = repo_root / "docs" / "thesis" / "figures"
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
    appendix_md = ""
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
        "# LỜI CAM ĐOAN",
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
        "# DANH MỤC HÌNH ẢNH",
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
            str(figures_dir),
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

        _apply_standard_styles(doc)

        anchor_first = doc.paragraphs[0]
        _insert_cover_pages_before_first_paragraph(
            doc,
            anchor_first,
            fm_parts["cover_main_blocks"],
            fm_parts["cover_sub_blocks"],
            figures_dir / "logo_ctut.png",
        )
        _split_sections_at_main_sentinel(doc)

        _style_front_matter_headings(doc)
        _format_all_tables(doc)
        _scale_images_and_style_paragraphs(doc)
        _populate_toc_and_lists(doc, fm_parts)

        if len(doc.sections) != 3:
            raise RuntimeError(f"Kỳ vọng 3 Section nhưng thu được {len(doc.sections)} Section.")

        border_png = figures_dir / "khung_trang_bia.png"
        _configure_section_page_layout(
            doc.sections[0], page_num_fmt=None, border_png=border_png
        )
        _configure_section_page_layout(
            doc.sections[1], page_num_fmt="lowerRoman", start_num=1, border_png=None
        )
        _configure_section_page_layout(
            doc.sections[2], page_num_fmt="decimal", start_num=1, border_png=None
        )

        _enable_auto_update_fields(doc)
        doc.save(str(out_file))
    finally:
        if tmp_docx.exists():
            tmp_docx.unlink()

    if try_wps_com:
        if not _try_update_fields_with_wps(out_file, export_pdf_path=export_pdf_path):
            raise RuntimeError(
                "WPS Writer COM không cập nhật được trường TOC/PAGEREF hoặc xuất PDF thất bại."
            )

    if mirror_output_path is not None:
        mirror_output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(out_file, mirror_output_path)

    return out_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Chuyển đổi báo cáo Markdown sang .docx chuẩn báo cáo đồ án CTUT (KHMT 1).")
    parser.add_argument("--wps", action="store_true", help="Cập nhật trường số trang qua WPS Writer COM nếu khả dụng.")
    parser.add_argument("--pdf-out", type=Path, default=None, help="Đường dẫn xuất thêm tệp PDF qua WPS Writer (tùy chọn).")
    args = parser.parse_args()

    default_out = REPO_ROOT.parent / "BAO_CAO_DO_AN_KHMT1_HOAN_CHINH.docx"
    mirror_out = REPO_ROOT / "docs" / "thesis" / "BAO_CAO_DO_AN_KHMT1_HOAN_CHINH.docx"
    result = build(
        REPO_ROOT,
        output_path=default_out,
        mirror_output_path=mirror_out,
        try_wps_com=args.wps,
        export_pdf_path=args.pdf_out,
    )
    print(f"Built DOCX: {result} ({result.stat().st_size:,} bytes)")
    print(f"Mirror DOCX: {mirror_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
