ASCII_MAX: int = 127
ASCII_CHAR_COUNT = 128
ASCII_ESCAPES_KEYS_COUNT = 32

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

if __name__ == "__main__" :
    print("Bienvenu dans le programme BOUBOU !")
    print(vigenere_cipher("Lorem ipsum sit amet", "ZAEDQS;C;"))
    print(vigenere_cipher("Lorem ipsum sit amet", "ZaAEDn QS;C;"))
    print(vigenere_cipher("Lorem ipsum sit amet", "Hatim Bougrini & Martial Bouyssou ont réaliser ce programme"))

    