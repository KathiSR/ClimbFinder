# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Climb(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    protection = scrapy.Field()
    location = scrapy.Field()
    crag = scrapy.Field()
    grade = scrapy.Field()
    area = scrapy.Field()
    areaurl = scrapy.Field()
    region = scrapy.Field()
    average_rating = scrapy.Field()
    number_of_votes = scrapy.Field()
    climb_info = scrapy.Field() #this is a list of type, length and pitch - tease apart in later processing step)
    #climbtype = scrapy.Field() 
    #length = scrapy.Field()
    #pitches = scrapy.Field()