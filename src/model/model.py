import osmnx as ox
import os
import pickle as pkl
import numpy as np

# Co-ordinates of UMass Amherst
initial_point = (42.3867637, -72.5322402) 
google_api_key = "AIzaSyCC19S4I6tEZYE9Iv89zhsNRixctc6gp_Dc"
radius = 6371008.8 
#Coordinates of the destination (home)
end_point = (42.458867036514775, -72.57851963471636)
G = ox.graph_from_point(initial_point, dist=20000, network_type='walk')
G = ox.add_node_elevations(G, api_key=google_api_key)
pkl.dump(G, open("src/graph.p", "wb"))
nodes = ox.get_nearest_nodes(ox.graph_from_point(initial_point, dist=20000, network_type='walk'))
end_node = G.nodes[ox.get_nearest_node(G, point=end_point)]

def dist_nodes(self,lat1,long1,lat2,long2):
		# Given latitudes and longitudes of two nodes, returns the distance between them.
    radius=6371008.8 # Earth radius
        
    lat1, long1 = np.radians(lat1), np.radians(long1)
    lat2, long2 = np.radians(lat2),np.radians(long2)

    dlong,dlat = long2 - long1,lat2 - lat1

    temp1 = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlong / 2)**2
    temp2 = 2 * np.arctan2(np.sqrt(temp1), np.sqrt(1 - temp1))
    return radius * temp2

for node, data in G.nodes(data=True):
    node_lat = G.nodes[node]['x']
    node_long = G.nodes[node]['y']
    last_lat = end_node['x']
    last_long = end_node['y']
    data['dist_from_dest'] = dist_nodes(last_lat,last_long,node_lat,node_long)

class Graph:
  def __init__(self):
    self.G = None
    self.initial_point = (42.3867637, -72.5322402) # Co-ordinates of UMass Amherst
    self.saved_map_path = "src/graph.p"
    self.gmap_api_key = "AIzaSyCC19S4I6tEZYE9Iv4zhsNRixctc6gp_Dc"
    self.isMapLoaded = os.path.exists(self.saved_map_path)
    self.end_point = (42.458867036514775, -72.57851963471636)

  def load_map(self):
    if self.isMapLoaded:
      self.G = pkl.load(open(self.saved_map_path, "rb"))
    else:
      self.G = ox.graph_from_point(self.initial_point, dist=20000, network_type='walk')
      self.G = ox.add_node_elevations(self.G, api_key=self.gmap_api_key)
      pkl.dump(self.G, open(self.saved_map_path, "wb"))
    return self.G
  
  def get_nearest_node(self, point):
    return ox.get_nearest_node(self.G, point)
  
  def distance(self, lat1, long1, lat2, long2):
    radius = 6371008.8
    lat1, long1 = np.radians(lat1), np.radians(long1)
    lat2, long2 = np.radians(lat2), np.radians(long2)
    dlong, dlat = long2 - long1, lat2 - lat1  
    temp1 = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlong / 2)**2
    temp2 = 2 * np.arctan2(np.sqrt(temp1), np.sqrt(1 - temp1))
    return radius * temp2
  
  def get_distance_from_dest(self, dest_node):
    end_node = self.G.nodes[ox.get_nearest_node(self.G, point=dest_node)]
    for node, data in self.G.nodes(data=True):
        node_lat = self.G.nodes[node]['x']
        node_long = self.G.nodes[node]['y']
        last_lat = end_node['x']
        last_long = end_node['y']
        data['dist_from_dest'] = self.dist_nodes(last_lat,last_long,node_lat,node_long)
    return self.G
  
  def get_graph(self, dest_node):
    print("Fetching the Map")
    self.G = ox.graph_from_point(self.initial_point, dist=20000, network_type='walk')

    # appending elevation data to each node and populating the graph
    self.G = ox.add_node_elevations(G, api_key=self.gmap_api_key) 
    pkl.dump(self.G, open(self.saved_map_path, "wb"))
    print("Stored the Map") 
    return self.get_distance_from_dest(dest_node)

  
