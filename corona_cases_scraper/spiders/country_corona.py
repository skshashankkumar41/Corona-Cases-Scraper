# -*- coding: utf-8 -*-
import scrapy


xpaths = {
    "coronavirus_cases" : {
        "url":"https://www.grainmart.in/news/coronavirus-covd-19-live-cases-tracker-john-hopkins/",
        "table_xpath":"//*[@id=\"post-3287\"]/div/figure/table//tbody/tr",
        "value_xpath":"td[2]//text()",
        "state_xpath":"td[1]//text()"
    }
   
}

"""
# If you also want population of each state just put this dictionary in xpaths
"population" : {
        "url":"https://www.careerpower.in/largest-state-india.html",
        "table_xpath":"//*[@id=\"middle\"]/table[3]//tbody/tr",
        "value_xpath":"td[3]//text()",
        "state_xpath":"td[2]//text()"
    }
"""


class CountryCoronaSpider(scrapy.Spider):
    name = "country_corona"
    def start_requests(self):
        for attribute in xpaths:       
            yield scrapy.Request(url=xpaths.get(attribute).get("url"),callback=self.parse, meta = {"attribute":attribute})
    
    def parse(self, response):
        attribute = response.meta.get('attribute')
        for row in response.xpath(xpaths.get(attribute).get("table_xpath")):
            state = row.xpath(xpaths.get(attribute).get("state_xpath")).get()
            
            if state == 'CORONAVIRUS COVID-19 ' or state == 'State Wise Breakdown' or state == None:
                continue
            

            yield {
                'country': 'India',
                'state':state.strip(),
                'attribute':attribute,
                'value':row.xpath(xpaths.get(attribute).get("value_xpath")).get(),
            }
        