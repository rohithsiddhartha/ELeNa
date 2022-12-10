import sys
import osmnx as ox
import networkx as nx
sys.path.insert(1, sys.path[0][:-5])
import pickle as p
import geopy
import math
from src.controller.ShortestPathController import ShortestPathController
from src.controller.AlgorithmController import AlgorithmController
from src.controller.RouteController import RouteController
from src.model.map_model import Graph
from src.view.view import MapView

def Test(value = ""):
    def temp(function):
        def condition(*args, **kwargs):
            try:
                function(*args,**kwargs)
                print("Test case passed.." ) # if a condition passes
                print()
            except Exception as error:
                print(error)
                print("Test case failed..") # if a condition failed
                print()
        return condition
    return temp

@Test("")
def test_get_graph(end):
    print("# Testing the get_graph method in MapGraphModel.py......")

    G = Graph().get_graph(end)
    assert isinstance(G, nx.classes.multidigraph.MultiDiGraph)

@Test("")
def test_get_shortest_path():

    print("# Testing get_shortest_path method in ShortestPathController......") 

    startpt=(42.3732216,-72.5198537)
    endpt =(42.4663727,-72.5795115)
    G = Graph().get_graph(endpt)
    controller = ShortestPathController(G)
    shortest_path = controller.get_shortest_path(startpt,endpt)
    assert abs(shortest_path.get_distance()-11956.737999999996)<=100


if __name__ == "__main__":
    start, end = (42.3732216,-72.5198537), (42.4663727,-72.5795115)
    # Tests #####
    test_get_graph(end)
    test_get_shortest_path()