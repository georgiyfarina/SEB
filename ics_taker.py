import csv
import email
import imaplib
import urllib
from datetime import datetime
from email.utils import parseaddr
from nntplib import decode_header
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
import ics

import time

def ics_taker(email_address, password):
    # FIrst part to get to the home of icorsi
    PATH = "C://Users//Gabri//Documents//chromedriver_win32//chromedriver.exe"
    serv = Service(PATH)
    driver = webdriver.Chrome(service=serv)

    driver.get("https://www.icorsi.ch/login/index.php")

    search = driver.find_element(By.XPATH, value='/html/body/div[1]/div[2]/div/div/div/div/div/div/div[2]/div/a')
    search.click()

    search = driver.find_element(By.ID, value='username')
    search.send_keys(email_address)

    search = driver.find_element(By.ID, value='password')
    search.send_keys(password)

    search = driver.find_element(By.TAG_NAME, value='button')
    search.click()
    time.sleep(5)
    # --------------------------------------------------------
    cal_button = driver.find_element(By.XPATH, value='//*[@id="region-main"]/div[1]/div/div/div/div[1]/div/div/div[1]/a')
    cal_button.click()
    time.sleep(1)

    export = driver.find_element(By.XPATH, value='//*[@id="region-main"]/div/div/div[2]/div[1]')
    export.click()
    time.sleep(1)

    all = driver.find_element(By.XPATH, value='//*[@id="id_events_exportevents_all"]')
    all.click()
    time.sleep(1)

    week = driver.find_element(By.XPATH, value='// *[ @ id = "id_period_timeperiod_weeknow"]')
    week.click()
    time.sleep(1)

    get_url = driver.find_element(By.XPATH, value='//*[@id="id_generateurl"]')
    get_url.click()
    time.sleep(5)

    urll = driver.find_element(By.XPATH, value='// *[ @ id = "region-main"] / div / div / div')
    print(urll.text)
    url = urll.text.split(":", 1)
    url = url[1].strip()
    print(url)

    ics_file = requests.get(url)

    calendar = ics.Calendar(ics_file.text)

    for event in calendar.events:
        print(f"Event: {event.name}")
        print(f"{event.categories}")
        print(f"{event.extra}")
        print(f"Starts: {event.begin}")
        print(f"Ends: {event.end}")
        print("-" * 20)

# crea il tuo main
