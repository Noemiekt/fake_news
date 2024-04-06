import json
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import random



# Load the data from the JSON file
with open('json_co_v5.json', 'r') as file:
    data = json.load(file)

# Extract influencers and students
influencers = data['influencers']
students = data['students']

# Créer le graphe du réseau social
G = nx.DiGraph()

# Ajouter les nœuds (utilisateurs)
for student in students:
    G.add_node(student['username'], type='student', state='S')

for influencer in influencers:
    G.add_node(influencer['username'], type='influencer', state='S',
               credibility=influencer['credibility'], activity_rate=influencer['activity_rate'])
    # Add edges from influencer to followers (students)
    for follower in influencer['followers']:
        G.add_edge(influencer['username'], follower['username'])

# Add edges between students based on their followers
for student in students:
    for follower in student['followers']:
        G.add_edge(student['username'], follower)


# G est déjà votre graphe NetworkX initialisé

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


# Fonction pour mettre à jour l'état des nœuds et visualiser le graphe
def update_states_and_visualize(G, pos, nodes_to_infect, step):
    # Mettre à jour l'état des nœuds
    for node in nodes_to_infect:
        if node in G.nodes:
            G.nodes[node]['state'] = 'I'

    # Définition des arêtes (similaire à ce qui a été fait plus haut)
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
    node_text = []  # Texte pour afficher lors du survol
    node_color = []  # Couleur des nœuds basée sur leur état

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(f'{node}: {G.nodes[node]["state"]}')
        # Couleur en fonction de l'état
        if G.nodes[node]['state'] == 'I':
            node_color.append('red')
        elif G.nodes[node]['state'] == 'S':
            node_color.append('blue')
        elif G.nodes[node]['state'] == 'R':
            node_color.append('green')  

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        hoverinfo='text',
        marker=dict(
            color=node_color,
            size=10,
            line_width=2))

    # Création et affichage de la figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    fig.update_layout(title_text=f"Étape {step}")
    fig.show()


# Exécuter la simulation
def simulate_disinformation_spread(G, posts, steps=3):
    infected_at_t0 = set()
    initial_sharers = set()  # Sharers initiales
    second_sharers = set()  # Second sharers

    # t=0: Marquez les influenceurs avec des fake news comme infectés ('I')
    for post in posts:
        if post['is_fake_news']:
            influencer_username = next(
                (influencer['username'] for influencer in data['influencers'] if influencer['influencer_id'] == post['influencer_id']), None
            )
            if influencer_username:
                infected_at_t0.add(influencer_username)

    # Mettre à jour l'état et visualiser le graphe à t=0
    update_states_and_visualize(G, pos, infected_at_t0, 0)

    # t+1: Identifier les "sharers initiaux" et les infecter
    for post in posts:
        if post['is_fake_news']:
            # Construire la liste des receivers pour tous les partages
            all_receivers = {receiver['username'] for share in post['shares'] for receiver in share['to']}
            
            for share in post['shares']:
                sharer = share['username']
                # Si le sharer n'est pas un receiver, c'est un "sharer initial"
                if sharer not in all_receivers:
                    initial_sharers.add(sharer)
                else:
                    # Sinon, c'est un "second sharer"
                    second_sharers.add(sharer)

    # Mettre à jour l'état et visualiser le graphe à t+1
    update_states_and_visualize(G, pos, initial_sharers, 1)

    # t+2: Infectez les "second sharers" et les likers des "sharers initiaux"
    for sharer in initial_sharers:
        if sharer in G:
            for receiver_username in G.successors(sharer):  # Utilisez successors pour trouver les followers
                if receiver_username in second_sharers or any(like['username'] == receiver_username for like in post['likes']):
                    G.nodes[receiver_username]['state'] = 'I'

    # Mettre à jour l'état et visualiser le graphe à t+2
    update_states_and_visualize(G, pos, second_sharers, 2)
    

# Lancer la simulation avec le graphe statique et la logique de propagation basée sur les données JSON
simulate_disinformation_spread(G, data['posts'])
































# import json
# import networkx as nx
# import matplotlib.pyplot as plt
# import plotly.graph_objects as go
# import random

# # Charger les données JSON
# with open('json_co_v5.json', 'r') as file:
#     data = json.load(file)

# # Créer le graphe du réseau social
# G = nx.DiGraph()

# # Ajouter les nœuds (utilisateurs)
# for student in data['students']:
#     G.add_node(student['username'], type='student', state='S')

# for influencer in data['influencers']:
#     G.add_node(influencer['username'], type='influencer', state='S', 
#                credibility=influencer['credibility'], activity_rate=influencer['activity_rate'])
    


# # Ajouter les arêtes (relations de suivi)
# for influencer in data['influencers']:
#     for follower in influencer['followers']:
#         G.add_edge(influencer['username'], follower['username'])



# # Supposons que G est déjà votre graphe NetworkX initialisé

# # Créez la position des nœuds en utilisant l'algorithme de mise en page de votre choix
# pos = nx.spring_layout(G)


# # Définition des arêtes
# edge_x = []
# edge_y = []
# for edge in G.edges():
#     x0, y0 = pos[edge[0]]
#     x1, y1 = pos[edge[1]]
#     edge_x.extend([x0, x1, None])
#     edge_y.extend([y0, y1, None])

# edge_trace = go.Scatter(
#     x=edge_x, y=edge_y,
#     line=dict(width=0.5, color='#888'),
#     hoverinfo='none',
#     mode='lines')

# # Définition des nœuds
# node_x = []
# node_y = []
# node_text = []  # Stocke le texte à afficher lors du survol d'un nœud
# for node in G.nodes():
#     x, y = pos[node]
#     node_x.append(x)
#     node_y.append(y)
#     # Ajouter le texte à afficher lors du survol
#     node_info = f"{node}"
#     node_text.append(node_info)

# node_trace = go.Scatter(
#     x=node_x, y=node_y,
#     mode='markers+text',  # Ajouter du texte aux marqueurs
#     hoverinfo='text',
#     text=node_text,  # Le texte à afficher sur le survol
#     textposition="top center",
#     marker=dict(
#         showscale=True,
#         colorscale='YlGnBu',
#         reversescale=True,
#         color=[],
#         size=10,
#         colorbar=dict(
#             thickness=15,
#             title='Niveau de Confiance',
#             xanchor='left',
#             titleside='right'
#         ),
#         line_width=2))

# # Couleurs des nœuds basées sur l'attribut 'state'
# node_adjacencies = []
# for node, adjacencies in enumerate(G.adjacency()):
#     node_adjacencies.append(len(adjacencies[1]))

# node_trace.marker.color = node_adjacencies

# # Créer la figure
# fig = go.Figure(data=[edge_trace, node_trace],
#                 layout=go.Layout(
#                     showlegend=False,
#                     hovermode='closest',
#                     margin=dict(b=0,l=0,r=0,t=0),
#                     xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
#                     yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
#                 )

# fig.show()


# # # Fonction pour mettre à jour l'état des nœuds et visualiser le graphe
# # def update_states_and_visualize(G, nodes_to_infect, step):
# #     for node in nodes_to_infect:
# #         if node in G.nodes:
# #             G.nodes[node]['state'] = 'I'
# #     # Visualisation du graphe avec les états mis à jour
# #     color_map = {'S': 'blue', 'I': 'red', 'R': 'green'}
# #     node_colors = [color_map[G.nodes[node]['state']] for node in G.nodes()]
# #     plt.figure(figsize=(12, 8))
# #     plt.title(f"Step {step}")
# #     nx.draw_networkx(G, node_color=node_colors, with_labels=True, arrowstyle='->', arrowsize=10)
# #     plt.show()

# def update_states_and_visualize(G, pos, nodes_to_infect, step):
#     # Mettre à jour l'état des nœuds
#     for node in nodes_to_infect:
#         if node in G.nodes:
#             G.nodes[node]['state'] = 'I'

#     # Définition des arêtes (similaire à ce qui a été fait plus haut)
#     edge_x = []
#     edge_y = []
#     for edge in G.edges():
#         x0, y0 = pos[edge[0]]
#         x1, y1 = pos[edge[1]]
#         edge_x.extend([x0, x1, None])
#         edge_y.extend([y0, y1, None])

#     edge_trace = go.Scatter(
#         x=edge_x, y=edge_y,
#         line=dict(width=0.5, color='#888'),
#         hoverinfo='none',
#         mode='lines')

#     # Définition des nœuds
#     node_x = []
#     node_y = []
#     node_text = []  # Texte pour afficher lors du survol
#     node_color = []  # Couleur des nœuds basée sur leur état

#     for node in G.nodes():
#         x, y = pos[node]
#         node_x.append(x)
#         node_y.append(y)
#         node_text.append(f'{node}: {G.nodes[node]["state"]}')
#         # Couleur en fonction de l'état
#         if G.nodes[node]['state'] == 'I':
#             node_color.append('red')
#         elif G.nodes[node]['state'] == 'S':
#             node_color.append('blue')
#         else:
#             node_color.append('green')  # Pour d'autres états potentiels

#     node_trace = go.Scatter(
#         x=node_x, y=node_y,
#         mode='markers+text',
#         text=node_text,
#         hoverinfo='text',
#         marker=dict(
#             color=node_color,
#             size=10,
#             line_width=2))

#     # Création et affichage de la figure
#     fig = go.Figure(data=[edge_trace, node_trace],
#                     layout=go.Layout(
#                         showlegend=False,
#                         hovermode='closest',
#                         margin=dict(b=0, l=0, r=0, t=0),
#                         xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
#                         yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
#                     )
#     fig.update_layout(title_text=f"Étape {step}")
#     fig.show()


# # Exécuter la simulation
# def simulate_disinformation_spread(G, posts, steps=3):
#     infected_at_t0 = set()
#     initial_sharers = set()  # Sharers initiales
#     second_sharers = set()  # Second sharers

#     # t=0: Marquez les influenceurs avec des fake news comme infectés ('I')
#     for post in posts:
#         if post['is_fake_news']:
#             influencer_username = next(
#                 (influencer['username'] for influencer in data['influencers'] if influencer['influencer_id'] == post['influencer_id']), None
#             )
#             if influencer_username:
#                 infected_at_t0.add(influencer_username)

#     # Mettre à jour l'état et visualiser le graphe à t=0
#     update_states_and_visualize(G, pos, infected_at_t0, 0)

#     # t+1: Identifier les "sharers initiaux" et les infecter
#     for post in posts:
#         if post['is_fake_news']:
#             # Construire la liste des receivers pour tous les partages
#             all_receivers = {receiver['username'] for share in post['shares'] for receiver in share['to']}
            
#             for share in post['shares']:
#                 sharer = share['username']
#                 # Si le sharer n'est pas un receiver, c'est un "sharer initial"
#                 if sharer not in all_receivers:
#                     initial_sharers.add(sharer)
#                 else:
#                     # Sinon, c'est un "second sharer"
#                     second_sharers.add(sharer)

#     # Mettre à jour l'état et visualiser le graphe à t+1
#     update_states_and_visualize(G, pos, initial_sharers, 1)

#     # t+2: Infectez les "second sharers" et les likers des "sharers initiaux"
#     for sharer in initial_sharers:
#         if sharer in G:
#             for receiver_username in G.successors(sharer):  # Utilisez successors pour trouver les followers
#                 if receiver_username in second_sharers or any(like['username'] == receiver_username for like in post['likes']):
#                     G.nodes[receiver_username]['state'] = 'I'

#     # Mettre à jour l'état et visualiser le graphe à t+2
#     update_states_and_visualize(G, pos, second_sharers, 2)

# # Lancer la simulation avec le graphe statique et la logique de propagation basée sur les données JSON
# simulate_disinformation_spread(G, data['posts'])
