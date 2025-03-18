from mesa import Agent
from neuron import hungerSensingCell, predatorSensingCell, eatingCell
import networkx as nx
import random

class Creature(Agent):
    
    def __init__(self, model):

        super().__init__(model)
        self.fullness = 45
        self.predator = 0
        self.smell = 0
        
        self.fullSensingCell = fullSensingCell(model, self)
        self.hungerSensingCell = hungerSensingCell(model, self)
        self.smellSensingCell = smellSensingCell(model, self)
        self.interNueron1 = interNeuron(model, self)
        self.interNeuron2 = interNeuron(model, self)
        self.forwardCell = actingCell(model, self)
        self.backwardCell = actingCell(model, self)
  
        
        self.brain = nx.DiGraph()
        
        self.brain.add_edge(self.fullSensingCell, self.interNeuron1, weight=0.2)
        self.brain.add_edge(self.fullSensingCell, self.interNeuron2, weight=0.2)
        self.brain.add_edge(self.hungerSensingCell, self.interNeuron1, weight=0.2)
        self.brain.add_edge(self.hungerSensingCell, self.interNeuron2, weight=0.2)
        self.brain.add_edge(self.smellSensingCell, self.interNeuron1, weight=0.2)
        self.brain.add_edge(self.smellSensingCell, self.interNeuron2, weight=0.2)
        self.brain.add_edge(self.interNeuron1, self.forwardCell, weight=0.2)
        self.brain.add_edge(self.interNeuron2, self.backwardcell, weight=0.2)

    def reportFullness(self):
        return self.fullness
    
    def reportPredator(self):
        return self.predator
        
    def reportSmell(self):
        return self.smell
        
    def step(self):
        self.fullness -= 1
        
        smell = self.model.smell_grid.get_smell(self.pos)

        # 현재 위치에서 음식이 있는지 확인
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        for obj in cell_contents:
            if isinstance(obj, Food):
                self.model.grid.remove_agent(obj)  # 음식 제거 (먹음)
                self.fullness += 10

        possible_moves = [(0, -1), (1, 0), (-1, 0)]  # 상, 하, 좌, 우 이동
        move = random.choice(possible_moves)  # 랜덤한 방향 선택
        new_x = self.pos[0] + move[0]
        new_y = self.pos[1] + move[1]
        
        if self.forwardCell.fire:
            self.model.grid.move_agent(self, (self.pos[0], self.pos[1]+1))

        
        if self.predatorSensingCell.fire:
            for recv in self.brain.successors(self.predatorSensingCell):
                recv.potential -= 20
                
        if self.hungerSensingCell.fire:
            for recv in self.brain.successors(self.hungerSensingCell):
                recv.potential += 20
