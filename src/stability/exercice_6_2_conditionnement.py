"""
Exercice 6.2 : Le Multiplicateur de Mensonge - Sensibilite au conditionnement.

Une perturbation de l'ordre du bruit machine (1e-14) sur le second membre b peut
modifier radicalement la solution x d'un systeme Ax = b mal conditionne.
"""
import numpy as np

# Matrice de Hilbert 3x3 (cas d'ecole reputé mal conditionne).
A = np.array(
    [
        [1.0, 1.0 / 2.0, 1.0 / 3.0],
        [1.0 / 2.0, 1.0 / 3.0, 1.0 / 4.0],
        [1.0 / 3.0, 1.0 / 4.0, 1.0 / 5.0],
    ]
)

b = np.array([1.0, 0.5, 0.3333])

# 1. Conditionnement en norme 2
kappa_A = np.linalg.cond(A, 2)
print(f"Conditionnement de la matrice de resolution kappa(A) = {kappa_A}")

# 2. Resolution du systeme exact (solveur stable, JAMAIS .inv())
x_exact = np.linalg.solve(A, b)

# 3. Perturbation microscopique du vecteur b
b_perturbe = b.copy()
b_perturbe[2] += 1e-14  # de l'ordre du bruit de mesure

x_perturbe = np.linalg.solve(A, b_perturbe)

# 4. Erreur relative induite sur la solution
erreur_relative = np.linalg.norm(x_exact - x_perturbe) / np.linalg.norm(x_exact)
print(f"x_exact    = {x_exact}")
print(f"x_perturbe = {x_perturbe}")
print(f"Erreur relative induite sur la prediction x : {erreur_relative:.6f}")
print(f"  (en notation scientifique : {erreur_relative:.3e})")
print(f"  borne theorique kappa(A) * (||db||/||b||) ~ {kappa_A * (1e-14 / np.linalg.norm(b)):.3e}")
