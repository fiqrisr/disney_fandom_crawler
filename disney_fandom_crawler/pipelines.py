# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonItemExporter
import os

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class JsonWriterPipeline:
    def open_spider(self, spider):
        if not os.path.exists("output/%s" % spider.name):
            os.system("mkdir -p output/%s" % spider.name)

        self.file = open("output/%s/out.json" % spider.name, "w+b")
        self.exporter = JsonItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
