import scrapy
from ..items import ScrapyArticlesItem
import re


class ArticleSpider(scrapy.Spider):
    name = "arcticle_spider"

    start_urls = [
        'https://habrahabr.ru/users/stannislav/posts/',
    ]

    def parse(self, response):
        for href in response.css('h2.post__title a::attr(href)'):
            yield response.follow(href, self.parse_article)

        for href in response.css('li.toggle-menu__item.toggle-menu__item_pagination a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_article(self, response):
        def extract_with_css(query):
            result = response.css(query).extract_first().strip()
            res = re.sub(r'<.*?>', '', result)
            return res

        item = ScrapyArticlesItem()
        item['name'] = extract_with_css('h1.post__title.post__title_full span::text')
        item['article'] = extract_with_css('div.post__text.post__text-html.js-mediator-article')
        yield item
