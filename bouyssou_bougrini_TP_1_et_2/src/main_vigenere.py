ASCII_PRINTABLE_START = 32
ASCII_PRINTABLE_END = 126
ASCII_PRINTABLE_RANGE = ASCII_PRINTABLE_END - ASCII_PRINTABLE_START + 1
MENU_CHOICE_ENCODE = "1"
MENU_CHOICE_EXIT = "exit"


def display_menu() -> None:
    print("Type :\n - 1 to encode a message using vigenere;\n - exit to leave")


def encode_message() -> None:
    brut_text: str = input("Text to encode: ")
    key: str = input("Key: ")

    try:
        cipher_text=vigenere_cipher(brut_text, key)
        print(f"Encoded text: {cipher_text}")
        print(f"Decoded text: {vigenere_decipher(cipher_text,key)}")
      
    except ValueError as error:
        print(f"Error: {error}")


def is_printable_ascii(value: str) -> bool:
    return all(ASCII_PRINTABLE_START <= ord(character) <= ASCII_PRINTABLE_END for character in value)


def ensure_printable_ascii(value: str, label: str) -> None:
    if not value:
        raise ValueError(f"{label} cannot be empty")

    if not is_printable_ascii(value):
        raise ValueError(f"{label} must contain only printable ASCII characters")

def generate_vigenere_key(starter_key: str, brut_text_length: int) -> str :
    """
    starter_key : string => generate a vigenere key that as the same length as brut_text_length -- MUST not be empty
    brut_text_length: int => the length of the text to encode
    return string your vigenere key 
    """
    ensure_printable_ascii(starter_key, "The key")

    repeats: int = (brut_text_length + len(starter_key) - 1) // len(starter_key)
    return (starter_key * repeats)[:brut_text_length]


def vigenere_cipher(brut_text: str, key: str) -> str :
    """
    brut_text : string => your text to encode, all letters must be upper cased letters
    key : string => key to encode the brut_text, all letters must be upper cased letters
    return string your encoded text with vigenere cipher  
    """
    ensure_printable_ascii(brut_text, "The text")
    ensure_printable_ascii(key, "The key")

    vigenere_key: str = generate_vigenere_key(key, len(brut_text))
    encoded_text: str = ""

    for i in range(len(brut_text)):
        encoded_letter_code: int = (
            ord(brut_text[i]) - ASCII_PRINTABLE_START + (ord(vigenere_key[i]) - ASCII_PRINTABLE_START)
        ) % ASCII_PRINTABLE_RANGE

        encoded_text += chr(ASCII_PRINTABLE_START + encoded_letter_code)

    return encoded_text
    
def vigenere_decipher(cipher_text: str, key: str)-> str:
    """
    cipher_text : string => your text to decode
    key : string => key to decode the cipher_text
    return string your decoded text with vigenere cipher  
    """
    ensure_printable_ascii(cipher_text, "The text")
    ensure_printable_ascii(key, "The key")

    vigenere_key: str = generate_vigenere_key(key, len(cipher_text))
    decoded_text: str = "" 

    for i in range(len(cipher_text)):
        
        decoded_letter_code: int = (
            ord(cipher_text[i]) - ASCII_PRINTABLE_START - (ord(vigenere_key[i]) - ASCII_PRINTABLE_START)
        ) % ASCII_PRINTABLE_RANGE

        decoded_text += chr(ASCII_PRINTABLE_START + decoded_letter_code)

    return decoded_text

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
        else:
            print("Invalid choice. Please type 1 or exit.")


    
