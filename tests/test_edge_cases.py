import unittest

from src import Document, EmbeddingStore, KnowledgeBaseAgent
from src.chunking import RecursiveChunker, SentenceChunker, compute_similarity


class TestEdgeCases(unittest.TestCase):
    def test_recursive_preserves_text_and_bounds_with_missing_separators(self):
        text = "Điều 1.\n\n" + "abcdefghij" * 20 + "\nĐiều 2. Kết thúc."
        for separators in (None, [], ["\n\n"], [". ", ""]):
            chunks = RecursiveChunker(separators=separators, chunk_size=17).chunk(text)
            self.assertEqual("".join(chunks), text)
            self.assertTrue(all(0 < len(chunk) <= 17 for chunk in chunks))

    def test_sentence_empty_and_punctuation(self):
        self.assertEqual(SentenceChunker().chunk(" \n "), [])
        self.assertEqual(SentenceChunker(2).chunk("Một.\nHai! Ba?"), ["Một. Hai!", "Ba?"])

    def test_cosine_checks_dimensions_and_ignores_magnitude(self):
        self.assertAlmostEqual(compute_similarity([3, 4], [30, 40]), 1)
        with self.assertRaises(ValueError):
            compute_similarity([1, 2], [1])

    def test_prefilter_and_delete_all_parent_chunks(self):
        vectors = {"q": [1, 0], "buyer": [10, 0], "seller": [0, 1]}
        store = EmbeddingStore(embedding_fn=vectors.__getitem__)
        store.add_documents([
            Document("b", "buyer", {"audience": "buyer"}),
            Document("s1", "seller", {"audience": "seller", "doc_id": "policy"}),
            Document("s2", "seller", {"audience": "seller", "doc_id": "policy"}),
        ])
        self.assertEqual(store.search("q", 1)[0]["id"], "b")
        result = store.search_with_filter("q", 1, {"audience": "seller"})
        self.assertEqual(result[0]["metadata"]["doc_id"], "policy")
        self.assertEqual(store.search("q", 0), [])
        self.assertTrue(store.delete_document("policy"))
        self.assertEqual(store.get_collection_size(), 1)
        self.assertFalse(store.delete_document("policy"))

    def test_agent_prompt_uses_only_filtered_context(self):
        store = EmbeddingStore(embedding_fn=lambda _: [1, 0])
        store.add_documents([
            Document("b", "BUYER_EVIDENCE", {"audience": "buyer"}),
            Document("s", "SELLER_EVIDENCE", {"audience": "seller"}),
        ])
        agent = KnowledgeBaseAgent(store, lambda prompt: prompt)
        prompt = agent.answer("Question?", metadata_filter={"audience": "seller"})
        self.assertIn("SELLER_EVIDENCE", prompt)
        self.assertNotIn("BUYER_EVIDENCE", prompt)
        self.assertIn("Question?", prompt)
        self.assertIn("[1]", prompt)


if __name__ == "__main__":
    unittest.main()
