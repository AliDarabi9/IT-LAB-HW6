from .library import Library
from .utils import prompt_int, prompt_nonempty


def print_books(books):
    if not books:
        print("\nNo books found.\n")
        return
    print("\nBooks:")
    for b in books:
        print(f"- [#{b.id}] {b.title} | {b.author} | {b.year}")
    print("")


def main():
    lib = Library(db_path="books.json")

    while True:
        print("==== Mini Library App ====")
        print("1) List books")
        print("2) Add book")
        print("3) Delete book (by ID)")
        print("4) Delete book (by Title)")
        print("5) Search")
        print("0) Exit")

        choice = input("Select: ").strip()

        if choice == "1":
            print_books(lib.list_books())

        elif choice == "2":
            title = prompt_nonempty("Title: ")
            author = prompt_nonempty("Author: ")
            year = prompt_int("Year: ")
            book = lib.add_book(title, author, year)
            print(f"\nAdded: [#{book.id}] {book.title}\n")

        elif choice == "3":
            book_id = prompt_int("Book ID to delete: ")
            ok = lib.delete_book_by_id(book_id)
            print("\nDeleted.\n" if ok else "\nNo book with that ID.\n")

        elif choice == "4":
            title = prompt_nonempty("Exact Title to delete: ")
            count = lib.delete_book_by_title(title)
            print(f"\nDeleted {count} book(s).\n" if count else "\nNo match.\n")

        elif choice == "5":
            q = input("Search query (title/author): ").strip()
            results = lib.search(q)
            print_books(results)

        elif choice == "0":
            print("Bye!")
            break

        else:
            print("\nInvalid option.\n")


if __name__ == "__main__":
    main()
