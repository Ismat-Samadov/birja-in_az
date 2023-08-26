import scrapy


class ContentSpider(scrapy.Spider):
    name = "content"
    allowed_domains = ["birja-in.az"]
    start_urls = ["https://birja-in.az/Telebe-qizlara-kiraye-ev-adv239837.html"]

    def parse(self, response):
        yield {
            'name': response.css('td.td_name_param_adder + td.name_adder::text').get(),
            'phone': response.css('td.td_name_param_phone + td::text').get(),
            'owner_cat': response.css('td.name_adder span::text').get(),
        }
