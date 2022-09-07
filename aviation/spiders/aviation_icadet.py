from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from aviation.items import AviationItem

import re

class AviationScraper(CrawlSpider):
    name = "aviation_icadet"
    start_urls = [
        "https://icadet.com/flight-schools/united-kingdom/",
    ]

    rules = (
        #Rule(LinkExtractor(restrict_css=".pages > li > a"), follow=True),
        Rule(LinkExtractor(restrict_css="#page > div > div > div.page-content > div.schools-list > div > div > div.links > div > a.btn-main"), callback="parse_club"),
    )

    def parse_club(self, response):
        aviation_club = AviationItem()
        
        # Get type and country details from the referer url
        referer = response.request.headers.get('Referer').decode("utf-8")
        re_search_groups = re.search(r"^.*icadet\.com\/(helicopter-schools|flight-schools)\/(australia|united-kingdom|new-zealand)", referer)
        school_type = re_search_groups.group(1)
        country = re_search_groups.group(2)
        
        aviation_club["school_type"] = school_type
        aviation_club["country"] = country

        aviation_club["legal_name"] = response.css("#page > div > div > div.page-content > div > div.item.detail > div.text > h1::text").get().strip().encode("latin-1").decode("utf-8")
        aviation_club["address"] = response.css("#page > div > div > div.page-content > div > div.item.detail > div.text > div.place::text").get().strip().encode("latin-1").decode("utf-8")
        aviation_club["phone"] = response.css("#page > div > div > div.page-content > div > div.school-detail-info > div.col.info > div:nth-child(2) > div.data::text").get().strip().encode("latin-1").decode("utf-8")
        aviation_club["website"] = response.css("#page > div > div > div.page-content > div > div.school-detail-info > div.col.info > div:nth-child(1) > div.data > a::text").get().strip().encode("latin-1").decode("utf-8")
        encoded_email_1 = response.css("#page > div > div > div.page-content > div > div.school-detail-info > div.col.info > div:nth-child(2) > div.data > a > span::attr(data-cfemail)").get()
        encoded_email_2 = response.css("#page > div > div > div.page-content > div > div.school-detail-info > div.col.info > div:nth-child(3) > div.data > a > span::attr(data-cfemail)").get()
        encoded_email = encoded_email_1 or encoded_email_2
        aviation_club["email"] = self.cfDecodeEmail(encoded_email) if encoded_email else ""
        aviation_club["categories"] = ""
        aviation_club["courses"] = ""
        aviation_club["url"] = response.url
        aviation_club["referer"] = referer
        
        return aviation_club
    
    def cfDecodeEmail(self, encodedString):
        r = int(encodedString[:2],16)
        email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
        return email