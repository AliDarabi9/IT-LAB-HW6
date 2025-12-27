from typing import List, Optional
from .models import Book
from .storage import load_db, save_db


class Library:
    def __init__(self, db_path: str = "books.json"):
        self.db_path = db_path
        self._db = load_db(self.db_path)

    def _persist(self) -> None:
        save_db(self.db_path, self._db)

    def list_books(self) -> List[Book]:
        return [Book(**b) for b in self._db["books"]]

    def add_book(self, title: str, author: str, year: int) -> Book:
        title = title.strip()
        author = author.strip()

        if not title:
            raise ValueError("Title cannot be empty.")
        if not author:
            raise ValueError("Author cannot be empty.")
        if year < 0:
            raise ValueError("Year must be a positive integer.")

        new_id = int(self._db["next_id"])
        book = Book(id=new_id, title=title, author=author, year=int(year))
        self._db["books"].append(book.to_dict())
        self._db["next_id"] = new_id + 1
        self._persist()
        return book

    def delete_book_by_id(self, book_id: int) -> bool:
        before = len(self._db["books"])
        self._db["books"] = [b for b in self._db["books"] if int(b["id"]) != int(book_id)]
        after = len(self._db["books"])
        if after != before:
            self._persist()
            return True
        return False

    def delete_book_by_title(self, title: str) -> int:
        title = title.strip().lower()
        before = len(self._db["books"])
        self._db["books"] = [b for b in self._db["books"] if b["title"].strip().lower() != title]
        deleted = before - len(self._db["books"])
        if deleted > 0:
            self._persist()
        return deleted

    def search(self, query: str) -> List[Book]:
        q = query.strip().lower()
        if not q:
            return self.list_books()

        results = []
        for b in self._db["books"]:
            title = b["title"].strip().lower()
            author = b["author"].strip().lower()
            if q in title or q in author:
                results.append(Book(**b))
        return results

    def get_book(self, book_id: int) -> Optional[Book]:
        for b in self._db["books"]:
            if int(b["id"]) == int(book_id):
                return Book(**b)
        return None
