from mesa import Model
from mesa.datacollection import DataCollector
from agents import Creature
from mesa.space import MultiGrid
from smell import SmellGrid, Food

class NeuralNet(Model):

    def __init__(self, width=10, height=10, seed=None):
        super().__init__(seed=seed)
        self.fullness = 1
        self.predator = 0
        self.grid = MultiGrid(width, height, torus=True)

        # Set up data collection
        self.datacollector = DataCollector(
            model_reporters={"Fullness":"fullness", "Smell":"smell"},
            agent_reporters={},
        )

        self.agent = Creature(self)
        self.grid.place_agent(self.agent, (2, 2))
        food = Food(i, self)
        x, y = self.random.randrange(width), self.random.randrange(height)
        self.grid.place_agent(food, (x, y))
        
        self.running = True
        self.datacollector.collect(self)

    def step(self):
        # Update smell grid
        food_agents = [agent for agent in self.schedule.agents if isinstance(agent, Food)]
        self.smell_grid.spread_smell(food_agents)
        
        self.fullness = self.agent.reportFullness()
        #self.predator = self.agent.reportPredator()
        self.smell = self.agent.reportSmell()
        self.agents.shuffle_do("step")  # Activate all agents in random order
        self.datacollector.collect(self)  # Collect data
