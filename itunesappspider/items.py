# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in: # http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ItunesappspiderItem(scrapy.Item):
    # define the fields for your item here like:
    ID = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    icon = scrapy.Field()
    lastVersion = scrapy.Field()
    lastUpdate = scrapy.Field()
    category = scrapy.Field()
    ranking = scrapy.Field()
    price = scrapy.Field()
    size = scrapy.Field()
    description = scrapy.Field()
    compatibility = scrapy.Field()
    language = scrapy.Field()
    reviewCount = scrapy.Field()
    reviewRating = scrapy.Field()
    ageRating = scrapy.Field()
    copyright = scrapy.Field()
    seller = scrapy.Field()
    developerUrl = scrapy.Field()
    supportUrl = scrapy.Field()
    moreByThisDeveloper = scrapy.Field()
    customersAlsoBought = scrapy.Field()
