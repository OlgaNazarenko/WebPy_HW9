import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field


class QuotesItem(Item):
    author = Field()
    quote = Field()
    tags = Field()


class QuotesPipeline(object):
    def __init__(self):
        self.quotes = []

    def process_items(self, item, spider):
        adapter = ItemAdapter(item)
        if 'author' in adapter.keys():
            self.quotes.append({
                'author': adapter['author'],
                'quote': adapter['quote'],
                'tags': adapter['tags']
            })
            return item

    # def close_spider(self, spider):
    #     with open(os.path.join('data', 'quotes.json'), 'w', encoding='utf-8') as f:
    #         json.dump(self.quotes, f, ensure_ascii=False)


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    custom_settings = {
        "FEED_FORMAT": 'json',
        "FEED_URI": 'data/quotes.json',
        "FEED_EXPORT_ENCODING": 'utf-8',
        "REQUEST_FINGERPRINT_IMPLEMENTATION": '2.7',
        "ITEM_PIPELINES": {
            QuotesPipeline: 300,
        }
    }
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']") :
            yield {
                "tags": quote.xpath("div[@class='tags']/a/text()").getall(),
                "author": quote.xpath("span/small/text()").get(),
                "quote": quote.xpath("span[@class='text']/text()").get()
            }
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url = self.start_urls[0] + next_link)


# process = CrawlerProcess()
# process.crawl(QuotesSpider)
# process.start()
