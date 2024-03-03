import json
import numpy as np
import matplotlib.pyplot as plt

# Charger les données depuis le fichier JSON
with open('fake_news_data.json', 'r') as file:
    data = json.load(file)

# Paramètres initiaux du modèle SIR
beta = 0.001  # Taux de transmission par interaction: probabilité qu'une interaction avec un post contenant des fake news entraîne la contamination d'un utilisateur 
gamma = 0.1  # Taux de récupération: pb qu'un utilisateur infecté devienne recovered par jour 

# Nombre initial de susceptibles, infectieux et récupérés
N = sum(user['followers_count'] for user in data['users'])  # Population totale: sum(followers)
I_initial = sum(post['likes'] + post['comments'] + post['shares'] for post in data['posts'] if post['is_fake_news'])  # Initial infectieux basé sur l'engagement des fausses nouvelles
S_initial = N - I_initial  # Initial susceptibles
R_initial = 0  # Initial récupérés

# Simulation du modèle SIR sur 50 jours
T = 50
S, I, R = [S_initial], [I_initial], [R_initial]

for _ in range(1, T):
    new_infections = (beta * S[-1] * I[-1]) / N
    new_recoveries = gamma * I[-1]
    S.append(S[-1] - new_infections)
    I.append(I[-1] + new_infections - new_recoveries)
    R.append(R[-1] + new_recoveries)

# Afficher la simulation avec Matplotlib
days = np.arange(T)
plt.figure(figsize=(10, 6))
plt.plot(days, S, label='Susceptible')
plt.plot(days, I, label='Infectious')
plt.plot(days, R, label='Recovered')
plt.title("SIR Model Simulation of Fake News Spread on Health")
plt.xlabel("Day")
plt.ylabel("Number of Users")
plt.legend()
plt.grid(True)
plt.show()
