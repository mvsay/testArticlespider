# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JobBoleArticleItem(scrapy.Item):
    url=scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url=scrapy.Field()
    front_image_path = scrapy.Field()
    title_css = scrapy.Field()
    create_date_css = scrapy.Field()
    praise_number_css = scrapy.Field()
    fav_nums_css = scrapy.Field()
    comment_nums_css = scrapy.Field()
    content_css = scrapy.Field()
    tag_list = scrapy.Field()
