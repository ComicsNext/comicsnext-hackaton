import json
import os
from .retriever import retrieve_top_k
from typing import Any, Dict, List
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI
import re

load_dotenv()
DEBUG = False

def _load_corpus() -> List[Dict[str, Any]]:
    """
    Carga el corpus externo desde disco y lo devuelve como lista de documentos
    """
    here = os.path.dirname(__file__)
    path = os.path.join(here, "data", "corpus.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _keyword_retrieve(corpus: List[Dict[str, Any]], query: str, k: int = 8) -> List[Dict[str, Any]]:
    """
    Retrieval MVP: Convierte el perfil del usuario en una query
    Busca coincidencias simples de palabras
    Devuelve los documentos más relevantes
    busca coincidencias de palabras (simple, explicable).
    Luego lo sustituiremos por embeddings + FAISS + similitud de coseno
    """
    q = query.lower()
    tokens = [t for t in q.replace(",", " ").replace(".", " ").split() if len(t) > 2]

    scored: List[tuple[int, Dict[str, Any]]] = []
    for doc in corpus:
        text = " ".join([
            str(doc.get("title", "")),
            " ".join(doc.get("genres", [])),
            str(doc.get("text", ""))
        ]).lower()

        score = sum(1 for t in tokens if t in text)
        if score > 0:
            scored.append((score, doc))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [d for _, d in scored[:k]]

def _extract_json(text: str) -> str:
    """
    Extrae el primer JSON array [...] o JSON object {...} aunque venga envuelto en ```json ... ```.
    """
    if not text:
        raise ValueError("Respuesta vacía del modelo.")

    cleaned = text.strip().replace("```json", "").replace("```", "").strip()

    # Primero intenta array
    m = re.search(r"\[.*\]", cleaned, re.DOTALL)
    if m:
        return m.group(0)

    # Si no, intenta objeto
    m = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if m:
        return m.group(0)

    raise ValueError(f"No se encontró JSON en la respuesta: {cleaned[:200]}")


def rag_recommend(user_profile: Dict[str, Any],  candidates: List[Dict[str, Any]], top_k: int = 5,  history: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    
    #Comprueba que hay apikey, si no para
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta OPENAI_API_KEY en rag/.env")

    #crea el cliente de openai
    client = OpenAI(api_key=api_key)

    #crafa el corpus externo
    corpus = _load_corpus()

    #construye un query a partir del usuario
    likes = user_profile.get("likes", [])
    dislikes = user_profile.get("dislikes", [])
    query = f"likes: {likes} dislikes: {dislikes} history: {history or []}"

    #selecciona que documentos van al prompt
    # Retrieval con embeddings + FAISS
    retrieved_meta = retrieve_top_k(query, k=8)

    # Convertimos meta -> docs del corpus (para mantener el mismo formato de CONTEXTO)
    id_set = set(m["comic_id"] for m in retrieved_meta)
    retrieved = [d for d in corpus if d.get("comic_id") in id_set]

    if not retrieved:
        retrieved = corpus[:8]  # fallback
        
    #Construccion del contexto que se inyecta al LLM
    context = "\n\n".join(
        [f"[comic_id={d['comic_id']}] {d.get('title','')} | genres={d.get('genres', [])}\n{d.get('text','')}"
         for d in retrieved]
    )

    
      
    # IDs permitidos (candidates)
   
    allowed_ids = [c.get("comic_id") for c in candidates if c.get("comic_id") is not None]
    allowed_ids = [int(x) for x in allowed_ids]

    # (Opcional pero recomendado) candidates “ligeros” para meterlos al prompt
    slim_candidates = []
    for c in candidates:
        if c.get("comic_id") is None:
            continue
        slim_candidates.append({
            "comic_id": int(c["comic_id"]),
            "title": c.get("title", ""),
            "genres": c.get("genres", []),
            "synopsis": (c.get("synopsis", "") or "")[:400],
        })
    
    
#Prompt
    prompt = f"""
Eres un recomendador de cómics.
Tienes un CONTEXTO externo (ayuda) y una lista de CANDIDATES (los únicos cómics que puedes recomendar).
Tu tarea es devolver EXACTAMENTE JSON válido.

Reglas:
- Devuelve SOLO JSON. Sin texto extra.
- Devuelve EXACTAMENTE {top_k} recomendaciones (o menos si el contexto no da para más).
- Usa SOLO comic_id presentes en CANDIDATES.
- Cada item: comic_id (int), score (0..1), reason (1-2 frases, en español).
- reason debe mencionar por qué encaja con likes/dislikes/historial.

Entrada:
user_profile={user_profile}
history={history}

CONTEXTO:
{context}

CANDIDATES (los únicos válidos):
{json.dumps(slim_candidates, ensure_ascii=False)}

Formato esperado (JSON array):
[
  {{ "comic_id": 1, "score": 0.91, "reason": "..." }}
]
"""
#llamada al modelo de openAI con el prompt
    resp = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    text = (resp.output_text or "").strip()
    
    if DEBUG:
        print("\n--- RAW OUTPUT ---\n", repr(text), "\n------------------\n")

    #Parseo para extraer JSON aunque venga ```
    json_text = _extract_json(text)
    data = json.loads(json_text)


    recs = data if isinstance(data, list) else data.get("recommendations", [])
    recs = recs[:top_k]

    allowed_set = set(allowed_ids)
    
    clean_recs = []
    for r in recs:
        try:
            comic_id = int(r.get("comic_id"))
            if comic_id not in allowed_set:
                continue
            
            score = float(r.get("score", 0.0))
            score = max(0.0, min(1.0, score))
            reason = str(r.get("reason", "")).strip()
            if reason:
                clean_recs.append({"comic_id": comic_id, "score": score, "reason": reason})
        except Exception:
            continue

    #Cortar a top_k y limpiar resultado
    recs = clean_recs


    return recs


