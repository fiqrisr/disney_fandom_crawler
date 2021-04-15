import scrapy
from scrapy.loader import ItemLoader
from disney_fandom_crawler.items import Character
from disney_fandom_crawler.constants import selectors, characters_string_skip_list


class CharactersSpider(scrapy.Spider):
    name = "characters"
    allowed_domains = ["disney.fandom.com"]
    start_urls = ["https://disney.fandom.com/wiki/Category:Disney_characters"]

    def parse(self, response):
        for item in response.css(selectors["CATEGORY_LIST"]):
            name = item.css(selectors["CATEGORY_NAME"]).get()

            if any(el in name for el in characters_string_skip_list):
                continue

            thumbnail = item.css(selectors["CATEGORY_THUMBNAIL"]).get()
            url = item.css(selectors["CATEGORY_URL"])

            char = Character()
            char["name"] = name
            char["thumbnail"] = thumbnail

            yield from response.follow_all(
                url, self.parse_detail, cb_kwargs=dict(char=char)
            )

        next_page = response.css(selectors["CATEGORY_NEXT_PAGE"])

        if next_page:
            yield from response.follow_all(next_page, self.parse)

    def parse_detail(self, response, char):
        char["url"] = response.url
        char["feature_films"] = response.css(
            selectors["CHARACTERS_FEATURE_FILMS"]
        ).getall()
        char["short_films"] = response.css(selectors["CHARACTERS_SHORT_FILMS"]).getall()

        yield char
