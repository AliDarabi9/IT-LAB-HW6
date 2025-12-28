import json
from pathlib import Path


DEFAULT_DB = {
    "next_id": 1,
    "books": []
}


def load_db(db_path: str) -> dict:
    path = Path(db_path)
    if not path.exists():
        save_db(db_path, DEFAULT_DB)
        return DEFAULT_DB.copy()

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if "next_id" not in data or "books" not in data:
        return DEFAULT_DB.copy()

    return data


def save_db(db_path: str, data: dict) -> None:
    path = Path(db_path)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
