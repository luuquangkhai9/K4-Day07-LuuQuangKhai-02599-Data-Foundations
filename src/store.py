from __future__ import annotations

from typing import Any, Callable
from copy import deepcopy
from uuid import uuid4

from .chunking import compute_similarity
from .embeddings import _mock_embed
from .models import Document


class EmbeddingStore:
    """
    A vector store for text chunks.

    Tries to use ChromaDB if available; falls back to an in-memory store.
    The embedding_fn parameter allows injection of mock embeddings for tests.
    """

    def __init__(
        self,
        collection_name: str = "documents",
        embedding_fn: Callable[[str], list[float]] | None = None,
    ) -> None:
        self._embedding_fn = embedding_fn or _mock_embed
        self._collection_name = collection_name
        self._use_chroma = False
        self._store: list[dict[str, Any]] = []
        self._collection = None
        self._next_index = 0

        try:
            import chromadb  # noqa: F401

            self._client = chromadb.EphemeralClient()
            # Chroma clients can share state; each store owns a fresh collection.
            self._collection = self._client.create_collection(
                name=f"{collection_name}-{uuid4().hex}", embedding_function=None
            )
            self._use_chroma = True
        except Exception:
            self._use_chroma = False
            self._collection = None

    def _make_record(self, doc: Document) -> dict[str, Any]:
        metadata = deepcopy(doc.metadata)
        metadata.setdefault("doc_id", doc.id)
        record = {"id": doc.id, "content": doc.content, "metadata": metadata,
                  "embedding": list(self._embedding_fn(doc.content)),
                  "storage_id": str(self._next_index)}
        self._next_index += 1
        return record

    def _search_records(self, query: str, records: list[dict[str, Any]], top_k: int) -> list[dict[str, Any]]:
        if top_k <= 0 or not records:
            return []
        query_embedding = self._embedding_fn(query)
        results = [{"id": record["id"], "content": record["content"],
                    "metadata": deepcopy(record["metadata"]),
                    "score": compute_similarity(query_embedding, record["embedding"])}
                   for record in records]
        return sorted(results, key=lambda result: result["score"], reverse=True)[:top_k]

    def add_documents(self, docs: list[Document]) -> None:
        """
        Embed each document's content and store it.

        For ChromaDB: use collection.add(ids=[...], documents=[...], embeddings=[...])
        For in-memory: append dicts to self._store
        """
        records = [self._make_record(doc) for doc in docs]
        if not records:
            return
        dimensions = {len(record["embedding"]) for record in self._store + records}
        if len(dimensions) != 1 or 0 in dimensions:
            raise ValueError("Embeddings must have the same nonzero dimension")
        if self._use_chroma:
            # Keep full arbitrary metadata in memory; Chroma accepts scalar fields.
            self._collection.add(
                ids=[record["storage_id"] for record in records],
                documents=[record["content"] for record in records],
                embeddings=[record["embedding"] for record in records],
                metadatas=[{"doc_id": str(record["metadata"]["doc_id"])} for record in records],
            )
        self._store.extend(records)

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """
        Find the top_k most similar documents to query.

        Use exact cosine ranking over the in-memory records in both backends.
        Chroma is an optional storage mirror; scores and metadata stay consistent.
        """
        return self._search_records(query, self._store, top_k)

    def get_collection_size(self) -> int:
        """Return the total number of stored chunks."""
        return len(self._store)

    def search_with_filter(self, query: str, top_k: int = 3, metadata_filter: dict = None) -> list[dict]:
        """
        Search with optional metadata pre-filtering.

        First filter stored chunks by metadata_filter, then run similarity search.
        """
        filters = metadata_filter or {}
        records = [record for record in self._store
                   if all(key in record["metadata"] and record["metadata"][key] == value
                          for key, value in filters.items())]
        return self._search_records(query, records, top_k)

    def delete_document(self, doc_id: str) -> bool:
        """
        Remove all chunks belonging to a document.

        Returns True if any chunks were removed, False otherwise.
        """
        matching = [record for record in self._store if record["metadata"]["doc_id"] == doc_id]
        if not matching:
            return False
        if self._use_chroma:
            self._collection.delete(ids=[record["storage_id"] for record in matching])
        self._store = [record for record in self._store if record["metadata"]["doc_id"] != doc_id]
        return True
