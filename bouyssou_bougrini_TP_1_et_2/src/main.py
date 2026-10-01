from math import gcd
from pathlib import Path

ASCII_PRINTABLE_START = 32
ASCII_PRINTABLE_END = 126
ASCII_PRINTABLE_RANGE = ASCII_PRINTABLE_END - ASCII_PRINTABLE_START + 1
MENU_CHOICE_ENCODE = "1"
MENU_CHOICE_DECODE = "2"
MENU_CHOICE_KASISKI = "3"
MENU_CHOICE_EXIT = "exit"
MIN_FRAGMENT_LENGTH = 4


def display_menu() -> None:
    print("Type :\n - 1 to encode a message using Vigenere;\n"
    " - 2 to decode a message using Vigenere;\n - 3 to find key lenght with Kasiski \n - exit to leave")

def display_repetitions(repetitions: list[tuple[str, int]]) -> None:
    if not repetitions:
        print("Aucune répétition trouvée.")
        return

    print("\nRépétitions trouvées :")

    for fragment, distance in repetitions:
        print(f'"{fragment}" -> distance : {distance}')

def find_repetitions(text: str) -> list[tuple[str, int]]:
    repetitions = []

    for length in range(len(text), MIN_FRAGMENT_LENGTH - 1, -1):
        fragments = {}

        for i in range(len(text) - length + 1):
            fragment = text[i:i + length]

            if fragment not in fragments:
                fragments[fragment] = []

            fragments[fragment].append(i)

        for fragment, positions in fragments.items():
            if len(positions) < 2:
                continue

            for i in range(len(positions)):
                for j in range(i + 1, len(positions)):
                    distance = positions[j] - positions[i]
                    repetitions.append((fragment, distance))

    return repetitions


def get_divisors(number: int) -> list[int]:
    divisors = []

    for i in range(2, number + 1):
        if number % i == 0:
            divisors.append(i)

    return divisors

def find_key_sizes(repetitions: list[tuple[str, int]]) -> list[int]:
    if not repetitions:
        return []

    candidates = get_divisors(repetitions[0][1])

    for _, distance in repetitions[1:]:
        temp = []

        for candidate in candidates:
            value = gcd(candidate, distance)

            if value != 1:
                temp.append(value)

        if temp:
            candidates = list(dict.fromkeys(temp))

    return candidates

def kasiski(text: str) -> tuple[list[tuple[str, int]], list[int]]:
    repetitions = find_repetitions(text)
    candidates = find_key_sizes(repetitions)

    return repetitions, candidates

def encode_message() -> None:
    brut_text: str = input("Text to encode: ")
    key: str = input("Key: ")

    try:
        cipher_text = vigenere_cipher(brut_text, key)
        print(f"Encoded text: {cipher_text}")
    except ValueError as error:
        print(f"Error: {error}")

def decode_message() -> None:
    cipher_text: str = input("Text to decode: ")
    key: str = input("Key: ")

    try:
        decoded_text = vigenere_decipher(cipher_text, key)
        print(f"Decoded text: {decoded_text}")
    except ValueError as error:
        print(f"Error: {error}")


def is_printable_ascii(value: str) -> bool:
    return all(ASCII_PRINTABLE_START <= ord(character) <= ASCII_PRINTABLE_END for character in value)

def ensure_printable_ascii(value: str, label: str) -> None:
    if not value:
        raise ValueError(f"{label} cannot be empty")

    if not is_printable_ascii(value):
        raise ValueError(f"{label} must contain only printable ASCII characters")

def generate_vigenere_key(starter_key: str, brut_text_length: int) -> str:
    ensure_printable_ascii(starter_key, "The key")

    repeats: int = (brut_text_length + len(starter_key) - 1) // len(starter_key)
    return (starter_key * repeats)[:brut_text_length]

def vigenere_cipher(brut_text: str, key: str) -> str:
    ensure_printable_ascii(brut_text, "The text")
    ensure_printable_ascii(key, "The key")

    vigenere_key: str = generate_vigenere_key(key, len(brut_text))
    encoded_text: str = ""

    for i in range(len(brut_text)):
        encoded_letter_code: int = (
            ord(brut_text[i]) - ASCII_PRINTABLE_START
            + ord(vigenere_key[i]) - ASCII_PRINTABLE_START
        ) % ASCII_PRINTABLE_RANGE

        encoded_text += chr(ASCII_PRINTABLE_START + encoded_letter_code)

    return encoded_text

def vigenere_decipher(cipher_text: str, key: str) -> str:
    ensure_printable_ascii(cipher_text, "The text")
    ensure_printable_ascii(key, "The key")

    vigenere_key: str = generate_vigenere_key(key, len(cipher_text))
    decoded_text: str = ""

    for i in range(len(cipher_text)):
        decoded_letter_code: int = (
            ord(cipher_text[i]) - ASCII_PRINTABLE_START
            - (ord(vigenere_key[i]) - ASCII_PRINTABLE_START)
        ) % ASCII_PRINTABLE_RANGE

        decoded_text += chr(ASCII_PRINTABLE_START + decoded_letter_code)

    return decoded_text

def kasiski_menu_manager() -> None:
    filename = input("Nom du fichier contenant le texte chiffré : ").strip()
    project_root = Path(__file__).parent.parent
    file_path = project_root / "resources" / filename
    print(file_path)

    try:
        text = file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print("Fichier introuvable.")
        return
    except OSError as error:
        print(f"Erreur lors de la lecture du fichier : {error}")
        return

    repetitions, candidates = kasiski(text)

    display_repetitions(repetitions)

    print("\nTailles de clé possibles :")

    if candidates:
        print(candidates)
    else:
        print("Error?")

if __name__ == "__main__":
    print("Welcome !")

    is_leaving: bool = False
    while not is_leaving:
        display_menu()
        client_input: str = input("What do you want to do ? ").strip().lower()

        if client_input == MENU_CHOICE_EXIT:
            print("Bye !")
            is_leaving = True
        elif client_input == MENU_CHOICE_ENCODE:
            encode_message()
        elif client_input == MENU_CHOICE_DECODE:
            decode_message()
        elif client_input == MENU_CHOICE_KASISKI:
            kasiski_menu_manager()
        else:
            print("Invalid choice. Please type 1, 2 or exit.")
