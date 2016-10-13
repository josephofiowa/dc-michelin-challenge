
# coding: utf-8

# In[ ]:


# #https://doc.scrapy.org/en/1.2/
#ingridFitzgerald

import scrapy
from scrapy import Request

class YelpSpiderDC(scrapy.Spider):
    name = 'yelpspiderdc'
    start_urls = ['https://www.yelp.ca/search?find_loc=Washington,+DC,+United+States&start=0&cflt=restaurants&attrs=RestaurantsPriceRange2.4,RestaurantsPriceRange2.3']

    def parse(self, response):
        urls = response.xpath('//*[@id="super-container"]/div/div[2]/div[1]/div/div[4]/ul[2]/li/div/div[1]/div[1]/div/div[2]/h3/span/a/@href').extract()
        for url in urls:
            yield scrapy.Request(response.urljoin(url), callback=self.parse_contents)

        next_page = response.xpath('//*[@id="super-container"]/div/div[2]/div[1]/div/div[4]/div/div/div/div[2]/div/div[last()]/a/@href')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)

    def parse_contents(self, response):
        name = ' '.join(
            response.xpath('//*[@id="wrap"]/div[3]/div/div[1]/div/div[2]/div[1]/div[1]/h1/text()').extract()).strip(
            '\n')

        reviews_sections = response.xpath('//*[@id="super-container"]/div[1]/div/div[1]/div[4]/div[1]/div[2]/ul/li')
          

        # from scrapy.shell import inspect_response  
        # inspect_response(response, self)

        for sel in reviews_sections:

            reviews_user = sel.xpath('div/div[1]/div/div/div[2]/ul[1]/li[1]/a/text()').extract()
            reviews_user_url = sel.xpath('div/div[1]/div/div/div[2]/ul[1]/li[1]/a/@href').extract()
            reviews_date = sel.xpath('div/div[2]/div[1]/div/span/meta/@content').extract()
            reviews_stars = sel.xpath('div/div[2]/div[1]/div/div/div/meta/@content').extract()
            reviews_contents = sel.xpath('div/div[2]/div[1]/p/text()').extract()

            yield {'name': name,
                   'reviews_user': reviews_user,
                   'reviews_user_url': 'https://www.yelp.ca/dc' + ''.join(reviews_user_url),
                   'reviews_date': reviews_date,
                   'reviews_stars': reviews_stars,
                   'reviews_contents': reviews_contents,
                   'restaurant_url': response.url
                   }


        review_next_page = response.xpath('//*[@id="super-container"]/div[1]/div/div[1]/div[4]/div[1]/div[3]/div/div/div[2]/div/div[last()]/a/@href')
        if review_next_page:
            url = response.urljoin(review_next_page[0].extract())
            yield scrapy.Request(url, self.parse_contents)
            
            
#yield=will give the .txt

