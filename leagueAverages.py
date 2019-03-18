import json 
 

#open the file
with open('2018-2019ShotDistribution.json') as f:
  data = json.load(f)
 
#reading file
#listOfYear = ["2000-01","2001-02","2002-03","2003-04","2004-05","2005-06","2006-07","2007-08","2008-09","2009-10","2010-11","2011-12","2012-13","2013-14","2014-15","2015-16","2016-17","2017-18","2018-19"]

def yearFind():

    year = "2018-19"
    #for year in listOfYear:
    totalShotAttempts = 0
    shot1 = 0
    shot2 = 0
    shot3 = 0
    shot4 = 0
    shot5 = 0
    totalShotMade = 0
    shot1M = 0
    shot2M = 0
    shot3M = 0
    shot4M = 0
    shot5M = 0
    numberOfPlayers = 0
    for emp in data:
      numberOfPlayers += 1
      totalShotAttempts += sum(emp['Shot Distribution Attempts'])
      shot1 += emp['Shot Distribution Attempts'][0]
      shot2 += emp['Shot Distribution Attempts'][1]
      shot3 += emp['Shot Distribution Attempts'][2]
      shot4 += emp['Shot Distribution Attempts'][3]
      shot5 += emp['Shot Distribution Attempts'][4]

      totalShotMade += sum(emp['Shot Distribution Made']) 
      shot1M += emp['Shot Distribution Made'][0]
      shot2M += emp['Shot Distribution Made'][1]
      shot3M += emp['Shot Distribution Made'][2]
      shot4M += emp['Shot Distribution Made'][3]
      shot5M += emp['Shot Distribution Made'][4]

      shotsAttempts = [shot1,shot2,shot3,shot4,shot5]
      shotAttemptsRatio = [round(shot1/totalShotAttempts,2),round(shot2/totalShotAttempts,2),round(shot3/totalShotAttempts,2),round(shot3/totalShotAttempts,2),round(shot4/totalShotAttempts,2),round(shot5/totalShotAttempts,2) ]
      shotMades = [shot1M,shot2M,shot3M,shot4M,shot5M]
      shotMadeRatio = [round(shot1M/totalShotMade,2),round(shot2M/totalShotMade,2),round(shot3M/totalShotMade,2),round(shot3M/totalShotMade,2),round(shot4M/totalShotMade,2),round(shot5M/totalShotMade,2) ]


    r = {"Year" : year, "TotalShotAttempts" : totalShotAttempts, "shotDistributionAttempts" : shotsAttempts, "shotAttemptsRatio" : shotAttemptsRatio, "TotalShotMade": totalShotMade, "shotDistributionMade" : shotMades, "shotMadeRatio":shotMadeRatio }
    with open('YearAverage.json', 'a') as f:
            json.dump(r, f)
        

yearFind()