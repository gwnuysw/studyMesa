from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import numpy as np


class Food(Agent):
    def __init__(self, unique_id, model, intensity=10):
        super().__init__(unique_id, model)
        self.intensity = intensity  # Initial smell intensity

class SmellGrid:
    def __init__(self, width, height):
        self.grid = np.zeros((width, height))
    
    def spread_smell(self, food_agents, decay_factor=0.9):
        """ 음식의 냄새를 퍼뜨리되, 거리에 따라 점진적으로 감소 """
        self.grid.fill(0)

        for food in food_agents:
            x, y = food.pos
            self.grid[x, y] += food.intensity  # 음식이 있는 곳의 기본 냄새 강도

            # 주변으로 확산
            for dx in range(-2, 3):  # 확산 반경 설정
                for dy in range(-2, 3):
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < self.grid.shape[0] and 0 <= new_y < self.grid.shape[1]:
                        distance = abs(dx) + abs(dy)  # 맨해튼 거리
                        self.grid[new_x, new_y] += food.intensity * (decay_factor ** distance)
    
    def get_smell(self, pos):
        x, y = pos
        return self.grid[x, y]