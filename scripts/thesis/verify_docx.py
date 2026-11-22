"""Kiểm định tự động cấu trúc, định dạng, công thức, ảnh, Booktabs và độ toàn vẹn của tệp DOCX chuẩn Báo cáo Học máy."""

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

from build_docx import FONT_NAME, FRONT_TITLE_TEXTS, ORDER  # noqa: E402
from check_captions import extract_captions  # noqa: E402

EXPECTED_FRONT_TITLES: tuple[str, ...] = FRONT_TITLE_TEXTS

EXPECTED_MAIN_H1_PREFIXES: tuple[str, ...] = (
    "CHƯƠNG 1.",
    "CHƯƠNG 2.",
    "CHƯƠNG 3.",
    "CHƯƠNG 4.",
    "CHƯƠNG 5.",
    "CHƯƠNG 6.",
    "TÀI LIỆU THAM KHẢO",
    "PHỤ LỤC",
)

EXPECTED_APPENDIX_H2_PREFIXES: tuple[str, ...] = (
    "Phụ lục A.",
    "Phụ lục B.",
    "Phụ lục C.",
    "Phụ lục D.",
)

FORBIDDEN_STRINGS: tuple[str, ...] = (
    "[!NOTE]",
    "[!IMPORTANT]",
    "[!WARNING]",
    "TODO",
    "TBD",
    "FIXME",
    "…",
    "Tổng: 31 bảng",
    "Tổng: 9 hình",
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
    """Trích chuỗi văn bản thuần `<w:t>` của một phần tử đoạn `<w:p>` (bỏ `<m:t>`)."""
    w_ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    m_ns = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"
    texts: list[str] = []

    def _walk(node: ET.Element) -> None:
        if node.tag.startswith(m_ns):
            return
        if node.tag == f"{w_ns}t" and node.text:
            texts.append(node.text)
        for child in node:
            _walk(child)

    _walk(p_el)
    return "".join(texts)


def _verify_booktabs_table(tbl_el: ET.Element, idx: int, w_ns: str) -> list[str]:
    """Kiểm định một bảng dữ liệu có tuân thủ đúng quy chuẩn Booktabs hay không."""
    errs: list[str] = []
    tbl_pr = tbl_el.find(f"{w_ns}tblPr")
    if tbl_pr is None:
        return [f"Bảng #{idx} thiếu <w:tblPr>."]
    borders = tbl_pr.find(f"{w_ns}tblBorders")
    if borders is None:
        return [f"Bảng #{idx} thiếu <w:tblBorders>."]

    top = borders.find(f"{w_ns}top")
    bot = borders.find(f"{w_ns}bottom")
    inside_v = borders.find(f"{w_ns}insideV")
    if top is None or top.attrib.get(f"{w_ns}val") != "single" or top.attrib.get(f"{w_ns}sz") != "12":
        errs.append(f"Bảng #{idx} sai viền trên Booktabs (kỳ vọng single sz=12).")
    if bot is None or bot.attrib.get(f"{w_ns}val") != "single" or bot.attrib.get(f"{w_ns}sz") != "12":
        errs.append(f"Bảng #{idx} sai viền dưới Booktabs (kỳ vọng single sz=12).")
    if inside_v is not None and inside_v.attrib.get(f"{w_ns}val") not in ("none", "nil"):
        errs.append(f"Bảng #{idx} còn kẻ dọc insideV={inside_v.attrib.get(f'{w_ns}val')}.")

    rows = tbl_el.findall(f"{w_ns}tr")
    if rows:
        hdr = rows[0]
        hdr_pr = hdr.find(f"{w_ns}trPr")
        if hdr_pr is None or hdr_pr.find(f"{w_ns}tblHeader") is None:
            errs.append(f"Bảng #{idx} thiếu <w:tblHeader/> ở hàng tiêu đề.")
        for cell in hdr.findall(f"{w_ns}tc"):
            tc_pr = cell.find(f"{w_ns}tcPr")
            shd = tc_pr.find(f"{w_ns}shd") if tc_pr is not None else None
            if shd is not None and shd.attrib.get(f"{w_ns}fill", "auto") not in ("auto", "FFFFFF", "clear"):
                errs.append(f"Bảng #{idx} có tô nền ở hàng tiêu đề ({shd.attrib.get(f'{w_ns}fill')}).")
            c_bot = tc_pr.find(f"{w_ns}tcBorders/{w_ns}bottom") if tc_pr is not None else None
            if c_bot is None or c_bot.attrib.get(f"{w_ns}val") != "single" or c_bot.attrib.get(f"{w_ns}sz") != "6":
                errs.append(f"Bảng #{idx} thiếu gạch dưới hàng tiêu đề Booktabs (sz=6).")
        for r_i, row in enumerate(rows):
            r_pr = row.find(f"{w_ns}trPr")
            if r_pr is None or r_pr.find(f"{w_ns}cantSplit") is None:
                errs.append(f"Bảng #{idx} hàng {r_i} thiếu <w:cantSplit/>.")
                break
    return errs


def _load_style_id_map(styles_xml: ET.Element, w_ns: str) -> dict[str, str]:
    """Ánh xạ `styleId` (có thể bị Word/WPS đổi sang số) về `w:name` chuẩn hóa."""
    mapping: dict[str, str] = {}
    for st in styles_xml.findall(f"{w_ns}style"):
        sid = st.attrib.get(f"{w_ns}styleId", "")
        nm = st.find(f"{w_ns}name")
        raw_name = nm.attrib.get(f"{w_ns}val", sid) if nm is not None else sid
        canon = re.sub(r"\s+", " ", raw_name.strip()).lower()
        mapping[sid] = canon
    return mapping


def verify_docx(docx_path: Path, repo_root: Path = REPO_ROOT) -> tuple[list[str], dict[str, object]]:
    """Kiểm định toàn diện tệp DOCX theo chuẩn báo cáo Học máy; trả về (danh sách lỗi, thống kê)."""
    issues: list[str] = []
    stats: dict[str, object] = {}

    if not docx_path.exists():
        return [f"Không tìm thấy tệp DOCX: {docx_path}"], stats

    doc = docx.Document(str(docx_path))

    # 1. Kiểm tra file zip, media (9 hình + khung bìa + logo CTUT = 11), OMML và updateFields
    with zipfile.ZipFile(docx_path) as zf:
        media_files = [
            n for n in zf.namelist() if n.startswith("word/media/") and not n.endswith("/")
        ]
        doc_xml = ET.fromstring(zf.read("word/document.xml"))
        settings_xml = ET.fromstring(zf.read("word/settings.xml"))
        styles_xml = ET.fromstring(zf.read("word/styles.xml"))
        numbering_xml = (
            ET.fromstring(zf.read("word/numbering.xml"))
            if "word/numbering.xml" in zf.namelist()
            else None
        )

    m_ns = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"
    w_ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    wp_ns = "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}"
    style_id_to_canon = _load_style_id_map(styles_xml, w_ns)
    omath_nodes = doc_xml.findall(f".//{m_ns}oMath")
    stats["media_count"] = len(media_files)
    stats["omath_count"] = len(omath_nodes)

    if numbering_xml is not None:
        for lvl in numbering_xml.findall(f".//{w_ns}lvl"):
            nf = lvl.find(f"{w_ns}numFmt")
            if nf is None or nf.attrib.get(f"{w_ns}val") != "bullet":
                continue
            lt = lvl.find(f"{w_ns}lvlText")
            lt_val = lt.attrib.get(f"{w_ns}val", "") if lt is not None else ""
            if lt_val in ("\uf0b7", "o", "\uf0a7", "•"):
                issues.append(f"Danh sách bullet vẫn dùng ký hiệu tròn/ô '{repr(lt_val)}' trong word/numbering.xml.")
            rf = lvl.find(f"{w_ns}rPr/{w_ns}rFonts")
            if rf is not None:
                for attr in ("ascii", "hAnsi"):
                    fval = rf.attrib.get(f"{w_ns}{attr}", "")
                    if fval in ("Symbol", "Courier New", "Wingdings"):
                        issues.append(
                            f"Danh sách trong word/numbering.xml vẫn dùng phông ký hiệu '{fval}'."
                        )

    if len(media_files) != 11:
        issues.append(
            f"Số tệp ảnh trong word/media/ là {len(media_files)} (kỳ vọng 11: 9 hình báo cáo + khung bìa + logo CTUT)."
        )
    if len(omath_nodes) < 100:
        issues.append(f"Số công thức OMML <m:oMath> quá thấp: {len(omath_nodes)} (kỳ vọng > 100).")

    upd_el = settings_xml.find(f".//{w_ns}updateFields")
    if upd_el is None or upd_el.attrib.get(f"{w_ns}val") != "true":
        issues.append("Thiếu cờ <w:updateFields w:val='true'/> trong word/settings.xml.")

    # 2. Kiểm tra 3 Section, khổ A4, lề chuẩn (2.0/2.0/3.0/2.0 cm), khung bìa behindDoc và đánh số trang
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
                abs(sec.top_margin.cm - 2.0) > 0.05
                or abs(sec.bottom_margin.cm - 2.0) > 0.05
                or abs(sec.left_margin.cm - 3.0) > 0.05
                or abs(sec.right_margin.cm - 2.0) > 0.05
            ):
                issues.append(
                    f"Section {idx} sai lề chuẩn ML (2.0/2.0/3.0/2.0 cm): "
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

        # Kiểm tra khung bìa ở header Section 0 (behindDoc="1") và không rò sang Section 1, 2
        anchors_s0 = doc.sections[0].header._element.findall(f".//{wp_ns}anchor")
        if not any(a.get("behindDoc") == "1" for a in anchors_s0):
            issues.append("Section 0 thiếu ảnh khung viền trang bìa (behindDoc='1') trong header.")
        for idx in (1, 2):
            if doc.sections[idx].header._element.findall(f".//{wp_ns}anchor"):
                issues.append(f"Section {idx} bị rò ảnh header từ Section 0.")

    # 3. Kiểm tra phông chữ các style chính là Times New Roman (kể cả Source Code)
    for st_name in (
        "Normal",
        "Body Text",
        "First Paragraph",
        "Compact",
        "Block Text",
        "Front Title",
        "Front Heading 2",
        "Heading 1",
        "Heading 2",
        "Heading 3",
        "Caption Table",
        "Caption Figure",
        "Source Code",
    ):
        if st_name in doc.styles and doc.styles[st_name].font.name != FONT_NAME:
            issues.append(f"Style '{st_name}' dùng phông '{doc.styles[st_name].font.name}' != '{FONT_NAME}'.")

    # 4. Kiểm tra thứ tự Front Title, Heading 1 và Phụ lục (Heading 2)
    front_texts = [
        p.text.strip()
        for p in doc.paragraphs
        if p.style and p.style.name == "Front Title" and p.text.strip()
    ]
    pos_ft = -1
    for ft in EXPECTED_FRONT_TITLES:
        found = next((i for i, t in enumerate(front_texts) if i > pos_ft and t == ft), None)
        if found is None:
            issues.append(f"Thiếu hoặc sai thứ tự Front Title '{ft}'.")
        else:
            pos_ft = found

    h1_texts = [
        p.text.strip()
        for p in doc.paragraphs
        if p.style and p.style.name == "Heading 1" and p.text.strip()
    ]
    pos_h1 = -1
    for prefix in EXPECTED_MAIN_H1_PREFIXES:
        found = next((i for i, t in enumerate(h1_texts) if i > pos_h1 and t.startswith(prefix)), None)
        if found is None:
            issues.append(f"Thiếu hoặc sai thứ tự Heading 1 bắt đầu bằng '{prefix}'.")
        else:
            pos_h1 = found

    h2_texts = [
        p.text.strip()
        for p in doc.paragraphs
        if p.style and p.style.name == "Heading 2" and p.text.strip()
    ]
    for app_prefix in EXPECTED_APPENDIX_H2_PREFIXES:
        if not any(t.startswith(app_prefix) for t in h2_texts):
            issues.append(f"Thiếu Heading 2 phụ lục bắt đầu bằng '{app_prefix}'.")

    # 5. Quét toàn bộ <w:p> và <w:tbl> trong body
    report_dir = repo_root / "docs" / "thesis" / "report"
    exp_tables: list[str] = []
    exp_figures: list[str] = []
    for ch_path in sorted(report_dir.glob("chuong-*.md")):
        tbls, figs = extract_captions(ch_path.read_text(encoding="utf-8"))
        exp_tables.extend(tid for tid, _, _ in tbls)
        exp_figures.extend(fid for fid, _, _ in figs)

    body_el = doc_xml.find(f"{w_ns}body")
    assert body_el is not None
    body_children = list(body_el)
    top_level_ps = set(body_el.findall(f"{w_ns}p"))

    # Kiểm tra chuẩn Booktabs cho mọi bảng dữ liệu (sau trang bìa)
    data_table_idx = 0
    for el in body_children:
        if el.tag == f"{w_ns}tbl":
            tbl_pr = el.find(f"{w_ns}tblPr")
            tbl_ind = tbl_pr.find(f"{w_ns}tblInd") if tbl_pr is not None else None
            if tbl_ind is not None and tbl_ind.attrib.get(f"{w_ns}w") == "1389":
                continue  # Bảng sinh viên không viền trên bìa chính/phụ
            data_table_idx += 1
            issues.extend(_verify_booktabs_table(el, data_table_idx, w_ns))
    stats["data_tables"] = data_table_idx

    # Kiểm tra caption Bảng/Hình (phong cách + dấu `:`), vị trí kề bảng/ảnh, phông run, chuỗi cấm và `$`
    in_main = False
    found_tbl_caps: list[str] = []
    found_fig_caps: list[str] = []
    main_words = 0

    for idx_child, el in enumerate(body_children):
        if el.tag == f"{w_ns}p":
            p_style_el = el.find(f"{w_ns}pPr/{w_ns}pStyle")
            p_style_id = p_style_el.attrib.get(f"{w_ns}val", "") if p_style_el is not None else ""
            p_style_canon = style_id_to_canon.get(p_style_id, p_style_id.lower())
            txt = _paragraph_text_xml(el).strip()
            if p_style_canon in ("heading 1", "heading1") and txt.startswith("CHƯƠNG 1."):
                in_main = True
            if in_main:
                main_words += len(re.findall(r"\S+", txt))

                if m_t := re.match(r"^Bảng\s+([A-D0-9]+\.\d+)\s*(:)\s*", txt):
                    if p_style_canon not in ("caption table", "captiontable"):
                        issues.append(
                            f"Caption 'Bảng {m_t.group(1)}:' sai style ('{p_style_canon}' != 'caption table')."
                        )
                    found_tbl_caps.append(m_t.group(1))
                    next_el = body_children[idx_child + 1] if idx_child + 1 < len(body_children) else None
                    if next_el is None or next_el.tag != f"{w_ns}tbl":
                        issues.append(f"Caption 'Bảng {m_t.group(1)}:' không đứng ngay trước bảng dữ liệu.")
                elif m_f := re.match(r"^Hình\s+([A-D0-9]+\.\d+)\s*(:)\s*", txt):
                    if p_style_canon not in ("caption figure", "captionfigure"):
                        issues.append(
                            f"Caption 'Hình {m_f.group(1)}:' sai style ('{p_style_canon}' != 'caption figure')."
                        )
                    found_fig_caps.append(m_f.group(1))
                    prev_el = body_children[idx_child - 1] if idx_child > 0 else None
                    has_img = prev_el is not None and bool(prev_el.findall(f".//{w_ns}drawing"))
                    if not has_img:
                        issues.append(f"Caption 'Hình {m_f.group(1)}:' không đứng ngay sau đoạn chứa ảnh.")
        elif in_main:
            for p_sub in el.iter(f"{w_ns}p"):
                main_words += len(re.findall(r"\S+", _paragraph_text_xml(p_sub).strip()))

    for p_el in body_el.iter(f"{w_ns}p"):
        txt = _paragraph_text_xml(p_el).strip()
        for bad in FORBIDDEN_STRINGS:
            if bad in txt:
                issues.append(f"Phát hiện chuỗi cấm '{bad}' trong đoạn: '{txt[:80]}'.")

        p_style_el = p_el.find(f"{w_ns}pPr/{w_ns}pStyle")
        p_style_id = p_style_el.attrib.get(f"{w_ns}val", "") if p_style_el is not None else ""
        p_style_canon = style_id_to_canon.get(p_style_id, p_style_id.lower())
        if p_style_canon not in ("source code", "sourcecode") and "$" in txt and "$PORT" not in txt:
            issues.append(f"Phát hiện ký tự '$' có thể chưa biên dịch toán học: '{txt[:90]}'.")

        # Kiểm tra mọi run ngoài <m:oMath> đều mang Times New Roman (nếu có rFonts tường minh)
        for child in p_el:
            if child.tag != f"{w_ns}r":
                continue
            rf = child.find(f"{w_ns}rPr/{w_ns}rFonts")
            if rf is not None:
                asc = rf.attrib.get(f"{w_ns}ascii")
                if asc and asc != FONT_NAME:
                    issues.append(f"Phát hiện run mang phông '{asc}' != '{FONT_NAME}' tại đoạn '{txt[:60]}'.")
                    break

    stats["body_tables"] = len(found_tbl_caps)
    stats["body_figures"] = len(found_fig_caps)

    if found_tbl_caps != exp_tables:
        issues.append(
            f"Danh sách Bảng (đúng chuẩn 'Bảng X.Y:') trong DOCX ({len(found_tbl_caps)}) không khớp nguồn Markdown ({len(exp_tables)})."
        )
    if found_fig_caps != exp_figures:
        issues.append(
            f"Danh sách Hình (đúng chuẩn 'Hình X.Y:') trong DOCX ({len(found_fig_caps)}) không khớp nguồn Markdown ({len(exp_figures)})."
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
