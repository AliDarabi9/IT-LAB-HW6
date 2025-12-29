import json
from pathlib import Path


DEFAULT_DB = {
    "next_id": 1,
    "books": []
}


def load_db(db_path: str) -> dict:
    path = Path(db_path)

    if not path.exists():
        save_db(db_path, DEFAULT_DB.copy())
        return DEFAULT_DB.copy()

    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)

    if not all(k in data for k in ("next_id", "books")):
        return DEFAULT_DB.copy()

    return data


def save_db(db_path: str, data: dict) -> None:
    path = Path(db_path)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
