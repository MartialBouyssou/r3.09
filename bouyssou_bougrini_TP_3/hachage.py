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
    (/ ! \ Généré à l'IA)
    """
    if not isinstance(car, str):
        raise TypeError("Le carac doit être un string")

    if len(car) != 1:
        raise ValueError("Un UNIQUE carac doit ê passé en.")

    if not car.isascii() or not (car.isalpha() or car in "!#()*+/?"):
        raise ValueError("Le carac n'est pas pris en charge par le service que vous utilisez actuellement.")

    return ord(car)