
import traceback
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log
#from tutorial.tutorial.spiders.mls_spider import MLSSpider
from mlsscraper.mlsscraper.spiders.mls_spider import MLSSpider
from scrapy.utils.project import get_project_settings

class MLSScraperLauncher:
    
    def setup_crawler(self , domain, neighborhoodsCoords):
        spider = MLSSpider(domain=domain, neighborhoodsCoords=neighborhoodsCoords)
        settings = get_project_settings()
        crawler = Crawler(settings)
        crawler.configure()
        crawler.crawl(spider)
        crawler.start()
            
    def run_spiders(self, neighborhoodsCoords):
        for domain in ['themlsonline.com']:
            self.setup_crawler(domain, neighborhoodsCoords)
        log.start()
        reactor.run()

"""
if __name__ == '__main__':
    try:
        print "hi"
        run_spiders()
    except (KeyboardInterrupt, SystemExit, Exception) as e:
        print str(e)
        print traceback.format_exc()
"""

        
        