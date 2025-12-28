def prompt_int(message: str) -> int:
    while True:
        raw = input(message).strip()
        try:
            return int(raw)
        except ValueError:
            print("Please enter a valid integer.")


def prompt_nonempty(message: str) -> str:
    while True:
        raw = input(message).strip()
        if raw:
            return raw
        print("Input cannot be empty.")
