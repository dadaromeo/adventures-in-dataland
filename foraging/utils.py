import math

def euclidean(u, v):
    """The euclidean distance between two points."""
    
    x,y = u
    i,j = v
    return math.sqrt((x-i)**2 + (y-j)**2)