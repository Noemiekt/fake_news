import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
from scipy.spatial import distance_matrix
import os

class Agent():
    def __init__(self, x, y, infected, resistance, infectedCounter=0):
        self.x = x
        self.y = y
        self.infected = infected
        self.resistance = resistance
        self.infectedCounter = infectedCounter 
        
    def movement(self, stepSize, xBounds, yBounds):
        self.x += stepSize * np.random.uniform(-1, 1)
        self.y += stepSize * np.random.uniform(-1, 1)
        
        if self.x < xBounds[0]:
            self.x = xBounds[0]
        elif self.x > xBounds[1]:
            self.x = xBounds[1]
        
        if self.y < yBounds[0]:
            self.y = yBounds[0]
        elif self.y > yBounds[1]:
            self.y = yBounds[1]
            
        if self.infected:
            self.infectedCounter -= 1
            if self.infectedCounter <= 0:
                self.infected = False
        
    def infect(self):
        infectRoll = np.random.uniform()
        if not self.infected and infectRoll > self.resistance:
            self.infected = True
            self.infectedCounter = 50
            self.resistance *= 1.5

def get_position(agents):
    positions = np.array([[agent.x, agent.y] for agent in agents])
    return positions

def move_agents(agents, stepSize, xBounds, yBounds):
    for agent in agents:
        agent.movement(stepSize, xBounds, yBounds)
    return agents

def get_infected(agents):
    return [agent.infected for agent in agents]

def get_close_agents(distanceMatrix, agentNumber):
    sort = np.argsort(distanceMatrix[agentNumber])
    closeMask = distanceMatrix[agentNumber][sort] < 10
    closeAgents = np.argsort(distanceMatrix[agentNumber])[closeMask][1:]
    return closeAgents

def roll_infect(agents):
    positions = get_position(agents)
    distanceMatrix = distance_matrix(positions, positions)
    for i, agent in enumerate(agents):
        closeAgents = get_close_agents(distanceMatrix, i)
        for j in closeAgents:
            if agents[j].infected:
                agent.infect()
    return agents

def make_gif(frames, name):
    if not os.path.exists("frames"):
        os.makedirs("frames")
    
    counter = 0
    images = []
    for i, frame in enumerate(frames):
        plt.figure(figsize=(6, 6))
        plt.scatter(frame[0], frame[1], c=frame[2], cmap="RdYlGn_r")
        plt.title("Infected = " + str(np.sum(frame[2])))
        plt.tick_params(left=False, right=False, labelleft=False, labelbottom=False, bottom=False)
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


agents = [Agent(np.random.uniform(0, 500), np.random.uniform(0, 500), 0, 0.3) for _ in range(500)]
for agent in agents[:10]:
    agent.infected = 1
    agent.infectedCounter = 50
    
stepSize = 5
xBounds = [0, 500]
yBounds = [0, 500]

frames = []
for _ in range(500):
    agents = move_agents(agents, stepSize, xBounds, yBounds)
    agents = roll_infect(agents)
    positions = get_position(agents)
    infected = get_infected(agents)
    frames.append([positions[:, 0], positions[:, 1], infected])
    
make_gif(frames, "Simulation.gif")
