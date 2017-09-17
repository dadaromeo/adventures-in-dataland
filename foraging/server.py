from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer

from foraging.agents import Bean, Corn, Soy, Bug
from foraging.model import Foraging

width = 50
height = 50

def food_portrayal(agent):
    
    if agent is None:
        return
    
    portrayal = {"Shape": "rect", "Filled": "true", "w": 0.8, "h": 0.8, "Layer": 0}
    
    if type(agent) is Bean:
        portrayal["Color"] = "cornflowerblue"
    
    elif type(agent) is Corn:
        portrayal["Color"] = "blueviolet"
    
    elif type(agent) is Soy:
        portrayal["Color"] = "forestgreen"
    
    elif type(agent) is Bug:
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "tomato"
        portrayal["r"] = 1
        portrayal["Layer"] = 1
    
    return portrayal

bean = {"Label": "Bean", "Color": "cornflowerblue"}
corn = {"Label": "Corn", "Color": "blueviolet"}
soy = {"Label": "Soy", "Color": "forestgreen"}
bug = {"Label": "Bug", "Color": "tomato"}

canvas = CanvasGrid(food_portrayal, width, height)
chart_count = ChartModule([bean, corn, soy, bug])

model_params = {"strategy": "stick"}
server = ModularServer(Foraging, [canvas, chart_count], name="Foraging", model_params)

server.launch()
