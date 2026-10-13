import hashlib as h
import string
import os

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
    chaine: str = maitre + tag

    donnees = chaine.encode("utf-8")
    hachage: bytes = h.sha256(donnees).digest()
    alphabet = string.ascii_letters + string.digits + string.punctuation

    resultat = "".join(alphabet[o % len(alphabet)] for o in hachage[:8])
    return resultat

def generateurMotDePasseChoixTaille() -> str:
    n: int = int(input("Entrer un nombre compris entre 1 et 12 !\n: "))
    if n < 1 or n > 12:
        print("L'entier n doit etre compris entre 1 et 12 !!")
        return ""

    maitre: str = recupererMotDePasseMaitre()
    tag: str = input("Veuillez entrer le tag\n: ")
    chaine: str = maitre + tag

    donnees = chaine.encode("utf-8")
    hachage: bytes = h.sha256(donnees).digest()
    alphabet = string.ascii_letters + string.digits + string.punctuation

    resultat = "".join(alphabet[o % len(alphabet)] for o in hachage[:n])
    return resultat

if input("Voulez-vous changer le mot de passe maitre ? (o/n)\n: ").lower() == "o":
    changerMotDePasseMaitre()

print(generateurMotDePasseChoixTaille())