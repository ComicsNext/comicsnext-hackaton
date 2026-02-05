import os
from typing import Tuple

import faiss
import numpy as np


def build_faiss_index(embeddings_path: str, index_path: str) -> None:
    """
    Crea un índice FAISS (L2) y lo guarda en disco.
    """
    emb = np.load(embeddings_path).astype("float32")
    dim = emb.shape[1]

    index = faiss.IndexFlatL2(dim)  # simple y estable
    index.add(emb)

    faiss.write_index(index, index_path)


def load_faiss_index(index_path: str):
    return faiss.read_index(index_path)


def ensure_index(base_dir: str) -> Tuple[str, str]:
    """
    Devuelve rutas (embeddings.npy, index.faiss) y crea el índice si no existe.
    """
    embeddings_path = os.path.join(base_dir, "embeddings.npy")
    index_path = os.path.join(base_dir, "index.faiss")

    if not os.path.exists(index_path):
        build_faiss_index(embeddings_path, index_path)

    return embeddings_path, index_path


if __name__ == "__main__":
    here = os.path.dirname(__file__)
    base = os.path.join(here, "vectorstore")
    _, idx = ensure_index(base)
    print(f"OK index creado/cargado en: {idx}")
