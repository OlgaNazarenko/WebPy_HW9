import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field
from scrapy.utils.project import get_project_settings


class AuthorsItem(Item):
    fullname = Field()
    born_date = Field()
    born_location = Field()
    description = Field()


class AuthorsPipeline(object):
    def __init__(self):
        self.authors = []

    def process_items(self, item, spider):
        adapter = ItemAdapter(item)
        if 'fullname' in adapter.keys():
            self.authors.append({
                'fullname': adapter['fullname'],
                'born_date': adapter['born_date'],
                'born_location': adapter['born_location'],
                'description': adapter['description'],
            })
        return item

    # def close_spider(self, spider):
    #     with open(os.path.join('data', 'authors.json'), 'w', encoding='utf-8') as f:
    #         json.dump(self.authors, f, ensure_ascii=False)
    #


class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    custom_settings = {
        "FEED_FORMAT": 'json',
        "FEED_URI": 'data/authors.json',
        "FEED_EXPORT_ENCODING": 'utf-8',
        "REQUEST_FINGERPRINT_IMPLEMENTATION": '2.7',
        "ITEM_PIPELINES": {
            AuthorsPipeline: 300,
        }
    }
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for author in response.xpath("/html//div[@class='quote']"):
            yield response.follow(url=self.start_urls[0] + author.xpath('span/a/@href').get(), callback=self.parse_author)

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url = self.start_urls[0] + next_link)

    def parse_author(self, response):
        author = response.xpath("/html//div[@class='author-details']")
        fullname = author.xpath("h3[@class='author-title']/text()").get().strip()
        born_date = author.xpath("p/span[@class='author-born-date']/text()").get().strip()
        born_location = author.xpath("p/span[@class='author-born-location']/text()").get().strip()
        description = author.xpath("div[@class='author-description']/text()").get().strip()
        yield AuthorsItem(fullname=fullname, born_date=born_date, born_location=born_location, description=description)


# process = CrawlerProcess(settings=get_project_settings())
# process.crawl(AuthorsSpider)
# process.start()
# # if not reactor.running:
# #     process.crawl(AuthorsSpider)
# #     process.start()