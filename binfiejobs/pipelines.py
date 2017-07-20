# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BinfiejobsPipeline (object):
    def process_item(self, item, spider):
        return item

import json
from datetime import datetime

class JsonWriterPipeline(object):

    def open_spider(self, spider):
        now = datetime.now()
        dt_str = datetime.strftime (now, '%Y%m%d')
        file_name = 'binfie-%s.jl' % dt_str
        self.file = open (file_name, 'w+')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
