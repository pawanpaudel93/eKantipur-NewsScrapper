# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from datetime import datetime, timedelta
from scrapy.exceptions import CloseSpider
from NepaliNewsScrapper.items import NepalinewsscrapperItem


class EkantipurSpider(Spider):
    name = 'eKantipur'

    def __init__(self, start=None, stop=None, **kwargs):
        super().__init__(**kwargs)
        self.stop = stop
        self.start = start
        self.start_urls = ['https://ekantipur.com']
        self.allowed_domains = ['ekantipur.com']

    def parse(self, response):
        if not response.xpath('//*[@class="logo "]/a/img/@src').extract_first():
            yield Request(url=response.url, dont_filter=True)

        categories = [
            'https://ekantipur.com/business',
            'https://ekantipur.com/sports',
            'https://ekantipur.com/diaspora',
            'https://ekantipur.com/entertainment',
            'https://ekantipur.com/national',
            'https://ekantipur.com/world',
            'https://ekantipur.com/literature',
            'https://ekantipur.com/technology',
            'https://ekantipur.com/feature'
        ]
        for category in categories:
            yield Request(category, callback=self.parse_cat)

    def parse_cat(self, response):
        if not response.xpath('//*[@class="logo "]/a/img/@src').extract_first():
            yield Request(url=response.url, dont_filter=True)

        today = datetime.strptime(self.start, '%Y/%m/%d')
        edate = today.strftime('%Y/%m/%d')
        cat_nep = response.xpath('//*[@class="catName"]/text()').extract_first()
        page_url = response.url + '/' + edate
        yield Request(page_url,
                      callback=self.parse_pages,
                      meta={
                          'today': today
                      })

    def parse_pages(self, response):
        if not response.xpath('//*[@class="logo "]/a/img/@src').extract_first():
            yield Request(url=response.url, dont_filter=True)
        today = response.meta['today']
        if today.strftime('%Y/%m/%d') > self.stop:
            raise CloseSpider('termination condition met')
        else:
            news_urls = response.xpath('//*[@class="teaser offset"]/h2/a/@href').extract()
            for url in news_urls:
                yield Request(response.urljoin(url),
                              callback=self.parse_page)
            today = today + timedelta(days=1)
            edate = today.strftime('%Y/%m/%d')
            next_page = response.url[:-10] + edate
            yield Request(next_page,
                          meta={
                              'today': today
                          }, callback=self.parse_pages)

    def parse_page(self, response):
        if not response.xpath('//*[@class="logo "]/a/img/@src').extract_first():
            yield Request(url=response.url, dont_filter=True)
        article_title = response.xpath('//*[@class="article-header"]/h1/text()').extract_first()
        article_description = '\n'.join(response.xpath('//p/text()').extract())
        news = NepalinewsscrapperItem()
        news['category'] = response.xpath('//*[@class="cat_name"]/a/text()').extract_first()
        news['title'] = article_title
        news['description'] = article_description
        yield news
