from scrapy.http.response import Response
import scrapy


class UaHotels(scrapy.Spider):
    name = 'uahotels'
    allowed_domains = ['uahotels.info']
    start_urls = ['https://uahotels.info/']

    def parse(self, response: Response):
        all_images = response.xpath("//img/@src[starts-with(., 'https')]")
        yield {'url': response.url, 'payload': [{'type': 'image', 'data': image.get()} for image in all_images]}
        if response.url == self.start_urls[0]:
            all_links = response.xpath("//a/@href[starts-with(., 'https://uahotels.info/')]")
            selected_links = [link.get() for link in all_links][:19]
            for link in selected_links:
                yield scrapy.Request(link, self.parse)


class Zvetsad(scrapy.Spider):
    name = 'zvetsad'
    allowed_domains = ['www.zvetsad.com.ua']
    start_urls = ['https://www.zvetsad.com.ua/catalog/rozyi']

    def parse(self, response: Response):
        products = response.xpath("//div[contains(@class, 'item_div')]")[:20]
        for files in range(20):
            yield {
                'description': products.xpath("//div[contains(@class, 'item_nazvanie')]/a/text()").extract()[files],
                'price': products.xpath("//div[contains(@class, 'price fl')]/text()").extract()[files],
                'img': products.xpath("//img/@src").extract()[files],
            }