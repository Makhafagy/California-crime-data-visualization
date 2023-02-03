# California-house-prices-prediction
## Current data covers years (2000-2013)

## Project Purpose
The project provides valuable insights into the relationship between crime rates and house prices in California. The data visualizations created in this project can be used by potential home buyers, real estate agents, and city planners to make more informed decisions. This can include identifying areas where home prices may be undervalued due to high crime rates, or areas where crime may be a concern for potential home buyers. Additionally, this project can be used as a starting point for further research and analysis on the topic.

## Overview
The objective of this data visualization project is to explore the potential correlation between variables like crime rates and house prices in California. The project aims to answer the question of whether areas with higher crime rates tend to have lower house prices, and vice versa.

To accomplish this, the project utilizes data from two sources: the California Department of Justice and Zillow. The crime data includes information on various crime types such as burglary, theft, and assault, as well as the location of the incidents. The housing data includes information on median home prices, home values, and the number of homes sold.

The data is then cleaned and merged to create a comprehensive dataset that includes both crime and housing information for various cities in California. This dataset is then used to create various visualizations such as scatter plots, line charts, and heat maps to better understand the relationship between crime rates and house prices.

Additionally, other variables such as population density, median income, and education level will also be taken into consideration in the future to see if they have any impact on house prices.

## Data Cleaning and Preparation
The first step in the project was to gather and clean the data. The crime data was obtained from the California Department of Justice and required some cleaning to remove any irrelevant information and ensure that the data was consistent. The housing data was obtained from Zillow and also required cleaning to ensure that it was in a format that could be easily merged with the crime data.

## Data Analysis
After cleaning and merging the data, the project then moved on to the data analysis phase. Various visualizations were created to better understand the relationship between crime rates and house prices. This included scatter plots, line charts, and heat maps. These visualizations helped to identify patterns and trends in the data that could not be easily observed by simply looking at the raw data.

## Prediction
There is a clear relationship between crime rates and house prices in California. Cities with higher crime rates tend to have lower house prices, and vice versa. However, this relationship is not always linear and can vary depending on the type of crime and the location.

## Results
We used Seaborn's FacetGrid and regplot functions to create scatterplots that showed the relationship between crime rates and average house prices for each year in the data set. We also drew a line of regression to determine the correlation between the two variables.

After analyzing the data, we found that there was no clear correlation between crime rates and house prices in California. The scatterplots showed a weak, scattered relationship between the two variables, and the lines of regression had low slope values and poor R-squared values.
![image](https://user-images.githubusercontent.com/52415396/216567057-9220aeb2-c699-42d8-84eb-6e0a14159a99.png)

This result suggests that crime rates do not have a significant impact on house prices in California. Other factors, such as the local economy, housing supply, and demand, likely have a greater influence on house prices in the state.

## Conclusion
This study provides evidence that there is no significant correlation between crime rates and house prices in California.

More conclusions are to come as we take other variables into consideration.

## Getting Started

### Requirements
Install Python, pip, Visual Studio Code.

### Dependencies
Install required dependencies:
```
pip install pandas
```
```
pip install numpy
```
### How To Run
```
python california.py
```

## Author
* **Mahmoud Khafagy**
