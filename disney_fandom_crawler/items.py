# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field, item


class Character(Item):
    thumbnail = Field()
    url = Field()
    image = Field()
    name = Field()
    feature_films = Field()
    short_films = Field()
    shows = Field()
    games = Field()
    rides = Field()
    animator = Field()
    designer = Field()
    voice = Field()
    portrayed_by = Field()
    performance_model = Field()
    inspiration = Field()
    awards = Field()
    fullname = Field()
    other_names = Field()
    occupation = Field()
    affiliations = Field()
    home = Field()
    likes = Field()
    dislikes = Field()
    powers = Field()
    paraphernalia = Field()
    status = Field()
    parents = Field()
    siblings = Field()
    family = Field()
    partner = Field()
    children = Field()
    pets = Field()


class Location(Item):
    name = Field()
    thumbnail = Field()
