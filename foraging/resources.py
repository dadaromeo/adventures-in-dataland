import random

from mesa.agent import Agent

class Food(Agent):
    
    fully_grown = False
    
    def __init__(self, unique_id, model, pos=None):
        super().__init__(unique_id, model)
        self.pos = pos
    
    def step(self):
        if self.fully_grown:
            self.energy -= self.wilt_rate
        else:
            self.energy += self.growth_rate
        
        if self.energy >= self.max_growth:
            self.fully_grown = True
        
        # new Food
        if self.fully_grown and (self.energy >= self.max_growth):
            neig = self.model.grid.get_neighborhood(self.pos, True, False)
            is_empty = self.model.grid.is_cell_empty
            
            if any(map(is_empty, neig)):
                empty = list(filter(is_empty, neig))
                pos = random.choice(empty)
                food_name = type(self).__name__.lower()
                attr_name = "number_of_{}".format(food_name)
                last = getattr(self.model, attr_name)
                new_food = type(self)(last + 1, self.model)
                self.energy -= new_food.energy
                setattr(self.model, attr_name, last + 1)
                self.model.grid.place_agent(new_food, pos)
                self.model.schedule.add(new_food)
        
        # Death
        if self.energy <= 0:
            food_name = type(self).__name__.lower()
            attr_name = "number_of_{}".format(food_name)
            last = getattr(self.model, attr_name)
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            setattr(self.model, attr_name, last - 1)