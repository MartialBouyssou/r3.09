import string

import hachage

alphabet_min = [hachage.hachage_car(chr(i)) for i in range(97, 123)]



def recherche_collision(Lcaractères: list) -> list:
    """Recherche les collisions dans l'alphabet minuscule.

    Returns:
        Une liste de tuples contenant les paires de caractères qui ont le même hachage.
    """
    collisions = []
    for i in range(len(Lcaractères)):
        for j in range(i + 1, len(Lcaractères)):
            if Lcaractères[i] == Lcaractères[j]:
                collisions.append((chr(i + 97), chr(j + 97)))
    return collisions

def rechercheprimage(hachage_recherche: int) -> list:
    """Recherche les préimages d'un hachage donné.

    Args:
        hachage_recherche: Le hachage pour lequel on souhaite trouver les préimages.

    Returns:
        Une liste de caractères dont le hachage correspond à hachage_recherche.
    """
    preimages = []
    for car in string.ascii_lowercase:
        if hachage.hachage_car(car) == hachage_recherche:
            preimages.append(car)
    return preimages

print("Collisions dans l'alphabet minuscule :", recherche_collision(alphabet_min))
print("Préimages du hachage 42 :", rechercheprimage(42))