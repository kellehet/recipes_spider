# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from time import sleep


class YumSpider(scrapy.Spider):
    name = 'yum'
    allowed_domains = ['https://www.yummly.com']
    start_urls = ['https://www.yummly.com/recipes?q=indian']

    def start_requests(self):
        url = 'https://www.yummly.com/recipes?q=indian'
        start_page = 'https://www.yummly.com'
        self.driver = webdriver.Chrome('/Users/megboudreau/Desktop/chromedriver')
        self.driver.get(url)

        sel = Selector(text=self.driver.page_source)
        page = sel.xpath('//*[@class="recipe-card single-recipe visible"]/a/@href').extract()
        for link in page:
            next_page = start_page + link
            yield scrapy.Request(next_page, callback=self.parse_recipe, dont_filter=True)

    def parse_recipe(self, response):
        self.driver = webdriver.Chrome('/Users/megboudreau/Desktop/chromedriver')
        url =response.request.url
        self.driver.get(url)
        sleep(3)
        sel = Selector(text=self.driver.page_source)

        title = sel.xpath('//*[@class="primary-info-text"]/h1/text()').extract_first()
        rating = sel.xpath('//*[@class="full-star"]/@data-tip').extract_first()  #Outstanding- 5 Stars, Really Good 4.5 stars, Just Good 3 Stars,
        number_ingredients =  sel.xpath('//*[@class="recipe-summary-item "]/span/text()').extract()[0]
        cook_time = sel.xpath('//*[@class="recipe-summary-item "]/span/text()').extract()[1]
        calories = sel.xpath('//*[@class="recipe-summary-item nutrition"]/span/text()').extract_first()
        sodium = sel.xpath('//*[@class="raw-value"]/text()').extract()[0]
        fat = sel.xpath('//*[@class="raw-value"]/text()').extract()[1]
        protein = sel.xpath('//*[@class="raw-value"]/text()').extract()[2]
        carbs = sel.xpath('//*[@class="raw-value"]/text()').extract()[3]
        fibre = sel.xpath('//*[@class="raw-value"]/text()').extract()[4]
        dirctions_url = sel.xpath('//*[@class="recipe-show-full-directions btn-inline"]/@href').extract_first()
        ing_sel = sel.xpath('//*[@class="IngredientLine"]').extract()

        ing_list=[]
        for s in ing_sel:
            if s.find("numerator") !=-1:
                if s.find('</span> </span><span class="numerator"')!=-1:
                    startIndex=s[29:].find('e">')+44
                    endIndex = s[startIndex:].find("</")+startIndex
                    wholeNum = s[startIndex:endIndex]
                    i=s.find("numerator")+11
                    numerator = s[i]
                    i=s.find("solidus")+9
                    solidus=s[i]
                    i=s.find("denominator")+13
                    denominator=s[i]
                    amount= wholeNum + " " + numerator + solidus + denominator
                else:
                    i=s[29:].find('e">')+56
                    numerator = s[i]
                    i=s.find("solidus")+9
                    solidus=s[i]
                    i=s.find("denominator")+13
                    denominator=s[i]
                    amount=numerator+solidus+denominator
            else:
                if s.find("amount")!=-1:
                    startIndex=s[29:].find('e">')+38
                    endIndex = s[startIndex:].find("</")+startIndex
                    amount = s[startIndex:endIndex]
                else:
                    amount = ""
            unit = ""
            if s.find("unit")!=-1:
                startIndex =s.find("unit")+6
                endIndex = s[startIndex:].find("</")+startIndex
                unit = s[startIndex:endIndex]
            startIndex = s.find("ingredient")+12
            endIndex = s[startIndex:].find("</")+startIndex
            ingredient = s[startIndex:endIndex]
            item = amount + " " + unit + " " + ingredient
            ing_list.append(item)

        yield {
            'title': title,
            'rating': rating,
            'number_ingredients': number_ingredients,
            'cook_time': cook_time,
            'calories': calories,
            'sodium': sodium,
            'fat': fat,
            'protein': protein,
            'carbs': carbs,
            'fibre': fibre,
            'directions_url':dirctions_url,
            'ingredient_list': ing_list
            }







