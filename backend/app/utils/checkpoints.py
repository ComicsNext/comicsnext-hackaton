import json
import os
from datetime import datetime, timezone
from typing import Any, Dict


def _safe_filename(name: str) -> str:
    keep = []
    for ch in name:
        if ch.isalnum() or ch in ("-", "_"):
            keep.append(ch)
        else:
            keep.append("_")
    return "".join(keep)


def save_checkpoint(
    kind: str,
    payload: Dict[str, Any],
    base_dir: str = "checkpoints",
) -> str:
    """
    Guarda un JSON por llamada para debug/demo.
    Devuelve la ruta del archivo creado.
    """
    os.makedirs(base_dir, exist_ok=True)

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    filename = f"{_safe_filename(kind)}_{ts}.json"
    path = os.path.join(base_dir, filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    return path