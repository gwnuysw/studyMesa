from mesa import Model
from mesa.datacollection import DataCollector
from agents import Creature
from mesa.space import MultiGrid


class NeuralNet(Model):


    def __init__(self, width=10, height=10, seed=None):
        super().__init__(seed=seed)
        self.fullness = 1
        self.predator = 0
        self.grid = MultiGrid(width, height, torus=True)

        # Set up data collection
        self.datacollector = DataCollector(
            model_reporters={"Fullness":"fullness", "Predator":"predator"},
            agent_reporters={},
        )

        self.agent = Creature(self)
        self.grid.place_agent(self.agent, (2, 2))
        
        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.fullness = self.agent.reportFullness()
        self.predator = self.agent.reportPredator()
        self.agents.shuffle_do("step")  # Activate all agents in random order
        self.datacollector.collect(self)  # Collect data
