import scrapy


class CombinedSpider(scrapy.Spider):
    name = "main"
    allowed_domains = ["birja-in.az"]
    start_urls = [
        "https://birja-in.az/elanlar/avto/",
        "https://birja-in.az/elanlar/ev-alqi-satqisi/",
        "https://birja-in.az/elanlar/elektronika/",
        "https://birja-in.az/elanlar/is-elanlari-xidmetler/",
        "https://birja-in.az/elanlar/ev-esyalari/",
        "https://birja-in.az/elanlar/Hobbi-ve-istirahet/",
        "https://birja-in.az/elanlar/Heyvanlar/",
        "https://birja-in.az/elanlar/muxtelif/"
    ]

    def parse(self, response):
        # Extract the current page's links
        links = response.css('.block_info_adv h2 a::attr(href)').getall()

        # Yield the links on the current page
        for link in links:
            yield response.follow(link, callback=self.parse_content, meta={"href": link})

        # Find the next page's URL
        next_page_span = response.css('.navigator_page_podcategory span.pageoff:contains("»")')
        if next_page_span:
            next_page = next_page_span.xpath('parent::a/@href').get()
            if next_page:
                # Follow the pagination link
                yield response.follow(next_page, callback=self.parse)

    def parse_content(self, response):
        yield {
            'link': response.request.meta['href'],
            'name': response.css('td.td_name_param_adder + td.name_adder::text').get(),
            'phone': response.css('td.td_name_param_phone + td::text').get(),
            'owner_cat': response.css('td.name_adder span::text').get(),
        }
