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

# don't forget to install cartopy in conda
import cartopy.crs as ccrs 
import cartopy.feature as cfeature
import warnings # that is because cartopy throws a lot of warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

def show_map(cities, roads):
    '''shows a map of europe'''
    plt.figure(figsize=(18, 18)) # change this to fit your screen
        
    # find the bounding box in degrees so that the path covers 
    # a large part of the printed map
    margin = 2
    latitudes = [city.latitude for city in cities.values()]
    longitudes = [city.longitude for city in cities.values()]
    lower_latitude = min(latitudes) - margin
    upper_latitude = max(latitudes) + margin
    lower_longitude = min(longitudes) - margin
    upper_longitude = max(longitudes) + margin

    # Set up Cartopy map with Mercator projection
    ax = plt.axes(projection=ccrs.Mercator())

    # Set extent
    ax.set_extent([lower_longitude, upper_longitude, 
                   lower_latitude, upper_latitude], 
        crs=ccrs.PlateCarree()
    )

    # Add background features
    ax.add_feature(cfeature.LAND, facecolor='white')
    ax.add_feature(cfeature.OCEAN, facecolor='aqua')
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAKES, edgecolor='black', 
                   facecolor='aqua', linewidth=0.5)
    ax.add_feature(cfeature.RIVERS)

    # Draw cities and roads
    for key, city in cities.items():
        ax.plot(city.longitude, city.latitude, 'bo', markersize=2, 
            transform=ccrs.PlateCarree())
        ax.text(city.longitude, city.latitude, f' {city}', 
            fontsize=4, transform=ccrs.PlateCarree()
        )

    for r in roads:
        city_a = cities[r.a]
        city_b = cities[r.b]
        ax.plot([city_a.longitude, city_b.longitude], 
                [city_a.latitude, city_b.latitude], 
            'r-', transform=ccrs.PlateCarree()
        )

    title = (f"Map of Europe")
    plt.title(title)
    plt.show()  


def show_path(cities, path, adjacency_map=None, visited=None):
    """Plots a path on a map. Arguments: cities, path, 
    adjacency_map (optional), visited (optional, a list of pairs 
    of cities indices that have been looked at during the search)"""

    if len(path) == 0:
        print("sorry, no path")
        return

    plt.figure(figsize=(18, 18)) # change this to fit your screen

    if visited is not None:
        all_coords = (
            [cities[i].gps for i in path] +
            [cities[a].gps for a, _ in visited] +
            [cities[b].gps for _, b in visited]
        )
    else:
        all_coords = [cities[i].gps for i in path]

    latitudes = [latitude for latitude, _ in all_coords]
    longitudes = [longitude for _, longitude in all_coords]
    margin = 2
    lower_latitude = min(latitudes) - margin
    upper_latitude = max(latitudes) + margin
    lower_longitude = min(longitudes) - margin
    upper_longitude = max(longitudes) + margin

    ax = plt.axes(projection=ccrs.Mercator())
    ax.set_extent([lower_longitude, upper_longitude, 
        lower_latitude, upper_latitude], 
        crs=ccrs.PlateCarree()
    )

    # Add map features
    ax.add_feature(cfeature.LAND, facecolor='white')
    ax.add_feature(cfeature.OCEAN, facecolor='aqua')
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAKES, edgecolor='black', 
                   facecolor='aqua', linewidth=0.5)
    ax.add_feature(cfeature.RIVERS)

    # Color gradient for visited roads
    if visited is not None:
        cmap = plt.get_cmap('summer')
        colors = [cmap(i / (len(visited) - 1)) for i in range(len(visited))]

        for idx, (a, b) in enumerate(visited):
            a_latitude, a_longitude = cities[a].gps
            b_latitude, b_longitude = cities[b].gps
            ax.plot([a_longitude, b_longitude], [a_latitude, b_latitude], 
                '-', color=colors[idx], linewidth=1, transform=ccrs.PlateCarree())
            
        plt.title(f"Path from {cities[path[0]]} to "
                f"{cities[path[-1]]} in red; "
                f"other visited roads in other colors")
    else:
        plt.title(f"Path from {cities[path[0]]} to "
                  f"{cities[path[-1]]} in red")
        
    # Final path in red
    for i in range(len(path)-1):
        a = cities[path[i]]
        b = cities[path[i+1]]
        ax.plot(
            [a.longitude, b.longitude], 
            [a.latitude, b.latitude],
            'r-', linewidth=2, transform=ccrs.PlateCarree()
        )

    # Labels and dots
    for p in path:
        city = cities[p]
        ax.plot(city.longitude, city.latitude, 
            'bo', markersize=2, 
            transform=ccrs.PlateCarree()
        )
        ax.text(city.longitude, city.latitude, 
            f' {city.name}', fontsize=8, 
            transform=ccrs.PlateCarree()
        )

    print("path length in number of nodes:", len(path))

    if adjacency_map is not None:
        my_length = 0
        for i in range(len(path)-1):
            my_length += adjacency_map[path[i]][path[i+1]]
        print("path length in km:", my_length)
        visited_unique = {(min(a, b), max(a, b)) for a, b in visited}
        print(f"number of roads looked at: {len(visited_unique)}")

    plt.show()


