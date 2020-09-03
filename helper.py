import pandas as pd
import pandasql as sql
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import numpy as np
from datetime import datetime


'''
The below HelperClass contains the following functions:
1) get_top10_countries:
   This function first calls the process_data function passing the dataframe to be processed. It returns a processed_dataset dataframe which contains 
   all the countires processed into a single time-seris
   Now running two queries, it would create two dataframes top10_countries_by_confirmed and top10_countries_by_death
   it would return top10_countries_by_confirmed , top10_countries_by_death , processed_dataset
   top10_countries_by_confirmed -> This dataframe contains information of top 10 countries based on confirmed cases
   top10_countries_by_death -> This dataframe contains information of top 10 countries based on deaths repoted
   processed_dataset -> This dataframe contains information of all countires processed into single time-series

2) process_data:
   This function is used to take the complete covid-19 data from csv file (passed from main.py) and process all countires into a proper time-series
   the first query used to fetch detials of all countires that have proviences
   the second query is used to fetch detials of all countries that dont have proviences
   now processed_dataset appends the outputs of the above two queries
   the third query is run on processed_dataset that is used to sum all the deaths or confirmed cases per day for all countires which can later be easily visualized

3) plot_data:
   This function is used to later visualize the top 10 countires after their 100th case is repoted in a time-series fashion
'''

class HelperClass:

    def get_top10_countries(self,dataframe):
        processed_dataset=self.process_data(dataframe)
        top10_countries_by_confirmed=(sql.sqldf("select Date,Country,Max(Confirmed) as Confirmed,Lat,Long from processed_dataset GROUP BY Country ORDER BY Confirmed DESC LIMIT 10",locals()))
        top10_countries_by_death=(sql.sqldf("select Date,Country,Max(Deaths) as Deaths,Lat,Long from processed_dataset GROUP BY Country ORDER BY Deaths DESC LIMIT 10",locals()))
    
        return top10_countries_by_confirmed,top10_countries_by_death,processed_dataset

    def process_data(self,dataframe):
        query1="SELECT Date,Country,SUM(Confirmed) as Confirmed,SUM(Deaths) as Deaths,Lat,Long FROM dataframe WHERE Province NOT NULL GROUP BY Date,Country ORDER BY Country" 
        query2="SELECT Date,Country,Confirmed,Deaths,Lat,Long FROM dataframe WHERE Province IS NULL"
        query3="SELECT Date,Country,SUM(Confirmed) as Confirmed,SUM(Deaths) as Deaths,Lat,Long FROM processed_dataset GROUP BY Date,Country ORDER BY Country"
        dataset_with_provience=sql.sqldf(query1)
        dataset_without_proviences=sql.sqldf(query2)
        processed_dataset=dataset_with_provience.append(dataset_without_proviences,ignore_index=True )
    
        return sql.sqldf(query3)
                    
    def plot_data(self,data_set):
        for i in range(len(data_set)):
            data_set[i]['Date']=pd.to_datetime(data_set[i]['Date'])
            plt.legend(loc="upper left")
            plt.plot(data_set[i]['Date'],data_set[i]['Confirmed'],label=data_set[i]['Country'].iloc[0])
            plt.xticks(rotation=15)
         
        ax = plt.axes()
        ax.grid(linestyle='-', linewidth='0.2', color='white')
        plt.title('Top 10 Countries COVID-19 Confirmed after 100th case reported')
        ax.set_facecolor("black")
        plt.show()