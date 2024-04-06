import json
import numpy as np
import matplotlib.pyplot as plt

# Chargement des données (supposées similaires à l'exemple 1)
N = 10000  # Population totale
S0, I0, R0 = N - 1, 1, 0  # Supposons 1 infecté initial
gamma = 0.1  # Taux de guérison
days = 50

S, I, R = [S0], [I0], [R0]

# Beta varie avec le temps
betas = [0.3 - 0.005*i for i in range(days)]

for day in range(days):
    beta = betas[day]
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
