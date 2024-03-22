# beta dépend du nombre moyen des abonnées des utilisateurs 


import numpy as np
import matplotlib.pyplot as plt

# Paramètres
N = 10000  # Population totale
I0 = 1     # Nombre initial d'infectés
S0 = N - I0 # Nombre initial de susceptibles
R0 = 0     # Nombre initial de rétablis
avg_followers = 500 # nombre moyen des abonnées
beta = 0.1 + 0.05 * np.log(avg_followers) # Taux de transmission
gamma = 0.1 # Taux de guérison

# Simulation sur 50 jours
days = 50
S, I, R = [S0], [I0], [R0]

for _ in range(days):
    new_infections = (beta * S[-1] * I[-1]) / N
    new_recoveries = gamma * I[-1]
    S.append(S[-1] - new_infections)
    I.append(I[-1] + new_infections - new_recoveries)
    R.append(R[-1] + new_recoveries)

# Affichage des résultats
plt.figure(figsize=(10,6))
plt.plot(S, label='Susceptibles')
plt.plot(I, label='Infectés')
plt.plot(R, label='Rétablis')
plt.xlabel('Jours')
plt.ylabel('Nombre de personnes')
plt.legend()
plt.show()
