# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import logging

fileName = 'itunesapp.json'

class ItunesappspiderPipeline(object):
    def __init__(self):
        # json
        with open(fileName, 'w') as f:
            f.write('[\n')

    def open_spider(self, spider):
       return 


    def close_spider(self, spider):
        # json
        with open(fileName, 'r') as f:
            content = f.read()
        with open(fileName, 'w') as f:
            f.write(content[:-1] + "\n]")

    def process_item(self, item, spider):
        #if str(item['Link']).find('details?id') != - 1:
        # json
        line = json.dumps(dict(item), ensure_ascii=False, indent=4) + ','
        with open(fileName, 'a') as f:
            f.write(line)
        return item
