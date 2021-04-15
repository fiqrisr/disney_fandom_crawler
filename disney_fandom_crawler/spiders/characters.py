import scrapy
from disney_fandom_crawler.items import Character


class CharactersSpider(scrapy.Spider):
    name = "characters"
    allowed_domains = ["disney.fandom.com"]
    start_urls = ["https://disney.fandom.com/wiki/Category:Disney_characters"]

    def parse(self, response):
        LIST_SELECTOR = "li.category-page__member"
        NAME_SELECTOR = "a.category-page__member-link::text"
        THUMBNAIL_SELECTOR = "img.category-page__member-thumbnail::attr(src)"
        NEXT_PAGE_SELECTOR = "a.category-page__pagination-next::attr(href)"

        skip_this = [
            "Disney characters",
            "Category:",
            "User blog:",
            "Disney Prince",
            "Disney Princess",
        ]

        for item in response.css(LIST_SELECTOR):
            name = item.css(NAME_SELECTOR).get()

            if any(el in name for el in skip_this):
                continue

            thumbnail = item.css(THUMBNAIL_SELECTOR).get()

            char = Character()
            char["name"] = name
            char["thumbnail"] = thumbnail

            yield char

        next_page = response.css(NEXT_PAGE_SELECTOR)

        if next_page:
            yield from response.follow_all(next_page, self.parse)
