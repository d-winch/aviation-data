from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from aviation.items import AviationItem

import re

class AviationScraper(CrawlSpider):
    name = "aviation_bestaviation"
    start_urls = [
        "https://www.bestaviation.net/flight_school/united-kingdom/",
        "https://www.bestaviation.net/flight_school/australia/",
        "https://www.bestaviation.net/flight_school/new-zealand/",
        "https://www.bestaviation.net/helicopter_schools/united-kingdom/",
        "https://www.bestaviation.net/helicopter_schools/new-zealand/",
        "https://www.bestaviation.net/helicopter_schools/australia/",
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=".pages > li > a"), follow=True),
        Rule(LinkExtractor(restrict_css=".sl-grid-list > .sl-list > li > a"), callback="parse_club")
    )

    def parse_club(self, response):
        aviation_club = AviationItem()
        
        if "ref=ad" in response.url:
            return
        
        # Get type and country details from the referer url
        referer = response.request.headers.get('Referer').decode("utf-8")
        re_search_groups = re.search(r"^.*bestaviation\.net\/(helicopter_schools|flight_school)\/(australia|united-kingdom|new-zealand)", referer)
        school_type = re_search_groups.group(1)
        country = re_search_groups.group(2)
        
        aviation_club["school_type"] = school_type
        aviation_club["country"] = country

        aviation_club["legal_name"] = response.css("body > main > div.sp-head > div > h1::text").get().strip()
        aviation_club["address"] = "\n".join(response.css("body > main > div.sp-grid > div.sp-grid-side > div.sp-box.sp-contact > p > span::text").getall()).strip()
        aviation_club["phone"] = response.css("body > main > div.sp-grid > div.sp-grid-side > div.sp-box.sp-contact > ul > li:nth-child(1) > a::text").get().strip()
        aviation_club["website"] = response.css("body > main > div.sp-grid > div.sp-grid-side > div.sp-box.sp-contact > ul > li:nth-child(2) > a::attr(href)").get().strip()
        aviation_club["email"] = ""
        aviation_club["categories"] = ", ".join(response.css("body > main > div.sp-grid > div.sp-grid-main > section:nth-child(3) > ul:nth-child(3) > li::text").getall())
        aviation_club["courses"] = ", ".join(response.css("body > main > div.sp-grid > div.sp-grid-main > section:nth-child(3) > ul:nth-child(5) > li:nth-child(1)::text").getall())
        aviation_club["url"] = response.url
        aviation_club["referer"] = referer
        
        return aviation_club