selectors = {
    "CATEGORY_LIST": "li.category-page__member",
    "CATEGORY_NAME": "a.category-page__member-link::text",
    "CATEGORY_THUMBNAIL": "img.category-page__member-thumbnail::attr(src)",
    "CATEGORY_URL": "a.category-page__member-link",
    "CATEGORY_NEXT_PAGE": "a.category-page__pagination-next::attr(href)",
    "CHARACTERS_FEATURE_FILMS": "div[data-source=films] div.pi-data-value > i > a::text",
    "CHARACTERS_SHORT_FILMS": "div[data-source=shorts] div.pi-data-value > i > a::text",
}

characters_string_skip_list = [
    "Disney characters",
    "Category:",
    "User blog:",
    "Disney Prince",
    "Disney Princess",
]
