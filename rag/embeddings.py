import json
import os
from typing import Any, Dict, List

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

EMBED_MODEL = "text-embedding-3-small"


def _load_corpus() -> List[Dict[str, Any]]:
    here = os.path.dirname(__file__)
    path = os.path.join(here, "data", "corpus.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def build_embeddings(out_dir: str = None, batch_size: int = 32) -> str:
    """
    Genera embeddings para cada doc del corpus y guarda:
      - embeddings.npy (NxD)
      - meta.json (lista con comic_id, title, source, text_preview)
    Devuelve la ruta del directorio de salida.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta OPENAI_API_KEY en rag/.env")

    client = OpenAI(api_key=api_key)

    here = os.path.dirname(__file__)
    out_dir = out_dir or os.path.join(here, "vectorstore")
    _ensure_dir(out_dir)

    corpus = _load_corpus()

    texts = []
    meta = []
    for d in corpus:
        text = f"{d.get('title','')}\n{d.get('text','')}".strip()
        texts.append(text)
        meta.append({
            "comic_id": d.get("comic_id"),
            "title": d.get("title", ""),
            "source": d.get("source", ""),
            "text_preview": (d.get("text", "")[:200] + "...") if d.get("text") else ""
        })

    vectors = []
    for i in range(0, len(texts), batch_size):
        chunk = texts[i:i + batch_size]
        resp = client.embeddings.create(model=EMBED_MODEL, input=chunk)
        vectors.extend([item.embedding for item in resp.data])

    emb = np.array(vectors, dtype=np.float32)

    npy_path = os.path.join(out_dir, "embeddings.npy")
    meta_path = os.path.join(out_dir, "meta.json")

    np.save(npy_path, emb)
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    return out_dir


if __name__ == "__main__":
    out = build_embeddings()
    print(f"OK embeddings guardados en: {out}")
