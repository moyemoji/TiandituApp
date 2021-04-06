# -*- coding: utf-8 -*-
#!/usr/bin/env pcolthon
import http, time, random
import urllib.request
import glob, re
from PIL import Image



def getHeader():
    USER_AGENTS = [
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
    ]

    user_agent = random.choice(USER_AGENTS)
    headers = {
        'User-Agent':user_agent
    }

    return headers


def downloadTile(url, file_name, num_retries=3):
    """
        下载瓦片图片
        url：瓦片地址
        file_name：瓦片图片保存地址
        num_retries：重试次数
    """
    try:
        headers = getHeader()
        request = urllib.request.Request(url, headers=headers)
        res = urllib.request.urlopen(request)
        with open(file_name, "wb") as f:
            content = res.read()
            f.write(content)
            res.close()
    except http.client.IncompleteRead or http.client.RemoteDisconnected:
        if num_retries == 0: # 重连机制
            return
        else:
            downloadTile(url, file_name, num_retries - 1)


def sortImagePath(root_dir):
    """
        对根目录下的瓦片进行排序
        root_dir：瓦片图片根目录
        image_path_list：排序后的瓦片路径列表
    """
    # 按照x、y顺序对文件名进行排序
    images = glob.glob(root_dir+'/*.jpg')
    images.sort(key=lambda x: tuple(int(i) for i in re.findall(r'\d+', x)[:2]))

    # 将每一行文件名保存到一个字典中
    image_path_dict = {}
    for item in images:
        match = re.search(r'(\d+)-(\d+)', item)
        pre = int(match.group(1))

        if not image_path_dict.get(pre):
            image_path_dict[pre] = []
            
        image_path_dict[pre].append(item)

    # 键值对转排序后的列表
    image_path_list = sorted(zip(image_path_dict.keys(), image_path_dict.values()))
    return image_path_list


def mergeTiles(root_dir, merge_image_path):
    """
        拼合瓦片图片
        root_dir：瓦片图片根目录
        merge_image_path：拼合图片保存地址
    """
    image_path_list = sortImagePath(root_dir)

    # 预先生成合并后大小的空图片
    total_height = len(image_path_list) * 256
    total_width = len(image_path_list[0][1]) * 256
    new_image = Image.new("RGB", (total_width, total_height))

    # 逐行拼接
    y_offset = 0
    for item in image_path_list:
        x_offset = 0
        images = list(map(Image.open, item[1])) # 映射函数，返回列表
        for subitem in images:
            new_image.paste(subitem, (x_offset, y_offset))
            x_offset += subitem.size[0]
        y_offset += images[0].size[0]

    new_image.save(merge_image_path, quality = 100)

    return total_width, total_height