import json 
 

#open the file
with open('March152019.json') as f:
  data = json.load(f)
 
#reading file
listOfYear = ["2000-01","2001-02","2002-03","2004-05","2005-06","2006-07","2007-08","2008-09","2009-10","2010-11","2011-12","2012-13","2013-14","2014-15","2015-16","2016-17","2017-18","2018-19"]

def yearFind():
    for year in listOfYear:
        print(year)
        totalShotAttempts = 0
        shot1 = 0
        shot2 = 0
        shot3 = 0
        shot4 = 0
        shot5 = 0
        numberOfPlayers = 0


        for emp in data:
            if(emp['Year'] == year):
                numberOfPlayers += 1
                totalShotAttempts += sum(emp['Shot Distribution Attempts'])
                shot1 += emp['Shot Distribution Attempts'][0]
                shot2 += emp['Shot Distribution Attempts'][1]
                shot3 += emp['Shot Distribution Attempts'][2]
                shot4 += emp['Shot Distribution Attempts'][3]
                shot5 += emp['Shot Distribution Attempts'][4]
        r = {"Year" : year, "TotalShotAttempts" : totalShotAttempts, "shot1Average" : round(shot1/totalShotAttempts,2), 
        "shot2Average" : round(shot2/totalShotAttempts,2), "shot3Average" : round(shot3/totalShotAttempts,2)
        , "shot4Average" : round(shot4/totalShotAttempts,2), "shot5Average" : round(shot5/totalShotAttempts,2) }
        with open('test.json', 'a') as f:
            json.dump(r, f)
        

yearFind()