import json
import os
from typing import Any, Dict, List, Tuple

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

from .vector_store import load_faiss_index, ensure_index

load_dotenv()

EMBED_MODEL = "text-embedding-3-small"


def _load_meta(meta_path: str) -> List[Dict[str, Any]]:
    with open(meta_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _embed_query(client: OpenAI, text: str) -> np.ndarray:
    resp = client.embeddings.create(model=EMBED_MODEL, input=text)
    v = np.array(resp.data[0].embedding, dtype=np.float32)
    return v


def retrieve_top_k(query: str, k: int = 5) -> List[Dict[str, Any]]:
    """
    Devuelve lista de metadatos de los docs más cercanos a la query.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta OPENAI_API_KEY en rag/.env")

    client = OpenAI(api_key=api_key)

    here = os.path.dirname(__file__)
    base_dir = os.path.join(here, "vectorstore")

    # Asegura que existe el índice
    _, index_path = ensure_index(base_dir)

    meta_path = os.path.join(base_dir, "meta.json")
    embeddings_path = os.path.join(base_dir, "embeddings.npy")

    meta = _load_meta(meta_path)
    emb = np.load(embeddings_path).astype("float32")

    index = load_faiss_index(index_path)

    qv = _embed_query(client, query).reshape(1, -1)

    # Devuelve distancias y posiciones
    distances, indices = index.search(qv, k)

    results = []
    for dist, idx in zip(distances[0].tolist(), indices[0].tolist()):
        if idx < 0:
            continue
        item = meta[idx].copy()
        item["_faiss_distance"] = dist
        results.append(item)

    return results


if __name__ == "__main__":
    demo_q = "Me gustan historias noir y oscuras, con política y dilemas morales"
    out = retrieve_top_k(demo_q, k=3)
    print(out)
