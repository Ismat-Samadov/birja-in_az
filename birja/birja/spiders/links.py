import scrapy


class LinksSpider(scrapy.Spider):
    name = "links"
    allowed_domains = ["birja-in.az"]
    start_urls = ["https://birja-in.az/elanlar/ev-alqi-satqisi/kiraye-evler/"]

    def parse(self, response):
        # Extract the current page's links
        links = response.css('.block_info_adv h2 a::attr(href)').getall()

        # Yield the links on the current page
        for link in links:
            yield {
                'href': link
            }

        # Find the next page's URL
        next_page_span = response.css('.navigator_page_podcategory span.pageoff:contains("»")')
        if next_page_span:
            next_page = next_page_span.xpath('parent::a/@href').get()
            if next_page:
                # Follow the pagination link
                yield response.follow(next_page, callback=self.parse)
