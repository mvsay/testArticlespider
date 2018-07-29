# -*- coding: utf-8 -*-
import re
import urllib

import scrapy
from scrapy.http  import Request
from articlespider.items import JobBoleArticleItem

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        #获取文章列表页的文章url并交给scrapy，下载后进行解析
        #获取下一页的Url并交给scrapy进行下载，下载完成后交给parse

        # post_urls=response.css("#archive div.floated-thumb div.post-thumb a::attr(href)").extract()
        # for post_url in post_urls:
        #     post_url=urllib.parse.urljoin(response.url, post_url)
        #     yield Request(url=post_url,callback=self.parse_detail)

        post_nodes=response.css("#archive div.floated-thumb div.post-thumb a")
        for post_node in post_nodes:
            image_url = urllib.parse.urljoin(response.url, post_node.css("img::attr(src)").extract_first(""))
            post_url=urllib.parse.urljoin(response.url, post_nodes.css("::attr(href)").extract_first(""))
            yield Request(url=post_url,callback=self.parse_detail,meta={"front_image_url":image_url})

         #提取下一页
        next_urls=response.css(".next.page-numbers::attr(href)").extract_first()
        if next_urls:
            next_urls = urllib.parse.urljoin(response.url, next_urls)
            yield Request(url=next_urls, callback=self.parse)

    def parse_detail(self,response):
        '''使用xpath获取页面内容
        #//*[@id="post-113493"]/div[1]/h1
        #xpath 返回一个selector,再通过extract()方法，可以得到str的数组
        re_selector=response.xpath("//div[@class='entry-header']/h1/text()")
        title=re_selector.extract()[0]
        create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract_first().strip().replace('·','').strip()
        #获取点赞数
        praise_number=int(response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract_first())
        #获取收藏数
        fav_nums=response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract_first()
        match_re = re.match(r'.*(\d+).*', fav_nums)
        if match_re:
            fav_nums=int(match_re.group(1))
        else:
            fav_nums = 0
        #获取评论数
        comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        match_re = re.match(r'.*?(\d+).*', comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums=0
        #内容
        content=response.xpath("//div[@class='entry']").extract()[0]

        tags = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()

        tag_list=[element for element in tags if not element.strip().endswith('评论')]
        tag_list=",".join(tag_list)
        '''

        article= JobBoleArticleItem()

        #取文章封面图，通过meta方式传参进来的
        front_image_url=response.meta.get("front_image_url","")

        #通过CSS选择器提取字段=============================
        title_css = response.css(".entry-header h1::text").extract_first()
        create_date_css = response.css("p.entry-meta-hide-on-mobile ::text").extract()[0].strip().replace('·','').strip()

        # 获取点赞数
        praise_number_css = int(response.css(".vote-post-up h10::text").extract()[0])
        # 获取收藏数
        fav_nums_css = response.css(".bookmark-btn::text").extract()[0]
        match_re = re.match(r'.*(\d+).*', fav_nums_css)
        if match_re:
            fav_nums_css = int(match_re.group(1))
        else:
            fav_nums_css = 0
        # 获取评论数
        comment_nums_css = response.css("a[href='#article-comment'] span::text").extract_first()
        match_re = re.match(r'.*?(\d+).*', comment_nums_css)
        if match_re:
            comment_nums_css =int( match_re.group(1))
        else:
            comment_nums_css = 0
        # 内容
        content_css = response.css("div.entry").extract()[0]

        tags_css = response.css("p.entry-meta-hide-on-mobile a::text").extract()

        tag_list = [element for element in tags_css if not element.strip().endswith('评论')]
        tag_list = ",".join(tag_list)

        article["title_css"]=title_css
        article["front_image_url"] = [front_image_url]
        article["create_date_css"] = create_date_css
        article["praise_number_css"] = praise_number_css
        article["fav_nums_css"] = fav_nums_css
        article["comment_nums_css"] = comment_nums_css
        article["content_css"] = content_css
        article["tag_list"] = tag_list
        article["url"] = response.url
        # article["title_css"] = title_css
        # article["title_css"] = title_css
        yield article

