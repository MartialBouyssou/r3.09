# RAPPORT



## Gestion mot de passe maitre

### Enregistrement du mot de passe maitre

Pour enregistrer le mot de passe, nous avons créé le système de stockage du mot de passe maitre dans un fichier txt: `mpwd.txt`.

La fonction `changerMotDePasseMaitre()` permet à l'utilisateur changer de mot de passe maitre. Le programme vérifie que le mot de passe n'est pas vide et qu'il contient pas d'espaces.

Si toutes les conditions sont bien respectées, le mot de passe est enregistré dans le fichier. Sinon, le programme redemande une saisie.

```
def changerMotDePasseMaitre() -> None:
    while True:
        maitre: str = input(
            "Veuillez entrer un nouveau mot de passe maitre\n: "
        )
        if maitre and not any(c.isspace() for c in maitre):
            with open("mpwd.txt", "w", encoding="utf-8") as fichier:
                fichier.write(maitre)
            return
        print("Le mot de passe maitre ne doit pas etre vide ni contenir d'espaces.")
```

