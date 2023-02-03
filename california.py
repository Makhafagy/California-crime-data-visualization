import pandas as pd
import numpy as np

crime_data = pd.read_csv("california_crimes.csv", low_memory=False)
housing_data = pd.read_csv("california_housing_prices.csv")

# rename RegionName to City, so we can inner join crime and housing data
crime_data = crime_data.rename(columns={'geoname': 'city', 'rate':'crime_rate', 'reportyear':'crime_report_year',
                                        'numerator':'criminals_population', 'denominator':'all_population'})

# rename RegionName to City, so we can inner join crime and housing data
housing_data = housing_data.rename(columns={'RegionName': 'city', 'RegionID': 'region_id', 'SizeRank':'size_rank'})

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

for col in housing_data3.select_dtypes(include=[np.float64]):
    housing_data3[col] = housing_data3[col].fillna(0).astype(np.int64)

for col in crime_data3.select_dtypes(include=[np.float64]):
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
                                        'region_code', 'dof_population'], axis=1)

housing_data2['county_name'] = housing_data2['county_name'].replace(to_replace=' County', value='', regex=True)
housing_data2['city'] = housing_data2['city'].replace(to_replace=' City', value='', regex=True)

crime_data2['county_name'] = crime_data2['county_name'].replace(to_replace=' County', value='', regex=True)
crime_data2['city'] = crime_data2['city'].replace(to_replace=' city', value='', regex=True)

crime_data2.drop("city", axis=1, inplace=True)

# print(housing_data2)
# print(crime_data2)
# print(crime_data2['strata_level_name_code'])

#inner join both crime and housing datasets
combined_data = pd.merge(crime_data2, housing_data2, on='county_name', how='inner')
# combined_data.info()
if combined_data.empty:
    print("The DataFrame is empty.")


# get the current column order
cols = combined_data.columns.tolist()

mask = combined_data['criminals_population'] == 0
combined_data.drop(combined_data[mask].index, inplace=True)

mask = combined_data['all_population'] == 0
combined_data.drop(combined_data[mask].index, inplace=True)
combined_data.reset_index(inplace=True)

# reorder columns
cols.insert(0, cols.pop(cols.index('city')))
cols.insert(1, cols.pop(cols.index('county_name')))
cols.insert(2, cols.pop(cols.index('state')))

# reindex the dataframe with the new column order
combined_data = combined_data.reindex(columns=cols)

# Get the values of the "city" column:
city = combined_data["city"].values

# Create a new column 'crime_report_year_diff' to store the difference between consecutive values in the 'crime_report_year' column:
combined_data['crime_report_year_diff'] = combined_data['crime_report_year'].diff()

# drop instances where city is repeated throughout the same crime_report_year
mask = combined_data['crime_report_year_diff'] == 0
combined_data.drop(combined_data[mask].index, inplace=True)

# drop instances where 2013_price_avg = 0, 
# efficient way to check if the entire city has 0 price avg throughout all years 2000-2013
mask = combined_data['2013_price_avg'] == 0
combined_data.drop(combined_data[mask].index, inplace=True)

# drop crime_report_year_diff since we don't need that column anymore
combined_data = combined_data.drop(columns=['crime_report_year_diff'], axis=1)

condition_2000 = (combined_data['crime_report_year'] == 2000)
condition_2001 = (combined_data['crime_report_year'] == 2001)
condition_2002 = (combined_data['crime_report_year'] == 2002)
condition_2003 = (combined_data['crime_report_year'] == 2003)
condition_2004 = (combined_data['crime_report_year'] == 2004)
condition_2005 = (combined_data['crime_report_year'] == 2005)
condition_2006 = (combined_data['crime_report_year'] == 2006)
condition_2007 = (combined_data['crime_report_year'] == 2007)
condition_2008 = (combined_data['crime_report_year'] == 2008)
condition_2009 = (combined_data['crime_report_year'] == 2009)
condition_2010 = (combined_data['crime_report_year'] == 2010)
condition_2011 = (combined_data['crime_report_year'] == 2011)
condition_2012 = (combined_data['crime_report_year'] == 2012)
condition_2013 = (combined_data['crime_report_year'] == 2013)

date_columns=['2000_price_avg', '2001_price_avg', '2002_price_avg', '2003_price_avg', '2004_price_avg', '2005_price_avg', '2006_price_avg', 
              '2007_price_avg', '2008_price_avg', '2009_price_avg', '2010_price_avg', '2011_price_avg', '2012_price_avg', '2013_price_avg']

# Create the new column 'D'
combined_data['price_avg_this_year'] = 0
if condition_2000.any():
    if '2000_price_avg' in date_columns:
        date_columns.remove('2000_price_avg')
    combined_data.loc[condition_2000, date_columns] = 0
    date_columns.append('2000_price_avg')
    
if condition_2001.any():
    if '2001_price_avg' in date_columns:
        date_columns.remove('2001_price_avg')
    combined_data.loc[condition_2001, date_columns] = 0
    date_columns.append('2001_price_avg')
    
if condition_2002.any():
    if '2002_price_avg' in date_columns:
        date_columns.remove('2002_price_avg')
    combined_data.loc[condition_2002, date_columns] = 0
    date_columns.append('2002_price_avg')
    
if condition_2003.any():
    if '2003_price_avg' in date_columns:
        date_columns.remove('2003_price_avg')
    combined_data.loc[condition_2003, date_columns] = 0
    date_columns.append('2003_price_avg')
    
if condition_2004.any():
    if '2004_price_avg' in date_columns:
        date_columns.remove('2004_price_avg')
    combined_data.loc[condition_2004, date_columns] = 0
    date_columns.append('2004_price_avg')
    
if condition_2005.any():
    if '2005_price_avg' in date_columns:
        date_columns.remove('2005_price_avg')
    combined_data.loc[condition_2005, date_columns] = 0
    date_columns.append('2005_price_avg')
    
if condition_2006.any():
    if '2006_price_avg' in date_columns:
        date_columns.remove('2006_price_avg')
    combined_data.loc[condition_2006, date_columns] = 0
    date_columns.append('2006_price_avg')
    
if condition_2007.any():
    if '2007_price_avg' in date_columns:
        date_columns.remove('2007_price_avg')
    combined_data.loc[condition_2007, date_columns] = 0
    date_columns.append('2007_price_avg')
    
if condition_2008.any():
    if '2008_price_avg' in date_columns:
        date_columns.remove('2008_price_avg')
    combined_data.loc[condition_2008, date_columns] = 0
    date_columns.append('2008_price_avg')
    
if condition_2009.any():
    if '2009_price_avg' in date_columns:
        date_columns.remove('2009_price_avg')
    combined_data.loc[condition_2009, date_columns] = 0
    date_columns.append('2009_price_avg')
    
if condition_2010.any():
    if '2010_price_avg' in date_columns:
        date_columns.remove('2010_price_avg')
    combined_data.loc[condition_2010, date_columns] = 0
    date_columns.append('2010_price_avg')
    
if condition_2011.any():
    if '2011_price_avg' in date_columns:
        date_columns.remove('2011_price_avg')
    combined_data.loc[condition_2011, date_columns] = 0
    date_columns.append('2011_price_avg')
    
if condition_2012.any():
    if '2012_price_avg' in date_columns:
        date_columns.remove('2012_price_avg')
    combined_data.loc[condition_2012, date_columns] = 0
    date_columns.append('2012_price_avg')
    
if condition_2013.any():
    if '2013_price_avg' in date_columns:
        date_columns.remove('2013_price_avg')
    combined_data.loc[condition_2013, date_columns] = 0
    date_columns.append('2013_price_avg')

    
combined_data['price_avg_this_year'] = combined_data['2000_price_avg'] + combined_data['2001_price_avg'] + combined_data['2002_price_avg'] + combined_data[
        '2003_price_avg'] + combined_data['2004_price_avg'] + combined_data['2005_price_avg'] + combined_data['2006_price_avg'] + combined_data[
        '2007_price_avg'] + combined_data['2008_price_avg'] + combined_data['2009_price_avg'] + combined_data['2010_price_avg'] + combined_data[
        '2011_price_avg'] + combined_data['2012_price_avg'] + combined_data['2013_price_avg']

mask = combined_data['price_avg_this_year'] == 0
combined_data.drop(combined_data[mask].index, inplace=True)

# date_columns=['2000_price_avg', '2001_price_avg', '2002_price_avg', '2003_price_avg', '2004_price_avg', '2005_price_avg', '2006_price_avg', 
#               '2007_price_avg', '2008_price_avg', '2009_price_avg', '2010_price_avg', '2011_price_avg', '2012_price_avg', '2013_price_avg']

# for column in combined_data.columns:
#     if column in date_columns:
#         if condition_2000.any():
#             if '2000_price_avg' in date_columns:
#                 date_columns.remove('2000_price_avg')
#             combined_data.loc[condition_2000.any(), date_columns] = 0
#         elif condition_2001.any():
#             if '2001_price_avg' in date_columns:
#                 date_columns.remove('2001_price_avg')
#             combined_data.loc[condition_2001, date_columns] = 0
#         elif condition_2002.any():
#             if '2002_price_avg' in date_columns:
#                 date_columns.remove('2002_price_avg')
#             combined_data.loc[condition_2002, date_columns] = 0
#         elif condition_2003.any():
#             if '2003_price_avg' in date_columns:
#                 date_columns.remove('2003_price_avg')
#             combined_data.loc[condition_2003, date_columns] = 0
#         elif condition_2004.any():
#             if '2004_price_avg' in date_columns:
#                 date_columns.remove('2004_price_avg')
#             combined_data.loc[condition_2004, date_columns] = 0
#         elif condition_2005.any():
#             if '2005_price_avg' in date_columns:
#                 date_columns.remove('2005_price_avg')
#             combined_data.loc[condition_2005, date_columns] = 0
#         elif condition_2006.any():
#             if '2006_price_avg' in date_columns:
#                 date_columns.remove('2006_price_avg')
#             combined_data.loc[condition_2006, date_columns] = 0
#         elif condition_2007.any():
#             if '2007_price_avg' in date_columns:
#                 date_columns.remove('2007_price_avg')
#             combined_data.loc[condition_2007, date_columns] = 0
#         elif condition_2008.any():
#             if '2008_price_avg' in date_columns:
#                 date_columns.remove('2008_price_avg')
#             combined_data.loc[condition_2008, date_columns] = 0
#         elif condition_2009.any():
#             if '2009_price_avg' in date_columns:
#                 date_columns.remove('2009_price_avg')
#             combined_data.loc[condition_2009, date_columns] = 0
#         elif condition_2010.any():
#             if '2010_price_avg' in date_columns:
#                 date_columns.remove('2010_price_avg')
#             combined_data.loc[condition_2010, date_columns] = 0
#         elif condition_2011.any():
#             if '2011_price_avg' in date_columns:
#                 date_columns.remove('2011_price_avg')
#             combined_data.loc[condition_2011, date_columns] = 0
#         elif condition_2012.any():
#             if '2012_price_avg' in date_columns:
#                 date_columns.remove('2012_price_avg')
#             combined_data.loc[condition_2012, date_columns] = 0
#         elif condition_2013.any():
#             if '2013_price_avg' in date_columns:
#                 date_columns.remove('2013_price_avg')
#             combined_data.loc[condition_2013, date_columns] = 0

# Reindex the DataFrame:
combined_data = combined_data.reset_index(drop=True)

# Save the clean optimized DataFrame to a .csv file:
combined_data.to_csv('california_clean.csv', index=False)

print(combined_data)
# Replace values in columns 'A' and 'B' where the condition_2000 is True
# combined_data.loc[condition_2000, ['A', 'B']] = 0