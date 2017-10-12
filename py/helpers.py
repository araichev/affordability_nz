"""
This module contains the functions that create most of data files for
a particular region of New Zealand.
It assumes that you have the created the following files for a region
<region> already::

    |- data/
        |- processed/
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

def get_secret(key, secrets_path=ROOT/'secrets.json'):
    """
    Open the JSON file at ``secrets_path``, and return the value
    corresponding to the given key.
    """
    secrets_path = Path(secrets_path)
    with secrets_path.open() as src:
        secrets = json.load(src)
    return secrets[key]

def get_path(key, region=None):
    """
    Return the path (Path object) of the file corresponding to the given
    key (string) and region (string).
    """
    path = DATA_DIR/'processed'
    error = ValueError('Invalid key-region pair ({!s}, {!s})'.format(
      key, region))
    if region is None:
        if key == 'property_titles':
            # Special case using collected data
            path = DATA_DIR/'collected'/'nz-cadastral-titles-jan-10.gpkg'
        elif key == 'au2001_csv':
            path /= 'au2001.csv'
        elif key == 'au2001':
            path /= 'au2001.geojson'
        elif key == 'rental_areas_csv':
            path /= 'rental_areas.csv'
        elif key == 'rental_areas':
            path /= 'rental_areas.geojson'
        elif key == 'rental_points':
            path /= 'rental_points.geojson'
        elif key == 'rents':
            path /= 'rents.csv'
        else:
            raise error
    else:
        path /= region
        if key == 'rental_areas':
            path /= 'rental_areas.geojson'
        elif key == 'rental_points':
            path /= 'rental_points.geojson'
        elif key == 'rents':
            path /= 'rents.csv'
        elif key == 'rents_json':
            path /= 'rents.json'
        elif key == 'commutes_walking':
            path /= 'commutes_walking.csv'
        elif key == 'commutes_bicycling':
            path /= 'commutes_bicycling.csv'
        elif key == 'commutes_driving':
            path /= region/'commutes_driving.csv'
        elif key == 'commutes_transit':
            path /= 'commutes_transit.csv'
        elif key == 'transit_costs':
            path /= 'transit_costs.csv'
        elif key == 'commute_costs':
            path /= 'commute_costs.json'
        else:
            raise error

    return path

def get_data(key, region=None):
    """
    Return the data corresponding to the given key (string) and
    region (string) and key.
    """
    path = get_path(key, region)
    if not path.exists:
        raise ValueError('Data does not exist for key-region pair'
         ' ({!s}, {!s})'.format(key, region))

    s = path.suffix
    if s == '.csv':
        result = pd.read_csv(path, dtype={'au2001': str})
    elif s in ['.geojson', '.gpkg']:
        result = gpd.read_file(str(path))
    elif s == '.json':
        with path.open() as src:
            result = json.load(src)
    return result

def get_latest_quarters(n, from_data=True):
    """
    Return a list of the latest ``n`` (positive integer)
    rental data quarters as YYYY-MM-DD datestrings sorted
    chronologically.
    Each quarter will be of the form YYYY-03-01, YYYY-06-01,
    YYYY-09-01, or YYYY-12-01.
    If ``from_data``, then get the latest quarters from the stored
    rental data.
    Otherwise, get the latest quarters theoretically possible from
    today's date.
    """
    if from_data:
        quarters = get_data('rents')['quarter'].unique()[-n:].tolist()
    else:
        quarters = [q.strftime('%Y-%m') + '-01' for q in
          pd.date_range(end=dt.datetime.now(), freq='Q', periods=n)]
    return(quarters)

def aggregate_rents(rents, date=None, groupby_cols=('rental_area',
  '#bedrooms')):
    """
    Given a DataFrame of rents, group the rents by the given groupby
    columns, recomputing the counts and means.
    Return the resulting data frame, which have the following columns.

    - the columns in ``groupby_cols``
    - ``'territory'``
    - ``'region'``
    - ``'rent_count'``
    - ``'rent_mean'``
    - ``'rent_geo_mean'``

    If a date (YYYY-MM-DD date string) is given, then first slice the
    rents to calendar quarters equal to or later than the date.
    """

    if date is not None:
        cond = rents['quarter'] >= date
        f = rents[cond].copy()
    else:
        f = rents.copy()

    def my_agg(group):
        d = {}
        if 'territory' not in groupby_cols:
            d['territory'] = group['territory'].iat[0]
        if 'region' not in groupby_cols:
            d['region'] = group['region'].iat[0]
        d['rent_count'] = group['rent_count'].sum()
        d['rent_mean'] = (group['rent_mean']*group['rent_count']).sum()/\
          d['rent_count']
        d['rent_geo_mean'] = (group['rent_geo_mean']**(
          group['rent_count']/d['rent_count'])).prod()
        return pd.Series(d)

    g = f.groupby(groupby_cols).apply(my_agg).reset_index()
    return g

def nan_to_none(df):
    """
    Replace the NaN values in the given DataFrame with None and return
    the resulting DataFrame.
    """
    return df.where((pd.notnull(df)), None)

def build_json_rents(rents):
    """
    Given a DataFrame of rents of the form output by
    :func:read_data('rents'), aggregate the rents by rental area
    and number of bedrooms ('1', '2', '3', or '4'), and return the
    result as a dictionary of the form
    rental area -> #bedrooms -> rent geometric mean.
    Some of the mean rents could be ``None``.
    """
    f = aggregate_rents(rents)

    # Drop 5+ bedrooms and round to nearest dollar
    f = f[f['#bedrooms'] != '5+'].copy().round()

    # Replace NaN with None to make JSON-compatible
    f = nan_to_none(f)

    # Save to dictionary of form rental area -> #bedrooms -> rent geo mean
    d = {area: dict(g[['#bedrooms', 'rent_geo_mean']].values)
      for area, g in f.groupby('rental_area')}

    return d
