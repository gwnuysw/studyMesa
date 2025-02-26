from mesa import Agent
from neuron import hungerSensingCell, predatorSensingCell, eatingCell
import networkx as nx
#아직 개발중
class Creature(Agent):
    
    def __init__(self, model):

        super().__init__(model)
        self.fullness = 25
        self.hungerSensingCell = hungerSensingCell()
        self.predatorSensingCell = predatorSensingCell()
        self.eatingCell = eatingCell()
        
        brain = nx.Graph()
        brain.add_nodes_from([self.hungerSensingCell, self.predatorSensingCell, self.eatingCell])

        brain.add_edge_from([(self.hungerSensingCell, self.eatingCell), (self.predatorSensingCell, self.eatingCell)])
        
    def step(self):
        self.fullness -= 1