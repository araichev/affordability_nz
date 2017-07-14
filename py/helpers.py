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
import datetime as dt 

import pandas as pd 
import geopandas as gpd


ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = ROOT/'data'
CRS_NZGD49 = {'init': 'epsg:27200', 'no_defs': True}
CRS_NZTM = {'init': 'epsg:2193', 'no_defs': True}
CRS_WGS84 = {'init': 'epsg:4326'}
REGIONS = [
    'auckland', 
    'canterbury', 
    'wellington',
]
MODES = [
    'walking', 
    'bicycling', 
    'driving', 
    'transit',
]
# Cost in NZD/km. Get transit costs from an origin-destination matrix.
COST_BY_MODE = {
    'walking': 0, 
    'bicycling': 0, 
    'driving': 0.274, 
    'transit': 0,
}

def get_path(region, key=None):
    """
    Return the path (Path object) of the file corresponding to the given
    region (string) and key (string).
    """
    path = DATA_DIR/region
    if key is None:
        return path  
    elif key == 'rental_areas':
        path /= 'rental_areas.geojson'
    elif key == 'rental_points':
        path /= 'rental_points.geojson'
    elif key == 'rents_csv':
        path /= 'rents.csv'
    elif key == 'rents_json':
        path /= 'rents.json'
    elif key == 'commutes_walking':
        path /= 'commutes_walking.csv'
    elif key == 'commutes_bicycling':
        path /= 'commutes_bicycling.csv'
    elif key == 'commutes_driving':
        path /= 'commutes_driving.csv'
    elif key == 'commutes_transit':
        path /= 'commutes_transit.csv'
    elif key == 'transit_costs':
        path /= 'transit_costs.csv'
    elif key == 'commute_costs':
        path /= 'commute_costs.json'
    else:
        raise ValueError('Invalid region-key pair ({!s}, {!s})'.format(region, key))

    return path 

def get_data(region, key):
    """
    Return the data corresponding to the given region (string) and key (string).
    """
    path = get_path(region, key)
    if not path.exists:
        raise ValueError('Data does not exist for ({!s}, {!s})'.format(region, key))

    s = path.suffix
    if s == '.csv':
        result = pd.read_csv(path, dtype={'au2001': str})
    elif s == '.geojson':
        result = gpd.read_file(str(path))
    elif s == '.json':
        with path.open() as src:
            result = json.load(src)
    return result 

def nan_to_none(df):
    """
    Replace the NaN values in the given DataFrame with None and return
    the resulting DataFrame.
    """
    return df.where((pd.notnull(df)), None)

def aggregate_rents(rents, date, groupby_cols=('rental_area', '#bedrooms')):
    """
    Given a DataFrame of rents and a date (YYYY-MM-DD date string), 
    filter the rents to quarters equal to or later than the date, and group the 
    rents by the given groupby columns, recomputing the counts and means.
    Return the resulting data frame, which have the following columns.
    
    - the columns in ``groupby_cols``
    - ``'territory'``
    - ``'region'``
    - ``'rent_count'``
    - ``'rent_mean'``
    - ``'rent_geo_mean'``
    
    """
    cond = rents['quarter'] >= date
    f = rents[cond].copy()
    
    def my_agg(group):
        d = {}
        d['territory'] = group['territory'].iat[0]
        d['region'] = group['region'].iat[0]
        d['rent_count'] = group['rent_count'].sum()
        d['rent_mean'] = (group['rent_mean']*group['rent_count']).sum()/d['rent_count']
        d['rent_geo_mean'] = (group['rent_geo_mean']**(group['rent_count']/d['rent_count'])).prod()
        return pd.Series(d)

    g = f.groupby(groupby_cols).apply(my_agg).reset_index()
    return g

def get_secret(key, secrets_path=ROOT/'secrets.json'):
    """
    Open the JSON file at ``secrets_path``, and return the value corresponding to the given key. 
    """
    secrets_path = Path(secrets_path)
    with secrets_path.open() as src:
        secrets = json.load(src)
    return secrets[key]

def get_latest_quarters(n):
    """
    Return a list of the latest ``n`` (positive integer) rental data quarters as YYYY-MM-DD datestrings sorted chronologically.
    Each quarter will be of the form YYYY-03-01, YYYY-06-01, YYYY-09-01, or YYYY-12-01.
    """
    return [q.strftime('%Y-%m') + '-01' for q in pd.date_range(end=dt.datetime.now(), freq='Q', periods=n)]

