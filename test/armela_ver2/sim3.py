import json
import numpy as np
import matplotlib.pyplot as plt

# Chargement des données utilisateur
with open('database3.json', 'r') as file:
    data = json.load(file)

# Paramètres de base
N = len(data["utilisateurs"])
gamma = 0.1
days = 50

# Calcul de beta en fonction du nombre moyen d'abonnés des utilisateurs infectés
abonnes_infectes = [user["abonnes"] for user in data["utilisateurs"] if user["etat"] == "infecte"]
beta = 0.1 + 0.05 * np.log(np.mean(abonnes_infectes) + 1)

# Initialisation
S0, I0, R0 = N - 1, 1, 0  # Supposons 1 infecté initial
S, I, R = [S0], [I0], [R0]

# Simulation
for _ in range(days):
    new_infections = (beta * S[-1] * I[-1]) / N
    new_recoveries = gamma * I[-1]
    S.append(S[-1] - new_infections)
    I.append(I[-1] + new_infections - new_recoveries)
    R.append(R[-1] + new_recoveries)

# Affichage des résultats
plt.plot(S, label='Susceptibles')
plt.plot(I, label='Infectés')
plt.plot(R, label='Rétablis')
plt.legend()
plt.show()
