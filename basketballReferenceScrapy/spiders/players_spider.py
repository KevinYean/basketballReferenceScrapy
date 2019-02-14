import scrapy
import re

#response.css('td[data-stat="player"]').getall() //Teams
#response.css('td[data-stat="player"] a::attr(href)').getall()

class QuotesSpider(scrapy.Spider):
    name = "player"
    DOWNLOAD_DELAY = 1

    def start_requests(self):
        urls = [ #List of Urls to go through
            "https://www.basketball-reference.com/teams/LAC/2019.html"
            #'https://www.basketball-reference.com/teams/PHI/2019.html',
            #"https://www.basketball-reference.com/players/e/embiijo01.html",
        ]
        for url in urls: #Run parse for each url in urls
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        urlString = str(response)

        #Player specific
        if "player" in urlString:
            #Player's Name
            playerName = response.css("h1::text").getall()
            yield{
            'Player': playerName
            }
            #Past Salary
            salary = response.css("div#all_all_salaries").getall() #Get the comments sections which has information about salaries
            listsalary = re.findall(r'<tr >(.+?)</tr>', str(salary)) #Regular expression to split with <td></td> and creates list
            for i in listsalary[:-1]:
                seasonSalary = re.findall(r' >(.+?)</td', i) #Regular expression to split with <tr></tr>
                length = len(seasonSalary)
                season = re.findall(r'>(.+?)</th>', i) #Regular expression to split with <td></td>
                yield {
                    'Season': season[0],
                    'Salary': seasonSalary[length-1],
                }
            #Contract, current.
            contract = response.xpath('//div[contains(@id,"all_contracts")]').get()
            listContract = re.findall(r'class="">(.+?)</span>', str(contract)) #Regular expression to split with <td></td> and creates list
            year = 2018
            for i in listContract:
                yield {
                    'Season': str(year) + "-" + str(year+1)[2:],
                    'Salary': i,
                }
                year+=1

            
        #Team Specific
        next_page = response.css('td[data-stat="player"] a::attr(href)').getall()
        if next_page is not None:
            for i in next_page:
                x = response.urljoin(i)
                yield scrapy.Request(x, callback=self.parse)