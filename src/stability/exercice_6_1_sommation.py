"""
Exercice 6.1 : Horizon de visibilite numerique et non-associativite.

On observe l'accumulation des erreurs d'arrondi lorsqu'on additionne un grand
nombre a une multitude de petites valeurs sous le seuil de visibilite machine.
"""
import numpy as np


def sommation_naive(tableau):
    somme = 0.0
    for x in tableau:
        somme += x
    return somme


def sommation_kahan(tableau):
    somme = 0.0
    c = 0.0  # compensation : memorise les bits de poids faible perdus
    for x in tableau:
        y = x - c            # on re-injecte la perte du tour precedent
        t = somme + y        # cette addition perd les bits de poids faible de y
        c = (t - somme) - y  # (t - somme) recupere la partie "vue" ; - y isole la partie perdue
        somme = t
    return somme


if __name__ == "__main__":
    epsilon_machine = np.finfo(float).eps
    print(f"Epsilon Machine de votre processeur : {epsilon_machine}")

    # Un grand nombre suivi de 10000 valeurs juste sous le seuil de visibilite.
    valeurs = [1.0] + [epsilon_machine / 2.0] * 10000

    print(f"Somme Naive : {sommation_naive(valeurs)}")
    print(f"Somme Kahan : {sommation_kahan(valeurs)}")
    print(f"Resultat mathematique attendu (R) : {1.0 + 10000 * (epsilon_machine / 2.0)}")
