from mesa import Agent
from neuron import hungerSensingCell, predatorSensingCell, eatingCell
import networkx as nx
import random

class Creature(Agent):
    
    def __init__(self, model):

        super().__init__(model)
        self.fullness = 25
        self.predator = 0
        
        self.hungerSensingCell = hungerSensingCell(model, self)
        self.eatingCell = eatingCell(model,self)
        self.predatorSensingCell = predatorSensingCell(model, self)
        
        self.brain = nx.DiGraph()
        
        self.brain.add_nodes_from([(self.hungerSensingCell,self.eatingCell), (self.predatorSensingCell, self.eatingCell)])
        self.brain.add_edge(self.predatorSensingCell, self.eatingCell)
        self.brain.add_edge(self.hungerSensingCell, self.eatingCell)

    def reportFullness(self):
        return self.fullness
    
    def reportPredator(self):
        return self.predator
        
    def step(self):
        self.fullness -= 1
        self.predator = random.choice([0, 1])
        
        if self.predatorSensingCell.fire:
            for recv in self.brain.successors(self.predatorSensingCell):
                recv.potential -= 20
                
        if self.hungerSensingCell.fire:
            for recv in self.brain.successors(self.hungerSensingCell):
                recv.potential += 20
