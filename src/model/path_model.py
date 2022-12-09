from src.model.observable import Observable

class Path(Observable):
    """Get and set methods for path"""
    def __init__(self):
        """Variable initialization"""
        super().__init__()
        self.algo = ""
        self.gain = 0
        self.drop = 0
        self.path = []
        self.distance = 0.0
        self.origin = None, None
        self.destination = None, None
        self.path_flag = 1
        self.observers = set() 
    
    def register(self, obs):
        """Register an observer"""
        self.observers.add(obs)

    def unegister(self, obs):
        """Unregister a registered observer"""
        self.observers.remove(obs)

    def set_algo(self, algo):
        """Set the algorithm to be used"""
        self.algo = algo
        self.state_changed()

    def set_elevation_gain(self, gain):
        """Set the elevation gain"""
        self.gain = gain
        self.state_changed()

    def set_drop(self, drop):
        """Set the elevation drop"""
        self.drop = drop
        self.state_changed()

    def set_path(self, path):
        """Set the path"""
        self.path = path
        self.state_changed()

    def set_distance(self, distance):
        """Set the distance"""
        self.distance = distance
        self.state_changed()
    
    def set_path_flag(self, path_flag):
        """Set the path flag"""
        self.path_flag = path_flag
    
    def get_path_flag(self):
        """Get the path flag"""
        return self.path_flag

    def get_algo(self):
        """Get the algorithm"""
        return self.algo

    def get_gain(self):
        """Get the elevation gain"""
        return self.gain

    def get_drop(self):
        """Get the elevation drop"""
        return self.drop

    def get_path(self):
        """Get the path"""
        return self.path
    
    def get_distance(self):
        """Get the distance"""
        return self.distance

    def set_start_location(self, origin):
        """Set the start location"""
        self.origin = origin
        self.state_changed()

    def get_origin(self):
        """Get the start location"""
        return self.origin

    def set_end_location(self, destination):
        """Set the end location"""
        self.destination = destination
        self.state_changed()

    def get_destination(self):
        """Get the end location"""
        return self.destination
    
    def state_changed(self):
        """Notify all observers when a state is changed"""
        for observer in self.observers:
            observer.update(self)
