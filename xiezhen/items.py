# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import random

COLORS = [
"bg-cat-1",
"bg-cat-4",
"bg-danger",
"bg-cat-2",
"bg-primary",
"bg-info",
"bg-success",
"bg-warning",
"bg-cat-3",
"bg-cat-5",
"bg-secondary",
"bg-dark"
]

class XiezhenItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    post_instant = scrapy.Field()
    post_desc = scrapy.Field()
    post_title = scrapy.Field()
    post_slug = scrapy.Field()
    post_media = scrapy.Field()
    post_video = scrapy.Field()
    video_url = scrapy.Field()
    media_alt = scrapy.Field()
    origin_link = scrapy.Field()
    origin_created_at = scrapy.Field()
    images = scrapy.Field()
    category_id = scrapy.Field()
    post_type= scrapy.Field()

class CategoryItem(scrapy.Item):

    title = scrapy.Field()
    name = scrapy.Field()

    def get_color(self):
        return random.choice(COLORS)
