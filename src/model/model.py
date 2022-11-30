import osmnx as ox
import os
import pickle as pkl
import numpy as np

# Co-ordinates of UMass Amherst
initial_point = (42.3867637, -72.5322402) 
google_api_key = "AIzaSyCC19S4I6tEZYE9Iv4zhsNRixctc6gp_Dc"
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