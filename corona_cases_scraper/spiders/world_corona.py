# -*- coding: utf-8 -*-
import scrapy


xpaths = {
    "coronavirus_cases" : {
        "url":"https://www.worldometers.info/coronavirus/",
        "table_xpath":"//*[@id=\"main_table_countries_today\"]//tbody/tr",
        "value_xpath":"td[2]//text()",
        "country_xpath":"td[1]/a//text()"
    }
}

'''
# If you also want population of each contries just put this dictionary in xpaths
"population" : {
        "url":"https://www.worldometers.info/world-population/population-by-country/",
        "table_xpath":"//*[@id=\"example2\"]//tbody/tr",
        "value_xpath":"td[3]//text()",
        "country_xpath":"td[2]//text()"
    }

'''

class WorldCoronaSpider(scrapy.Spider):
    name = "world_corona"
    def start_requests(self):
        for attribute in xpaths:       
            yield scrapy.Request(url=xpaths.get(attribute).get("url"),callback=self.parse, meta = {"attribute":attribute})
    
    def parse(self, response):
        attribute = response.meta.get('attribute')
        for row in response.xpath(xpaths.get(attribute).get("table_xpath")):
            country = row.xpath(xpaths.get(attribute).get("country_xpath")).get()
            '''
            if country == ' ' and attribute == 'coronavirus_cases':
                country = row.xpath("td[1]/a//text()").get()
            if country == None and attribute == 'coronavirus_cases':
                country = row.xpath("td[1]/span//text()").get()
            '''
            if country == None:
                continue
            yield {
                'country':country.strip(),
                'attribute':attribute,
                'value':row.xpath(xpaths.get(attribute).get("value_xpath")).get(),
            }
        