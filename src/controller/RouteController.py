from src.model.AlgorithmModel import AlgorithmModel
from src.model.MapGraphModel import MapGraphModel
from src.controller.ShortestPathController import ShortestPathController
from src.controller.AlgorithmController import AlgorithmController

class RouteController:
    """
    Controller Class to modify the route models
    """
    def __init__(self):
        """
        init method: initializes the  class attributes - algorithm_model, shortest_path, elevation_path
        """
        self.algorithm_model = AlgorithmModel()
        self.shortest_path = None
        self.elevation_path = None

    def calculate_shortest_path(self, source, destination):
        """
        This method gets the shortest path model based on the starting and ending coordinates.
        """

        self.algorithm_model.set_graph(MapGraphModel().get_map_graph(destination))
        shortestPathController = ShortestPathController(self.algorithm_model.get_graph())
        return shortestPathController.get_shortest_path(source, destination)

    def calcuate_elevation_path(self):
        """
        This method gets the elevation gain path model based on the source and destination coordinates.
        """

        algorithmController = AlgorithmController(self.algorithm_model.get_graph(), self.shortest_path.get_distance(),
                                    self.algorithm_model.get_path_limit(), self.algorithm_model.get_elevation_strategy(),
                                    self.shortest_path.get_origin(), self.shortest_path.get_destination(),
                                    self.shortest_path.get_gain(), self.algorithm_model.get_algo_flag())
        return algorithmController.fetch_route_with_elevation()

    def print_route_attributes(self, path):
        """
        Displays the information about the path.

        Parameters
        ----------
            path: the path for which the information needs to be displayed
        """

        print("Total Route Distance: " + str(path.get_distance()))
        print("Elevation Gain of the Route: " + str(path.get_gain()))
        print("Algorithm Used to Calculate Route: " + path.get_algo())

    def calculate_final_route(self, start_point, end_point, deviation_percent, minmax_elev_gain, map_view):
        """
        This method gets the final shortest path model with desired elevation with in path distance deviation limit provided.
        """

        self.shortest_path = self.calculate_shortest_path(start_point, end_point)
        self.print_route_attributes(self.shortest_path)

        if deviation_percent == "100":
            self.shortest_path.register(map_view)
            self.shortest_path.state_changed()
            return

        self.algorithm_model.set_path_limit(float(deviation_percent) / 100.0)
        self.algorithm_model.set_elevation_strategy(minmax_elev_gain)
        self.algorithm_model.set_algo_flag(2)

        self.elevation_path = self.calcuate_elevation_path()
        self.print_route_attributes(self.elevation_path)

        self.shortest_path.register(map_view)
        self.shortest_path.state_changed()
        self.elevation_path.register(map_view)
        self.elevation_path.state_changed()