"""Split the saved Shopee article 77251 by audience, without fetching the web."""

import csv
import json
import re
import zipfile
from pathlib import Path

from normalize_return_refund import norm, parse


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/return-refund-policy"
REPORT = ROOT / "report/data-normalization"
SELECTIONS = {
    "buyer": [1, 2, 3, 4, 6, 8, 9, 10, 11, 12],
    "seller": [1, 2, 3, 4, 5, 7, 9, 10, 11, 12],
}


def render(lines):
    result = []
    for line in lines:
        if re.match(r"^\d+\.\s", line):
            line = "## " + line
        elif re.match(r"^\d+\.\d+\.?\s", line):
            # Short subsection names become headings; actual clauses stay prose.
            if len(line) < 140 and not line.endswith("."):
                line = "### " + line
        elif re.match(r"^(?:[a-c]|i{1,3}|iv|v|vi)\.\s", line):
            line = "- " + line
        result.append(line)
    body = "\n\n".join(result) + "\n"
    restored = [re.sub(r"^(?:#{2,3} |- )", "", line)
                for line in body.splitlines() if line.strip()]
    assert restored == lines, "Clause text or order changed"
    return body


def main():
    originals = list(DATA.glob("77251-*.md"))
    assert len(originals) == 1, "Expected exactly one original article 77251"
    original = originals[0]
    metadata, body = parse(original.read_text(encoding="utf-8"))
    lines = [norm(line) for line in body.splitlines() if line.strip()]
    assert lines[2] == "Xin chào, Shopee có thể giúp gì cho bạn?"
    assert lines[-3:] == ["Bạn có hài lòng với bài viết này?", "Hài lòng", "Không hài lòng"]
    lines = lines[4:-3]
    sections = {}
    for line in lines:
        match = re.match(r"^(\d+)\.\s", line)
        if match:
            number = int(match[1])
            assert number not in sections
            sections[number] = []
        sections[number].append(line)
    assert list(sections) == list(range(1, 13))
    assert "có hiệu lực kể từ ngày 11/3/2026" in sections[12][-1]
    with (DATA / "sources.csv").open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    source = next(row for row in rows if row["doc_id"] == metadata["doc_id"])
    remaining = [row for row in rows if row["doc_id"] != metadata["doc_id"]]
    plans = []
    for audience, selected in SELECTIONS.items():
        suffix = "nguoi-mua" if audience == "buyer" else "nguoi-ban"
        label = "Người Mua" if audience == "buyer" else "Người Bán"
        doc_id = "shopee-chinh-sach-tra-hang-" + suffix
        target = DATA / (doc_id + ".md")
        assert not target.exists()
        title = "Chính sách Trả hàng và Hoàn tiền — " + label
        info = dict(metadata, doc_id=doc_id, title=title, audience=audience,
                    document_version="2026-03-11", category="returns-policy", language="vi",
                    source_article_id="77251", source_sections=", ".join(map(str, selected)))
        excerpt = [line for number in selected for line in sections[number]]
        front = "---\n" + "\n".join(k + ": " + json.dumps(v, ensure_ascii=False)
                                       for k, v in info.items()) + "\n---\n\n"
        text = front + "# " + title + "\n\n" + render(excerpt)
        row = dict(source, doc_id=doc_id, title=title, document_version="2026-03-11",
                   file_path=target.relative_to(ROOT).as_posix())
        plans.append((target, text, row))
    REPORT.mkdir(parents=True, exist_ok=True)
    backup = REPORT / "shopee-77251-original.zip"
    with zipfile.ZipFile(backup, "x", zipfile.ZIP_DEFLATED) as archive:
        for path in (original, DATA / "sources.csv"):
            archive.write(path, path.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(backup) as archive:
        assert archive.testzip() is None
        for path in (original, DATA / "sources.csv"):
            assert archive.read(path.relative_to(ROOT).as_posix()) == path.read_bytes()
    for target, text, row in plans:
        target.write_text(text, encoding="utf-8", newline="\n")
        remaining.append(row)
    with (DATA / "sources.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(source), lineterminator="\n")
        writer.writeheader()
        writer.writerows(sorted(remaining, key=lambda row: row["doc_id"]))
    assert original.resolve().parent == DATA.resolve()
    original.unlink()
    print("Split 77251 into buyer/seller, preserving selected clauses exactly; backed up original and CSV.")


if __name__ == "__main__":
    main()
