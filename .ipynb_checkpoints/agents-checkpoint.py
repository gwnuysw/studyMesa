from mesa import Agent
import neuron
import networkx as nx
import random
from smell import Food

class Creature(Agent):
    
    def __init__(self, model):
        super().__init__(model)

        #Creatur의 State
        self.fullness = 45
        self.prevFullness = self.fullness
        # Report용 속성
        self.smellup = 0
        self.smelldown = 0
        
        self.smellWeight1 = 0
        self.fullWeight1 = 0

        self.smellWeight2 = 0
        self.fullWeight2 = 0
        
        self.interNeuron1Pt = 0
        self.interNeuron2Pt = 0

        #뇌세포 생성
        self.fullSensingCellup = neuron.fullSensingCell(model, self)
        self.smellSensingCellup = neuron.smellSensingCellup(model, self)
        self.fullSensingCelldown = neuron.fullSensingCell(model, self)
        self.smellSensingCelldown = neuron.smellSensingCelldown(model, self)
        
        self.interNeuron1 = neuron.interNeuron(model, self)
        self.interNeuron2 = neuron.interNeuron(model, self)
        
        self.forwardCell = neuron.actingCell(model, self)
        self.backwardCell = neuron.actingCell(model, self)

        #뇌세포 연결
        self.brain = nx.DiGraph()
        
        self.brain.add_edge(self.fullSensingCellup, self.interNeuron1, weight=0.2)
        self.brain.add_edge(self.smellSensingCellup, self.interNeuron1, weight=0.2)
        self.brain.add_edge(self.interNeuron1, self.forwardCell, weight=0.2)
        
        self.brain.add_edge(self.fullSensingCelldown, self.interNeuron2, weight=0.2)
        self.brain.add_edge(self.smellSensingCelldown, self.interNeuron2, weight=0.2)
        self.brain.add_edge(self.interNeuron2, self.backwardCell, weight=0.2)

    def reportFullness(self):
        return self.fullness
    
    def reportPredator(self):
        return self.predator
        
    def reportSmell(self):
        return self.smellup, self.smelldown

    def reportWeight1(self):
        return self.smellWeight1, self.fullWeight1

    def reportWeight2(self):
        return self.smellWeight2, self.fullWeight2

    def reportPotential(self):
        return self.interNeuron1Pt, self.interNeuron2Pt

    def eating(self, posX, posY):
        # 현재 위치에서 음식이 있는지 확인
        cell_contents = self.model.grid.get_cell_list_contents([(posX, posY)])
        for obj in cell_contents:
            if isinstance(obj, Food):
                print(obj," is removed")
                self.model.grid.remove_agent(obj)  # 음식 제거 (먹음)
                self.prevFullness = self.fullness
                self.fullness += 10
                print("model set food")
                self.model.setFood(self.model.width, self.model.height)

    def step(self):
        self.fullness -= 5

        # agent의 상단 냄새, 위가 없으면 상단의 냄새는 0이다.
        if self.pos[1] == 4:
            self.smellup = 0
        else:
            self.smellup = self.model.food.getSmell(self.pos[1]+1)
            self.eating(self.pos[0], self.pos[1]+1)

        # agent의 하단 냄새, 아래가 없으면 하단의 냄새는 0이다.
        if self.pos[1] == 0:
            self.smelldown = 0
        else:
            self.smelldown = self.model.food.getSmell(self.pos[1]-1)
            self.eating(self.pos[0], self.pos[1]-1)
            
        print("(",self.pos[0],self.pos[1],")", "smellup : ",self.smellup)
        print("(",self.pos[0],self.pos[1],")", "smelldown : ",self.smelldown)

        
        if self.pos[1] == 4:
            if self.backwardCell.fire == True:
                self.model.grid.move_agent(self, (self.pos[0], self.pos[1]-1))
                print("##pos Top End : ", self.pos[0],", ", self.pos[1])
        elif self.pos[1] == 0:
            if self.forwardCell.fire == True:
                self.model.grid.move_agent(self, (self.pos[0], self.pos[1]+1))
                print("##pos bottom End : ", self.pos[0],", ", self.pos[1])
        else:
            if self.forwardCell.fire == True:    
                self.model.grid.move_agent(self, (self.pos[0], self.pos[1]+1))
                print("forwardCell fired ", self.forwardCell.fire)
            elif self.backwardCell.fire == True:
                self.model.grid.move_agent(self, (self.pos[0], self.pos[1]-1))
                print("backwardCell fired", self.backwardCell.fire)

        '''
        possible_moves = [(0, 1), (0, -1), (0, 0)]  # 상, 하, 좌, 우, 제자리 이동
        move = random.choice(possible_moves)  # 랜덤한 방향 선택
        new_x = self.pos[0] + move[0]
        new_y = self.pos[1] + move[1]
        '''

        self.fullWeight1 = self.brain[self.fullSensingCellup][self.interNeuron1]['weight']
        self.smellWeight1 = self.brain[self.smellSensingCellup][self.interNeuron1]['weight']
        self.interNeuron1Pt = self.interNeuron1.potential
        
        self.fullWeight2 = self.brain[self.fullSensingCelldown][self.interNeuron2]['weight']
        self.smellWeight2 = self.brain[self.smellSensingCelldown][self.interNeuron2]['weight']
        self.interNeuron2Pt = self.interNeuron2.potential