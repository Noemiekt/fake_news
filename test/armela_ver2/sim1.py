import json
import numpy as np
import matplotlib.pyplot as plt

# Chargement des données utilisateur
with open('database1.json', 'r') as file:
    data = json.load(file)

# Initialisation des paramètres
N = len(data["utilisateurs"])
print(N)
I0 = sum(1 for user in data["utilisateurs"] if user["etat"] == "infecte")
S0 = N - I0
R0 = sum(1 for user in data["utilisateurs"] if user["etat"] == "retabli")
beta, gamma = 0.3, 0.1
days = 50
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
