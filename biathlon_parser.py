# Import libraries
import pandas as pd
from pandas.core.frame import DataFrame
import numpy as np
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

# Functions
def get_sec(time_str):
    if time_str == 'DNS' or time_str == 'DNF' or time_str == 'LAP':
        return float(0)
    else:
        time_str = time_str.replace('+', '')
        time_str = time_str.split('.', 1)
        time_str_main = time_str[0]
        ms = time_str[1]
        if 1 <= len(time_str_main) <= 2:
            m = 0
            s = time_str_main
        else:
            m, s = time_str_main.split(':')
        return float(m) * 60 + float(s) + float(ms) * 0.1

def get_full_time(time):
    if time == leaderTime:
        return str(leaderTime)
    elif time == 0:
        return("NA")
    else:
        return leaderTime + time

# Variables
url = 'https://www.biathlonworld.com/calendar/bmw-ibu-world-cups/season/2021/'
mainDF = pd.DataFrame()
outRoute = r'route_to_export_file'

# Parse flow

# Open URL and expand all the stages
driver = webdriver.Chrome(executable_path = r'route_to_chromedriver')
page = driver.get(url)
acceptButton = driver.find_element_by_id('cookieChoiceDismiss')
acceptButton.click()
time.sleep(1)
toggles = driver.find_elements_by_xpath('//*/h3/a')
for i in toggles:
    i.click()
    time.sleep(1)

# Collect stages
stages = driver.find_elements_by_xpath('//*[@id="dcm-competitionList"]/li/a[1]')
stagesLinks = []
for i in stages:
    link = i.get_attribute("href")
    if 'relay' in link or 'women' in link:
        continue
    else:
        stagesLinks =  stagesLinks + [link]

# Parse stages
for i in stagesLinks:
    driver.get(i)
    time.sleep(2)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ibuCompetitionDetailApp"]/div/div/section/div/div[2]/a')))
    showMore = driver.find_element_by_xpath('//*[@id="ibuCompetitionDetailApp"]/div/div/section/div/div[2]/a')
    showMore.click()
    fullHtml = driver.page_source
    soup = BeautifulSoup(fullHtml,'html.parser')
    htmlTable = soup.find('table', { 'class' : 'dcm-table dcm-athletes-table' })
    dfList = pd.read_html(str(htmlTable))
    df = pd.DataFrame(np.concatenate(dfList))
    leaderTime = df.iloc[0][6]
    leaderTime = get_sec(leaderTime)
    df[6] = df[6].apply(get_sec)
    df[6] = df[6].apply(get_full_time)
    df = df[[2, 6]]
    mainDF = mainDF.append(df)
    time.sleep(4)

# Export results
mainDF.to_excel(outRoute)