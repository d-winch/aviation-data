# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AviationItem(scrapy.Item):

    
    legal_name = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    website = scrapy.Field()
    email = scrapy.Field()
    categories = scrapy.Field()
    courses = scrapy.Field()
    url = scrapy.Field()
    country = scrapy.Field()
    school_type = scrapy.Field()
    referer = scrapy.Field()
    