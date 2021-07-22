from asyncio import windows_events
from dask.base import compute
import dask.dataframe as dd
from dask.diagnostics import ProgressBar
from numpy import NaN
import pandas as pd
import matplotlib.pyplot as plt

"""RespondentID,
Have you seen any of the 6 films in the Star Wars franchise?,
Do you consider yourself to be a fan of the Star Wars film franchise?,
Which of the following Star Wars films have you seen? Please select all that apply.,,,,,,
Please rank the Star Wars films in order of preference with 1 being your favorite film in the franchise and 6 being your least favorite film.,,,,,,
"Please state whether you view the following characters favorably, unfavorably, or are unfamiliar with him/her.",,,,,,,,,,,,,,
Which character shot first?,
Are you familiar with the Expanded Universe?,
Do you consider yourself to be a fan of the Expanded Universe?��,
Do you consider yourself to be a fan of the Star Trek franchise?,
Gender,
Age,
Household Income
,Education,
Location (Census Region)
,Response,Response,Star Wars: Episode I  The Phantom Menace,Star Wars: Episode II  Attack of the Clones,Star Wars: Episode III  Revenge of the Sith,Star Wars: Episode IV  A New Hope,Star Wars: Episode V The Empire Strikes Back,Star Wars: Episode VI Return of the Jedi,Star Wars: Episode I  The Phantom Menace,Star Wars: Episode II  Attack of the Clones,Star Wars: Episode III  Revenge of the Sith,Star Wars: Episode IV  A New Hope,Star Wars: Episode V The Empire Strikes Back,Star Wars: Episode VI Return of the Jedi,Han Solo,Luke Skywalker,Princess Leia Organa,Anakin Skywalker,Obi Wan Kenobi,Emperor Palpatine,Darth Vader,Lando Calrissian,Boba Fett,C-3P0,R2 D2,Jar Jar Binks,Padme Amidala,Yoda,Response,Response,Response,Response,Response,Response,Response,Response,Response
3292879998,Yes,Yes,Star Wars: Episode I  The Phantom Menace,Star Wars: Episode II  Attack of the Clones,Star Wars: Episode III  Revenge of the Sith,Star Wars: Episode IV  A New Hope,Star Wars: Episode V The Empire Strikes Back,Star Wars: Episode VI Return of the Jedi,3,2,1,4,5,6,Very favorably,Very favorably,Very favorably,Very favorably,Very favorably,Very favorably,Very favorably,Unfamiliar (N/A),Unfamiliar (N/A),Very favorably,Very favorably,Very favorably,Very favorably,Very favorably,I don't understand this question,Yes,No,No,Male,18-29,,High school degree,South Atlantic
"""

#ID,haveyouseenany,Which ones (up to 6), Rankmovies1to6 1 isbest, Rate 14 characters,Whoshotfirst?,KnowExpUniv?,StarTrek?,Gender,Age,Income,Education,Region

#Who shot first?
#Han
#Greedo
#I don't understand this question

#rate characters:
#Han Solo,Luke Skywalker,Princess Leia Organa,Anakin Skywalker,
# Obi Wan Kenobi,Emperor Palpatine,Darth Vader,Lando Calrissian,
# Boba Fett,C-3P0,R2 D2,Jar Jar Binks,Padme Amidala,Yoda

def get_movie_seen_counts(n):
    ep1count = ep2count = ep3count  = ep4count = ep5count = ep6count = 0
    if n == "Star Wars: Episode I  The Phantom Menace":
        ep1count+=1
        n = "Ep1"
    if n == "Star Wars: Episode II  Attack of the Clones":
        ep2count+=1
        n = "Ep2"
    if n == "Star Wars: Episode III  Revenge of the Sith":
        ep3count+=1
        n = "Ep3"
    if n == "Star Wars: Episode IV  A New Hope":
        ep4count+=1
        n = "Ep4"
    if n == "Star Wars: Episode V The Empire Strikes Back":
        ep5count+=1
        n = "Ep5"
    if n == "Star Wars: Episode VI Return of the Jedi":
        ep6count+=1
        n = "Ep6"
    return n


def main():
    swDF = pd.read_csv("starwars.csv")
    
    new_columns = ['ID', 'HasSeenAny', 'Fan', 'SeenEp1', 'SeenEp2', \
        'SeenEp3', 'SeenEp4', 'SeenEp5', 'SeenEp6', \
        'RankEp1', 'RankEp2', 'RankEp3', 'RankEp4', 'RankEp5', 'RankEp6' \
        'RateHan', 'RateLuke','RateLeia', 'RateAnakin', 'RateObi', 'RateEmperor', \
        'RateVader', 'RateLando', 'RateBoba', 'RateC3PO', 'RateR2D2', 'RateJarJar', \
        'RatePadme', 'RateYoda', \
        'ShotFirst', 'KnowsExpUni', 'FanStarTrek', \
        'Gender', 'Age', 'Income', 'Education', 'Region']
    swDF = swDF.rename(columns=dict(zip(swDF.columns, new_columns)))
    swDF = swDF.drop('ID', axis=1)

    count = 0
    rowcount = 0
    for i,row in swDF.iterrows():
        rowcount+=1
        if row['SeenEp1'] is not NaN:
            count+=1
    print(swDF.head(2))
    print(f"Seen Ep1 Count {count} Row Count {rowcount}")
    seenEp1 = swDF["SeenEp1"].notnull().sum()
    seenEp2 = swDF["SeenEp2"].notnull().sum()
    seenEp3 = swDF["SeenEp3"].notnull().sum()
    seenEp4 = swDF["SeenEp4"].notnull().sum()
    seenEp5 = swDF["SeenEp5"].notnull().sum()
    seenEp6 = swDF["SeenEp6"].notnull().sum()


    watchTotals = [seenEp1,seenEp2,seenEp3,seenEp4,seenEp5,seenEp6]
    wT = {'Ep1': [seenEp1], 'Ep2': [seenEp2], 'Ep3': [seenEp3], \
        'Ep4': [seenEp4],'Ep5': [seenEp5], 'Ep6': [seenEp6] }
    wT = pd.DataFrame(data = wT)

    watchTotalsBarChart = plt.figure()
    watchTotalsBarChart = watchTotalsBarChart.add_axes([0,0,1,1])
    x = ['Ep1', 'Ep2', 'Ep3', 'Ep4', 'Ep5', 'Ep6']
    y = watchTotals
    watchTotalsBarChart.bar(x,y)
    plt.show()

    

main()


