import json
from pathlib import Path


DEFAULT_DB = {
    "next_id": 1,
    "books": []
}


def load_db(db_path: str) -> dict:
    path = Path(db_path)
    if path.exists():
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
        if all(key in data for key in ("next_id", "books")):
            return data
        return DEFAULT_DB.copy()

    save_db(db_path, DEFAULT_DB)
    return DEFAULT_DB.copy()


def save_db(db_path: str, data: dict) -> None:
    path = Path(db_path)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
