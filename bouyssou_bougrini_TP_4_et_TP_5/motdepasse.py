import hashlib as h
import string
import os
from itertools import product

def changerMotDePasseMaitre() -> None:
    while True:
        maitre: str = input("Veuillez entrer un nouveau mot de passe maitre (sans espaces)\n: ")
        if maitre and not any(c.isspace() for c in maitre):
            with open("mpwd.txt", "w", encoding="utf-8") as fichier:
                fichier.write(maitre)
            return
        print("Le mot de passe maitre ne doit pas etre vide ni contenir d'espaces.")

def recupererMotDePasseMaitre() -> str:
    if os.path.exists("mpwd.txt"):
        with open("mpwd.txt", "r", encoding="utf-8") as fichier:
            maitre: str = fichier.read()
        if maitre and not any(c.isspace() for c in maitre):
            return maitre
    changerMotDePasseMaitre()
    return recupererMotDePasseMaitre()

def generateurMotDePasse() -> str:
    maitre: str = recupererMotDePasseMaitre()
    tag: str = input("Veuillez entrer le tag\n: ")
    return generateurMotDePassePourTag(maitre, tag, 8)

def generateurMotDePassePourTag(maitre: str, tag: str, n: int) -> str:
    chaine: str = maitre + tag
    donnees = chaine.encode("utf-8")
    hachage: bytes = h.sha256(donnees).digest()
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return "".join(alphabet[o % len(alphabet)] for o in hachage[:n])

def generateurMotDePasseChoixTaille() -> str:
    n: int = int(input("Entrer un nombre compris entre 1 et 12 !\n: "))
    if n < 1 or n > 12:
        print("L'entier n doit etre compris entre 1 et 12 !!")
        return ""

    maitre: str = recupererMotDePasseMaitre()
    tag: str = input("Veuillez entrer le tag\n: ")
    return generateurMotDePassePourTag(maitre, tag, n)

def attaqueDictionnaire(n: int, tags: list[str]) -> None:
    maitre: str = recupererMotDePasseMaitre()
    alphabet = string.ascii_letters + string.digits + string.punctuation

    motsDePasseCibles = {
        tag: "".join(
            alphabet[o % len(alphabet)]
            for o in h.sha256((maitre + tag).encode("utf-8")).digest()[:n]
        )
        for tag in tags
    }

    essais: int = 0

    for caracteres in product(alphabet, repeat=10):
        candidat: str = "".join(caracteres)
        essais += 1

        if all(
            "".join(
                alphabet[o % len(alphabet)]
                for o in h.sha256((candidat + tag).encode("utf-8")).digest()[:n]
            ) == motsDePasseCibles[tag]
            for tag in tags
        ):
            print("Mot de passe maitre trouve :", candidat)
            print("Nombre d'essais :", essais)
            return

    print("Aucun mot de passe maitre trouve.")
    print("Nombre d'essais :", essais)

if input("Voulez-vous changer le mot de passe maitre ? (o/n)\n: ").lower() == "o":
    changerMotDePasseMaitre()

print("1 - Generer un mot de passe")
print("2 - Attaque sur Unilim (N=1)")
print("3 - Attaque sur Unilim, Amazon et Netflix (N=1)")
print("4 - Attaque sur les trois tags (N=2)")
print("5 - Attaque sur les trois tags (N=3)")

choix: str = input("Votre choix : ")

if choix == "1":
    print(generateurMotDePasseChoixTaille())
elif choix == "2":
    attaqueDictionnaire(1, ["Unilim"])
elif choix == "3":
    attaqueDictionnaire(1, ["Unilim", "Amazon", "Netflix"])
elif choix == "4":
    attaqueDictionnaire(2, ["Unilim", "Amazon", "Netflix"])
elif choix == "5":
    attaqueDictionnaire(3, ["Unilim", "Amazon", "Netflix"])