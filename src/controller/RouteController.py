from src.model.algo_model import AlgorithmModel
from src.model.map_model import Graph
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

        Parameters
        ----------
            source: starting point
            destination:   final destination point

        Returns
        -------
            The Shortest Path model
        """

        self.algorithm_model.set_graph(Graph().get_graph(destination))
        shortestPathController = ShortestPathController(self.algorithm_model.get_graph())
        return shortestPathController.get_shortest_path(source, destination)

    def calcuate_elevation_path(self):
        """
        This method gets the elevation gain path model based on the source and destination coordinates.

        Returns
        -------
            Elevation gain Shortest Path model
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

        # Printing the path details
        print("Total Route Distance: " + str(float(path.get_distance()/1609.344)) + " miles")
        print("Elevation Gain of the Route: " + str(path.get_gain()))
        # print("Algorithm Used to Calculate Route: " + path.get_algo())

    def calculate_final_route(self, start_point, end_point, deviation_percent, minmax_elev_gain, map_view):
        """
        This method gets the final shortest path model with desired elevation with in path distance deviation limit provided.

        Parameters
        ----------
            start_point: Source point
            end_point: Destination point
            deviation_percent: Specifies the upper limit for the path distance being calculated
            minmax_elev_gain: Maximum or minimum elevation gain that is requested by the user.
            map_view:MapView view
        """

        # Shortest path calculation
        self.shortest_path = self.calculate_shortest_path(start_point, end_point)
        self.print_route_attributes(self.shortest_path)

        # No upper limit on path so should return the shortest path irrespective of elevation gain
        if deviation_percent == "100":
            self.shortest_path.register(map_view)
            self.shortest_path.state_changed()
            return

        # Configuring the algorith model to calculate the path
        self.algorithm_model.set_path_limit(float(deviation_percent) / 100.0)
        self.algorithm_model.set_elevation_strategy(minmax_elev_gain)
        self.algorithm_model.set_algo_flag(2)

        # Elevation gain shortest path calculation
        self.elevation_path = self.calcuate_elevation_path()
        self.print_route_attributes(self.elevation_path)

        # Linking the view with the path model
        self.shortest_path.register(map_view)
        self.shortest_path.state_changed()
        self.elevation_path.register(map_view)
        self.elevation_path.state_changed()