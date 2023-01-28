from scrapy.crawler import CrawlerProcess

from scrapy_folder.authors import AuthorsSpider
from scrapy_folder.quotes import QuotesSpider


def start_crawler():
    process = CrawlerProcess()
    process.crawl(AuthorsSpider)
    process.crawl(QuotesSpider)
    process.start()


if __name__ == '__main__':
    start_crawler()
