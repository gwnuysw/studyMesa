from mesa import Agent
import random
class Neuron(Agent):

    def __init__(self, model):
        super().__init__(model)
        self.potential = 0
        self.threshold = 0.8
        self.fire = False
    
    def resetPotential(self):
        self.potential /= 2

class interNeuron(Neuron):
    def __init__(self, model, creature):
        super().__init__(model)
        self.creature = creature
    def step(self):
        incoming_edges = self.creature.brain.in_edges(self,data=True)
        for source, target, attrs in incoming_edges:
            if source.fire == True:
                if self.potential <= 1:
                    self.potential += attrs['weight'] * 2
                
        for source, target, attrs in incoming_edges:
            if source.fire == True:
                if self.potential >= self.threshold:
                    if attrs['weight'] <= 1.5:
                        attrs['weight'] += 0.2
                else:
                    if attrs['weight'] >= 0.3:
                        attrs['weight'] -= 0.2
        if self.threshold <= self.potential:
            self.fire = True
        else:
            self.fire = False

        self.resetPotential()

class actingCell(Neuron):

    def __init__(self, model, creature):
        super().__init__(model)
        self.creature = creature
    def step(self):
        incoming_edges = self.creature.brain.in_edges(self,data=True)
        for source, target, attrs in incoming_edges:
            if source.fire == True:
                self.potential += 0.9
        if self.threshold <= self.potential:
            self.fire = True
        else:
            self.fire = False

        self.resetPotential()

class eatingCell(Neuron):

    def __init__(self, model, creature):
        super().__init__(model)
        self.creature = creature
    def step(self):
        if self.threshold <= self.potential:
            self.fire = True
            self.creature.fullness += 10
            self.resetPotential()
        else:
            self.fire = False

class smellSensingCellup(Neuron):
    def __init__(self, model, creature):
        super().__init__(model)
        self.creature = creature
    def step(self):
        if self.creature.smellup > 4:
            self.fire = True
        else:
            self.fire = False

class smellSensingCelldown(Neuron):
    def __init__(self, model, creature):
        super().__init__(model)
        self.creature = creature
        
    def step(self):
        if self.creature.smelldown > 4:
            self.fire = True
        else:
            self.fire = False
            
class hungerSensingCell(Neuron):
    def __init__(self, model, creature):
        super().__init__(model)
        self.creature = creature
    def step(self):
        if self.creature.fullness <= 20:
            self.fire = True
        else:
            self.fire = False

class fullSensingCell(Neuron):
    def __init__(self, model, creature):
        super().__init__(model)
        self.creature = creature
    def step(self):
        if self.creature.prevFullness < self.creature.fullness:
            self.fire = True
        else:
            self.fire = False

class predatorSensingCell(Neuron):
    def __init__(self, model, creature):
        super().__init__(model)
        self.creature = creature

    def step(self):
        if self.creature.predator == 1:
            self.fire = True
        else:
            self.fire = False