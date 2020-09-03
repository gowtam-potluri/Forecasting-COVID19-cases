import pandas as pd
import warnings
warnings.filterwarnings("ignore")
import pandasql as sql
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import seaborn as sns
import gmplot
import helper
import math

'''
The helper file contains HelperClass which contains a few functions like get_top10_countries , process_data which
help with the data wrangling(More documentation on how each function works is available in the helper.py file.
Below code is used to load the data from the coviddata.csv file and properly format the Dates column. Now that
dataframe is sent to the get_top10_countries function in helper class which returns a processed dataframe called
processed_dataset

'''
helperclass=helper.HelperClass()
dataframe = pd.read_csv('coviddata.csv',parse_dates=True)
dataframe['Date']=pd.to_datetime(dataframe['Date'])  #This helps to convert the Data column in coviddata.csv which is a string to a properly formated time stamp.(Year-Month-Day)
top10_by_confirmed,top10_by_deaths,processed_dataset=helperclass.get_top10_countries(dataframe) #This returns 3 dataframes 1) top10 countries in terms of confirmed 2)top 10 in terms of deaths
#and processed_dataset which contains detials of all countries brought into a single time-series.

plt.style.use('ggplot') #using ggplot in matplotlib to make graphs look better

#Plotting starts

'''
The Below code is used to generate the heat map of the given COVID-19 data.
This below code uses gmplot module which provide a matplotlib like interface to plotting data with Google Maps.
The output for this paticular code would be saved as world_heatmap.html in current working directory
'''
# declare the center of the map, and how much we want the map zoomed in
gmap = gmplot.GoogleMapPlotter(0, 0, 2)
# plot heatmap
gmap.heatmap(processed_dataset['Lat'], processed_dataset['Long'])
#Google_API_Key to plot the data on google maps (Since Google Maps is charging a fee for using their api, It dispalys "for developer use" when plotting the data for free)
gmap.apikey = "AIzaSyCgmGABehKA9_KCmeuWqKq5Z_F2EjlDHhk"
# save it to html
gmap.draw(r"world_heatmap.html")
#sending a notification to command line 
print('Heat Map of COVID-19 world data is saved as world_heatmap.html in the current working directory')

'''
The below code is used to visualize the outliers in the data in terms of confirmed cases and deaths reported.
This below code uses pandasql module which allows you to query pandas DataFrames using SQL syntax.
'''
#The below query is used to fetch the total number of confirmed cases and deaths reported for every country till 4/8/2020
query="SELECT Date, Country , MAX(Confirmed) as Confirmed, MAX(Deaths) as Deaths from processed_dataset group by Country"
#using seaborn module to present the below two boxplots
sns.boxplot(sql.sqldf(query)['Deaths']).set_title('Outliers in number of deaths reported globally')  #sql.sqldf is used to run the above SQL query against dataframe to fetch corresponding columns
plt.show()
sns.boxplot(sql.sqldf(query)['Confirmed']).set_title('Outliers in number of confirmed reported globally')
plt.show()

'''
The Below code is used to visualize the time series of number of confirmed cases in the USA and no of deaths reported in Italy
This below code uses pandasql module which allows you to query pandas DataFrames using SQL syntax.
'''
#The below query is used to fetch Country, Confirmed , Deaths data from the dataframe processed_dataset for countries Italy and the US
query="SELECT Date, Country , Confirmed , Deaths from processed_dataset where Country='Italy' or Country='US'"
dframe=sql.sqldf(query)
dframe_US=dframe[dframe['Country']=='US'] #since dframe dataframe contains data of both Italy and US, splitting data of the US and Italy into respective dataframes
dframe_Italy=dframe[dframe['Country']=='Italy']

dframe_Italy['Time']=np.arange(len(dframe_Italy['Deaths'])) #adding a new column time which contains dates staring from 0 when first case reported and till the latest date(4/8/2020)
dframe_US['Time']=np.arange(len(dframe_US['Confirmed']))


plt.plot(dframe_Italy['Time'],dframe_Italy['Deaths'])

ax = plt.axes() # getting the plot axes to set the grid , color properties
ax.grid(linestyle='-', linewidth='0.2', color='white')
ax.set_facecolor("black")
plt.title('Deaths reproted in Italy')
plt.xticks(rotation=15)
plt.show()

plt.plot(dframe_US['Time'],dframe_US['Confirmed'])

ax = plt.axes()
ax.grid(linestyle='-', linewidth='0.2', color='white')
plt.title('Confirmed cases in the USA')
ax.set_facecolor("black")
plt.xticks(rotation=15)

plt.show()

'''
Below code is used to visualize the top 10 countries in terms of confirmed cases after their 100th case is reported
'''
#The below query is used to fetch details of all countires from the time after their 100th case is reported and filtering out countires which have less than 20000 cases 
#The query return a dataframe which contains all the countires names with the above requirments
query="SELECT Date, Country , MAX(Confirmed) as Total FROM( SELECT Date,Country , Confirmed FROM processed_dataset where Confirmed > 100) GROUP BY Country HAVING Total > 20000"
newDset=sql.sqldf(query)
nndset=[]
temp=0
#The below loop is used to check the previous fetched countires list and match them with processed_dataset dataframe which contain all countires data 
#and filter only the requied countires and at the same time convert the date from string to time format and store them in nndset array
for i in range(len(newDset)):
    temp=(processed_dataset[processed_dataset['Country'].str.match(newDset['Country'][i]) & (processed_dataset['Confirmed'] >100)])
    temp['Date']=pd.to_datetime(temp['Date'])
    nndset.append(temp)
helperclass.plot_data(nndset) # The plot_data func helps to plot the given dataframe to set and visualize the above data in time seires(more documentation about function in the helper class)

'''
Below code is used to visualizae US and South Korea comparision time series
'''

query="SELECT Date, Country , Confirmed , Deaths from processed_dataset where Country='Korea, South' or Country='US'"
dframe=sql.sqldf(query)

dframe_US=dframe[dframe['Country']=='US'] #since dframe dataframe contains data of both SKorea and US, splitting data of the US and SKorea into respective dataframes
dframe_SKorea=dframe[dframe['Country']=='Korea, South']
dframe_US['Time']=np.arange(len(dframe_US['Confirmed']))
dframe_US['Confirmed']=np.log(dframe_US['Confirmed'])


dframe_SKorea['Time']=np.arange(len(dframe_SKorea['Confirmed']))
dframe_SKorea['Confirmed']=np.log(dframe_SKorea['Confirmed'])

plt.plot(dframe_US['Time'],dframe_US['Confirmed'],label="US")
plt.plot(dframe_SKorea['Time'],dframe_SKorea['Confirmed'],label="South Korea")
ax = plt.axes()
ax.grid(linestyle='-', linewidth='0.2', color='white')
plt.title('Comparision of Confirmed cases between the US and South Korea(Log Scale)')
ax.set_facecolor("black")
plt.xticks(rotation=15)
plt.legend(loc="upper left")
plt.show()
'''
Below code is for the curve fitting(Taking India as Example)
'''
query="select * from processed_dataset where Country='India' and Confirmed >0"
dframe=sql.sqldf(query)
dframe['logInfo']=np.log(dframe['Confirmed']) # converting confirmed cases into respective log values (check report for more details)
dframe['Time'] = np.arange(len(dframe))

plt.scatter(dframe['Time'].values.reshape(-1,1),dframe['Confirmed'].values.reshape(-1,1),color='r') #Visualizing the confirmed cases from origianl dataset

a,b=(np.polyfit(dframe['Time'], np.log(dframe['Confirmed']), 1, w=np.sqrt(dframe['Confirmed']))) #finding the best coeffcients for the given data 

#converting log back to exp (check report for more info)
a=math.exp(a)
b=math.exp(b)


def pred(t):
    return b*a**t

#adding a new column named predictions which can later be compared with confirmed cases to check the accruacy and plot the curve fit
dframe['Predictions'] = dframe.Time.apply(pred)

print(dframe)

plt.plot(dframe['Time'].values.reshape(-1,1),dframe['Predictions'].values.reshape(-1,1),color='blue')
plt.show()

