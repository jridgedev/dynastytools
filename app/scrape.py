from lxml import html
import requests
import json
import os

class Scrape:
    availablePositions = ['QB', 'RB', 'WR', 'TE', 'D/ST', 'K']
    fileLocation = os.getcwd() + '/json/'

    def writeTeamData(self, teamData):
        fileName = self.fileLocation + 'leagueTeams.json'
        fileContent = json.dumps(teamData)
        with open(fileName, 'w') as f:
            f.write(json.dumps(fileContent))

    def getJson(self, teamName, playerNodes):
        teamData = {}
        players = []
        for node in playerNodes:
            player = {}
            name = node.xpath('a')[0].text
            raw = node.text_content()
            split = str.split(raw, '\u00a0')
            position = split[1]
            playerTeam = str.replace(str.replace(split[0], name, ''), ', ', '')

            player['name'] = name
            player['position'] = position
            player['team'] = playerTeam
            players.append(player)

        teamData['teamName'] = teamName
        teamData['players'] = players
        return teamData

    def scrape(self, leagueId, teams):
        urlBase = 'http://games.espn.go.com/ffl/clubhouse?leagueId=' + leagueId + '&teamId='
        season = '&seasonId=2016'

        teamData = {}
        teamList = []
        for i in range(1,teams + 1):
            url = urlBase + str(i) + season
            page = requests.get(url)
            tree = html.fromstring(page.content)
            players = tree.xpath('//*[@class="playertablePlayerName"]')
            nameNode = tree.xpath('//h3[@class="team-name"]')
            teamName = nameNode[0].text.rstrip()
            teamJson = self.getJson(teamName, players)
            teamList.append(teamJson)

        teamData['teams'] = teamList
        self.writeTeamData(teamData)

Scrape().scrape('288521', 12)