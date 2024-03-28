import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import imageio.v2 as imageio
import os

# Fonctions d'aide
def make_gif(networks, name, pos):
    if not os.path.exists("frames"):
        os.makedirs("frames")

    counter = 0
    images = []
    for i, graph in enumerate(networks):
        plt.figure(figsize=(8, 8))
        color = get_color(graph)
        nx.draw(graph, node_color=color, arrowsize=20, pos=pos)
        plt.savefig(f"frames/{counter}.png")
        images.append(imageio.imread(f"frames/{counter}.png"))
        counter += 1
        plt.close()

    imageio.mimsave(name, images)
    for file_name in os.listdir("frames"):
        file_path = os.path.join("frames", file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
    os.rmdir("frames")

def get_color(graph):
    color_dict = {0: "red", 1: "green"}
    color = [color_dict[node[1]['Informed']] for node in graph.nodes(data=True)]
    return color

# Classe Network
class Network:
    def __init__(self):
        self.G = nx.DiGraph()

    def create_source(self):
        self.G.add_node(0, Informed=1)

    def add_node(self):
        index = len(self.G.nodes)
        self.G.add_node(index, Informed=0)

    def add_connection(self, node1, node2):
        self.G.add_edge(node1, node2)
        self.G[node1][node2]["Connection"] = nx.degree_centrality(self.G)[node1]

    def propagate_information(self, resistance):
        for edge in list(self.G.edges):
            rand = np.random.uniform(0, resistance)
            if self.G.nodes[edge[0]]["Informed"] == 1 and rand < self.G[edge[0]][edge[1]]["Connection"]:
                self.G.nodes[edge[1]]["Informed"] = 1

# Simulation
network = Network()
network.create_source()

for _ in range(100):
    network.add_node()

nodes = list(network.G.nodes)
for _ in range(300):
    if _ == 0:
        node1 = nodes[0]
    else:
        node1 = np.random.choice(nodes)
    node2 = np.random.choice(nodes)

    if node1 != node2:
        network.add_connection(node1, node2)

pos = nx.kamada_kawai_layout(network.G)
color = get_color(network.G)

# Affichage du réseau initial
plt.figure(figsize=(10, 10))
nx.draw(network.G, node_color=color, arrowsize=20, pos=pos)

# Propagation de l'information
informed = []
networks = [network.G.copy()]
for _ in range(50):
    network.propagate_information(0.3)
    informed.append(sum(list(dict(network.G.nodes(data="Informed")).values())))
    networks.append(network.G.copy())

# Affichage du réseau final
plt.figure(figsize=(10, 10))
color = get_color(network.G)
nx.draw(network.G, node_color=color, arrowsize=20, pos=pos)

# Courbe de contagion
plt.figure()
t = np.arange(0, len(informed), 1)
plt.plot(t, informed)
plt.xlabel("Temps")
plt.ylabel("Membres Informés")
plt.title("Courbe de Contagion d'Information")
plt.savefig("contagionCurve.png")

# Création du GIF
make_gif(networks, "contagion.gif", pos)
