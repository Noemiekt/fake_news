import json
import numpy as np
import matplotlib.pyplot as plt

# Chargement des données
with open('database4.json', 'r') as file:
    data = json.load(file)

# Paramètres de base
N = len(data["utilisateurs"])
gamma = 0.1  # Taux de guérison
days = 50

# Calcul du beta ajusté en fonction de l'engagement
engagements = [pub["likes"] + pub["commentaires"] + pub["partages"] 
               for pub in data["publications"] if pub["id_user"] == 2]  # ID 2 pour l'exemple
engagement_moyen = np.mean(engagements) if engagements else 0
beta_base = 0.3
beta = beta_base * (1 + engagement_moyen / 1000)  # Ajustement simplifié

# Initialisation
S0 = sum(1 for user in data["utilisateurs"] if user["etat"] == "susceptible")
I0 = sum(1 for user in data["utilisateurs"] if user["etat"] == "infecte")
R0 = sum(1 for user in data["utilisateurs"] if user["etat"] == "retabli")
S, I, R = [S0], [I0], [R0]

# Simulation
for _ in range(days):
    new_infections = (beta * S[-1] * I[-1]) / N
    new_recoveries = gamma * I[-1]
    S.append(S[-1] - new_infections)
    I.append(I[-1] + new_infections - new_recoveries)
    R.append(R[-1] + new_recoveries)

# Affichage des résultats
plt.figure(figsize=(10, 6))
plt.plot(S, label='Susceptibles')
plt.plot(I, label='Infectés')
plt.plot(R, label='Rétablis')
plt.title("Simulation de la Propagation en Fonction de l'Engagement")
plt.xlabel('Jours')
plt.ylabel('Nombre de personnes')
plt.legend()
plt.show()
