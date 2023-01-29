import pandas as pd

crime_data = pd.read_csv("california_crimes.csv")
housing_data = pd.read_csv("california_housing_prices.csv")

# rename RegionName to City, so we can inner join crime and housing data
crime_data = crime_data.rename(columns={'reportyear': 'Year'})
# print(crime_data)

# rename RegionName to City, so we can inner join crime and housing data
housing_data = housing_data.rename(columns={'RegionName': 'City'})


# extract the year and group by it
#housing_data = housing_data.groupby(housing_data[['1/31/2022','2/28/2022','3/31/2022','4/30/2022','5/31/2022','6/30/2022','7/31/2022',
#                                                  '8/31/2022','9/30/2022','10/31/2022','11/30/2022','12/31/2022']].dt.year, axis=1).sum()

not_date_columns = ['RegionID','SizeRank','City','RegionType','StateName','State','Metro','CountyName']

for column in housing_data.columns:
    if column not in not_date_columns:
        if column.find('2000') != -1:
            housing_data = housing_data.rename(columns={column: '2000'})
        elif column.find('2001') != -1:
            housing_data = housing_data.rename(columns={column: '2001'})
        elif column.find('2002') != -1:
            housing_data = housing_data.rename(columns={column: '2002'})
        elif column.find('2003') != -1:
            housing_data = housing_data.rename(columns={column: '2003'})
        elif column.find('2004') != -1:
            housing_data = housing_data.rename(columns={column: '2004'})
        elif column.find('2005') != -1:
            housing_data = housing_data.rename(columns={column: '2005'})
        elif column.find('2006') != -1:
            housing_data = housing_data.rename(columns={column: '2006'})
        elif column.find('2007') != -1:
            housing_data = housing_data.rename(columns={column: '2007'})
        elif column.find('2008') != -1:
            housing_data = housing_data.rename(columns={column: '2008'})
        elif column.find('2009') != -1:
            housing_data = housing_data.rename(columns={column: '2009'})
        elif column.find('2010') != -1:
            housing_data = housing_data.rename(columns={column: '2010'})
        elif column.find('2011') != -1:
            housing_data = housing_data.rename(columns={column: '2011'})
        elif column.find('2012') != -1:
            housing_data = housing_data.rename(columns={column: '2012'})
        elif column.find('2013') != -1:
            housing_data = housing_data.rename(columns={column: '2013'})
        else:
            housing_data = housing_data.drop(labels=column, axis=1)
            

if housing_data.empty:
    print("The DataFrame is empty.")
else:
    housing_data = housing_data.select_dtypes(include=['float64','int64'])
    housing_data = housing_data.apply(pd.to_numeric, errors='coerce')
    housing_data = housing_data.groupby(housing_data.columns, axis=1).mean()

# date_housing_data = date_housing_data.groupby(date_housing_data.columns, axis=1)

print(housing_data)


# if all(col in housing_data.columns for col in housing_data.columns):
#     housing_data = housing_data.groupby(housing_data.columns, axis=1).mean()
# print(housing_data)
# inner join both crime and housing datasets
# merged_data = pd.merge(crime_data, housing_data, on='City', how='inner')
# print(merged_data)

