import json
import os
import re
from typing import List, Dict, Any

import requests
from tqdm import tqdm


WIKI_SUMMARY_API = "https://en.wikipedia.org/api/rest_v1/page/summary/{title}"


def _read_pages(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        pages = []
        for line in f:
            t = line.strip()
            if t and not t.startswith("#"):
                pages.append(t)
        return pages


def _guess_genres(text: str) -> List[str]:
    """
    Heurística muy simple para demo ( mejorarla luego).
    """
    t = text.lower()
    genres = set()
    keywords = {
        "noir": ["noir", "crime", "detective"],
        "superhero": ["superhero", "batman", "marvel", "dc comics"],
        "fantasy": ["fantasy", "myth", "dream"],
        "horror": ["horror", "zombie", "terror"],
        "sci-fi": ["science fiction", "sci-fi", "space"],
        "historical": ["holocaust", "war", "historical"],
        "comedy": ["comedy", "humor", "funny"],
        "drama": ["drama", "family", "relationships"],
    }
    for g, kws in keywords.items():
        if any(k in t for k in kws):
            genres.add(g)
    return sorted(genres)


def _clean_text(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    return s


def fetch_summary(title: str) -> Dict[str, Any]:
    url = WIKI_SUMMARY_API.format(title=title)
    r = requests.get(url, headers={"User-Agent": "ComicsNextHackathon/1.0"})
    if r.status_code != 200:
        raise RuntimeError(f"Wikipedia API error {r.status_code} for {title}: {r.text[:200]}")
    return r.json()


def build_corpus(pages: List[str]) -> List[Dict[str, Any]]:
    corpus = []
    comic_id = 1

    for title in tqdm(pages, desc="Fetching Wikipedia summaries"):
        data = fetch_summary(title)

        page_title = data.get("title") or title
        extract = data.get("extract") or ""
        extract = _clean_text(extract)

        if not extract:
            continue

        doc = {
            "comic_id": comic_id,  # IMPORTANTE: aquí estamos generando IDs "internos" para demo
            "title": page_title,
            "genres": _guess_genres(extract),
            "text": extract,
            "source": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
        }
        corpus.append(doc)
        comic_id += 1

    return corpus


if __name__ == "__main__":
    here = os.path.dirname(__file__)
    pages_path = os.path.join(here, "data", "wiki_pages.txt")
    out_path = os.path.join(here, "data", "corpus.json")

    pages = _read_pages(pages_path)
    corpus = build_corpus(pages)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)

    print(f"OK: generado {out_path} con {len(corpus)} docs")
