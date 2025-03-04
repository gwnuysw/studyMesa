from mesa import Agent

class Neuron(Agent):

    def __init__(self, model):
        super().__init__(model)
        self.potential = 0
        self.threshold = 50
        self.fire = False
    
    def resetPotential(self):
        if self.fire:
            self.potential = 0

class eatingCell(Neuron):

    def __init__(self, model, creature):
        super().__init__(model)
        self.creature = creature
    def step(self):
        if self.threshold < self.potential:
            self.fire = True
            self.creature.fullness += 10
            self.resetPotential()
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

class predatorSensingCell(Neuron):
    def __init__(self, model, creature):
        super().__init__(model)
        self.creature = creature

    def step(self):
        if self.creature.predator == 1:
            self.fire = True
        else:
            self.fire = False