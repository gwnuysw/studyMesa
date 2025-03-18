from mesa import Agent

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
        incoming_edges = self.creature.brain.incoming_edges(self,data=True)
        for source, target, attrs in incoming_edges:
            if source.fire = True:
                self.potential += attrs['weight']
                if self.potential >= self.threshold:
                    attrs['weight'] += 0.05
                else:
                    attrs['weight'] -= 0.05
            
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
        incoming_edges = self.creature.brain.incoming_edges(self,data=True)
        for source, target, attrs in incoming_edges:
            if source.fire = True:
                self.potential += 0.9

        if self.threshold <= self.potential:
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

class smellSensingCell(Neuron):
    def __init__(self, model, creature):
        super().__init__(model)
        self.creature = creature
    def step(self):
        if self.creature.smell > 5:
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
        if self.creature.fullness >= 30:
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