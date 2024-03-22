import json
import numpy as np
import matplotlib.pyplot as plt

# Chargement des données utilisateur
with open('database2.json', 'r') as file:
    data = json.load(file)

# Initialisation des paramètres
N = len(data["utilisateurs"])
beta_base = 0.3  # Taux de transmission de base
gamma = 0.1  # Taux de guérison
days = 50

# Calcul du beta ajusté en fonction de la crédibilité
credibilities = [user["credibilite"] for user in data["utilisateurs"] if user["etat"] == "infecte"]
beta_adjusted = beta_base * np.mean(credibilities) if credibilities else beta_base

S0 = sum(1 for user in data["utilisateurs"] if user["etat"] == "susceptible")
I0 = sum(1 for user in data["utilisateurs"] if user["etat"] == "infecte")
R0 = sum(1 for user in data["utilisateurs"] if user["etat"] == "retabli")

S, I, R = [S0], [I0], [R0]

# Simulation
for _ in range(days):
    new_infections = (beta_adjusted * S[-1] * I[-1]) / N
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
