import string
from collections import Counter
import hachage

alphabet_min = [hachage.hachage_car(chr(i)) for i in range(97, 123)]



def recherche_collision(Lcaractères: list) -> list:
    """Recherche les collisions dans l'alphabet minuscule.

    Returns:
        Une liste de tuples contenant les paires de caractères qui ont le même hachage.
    """
    collisions = [] # la liste des collisions trouvées
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



nombre_egalites = 0
nombre_vraies_collisions = 0
total = 0

for car1 in alphabet_min:
    for car2 in alphabet_min:
        total += 1

        if hachage.hachage_car(car1) == hachage.hachage_car(car2):
            nombre_egalites += 1

            if car1 != car2:
                nombre_vraies_collisions += 1

print("Probabilité même hachage :", nombre_egalites / total) # en admettant qu'on peut piocher 2 fois la meme lettre
print("Probabilité vraie collision :", nombre_vraies_collisions / total)


def charger_mots(nom_fichier: str) -> list[str]:
    with open(nom_fichier, encoding="utf-8") as fichier:
        return [mot.strip() for mot in fichier if mot.strip()]


def probabilites_hachage(mots: list[str]) -> None:
    hachages = [hachage.hachage_etoile(mot) for mot in mots]
    compteurs = Counter(hachages) # Compte le nombre d'occurrences de chaque hachage

    nombre_mots = len(mots)

    # Pour chaque hachage, nombre / nombre_mots est la probabilité
    # qu'un mot choisi au hasard possède ce hachage.
    # On met cette probabilité au carré car on choisit deux mots :
    # les deux doivent avoir le même hachage.
    # On additionne ensuite le résultat pour tous les hachages.
    probabilite_egale = sum(
        (nombre / nombre_mots) ** 2 for nombre in compteurs.values()
    )

    # On cherche ici une vraie collision : les deux textes doivent être
    # différents, mais avoir le même hachage.
    if nombre_mots >= 2:
        # nombre * (nombre - 1) compte les couples ordonnés de textes
        # différents qui possèdent cette même valeur de hachage.
        # Le dénominateur compte tous les couples ordonnés de textes
        # différents possibles.
        probabilite_collision = sum(
            nombre * (nombre - 1) for nombre in compteurs.values()
        ) / (nombre_mots * (nombre_mots - 1))
    else:
        probabilite_collision = 0

    print(f"Nombre de textes : {nombre_mots}")
    print(f"Nombre de hachages différents : {len(compteurs)}")
    print(f"Probabilité d'égalité des hachages : {probabilite_egale}")
    print(f"Probabilité de vraie collision : {probabilite_collision}")

    print("\nProbabilité de préimage pour chaque hachage :")
    for valeur, nombre in sorted(compteurs.items()):
        # nombre / nombre_mots est la probabilité qu'un mot choisi
        # au hasard ait la valeur de hachage « valeur ».
        probabilite = nombre / nombre_mots
        print(f"{valeur} : {probabilite}")


mots = charger_mots("bouyssou_bougrini_TP_3//ressources//ods5.txt")
probabilites_hachage(mots)

def recherche_collision_simplifie(fichier: str) -> tuple[str, str, int] | None:
    """Cherche deux mots différents ayant le même hachage."""

    hachages = {}
    valeurs_essayees = 0

    with open(fichier, "r", encoding="utf-8") as dictionnaire:
        for ligne in dictionnaire:
            mot = ligne.strip()

            if mot.isalpha() and mot.isascii():
                variantes = {mot.lower(), mot.upper(), mot.capitalize()}

                for variante in variantes:
                    valeurs_essayees += 1
                    resultat = hachage.hachage_etoile(variante)

                    if resultat in hachages and hachages[resultat].lower() != variante.lower():
                        return hachages[resultat], variante, valeurs_essayees

                    hachages[resultat] = variante

    return None


collision = recherche_collision_simplifie("ods5.txt")

if collision is None:
    print("Aucune collision trouvée.")
else:
    mot1, mot2, essais = collision
    print(f"Collision : {mot1} et {mot2}")
    print(f"Hachage commun : {hachage.hachage_etoile(mot1)}")
    print(f"Valeurs essayées : {essais}")