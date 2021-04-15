import scrapy
from disney_fandom_crawler.items import Character


class CharactersSpider(scrapy.Spider):
    name = "characters"
    allowed_domains = ["disney.fandom.com"]
    start_urls = ["https://disney.fandom.com/wiki/Category:Disney_characters"]

    def parse(self, response):
        skip_this = [
            "Disney Characters",
            "Category:",
            "User blog:",
            "Disney Prince",
            "Disney Princess",
        ]

        for item in response.css("li.category-page__member"):
            name = item.css("a.category-page__member-link::text").get()

            if any(el in name for el in skip_this):
                continue

            thumbnail = item.css("img.category-page__member-thumbnail::attr(src)").get()

            char = Character()
            char["name"] = name
            char["thumbnail"] = thumbnail

            yield char
