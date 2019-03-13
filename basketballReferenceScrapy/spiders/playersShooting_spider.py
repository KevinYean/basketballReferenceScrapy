import scrapy
import re


class QuotesSpider(scrapy.Spider):
    name = "playerShooting"
    download_delay = 0.5
    currentseason = ""

    def start_requests(self):
        urls = [  # List of Urls to go through
            "https://www.basketball-reference.com/teams/TOR/2019.html",
            "https://www.basketball-reference.com/teams/PHI/2019.html",
            "https://www.basketball-reference.com/teams/BOS/2019.html",
            "https://www.basketball-reference.com/teams/BRK/2019.html",
            "https://www.basketball-reference.com/teams/NYK/2019.html"
        ]
        for url in urls:  # Run parse for each url in urls
            yield scrapy.Request(url=url, callback=self.parseTeam)

    def parseLeague(self, response):
        #League Specific
        teams_page = response.css(
            'th[data-stat="team_name"] a::attr(href)').getall()
        nbaSeason = response.css(
            'h1 span::text').get()
        currentseason = str(nbaSeason)
        if teams_page is not None:
            for i in teams_page:
                x = response.urljoin(i)
                yield scrapy.Request(x, callback=self.parseTeam)
    
    def parseTeam(self,response):
        #Team Specific
        next_page = response.css(
            'td[data-stat="player"] a::attr(href)').getall()
        nbaTeam = response.css(
            'h1 span::text').getall()
        if next_page is not None:
            for i in next_page:
                x = response.urljoin(i)
                yield scrapy.Request(x, callback=self.parsePlayer)

    def parsePlayer(self, response):
        playerShootingSeasons = response.xpath('//li[contains(@class,"full hasmore")] //a[contains(@href,"shooting")]/@href').getall()
        for i in playerShootingSeasons:
            x = response.urljoin(i)
            yield scrapy.Request(x,callback=self.parseSeasonShooting)
            
            
    def parseSeasonShooting(self,response):
        year = response.css('h1::text').get()
        year = re.sub(r'[^0-9\-]','',year)
        player = response.xpath('//div[contains(@itemtype,"Person")]//strong//strong').get()
        player = re.findall(r'<strong>(.+?)</strong>', player)
        shootingDistanceAttempts = response.xpath('//tr//td[contains(@data-stat,"fga")]')[7:12]
        shootingDistanceAttempts = shootingDistanceAttempts.css('td::text').getall()
        yield{
            'Player': player[0],
            'Year': year,
            'Type': "Attempts",
            'At Rim' : shootingDistanceAttempts[0],
            '3 to <10 ft': shootingDistanceAttempts[1],
            '10 to <16 ft': shootingDistanceAttempts[2],
            '16ft to <3-pt': shootingDistanceAttempts[3],
            '3-pt': shootingDistanceAttempts[4]
        }
        shootingDistanceMade = response.xpath('//tr//td[@data-stat="fg"]')[7:12]
        shootingDistanceMade = shootingDistanceMade.css('td::text').getall()
        yield{
            'Player': player[0],
            'Year': year,
            'Type': "Made",
            'At Rim' : shootingDistanceMade[0],
            '3 to <10 ft': shootingDistanceMade[1],
            '10 to <16 ft': shootingDistanceMade[2],
            '16ft to <3-pt': shootingDistanceMade[3],
            '3-pt': shootingDistanceMade[4]
        }