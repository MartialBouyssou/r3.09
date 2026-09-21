ASCII_MAX: int = 127
ASCII_CHAR_COUNT = 128
ASCII_ESCAPES_KEYS_COUNT = 32
MENU_CHOICE_ENCODE = "1"
MENU_CHOICE_EXIT = "exit"


def display_menu() -> None:
    print("Type :\n - 1 to encode a message using vigenere;\n - exit to leave")


def encode_message() -> None:
    brut_text: str = input("Text to encode: ")
    key: str = input("Key: ")
    print(f"Encoded text: {vigenere_cipher(brut_text, key)}")

def generate_vigenere_key(starter_key: str, brut_text_length: int) -> str :
    """
    starter_key : string => generate a vigenere key that as the same length as brut_text_length -- MUST not be empty
    brut_text_length: int => the length of the text to encode
    return string your vigenere key 
    """
    if not starter_key:
        raise ValueError("The key cannot be empty")
    
    missing_letters: int = brut_text_length - len(starter_key)
    key: str = starter_key 

    if missing_letters < 0:
        key = starter_key[:brut_text_length]
    else:
        for i in range(missing_letters):
            key += starter_key[i % len(starter_key)]

    return key


def vigenere_cipher(brut_text: str, key: str) -> str :
    """
    brut_text : string => your text to encode, all letters must be upper cased letters
    key : string => key to encode the brut_text, all letters must be upper cased letters
    return string your encoded text with vigenere cipher  
    """
    vigenere_key: str = generate_vigenere_key(key, len(brut_text))
    encoded_text: str = ""

    for i in range(len(brut_text)): 
        encoded_letter_code: int = (ord(brut_text[i]) + ord(vigenere_key[i]))
        if encoded_letter_code > ASCII_MAX:
            encoded_letter_code -= ASCII_CHAR_COUNT
            encoded_letter_code +=  ASCII_ESCAPES_KEYS_COUNT
        
        encoded_text += chr(encoded_letter_code)

    return encoded_text

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


    