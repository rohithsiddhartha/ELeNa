import osmnx as ox
import os
import pickle as pkl
import numpy as np


class Graph:

  """Class that offers the tools to make a graph using elevation information specific to a chosen location."""
  def __init__(self):
    self.G = None
    # Co-ordinates of UMass Amherst
    self.initial_point = (42.3867637, -72.5322402) 
    self.saved_map_path = "src/graph.p"
    self.gmap_api_key = "AIzaSyCC19S4I6tEZYE9Iv4zhsNRixctc6gp_Dc"
    self.isMapLoaded = os.path.exists(self.saved_map_path)


  def distance(self, lat1, long1, lat2, long2):
    """Returns distance between given coordinates"""
    radius = 6371008.8
    lat1, long1 = np.radians(lat1), np.radians(long1)
    lat2, long2 = np.radians(lat2), np.radians(long2)
    dlong, dlat = long2 - long1, lat2 - lat1  
    temp1 = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlong / 2)**2
    temp2 = 2 * np.arctan2(np.sqrt(temp1), np.sqrt(1 - temp1))
    return radius * temp2
  
  def get_distance_from_dest(self, dest_node):
    """Returns the graph with distance from destination node for each node in the graph"""
    end_node = self.G.nodes[ox.get_nearest_node(self.G, point=dest_node)]
    for node, data in self.G.nodes(data=True):
        node_lat = self.G.nodes[node]['x']
        node_long = self.G.nodes[node]['y']
        last_lat = end_node['x']
        last_long = end_node['y']
        data['dist_from_dest'] = self.distance(last_lat,last_long,node_lat,node_long)
    return self.G
  
  def get_graph(self, dest_node):
    """Returns the graph"""
    if not self.isMapLoaded:
      print("Fetching the Map")
      self.G = ox.graph_from_point(self.initial_point, dist=20000, network_type='walk')

      self.G = ox.add_node_elevations(self.G, api_key=self.gmap_api_key) 
      pkl.dump(self.G, open(self.saved_map_path, "wb"))
      print("Stored the Map")
    else:
      self.G = pkl.load(open(self.saved_map_path, "rb"))
      self.G = ox.add_edge_grades(self.G)
    return self.get_distance_from_dest(dest_node)

  
