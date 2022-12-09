NORMAL = "normal"
LENGTH = "length"
WEIGHT = "weight"
ELEVATION_GAIN = "elevation_gain"
ELEVATION = "elevation"

class AlgorithmModel:

    """Critical parameters like the graph, algorithm, path limit, etc. are initialized by this class. 
    It has methods for registering observers, setting algorithms, setting algorithm objects, printing 
    route data, and notifying observers, among other things."""

    def __init__(self):
        """Initializes the route and algorithm attributes."""
        self.graph = None
        self.observer = None
        self.algorithm = None
        self.path_limit = None
        self.elevation_strategy = None
        self.algo_flag = 1

    def set_graph(self, graph):
        """Sets the graph attribute to the given graph."""
        self.graph = graph
    
    def get_graph(self):
        """Returns the graph attribute."""
        return self.graph
    
    def set_algo_flag(self, algo_flag):
        """Sets the algo_flag attribute to the given algo_flag."""
        self.algo_flag = algo_flag
    
    def get_algo_flag(self):
        """Returns the algo_flag attribute."""
        return self.algo_flag

    def set_path_limit(self, path_limit):
        """Sets the path_limit attribute to the given path_limit."""
        self.path_limit = path_limit
    
    def get_path_limit(self):
        """Returns the path_limit attribute."""
        return self.path_limit

    def set_elevation_strategy(self, elevation_strategy):
        """Sets the elevation_strategy attribute to the given elevation_strategy."""
        self.elevation_strategy = elevation_strategy
    
    def get_elevation_strategy(self):
        """Returns the elevation_strategy attribute."""
        return self.elevation_strategy

    def set_start_point(self, start_point):
        """Sets the start_point attribute to the given start_point."""
        self.start_point = start_point

    def set_end_point(self, end_point):
        """Sets the end_point attribute to the given end_point."""
        self.end_point = end_point

    def get_weight(self, graph, node_1, node_2, weight_type=NORMAL):
        """Returns the weight of the edge between the given nodes."""
        if weight_type == NORMAL:
            try:
                return graph.edges[node_1, node_2, 0][LENGTH]
            except:
                return graph.edges[node_1, node_2][WEIGHT]
        elif weight_type == ELEVATION_GAIN:
            return max(0.0, graph.nodes[node_2][ELEVATION] - graph.nodes[node_1][ELEVATION])

    def get_path_weight(self, graph, route, weight_attribute):
        """Returns the weight of the given route."""
        total = 0
        for i in range(len(route) - 1):
            total += self.get_weight(graph, route[i], route[i + 1], weight_attribute)
        return total