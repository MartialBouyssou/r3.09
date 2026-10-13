import hashlib as h
"""
Fonctions utiles :
- hashlib.sha1(data) : hachage SHA-1.
- hashlib.sha256(data) : hachage SHA-256.
- .digest() : résultat sous forme d'octets.
- .hexdigest() : résultat sous forme hexadécimale.
"""
import string
def generateurMotDePasse()->str:
    chaine1 : str = input("Veuiller entrer une premier chaine de caractere\n: ")
    chaine2 : str = input("Veuiller entrer une deuxieme chaine de caractere\n: ")
    chaine : str = chaine1 + chaine2
    donnees = chaine.encode("utf-8")
    hachage : bytes = h.sha256(donnees).digest()
    alphabet = string.ascii_letters + string.digits + string.punctuation

    resultat = "".join(
        alphabet[o % len(alphabet)] for o in hachage[:8]
    )
    print(resultat)
    return resultat

def generateurMotDePasseChoixTaille()->str:
    n : int = int(input("Entrer un nombre compris entre 1 et 12 !\n: "))
    if (0>n>13):
        print("L'entier n doit etre compris entre 1 et 12 !!")
        return ""
    chaine1 : str = input("Veuiller entrer une premier chaine de caractere\n: ")
    chaine2 : str = input("Veuiller entrer une deuxieme chaine de caractere\n: ")
        
    chaine : str = chaine1 + chaine2
    donnees = chaine.encode("utf-8")
    hachage : bytes = h.sha256(donnees).digest()
    alphabet = string.ascii_letters + string.digits + string.punctuation

    # 4. Convertir les octets en 8 caractères imprimables
    resultat = "".join(
        alphabet[o % len(alphabet)] for o in hachage[:n]
    )
    print(resultat)
    return resultat
generateurMotDePasse()
generateurMotDePasseChoixTaille()