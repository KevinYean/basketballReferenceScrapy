import scrapy
import re


class QuotesSpider(scrapy.Spider):
    name = "playerShooting"
    download_delay = 0.5
    currentseason = ""

    def start_requests(self):
        urls = [  # List of Urls to go through
            "https://www.basketball-reference.com/players/l/lowryky01.html"
        ]
        for url in urls:  # Run parse for each url in urls
            yield scrapy.Request(url=url, callback=self.parsePlayer)

    def parsePlayer(self, response):
        playerShootingSeasons = response.xpath('//li[contains(@class,"full hasmore")] //a[contains(@href,"shooting")]/@href').getall()
        for i in playerShootingSeasons:
            x = response.urljoin(i)
            yield scrapy.Request(x,callback=self.parseSeasonShooting)
            
            
    def parseSeasonShooting(self,response):
        year = response.css('h1::text').get()
        year = re.sub(r'[^0-9\-]','',year)
        shootingDistance = response.xpath('//tr//td[contains(@data-stat,"fga")]')[8:13]
        shootingDistance = shootingDistance.css('td::text').getall()
        yield{
            'Player': "Kyle Lowry",
            'Year': year,
            'At Rim' : shootingDistance[0],
            '3 to <10 ft': shootingDistance[1],
            '10 to <16 ft': shootingDistance[2],
            '16ft to <3-pt': shootingDistance[3],
            '3-pt': shootingDistance[4]

        }
    
