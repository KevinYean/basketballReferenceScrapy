import json
from json import loads, dumps
from collections import defaultdict
import os

filename = '1984-85' #Need to change year for each file. //Automate it if necesary.
os.mkdir(filename) #Create directory

with open(filename + '.json', 'r') as f:
    nbaSeason = json.load(f)

allTeam = {}

#Goes through the entire list of JSONs
for players in nbaSeason:
    #For each new team add it to the list of teams
    teamName = players["Team"]
    if(teamName not in allTeam):
        allTeam[teamName] = [] #Add empty team
    allTeam[teamName].append(players) #Add team to appropriate list

for team in allTeam: #Split all the teams into theire seperate files accordingly
    teamName = str(team) + filename
    file = open(filename+"/"+teamName.replace(' ','')+" .json","w") 
    file.write((json.dumps(allTeam[team],indent=3)))
    file.close()