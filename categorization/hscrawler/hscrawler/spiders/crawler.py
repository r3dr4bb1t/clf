import scrapy
import time
import csv
import datetime
    
class Item(scrapy.Item):
    date = scrapy.Field() 
    name = scrapy.Field()
    company = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    pass

items = Item()

def count():
    count.counter;
    count.date ;
   
class hsSpider(scrapy.Spider):
    name = "hsSpider"
    start_urls = ['http://hsmoa.com']
    strdate=''
    count.counter=30;
    count.date = datetime.datetime.now()

    def parse(self, response):

        strdate = count.date.strftime('%Y%m%d')
        items['date'] = strdate
        items['price'] = response.xpath("//*/div/div/a/div/div//span[@class=' strong font-17 c-black']/text()|//*/div/div/a/div/div//span[@class='strong font-17 c-black']/text()").extract()
        items['name'] = response.xpath("//*/div/div/a/div/div//div[@class='font-15']/text()").extract()
        items['url'] = response.xpath('//*/div/div/a[@class="disblock"]/@href').extract()

        temp = []
        for i in response.xpath("//*/div//div[contains(@class, 'timeline-item')]").extract():
            temp.append(i.split()[2])
        items['company'] = temp;

        for item in zip(items['company'],items['name'],items['url'],items['price']):
            scraped_info = {
                'date' : items['date'],
                'company' : item[0].strip(),
                'name' : item[1].strip(),
                'url' : item[2].strip(),
                'price': item[3].strip().strip('원').strip(',')
            }
            yield scraped_info
        
        count.counter-=1;
        count.date -= datetime.timedelta(days=1)
        strdate = count.date.strftime('%Y%m%d')
        next_page = 'http://hsmoa.com/?date='+strdate+'&site=&cate='

        if count.counter is not 0:
            yield scrapy.Request(next_page, dont_filter=True)
