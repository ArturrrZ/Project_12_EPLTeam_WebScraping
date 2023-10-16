import requests
from bs4 import BeautifulSoup

###STEP 1: open website and get html text

ARSENAL_FLASHSCORE='https://www.flashscore.com/team/arsenal/hA1Zm19f/squad/'
header={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
    "Accept-Language":"en-US,en;q=0.9",
}

website=requests.get(url=ARSENAL_FLASHSCORE, headers=header)
website.raise_for_status()
print(website.status_code)
website_html=website.text
# print(website_html)
###STEP 2: pass into BS4
soup=BeautifulSoup(website_html,'html.parser')

#STEP 3: FIND ALL DIVS
#FIND ALL DIVS cuz find all by string does not work :(
divs=soup.find_all('div')
###STEP 4:find all players and the coach
#Goalkeepers
parent_gks=[]
for div_gks in divs:
    if div_gks.getText() == 'Goalkeepers':
        parent_gks.append(div_gks.parent)

anchors_gks=parent_gks[0].find_all('a')
players_gks=[player.getText().strip() for player in anchors_gks]

print(players_gks)
#Defenders
parent_def=[]
for each in divs:
    if each.getText() == "Defenders":
        parent_def.append(each.parent)
anchors=parent_def[0].find_all('a')
players_defenders=[player.getText().strip() for player in anchors]