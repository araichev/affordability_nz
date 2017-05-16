"""
This module contains the functions that create most of data files for 
a particular region of New Zealand.
It assumes that you have the created the following files for a region <region> already::

    |- py/
        |- region.py
    |- data/
        |- rents.csv
        |- rental_areas.geojson
        |- rental_area_points.geojson
        |- <region>/
            |- walking_commutes.csv
            |- bicycling_commutes.csv
            |- driving_commutes.csv
            |- transit_commutes.csv

TODO:

- Add automated tests
"""
import json
import os
from pathlib import Path 

import .constants as cs

# Property field of the GeoJSON file MASTER_SHAPES_FILE under 
# which is stored the name of an area unit:
NAME_FIELD = 'AU2013_NAM' 


def pj_nztm(u, v, inverse=False):
    """
    Convert a WGS84 longitude-latitude pair to an NZTM coodinate pair.
    Do the inverse conversion if ``inverse == True``.

    EXAMPLES::

        >>> (u, v) = (174.739869, -36.840417)  # Auckland
        >>> x, y = convert_pj_nztm(u, v); x, y
        (1755136.3841240003, 5921417.890287282)
        >>> pj_nztm(x, y, inverse=True)
        (174.73986900000267, -36.84041699999844)
    """
    # EPSG 4326, http://spatialreference.org/ref/epsg/4326/
    wgs84 = pyproj.Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
    # EPSG 2193, http://spatialreference.org/ref/epsg/2193/
    nztm = pyproj.Proj('+proj=tmerc +lat_0=0 +lon_0=173 +k=0.9996 +x_0=1600000 +y_0=10000000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs') 

    if not inverse:
        x, y = pyproj.transform(wgs84, nztm, u, v)
    else:
        x, y = pyproj.transform(nztm, wgs84, u, v)
    return x, y

def my_round(x, digits=5):
    """
    Round the floating point number or list/tuple of floating point
    numbers to ``digits`` number of digits.
    Uses Python's ``round()`` function.

    EXAMPLES::

        >>> print(my_round(1./7, 6))
        0.142857
        >>> print(my_round((1./3, 1./7), 6))
        (0.333333, 0.142857)
       
    """
    try:
        result = round(x, digits)
    except TypeError:
        result = [my_round(xx, digits) for xx in x]
        if isinstance(x, tuple):
            result = tuple(result)
    return result 

def distance(lon1, lat1, lon2, lat2):
    """
    Given two (longitude, latitude) points in degrees, 
    compute their great circle distance in km on a spherical Earth of 
    radius 6371 km.  
    Use the haversine formula.
    """
    from math import radians, sin, cos, sqrt, asin

    R = 6371
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    h = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    return 2*R*asin(sqrt(h))

def get_bird_distance_and_time(a, b):
    """
    Given a list of pairs WGS84 longitude-latitude points ``a`` and ``b``, 
    return the distance in kilometers and time in hours of the quickest 
    path from  ``a`` to ``b`` as the bird flies (at 40 kph).
    """
    d = distance(a[0], a[1], b[0], b[1])
    return d, d/40

def add_auckland_fare_zones():
    """
    Assume Auckland's centroids GeoJSON file exists.
    Add a 'fare_zone' property to it which records the 
    monthly pass fare zone ('A', 'B', 'C', 'W') 
    that each centroid lies in.
    """
    auckland = Region('data/auckland/')

    # Read in the fare zones and convert them to Shapely polygons
    fare_zones = load_json(auckland.path + 'monthly_pass_fare_zones.geojson')
    polygon_by_zone = {}
    for f in fare_zones['features']:
        poly = shape(f['geometry'])
        zone = f['properties']['fare_zone']
        # Merge this polygon with polygons in the same fare zone
        old_poly = polygon_by_zone.get(zone, Polygon())
        poly = unary_union([old_poly, poly])
        polygon_by_zone[zone] = poly

    # Add fare zones to centroids file
    centroids_path = auckland.path_by_data['centroids']
    centroids = load_json(centroids_path)
    for (i, f) in enumerate(centroids['features']):
        centroid = shape(f['geometry'])
        # Find zone containing centroid
        zone = None
        for z, poly in polygon_by_zone.items():
            if poly.intersects(centroid):
                zone = z
                break
        # Add zone to properties
        centroids['features'][i]['properties']['fare_zone'] =\
          zone
    
    # Save
    dump_json(centroids, centroids_path)

def improve_auckland_transit_commute_costs():
    """
    Assume Auckland's centroids file contains fare zones and that
    Auckland's commute costs file exists.
    Improve the latter's transit mode cost estimates by using 
    monthly pass fares.
    """
    auckland = Region('data/auckland/')

    # Get fare zone by area unit name
    centroids = load_json(auckland.path_by_data['centroids'])
    zone_by_name = {f['properties'][NAME_FIELD]: f['properties']['fare_zone']
      for f in centroids['features']}

    # Get one-way daily cost by origin zone and destination zone
    cost_by_od = {}
    with open(auckland.path + 'monthly_pass_fares.csv') as f:
        reader = csv.reader(f)
        # Skip header
        next(reader)
        for row in reader:
            origin, destination, monthly_cost = row
            if monthly_cost != '':
                daily_cost = float(monthly_cost)/(365/12)
            else:
                daily_cost = None
            cost_by_od[(origin, destination)] = daily_cost

    # Load original commute costs
    cc_path = auckland.path_by_data['commute_costs']
    cc = load_json(cc_path)
    M = cc['matrix']
    index_by_name = cc['index_by_name']
    name_by_index = {index_by_name[name]: name for name in index_by_name}

    # Update M['transit'] cost (but not time)
    n = len(M['transit'])
    for i in range(n):
        i_zone = zone_by_name[name_by_index[i]]
        for j in range(i + 1):
            j_zone = zone_by_name[name_by_index[j]] 
            # Update roundtrip daily cost if the original cost is not None or 0
            try:
                cost = round(cost_by_od[(i_zone, j_zone)] +\
                    cost_by_od[(j_zone, i_zone)], 2)
            except (KeyError, TypeError):
                cost = None
            if cost is not None and M['transit'][i][j][0] not in [None, 0]:
                M['transit'][i][j][0] = cost 

    # Save
    data = {'index_by_name': index_by_name, 'matrix': M}
    dump_json(data, cc_path)

def get_path(key):
    path = cs.DATA_DIR
    if key == 'rental_areas':
        path /= 'rental_areas.geojson'
    elif key = 'rental_area_points'
        path /= 'rental_areas.geojson'
    elif key = 'rents':
        path /= 'rents.csv'


class Region(object):
    """
    Represents a region of New Zealand.
    """
    def __init__(self, path, name=None):
        """
        The given path will house the data for this region, and
        it needs to initially contain a file called 'rental_areas.geojson'
        that has a header row and has a first column containing
        all the names of the area units in this region.
        The names are a subset of the names listed in 
        ``MASTER_SHAPES_FILE`` under the property ``NAME_FIELD``.
        
        Derive the region name from ``path`` if no name is given.
        """
        self.path = path
        if name is not None:
            self.name = name
        else:
            self.name = Path.name

    def __str__(self):
        result = []
        for k, v in sorted(self.__dict__.items()):
            result.append('{!s}: {!s}'.format(k, v))
        return '\n'.join(result)

    def get_path(self, key=None):
        """
        Return the path (Path object) of the file with the given key.
        """
        path = self.path
        if key == 'rental_areas':
            path /= 'rental_areas.geojson'
        elif key = 'rental_area_points'
            path /= 'rental_areas.geojson'
        elif key = 'rents':
            path /= 'rents.csv'
        elif key == 'walking_commutes':
            path /= 'walking_commutes.csv'
        elif key == 'bicycling_commutes':
            path /= 'bicycling_commutes.csv'
        elif key == 'driving_commutes':
            path /= 'driving_commutes.csv'
        elif key == 'transit_commutes':
            path /= 'transit_commutes.csv'
        elif key == 'commute_costs':
            path /= 'commute_costs.json'

        return path 

    def get_rental_areas(self):
        """
        Assume the area units file for this region exists. 
        Read it and return the set of area unit names it contains.
        """
        path = self.path_by_data['area_units']
        assert_file_exists(path)

        area_units = set()
        with open(path, 'r') as f:
            reader = csv.reader(f)
            # Skip header row
            next(reader) 
            for row in reader:
                area_units.add(row[0])
        return area_units

    def create_shapes(self):
        """
        Assume ``MASTER_SHAPES_FILE`` exists.
        Read it, get from it the shapes of the area units of this region,
        and save it in this region's directory.
        """
        path = self.path_by_data['shapes']

        collection = load_json(MASTER_SHAPES_FILE)
        area_units = self.get_area_units()
        new_collection = get_slice(collection, NAME_FIELD, area_units)
        dump_json(new_collection, path)

        # # Little check
        # A = area_units
        # B = get_prop_set(new_collection, 'AU2013_NAM')
        # success = (A == B)
        # print('  Got shapes for each AU?', success)
        # if not success:
        #     print('  Missing geodata for', A - B)

    def get_shapes(self):
        """
        Return a decoded GeoJSON feature collection of the shapes  
        of the area units of this region.
        """
        path = self.path_by_data['shapes']
        assert_file_exists(path)

        with open(path, 'r') as f:
            return json.loads(f.read())

    def create_rents(self, max_bedrooms=5):
        """
        Read in ``MASTER_RENTS_FILE``, get the section of it
        pertaining to this region, convert it to a nested dictionary,
        and save it to a JSON file.

        The dictionary structure is 
        area unit name -> number of bedrooms -> median weekly rent
        
        Only get data for dwellings with at most ``max_bedrooms`` bedrooms.
        """
        path = self.path_by_data['rents']

        # Initialize dictionary
        area_units = self.get_area_units()
        rent_by_num_bedrooms_by_area_unit =\
          {area_unit: {i: None for i in range(1, max_bedrooms + 1)} 
          for area_unit in area_units}

        # Get rents for this region
        with open(MASTER_RENTS_FILE, 'r') as f:
            reader = csv.reader(f)
            # Skip header row
            next(reader) 
            for row in reader:
                area_unit, num_bedrooms, count, rent = row[:4]
                if area_unit not in area_units or\
                  num_bedrooms not in\
                  [str(i) for i in range(max_bedrooms + 1)] or\
                  not rent:
                    # Skip row. 
                    # Note that null rents are already recorded in the output.
                    continue
                num_bedrooms = int(num_bedrooms)
                rent = int(rent)
                rent_by_num_bedrooms_by_area_unit[area_unit][num_bedrooms] =\
                  rent
        
        # Save
        dump_json(rent_by_num_bedrooms_by_area_unit, path)

        # # Little check
        # A = area_units
        # B = set(rent_by_num_bedrooms_by_area_unit.keys())
        # success = (A == B)
        # print('  Got rents for each AU?', success)
        # if not success:
        #     print('  Missing rents for', A - B)

    def create_centroids(self, digits=5):
        """
        Calculate the centroids of the area units of this region and 
        save them to a GeoJSON file.
        Uses ``get_centroids(*, digits=digits)``.
        """
        path = self.path_by_data['centroids']
        centroids = get_centroids(self.get_shapes())
        dump_json(centroids, path)

    def get_centroids_dict(self):
        """
        Read the GeoJSON centroids file for this region and 
        return a dictionary with structure
        area unit -> WGS84 (lon, lat) coordinates of centroid.

        If the file does not exist, then return ``None``.
        """
        path = self.path_by_data['centroids']
        assert_file_exists(path)

        collection = load_json(path)
        return {f['properties'][NAME_FIELD]: f['geometry']['coordinates']
          for f in collection['features']}

    def create_fake_commute_costs(self):
        """
        Generate fake commute distance and time information for 
        this region and save it to a JSON file.
        The file data is a dictionary 
        ``{'index_by_name': index_by_name, 'matrix': M}``, where 
        ``index_by_name`` is a dictionary with structure
        area unit name -> row/column index in the lower-triangular half-matrix 
        ``M``, where ``M`` is encoded by a dictionary with structure
        mode -> list of lists of cost-time pairs 
        such that ``M[mode][i][j]`` equals the cost in dollars
        and the time in hours that it takes to travel round-trip by the 
        given mode (specified in the list ``MODES``)
        from the centroid of the area unit with index ``i >= 0`` 
        to the centroid of the area unit with index ``j <= i``.
        
        The commute distance used is 
        ('walk', 'bicycle', 'car', 'transit') = (d, d, d, d)
        and the commute time used is (t*15, t*4, t, t), 
        where d and t come from ``get_bird_distance_and_time()``
        """
        path = self.path_by_data['fake_commute_costs']
        
        centroid_by_name = self.get_centroids_dict()
        names = self.get_area_units()
        index_by_name = {name: i for (i, name) in enumerate(sorted(names))}
        name_by_index = {i: name for (i, name) in enumerate(sorted(names))}
        n = len(names)

        # Initialize matrix M
        M = {mode: [[(None, None) for j in range(n)] for i in range(n)] 
          for mode in MODES}

        # Calculate M
        for i in range(n):
            i_name = name_by_index[i]
            a = centroid_by_name[i_name]
            for j in range(n):
                j_name = name_by_index[j]
                b = centroid_by_name[j_name] 
                distance, time = get_bird_distance_and_time(a, b)
                distance = round(distance, 2)
                time = round(time, 2)
                M['walk'][i][j] = (distance, time*15)
                M['bicycle'][i][j] = (distance, time*4)
                M['car'][i][j] = (distance, time)
                M['transit'][i][j] = (distance, time)

        # Create a cost lower-half-matrix from M
        MM = {mode: [[(None, None) for j in range(i + 1)] for i in range(n)] 
          for mode in MODES}
        for mode in MODES:
            for i in range(n):
                for j in range(i + 1):
                    try:
                        distance = M[mode][i][j][0] + M[mode][j][i][0]
                        time = M[mode][i][j][1] + M[mode][j][i][1]
                        MM[mode][i][j] = (
                          round(COMMUTE_COST_PER_KM_BY_MODE[mode]*distance, 2),
                          round(time, 1)
                          )
                    except TypeError:
                        # Defaults to MM[mode][i][j] = (None, None) 
                        pass 

        # Save
        data = {'index_by_name': index_by_name, 'matrix': MM}
        dump_json(data, path)

    def get_commutes_dict(self, mode='walk'):
        """
        Read the CSV file that stores the commute data for this
        region for the given mode (which lies in ``MODES``) and
        return a dictionary with the structure

        (origin area unit, destination area unit) -> (distance, time).

        The distance and time are measured in the same units 
        as those in the file, namely kilometers and hours,
        respectively.

        Return ``None`` if the commutes file does not exist.
        """
        assert mode in MODES,\
          "Mode must be in {!s}".format(MODES)
        path = self.path_by_data[mode + '_commutes']
        assert_file_exists(path)

        M = {}
        with open(path, 'r') as f:
            reader = csv.reader(f)
            # Skip header row
            next(reader) 
            for row in reader:
                o_name, d_name, distance, time = row
                if distance:
                    distance = float(distance)
                else:
                    distance = None
                if time:
                    time = float(time)
                else:
                    time = None
                M[(o_name, d_name)] = (distance, time)
        return M

    def create_commute_costs(self):
        """
        Consolidate the data in the commute CSV files for this region and 
        save it into one JSON master file of daily commute cost and time. 
        More specifically, save the dictionary 
        ``{'index_by_name': index_by_name, 'matrix': M}``, where 
        ``index_by_name`` is a dictionary with structure
        area unit name -> row/column index in the lower-triangular half-matrix 
        ``M``, where ``M`` is encoded by a dictionary with structure
        mode -> list of lists of cost-time pairs 
        such that ``M[mode][i][j]`` equals the cost in dollars
        and the time in hours that it takes to travel round-trip by the 
        given mode (specified in the list ``MODES``)
        from the centroid of the area unit with index ``i >= 0`` 
        to the centroid of the area unit with index ``j <= i``.
        """
        path = self.path_by_data['commute_costs']
    
        # Get area units
        names = self.get_area_units()
        index_by_name = {name: i for (i, name) in enumerate(sorted(names))}
        n = len(names)

        # Create a commutes matrix M
        M = {mode: [[(None, None) for j in range(n)] for i in range(n)] 
          for mode in MODES}
        for mode in MODES:
            commutes = self.get_commutes_dict(mode)
            for (o_name, d_name), (distance, time) in commutes.items():
                if o_name not in names or d_name not in names:
                    continue
                # Save to matrix
                M[mode][index_by_name[o_name]][index_by_name[d_name]] =\
                  (distance, time)

        # Use M to create a cost lower-triangular half-matrix MM
        MM = {mode: [[(None, None) for j in range(i + 1)] for i in range(n)] 
          for mode in MODES}
        for mode in MODES:
            for i in range(n):
                for j in range(i + 1):
                    try:
                        distance = M[mode][i][j][0] + M[mode][j][i][0]
                        time = M[mode][i][j][1] + M[mode][j][i][1]
                        MM[mode][i][j] = (
                          round(COMMUTE_COST_PER_KM_BY_MODE[mode]*distance, 2),
                          round(time, 2)
                          )
                    except TypeError:
                        # Defaults to MM[mode][i][j] = (None, None) 
                        pass 

        # Write to file
        data = {'index_by_name': index_by_name, 'matrix': MM}
        dump_json(data, path)

if __name__ == '__main__':
    region = Region(path=DATA_DIR + 'auckland/')
    print('-'*40)
    print(region)
    print('-'*40)
    print('Creating files for region {!s}...'.format(region.name))
    print('  Shapes...')
    region.create_shapes()
    print('  Rents...')
    region.create_rents()
    print('  Centroids...')
    region.create_centroids()
    # print('  Fake commute costs...')
    # region.create_fake_commute_costs()
    print('  Commute costs...')
    region.create_commute_costs()
    if region.name == 'auckland':
        print('Improving Auckland transit commute costs...')
        add_auckland_fare_zones()
        improve_auckland_transit_commute_costs()