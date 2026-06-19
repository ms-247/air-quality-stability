# Réponses aux Questions de Réflexion (§8.1)

*TP 1 & 2 — Science des Données et Calcul Scientifique Avancé (D1, 2026)*

---

## Question 1 — Analyse algorithmique : ratio de gain de temps (Exercice 6.3)

**Résultat observé.** Pour le système dense de taille `n = 4000`, le solveur direct
`np.linalg.solve` est environ **3 à 5× plus rapide** que l'inversion explicite
`np.linalg.inv(A) @ b` (la valeur exacte dépend de la machine et de l'implémentation
BLAS sous-jacente ; remplacer par le ratio affiché lors de votre exécution).

**Justification par les complexités en flops.** Les deux approches reposent sur une
factorisation LU, mais ne s'arrêtent pas au même endroit :

| Approche | Opérations | Coût (flops) |
|---|---|---|
| Solveur direct (`solve`) | factorisation LU **+** 2 substitutions (avant/arrière) | ≈ (2/3)·n³ + 2·n² ≈ **(2/3)·n³** |
| Inversion explicite (`inv`) | factorisation LU **+** résolution de n seconds membres (les colonnes de I) **+** produit A⁻¹·b | ≈ 2·n³ + 2·n² ≈ **2·n³** |

Le rapport théorique des termes dominants est donc :

```
coût(inv) / coût(solve) ≈ 2·n³ / ((2/3)·n³) = 3
```

L'inversion explicite fait à peu près **trois fois plus de travail arithmétique**,
car construire A⁻¹ revient à résoudre n systèmes linéaires (un par colonne de la
matrice identité) au lieu d'un seul. En pratique, le facteur observé peut dépasser 3
(souvent 4–5) à cause des surcoûts mémoire : l'inverse explicite alloue et parcourt
une matrice dense n×n supplémentaire, ce qui dégrade l'usage du cache.

**Conclusion.** L'inversion explicite est non seulement plus lente, mais aussi moins
précise (cf. norme du résidu) : il faut donc toujours préférer la factorisation
directe, conformément à la recommandation du cours.

---

## Question 2 — Interprétation mathématique : chiffres significatifs exacts

**Données.** Conditionnement κ(A) = 10¹³ ; epsilon machine ε_mach ≈ 10⁻¹⁶.

**Borne sur l'erreur.** Pour la résolution de Ax = b, l'erreur relative sur la
solution est majorée par le produit du conditionnement et de l'erreur relative
d'entrée (ici de l'ordre du bruit machine) :

```
‖δx‖/‖x‖  ≲  κ(A) · ε_mach  =  10¹³ × 10⁻¹⁶  =  10⁻³
```

**Nombre de chiffres exacts.** Le nombre de chiffres significatifs corrects est de
l'ordre de −log₁₀(erreur relative) :

```
−log₁₀(10⁻³) = 3  chiffres significatifs exacts
```

Autrement dit : la précision de départ offre ≈ 16 chiffres (−log₁₀ ε_mach), le
mauvais conditionnement en détruit log₁₀(κ) = 13, il en reste **16 − 13 = 3**.

**Que représentent les autres chiffres ?** Les ~13 chiffres restants **ne sont pas
de l'information** : c'est du **bruit numérique**. Ils résultent de l'amplification,
par le facteur κ(A), des erreurs d'arrondi inévitables de l'arithmétique IEEE 754.
Les afficher donnerait une fausse impression de précision : mathématiquement, ils
n'ont aucune signification.

---

## Question 3 — Éthique et rigueur : modification manuelle des données brutes

Modifier directement, à la main et sans trace un fichier de données brutes est une
faute de méthode scientifique majeure pour plusieurs raisons convergentes :

1. **Rupture de la traçabilité (provenance).** Une édition manuelle ne laisse aucune
   trace de *ce qui* a été changé, *quand*, *pourquoi* et *par qui*. La chaîne qui
   relie la donnée d'origine au résultat publié est brisée.

2. **Perte de reproductibilité.** La transformation n'existant nulle part sous forme
   de code, ni un tiers ni l'auteur lui-même ne peut régénérer le jeu de données
   modifié, donc le résultat devient irreproductible — ce qui le disqualifie comme
   résultat scientifique.

3. **La donnée brute est la source de vérité.** Elle doit rester intacte. Toute
   transformation (nettoyage, imputation, filtrage des outliers) doit passer par du
   **code versionné et documenté** — dans ce projet, la fonction `clean_data` — afin
   d'être auditable, rejouable et révisable.

4. **Indistinguable d'une falsification.** Même sans intention malveillante, une
   modification non documentée produit le même effet qu'une fabrication ou
   falsification de données : elle viole l'intégrité scientifique et compromet la
   confiance dans l'ensemble des conclusions.

**Lien avec le projet.** C'est précisément pour cette raison que le pipeline impose
les transformations *en code* (médiane, IQR) et que le `.gitignore` conserve la
donnée brute hors du versionnement tout en préservant l'architecture : la donnée
source n'est jamais éditée, seules des copies dérivées et reproductibles le sont.
