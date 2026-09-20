"""Reproducible retrieval benchmark using the group's agreed five questions."""
import csv
import hashlib
import json
import os
from pathlib import Path
import sys
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
from src import Document, EmbeddingStore, HeadingSectionChunker, MockEmbedder
from src import LocalEmbedder, OpenAIEmbedder, GeminiEmbedder


def main():
    load_dotenv(ROOT / ".env", override=False)
    provider = os.getenv("EMBEDDING_PROVIDER", "mock").strip().lower()
    if provider == "mock":
        embedder = MockEmbedder()
    elif provider == "local":
        embedder = LocalEmbedder()
    elif provider == "openai":
        embedder = OpenAIEmbedder(os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))
    elif provider == "gemini":
        embedder = GeminiEmbedder(os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001"))
    else:
        raise ValueError("Unknown EMBEDDING_PROVIDER")
    # Deliberately do not silently fall back after an API failure.
    report_path = ROOT / "report/REPORT_NHOM (1).md"
    report = report_path.read_text(encoding="utf-8-sig")
    query_section = report.split("### Câu hỏi đánh giá & Câu trả lời chuẩn", 1)[1]
    query_section = query_section.split("### Tổng hợp", 1)[0]
    queries = []
    for line in query_section.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == 4 and cells[0] in {"1", "2", "3", "4", "5"}:
            number = int(cells[0])
            audience = "buyer" if number in (1, 4) else "seller"
            queries.append(dict(number=number, question=cells[1], gold_answer=cells[2],
                                metadata_filter=None if number == 5 else {"audience": audience}))
    assert len(queries) == 5
    corpus = []
    all_chunks = []
    with (ROOT / "data/return-refund-policy/sources.csv").open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        path = ROOT / row["file_path"]
        raw = path.read_text(encoding="utf-8-sig")
        _, front, body = raw.split("---", 2)
        meta = {k: json.loads(v.strip()) for k, v in
                (line.split(":", 1) for line in front.strip().splitlines())}
        chunks = HeadingSectionChunker(800).chunk_document(Document(meta["doc_id"], body.strip(), meta))
        all_chunks.extend(chunks)
        corpus.append(dict(file=row["file_path"], sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                           chunks=len(chunks)))
    if provider == "gemini":
        cache_dir = ROOT / "report/benchmark-heading/cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        texts = list(dict.fromkeys([c.content for c in all_chunks] + [q["question"] for q in queries]))
        vectors = {}
        def cache_path(text):
            return cache_dir / (hashlib.sha256((embedder.model_name + "\0" + text).encode()).hexdigest() + ".json")
        missing = []
        for text in texts:
            path = cache_path(text)
            if path.exists():
                vectors[text] = json.loads(path.read_text(encoding="utf-8"))
            else:
                missing.append(text)
        for start in range(0, len(missing), 20):
            batch = missing[start:start + 20]
            for attempt in range(4):
                try:
                    response = embedder.client.models.embed_content(model=embedder.model_name, contents=batch)
                    break
                except Exception as exc:
                    code = getattr(exc, "code", None)
                    if code not in (429, 500, 503) or attempt == 3:
                        raise RuntimeError(f"Gemini embedding failed: {type(exc).__name__}, status={code}") from None
                    print(f"Gemini status={code}; retry in 30 seconds", flush=True)
                    time.sleep(30)
            assert len(response.embeddings) == len(batch)
            for text, embedding in zip(batch, response.embeddings):
                vector = list(embedding.values)
                vectors[text] = vector
                cache_path(text).write_text(json.dumps(vector), encoding="utf-8")
            print(f"Gemini embedded {min(start + 20, len(missing))}/{len(missing)} new texts", flush=True)
        embedding_fn = vectors.__getitem__
    else:
        embedding_fn = embedder
    store = EmbeddingStore("heading_benchmark", embedding_fn)
    store.add_documents(all_chunks)
    results = []
    for query in queries:
        filtered = store.search_with_filter(query["question"], 3, query["metadata_filter"])
        unfiltered = store.search(query["question"], 3)
        results.append(dict(**query, top3=filtered, unfiltered_top3=unfiltered,
                            agent_answer=None, rubric_score=None))
    output = ROOT / "report/benchmark-heading"
    output.mkdir(exist_ok=True)
    payload = dict(created_at=datetime.now(timezone.utc).isoformat(), provider=provider,
                   backend=embedder._backend_name, python=sys.version,
                   strategy="HeadingSectionChunker", chunk_size_target=800, top_k=3,
                   total_chunks=store.get_collection_size(), corpus=corpus,
                   group_report_sha256=hashlib.sha256(report_path.read_bytes()).hexdigest(),
                   generation_status="not_run_no_llm_configured", results=results)
    (output / "results.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Benchmark Heading/Section", "", f"Backend: `{provider}` / `{embedder._backend_name}`.",
             f"Corpus: {len(corpus)} tài liệu, {store.get_collection_size()} chunk; mục tiêu 800 ký tự, top-k=3.",
             "", "Chưa chạy LLM sinh câu trả lời; chưa chấm điểm /10. Gold answer được sao chép nguyên văn từ bản nhóm, chưa tự sửa.",
             "Các hash nguồn, cấu hình và top-3 không lọc để đối chiếu nằm trong `results.json`.", ""]
    for result in results:
        lines += [f"## Q{result['number']}: {result['question']}", "",
                  f"Filter: `{json.dumps(result['metadata_filter'])}`", "",
                  f"Gold theo nhóm: {result['gold_answer']}", ""]
        for rank, hit in enumerate(result["top3"], 1):
            lines += [f"### Top {rank} — score {hit['score']:.6f}", "",
                      f"ID: `{hit['id']}`; audience: `{hit['metadata']['audience']}`", "",
                      "````text", hit["content"], "````", ""]
    (output / "retrieval.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Completed {len(results)} queries; {len(corpus)} documents; {store.get_collection_size()} chunks; backend={provider}")


if __name__ == "__main__":
    main()
