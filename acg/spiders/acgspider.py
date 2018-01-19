#!/usr/bin/env python
# coding:utf-8

from acg.items import AcgItem;
from acg import settings;
import os;
import scrapy;
import urllib.request;
import urllib.parse;


class acgspiders(scrapy.Spider):
    ''' 爬取一个网站 '''
    name = 'images';
    start_urls = [
        "http://www.acg.fi",
    ];
    count = 0;
    page = 1;

    ''' 三级爬取 '''
    ''' 该部分主要获取要取得的内容 '''
    def parse3(self, response):
        # 判断已经获取了多少张图片了
        # 如果获取了够3000张图片了，就返回
        if self.count >= 3000:
            return None;
        # 先获取item
        item = response.meta["item"];
        # 抓取图片的url
        image_url = response.xpath("//article[@class='article-content']//img/@src").extract();
        # 打印一共有多少个图片url
        print("一共找到图片%d张" % len(image_url));
        # 进行图片的抓取
        for url in image_url:
            url = urllib.request.quote(url,safe='/:?=.!');
            if "jpg" in url:
                self.count += 1;
                item["img_url"] = url;
                item["img_name"] = "img"+str(self.count);
                yield item;
            if "png" in url:
                self.count += 1;
                item["img_url"] = url;
                item["img_name"] = "img"+str(self.count);
                yield item;


    ''' 二级爬取 '''
    ''' 该爬取主要是将各栏目中的页面的url给爬取出来 '''
    def parse2(self, response):
        # 先获取item
        item = response.meta["item"];
        # 爬取该栏目下的分页情况
        pages_url = response.xpath("//div[@class='fenye']//a/@href").extract();
        # 这个num主要是为了产生各下级页面的url
        num = 1;
        # 先判断该栏目是否只有一个页面
        if len(pages_url)==0:
            # 如果是的话，把该栏目该页的url作为iterator的内容给parse3
            page = response.xpath("//h1[@class='article-title']//a/@href").extract_first();
            yield scrapy.Request(page, meta={"item":item}, callback=self.parse3);
        else:
            # 如果该栏目下有多页的话，则把各个页面的url取出来
            # 这里一定要进行切片操作，因为每次进来的都是第一页，而下面总会有一个
            # 按钮名曰“下一页”，这里就是要舍弃这个下一页
            for page in pages_url[:len(pages_url)-1]:
                # 对该页面进行请求
                yield scrapy.Request(page, meta={"item":item}, callback=self.parse3);
                # 下级页面自加
                num+=1;
        # 打印当前自己爬取了多少界面
        print(">>>  [parse2] -> 该栏目一共有%d个分页" % num);


    ''' 一级爬取 '''
    ''' 该爬取主要找到当前界面下有多少个栏目（二级界面） '''
    def parse1(self, response):
        # 首先获取item的值
        item = response.meta["item"];
        # 爬取该网站下的二级界面
        pages_url = response.xpath("//div[@class='card-item']//h3//a/@href").extract();
        # 打印出来找到了多少个二级页面
        print(">>>  [parse1] -> %s栏目的第%d页一共有%d个卡片" % (item["dir_name"],int(item["page_num"]),len(pages_url)));
        # 生成generator
        for url in pages_url:
            yield scrapy.Request(url,meta={"item":item}, callback=self.parse2);
        # 爬到网页数自加，由于网页数量可能比较多，因此不希望无限制的抓取下去
        if item["page_num"] < 20:
            item["page_num"]=item["page_num"]+1;
        print(">>>  [parse1] -> item's page_num is : %d" % item["page_num"]);
        # 找寻下个一级页面
        next_url = item["lm_url"]+"/page/"+str(item["page_num"]);
        # 这里只生成一个generator
        yield scrapy.Request(next_url,meta={"item":item},callback=self.parse1);

    ''' 初级爬取 '''
    ''' 该函数主要找到该网站下的各个分栏，之后给parse1 '''
    def parse(self, response):
        # 抓取分栏
        # 要拿到名称和链接
        lm_name = response.xpath("//li[contains(@id,'menu-item')]//a/text()").extract();
        lm_url = response.xpath("//li[contains(@id,'menu-item')]//a/@href").extract();
        # 去除首页和后面的分栏
        for idx in range(1,7):
            # 建立文件夹
            # 先确定要存储的位置
            path = settings.SAVE_PATH+lm_name[idx];
            # 判断是否有该位置的文件夹，没有则重新建立
            if not os.path.exists(path):
                os.mkdir(path);
            # 打印栏目的名称和url
            print(">>>  [parse] -> 栏目名称 : %s  url : %s" % (lm_name[idx],lm_url[idx]));
            # 产生一个item
            item = AcgItem();
            item["dir_name"] = str(lm_name[idx]);
            item["lm_url"] = str(lm_url[idx]);
            item["page_num"] = 1;
            # 这里预留图像的url和img_name的值
            # 生成generator
            yield scrapy.Request(lm_url[idx], meta={"item":item}, callback=self.parse1);
