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

@Test("")
def test_calculate_elevation_path():
    print("# Testing calculate_elevation_path method in AlgorithmsController....")
    startpt=(42.3732216,-72.5198537)
    endpt =(42.4663727,-72.5795115)
    G = Graph().get_graph(endpt)
    s_controller = ShortestPathController(G)
    shortest_path = s_controller.get_shortest_path(startpt,endpt)
    controller = AlgorithmController(G,shortest_path.get_distance(),float(150) / 100.0,"max",shortest_path.get_origin(),shortest_path.get_destination(),1,2)
    elevation_path=controller.calculate_elevation_path(G, shortest_path.get_origin(), shortest_path.get_destination(), None,weight=lambda u, v, d:
                                              math.exp(1 * d[0]['length'] * (
                                                          d[0]['grade'] + d[0]['grade_abs']) / 2)
                                              + math.exp((1 / 100) * d[0]['length']))
    print("elev path",elevation_path[0])
    assert elevation_path[0]==66704169
    assert elevation_path[1]==6302552856

@Test("")
def test_fetch_elevation():
    print("# Testing fetch_route_with_elevation method in AlgorithmsController....")
    startpt=(42.3732216,-72.5198537)
    endpt =(42.4663727,-72.5795115)
    G = Graph().get_graph(endpt)
    s_controller = ShortestPathController(G)
    shortest_path = s_controller.get_shortest_path(startpt,endpt)
    controller = AlgorithmController(G,shortest_path.get_distance(),float(150) / 100.0,"max",shortest_path.get_origin(),shortest_path.get_destination(),1,2)
    elevation_path=controller.fetch_route_with_elevation()
    assert abs(elevation_path.get_gain()-45.797)<=100

if __name__ == "__main__":
    start, end = (42.3732216,-72.5198537), (42.4663727,-72.5795115)
    # Tests #####
    test_get_graph(end)
    test_get_shortest_path()
    test_calculate_elevation_path()
    test_fetch_elevation()