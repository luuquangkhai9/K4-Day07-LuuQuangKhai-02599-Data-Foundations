"""Markdown section chunking with a soft character target and source metadata."""

from copy import deepcopy
import re

from .models import Document


class HeadingSectionChunker:
    """Keep heading ancestry and split sections at paragraph/sentence boundaries.

    chunk_size includes the repeated headings. It is a soft target: an indivisible
    sentence, table row (with header), or fenced code block may exceed it.
    Input is Markdown content without YAML front matter. ATX headings (# ...)
    and pipe tables are supported; this is not a complete Markdown parser.
    """

    def __init__(self, chunk_size: int = 800) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        self.chunk_size = chunk_size

    def _sections(self, text):
        headings = []
        body = []
        fence = None
        for line in text.splitlines():
            marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
            if fence:
                body.append(line)
                if re.fullmatch(r"\s{0,3}" + re.escape(fence[0]) +
                                "{" + str(len(fence)) + r",}\s*", line):
                    fence = None
                continue
            if marker:
                fence = marker[1]
                body.append(line)
                continue
            match = re.match(r"^\s{0,3}(#{1,6})\s+(.+?)\s*$", line)
            if match:
                if any(part.strip() for part in body):
                    yield headings[:], "\n".join(body).strip()
                body = []
                level = len(match[1])
                while headings and headings[-1][0] >= level:
                    headings.pop()
                title = re.sub(r"\s+#+\s*$", "", match[2])
                headings.append((level, title))
            else:
                body.append(line)
        if any(part.strip() for part in body):
            yield headings[:], "\n".join(body).strip()

    @staticmethod
    def _blocks(body):
        # Fences are atomic even when they contain blank lines or fake headings.
        lines = body.splitlines()
        i = 0
        while i < len(lines):
            if not lines[i].strip():
                i += 1
                continue
            start = i
            fence = re.match(r"^\s{0,3}(`{3,}|~{3,})", lines[i])
            i += 1
            if fence:
                while i < len(lines):
                    closed = re.fullmatch(r"\s{0,3}" + re.escape(fence[1][0]) +
                                          "{" + str(len(fence[1])) + r",}\s*", lines[i])
                    i += 1
                    if closed:
                        break
            else:
                while i < len(lines) and lines[i].strip():
                    i += 1
            yield "\n".join(lines[start:i]), bool(fence)

    def _pieces(self, body, budget):
        for block, fenced in self._blocks(body):
            lines = block.splitlines()
            cells = lines[1].strip().strip("|").split("|") if len(lines) > 1 else []
            table = (lines[0].lstrip().startswith("|") and cells and
                     all(re.fullmatch(r"\s*:?-{3,}:?\s*", cell) for cell in cells))
            if table:
                header = "\n".join(lines[:2])
                current = header
                for row in lines[2:]:
                    if current != header and len(current) + len(row) + 1 > budget:
                        yield current
                        current = header
                    current += "\n" + row
                yield current
            elif fenced or len(block) <= budget:
                yield block
            else:
                # Keep numbering such as 7.1 intact; split only after sentence
                # punctuation followed by whitespace. Long sentences stay whole.
                yield from (part for part in re.split(r"(?<=[.!?])\s+", block) if part)

    def _chunks(self, text):
        for headings, body in self._sections(text):
            prefix = "\n".join("#" * level + " " + title for level, title in headings)
            budget = max(1, self.chunk_size - len(prefix) - (2 if prefix else 0))
            pending = ""
            for piece in self._pieces(body, budget):
                if pending and len(pending) + len(piece) + 2 > budget:
                    yield (prefix + "\n\n" + pending if prefix else pending), headings
                    pending = ""
                pending = pending + "\n\n" + piece if pending else piece
            if pending:
                yield (prefix + "\n\n" + pending if prefix else pending), headings

    def chunk(self, text: str) -> list[str]:
        return [content for content, _ in self._chunks(text)]

    def chunk_document(self, document: Document) -> list[Document]:
        """Inherit metadata, preserving parent doc_id for filtering/deletion."""
        chunks = []
        for index, (content, headings) in enumerate(self._chunks(document.content)):
            metadata = deepcopy(document.metadata)
            metadata.setdefault("doc_id", document.id)
            metadata.update(section_path=" > ".join(title for _, title in headings),
                            chunk_index=index, chunk_strategy="heading_section",
                            exceeds_target=len(content) > self.chunk_size)
            chunks.append(Document(id=f"{document.id}:heading:{index}",
                                   content=content, metadata=metadata))
        return chunks
