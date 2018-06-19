#!/usr/bin/python
# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from scrapy.selector import HtmlXPathSelector
from itunesappspider.items import ItunesappspiderItem
import urllib
import scrapy
import logging
import json

"""
the spider class, which will read and parse the url from itunes app store
    and extract the information for @see items.py;
    data crawled will be stored into MongoDB database
"""



class Itunesappspider(CrawlSpider):
    # define the name of the spider
    name = "ItunesAppSpider"

    # set the allowed domain to crawl
    # see document https://doc.scrapy.org/en/latest/topics/spiders.html
    #allowed_domains = ['itunes.apple.com']
    allowed_domains = []

    # start_urls to process
    start_urls =[
        "https://itunes.apple.com/cn/genre/ios/id36",
    ]

    # define the rule for Crawler
    '''
     please notice that the scrapy will check the first rule and the second, third
    '''
    rules = (
        Rule(LinkExtractor(allow=(r'https://itunes\.apple\.com/cn/app/.*/id\d+')), follow=True, callback='itunes_parse_item'),
        Rule(LinkExtractor(allow=(r'^https://itunes\.apple\.com/cn/genre/ios-%E7%A4%BE%E4%BA%A4/id6005')), follow=True), # 社交
        Rule(LinkExtractor(allow=(r'^https://itunes\.apple\.com/cn/genre/ios-%E6%96%B0%E9%97%BB/id6009')), follow=True), # 新闻
        Rule(LinkExtractor(allow=(r'^https://itunes\.apple\.com/cn/genre/ios-%E5%B7%A5%E5%85%B7/id6002')), follow=True), # 工具
        Rule(LinkExtractor(allow=(r'^https://itunes\.apple\.com/cn/genre/ios-%E6%8A%A5%E5%88%8A%E6%9D%82%E5%BF%97/id6021')), follow=True), # 报刊杂志
    )

    def itunes_parse_item(self, response):
        item = ItunesappspiderItem()

        jsondata = json.loads(response.xpath('//script[@id="shoebox-ember-data-store"]/text()').extract_first())

	# 苹果APP ID, 同customersAlsoBought和moreByThisDeveloper中的ID 
        item["ID"] = jsondata["data"]["id"]

	# 名称
        item["name"] = jsondata["data"]["attributes"]["name"]

	# 链接 
        item["link"] = str(response.url)

	# 图标
        item["icon"] =  jsondata["included"][2]["attributes"]["url"].split('png')[0] + "png/230x0w.jpg"

	# 最新版本
        item["lastVersion"] = jsondata["data"]["attributes"]["versionHistory"][0]["versionString"]

	# 最新版本发布日期
        item["lastUpdate"] = jsondata["data"]["attributes"]["versionHistory"][0]["releaseDate"][0:10]

        if "chartPositionForStore" in jsondata["data"]["attributes"].keys():
	    # 类别 
            item["category"] = jsondata["data"]["attributes"]["chartPositionForStore"]["appStore"]["genreName"]

	    # 同类排名 
            item["ranking"] = jsondata["data"]["attributes"]["chartPositionForStore"]["appStore"]["position"]
        else:
	    # 类别 
            item["category"] = json.loads(response.xpath('//script[@type="application/ld+json"]/text()').extract_first())["applicationCategory"]


	# 价格 
        item["price"] = jsondata["included"][0]["attributes"]["priceFormatted"]

	# 大小. 单位：字节 
        item["size"] = jsondata["data"]["attributes"]["size"]

	# 简介 
        item["description"] = jsondata["data"]["attributes"]["description"]

	# 兼容性 
        item["compatibility"] = jsondata["data"]["attributes"]["softwareInfo"]["requirementsString"]

	# 语言 
        item["language"] = jsondata["data"]["attributes"]["softwareInfo"]["languagesDisplayString"]

	# 评论量
        item["reviewCount"] = jsondata["data"]["attributes"]["userRating"]["ratingCount"]

	# 评分
        item["reviewRating"] = jsondata["data"]["attributes"]["userRating"]["value"]

	# 年龄分级
        advisories = ""
        for s in  jsondata["data"]["attributes"]["advisories"]:
            advisories +=  s + ", "
        advisories = advisories.rstrip(', ')

        item["ageRating"] = jsondata["data"]["attributes"]["ratingText"] + advisories

        # 版权 
        item["copyright"] = jsondata["data"]["attributes"]["copyright"]

	# 销售商
        item["seller"] = jsondata["data"]["attributes"]["softwareInfo"]["seller"]

	# 开发人员网站
        item["developerUrl"] = jsondata["data"]["attributes"]["softwareInfo"]["websiteUrl"]

	# App支持
        item["supportUrl"] = jsondata["data"]["attributes"]["softwareInfo"]["supportUrl"]

	# 更多来自此开发人员的App id列表
        if "moreByThisDeveloper" in jsondata["data"]["relationships"].keys():
            item["moreByThisDeveloper"] = [(d["id"]) for d in jsondata["data"]["relationships"]["moreByThisDeveloper"]["data"]]

	# 可能感兴趣的类似App id列表
        if "customersAlsoBoughtApps" in jsondata["data"]["relationships"].keys():
            item["customersAlsoBought"] = [(d["id"]) for d in jsondata["data"]["relationships"]["customersAlsoBoughtApps"]["data"]]

        yield item
