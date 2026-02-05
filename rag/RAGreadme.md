# RAG Module – ComicsNext


Módulo **RAG (Retrieval-Augmented Generation)** desacoplado para recomendaciones de cómics.  
Este módulo aporta **contexto externo** y **re-rankeo inteligente** sobre una lista de candidatos, sin depender de base de datos ni romper el flujo de IA principal.


---


## 🎯 Objetivo


- Mejorar las recomendaciones usando **información externa**
- Mantener el RAG **aislado** y fácil de integrar
- Devolver resultados **compatibles con JSON**
- No acceder a DB: solo trabaja con los **candidates** recibidos


---


## 🧩 Contrato de integración


### Función principal


```python
rag_recommend(
    user_profile: dict,
    candidates: list[dict],
    top_k: int = 5,
    history: list[dict] | None = None
) -> list[dict]
Entrada

user_profile
Información del usuario (likes, dislikes, etc.)

candidates
Lista de cómics candidatos sobre los que se debe decidir.
Cada candidato debe incluir al menos:

{
  "comic_id": 12,
  "title": "...",
  "genres": ["noir"],
  "synopsis": "..."
}

top_k
Número máximo de recomendaciones a devolver

history (opcional)
Historial de interacciones del usuario

Salida

La función devuelve una lista de recomendaciones ordenadas:

[
  {
    "comic_id": 12,
    "score": 0.91,
    "reason": "Encaja con los gustos noir y políticos del usuario."
  }
]

```
---
## 📌 Garantías

- Solo devuelve comic_id presentes en candidates

- score normalizado entre 0 y 1

- reason en texto corto y explicativo

- No se añade wrapper adicional (lista directa)

## 🧠 Qué hace internamente el RAG

Construye una query a partir de:

- user_profile

- history (si existe)

Recupera contexto externo mediante:

- Embeddings (OpenAI)

- FAISS (vector store local)

Inyecta:

- Contexto externo (como apoyo)

- Lista de candidates

- El LLM re-rankea solo los candidates

Devuelve recomendaciones limpias y filtradas

---
## ▶️ Demo / Prueba manual

Existe un script de demo para validar el contrato:
```
python -m rag.demo
```
Este script:

- Simula un usuario

- Define una lista de candidates

- Llama a rag_recommend

- Imprime la salida

---
## 🔑 Variables de entorno

Es necesario definir la API Key de OpenAI:
```
OPENAI_API_KEY=sk-...
```
El archivo .env se carga automáticamente desde el módulo rag/.
```
📦 Estructura del módulo
rag/
├── rag_pipeline.py      # Lógica principal del RAG
├── retriever.py         # Retrieval con embeddings + FAISS
├── vector_store.py      # Gestión del índice FAISS
├── demo.py              # Prueba manual del contrato
├── data/
│   └── corpus.json      # Corpus externo
├── vectorstore/
│   ├── embeddings.npy
│   ├── meta.json
│   └── index.faiss
└── __init__.py
````
---
## 🤝 Integración recomendada

Desde el servicio de IA principal:
```
from rag.rag_pipeline import rag_recommend


recs = rag_recommend(
    user_profile=user_profile,
    candidates=candidates,
    top_k=5,
    history=history
)

```
---
## ✅ Estado

✔️ Contrato cerrado

✔️ Módulo desacoplado

✔️ Demo funcional

✔️ Listo para integración


