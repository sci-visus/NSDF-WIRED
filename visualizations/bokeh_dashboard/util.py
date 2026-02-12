import time
import datetime
import pandas as pd
import numpy as np
from pyproj import Proj, CRS, Transformer

### Helper functions ###


def latlon_to_mercator(lat, lon):
    """
    Return a tuple of the given lat/lon coordinates in mercator projection
    ref: https://pyproj4.github.io/pyproj/stable/gotchas.html#gotchas
    
    Args:
        lat (float): Latitude in degrees.
        lon (float): Longitude in degrees.

    Returns:
        tuple[float, float]: (x, y) coordinates in mercator projection.
    """
    # get coordinate reference system for EPSG:4326 (used for GPS lat/lon)
    # and mercator (the CRS supported by bokeh)
    source_crs = CRS("EPSG:4326")  # geographic coordinate system (latitude, longitude)
    dest_crs = CRS("EPSG:3857")  # web mercator projection

    # create transformer from geographic coordinate system to web mercator
    transformer = Transformer.from_crs(source_crs, dest_crs)

    # transform points and save to iterator
    mercator_coords = transformer.transform(lat, lon)

    return mercator_coords


def latlon_to_mercator_iter(latlon_tuples):
    """
    Return an iterator/generator of tuples of the given lat/lon coordinates in mercator projection
    ref: https://pyproj4.github.io/pyproj/stable/gotchas.html#gotchas

    Args:
        latlon_tuples (list): a list of tuples, each tuple holding a lat/lon coordinate
    """
    # get coordinate reference system for EPSG:4326 (used for GPS lat/lon)
    # and mercator (the CRS supported by bokeh)
    source_crs = CRS("EPSG:4326")  # geographic coordinate system (latitude, longitude)
    dest_crs = CRS("EPSG:3857")  # web mercator projection

    # create transformer from geographic coordinate system to web mercator
    transformer = Transformer.from_crs(source_crs, dest_crs)

    # transform points and save to iterator
    mercator_iter = transformer.itransform(latlon_tuples)

    return mercator_iter


def parse_tflag(tflag):
    """
    Return the tflag as a datetime object
    :param list tflag: a list of two int32, the 1st representing date and 2nd representing time
    """
    # obtain year and day of year from tflag[0] (date)
    date = int(tflag[0])
    year = date // 1000  # first 4 digits of tflag[0]
    day_of_year = date % 1000  # last 3 digits of tflag[0]

    # create datetime object representing date
    final_date = datetime.datetime(year, 1, 1) + datetime.timedelta(
        days=day_of_year - 1
    )

    # obtain hour, mins, and secs from tflag[1] (time)
    time = int(tflag[1])
    hours = time // 10000  # first 2 digits of tflag[1]
    minutes = (time % 10000) // 100  # 3rd and 4th digits of tflag[1]
    seconds = time % 100  # last 2 digits of tflag[1]

    # create final datetime object
    full_datetime = datetime.datetime(
        year, final_date.month, final_date.day, hours, minutes, seconds
    )
    return full_datetime


def get_pd_timestamp(year, month, day, hour):
    """
    return a pandas timestamp using the given date-time arguments
    :param int year: year
    :param int month: month
    :param int day: day
    :param int hour: hour
    """
    # Convert year, month, day, and hour to a datetime object
    full_datetime = datetime.datetime(year, month, day, hour)

    # Extract components from the datetime object
    year = full_datetime.year
    day_of_year = full_datetime.timetuple().tm_yday
    hours = full_datetime.hour
    minutes = full_datetime.minute
    seconds = full_datetime.second

    # Compute tflag[0] and tflag[1]
    tflag0 = year * 1000 + day_of_year
    tflag1 = hours * 10000 + minutes * 100 + seconds

    # Return the Pandas Timestamp object
    return pd.Timestamp(full_datetime)


def get_datetime(year, month, day, hour):
    """
    Return a datetime timestamp
    """
    pd_t = get_pd_timestamp(year, month, day, hour)
    return pd.to_datetime(pd_t, utc=True)
