# Forecasting-COVID19-cases

This is a project on COVID-19 Analysis which visualizes the data from the johns hopkins GITHUB handel. This project contains a detailed report on key observations learnt from the given data.


# How to RUN and Modules Required
To render the visualizations, Please run the **main.py** file which produces the graphs. (Details of each file and folder structure  is mentioned below)

A few modules have been used to make this visualizations possible. Below are the **required** modules to run the main.py file.

 - **Pandas Sql** (This module is used to run SQL queries on Pandas Dataframe)(pip install pandasql)
 - **Numpy** (This module is used while curve fitting) (pip install numpy)
 -  **Seaborn** (This module is used to better visualize the box-plots) (pip install seaborn)
 - **gmplot** (This module is used to plot the heat map of global data of COVID-19 on Google Maps)

# Files

This project contains two files:
1) helper.py:
	**This file contains HelperClass which contains the following functions:**
	
	a) **get_top10_countries**:
   This function first calls the process_data function passing the dataframe to be processed. It returns a processed_dataset dataframe which contains 
   all the countires processed into a single time-seris
   Now running two queries, it would create two dataframes top10_countries_by_confirmed and top10_countries_by_death
   it would return top10_countries_by_confirmed , top10_countries_by_death , processed_dataset
   top10_countries_by_confirmed -> This dataframe contains information of top 10 countries based on confirmed cases
   top10_countries_by_death -> This dataframe contains information of top 10 countries based on deaths repoted
   processed_dataset -> This dataframe contains information of all countires processed into single time-series

b) **process_data**:
   This function is used to take the complete covid-19 data from csv file (passed from main.py) and process all countires into a proper time-series
   the first query used to fetch detials of all countires that have proviences
   the second query is used to fetch detials of all countries that dont have proviences
   now processed_dataset appends the outputs of the above two queries
   the third query is run on processed_dataset that is used to sum all the deaths or confirmed cases per day for all countires which can later be easily visualized

c) **plot_data**:
   This function is used to later visualize the top 10 countires after their 100th case is repoted in a time-series fashion

2) Main.py:
	This file is the main file that should be run to generate the visualizations

# Folder Structure
output graphs

> This folder contains all the snippets of visualizations made.

main.py

> This is the main file that should be run to produce the output.

helper.py

> This is the helper file for processing and visualizing the data

coviddata.csv

> This is the data file that is used to perform the analysis and
> visualization. It is taken from Johns Hopkins github

report.pdf

> This report contains detailed analysis of key patterns found in the
> data



         
