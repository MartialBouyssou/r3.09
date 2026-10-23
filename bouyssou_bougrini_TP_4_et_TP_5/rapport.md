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

### Récupéré le mot de passe maitre

La fonction `recupererMotDePasseMaitre()` permet de récupérer le mot de passe maitre du fichier `mpwd.txt`.

Le programme vérifie si le fichier existe. Si c'est le cas, il lit son contenu et vérifi qu'il est valide.

Si le fichier n'existe pas ou que son contenu est vide/invalide, alors le programme demande un nouveau mot de passe maitre. Ensuite il est enregistré et récupéré.

```
def recupererMotDePasseMaitre() -> str:
    if os.path.exists("mpwd.txt"):
        with open("mpwd.txt", "r", encoding="utf-8") as fichier:
            maitre: str = fichier.read()
        if maitre and not any(c.isspace() for c in maitre):
            return maitre

    changerMotDePasseMaitre()
    return recupererMotDePasseMaitre()
```

Le but étant d'éviter qu'à chaque génération l'on soit obligé de re-saisir le mot de passe maitre, bien que l'on demande en début de programme si l'utilisateur veut le changer.

Cependant, le mot de passe est enregistré directement en clair dans le fichier. Une personne qui peut lire ce fichier peut donc récupérer le mot de passe maitre. Il serait possible d'améliorer ce point en sécurisant le stockage.

## Attaque par dictionnaire

### Principe de l'attaque

Le but est de retrouver un mot de passe maitre possible sans le connaitre ! Pour cela on utilise des mots de passe généré pour les différents tags.

Nous utilisons un mot de passe maitre de 10 caractères. Les tags demandés sont : `Unilim`, `Amazon` et `Netflix`.

Le programme commence par encoder les mots de passe cibles grâce au vrai mot de passe maitre. Il teste ensuite les candidats de 10 caractères jusqu'à ce qu'il ait trouvé un mot de passe maitre qui match les mêmes résultats.

### Génération des mots de passe cibles

Pour commencer il faut récupérer le mot de passe maitre pour généré le mot de passe pour chaque tag.

Les mots de passe obtenus servent de référence pendant l'attaque !

```
maitre: str = recupererMotDePasseMaitre()
alphabet = string.ascii_letters + string.digits + string.punctuation

motsDePasseCibles = {
    tag: "".join(
        alphabet[o % len(alphabet)]
        for o in h.sha256((maitre + tag).encode("utf-8")).digest()[:n]
    )
    for tag in tags
}
```

Nous utilisons SHA-256 pour calculer le hachage du mot de passe maitre concaténé avec le tag. Le résultat est ensuite transformé en caractères à l'aide de notre alphabet.

La sortie est tronquée à la taille demandée : `n`.

### Recherche du mot de passe maitre

Le programme utilise `product()` qui génère une liste de toute les combinaison de 10 caractères possible.

Chaque caractère est choisi dans l'alphabet contenant les lettres minuscules et majuscules, les chiffres et les caractères spéciaux.

Pour chaque candidat, le programme calcule les mots de passe pour chaque tags. Il les compare ensuite aux mots de passe cibles.

```
essais: int = 0

for caracteres in product(alphabet, repeat=10):
    candidat: str = "".join(caracteres)
    essais += 1

    if all(
        "".join(
            alphabet[o % len(alphabet)]
            for o in h.sha256(
                (candidat + tag).encode("utf-8")
            ).digest()[:n]
        ) == motsDePasseCibles[tag]
        for tag in tags
    ):
        print("Mot de passe maitre trouve :", candidat)
        print("Nombre d'essais :", essais)
        return

print("Aucun mot de passe maitre trouve.")
print("Nombre d'essais :", essais)
```

### Résultats et comparaison

Pour le premier test, avec le tag `Unilim`, avec une taille de mot de passe `N = 1`.

Dans ce cas, le programme doit seulement trouver un candidat qui produit le même caractère que le mot de passe maitre d'origine.

| Test | Taille N | Tags utilisés           | Nombre d'essais |
| ---- | -------- | ----------------------- | --------------- |
| 1    | 1        | Unilim                  | 74              |
| 2    | 1        | Unilim, Amazon, Netflix | 566039          |
| 3    | 2        | Unilim, Amazon, Netflix |                 |
| 4    | 3        | Unilim, Amazon, Netflix |                 |

Avec un seul caractère, beaucoup de candidats différents peuvent produire le même mot de passe. La recherche est donc rapide.

Lorsque nous utilisons trois tags, le candidat doit produire les trois mêmes mots de passe. Les conditions sont bien plus nombreuses. C'est plus difficile.

Enfin, lorsque nous augmentons la taille `N`, le nombre de caractères à retrouver augmente également. Il devient donc moins probable qu'un candidat choisi au hasard corresponde à tous les résultats attendus.

### Probabilité théorique

Notre alphabet contient 94 caractères possibles. Il existe donc :
$$
94^{10} \approx 5,39 \times 10^{19}
$$
mots de passe maitres possibles de 10 caractères.

Retrouver le vrai mot de passe maitre par force brute est donc très difficile quand il a été choisi au hasard.

Cependant, notre attaque ne cherche pas forcément le vrai mot de passe maitre. Il cherche un candidat qui donne les mêmes mots de passe pour chaque tags.

En supposant qu'ils soient indépendants et uniformément répartis, la probabilité qu'un candidat corresponde à un mot de passe cible de taille `N` pour un tag est :
$$
P = \frac{1}{94^N}
$$
Avec trois tags distincts, cette probabilité devient :
$$
P = \frac{1}{94^{3N}}
$$
Pour `N = 1`, cela donne :
$$
P = \frac{1}{94^3}
\approx 1,20 \times 10^{-6}
$$
Il faut donc environ 830 584 essais en moyenne pour trouver une correspondance sur les trois tags.

Pour `N = 2` et `N = 3`, le nombre d'essais attendu augmente fortement. La recherche est donc beaucoup trop longue.