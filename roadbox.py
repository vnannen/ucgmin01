'''This module contains the class definitions for the classes Country, City, and Road.
It also contains code that allows students to plot a map of Europe with roads, paths, and cities.
'''

class Country:
    '''a country has the property name'''
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        '''gives the name of the country'''
        return self._name

    def __str__(self):
        '''formats the country's name'''
        return self.name

    def __repr__(self):
        '''formats the country's name'''
        return f"Country(\"{self.name}\")"


class City:
    '''a city has the properties name (string), country (index),
    gps (a tuple of two numbers), degree (number of connections)'''
    def __init__(self, name, country_index, gps=None):
        self._name = name
        self._country = country_index
        self._gps = gps
        self._degree = None

    @property
    def name(self):
        '''gives the name of the city. 
        Use the format method to get the name of the city with the country name'''
        return self._name

    @property
    def country(self):
        '''gives the index of the country of the city'''
        return self._country
    
    @property
    def degree(self):
        '''gives the number of road connections of the city'''
        return self._degree
    
    @degree.setter
    def degree(self, value):
        '''sets the number of road connections of the city'''
        if value > 0:
            self._degree = value
    
    @property
    def latitude(self):
        '''gives the latitude of the city in degrees'''
        return self._gps[0]
        
    @property
    def longitude(self):
        '''gives the longitude of the city in degrees'''
        return self._gps[1]
    
    @property
    def gps(self):
        '''gives the gps coordinates of the city as a tuple (latitude, longitude)'''
        return self._gps

    def format(self, countries=None):
        '''formats the city's name with the country name if available'''
        if countries is not None and self.country in countries:
            return f"{self.name}, {countries[self._country]}"
        else:
            return f"{self.name}"

    def __str__(self):
        '''formats the city's name'''   
        return f"{self.name}"

    def __repr__(self):
        '''formats the city's name with the country index and gps coordinates'''
        return f"City(\"{self.name}\", {self._country}, {self.gps})"
    
class Road:
    '''a road has the properties int a and int b, wich are
    the indices of the cities in a companion list of cities,
    and a property distance in km''' 
    def __init__(self, city_a, city_b, distance):
        if city_a < city_b:
            self._city_a = city_a
            self._city_b = city_b
        else:
            self._city_a = city_b
            self._city_b = city_a
        self._distance = distance        

    @property
    def a(self):
        '''gives the index of the first city of the road'''
        return self._city_a
    
    @property
    def b(self):
        '''gives the index of the second city of the road'''
        return self._city_b

    @property
    def distance(self):
        '''gives the distance of the road in km'''
        return self._distance
        
    def format(self, cities=None, countries=None):
        '''formats the road with the names of the cities and countries if available'''
        if cities is not None and self.a in cities and self.b in cities:
            return (f"({self.a},{self.b}), "
                    f"{cities[self.a].format(countries)} <-> " 
                    f"{cities[self.b].format(countries)}; "
                    f"distance: {self._distance}")

    def __str__(self):
        '''formats the road with the indices of the cities and the distance'''
        return (f"({self.a}, {self.b}); distance: {self._distance}")
    
    def __repr__(self):
        '''formats the road with the indices of the cities and the distance'''
        return f"Road({self.a}, {self.b}, {self._distance})"

    def __eq__(self, other):
        '''checks if two roads connect the same cities'''
        equal = (type(other) == Road and
                ((self.a == other.a
                    and self.b == other.b)
                or (self.a == other.b
                    and self.b == other.a)))
        
    def __lt__(self, other):
        '''compares two roads by distance'''
        return self._distance < other._distance


import matplotlib.pyplot as plt

from mpl_toolkits.basemap import Basemap # don't forget to install basemap in conda

def create_map(cities, path=None):
    '''creates a map of Europe. 
    If a path is provided, the map will zoom in on the region around the path.'''
   # Calculate map bounds with margin

    # find the bounding box in degrees so that the path covers 
    # a large part of the printed map
    margin = 2
    if path is None:
        latitudes = [city.latitude for city in cities.values()]
        longitudes = [city.longitude for city in cities.values()]
    else:
        latitudes = [cities[p].latitude for p in path]
        longitudes = [cities[p].longitude for p in path]

    lower_latitude = min(latitudes) - margin
    upper_latitude = max(latitudes) + margin
    lower_longitude = min(longitudes) - margin
    upper_longitude = max(longitudes) + margin

    # Set up Basemap for Europe (using Mercator projection)
    my_map = Basemap(
        projection='merc', 
        llcrnrlat=lower_latitude, urcrnrlat=upper_latitude,   
        llcrnrlon=lower_longitude, urcrnrlon=upper_longitude,  
        resolution='i'
    )

    # Draw countries, coastlines, and boundaries
    my_map.drawcountries()
    my_map.drawcoastlines()
    my_map.drawmapboundary(fill_color='aqua')
    my_map.fillcontinents(color='white', lake_color='aqua')

    return my_map


# draw cities and roads on the map
def gps_to_xy(gps, geo_map):
    """converts latitude and longitude to horizontal x and vertical y coordinates."""
    x, y = geo_map(gps[1], gps[0]) # Basemap reverses the order
    return x, y 

def mark_city(city, geo_map):
    '''mark city with blue dot'''
    x, y = gps_to_xy(city.gps, geo_map)
    plt.plot(x, y, 'bo', markersize=.5)

def label_city(city, geo_map):
    '''add city name to map'''
    x, y = gps_to_xy(city.gps, geo_map)
    plt.text(x, y, f' {city.name}', fontsize=4)

def mark_road(city_a, city_b, geo_map):
    '''mark road with red line'''
    x1, y1 = gps_to_xy(city_a.gps, geo_map)
    x2, y2 = gps_to_xy(city_b.gps, geo_map)
    plt.plot([x1, x2], [y1, y2], 'r-', markersize=.5)  

def show_map(cities, roads):
    '''shows a map of europe'''

    plt.figure(figsize=(18, 18)) # change this to fit your screen

    europe = create_map(cities)
 
    # Draw cities and roads
    for key, city in cities.items():
        label_city(city, europe)
        mark_city(city, europe)

    for r in roads:
        mark_road(cities[r.a], cities[r.b], europe)

    title = (f"Map of Europe")
    plt.title(title)
    plt.show()  


def show_path(cities, path, adjacency_map=None, visited=None):
    """Will plot a path on a map. Arguments: cities, path, 
    adjacency_map (optional), visited (optional, a list of pairs 
    of cities indices that have been looked at during the search)"""

    if len(path) == 0:
        print("sorry, no path")
        return

    plt.figure(figsize=(18, 18)) # change this to fit your screen

    if visited is not None:
        # Get all coordinates involved for extent calculation
        my_path = path + [i for pairs in visited for i in pairs]
    else:
        my_path = path

    europe = create_map(cities, my_path)

    # Color gradient for visited roads
    if visited is not None:

        # 'autumn' is a predefined color spectrum, there are many others
        cmap = plt.get_cmap('summer') 
        # distributes the color spectrum over len(visited) steps
        colors = [cmap(i / (len(visited) - 1)) for i in range(len(visited))]

        color_counter = 0
        for a, b in visited:
            x1, y1 = gps_to_xy(cities[a].gps, europe)
            x2, y2 = gps_to_xy(cities[b].gps, europe)
            plt.plot([x1, x2], [y1, y2], '-', 
                    color=colors[color_counter], markersize=.5) 
            color_counter += 1

        plt.title(f"Path from {cities[path[0]]} to "
                f"{cities[path[-1]]} in red; "
                f"other visited roads in other colors")

    else:
        plt.title(f"Path from {cities[path[0]]} to "
                  f"{cities[path[-1]]} in red")

    for p in path:
        label_city(cities[p], europe)
    for i in range(len(path)-1):
        mark_road(cities[path[i]], cities[path[i+1]], europe)
    for p in path:
        mark_city(cities[p], europe) 

    print("path length in number of nodes: " + str(len(path)))

    if adjacency_map is not None:
        path_length = 0
        for i in range(len(path)-1):
            path_length += adjacency_map[path[i]][path[i+1]]
        print(f"path length in km: {path_length}")

    if visited is not None:
        # symmetries don't count
        visited_unique = {(min(a, b), max(a, b)) for a, b in visited} 
        print(f"number of roads looked at: {len(set(visited_unique))}")

    plt.show()   


