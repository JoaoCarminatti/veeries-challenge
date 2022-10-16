import io
import schedule
import time
import requests
import pandas as pd

baseAPIUrl = 'https://apps.fas.usda.gov/OpenData/api/esr'
API_KEY = '3a9ed7bf-8bb8-4858-8eb2-dbd5ec1a4663'

def startRoutine():
    print("created routine")
    countries = getCountries()
    chinaCode, mexicoCode = extractCountriesCode(countries)
    commodities = getCommodities()
    soyCode = extractCommoditiesCode(commodities)
    marketYear = getMarketYear()
    finalResultsMexico = getFinalResultsMexico(soyCode, mexicoCode, marketYear)
    finalResultsChina = getFinalResultsChina(soyCode, chinaCode, marketYear)
    df = pd.DataFrame.from_records(finalResultsMexico)
    df = pd.DataFrame.from_records(finalResultsChina)
    df.to_csv('outputfile.csv')

    print(marketYear)
    print(f'{soyCode}')
    print(f'{chinaCode} {mexicoCode}')
    print(finalResultsMexico)
    print(finalResultsChina)

def getCountries():
    headers_dict = {"API_KEY": f'{API_KEY}'}
    response = requests.get(url= f'{baseAPIUrl}/countries', headers=headers_dict)
    data = response.json()
    return data

def getCommodities():
    headers_dict = {"API_KEY": f'{API_KEY}'}
    response = requests.get(url= f'{baseAPIUrl}/commodities', headers=headers_dict)
    data = response.json()
    return data

def getMarketYear():
    year = int(input("Please, insert the Market Year: "))
    return year

def getFinalResultsMexico(soyCode, mexicoCode, marketYear):
    headers_dict = {"API_KEY": f'{API_KEY}'}
    response = requests.get(url= f'{baseAPIUrl}/exports/commodityCode/{soyCode}/countryCode/{mexicoCode}/marketYear/{marketYear}', headers=headers_dict)
    data = response.json()
    return data

def getFinalResultsChina(soyCode, chinaCode, marketYear):
    headers_dict = {"API_KEY": f'{API_KEY}'}
    response = requests.get(url= f'{baseAPIUrl}/exports/commodityCode/{soyCode}/countryCode/{chinaCode}/marketYear/{marketYear}', headers=headers_dict)
    data = response.json()
    return data


def extractCommoditiesCode(commodities):
    soyCode = ''

    for commodity in commodities:
        if commodity["commodityName"].strip() == "Soybean Oil":
            soyCode = commodity["commodityCode"]
    return soyCode        


def extractCountriesCode(countries):
    chinaCode = ''
    mexicoCode = ''
    
    for country in countries:
        if country["countryName"].strip() == "CHINA":
            chinaCode = country["countryCode"]
        if country["countryName"].strip() == "MEXICO":
            mexicoCode = country["countryCode"]
    return chinaCode, mexicoCode




schedule.every(2).seconds.do(startRoutine)

while 1:
    schedule.run_pending()
    time.sleep(1)

