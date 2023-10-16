import requests
from bs4 import BeautifulSoup
import pandas as pd
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
# print(players_gks)
#Defenders
parent_def=[]
for each in divs:
    if each.getText() == "Defenders":
        parent_def.append(each.parent)
anchors=parent_def[0].find_all('a')
players_defenders=[player.getText().strip() for player in anchors]
#Mid&For&Coach
parent_mid=[]
parent_for=[]
parent_coach=[]
for div in divs:
    if div.getText() == "Midfielders":
        parent_mid.append(div.parent)
    if div.getText() == 'Forwards':
        parent_for.append(div.parent)
    if div.getText()=='Coach':
        parent_coach.append(div.parent)
#Midfielders
anchors_mid=parent_mid[0].find_all('a')
players_mid=[player.getText().strip() for player in anchors_mid]
#Forwards
anchors_forwards=parent_for[0].find_all('a')
players_forwards=[player.getText().strip() for player in anchors_forwards]
#Coach
anchors_coach=parent_coach[0].find('a')
coach=anchors_coach.getText().strip()
# print(players_gks,players_defenders,players_mid,players_forwards,coach)

#ALL TEAM CSV FILE
all_players={
    'Player':[]
}
#Goalkeepers csv file
goalkeepers={
    'Player':[]
}
for goalkeeper in players_gks:
    goalkeepers['Player'].append(goalkeeper)
    all_players['Player'].append(goalkeeper)
goalkeepers_df=pd.DataFrame(goalkeepers)
goalkeepers_df.to_csv('goalkeepers.csv',index=False)
#Defenders csv file
defenders={
    'Player':[]
}
for player in players_defenders:
    defenders['Player'].append(player)
    all_players['Player'].append(player)
defenders_df=pd.DataFrame(defenders)
defenders_df.to_csv('defenders.csv',index=False)
#midfilders csv file
midfielders={
    'Player':[]
}
for player in players_mid:
    midfielders['Player'].append(player)
    all_players['Player'].append(player)
midfielders_df=pd.DataFrame(midfielders)
# midfielders_df.to_csv('midfielders.csv',index=False)

#Forward csv file
forwards={
    'Player': []
}
for player in players_forwards:
    forwards['Player'].append(player)
    all_players['Player'].append(player)
forwards_df=pd.DataFrame(forwards)
forwards_df.to_csv('forwards.csv',index=False)

# print(all_players)

all_players_df=pd.DataFrame(all_players)
all_players_df.to_csv('all_players.csv',index=False)
ages_mid=[]
# print(anchors_mid)
for anchor in anchors_mid:

    href=anchor.get('href')
    href_url=f"https://www.flashscore.com{href}"
    response=requests.get(url=href_url,headers=header)
    response.raise_for_status()
    href_html=response.text

    href_soup=BeautifulSoup(href_html,'html.parser')
    # print(href_html)
    profile_heading=href_soup.select('.player-profile-heading .typo-participant-info-regular')
    age_str=profile_heading[0].getText()
    age=int(age_str)
    ages_mid.append(age)
midfielders_df['Age']=ages_mid
midfielders_df_lastcell={
    'Player': "Average Age",
    'Age': midfielders_df['Age'].mean()
}
midfielders_df=midfielders_df._append(midfielders_df_lastcell,ignore_index=True)
midfielders_df.to_csv('midfielders.csv',index=False)







