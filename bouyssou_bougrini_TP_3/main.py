from hachage import hachage_car, hachage_etoile


def main() -> None:
    """Affiche un menu permettant de tester les fonctions de hachage."""
    while True:
        print("\n|=> MENU DE HACHAGE <=|")
        print("1. Hacher un caractère (H)")
        print("2. Hacher un texte (H*)")
        print("0. Quitter")

        choix = input("Votre choix : ").strip()

        if choix == "1":
            caractere = input("Entrez un carac: ")

            try:
                print(f"H({caractere}) = {hachage_car(caractere)}")
            except (TypeError, ValueError) as erreur:
                print(f"Erreur : {erreur}")

        elif choix == "2":
            texte = input("Entrez votre texte : ")

            try:
                print(f"H*({texte}) = {hachage_etoile(texte)}")
            except (TypeError, ValueError) as erreur:
                print(f"Erreur : {erreur}")

        elif choix == "0":
            print("Byyyye!")
            break

        else:
            print("Choix pas pris en charge...")


if __name__ == "__main__":
    main()