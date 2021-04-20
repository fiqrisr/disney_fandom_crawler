import scrapy
import logging
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
        loader.add_css("games", selectors["CHARACTER_GAMES"])
        loader.add_css("rides", selectors["CHARACTER_RIDES"])
        loader.add_css("animator", selectors["CHARACTER_ANIMATOR"])
        loader.add_css("designer", selectors["CHARACTER_DESIGNER"])
        loader.add_css("voice", selectors["CHARACTER_VOICE"])
        loader.add_css("portrayed_by", selectors["CHARACTER_PORTRAYED_BY"])
        loader.add_css("performance_model", selectors["CHARACTER_PERFORMANCE_MODEL"])
        loader.add_css("inspiration", selectors["CHARACTER_INSPIRATION"])
        loader.add_css("awards", selectors["CHARACTER_AWARDS"])
        loader.add_css("fullname", selectors["CHARACTER_FULLNAME"])
        loader.add_css("other_names", selectors["CHARACTER_OTHER_NAMES"])
        loader.add_css("occupation", selectors["CHARACTER_OCCUPATION"])
        loader.add_css("affiliations", selectors["CHARACTER_AFFILIATIONS"])
        loader.add_css("home", selectors["CHARACTER_HOME"])
        loader.add_css("likes", selectors["CHARACTER_LIKES"])
        loader.add_css("dislikes", selectors["CHARACTER_DISLIKES"])
        loader.add_css("powers", selectors["CHARACTER_POWERS"])
        loader.add_css("paraphernalia", selectors["CHARACTER_PARAPHERNALIA"])
        loader.add_css("status", selectors["CHARACTER_STATUS"])
        loader.add_css("parents", selectors["CHARACTER_PARENTS"])
        loader.add_css("siblings", selectors["CHARACTER_SIBLINGS"])
        loader.add_css("family", selectors["CHARACTER_FAMILY"])
        loader.add_css("partner", selectors["CHARACTER_PARTNER"])
        loader.add_css("children", selectors["CHARACTER_CHILDREN"])
        loader.add_css("pets", selectors["CHARACTER_PETS"])

        if len(loader.get_css(selectors["CHARACTER_NAME"])) < 1:
            loader.add_css("name", selectors["PAGE_HEADER_TITLE"])

        if len(loader.get_css(selectors["CHARACTER_IMAGE"])) < 1:
            loader.add_css("image", selectors["CHARACTER_THUMB_IMAGE"])

        logging.info("Crawl %s" % loader.get_collected_values("name"))

        char = loader.load_item()
        yield char
