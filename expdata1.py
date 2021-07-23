from numpy import NaN
import numpy as np
import pandas as pd
pd.options.plotting.backend = "plotly"
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

import seaborn as sns


"""RespondentID,
Have you seen any of the 6 films in the Star Wars franchise?,
Do you consider yourself to be a fan of the Star Wars film franchise?,
Which of the following Star Wars films have you seen? Please select all that apply.,,,,,,
Please rank the Star Wars films in order of preference with 1 being your favorite film in the franchise and 6 being your least favorite film.,,,,,,
"Please state whether you view the following characters favorably, unfavorably, or are unfamiliar with him/her.",,,,,,,,,,,,,,
Which character shot first?,
Are you familiar with the Expanded Universe?,
Do you consider yourself to be a fan of the Expanded Universe?,
Do you consider yourself to be a fan of the Star Trek franchise?,
Gender,
Age,
Household Income
,Education,
Location (Census Region)
,Response,Response,Star Wars: Episode I  The Phantom Menace,Star Wars: Episode II  Attack of the Clones,Star Wars: Episode III  Revenge of the Sith,Star Wars: Episode IV  A New Hope,Star Wars: Episode V The Empire Strikes Back,Star Wars: Episode VI Return of the Jedi,Star Wars: Episode I  The Phantom Menace,Star Wars: Episode II  Attack of the Clones,Star Wars: Episode III  Revenge of the Sith,Star Wars: Episode IV  A New Hope,Star Wars: Episode V The Empire Strikes Back,Star Wars: Episode VI Return of the Jedi,Han Solo,Luke Skywalker,Princess Leia Organa,Anakin Skywalker,Obi Wan Kenobi,Emperor Palpatine,Darth Vader,Lando Calrissian,Boba Fett,C-3P0,R2 D2,Jar Jar Binks,Padme Amidala,Yoda,Response,Response,Response,Response,Response,Response,Response,Response,Response

3292879998,Yes,Yes,Star Wars: Episode I  The Phantom Menace,Star Wars: Episode II  Attack of the Clones,Star Wars: Episode III  Revenge of the Sith,Star Wars: Episode IV  A New Hope,Star Wars: Episode V The Empire Strikes Back,Star Wars: Episode VI Return of the Jedi,3,2,1,4,5,6,Very favorably,Very favorably,Very favorably,Very favorably,Very favorably,Very favorably,Very favorably,Unfamiliar (N/A),Unfamiliar (N/A),Very favorably,Very favorably,Very favorably,Very favorably,Very favorably,I don't understand this question,Yes,No,No,Male,18-29,,High school degree,South Atlantic
"""

#Who shot first?
#Han
#Greedo
#I don't understand this question

def main():
    swDF = pd.read_csv("starwars.csv")
    
    new_columns = ['ID', 'HasSeenAny', 'Fan',\
        'SeenEp1', 'SeenEp2', 'SeenEp3', 'SeenEp4', 'SeenEp5', 'SeenEp6', \
        'RankEp1', 'RankEp2', 'RankEp3', 'RankEp4', 'RankEp5', 'RankEp6',\
        'RateHan', 'RateLuke','RateLeia', 'RateAnakin', 'RateObi', 'RateEmperor', 'RateVader',\
        'RateLando', 'RateBoba', 'RateC3PO', 'RateR2D2', 'RateJarJar', 'RatePadme', 'RateYoda', \
        'ShotFirst', 'KnowsExpUni', 'FanExpUni','FanStarTrek', \
        'Gender', 'Age', 'Income', 'Education', 'Region']
    swDF = swDF.rename(columns=dict(zip(swDF.columns, new_columns)))
    swDF = swDF.drop(0) #drop response questions/options row

    #shorten the titles of the movies
    swDF = swDF.replace("Star Wars: Episode I  The Phantom Menace", value="Ep1")
    swDF = swDF.replace("Star Wars: Episode II  Attack of the Clones", value="Ep2")
    swDF = swDF.replace("Star Wars: Episode III  Revenge of the Sith", "Ep3")
    swDF = swDF.replace("Star Wars: Episode IV  A New Hope", "Ep4")
    swDF = swDF.replace("Star Wars: Episode V The Empire Strikes Back", "Ep5")
    swDF = swDF.replace("Star Wars: Episode VI Return of the Jedi","Ep6")
    #output csv with shortened titles
    swDF.to_csv("titles-shortened.csv")

    #count each episodes watch counts over all survey respondents who answered
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

    # #for matplotlib.pyplot
    # watchTotalsBarChart = plt.figure()
    # watchTotalsBarChart = watchTotalsBarChart.add_axes([0,0,1,1])
    # x = ['Ep1', 'Ep2', 'Ep3', 'Ep4', 'Ep5', 'Ep6']
    # y = watchTotals
    # plt.xlabel("Episodes")
    # plt.ylabel("Watch Count")
    # watchTotalsBarChart.bar(x,y)
    # #plt.show()

    #seaborn plots
    sns.barplot(data=wT)
    plt.tight_layout()
    plt.title("Watch Count by Episode, all responses")
    plt.xlabel("Episode Number")
    plt.ylabel("WatchCount")
    plt.savefig("WatchCount")
    plt.close()
    #bar chart of Watch Count by Episode Number

    #Begin making dataframe of income and movie ranking responses
    swDFincome = swDF[pd.notnull(swDF["Income"])]
    swDF_incomeFav = swDFincome.dropna(subset=[\
        'RankEp1', 'RankEp2', 'RankEp3',\
        'RankEp4', 'RankEp5',\
        'RankEp6'], how="any")
    #"$100,000 - $149,999"
    swDF_incomeFav.groupby(swDF_incomeFav['Income'])
    swDF_incomeFav = swDF_incomeFav[['RankEp1','RankEp2','RankEp3','RankEp4','RankEp5','RankEp6', 'Income']]
    #at this point this dataframe is only income and movie rank responses
    swDF_incomeFav.to_csv("income-fav-movie.csv", index=False)

    swDF_incomeFav[['RankEp1','RankEp2','RankEp3','RankEp4','RankEp5','RankEp6']] \
        = swDF_incomeFav[['RankEp1','RankEp2','RankEp3','RankEp4','RankEp5','RankEp6']]\
        .apply(pd.to_numeric, errors='coerce')

    print(swDF_incomeFav.dtypes)


    ratings_income_group_mean = \
        swDF_incomeFav.groupby('Income').mean()
    ratings_income_group_size = \
        swDF_incomeFav.groupby('Income').size()
    

    print(ratings_income_group_mean)
    print(ratings_income_group_size)
    
    #group024k=ratings_income_group_mean.get_group("$0 - $24,999")

    ratings = sns.barplot(
        data=ratings_income_group_mean)
    plt.savefig("Ratings and Income")
    #TODO make bar chart of movie ratings by income level for each episode
    #TODO determine if difference between 150k+ liking Episode 4 the most is statistically significant
    #Ratings: 1 is best, 6 is worst. Lower scores, more favorites.

main()




