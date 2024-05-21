from pyjstat import pyjstat
import requests
import pandas as pd
import os
os.makedirs('data', exist_ok=True)
rename_dict = {
    'Czechia': 'Czech Rep.',
    'European Union - 27 countries (from 2020)': 'EU27',
    'Türkiye': 'Turkey'
}
flag_codes = {
    'Austria': ':at:',
    'Belgium': ':be:',
    'Bulgaria': ':bg:',
    'Croatia': ':hr:',
    'Cyprus': ':cy:',
    'Czech Rep.': ':cz:',
    'Denmark': ':dk:',
    'EU27': ':eu:',
    'Estonia': ':ee:',
    'Finland': ':fi:',
    'France': ':fr:',
    'Germany': ':de:',
    'Greece': ':gr:',
    'Hungary': ':hu:',
    'Ireland': ':ie:',
    'Italy': ':it:',
    'Latvia': ':lv:',
    'Lithuania': ':lt:',
    'Luxembourg': ':lu:',
    'Malta': ':mt:',
    'Netherlands': ':nl:',
    'Poland': ':pl:',
    'Portugal': ':pt:',
    'Romania': ':ro:',
    'Slovakia': ':sk:',
    'Slovenia': ':si:',
    'Spain': ':es:',
    'Sweden': ':se:'
}

#Life expectancy over time EU27 (2020)
dataset = pyjstat.Dataset.read('https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/demo_mlexpec?lang=en&lastTimePeriod=64&sex=T&sex=M&sex=F&age=Y_LT1&geo=EU27_2020')
df = dataset.write('dataframe')
df.replace(rename_dict, inplace=True)
df_new = df.pivot(index='Sex', columns='Time', values='value')
df_new.to_csv('data/Eurostat_Life_Expectancy_EU27_Overall.csv', index=True)

#Life expectancy latest year by country
dataset = pyjstat.Dataset.read('https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/demo_mlexpec?format=JSON&lang=en&freq=A&unit=YR&sex=T&age=Y_LT1&geo=EU27_2020&geo=BE&geo=BG&geo=CZ&geo=DK&geo=DE&geo=EE&geo=IE&geo=EL&geo=ES&geo=FR&geo=HR&geo=IT&geo=CY&geo=LV&geo=LT&geo=LU&geo=HU&geo=MT&geo=NL&geo=AT&geo=PL&geo=PT&geo=RO&geo=SI&geo=SK&geo=FI&geo=SE&lastTimePeriod=1')
df = dataset.write('dataframe')
df.replace(rename_dict, inplace=True)
df_new = df.pivot(index='Geopolitical entity (reporting)', columns='Time', values='value')
df_new.dropna(inplace=True)
df_new.to_csv('data/Eurostat_Life_Expectancy_Country_Latest_Year.csv', index=True)
df_new.index = [f"{flag_codes[country]} {country}" for country in df_new.index]
df_new.to_csv('data/Eurostat_Life_Expectancy_Country_Latest_Year_Flags.csv', index=True)

#Life expectancy latest year over time by country
dataset = pyjstat.Dataset.read('https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/demo_mlexpec?format=JSON&lang=en&freq=A&unit=YR&sex=T&age=Y_LT1&geo=EU27_2020&geo=BE&geo=BG&geo=CZ&geo=DK&geo=DE&geo=EE&geo=IE&geo=EL&geo=ES&geo=FR&geo=HR&geo=IT&geo=CY&geo=LV&geo=LT&geo=LU&geo=HU&geo=MT&geo=NL&geo=AT&geo=PL&geo=PT&geo=RO&geo=SI&geo=SK&geo=FI&geo=SE&lastTimePeriod=22')
df = dataset.write('dataframe')
df.replace(rename_dict, inplace=True)
df_new = df.pivot(index='Geopolitical entity (reporting)', columns='Time', values='value')
df_new['Change since 2002'] = df_new['2023'] - df_new['2002']
df_new['Change since 2002 in %'] = (df_new['2023'] - df_new['2002'])/df_new['2002']*100
df_new['Change since 2019'] = df_new['2023'] - df_new['2019']
df_new['Change since 2019 in %'] = (df_new['2023'] - df_new['2019'])/(df_new['2019'])*100
df_new = df_new[df_new['2023'].notna()]
df_new.to_csv('data/Eurostat_Life_Expectancy_Country_Overall_Time.csv', index=True)
