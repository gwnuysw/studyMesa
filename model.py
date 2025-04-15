from mesa import Model
from mesa.datacollection import DataCollector
from agents import Creature
from mesa.space import MultiGrid
from smell import SmellGrid, Food

class NeuralNet(Model):

    def __init__(self, width=10, height=10, seed=None):
        super().__init__(seed=seed)
        self.fullness = 1
        self.width = width
        self.height = height
        self.smellup = 0
        self.smelldown = 0
        
        self.smellWeight1 = 0
        self.fullWeight1 = 0

        self.smellWeight2 = 0
        self.fullWeight2 = 0

        self.interNeuron1PT = 0
        self.interNeuron2PT = 0
        
        self.grid = MultiGrid(self.width, self.height, torus=False)
        #self.smell_grid = SmellGrid(self.width, self.height)
        
        # Set up data collection
        self.datacollector = DataCollector(
            model_reporters={"Fullness":"fullness", "SmellUp":"smellup", "SmellDown":"smelldown", "fullWeight1":"fullWeight1", "SmellWeight1":"smellWeight1", "forward PT":"interNeuron1PT", "backward PT":"interNeuron2PT", "fullWeight2":"fullWeight2", "SmellWeight2":"smellWeight2"},
            agent_reporters={},
        )

        self.agent = Creature(self)
        self.grid.place_agent(self.agent, (0, 0))
        
        self.food = Food(self)
        self.grid.place_agent(self.food, (0, 1))
        
        self.running = True
        self.datacollector.collect(self)

    def setFood(self, width, height):
        self.food = Food(self)
        x, y = self.random.randrange(width), self.random.randrange(height)
        cell_contents = self.grid.get_cell_list_contents([(x, y)])
        
        for obj in cell_contents:
            if isinstance(obj, Creature):
                if y == 0:
                    y += 1
                elif y == 4:
                    y -= 1
                    
        self.grid.place_agent(self.food, (x, y))
        
    def step(self):
        # Update smell grid
        if self.food.pos is None:
            print("model set food")
            self.setFood(self.width, self.height)
            
        self.fullness = self.agent.reportFullness()
        self.smellup, self.smelldown = self.agent.reportSmell()
        self.smellWeight1, self.fullWeight1 = self.agent.reportWeight1()
        self.smellWeight2, self.fullWeight2 = self.agent.reportWeight2()
        self.interNeuron1PT, self.interNeuron2PT = self.agent.reportPotential()
        
        self.agents.shuffle_do("step")  # Activate all agents in random order
        self.datacollector.collect(self)  # Collect data
