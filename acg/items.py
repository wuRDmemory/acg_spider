# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AcgItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 文件夹的名称
    dir_name = scrapy.Field(serializer=str);
    lm_url = scrapy.Field(serializer=str);
    page_num = scrapy.Field(serializer=int);
    img_url = scrapy.Field(serializer=str);
    img_name = scrapy.Field(serializer=str);
