import math
import osmnx as ox
from heapq import heappush, heappop
from itertools import count
from networkx.algorithms.shortest_paths.weighted import _weight_function
from src.model.algo_model import AlgorithmModel
from src.model.path_model import *
import networkx as nx

MAXIMIZE = "max"
MINIMIZE = "min"
EMPTY = "empty"
LENGTH = "length"
ELEVATION_GAIN = "elevation_gain"


class AlgorithmController():
    """
    Controller Class to compute the shortest path with elevation using the chosen algorithm.
    """

    def __init__(self, graph, shortest_dist, path_limit, elevation_strategy, source, destination, elevation_gain,
                 algo_flag):
        """
        inti method: initializes the  class attributes
        """

        self.graph = graph
        self.origin = source
        self.destination = destination
        self.shortest_dist = shortest_dist
        self.elevation_path = None
        self.elevation_strategy = elevation_strategy
        self.elevation_gain = elevation_gain
        self.path_limit = path_limit
        self.algo_flag = algo_flag
        self.scaling_factor = 100
        self.model = AlgorithmModel()

    def calculate_elevation_path(self, Graph, source, target, heuristic, weight):
        """
        This method finds the path with nodes

        Parameters
        ----------
            Graph: area map as graph with all the points as nodes
            source: starting point
            destination: final destination point
        """

        if source not in Graph or target not in Graph:
            return

        if heuristic is None:
            def heuristic(u, v):
                return 0

        weight = _weight_function(Graph, weight)
        cnt = count()
        path_queue = [(0, next(cnt), source, 0, None)]
        enqueued = {}
        visited_parent = {}  # storing parent of a visited nodes
        while path_queue:
            _, __, current_node, distance, parent_node = heappop(path_queue)
            if current_node == target:
                node = parent_node
                path = [current_node]
                while node is not None:
                    path.append(node)
                    node = visited_parent[node]
                path.reverse()
                return path

            if current_node in visited_parent:
                if visited_parent[current_node] is None:
                    continue
                qcost, h = enqueued[current_node]
                if qcost < distance:
                    continue

            visited_parent[current_node] = parent_node
            for neighbor, w in Graph[current_node].items():
                cost = distance + weight(current_node, neighbor, w)
                if neighbor in enqueued:
                    qcost, h = enqueued[neighbor]
                    if qcost <= cost:
                        continue
                else:
                    h = heuristic(neighbor, target)
                enqueued[neighbor] = cost, h
                heappush(path_queue, (cost + h, next(cnt), neighbor, cost, current_node))

        raise nx.NetworkXNoPath(f"Node {target} not reachable from {source}")


    def fetch_route_with_elevation(self):
        """
        This method finds the elevated path in the graph
        """

        if self.elevation_strategy == MINIMIZE:
            minmax = 1
        else:
            minmax = -1

        self.elevation_path = nx.shortest_path(self.graph, source=self.origin, target=self.destination,
                                               weight=LENGTH)
        heurestic_val = None
        while self.scaling_factor < 10000:
            elevation_path = self.calculate_elevation_path(self.graph, source=self.origin, target=self.destination, heuristic=heurestic_val,
                                                           weight=lambda u, v, d: math.exp(minmax * d[0][LENGTH] * (d[0]['grade'] + d[0]['grade_abs']) / 2)
                                                           + math.exp((1 / self.scaling_factor) * d[0][LENGTH]))

            elevation_distance = sum(ox.utils_graph.get_route_edge_attributes(self.graph, elevation_path, LENGTH))
            elevation_gain = self.model.get_path_weight(self.graph, elevation_path, ELEVATION_GAIN)
            if elevation_distance <= (self.path_limit) * self.shortest_dist and \
                    minmax * elevation_gain <= minmax * self.elevation_gain:
                self.elevation_path = elevation_path
                self.elevation_gain = elevation_gain
            self.scaling_factor = self.scaling_factor*5

        # Configure the path model - setting appropriate attributes
        path_model = Path()
        path_model.set_algo(str(self.algo_flag))
        path_model.set_elevation_gain(self.model.get_path_weight(self.graph, self.elevation_path, ELEVATION_GAIN))
        path_model.set_drop(0)
        path_model.set_path([[self.graph.nodes[route_node]['x'], self.graph.nodes[route_node]['y']]
                             for route_node in self.elevation_path])
        path_model.set_distance(sum(ox.utils_graph.get_route_edge_attributes(self.graph, self.elevation_path, LENGTH)))
        path_model.set_path_flag(2)

        return path_model




