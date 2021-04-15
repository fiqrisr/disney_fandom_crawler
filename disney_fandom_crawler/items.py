# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field, item


class Character(Item):
    name = Field()
    thumbnail = Field()


class Location(Item):
    name = Field()
    thumbnail = Field()
