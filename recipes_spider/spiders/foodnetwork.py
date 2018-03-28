# -*- coding: utf-8 -*-
import scrapy


class FoodnetworkSpider(scrapy.Spider):
    name = 'foodnetwork'
    allowed_domains = ['www.foodnetwork.com']
    start_urls = ['https://www.foodnetwork.com/search/italian-/p/1/CUSTOM_FACET:RECIPE_FACET']


    def start_requests(self):
        start_page = 'https://www.foodnetwork.com/search/italian-/p/%s/CUSTOM_FACET:RECIPE_FACET'
        pages = range(1,767)
        for page in pages:
            next_page = start_page % page
            yield scrapy.Request(next_page)

    def parse(self, response):
        recipes_urls = response.xpath('//*[@class="m-MediaBlock__a-Headline"]/a/@href').extract()

        for url in recipes_urls:
            full_url = "https:" + url
            yield scrapy.Request(full_url, callback = self.scrape_recipe_page)

    def scrape_recipe_page(self, response):

        title = response.xpath('//*[@class="o-AssetTitle__a-HeadlineText"]/text()').extract()
        #rating = response.xpath('//*[@class="gig-rating-stars "]/@title').extract()
        image_url = response.xpath('//*[@class="o-AssetMultiMedia__a-Image"]/@src').extract()
        ingredients = response.xpath('//*[@class="o-Ingredients__a-ListItem"]/input/@value').extract()
        directions = response.xpath('//*[@class="o-Method__m-Body"]/p/text()').extract()
        recipe_url = response.xpath('//*[@class="recipePage"]/@data-shorten-url').extract()
        total_time = response.xpath('//*[@class="o-RecipeInfo__a-Description--Total"]/text()').extract_first()
        serving_size = response.xpath('//*[@class="o-RecipeInfo__a-Description"]/text()').extract()[-2]
        difficulty = response.xpath('//*[@class="o-RecipeInfo__a-Description"]/text()').extract()[-1]
        category_list = response.xpath('//*[@class="o-Capsule__a-Tag a-Tag"]/text()').extract()
        author = response.xpath('//*[@class="o-Attribution__a-Name"]/a/text()').extract_first()

        yield {
        'title': title,
        #'rating': rating, #need to fix
        'directions': directions,
        'recipe_url': recipe_url,
        'image_url': image_url,
        'ingredients': ingredients,
        'total_time': total_time,
        'serving_size': serving_size,
        'difficulty':difficulty,
        'category_list': category_list,
        'author': author
        }
