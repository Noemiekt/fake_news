import json
import networkx as nx
import pygame as pg
import numpy as np
import plotly.graph_objects as go
import sys
import matplotlib.pyplot as plt
import random
import seaborn as sns
import pandas as pd



# Load the data from the JSON file
with open('json_co_v6.json', 'r') as file:
    data = json.load(file)

# Extract influencers and users
influencers = data['influencers']
users = data['users']
total_users = data['totalUsers']
total_influencers = data['totalInfluencers']


# Créer le graphe du réseau social
G = nx.DiGraph()

# Ajouter les nœuds (utilisateurs)
for user in users:
    G.add_node(user['username'], type='user', state='S')

for influencer in influencers:
    G.add_node(influencer['username'], type='influencer', state='S',
               credibility=influencer['credibility_rate'], activity_rate=influencer['activity_rate'])
    # Add edges from influencer to followers (students)
    for follower in influencer['followers']:
        G.add_edge(influencer['username'], follower['username'])

# Add edges between students based on their followers
for user in users:
    for follower in user['followers']:
        G.add_edge(user['username'], follower['username'])
    

# Créez la position des nœuds en utilisant l'algorithme de mise en page de votre choix
pos = nx.spring_layout(G)


# Définition des arêtes
edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

# Définition des nœuds
node_x = []
node_y = []
node_text = []  # Stocke le texte à afficher lors du survol d'un nœud
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    # Ajouter le texte à afficher lors du survol
    node_info = f"{node}"
    node_text.append(node_info)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',  # Ajouter du texte aux marqueurs
    hoverinfo='text',
    text=node_text,  # Le texte à afficher sur le survol
    textposition="top center",
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Niveau de Confiance',
            xanchor='left',
            titleside='right'
        ),
        line_width=2))

# Couleurs des nœuds basées sur l'attribut 'state'
node_adjacencies = []
for node, adjacencies in enumerate(G.adjacency()):
    node_adjacencies.append(len(adjacencies[1]))

node_trace.marker.color = node_adjacencies

# Créer la figure
fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=0,l=0,r=0,t=0),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

fig.show()


# Initialisation de Pygame
pg.init()

# Configuration de la fenêtre
width, height = 1000, 750
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Simulation de la Propagation de Désinformation")

# Paramètres de la simulation
pop_size = total_users
recovery_time = 10000  # en millisecondes
velocity = 2
num_influencers = total_influencers  

# Caractéristiques des influenceurs
influencer_specs = []
for influencer in influencers: 
    specs = {
        "followers": influencer['followers_count'],
        "activity_rate": influencer['activity_rate'],
        "credibility_rate": influencer['credibility_rate']
    }
    influencer_specs.append(specs)

print(influencer_specs)

# Pour stocker le nombre d'individus dans chaque état à chaque itération
data = {"S": [], "I": [], "R": []}

class Person:
    def __init__(self, username, influencer=False, followers=0, activity_rate=0.0, credibility_rate=1.0, following=None):
        self.username = username
        self.followers = followers if followers else []
        self.following = following if following else []
        self.influencer = influencer
        self.followers = followers
        self.activity_rate = activity_rate
        self.credibility_rate = credibility_rate
        self.status = 'I' if influencer else 'S'
        self.position = np.random.rand(2) * np.array([width, height])
        self.velocity = np.random.randn(2) * velocity
        self.infection_time = pg.time.get_ticks() if influencer else None
        self.infected_by = None if not influencer else self

    def move(self):
        self.position += self.velocity
        if self.position[0] < 0 or self.position[0] > width:
            self.velocity[0] *= -1
        if self.position[1] < 0 or self.position[1] > height:
            self.velocity[1] *= -1

    def update_status(self):
        if self.status == 'I' and pg.time.get_ticks() - self.infection_time > recovery_time:
            self.status = 'R'

    def draw(self):
        color = colors[self.status]
        pg.draw.circle(screen, color, self.position.astype(int), 5)


# Initialisation de la population avec des influenceurs et des utilisateurs normaux
population = [
    Person(username=f"user{i+1}", influencer=False)  # Générer des noms d'utilisateur comme user1, user2, etc.
    for i in range(pop_size - num_influencers)
] + [
    Person(username=f"influencer{j+1}", influencer=True, followers=50, activity_rate=0.5, credibility_rate=0.9)  # Exemple pour les influenceurs
    for j in range(num_influencers)
]


# Initialisation des personnes (pseudo-code, adaptez à votre structure de données)
for user_data in users:
    person = Person(
        username=user_data['username'],
        influencer=False,
        following=user_data['userInfluencers'] 
    )
    population.append(person)

for influencer_data in influencers:
    person = Person(
        username=influencer_data['username'],
        influencer=True,
        followers=influencer_data['followers'],
        activity_rate=influencer_data['activity_rate'],
        credibility_rate=influencer_data['credibility_rate']
    )
    population.append(person)

# Couleurs
colors = {"S": (0, 0, 255), "I": (255, 0, 0), "R": (0, 255, 0)}

credibility_weight = 0.87
activity_weight = 0.13

clock = pg.time.Clock()
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((255, 255, 255))  # Fond blanc

    for person in population:
        person.move()
        person.update_status()
        person.draw()
        if person.status == 'I':
            for other in population:
                if np.linalg.norm(person.position - other.position) < 10 and other.status == 'S':

                    # Calculer la probabilité d'infection basée sur la crédibilité et le taux d'activité
                    infection_probability = credibility_weight * person.credibility_rate + activity_weight * person.activity_rate


                    infection_chance = infection_probability * person.credibility_rate * (person.activity_rate if person.influencer else 1)

                    # Augmenter la probabilité si 'other' suit 'person'
                    if person.username in other.following:
                        follow_influence_factor = 2
                        infection_chance *= follow_influence_factor  # follow_influence_factor > 1
                
                    # Si follow_influence_factor = 1, suivre un influenceur n'a aucun effet sur la probabilité d'être influencé.
                    # Si follow_influence_factor = 2, un follower est deux fois plus susceptible d'être influencé par cet influenceur que quelqu'un qui ne le suit pas.
                    # Si follow_influence_factor = 0.5, suivre un influenceur réduit en fait la probabilité d'être influencé (ce qui pourrait être contre-intuitif dans la plupart des cas).

                    if person.influencer:
                        infection_chance *= person.activity_rate
                    if np.random.rand() < infection_chance:
                        other.status = 'I'
                        other.infection_time = pg.time.get_ticks()
                        other.infected_by = person.infected_by

    pg.display.flip()
    clock.tick(30)

    # Compter et enregistrer le nombre d'individus dans chaque état
    counts = {"S": 0, "I": 0, "R": 0}
    for person in population:
        counts[person.status] += 1
    for status in ["S", "I", "R"]:
        data[status].append(counts[status])

pg.quit()


# -------------------------------- Affichage des graphiques --------------------------------

# Assurez-vous d'avoir des données pour tous les graphiques
influencer_usernames = [influencer['username'] for influencer in influencers]
followers_counts = [influencer['followers_count'] for influencer in influencers]
activity_rates = [influencer['activity_rate'] for influencer in influencers]
credibility_rates = [influencer['credibility_rate'] for influencer in influencers]
infections_counts = [sum(1 for person in population if person.infected_by and person.infected_by.username == influencer['username']) for influencer in influencers]


# Maintenant, les longueurs devraient correspondre
assert len(influencer_usernames) == len(infections_counts), "Les longueurs des labels et des comptes d'infection ne correspondent pas."

# Création du DataFrame
df = pd.DataFrame({
    'Influenceurs': influencer_usernames,
    'Followers': followers_counts,
    'Activité': activity_rates,
    'Crédibilité': credibility_rates,
    'Infections': infections_counts
})

# Définir les couleurs uniques pour chaque influenceur
palette = sns.color_palette("viridis", len(df['Influenceurs']))  # Utilisation d'une palette "hsv" pour la diversité
color_map = dict(zip(df['Influenceurs'], palette))  # Création d'une correspondance entre les influenceurs et les couleurs

# Initialiser la figure avec des subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 7.6), gridspec_kw={'width_ratios': [1, 1], 'height_ratios': [1, 1], 'wspace': 0.3, 'hspace': 0.4})

# Premier graphique: Nombre de followers
sns.barplot(x='Influenceurs', y='Followers', data=df, palette=color_map, ax=axs[0, 0])
axs[0, 0].set_title('Nombre de Followers par Influenceur')
axs[0, 0].set_xticklabels([])  # Retirer les noms sur l'axe x

# Deuxième graphique: Nombre d'infections
sns.barplot(x='Influenceurs', y='Infections', data=df, palette=color_map, ax=axs[0, 1])
axs[0, 1].set_title('Nombre d\'Infections par Influenceur')
axs[0, 1].set_xticklabels([])  # Retirer les noms sur l'axe x

# Troisième graphique: Taux d'activité avec taille proportionnelle au nombre de followers
sizes = df['Followers'] * 0.1  # ajuster le facteur de mise à l'échelle si nécessaire
scatter = sns.scatterplot(x='Influenceurs', y='Activité', size='Followers', data=df, sizes=(20, 500), legend=False, hue='Influenceurs', palette=color_map, ax=axs[1, 0])
axs[1, 0].set_title('Taux d\'Activité par Influenceur')
axs[1, 0].set_xticklabels([])  # Retirer les noms sur l'axe x

# Quatrième graphique: Taux de crédibilité avec taille proportionnelle au nombre d'infections
sns.scatterplot(x='Influenceurs', y='Crédibilité', size='Infections', data=df, sizes=(20, 500), legend=False, hue='Influenceurs', palette=color_map, ax=axs[1, 1])
axs[1, 1].set_title('Taux de Crédibilité par Influenceur')
axs[1, 1].set_xticklabels([])  # Retirer les noms sur l'axe x

# Ajouter une légende générale pour la figure
handles, labels = scatter.get_legend_handles_labels()
fig.legend(handles=[plt.Rectangle((0,0),1,1, color=color_map[name]) for name in df['Influenceurs']], title='Influenceurs',
            labels=df['Influenceurs'].tolist())


# Montrer la figure
plt.show()


# Créer le temps (axe x) en supposant que chaque itération représente un "tick" de temps
ticks = list(range(len(data["S"])))

# Tracer le graphe de l'évolution des catégories SIR
plt.figure(figsize=(10, 6))
plt.plot(ticks, data["S"], label="Susceptibles", color="blue")
plt.plot(ticks, data["I"], label="Infectés", color="red")
plt.plot(ticks, data["R"], label="Récupérés", color="green")
plt.xlabel("Temps")
plt.ylabel("Nombre d'individus")
plt.title("Évolution des catégories SIR au cours du temps")
plt.legend()
plt.tight_layout()  # Adjust layout to not cut off labels
plt.show()


sys.exit()