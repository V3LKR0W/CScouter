import requests, time, os
from colorit import *
from dotenv import load_dotenv, dotenv_values
init_colorit()
load_dotenv()


Config = dotenv_values('.env')



Players = []
kills = []
deaths = []
wins = []
surrenders = []
w = []
s = []
cs = []
a = []

try:
    Req = requests.get('https://127.0.0.1:2999/liveclientdata/allgamedata', verify=False).json()
except Exception:
    print(color('Couldn\'t find a connection to the local server.', Colors.red))



for Player in Req['allPlayers']:
    getSummonerUsername = requests.get(f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{Player["summonerName"]}?api_key={Config["API_KEY"]}').json()
    Players.append(dict(
                        name=getSummonerUsername['name'],
                        id=getSummonerUsername['puuid'],
                        current_champion=Player['championName'],
                        level=0,
                        games=[],
                        kill_arry=[], 
                        avg_kills=0,
                        death_arry=[],
                        avg_deaths=0,
                        wins_arry=[],
                        avg_wins=0,
                        surrenders_arry=[],
                        avg_surrenders=0,
                        cs_arry=[],
                        avg_cs=0,
                        assists_arry=[],
                        avg_assists=0,
                        ))


for x in range(len(Players)):
    games = requests.get(f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{Players[x]["id"]}/ids?type=normal&start=0&count={Config["Count"]}&api_key={Config["API_KEY"]}').json()
    Players[x]['games'] = games
    
    
def find_avg(table,store):
    for x in range(len(Players)):
        tble = Players[x][str(table)]
        ans = sum(tble) / int(Config['Count'])
        Players[x][str(store)] = int(ans)

def total(table, store):
    for x in range(len(Players)):
        tble = Players[x][str(table)]
        ans = sum(tble)
        Players[x][str(store)] = int(ans)
    
       

    
for i in range(len(Players)):
    for Games in Players[i]['games']:
        Match = requests.get(f'https://americas.api.riotgames.com/lol/match/v5/matches/{Games}?api_key={Config["API_KEY"]}').json()
        try:
            for z in range(len(Match['info']['participants'])):
                if Match['info']['participants'][z]['summonerName'] == Players[i]['name']:
                    
                    kills.append(Match['info']['participants'][z]['kills'])
                    
                    a.append(Match['info']['participants'][z]['assists'])
                    
                    deaths.append(Match['info']['participants'][z]['deaths'])
                    
                    wins.append(Match['info']['participants'][z]['win'])
                    
                    surrenders.append(Match['info']['participants'][z]['gameEndedInSurrender'])
                    
                    cs.append(Match['info']['participants'][z]['totalMinionsKilled'])
                    
                    
                    Players[i]['level'] = Match['info']['participants'][z]['summonerLevel']
                    
                    Players[i]['kill_arry'] = kills.copy()
                    
                    Players[i]['assists_arry'] = kills.copy()
                    
                    Players[i]['death_arry'] = deaths.copy()
                    
                    Players[i]['wins_arry'] = wins.copy()
                    
                    Players[i]['surrenders_arry'] = surrenders.copy()
                
                    Players[i]['cs_arry'] = cs.copy()
                    
        except:
            print(color('Ratelimit hit. Retrying in 40 seconds..', Colors.red))
            time.sleep(40)
            pass
            
    deaths.clear() 
    wins.clear()           
    kills.clear()
    wins.clear()
    surrenders.clear()
    cs.clear()
    a.clear()
    

    find_avg('kill_arry','avg_kills')
    
    find_avg('death_arry','avg_deaths')
    
    find_avg('cs_arry', 'avg_cs')
    
    find_avg('assists_arry', 'avg_assists')
    
    total('wins_arry', 'avg_wins')
    
    total('surrenders_arry', 'avg_surrenders')
    
   
                
# Final Output 
os.system('cls')
for x in range(len(Players)):
    print(color(f'{Players[x]["current_champion"]} - {Players[x]["name"]} - Level ({Players[x]["level"]}) \n Averages {Players[x]["avg_kills"]} kills per game. \n Averages {Players[x]["avg_deaths"]} deaths per game. \n Averages {Players[x]["avg_assists"]} assists per game. \n {Players[x]["avg_wins"]}/{Config["Count"]} have games been wins and {Players[x]["avg_surrenders"]} games were ended early by FF. \n They have an average CS score of {Players[x]["avg_cs"]}', Colors.blue))
    print(color('--------------------', Colors.purple))
         
print(color(f'All stats are based off the players last {Config["Count"]}. You Can change this in the ".env" file.', Colors.red))

