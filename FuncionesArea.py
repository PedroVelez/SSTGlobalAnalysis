# Funciones --------------------------------------------------------------
from shapely.geometry import Polygon, Point
from shapely.ops import transform
import pyproj
import xarray as xr
import numpy as np

def transform_polygon(polygon, src_crs='epsg:4326', tgt_crs='epsg:4326'):
    proj = pyproj.Transformer.from_proj(pyproj.Proj(src_crs), pyproj.Proj(tgt_crs), always_xy=True)
    return transform(lambda x, y: proj.transform(x, y), polygon)

def point_in_polygon(lon, lat, polygon):
    point = Point(lon, lat)
    return polygon.contains(point)

def locate(value: float,array : np.ndarray) -> int:
    """
    Return index from the array's element closest to value.
    :param value: float to search
    :param array: array in which to search
    :return: array index
    """
    dist = abs(value - array)
    index = np.argmin(dist)
    return index
#---------------------------------------------------------------------<<<<