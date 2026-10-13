import hashlib as h
"""
Fonctions utiles :
- hashlib.sha1(data) : hachage SHA-1.
- hashlib.sha256(data) : hachage SHA-256.
- .digest() : résultat sous forme d'octets.
- .hexdigest() : résultat sous forme hexadécimale.
"""
import string
def generateurMotDePasse(chaine1 : str , chaine2 : str):
    chaine : str = chaine1 + chaine2
    donnees = chaine.encode("utf-8")
    hachage : bytes = h.sha256(donnees).digest()
    alphabet = string.ascii_letters + string.digits + string.punctuation

    # 4. Convertir les octets en 8 caractères imprimables
    resultat = "".join(
        alphabet[o % len(alphabet)] for o in hachage[:8]
    )
    print(resultat)
generateurMotDePasse("Salut" , "Toi")