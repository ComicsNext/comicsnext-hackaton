import json
import os

from .build_corpus_wiki import build_corpus, _read_pages
from .embeddings import build_embeddings
from .vector_store import ensure_index


if __name__ == "__main__":
    here = os.path.dirname(__file__)

    # 1) Generar corpus.json desde Wikipedia API
    pages_path = os.path.join(here, "data", "wiki_pages.txt")
    corpus_path = os.path.join(here, "data", "corpus.json")

    pages = _read_pages(pages_path)
    corpus = build_corpus(pages)

    with open(corpus_path, "w", encoding="utf-8") as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)

    print(f"OK: corpus.json regenerado ({len(corpus)} docs)")

    # 2) Generar embeddings.npy + meta.json
    out_dir = build_embeddings()
    print("OK: embeddings regenerados")

    # 3) Crear/actualizar índice FAISS
    ensure_index(out_dir)
    print("OK: índice FAISS regenerado")
