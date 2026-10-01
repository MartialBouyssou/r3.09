## Jeux d'essai

Nous avons vérifié la répétition de la clé lorsque celle-ci est plus courte, de même longueur ou plus longue que le texte, ainsi que les cas de texte ou de clé vide.

Nous avons testé le chiffrement et le déchiffrement avec des majuscules, des minuscules, des espaces, des chiffres et des caractères spéciaux, puis vérifié que le texte original est bien retrouvé.

Nous avons également vérifié que les textes et les clés vides ou contenant des caractères non imprimables sont rejetés.
Tout ceci a été fait dans le fichier `test_vigenere.py`.

Pour la méthode de Kasiski, nous avons utilisé les fichiers `resources/casis.txt` et `resources/casis_hatim.txt` afin de rechercher les répétitions et les tailles de clé possibles.
