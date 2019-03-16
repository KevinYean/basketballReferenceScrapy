import scrapy
import re


class QuotesSpider(scrapy.Spider):
    name = "playerShooting"
    download_delay = 0.5
    currentseason = ""

    def start_requests(self):
        urls = [  # List of Urls to go through
           "https://www.basketball-reference.com/leagues/NBA_2019.html" 
           #"https://www.basketball-reference.com/players/l/lowryky01/shooting/2019"
           #"https://www.basketball-reference.com/players/l/lowryky01.html"
           #"https://www.basketball-reference.com/players/i/ingraan01/shooting/2018"
           #"https://www.basketball-reference.com/players/b/bertada02/shooting/2019"
        ]
        for url in urls:  # Run parse for each url in urls
            yield scrapy.Request(url=url, callback=self.parseLeague)

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
        player = response.xpath('//h1//text()').get() #Name
        playerArray = player.split()
        shootingDistanceAttemptsArray = [0,0,0,0,0]
        shootingDistanceMadeArray = [0,0,0,0,0]
        
        if response.xpath('//tr//td[a[contains(text(),"Rim")]]'):
            shootingDistanceAttemptsArray[0] = int(response.xpath('//tr//td[a[contains(text(),"Rim")]]/following-sibling::td[2]//text()').get())
            shootingDistanceMadeArray[0] = int(response.xpath('//tr//td[a[contains(text(),"Rim")]]/following-sibling::td[1]//text()').get())

        if response.xpath('//tr//td[a[contains(text(),"<10 ft")]]'):
            shootingDistanceAttemptsArray[1] = int(response.xpath('//tr//td[a[contains(text(),"<10 ft")]]/following-sibling::td[2]//text()').get())
            shootingDistanceMadeArray[1] = int(response.xpath('//tr//td[a[contains(text(),"<10 ft")]]/following-sibling::td[1]//text()').get())

        if response.xpath('//tr//td[a[contains(text(),"<16 ft")]]'):
            shootingDistanceAttemptsArray[2] = int(response.xpath('//tr//td[a[contains(text(),"<16 ft")]]/following-sibling::td[2]//text()').get())
            shootingDistanceMadeArray[2] = int(response.xpath('//tr//td[a[contains(text(),"<16 ft")]]/following-sibling::td[1]//text()').get())

        if response.xpath('//tr//td[a[contains(text(),"<3-pt")]]'):
            shootingDistanceAttemptsArray[3] = int(response.xpath('//tr//td[a[contains(text(),"<3-pt")]]/following-sibling::td[2]//text()').get())
            shootingDistanceMadeArray[3] = int(response.xpath('//tr//td[a[contains(text(),"<3-pt")]]/following-sibling::td[1]//text()').get())

        if response.xpath('//tr//td[a[text()="3-pt"]]'):
            shootingDistanceAttemptsArray[4] = int(response.xpath('//tr//td[a[text()="3-pt"]]/following-sibling::td[2]//text()').get())
            shootingDistanceMadeArray[4] = int(response.xpath('//tr//td[a[text()="3-pt"]]/following-sibling::td[1]//text()').get())

        yield{
            'Player': ' '.join(playerArray[:-2]),
            'Year': year,
            'Shot Distribution Attempts' : shootingDistanceAttemptsArray,
            'Shot Distribution Made' : shootingDistanceMadeArray
        }

        #response.xpath('//td').getall()
        #response.xpath('//td//a[contains(text(),"3 to <10")]//text()').get() Find the one