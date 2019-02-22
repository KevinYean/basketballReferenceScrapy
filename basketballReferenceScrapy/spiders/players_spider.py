import scrapy
import re

#response.css('td[data-stat="player"]').getall() //Teams
#response.css('td[data-stat="player"] a::attr(href)').getall()


class QuotesSpider(scrapy.Spider):
    name = "player"
    DOWNLOAD_DELAY = 0.5
    currentseason = ""

    def start_requests(self):
        urls = [  # List of Urls to go through
            "https://www.basketball-reference.com/leagues/NBA_1989.html"
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
       # yield{
        #    'NBA Season': str(nbaSeason)
        #}
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
        #yield{
         #   'NBA Team': str(nbaTeam)
        #}
        if next_page is not None:
            for i in next_page:
                x = response.urljoin(i)
                yield scrapy.Request(x, callback=self.parsePlayer)

    def parsePlayer(self, response):
        #Player's Name
        playerName = response.css("h1::text").get()
        playerTeam = response.xpath(
            '//div[contains(@itemtype,"https://schema.org/Person")] //a[contains(@href,"teams")]')
        playerTeam = playerTeam.css('a::text').get() #not clean

        #Past Salary
        salary = response.css("div#all_all_salaries").getall()        # Get the comments sections which has information about salaries
        listsalary = re.findall(r'<tr >(.+?)</tr>', str(salary))        # Regular expression to split with <td></td> and creates list
        for i in listsalary[:-1]:
            # Regular expression to split with <tr></tr>
            seasonSalary = re.findall(r' >(.+?)</td', i)
            length = len(seasonSalary)
            #Regular expression to split with <td></td>
            season = re.findall(r'>(.+?)</th>', i)
            targetyear = "1988-89"
            if(str(season[0]) == targetyear):
                yield {
                    'Player':playerName,
                    'Team':playerTeam,
                    'Season': season[0],
                    'Salary': seasonSalary[length-1],
                }
        #Contract, current.
        contract = response.xpath('//div[contains(@id,"all_contracts")]').get()
        listContract = re.findall(r'class="">(.+?)</span>', str(contract))         # Regular expression to split with <td></td> and creates list
        #year = 2018
        #for i in listContract:
         #   if year == 2018: #Only this year
          #      yield {
           #         'Player': playerName,
            #        'Team': playerTeam,
             #       'Season': str(year) + "-" + str(year+1)[2:],
              #      'Salary': i,
               # }
            #year += 1
