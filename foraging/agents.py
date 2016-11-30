import random

from mesa.agent import Agent

from foraging.utils import euclidean
from foraging.resources import Food

class Bug(Agent):
    
    treshold = 15
    metabolism = 1
    energy = 10
    strategy = None
    age = 0
    
    def __init__(self, unique_id, model, pos=None):
        super().__init__(unique_id, model)
        self.pos = pos
        self.move = {"stick": self.stick,
                     "switch": self.switch,
                    }
    
    def step(self):
        self.age += 1
        
        adult = self.age > 5
        old = self.age > 50
        
        if old:
            self.energy -= self.metabolism
        
        self.find_food()
        self.move[self.strategy]()
        
        # new Bug
        has_energy = self.energy >= self.treshold
        if has_energy and (adult):
            neig = self.model.grid.get_neighborhood(self.pos, True, False)
            
            if any(map(self.model.grid.is_cell_empty, neig)):
                empty = list(filter(self.model.grid.is_cell_empty, neig))
                pos = random.choice(empty)
                last = self.model.number_of_bug
                new_bug = Bug(last + 1, self.model)
                new_bug.strategy = self.strategy
                self.energy -= new_bug.energy
                self.model.grid.place_agent(new_bug, pos)
                self.model.schedule.add(new_bug)
                self.model.number_of_bug += 1
            else:
                pos = self.model.grid.find_empty()
                self.move_to(pos)
        
        # Death
        if self.energy <= 0:
            self.die()
    
    def switch(self):  
        neig = self.model.grid.get_neighborhood(self.pos, True, False)
        pos = random.choice(neig)
        if self.model.grid.is_cell_empty(pos):
            self.move_to(pos)
    
    def stick(self):
        neig = self.model.grid.get_neighbors(self.pos, True)
        if not(neig):
            pos = self.model.grid.find_empty()
            self.move_to(pos)
    
    def move_to(self, pos):
        distance = round(euclidean(self.pos, pos))
        cost = self.metabolism * distance
        
        self.model.grid.move_agent(self, pos)
        self.energy -= cost
    
    def find_food(self):
        neig = self.model.grid.get_neighbors(self.pos, True, False)
        if neig:
            agent = random.choice(neig)
            if isinstance(agent, Food):
                self.eat(agent)
    
    def eat(self, food):
        gain = self.age * self.metabolism
        self.energy += gain
        food.energy -= gain
    
    def die(self):
        self.model.grid._remove_agent(self.pos, self)
        self.model.schedule.remove(self)
        self.model.number_of_bug -= 1

class Bean(Food):
    
    density = 0.005
    growth_rate = 4
    wilt_rate = 2
    max_growth = 20
    energy = 4

class Corn(Food):
    
    density = 0.01
    growth_rate = 2
    wilt_rate = 1
    max_growth = 10
    energy = 2

class Soy(Food):
    
    density = 0.001
    growth_rate = 20
    wilt_rate = 10
    max_growth = 100
    energy = 20