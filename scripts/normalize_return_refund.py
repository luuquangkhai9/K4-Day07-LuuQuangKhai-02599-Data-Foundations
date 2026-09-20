"""Normalize the reviewed 2026-09-20 crawl; preserve a byte-for-byte ZIP backup.

Run once with Python 3.11 from any directory. No network requests are made.
This is specific to this crawl, not a general HTML/Markdown cleaner.
"""

import csv
import io
import json
import re
import unicodedata
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/return-refund-policy"
REPORT = ROOT / "report/data-normalization"
NAMES = {
    "164831": "kiem-tra-tien-hoan-spaylater",
    "188931": "quy-dinh-chung-tra-hang-hoan-tien",
    "189473": "thoi-gian-va-cach-kiem-tra-tien-hoan",
    "189476": "cach-theo-doi-van-chuyen-hang-hoan-tra",
    "189477": "phuong-thuc-va-phi-tra-hang",
    "190242": "quy-trinh-xu-ly-tra-hang",
    "190387": "tra-loi-de-xuat-hoan-tien-ngay",
    "204305": "tra-hang-doi-y",
    "79233": "huong-dan-gui-yeu-cau-tra-hang",
    "79258": "cam-nang-tra-hang-hoan-tien",
    "79298": "theo-doi-tinh-trang-tra-hang",
    "79465": "san-pham-han-che-tra-hang",
    "79467": "huong-dan-chuan-bi-bang-chung",
    "79508": "cach-dong-goi-don-hang-hoan-tra",
}
HEADINGS = {
    "Thời gian xử lý", "Kết quả xử lý", "Thời gian hoàn tiền",
    "Trường hợp Trả lại & Hoàn tiền", "Các bước đóng gói hàng hoàn trả:",
    "Chuẩn bị:", "Đóng hàng:", "Viết mã vận đơn lên hộp hàng:",
    "Cách kiểm tra mã vận đơn và thời hạn trả hàng:", "Hàng cồng kềnh là gì?",
    "Gửi yêu cầu", "Xử lý yêu cầu", "Trả hàng", "Hoàn tiền",
    "Sức khỏe, Vệ sinh & Đồ cá nhân", "Thực phẩm & Hàng mau hỏng",
    "Hàng đặc thù trong vận chuyển", "Sản phẩm số và dịch vụ", "Khác",
    "Thiết bị Điện tử & Công nghệ", "Nhóm ngành hàng Thời trang",
    "Nhóm ngành hàng Tiêu dùng nhanh", "Nhóm ngành hàng Đời sống",
    "Nhóm ngành hàng Thiết bị điện tử):", "Ví dụ:",
    "ĐƠN CÓ TRẠNG THÁI “ĐÃ HOÀN THÀNH”",
}


def norm(text):
    return unicodedata.normalize("NFC", " ".join(text.split()))


def parse(text):
    _, front, body = text.split("---", 2)
    # The crawler writes JSON-quoted scalar strings, which are valid YAML.
    metadata = {k: json.loads(v.strip()) for k, v in
                (line.split(":", 1) for line in front.strip().splitlines())}
    return metadata, body


def table(headers, rows):
    def row(cells):
        return "| " + " | ".join(c.replace("|", "\\|") for c in cells) + " |"
    return "\n".join([row(headers), row(["---"] * len(headers)),
                      *(row(cells) for cells in rows)])


def restore_tables(lines, article):
    # Reconstruct only unambiguous row/cell sequences in the saved crawl.
    if article == "188931":
        start = lines.index("Lý do")
        end = next(i for i, line in enumerate(lines) if line.startswith("2. Quy định chung"))
        cells = lines[start + 3:end]
        assert len(cells) == 43
        rows = [cells[i:i + 3] for i in range(0, 36, 3)]
        rows.append([cells[36], cells[37], "<br>".join(cells[38:])])
        lines[start:end] = [table(lines[start:start + 3], rows)]
        start = lines.index("Trường hợp")
        end = lines.index("⚠️ Lưu ý:", start)
        cells = lines[start + 4:end]
        assert len(cells) == 17
        rows = [
            [cells[0], cells[1], "<br>".join(cells[2:4]), "<br>".join(cells[4:6])],
            ["", *cells[6:9]],
            [cells[9], cells[10], cells[11], "<br>".join(cells[12:14])],
            ["", *cells[14:17]],
        ]
        lines[start:end] = [table(lines[start:start + 4], rows)]
    elif article == "79508":
        start = lines.index("Hộp vận chuyển")
        assert lines[start + 1] == "Hộp nhà sản xuất"
        cells = lines[start + 2:start + 6]
        assert all(cell.startswith("· ") for cell in cells)
        lines[start:start + 6] = [table(lines[start:start + 2],
                                      [["<br>".join(cells[:2]), "<br>".join(cells[2:])]])]
    elif article == "79467":
        start = lines.index("Loại bằng chứng")
        cells = lines[start + 2:start + 8]
        lines[start:start + 8] = [table(lines[start:start + 2],
                                      [cells[i:i + 2] for i in range(0, 6, 2)])]
    elif article == "190242":
        start = lines.index("Lý do khiếu nại")
        end = lines.index("Sản phẩm hoàn trả phải còn nguyên seal, tem, hộp sản phẩm")
        cells = lines[start + 9:end]
        assert len(cells) == 56
        headers = [lines[start], *lines[start + 3:start + 9], lines[start + 2]]
        rows = [cells[i:i + 7] + [""] for i in range(0, 56, 7)]
        rows[-1][-1] = lines[end]
        lines[start:end + 1] = [lines[start + 1], table(headers, rows)]
        start = lines.index("Các trường hợp không mong muốn")
        cells = lines[start + 2:start + 8]
        lines[start:start + 8] = [table(lines[start:start + 2],
                                      [cells[i:i + 2] for i in range(0, 6, 2)])]
    elif article == "189473":
        start = lines.index("Phương thức thanh toán")
        end = next(i for i, line in enumerate(lines) if line.startswith("Bảng 1:"))
        cells = lines[start:end]
        assert len(cells) == 36
        rows = [
            [cells[3], cells[4], " ".join(cells[5:8])],
            ["", cells[8], cells[9]],
            cells[10:13],
            [cells[13], cells[14], " ".join(cells[15:18])],
            cells[18:21], cells[21:24], cells[24:27], cells[27:30],
            [cells[30], "<br>".join(cells[31:35]), cells[35]],
        ]
        # Empty first cell continues the same payment method, as in the crawl.
        lines[start:end] = [table(cells[:3], rows)]
    return lines


def fingerprint(text):
    """Compare ordered content, ignoring only the Markdown added by this script."""
    text = text.replace("<br>", " ")
    return re.findall(r"\w+|✔", unicodedata.normalize("NFC", text))


def clean(body, metadata, article):
    lines = [norm(line) for line in body.splitlines() if line.strip()]
    full_title = norm(metadata["title"])
    source_title = full_title.split(" | Shopee Trung tâm trợ giúp")[0]
    assert lines[:4] == ["# " + full_title, full_title,
                         "Xin chào, Shopee có thể giúp gì cho bạn?", source_title]
    assert lines[-3:] == ["Bạn có hài lòng với bài viết này?", "Hài lòng", "Không hài lòng"]
    lines = lines[4:-3]
    lines = [line for line in lines if not re.fullmatch(r"[0-9a-f]{32}\.(mov|mp4)", line)]
    if article == "189476":
        assert lines[-3:] == ["1", "1", "1"]
        lines = lines[:-3]
    # Join detached bullet markers with their existing text.
    joined = []
    pending_bullet = False
    for line in lines:
        if line == "·":
            pending_bullet = True
            continue
        joined.append(("· " if pending_bullet else "") + line)
        pending_bullet = False
    assert not pending_bullet
    before = "\n".join(joined)
    lines = restore_tables(joined[:], article)
    formatted = []
    for line in lines:
        if line.startswith("| "):
            formatted.append(line)
        elif re.match(r"^\d+\.\d+\.?\s", line):
            formatted.append("### " + line)
        elif re.match(r"^\d+[./]\s", line):
            formatted.append("## " + line)
        elif re.match(r"^(Cách \d|Trường hợp [12AB]|Câu \d)", line) or line in HEADINGS:
            formatted.append("### " + line)
        elif re.fullmatch(r"(?:⚠️\s*|\*)?Lưu ý:", line):
            formatted.append("### " + line)
        elif re.match(r"^Bước \d+:", line):
            formatted.append("- " + line)
        elif re.match(r"^[·•+]\s+", line):
            formatted.append(re.sub(r"^[·•+]\s+", "- ", line))
        else:
            formatted.append(line)
    content = "\n\n".join(formatted)
    # Tables move headers/notes into cells but must preserve every content token.
    from collections import Counter
    assert Counter(fingerprint(before)) == Counter(fingerprint(content)), article
    if article not in {"190242", "189473"}:
        assert fingerprint(before) == fingerprint(content), article
    title = re.sub(r"^\[Trả hàng/\s*Hoàn tiền\]\s*", "", source_title)
    return title, "# " + title + "\n\n" + content + "\n"


def main():
    originals = sorted(DATA.glob("*.md"))
    if {p.name.split("-", 1)[0] for p in originals} != set(NAMES):
        raise SystemExit("Expected the 14 original crawl files; already normalized or changed. No files written.")
    with (DATA / "sources.csv").open(encoding="utf-8-sig", newline="") as stream:
        sources = list(csv.DictReader(stream))
    assert len(sources) == 14
    by_id = {row["doc_id"]: row for row in sources}
    assert len(by_id) == 14
    plans = []
    mapping = []
    for original in originals:
        metadata, body = parse(original.read_text(encoding="utf-8"))
        article = original.name.split("-", 1)[0]
        title, content = clean(body, metadata, article)
        new_id = "shopee-" + NAMES[article]
        target = DATA / (new_id + ".md")
        assert not target.exists()
        row = by_id[metadata["doc_id"]].copy()
        for key in ("title", "source_url", "retrieved_at", "document_version"):
            assert row[key] == metadata[key]
        metadata.update(doc_id=new_id, title=title, audience="buyer",
                        category="returns-policy", language="vi")
        if article == "79258":
            metadata["document_type"] = "navigation-index"
        front = "---\n" + "\n".join(k + ": " + json.dumps(v, ensure_ascii=False)
                                       for k, v in metadata.items()) + "\n---\n\n"
        row.update(doc_id=new_id, title=title, file_path=target.relative_to(ROOT).as_posix())
        plans.append((original, target, front + content, row))
        mapping.append({"article_id": article, "old_file": original.name,
                        "new_file": target.name, "old_doc_id": original.stem,
                        "new_doc_id": new_id})
    REPORT.mkdir(parents=True, exist_ok=True)
    backup = REPORT / "return-refund-policy-original.zip"
    # Exclusive creation: never overwrite the only raw backup.
    with zipfile.ZipFile(backup, "x", zipfile.ZIP_DEFLATED) as archive:
        for path in [*originals, DATA / "sources.csv"]:
            archive.write(path, path.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(backup) as archive:
        assert archive.testzip() is None
        for path in [*originals, DATA / "sources.csv"]:
            assert archive.read(path.relative_to(ROOT).as_posix()) == path.read_bytes()
    for original, target, text, _ in plans:
        target.write_text(text, encoding="utf-8", newline="\n")
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(sources[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(plan[3] for plan in plans)
    (DATA / "sources.csv").write_text(buffer.getvalue(), encoding="utf-8", newline="\n")
    (REPORT / "filename-map.json").write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + "\n",
                                             encoding="utf-8")
    # Delete only the exact original files inside DATA after backup verification.
    for original, _, _, _ in plans:
        assert original.resolve().parent == DATA.resolve()
        original.unlink()
    for _, target, _, row in plans:
        metadata, body = parse(target.read_text(encoding="utf-8"))
        assert metadata["doc_id"] == target.stem == row["doc_id"]
        assert metadata["audience"] == "buyer" and body.strip()
        assert "Xin chào, Shopee" not in body
        assert "Bạn có hài lòng với bài viết này?" not in body
    print("Normalized and verified 14 documents, 14 CSV rows, original ZIP and filename mapping.")


if __name__ == "__main__":
    main()
