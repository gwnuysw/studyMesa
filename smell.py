from mesa import Model, Agent
from mesa.space import MultiGrid
import numpy as np


class Food(Agent):
    def __init__(self, model, intensity=10):
        super().__init__(model)
        self.intensity = intensity  # Initial smell intensity

    def getSmell(self, y, decay_factor=0.7):
        if self.pos is not None:
            distance = abs(y) - abs(self.pos[1])
            return self.intensity * (decay_factor ** distance)

class SmellGrid:
    def __init__(self, width, height):
        self.grid = np.zeros((width, height))
    '''
    def spread_smell(self, food_agents, decay_factor=0.9):
        """ 음식의 냄새를 퍼뜨리되, 거리에 따라 점진적으로 감소 """
        self.grid.fill(0)
        for food in food_agents:
            x = food.pos[0]
            y = food.pos[1]
            self.grid[x, y] += food.intensity  # 음식이 있는 곳의 기본 냄새 강도

            # 주변으로 확산
            
            #for dx in range(-4, 0):  # 확산 반경 설정
            for dy in range(-4,0):
                dx = 0
                new_x, new_y = x + dx, y + dy
                print("new_y : ", new_y)
                if 0 <= new_y < self.grid.shape[1]:
                    distance = abs(dx) + abs(dy)  # 맨해튼 거리
                    self.grid[new_x, new_y] += food.intensity * (decay_factor ** distance)
                    print("(",new_x,new_y,") 냄새 강도 : ", self.grid[new_x, new_y])
    '''
    
    def get_smell(self, pos):
        x, y = pos
        return self.grid[x, y]