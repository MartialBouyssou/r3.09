def hachage_car(car: str) -> int:
    """Retourne l'encodage UTF-8 sur un octet du caractère fourni.

    Args:
        car: Une lettre majuscule, une lettre minuscule ou un caractère
             spécial parmi !, #, (, ), *, +, / et ?.

    Returns:
        La valeur numérique de l'octet UTF-8 du caractère.

    Raises:
        TypeError: Si car n'est pas une chaîne de caractères.
        ValueError: Si car n'est pas un caractère autorisé ou si son
                    encodage UTF-8 nécessite plusieurs octets.
    (/ ! \ Documentation généré à l'IA)
    """
    if not isinstance(car, str):
        raise TypeError("Le carac doit être un string")

    if len(car) != 1:
        raise ValueError("Un UNIQUE carac doit ê passé en.")

    if not car.isascii() or not (car.isalpha() or car in "!#()*+/?"):
        raise ValueError("Le carac n'est pas pris en charge par le service que vous utilisez actuellement.")

    return ord(car)

def hachage_etoile(texte: str) -> int:
    """Calcule le hachage d'un texte par XOR des hachages de ses caractères.

    Args:
        texte: Texte composé de lettres ASCII et des caractères spéciaux autorisés.

    Returns:
        Le hachage du texte sous la forme d'un entier compris entre 0 et 255.

    Raises:
        TypeError: Si texte n'est pas une chaîne de caractères.
        ValueError: Si le texte contient un caractère non autorisé.
    (/ ! \ Documentation généré à l'IA)
    """
    if not isinstance(texte, str):
        raise TypeError("Le txt doit ê une chaine de carac!!!")

    resultat = 0

    for car in texte:
        resultat ^= hachage_car(car)

    return resultat