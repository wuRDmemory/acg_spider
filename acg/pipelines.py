# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from acg.items import AcgItem;
from acg import settings;
from http.client import IncompleteRead;

import urllib.error;
import urllib.request;
import urllib.parse;
import numpy as np;
import cv2;
import os;

class AcgPipeline(object):

    ''' 初始化函数 '''
    def __init__(self):
        self.img_seen = set();

    ''' 执行函数 '''
    def process_item(self, item, spider):
        # 判断是否见过这个image_name
        if item["img_name"] in self.img_seen:
            # 如果是的话打印出信息
            print(">>>  [pipeline] -> old url is used!");
            # 并返回
            return item;
        else:
            # 把图片给resize一下，防止过大
            maxSize = 512;
            # 获取url
            url = item["img_url"];
            # 模仿浏览器进行访问
            req = urllib.request.Request(url=url);
            req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1");
            # req.add_header("GET",url);
            # req.add_header("Host", "img.gov.com.de");
            req.add_header("Referer", url);
            # 数据的获取
            try:
                # 获取该数据
                res = urllib.request.urlopen(req, timeout=100).read();
                # 转化为numpy类型的数据
                image = np.asarray(bytearray(res), dtype="uint8");
                # 转化为opencv的数据
                image = cv2.imdecode(image, cv2.IMREAD_COLOR);
                # reszie
                imgResize = cv2.resize(image, dsize=(maxSize, maxSize), interpolation=cv2.INTER_CUBIC);
                # 存储
                # 先确定要存储的位置
                path = settings.SAVE_PATH+item["dir_name"];
                # 判断是否有该位置的文件夹，没有则重新建立
                if not os.path.exists(settings.SAVE_PATH):
                    os.makedirs(path);
                # 生成图片保存的路径
                img_path = path + "/" + item["img_name"] + ".jpg";
                # 保存图片
                cv2.imwrite(img_path, imgResize);
                # 打印保存信息
                print(">>>  [pipeline] -> image saves in %s" % img_path);
            except urllib.error.HTTPError as e:
                print(">>>  [pipeline] -> HTTPError occur, it's code is %s" % str(e.code));
            except (IncompleteRead) as e:
                print(">>>  [pipeline] -> IncompleteRead occur, it's code is %s" % str(e.code));
            except urllib.error.URLError as e:
                print(">>>  [pipeline] -> URLError occur, it's code is %s" % str(e.code));
            # 别忘了返回item
            return item;
