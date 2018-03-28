# -*- coding: utf-8 -*-
import scrapy


class ReciepesSpider(scrapy.Spider):
    name = 'recipes'
    allowed_domains = ['http://allrecipes.com/']
    start_urls = ['https://www.allrecipes.com/recipes/728/world-cuisine/latin-american/mexican/']

    def start_requests(self):
        start_page = 'https://www.allrecipes.com/recipes/728/world-cuisine/latin-american/mexican/?page=%s'
        pages = range(1,118)
        for page in pages:
            next_page = start_page % page
            yield scrapy.Request(next_page, dont_filter=True)


    def parse(self, response):
        recipes_urls = response.xpath('//*[@class="fixed-recipe-card"]/a/@href').extract()

        for url in recipes_urls:
            yield scrapy.Request(url, callback=self.scrape_recipe_page, dont_filter=True)

    def scrape_recipe_page(self, response):
        title = response.xpath('//h1/text()').extract()
        ingredients = response.xpath('//*[@class="recipe-ingred_txt added"]/text()').extract()
        directions = response.xpath('//*[@class="recipe-directions__list--item"]/text()').extract()
        rating = response.xpath('//*[@class="recipe-summary__stars"]/div/@data-ratingstars').extract()
        image_url = response.xpath('//*[@class="rec-photo"]/@src').extract_first()
        link = response.xpath('//*[@itemprop="url"]/@href').extract_first()


        yield {
            'title': title,
            'link': link,
            'image_url': image_url,
            'ingredients': ingredients,
            'directions': directions,
            'rating': rating
            }






