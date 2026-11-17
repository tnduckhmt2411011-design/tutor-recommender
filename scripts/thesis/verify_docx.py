"""Kiểm định tự động cấu trúc, định dạng, công thức, ảnh và độ toàn vẹn của tệp DOCX đầu ra."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import docx
from docx.oxml.ns import qn

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from build_docx import ORDER  # noqa: E402
from check_captions import extract_captions  # noqa: E402

EXPECTED_H1_PREFIXES: tuple[str, ...] = (
    "LỜI CẢM ƠN",
    "LỜI CAM ĐOAN LIÊM CHÍNH HỌC THUẬT",
    "TÓM TẮT",
    "ABSTRACT",
    "DANH MỤC KÝ HIỆU VÀ CHỮ VIẾT TẮT",
    "DANH MỤC BẢNG BIỂU",
    "DANH MỤC HÌNH VẼ, SƠ ĐỒ, BIỂU ĐỒ",
    "CHƯƠNG 1.",
    "CHƯƠNG 2.",
    "CHƯƠNG 3.",
    "CHƯƠNG 4.",
    "CHƯƠNG 5.",
    "CHƯƠNG 6.",
    "TÀI LIỆU THAM KHẢO",
    "PHỤ LỤC A.",
    "PHỤ LỤC B.",
    "PHỤ LỤC C.",
    "PHỤ LỤC D.",
)

FORBIDDEN_STRINGS: tuple[str, ...] = (
    "[!NOTE]",
    "[!IMPORTANT]",
    "[!WARNING]",
    "TODO",
    "TBD",
    "FIXME",
    "…",
)


def _markdown_body_word_count(report_dir: Path) -> int:
    """Đếm số từ văn xuôi (đã bỏ công thức LaTeX và cú pháp Markdown) ở phần thân báo cáo."""
    total = 0
    for fname in ORDER[1:]:
        txt = (report_dir / fname).read_text(encoding="utf-8")
        clean = re.sub(r"\$\$[\s\S]*?\$\$|\$[^$\n]+\$", " ", txt)
        clean = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", clean)
        clean = re.sub(r">\s*\[!(?:NOTE|IMPORTANT|WARNING)\]", "Lưu ý:", clean)
        clean = re.sub(r"(?m)^\s*\|?(?:\s*:?-{2,}:?\s*\|)+\s*$", " ", clean)
        clean = re.sub(r"(?m)^\s*```[^\n]*\s*$", " ", clean)
        clean = re.sub(r"(?m)^\s*[-*#>]+\s+", " ", clean)
        clean = re.sub(r"(?m)^\s*\d+\.\s+", " ", clean)
        clean = (
            clean.replace("|", " ")
            .replace("**", "")
            .replace("*", "")
            .replace("`", "")
            .replace("<br/>", " ")
        )
        clean = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", clean)
        total += len(re.findall(r"\S+", clean))
    return total


def _paragraph_text_xml(p_el: ET.Element) -> str:
    """Trích chuỗi văn bản thuần `<w:t>` của một phần tử đoạn `<w:p>`."""
    w_ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    return "".join(t.text or "" for t in p_el.iter(f"{w_ns}t"))


def verify_docx(docx_path: Path, repo_root: Path = REPO_ROOT) -> tuple[list[str], dict[str, object]]:
    """Kiểm định toàn diện tệp DOCX; trả về (danh sách lỗi, thống kê kiểm định)."""
    issues: list[str] = []
    stats: dict[str, object] = {}

    if not docx_path.exists():
        return [f"Không tìm thấy tệp DOCX: {docx_path}"], stats

    doc = docx.Document(str(docx_path))

    # 1. Kiểm tra file zip, media, OMML và updateFields
    with zipfile.ZipFile(docx_path) as zf:
        media_files = [n for n in zf.namelist() if n.startswith("word/media/")]
        doc_xml = ET.fromstring(zf.read("word/document.xml"))
        settings_xml = ET.fromstring(zf.read("word/settings.xml"))

    m_ns = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"
    w_ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    omath_nodes = doc_xml.findall(f".//{m_ns}oMath")
    stats["media_count"] = len(media_files)
    stats["omath_count"] = len(omath_nodes)

    if len(media_files) != 9:
        issues.append(f"Số tệp ảnh trong word/media/ là {len(media_files)} (kỳ vọng 9).")
    if len(omath_nodes) < 100:
        issues.append(f"Số công thức OMML <m:oMath> quá thấp: {len(omath_nodes)} (kỳ vọng > 100).")

    upd_el = settings_xml.find(f".//{w_ns}updateFields")
    if upd_el is None or upd_el.attrib.get(f"{w_ns}val") != "true":
        issues.append("Thiếu cờ <w:updateFields w:val='true'/> trong word/settings.xml.")

    # 2. Kiểm tra 3 Section, khổ A4, lề và đánh số trang
    stats["sections"] = len(doc.sections)
    if len(doc.sections) != 3:
        issues.append(f"Số lượng Section là {len(doc.sections)} (kỳ vọng 3: Bìa, Mở đầu, Thân bài).")
    else:
        expected_sec = [
            (0, None, None, False),
            (1, "lowerRoman", "1", True),
            (2, "decimal", "1", True),
        ]
        for idx, exp_fmt, exp_start, need_page_field in expected_sec:
            sec = doc.sections[idx]
            w_mm = round(sec.page_width.mm)
            h_mm = round(sec.page_height.mm)
            if w_mm != 210 or h_mm != 297:
                issues.append(f"Section {idx} sai khổ giấy A4: {w_mm}x{h_mm} mm.")
            if (
                abs(sec.top_margin.cm - 2.5) > 0.05
                or abs(sec.bottom_margin.cm - 2.0) > 0.05
                or abs(sec.left_margin.cm - 3.0) > 0.05
                or abs(sec.right_margin.cm - 2.0) > 0.05
            ):
                issues.append(
                    f"Section {idx} sai lề chuẩn (2.5/2.0/3.0/2.0 cm): "
                    f"{sec.top_margin.cm:.2f}/{sec.bottom_margin.cm:.2f}/{sec.left_margin.cm:.2f}/{sec.right_margin.cm:.2f}."
                )
            pg = sec._sectPr.find(qn("w:pgNumType"))
            fmt = pg.get(qn("w:fmt")) if pg is not None else None
            start = pg.get(qn("w:start")) if pg is not None else None
            instrs = [el.text.strip() for el in sec.footer._element.xpath(".//w:instrText") if el.text]
            has_page = any("PAGE" in ins for ins in instrs)
            if fmt != exp_fmt or start != exp_start or has_page != need_page_field:
                issues.append(
                    f"Section {idx} đánh số trang không khớp: fmt={fmt}, start={start}, has_PAGE={has_page}."
                )

    # 3. Kiểm tra phông chữ các style chính
    for st_name in (
        "Normal",
        "Body Text",
        "First Paragraph",
        "Compact",
        "Block Text",
        "Heading 1",
        "Heading 2",
        "Heading 3",
    ):
        if st_name in doc.styles and doc.styles[st_name].font.name != "Times New Roman":
            issues.append(f"Style '{st_name}' dùng phông '{doc.styles[st_name].font.name}' != 'Times New Roman'.")

    # 4. Kiểm tra thứ tự Heading 1
    h1_texts = [
        p.text.strip()
        for p in doc.paragraphs
        if p.style and p.style.name == "Heading 1" and p.text.strip()
    ]
    pos = -1
    for prefix in EXPECTED_H1_PREFIXES:
        found_idx = next((i for i, t in enumerate(h1_texts) if i > pos and t.startswith(prefix)), None)
        if found_idx is None:
            issues.append(f"Thiếu hoặc sai thứ tự Heading 1 bắt đầu bằng '{prefix}'.")
        else:
            pos = found_idx

    # 5. Quét toàn bộ <w:p> qua XML nhanh để kiểm tra caption, từ cấm, dấu '$', đếm từ
    report_dir = repo_root / "docs" / "thesis" / "report"
    exp_tables: list[str] = []
    exp_figures: list[str] = []
    for ch_path in sorted(report_dir.glob("chuong-*.md")):
        tbls, figs = extract_captions(ch_path.read_text(encoding="utf-8"))
        exp_tables.extend(tid for tid, _, _ in tbls)
        exp_figures.extend(fid for fid, _, _ in figs)

    body_el = doc_xml.find(f"{w_ns}body")
    assert body_el is not None
    top_level_ps = set(body_el.findall(f"{w_ns}p"))

    in_main = False
    found_tbl_caps: list[str] = []
    found_fig_caps: list[str] = []
    main_words = 0

    for p_el in body_el.iter(f"{w_ns}p"):
        txt = _paragraph_text_xml(p_el).strip()
        if txt.startswith("CHƯƠNG 1."):
            in_main = True
        if in_main:
            main_words += len(re.findall(r"\S+", txt))

        # Chỉ kiểm tra caption ở cấp đoạn trực tiếp trong body (không phải cell Danh mục)
        is_top_level = p_el in top_level_ps
        if in_main and is_top_level:
            if m_t := re.match(r"^Bảng\s+([A-D0-9]+\.\d+)\s*[-–:]", txt):
                found_tbl_caps.append(m_t.group(1))
            if m_f := re.match(r"^Hình\s+([A-D0-9]+\.\d+)\s*[-–:]", txt):
                found_fig_caps.append(m_f.group(1))

        for bad in FORBIDDEN_STRINGS:
            if bad in txt:
                issues.append(f"Phát hiện chuỗi cấm '{bad}' trong đoạn: '{txt[:80]}'.")

        # Kiểm tra '$' sót lại ngoài mã nguồn / biến $PORT
        p_style_el = p_el.find(f"{w_ns}pPr/{w_ns}pStyle")
        p_style_val = p_style_el.attrib.get(f"{w_ns}val", "") if p_style_el is not None else ""
        if p_style_val != "SourceCode" and "$" in txt and "$PORT" not in txt:
            issues.append(f"Phát hiện ký tự '$' có thể chưa biên dịch toán học: '{txt[:90]}'.")

    stats["body_tables"] = len(found_tbl_caps)
    stats["body_figures"] = len(found_fig_caps)

    if found_tbl_caps != exp_tables:
        issues.append(
            f"Danh sách Bảng trong DOCX ({len(found_tbl_caps)}) không khớp nguồn Markdown ({len(exp_tables)})."
        )
    if found_fig_caps != exp_figures:
        issues.append(
            f"Danh sách Hình trong DOCX ({len(found_fig_caps)}) không khớp nguồn Markdown ({len(exp_figures)})."
        )

    # 6. Đối chiếu số từ phần thân
    md_words = _markdown_body_word_count(report_dir)
    diff_pct = abs(main_words - md_words) / max(md_words, 1) * 100.0
    stats["docx_main_words"] = main_words
    stats["md_main_words"] = md_words
    stats["word_diff_pct"] = round(diff_pct, 2)
    if diff_pct >= 3.0:
        issues.append(
            f"Chênh lệch số từ thân bài vượt 3%: docx={main_words}, md={md_words} ({diff_pct:.2f}%)."
        )

    return issues, stats


def main() -> int:
    docx_path = REPO_ROOT.parent / "BAO_CAO_DO_AN_KHMT1_HOAN_CHINH.docx"
    issues, stats = verify_docx(docx_path, REPO_ROOT)
    print(f"Verified DOCX: {docx_path}")
    print(f"Stats: {stats}")
    if issues:
        for err in issues:
            print(f"  [ERROR] {err}")
        return 1
    print("OK: 0 issues found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
