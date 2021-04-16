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
            char["thumbnail"] = thumbnail

            yield from response.follow_all(
                url, self.parse_detail, cb_kwargs=dict(char=char)
            )

        # next_page = response.css(selectors["CATEGORY_NEXT_PAGE"])

        # if next_page:
        #     yield from response.follow_all(next_page, self.parse)

    def parse_detail(self, response, char):
        loader = ItemLoader(item=char, response=response)

        loader.add_value("url", response.url)
        loader.add_css("image", selectors["CHARACTER_IMAGE"])
        loader.add_css("name", selectors["CHARACTER_NAME"])
        loader.add_css("feature_films", selectors["CHARACTER_FEATURE_FILMS"])
        loader.add_css("short_films", selectors["CHARACTER_SHORT_FILMS"])
        loader.add_css("shows", selectors["CHARACTER_SHOWS"])

        if len(loader.get_css(selectors["CHARACTER_NAME"])) < 1:
            loader.add_css("name", selectors["PAGE_HEADER_TITLE"])

        if len(loader.get_css(selectors["CHARACTER_IMAGE"])) < 1:
            loader.add_css("image", selectors["CHARACTER_THUMB_IMAGE"])

        char = loader.load_item()
        yield char
