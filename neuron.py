from mesa import Agent

class Neuron(Agent):

    def __init__(self, model):
        super().__init__(model)
        self.potential = 0
        self.threshold = 50
        self.fire = False
    
    def resetPotential():
        if self.fire:
            self.potential = 0

class eatingCell(Neuron):

    def __init__(self, model, creature):
        super().__init__(model)

    def step():
        if self..threshold < self.potential:
            self.fire = True
            self.creature.fullness += 5
        else:
            sel.fire = False
            
class hungerSensingCell(Neuron):
    def __init__(self, model, creature):
        super().__init__(model)
        
    def step():
        if self.creature.fullness <= 20:
            self.fire = Ture
        else:
            self.fire = False

class predatorSensingCell(Neuron):
    def __init__(self, model, creature):
        super().__init__(model)
        
    def isPredator(predatorFlag):
        if predatorFlag:
            self.potential += 20
        else:
            self.potential -= 20
            
    def step():
        if self.threshold < potential:
            self.fire = True
        else:
            self.fire = False