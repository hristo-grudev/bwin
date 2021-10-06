# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BwinItem(scrapy.Item):
    site = scrapy.Field()
    sport = scrapy.Field()
    date = scrapy.Field()
    participant1 = scrapy.Field()
    participant2 = scrapy.Field()
    coeff1 = scrapy.Field()
    coeffX = scrapy.Field()
    coeff2 = scrapy.Field()
