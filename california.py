import pandas as pd
import numpy as np

crime_data = pd.read_csv("california_crimes.csv", low_memory=False)
housing_data = pd.read_csv("california_housing_prices.csv")

# rename RegionName to City, so we can inner join crime and housing data
crime_data = crime_data.rename(columns={'geoname': 'city', 'rate':'crime_rate', 'reportyear':'report_year'})
# print(crime_data)

# rename RegionName to City, so we can inner join crime and housing data
housing_data = housing_data.rename(columns={'RegionName': 'city', 'RegionID': 'region_id', 'SizeRank':'size_rank'})


# extract the year and group by it
#housing_data = housing_data.groupby(housing_data[['1/31/2022','2/28/2022','3/31/2022','4/30/2022','5/31/2022','6/30/2022','7/31/2022',
#                                                  '8/31/2022','9/30/2022','10/31/2022','11/30/2022','12/31/2022']].dt.year, axis=1).sum()

not_date_columns = ['region_id','size_rank','city','RegionType','StateName','State','Metro','CountyName']

for column in housing_data.columns:
    if column not in not_date_columns:
        if column.find('2000') != -1:
            housing_data = housing_data.rename(columns={column: '2000_price_avg'})
        elif column.find('2001') != -1:
            housing_data = housing_data.rename(columns={column: '2001_price_avg'})
        elif column.find('2002') != -1:
            housing_data = housing_data.rename(columns={column: '2002_price_avg'})
        elif column.find('2003') != -1:
            housing_data = housing_data.rename(columns={column: '2003_price_avg'})
        elif column.find('2004') != -1:
            housing_data = housing_data.rename(columns={column: '2004_price_avg'})
        elif column.find('2005') != -1:
            housing_data = housing_data.rename(columns={column: '2005_price_avg'})
        elif column.find('2006') != -1:
            housing_data = housing_data.rename(columns={column: '2006_price_avg'})
        elif column.find('2007') != -1:
            housing_data = housing_data.rename(columns={column: '2007_price_avg'})
        elif column.find('2008') != -1:
            housing_data = housing_data.rename(columns={column: '2008_price_avg'})
        elif column.find('2009') != -1:
            housing_data = housing_data.rename(columns={column: '2009_price_avg'})
        elif column.find('2010') != -1:
            housing_data = housing_data.rename(columns={column: '2010_price_avg'})
        elif column.find('2011') != -1:
            housing_data = housing_data.rename(columns={column: '2011_price_avg'})
        elif column.find('2012') != -1:
            housing_data = housing_data.rename(columns={column: '2012_price_avg'})
        elif column.find('2013') != -1:
            housing_data = housing_data.rename(columns={column: '2013_price_avg'})
        else:
            housing_data = housing_data.drop(labels=column, axis=1)

housing_data3 = housing_data
housing_data3.fillna(0)

crime_data3 = crime_data
mask = crime_data3['strata_level_name_code'] != 5
crime_data3.drop(crime_data3[mask].index, inplace=True)
crime_data3.reset_index(level=0, inplace=True)

# so we can inner join later
crime_data3.dropna(subset=['county_name'], inplace=True)

for col in housing_data3.select_dtypes(include=[np.float]):
    housing_data3[col] = housing_data3[col].fillna(0).astype(np.int64)

for col in crime_data3.select_dtypes(include=[np.float]):
    if col != 'crime_rate':
        crime_data3[col] = crime_data3[col].fillna(0).astype(np.int64)
    
housing_data2 = housing_data3
crime_data2 = crime_data3


if housing_data2.empty:
    print("The DataFrame is empty.")
else:
    housing_data2 = housing_data2.select_dtypes(include=['float64','int64'])
    housing_data2 = housing_data2.apply(pd.to_numeric, errors='coerce')
    housing_data2 = housing_data2.groupby(housing_data2.columns, axis=1).mean().round(0)
    housing_data3 = housing_data3.select_dtypes(include=['object'])

if crime_data2.empty:
    print("crimes are not found")
else:
    crime_data2 = crime_data2.select_dtypes(include=['float64','int64'])
    crime_data2 = crime_data2.apply(pd.to_numeric, errors='coerce')
    crime_data3 = crime_data3.select_dtypes(include=['object'])

for col in housing_data2.columns:
    if housing_data2[col].dtype == 'float64':
        housing_data2[col] = np.ceil(housing_data2[col]).astype(int)

for col in crime_data2.columns:
    if crime_data2[col].dtype == 'int64' and col != 'crime_rate':
        crime_data2[col] = np.ceil(crime_data2[col]).astype(int)

cols = housing_data2.columns.tolist()
#print(cols)

cols = crime_data2.columns.tolist()
#print(cols)

housing_data2 = housing_data2.assign(city=housing_data3['city'],state=housing_data3['State'],
                                     county_name=housing_data3['CountyName'])

housing_data2 = housing_data2.drop(columns=['size_rank', 'region_id'], axis=1)

crime_data2 = crime_data2.assign(city=crime_data3['city'], county_name=crime_data3['county_name'])

crime_data2 = crime_data2.drop(columns=['race_eth_code', 'strata_name_code', 'county_fips', 'ca_decile',
                                        'ca_rr', 'll_95ci', 'rse', 'se', 'ul_95ci', 'index', 'geotypevalue',
                                        'region_code'], axis=1)

# print(housing_data2)
# print(crime_data2)

#print(cols)
# date_housing_data = date_housing_data.groupby(date_housing_data.columns, axis=1)
#print(housing_data)
#print(crime_data)

# print(housing_data2['city'])
housing_data2['county_name'] = housing_data2['county_name'].replace(to_replace=' County', value='', regex=True)
housing_data2['city'] = housing_data2['city'].replace(to_replace=' City', value='', regex=True)

crime_data2['county_name'] = crime_data2['county_name'].replace(to_replace=' County', value='', regex=True)
crime_data2['city'] = crime_data2['city'].replace(to_replace=' city', value='', regex=True)

crime_data2.drop("city", axis=1, inplace=True)

print(housing_data2)
print(crime_data2)

print(crime_data2['strata_level_name_code'])

#inner join both crime and housing datasets
combined_data = pd.merge(crime_data2, housing_data2, on='county_name', how='inner')
combined_data.info()
if combined_data.empty:
    print("The DataFrame is empty.")


# get the current column order
cols = combined_data.columns.tolist()

mask = combined_data['numerator'] == 0
combined_data.drop(combined_data[mask].index, inplace=True)

mask = combined_data['denominator'] == 0
combined_data.drop(combined_data[mask].index, inplace=True)
combined_data.reset_index(inplace=True)

# reorder columns
cols.insert(0, cols.pop(cols.index('city')))
cols.insert(1, cols.pop(cols.index('county_name')))
cols.insert(2, cols.pop(cols.index('state')))

# reindex the dataframe with the new column order
combined_data = combined_data.reindex(columns=cols)

print(combined_data)
