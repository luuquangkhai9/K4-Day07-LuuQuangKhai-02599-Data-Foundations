import unittest

from src import Document, HeadingSectionChunker


class TestHeadingSectionChunker(unittest.TestCase):
    def test_siblings_do_not_inherit_each_other(self):
        chunks = HeadingSectionChunker().chunk_document(Document(
            "policy", "# Policy\n## Buyer\nBuyer rule.\n## Seller\nSeller rule.",
            {"audience": "seller", "source_url": "example"}))
        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[1].metadata["section_path"], "Policy > Seller")
        self.assertNotIn("Buyer", chunks[1].content)
        self.assertEqual(chunks[1].metadata["doc_id"], "policy")
        self.assertEqual(chunks[1].metadata["audience"], "seller")

    def test_repeated_headings_and_soft_limit(self):
        chunker = HeadingSectionChunker(50)
        chunks = chunker.chunk("# Policy\n## Rules\n" + "A sentence here. " * 12)
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(c.startswith("# Policy\n## Rules\n") for c in chunks))
        self.assertTrue(all(len(c) <= 50 for c in chunks))
        long = chunker.chunk_document(Document("p", "# Rule\n" + "a" * 100))
        self.assertTrue(long[0].metadata["exceeds_target"])

    def test_table_headers_repeated_and_rows_preserved(self):
        header = "| Item | Rule |\n| --- | --- |"
        rows = [f"| {i} | rule {i} |" for i in range(8)]
        chunks = HeadingSectionChunker(85).chunk("# Policy\n" + header + "\n" + "\n".join(rows))
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(header in chunk for chunk in chunks))
        for row in rows:
            self.assertEqual(sum(chunk.count(row) for chunk in chunks), 1)

    def test_fences_empty_sections_and_plain_text(self):
        chunker = HeadingSectionChunker(30)
        self.assertEqual(chunker.chunk("# Empty\n\n"), [])
        self.assertEqual(chunker.chunk("plain text"), ["plain text"])
        code = "```md\n# Not a heading\n\nexample\n```"
        chunks = chunker.chunk("# Root\n" + code)
        self.assertEqual(chunks, ["# Root\n\n" + code])

    def test_metadata_is_not_mutated(self):
        doc = Document("p", "# Rule\nContent", {"doc_id": "parent", "tags": ["a"]})
        chunk = HeadingSectionChunker().chunk_document(doc)[0]
        chunk.metadata["tags"].append("b")
        self.assertEqual(doc.metadata, {"doc_id": "parent", "tags": ["a"]})
        self.assertEqual(chunk.metadata["doc_id"], "parent")
        with self.assertRaises(ValueError):
            HeadingSectionChunker(0)
