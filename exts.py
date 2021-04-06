#!/usr/bin/env python
# -* coding: utf-8 -*-
import os, time, random
from modules import cordsCalculator as CC, tilesProcessor as TP, tiffConverter as TC

def downloadImage(tl_lng, tl_lat, br_lng, br_lat, zoom):
    tl_row, tl_col = CC.lngLat2RowCol(float(tl_lng), float(tl_lat), int(zoom))
    br_row, br_col = CC.lngLat2RowCol(float(br_lng), float(br_lat), int(zoom))

    base_url = 'http://t0.tianditu.gov.cn/img_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=img&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX=%s&TILEROW=%s&TILECOL=%s&tk=xxxxx'
    ctime = int(time.time())
    root_dir = os.path.join("tiles", str(ctime))  # 防止斜杠被转义而创建文件夹失败

    # 创建根目录
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)

    # 下载地图瓦片
    print("#------ downloading tiles ------#")
    for r in range(tl_row, br_row + 1):
        for c in range(tl_col, br_col + 1):
            url = base_url%(zoom, r, c)
            file_name = os.path.join(root_dir, str(r) + "-" + str(c) + '.jpg')
            TP.downloadTile(url, file_name)
            time.sleep(random.random())
    print("#------ tiles downloaded ------#")

    # 拼接，返回图片宽高
    print("#------ merging tiles ------#")
    merge_image_path = os.path.join("merge", "jpg", str(ctime) + ".jpg")
    total_width, total_height = TP.mergeTiles(root_dir, merge_image_path)
    print("#------ tiles merged ------#")

    # gcp示例
    # gcp_items = [
    #     [113.203125, 22.431340156360612, 0, 0],         # 左上，0行0列
    #     [113.73046875, 22.431340156360612, 767, 0],     # 右上，0行x列
    #     [113.203125, 21.943045533438177, 0, 767],       # 左下，y行0列
    #     [113.73046875, 21.943045533438177, 767, 767]    # 右下，y行x列
    # ]

    # 转为tiff
    tl_lng2, tl_lat2 = CC.rowCol2LngLat(tl_row, tl_col, int(zoom))           # 左上角瓦片的左上角经纬度
    br_lng2, br_lat2 = CC.rowCol2LngLat(br_row + 1, br_col + 1, int(zoom))   # 右下角瓦片的右下角经纬度
    gcp_items = [
        [tl_lng2, tl_lat2, 0, 0],
        [br_lng2, tl_lat2, total_width - 1, 0],
        [tl_lng2, br_lat2, 0, total_height - 1],
        [br_lng2, br_lat2, total_width - 1, total_height - 1]
    ]
    tiff_save_path = os.path.join("merge", "tiff", str(ctime) + ".tiff")
    TC.jpg2Tiff(merge_image_path, tiff_save_path, gcp_items)

    return str(ctime) + ".tiff"

    