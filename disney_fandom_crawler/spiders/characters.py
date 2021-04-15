import scrapy
from disney_fandom_crawler.items import Character
from disney_fandom_crawler.constants import selectors, characters_string_skip_list


class CharactersSpider(scrapy.Spider):
    name = "characters"
    allowed_domains = ["disney.fandom.com"]
    start_urls = ["https://disney.fandom.com/wiki/Category:Disney_characters"]

    def parse(self, response):
        for item in response.css(selectors["CATEGORY_LIST_SELECTOR"]):
            name = item.css(selectors["CATEGORY_NAME_SELECTOR"]).get()

            if any(el in name for el in characters_string_skip_list):
                continue

            thumbnail = item.css(selectors["CATEGORY_THUMBNAIL_SELECTOR"]).get()

            char = Character()
            char["name"] = name
            char["thumbnail"] = thumbnail

            yield char

        next_page = response.css(selectors["CATEGORY_NEXT_PAGE_SELECTOR"])

        if next_page:
            yield from response.follow_all(next_page, self.parse)
