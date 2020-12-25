import argparse
import json
import time
import requests
import io
import datetime
from bs4 import BeautifulSoup

DORKS_FILE = "GoogleDorksFullList.txt"
DORKS_FILE2 = "GoogleDorksListRecentlyAdded.txt"

FullList = []
NewList = []

def fixDate(year, month ,day):
    stringDate = str(year) + "-"

    if(month<10):
        stringDate += "0" + str(month) + "-"
    else:
        stringDate += str(month) + "-"

    if(day<10):
        stringDate += "0" + str(day)
    else:
        stringDate += str(day)

    return stringDate

today = datetime.datetime.now()
daysBefore = datetime.timedelta(days=30)
dateToGoBack = today - daysBefore
monthbefore = fixDate(dateToGoBack.year, dateToGoBack.month, dateToGoBack.day)

def list_to_file(type,list):
    with io.open(type+".txt", 'w',encoding="utf-8") as f:
        for l in list:
            f.write(l + '\n')
    f.close()
    print(type + " writing into txt file...")

def retrieve_google_dorks():
    url = "https://www.exploit-db.com/google-hacking-database"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "deflate, gzip, br",
        "Accept-Language": "en-US",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
        "X-Requested-With": "XMLHttpRequest",
    }
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code != 200:
        print("Error retrieving google dorks from: {url}")
        return
    json_response = response.json()
    json_dorks = json_response["data"]
    totaldorks = 0
    newdorks = 0

    for i in json_dorks:
        totaldorks += 1
        soup = BeautifulSoup(i["url_title"], "html.parser")
        extracted_dork = soup.find("a").contents[0]
        print("Dork #" + str(totaldorks) + "\t" + extracted_dork)
        FullList.append(extracted_dork) #this list is for all the dorks collected
        if(monthbefore < i["date"]): #comparing with 1 month before date
            newdorks += 1
            NewList.append(extracted_dork)  # this list is for all the dorks collected

    list_to_file("GoogleDorksFullList",FullList)
    list_to_file("GoogleDorksListRecentlyAdded", NewList)

    print("Total Google Dorks " + str(totaldorks))
    print("Newly Added Google Dorks " + str(newdorks))

retrieve_google_dorks()

