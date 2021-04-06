# -*- coding: utf-8 -*-
#!/usr/bin/env pcolthon
import math



def lngLat2RowCol(lng, lat, zoom):
    """
        经纬度坐标转行列号
        lng：经度
        lat：纬度
        zoom：缩放级别
        row：行号
        col：列号
    """
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    col = int((lng + 180.0) / 360.0 * n)
    row = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return row, col


def rowCol2LngLat(row, col, zoom):
    """
        行列号转经纬度
        row：行号
        col：列号
        zoom：缩放级别
        lng：经度
        lat：纬度
    """
    n = 2.0 ** zoom
    lng = col / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * row / n)))
    lat = math.degrees(lat_rad)
    return lng, lat