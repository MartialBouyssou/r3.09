import string
import random
from collections import Counter
from pathlib import Path
import time
import hachage

alphabet_min = [hachage.hachage_car(chr(i)) for i in range(97, 123)]

PATH = Path(__file__).parent / "ressources" / "ods5.txt"
ALPHABET = string.ascii_letters + "!#()*+/?"
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


def recherche_preimage_aleatoire(longueur: int = 4) -> tuple[int, str, int]:
    """Cherche aléatoirement un texte ayant un hachage cible."""
    texte_cible = "".join(random.choices(ALPHABET, k=longueur))
    hachage_cible = hachage.hachage_etoile(texte_cible)
    essais = 0

    while True:
        candidat = "".join(random.choices(ALPHABET, k=longueur))
        essais += 1
        if hachage.hachage_etoile(candidat) == hachage_cible:
            return hachage_cible, candidat, essais


def experimenter_preimages(
    nombre_experiences: int = 100,
    longueur: int = 4,
) -> None:
    """Répète la recherche de préimages et affiche le nombre moyen d'essais."""
    nombres_essais = [
        recherche_preimage_aleatoire(longueur)[2]
        for _ in range(nombre_experiences)
    ]
    moyenne = sum(nombres_essais) / nombre_experiences

    print("\nExpérience de recherche de préimages")
    print(f"Nombre d'expériences : {nombre_experiences}")
    print(f"Longueur des textes : {longueur}")
    print(f"Nombre d'essais par expérience : {nombres_essais}")
    print(f"Nombre moyen d'essais : {moyenne:.2f}")
    print("Nombre théorique moyen attendu : 128")
    print("Probabilité théorique par essai : 1/128")

def charger_mots(nom_fichier: str | Path) -> list[str]:
    with open(nom_fichier, encoding="utf-8") as fichier:
        return [mot.strip() for mot in fichier if mot.strip()]


def probabilites_hachage(mots: list[str]) -> None:
    if not mots:
        print("Le fichier ne contient aucun texte.")
        return

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
def recherche_collision_paires(fichier: str) -> tuple[str, str, int] | None:
    """Méthode de base : compare chaque nouveau haché à tous les précédents.

    Returns:
        (mot1, mot2, nombre de comparaisons) ou None.
    """
    vus = []
    comparaisons = 0
    with open(fichier, "r", encoding="utf-8") as dictionnaire:
        for ligne in dictionnaire:
            mot = ligne.strip()
            if mot.isalpha() and mot.isascii():
                for variante in [mot.lower(), mot.upper(), mot.capitalize()]:
                    h = hachage.hachage_etoile(variante)
                    for h2, mot2 in vus:
                        comparaisons += 1
                        if h == h2 and mot2.lower() != variante.lower():
                            return mot2, variante, comparaisons
                    vus.append((h, variante))
    return None


def recherche_collision_anagrammes(fichier: str) -> tuple[str, str, int] | None:
    """Attaque ciblée : deux anagrammes ont forcément le même H*.

    Returns:
        (mot1, mot2, nombre de mots lus) ou None.
    """
    groupes = {}&
    mots_lus = 0
    with open(fichier, "r", encoding="utf-8") as dictionnaire:
        for ligne in dictionnaire:
            mot = ligne.strip().lower()
            if mot.isalpha() and mot.isascii():
                mots_lus += 1
                cle = "".join(sorted(mot))
                if cle in groupes and groupes[cle] != mot:
                    return groupes[cle], mot, mots_lus
                groupes[cle] = mot
    return None


def speedup(base, amelioree, fichier: str, repetitions: int = 20) -> None:
    """Affiche le speed-up de `amelioree` par rapport à `base`.

    Speed-up = coût de la méthode de base / coût de la méthode améliorée,
    en nombre d'opérations (3e valeur retournée) et en temps moyen.
    """
    resultats = []
    for fonction in (base, amelioree):
        debut = time.perf_counter()
        for _ in range(repetitions):
            resultat = fonction(fichier)
        temps = (time.perf_counter() - debut) / repetitions
        resultats.append((resultat, temps))

    (res_b, t_b), (res_a, t_a) = resultats
    print(f"{base.__name__} : {res_b}, {t_b:.6f} s")
    print(f"{amelioree.__name__} : {res_a}, {t_a:.6f} s")
    print(f"Speed-up en opérations : {res_b[2] / res_a[2]:.2f}")
    print(f"Speed-up en temps      : {t_b / t_a:.2f}")

def main() -> None:
    print(
        "Collisions dans l'alphabet minuscule :",
        recherche_collision(alphabet_min),
    )
    print("Préimages du hachage 42 :", rechercheprimage(42))
    experimenter_preimages()

    nombre_egalites = 0
    nombre_vraies_collisions = 0
    total = 0

    for car1 in string.ascii_lowercase:
        for car2 in string.ascii_lowercase:
            total += 1

            if hachage.hachage_car(car1) == hachage.hachage_car(car2):
                nombre_egalites += 1

                if car1 != car2:
                    nombre_vraies_collisions += 1

    print("Probabilité même hachage :", nombre_egalites / total)
    print("Probabilité vraie collision :", nombre_vraies_collisions / total)

    mots = charger_mots(PATH)
    probabilites_hachage(mots)

    collision = recherche_collision_simplifie(PATH)

    if collision is None:
        print("Aucune collision trouvée.")
    else:
        mot1, mot2, essais = collision
        print(f"Collision : {mot1} et {mot2}")
        print(f"Hachage commun : {hachage.hachage_etoile(mot1)}")
        print(f"Valeurs essayées : {essais}")

    speedup(recherche_collision_paires, recherche_collision_anagrammes, PATH)
    speedup(recherche_collision_paires, recherche_collision_simplifie, PATH)







if __name__ == "__main__":
    main()