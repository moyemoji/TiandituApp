# -*- coding: utf-8 -*-
#!/usr/bin/env pcolthon
from osgeo import gdal

# gcp = gdal.GCP(x, y, z, pixel, line)
# x: 横坐标/经度    GCP.GCPX
# y：纵坐标/维度    GCP.GCPY
# z：高程
# pixel：原图列数   GCP.GCPPixel
# line: 原图行数    GCP.GCPLine

# gdal.TranslateOptions()
# format：转出格式
# outputSRS：输出坐标系
# GCPs：控制点列表

# gcp示例
gcp_items = [
    [113.203125, 22.431340156360612, 0, 0],         # 左上，0行0列
    [113.73046875, 22.431340156360612, 767, 0],     # 右上，0行x列
    [113.203125, 21.943045533438177, 0, 767],       # 左下，y行0列
    [113.73046875, 21.943045533438177, 767, 767]    # 右下，y行x列
]

def jpg2Tiff(jpg_path, tiff_save_path, gcp_items):
    gcp_list = []
    for item in gcp_items:
        x, y, pixel, line = item
        z = 0
        gcp = gdal.GCP(x, y, z, pixel, line)
        gcp_list.append(gcp)

    options = gdal.TranslateOptions(format='GTiff', outputSRS='EPSG:4326',GCPs=gcp_list)
    gdal.Translate(tiff_save_path, jpg_path, options=options)