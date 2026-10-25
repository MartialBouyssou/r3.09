# RAPPORT

## a. Bibliothèques utilisées et choix

Bibliothèques retenues (Python) :

- `hashlib` : bibliothèque standard fournissant SHA-256 (effet d'avalanche indispensable pour le générateur) ;
- `string` : alphabet complet (lettres, chiffres, caractères spéciaux) sans oubli ;
- `itertools` : `product` pour parcourir l'espace de recherche de l'attaque (exercice 4) ;
- `os` : vérifier l'existence du fichier `mpwd.txt`.

| Langage | Candidat | Intérêt | Limite |
|---|---|---|---|
| Python | `hashlib` (standard) | SHA-1/256, PBKDF2, scrypt, sans installation | pas de chiffrement |
| Python | `cryptography` | AES-GCM, Fernet (utile pour l'extension) | dépendance externe |
| Java | `MessageDigest` / `javax.crypto` | standard, AES, HMAC, PBKDF2 | code plus verbeux |
| Java | Bouncy Castle | très complet (Argon2…) | lourd pour ce TP |

**Choix : Python + `hashlib`.** SHA-256 suffit (32 octets ≥ 12 caractères demandés), sans dépendance, et Python permet d'itérer vite sur l'attaque. SHA-1 est écarté : obsolète (collisions démontrées) et sortie plus courte (20 octets).

## b. Génération et troncature des mots de passe

Même algorithme pour le cas simple (`n = 8`) et la taille variable (`n` de 1 à 12) :

1. `chaine = maitre + tag`, encodée en UTF-8, puis `SHA-256(chaine)` : 32 octets ;
2. on garde les `n` premiers octets (`hachage[:n]`), car `n ≤ 12 < 32` ;
3. chaque octet `o` devient `alphabet[o % 94]` (lettres + chiffres + ponctuation : 94 symboles, sans espace ni caractère invisible).

```python
def generateurMotDePassePourTag(maitre: str, tag: str, n: int) -> str:
    chaine: str = maitre + tag
    donnees = chaine.encode("utf-8")
    hachage: bytes = h.sha256(donnees).digest()
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return "".join(alphabet[o % len(alphabet)] for o in hachage[:n])
```

**Jeux d'essais** (maître `arbrefeuil`) :

| Test | Résultat |
|---|---|
| N=1, Unilim / N=8, Amazon / N=12, Netflix | `Q` / `<lF^fFk>` / `m;c"5p+Ssk3-` |
| Longueur de sortie pour N = 1…12 | toujours N |
| Même entrée deux fois | même sortie |
| N = 0 ou N = 13 | refusé, message d'erreur |
| SHA-256(`arbrefeuilUnilim`) | `8853fee1…975314`, 32 octets ; ses premiers octets donnent bien `Q@%…` |
| Maître vide, avec espace, ou fichier absent | nouvelle saisie demandée |

**Distribution** (200 000 mots de passe de 8 caractères, maîtres aléatoires) : les 68 premiers symboles sortent à 1,17 % et les 26 derniers à 0,78 %, au lieu de 1/94 = 1,06 %. C'est un biais du modulo (256 = 2 × 94 + 68), confirmé par un χ² de 42 965 (93 degrés de liberté). Sa conséquence est faible : −0,02 bit d'entropie par caractère (6,555 → 6,534). Un tirage par rejet des octets ≥ 188 le corrigerait (non implémenté).

## c. Attaque contre les mots de passe : fonctionnement et vulnérabilités

### Algorithme

Le programme calcule d'abord les mots de passe cibles avec le vrai maître (10 caractères) pour les tags `Unilim`, `Amazon` et `Netflix`, puis teste tous les candidats de 10 caractères de l'alphabet (`product(alphabet, repeat=10)`) jusqu'à ce que **tous** les tags donnent le même résultat. Extrait de `attaqueDictionnaire()` :

```python
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
```

Ce parcours est séquentiel (`aaaaaaaaaa`, `aaaaaaaaab`, …). `attaque.py` tire au contraire les candidats au hasard (`secrets.choice`) : c'est équivalent en moyenne et permet de répéter les expériences.

### Vulnérabilités exploitées

- **Hachage rapide et sans sel** : SHA-256 se calcule en quelques microsecondes (pas de PBKDF2, scrypt ou Argon2).
- **Vérification hors-ligne** : un seul mot de passe généré connu suffit pour tester des candidats sans contacter le service.
- **Troncature** : N caractères (≈ 6,55 bits chacun) contiennent moins d'information que le maître (≈ 65,5 bits), d'où des collisions, d'autant plus nombreuses que N est petit.
- **Tag public** : l'attaquant connaît toute l'entrée sauf le maître.
- **Maître faible** : `arbrefeuil` est un mot en minuscules, testé en premier par un attaquant réaliste.

### Résultats

**Retrouver le maître lui-même.** 94¹⁰ ≈ 5,4 × 10¹⁹ possibilités (≈ 65,5 bits) : probabilité de 1,9 × 10⁻²⁰ par essai. À ≈ 75 000 essais/s (Python, mesuré) cela représente ≈ 10⁷ ans en moyenne ; à 10¹⁰ essais/s (matériel dédié hypothétique) ≈ 85 ans. Avec 10 minuscules seulement (cas de `arbrefeuil`), l'espace tombe à 26¹⁰ ≈ 1,4 × 10¹⁴ : environ 4 heures.

**Collisions** (cibles à N=1 : Unilim → `Q`, Amazon → `<`, Netflix → `m`) :

| Cas | Séquentiel (essais) | Aléatoire (moyenne) | Théorique 94^(N·T) |
|---|---|---|---|
| N=1, Unilim | 74 | 94,6 (20 essais) | 94 |
| N=2, Unilim | 10 564 | 10 290 (10 essais) | 8 836 |
| N=3, Unilim | — | 1 654 627 (5 essais) | 830 584 |
| N=1, 3 tags | 566 039 | 234 782 (3 essais) | 830 584 |
| N=2, 3 tags | non terminé | non terminé | 6,9 × 10¹¹ (≈ 106 jours) |
| N=3, 3 tags | non terminé | non terminé | 6,1 × 10¹⁷ (≈ 2,6 × 10⁵ ans) |

Les mesures suivent la théorie (loi géométrique de moyenne 1/p, d'où l'écart sur les petits échantillons). Passer d'un à trois tags multiplie le coût par 94² ≈ 8 800 (N=1), et chaque caractère de sortie en plus le multiplie par 94.

### Analyse

**Hypothèse pour N = 8, 10 et 12** : essais ≈ 94^N pour un tag (94^(3N) pour trois tags) :

| N | Essais (1 tag) | Python (75 000/s) | Matériel dédié (10¹⁰/s) |
|---|---|---|---|
| 8 | 6,1 × 10¹⁵ | ≈ 2 600 ans | ≈ 7 jours |
| 10 | 5,4 × 10¹⁹ | ≈ 2,3 × 10⁷ ans | ≈ 171 ans |
| 12 | 4,8 × 10²³ | ≈ 2 × 10¹¹ ans | ≈ 1,5 × 10⁶ ans |

Avec 3 tags, le coût est plafonné par la taille de l'espace des maîtres (94¹⁰). Le nombre de maîtres compatibles avec N·T caractères observés est ≈ 94^(10 − N·T) : pour N petit, le maître trouvé ne marche que pour les tags observés ; dès N·T ≥ 10, la collision revient à retrouver le vrai maître.

**Conclusion de design.** Le danger ne vient pas de N mais de la possibilité de tester très vite des candidats hors-ligne : seules la force du maître et la lenteur de la fonction de hachage protègent. Il faut un maître long et aléatoire, N = 12 si possible, et un hachage lent (PBKDF2, scrypt, Argon2) plutôt que SHA-256 seul.

## d. Extensions : stockage du mot de passe maître

Le maître est stocké dans `mpwd.txt`. `changerMotDePasseMaitre()` refuse un mot de passe vide ou contenant des espaces et redemande la saisie ; `recupererMotDePasseMaitre()` lit le fichier et, s'il est absent, vide ou invalide, demande un nouveau maître avant de le relire. Le programme propose de changer le maître au début de chaque exécution.

```python
def changerMotDePasseMaitre() -> None:
    while True:
        maitre: str = input("Veuillez entrer un nouveau mot de passe maitre\n: ")
        if maitre and not any(c.isspace() for c in maitre):
            with open("mpwd.txt", "w", encoding="utf-8") as fichier:
                fichier.write(maitre)
            return
        print("Le mot de passe maitre ne doit pas etre vide ni contenir d'espaces.")
```

Limite : le maître est enregistré **en clair** ; quiconque lit le fichier le récupère. Piste (Exercice 5, non implémentée) : dériver une clé de 256 bits d'une phrase de passe avec scrypt ou PBKDF2 (`hashlib`, sel aléatoire), chiffrer le maître en AES-256-GCM (`cryptography`) et stocker `sel | nonce | chiffré | tag`. GCM détecte toute modification ; pour changer le maître, on déchiffre puis on rechiffre avec un nouveau sel et un nouveau nonce.

<div style="page-break-before: always"></div>

## e. Page de réflexion : conclusions techniques et bonnes pratiques

**Intérêt.** Aucun mot de passe n'est stocké : il se recalcule hors-ligne, différent pour chaque service, et l'utilisateur ne retient qu'un secret. La fuite d'un site n'expose pas directement les autres comptes.

**Limites.**

- Le maître est un point de défaillance unique : compromis, tous les comptes le sont, et on ne peut pas le changer sans changer tous les mots de passe.
- Un seul mot de passe généré qui fuit permet une attaque hors-ligne sur le maître, d'autant plus rapide que le hachage est rapide (cf. notre attaque).
- Changer le mot de passe d'un seul service impose de modifier son tag (`Unilim2`) ; les politiques des sites (longueur, symboles interdits) ne sont pas gérées.
- Le fichier du maître en clair annule une grande partie de l'intérêt du système.

**Bonnes pratiques.**

1. Un **maître long et aléatoire** (5-6 mots tirés au hasard, ou ≥ 16 caractères), jamais un mot du dictionnaire.
2. La **taille maximale** (N = 12 ou plus) et tout l'alphabet quand le site l'accepte.
3. Une **dérivation lente avec sel** (PBKDF2, scrypt, Argon2) à la place de SHA-256 seul.
4. **Ne pas stocker le maître en clair** : le chiffrer ou le redemander, et restreindre les droits du fichier.
5. Des **tags uniques et versionnés**, avec un fichier de correspondance service ↔ tag.
6. Corriger le **biais du modulo** (tirage par rejet).
7. Activer l'**authentification à deux facteurs** quand elle existe.

**Conclusion.** Un tel générateur est utilisable si le maître est fort et protégé. Un gestionnaire de mots de passe chiffré reste préférable pour la plupart des utilisateurs, car il permet de changer un mot de passe isolément.

> Anthropic. (2026). Claude (Version 5 Sonnet) \[Grand modèle multimodal]. \[https://claude.ai](https://claude.ai/).
Compréhension de la documentation / aide sur le code / correction d’orthographe \[AIA] / aide  pour le rapport
>