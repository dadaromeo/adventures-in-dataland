from mesa.model import Model
from mesa.space import SingleGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from foraging.agents import Bean, Corn, Soy, Bug

class Foraging(Model):
    
    number_of_bean = 0
    number_of_corn = 0
    number_of_soy = 0
    
    def __init__(self, width=50, height=50, torus=True, num_bug=50, seed=42, strategy=None):
        super().__init__(seed=seed)
        self.number_of_bug = num_bug
        if not(strategy in ["stick", "switch"]):
            raise TypeError("'strategy' must be one of {stick, switch}")
        self.strategy = strategy
        
        self.grid = SingleGrid(width, height, torus)
        self.schedule = RandomActivation(self)
        data = {"Bean": lambda m: m.number_of_bean,
                "Corn": lambda m: m.number_of_corn,
                "Soy": lambda m: m.number_of_soy,
                "Bug": lambda m: m.number_of_bug,
                }
        self.datacollector = DataCollector(data)
        
        # create foods
        self._populate(Bean)
        self._populate(Corn)
        self._populate(Soy)
        
        # create bugs
        for i in range(self.number_of_bug):
            pos = self.grid.find_empty()
            bug = Bug(i, self)
            bug.strategy = self.strategy
            self.grid.place_agent(bug, pos)
            self.schedule.add(bug)
    
    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        
        if not(self.grid.exists_empty_cells()):
            self.running = False
    
    def _populate(self, food_type):
        prefix = "number_of_{}"
        
        counter = 0
        while counter < food_type.density * (self.grid.width * self.grid.height):
            pos = self.grid.find_empty()
            food = food_type(counter, self)
            self.grid.place_agent(food, pos)
            self.schedule.add(food)
            food_name = food_type.__name__.lower()
            attr_name = prefix.format(food_name)
            val = getattr(self, attr_name)
            val += 1
            setattr(self, attr_name, val)
            counter += 1