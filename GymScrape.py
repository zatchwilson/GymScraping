import requests
import sqlite3
import logging
from bs4 import BeautifulSoup
from datetime import datetime

logging.basicConfig(filename="C:/Python/GymScraping/app.log", format='%(name)s - %(levelname)s - %(message)s')
URL = "https://connect2concepts.com/connect2/?type=circle&key=c79d721a-d9cd-4ece-89b3-804fb3d0deba"
rq = requests.get(URL, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0"})

soup = BeautifulSoup(rq.content, "html.parser")
results = soup.find(id="container")
counts = results.find_all("div", attrs={"style": "text-align:center;"})

for c in counts:
    if "Core" in c.text:
        coreText = c.text

startIndex = 0
sub_s = ""
recentNum = False
s_length = len(coreText)

for x in range(0,s_length):
    if recentNum:
        if coreText[x].isnumeric():
            sub_s += coreText[x]
        else:
            break
    else:
        if coreText[x].isnumeric():
            sub_s += coreText[x]
            recentNum = True
            
colonIndex = coreText.find(':')

time_s = coreText[s_length-8:s_length]
date_s = coreText[s_length-19:s_length-9]
gym_count = coreText[colonIndex+2:s_length-28]
date_time = coreText[s_length-19: s_length]
weekday = datetime.now().isoweekday()


con = sqlite3.connect("C:/sqlite/testDB.db")

cur = con.cursor()

data = (
    {"date_time": date_time, "date": date_s, "time": time_s, "capacity": gym_count, "weekday": weekday}
)

try:
    cur.execute("INSERT INTO gym_capacity VALUES(:date_time, :date, :time, :capacity, :weekday)", data)
    con.commit()
except:
    logging.warning("Entry already exists - " + date_time + ". Logged at " + datetime.now().strftime("%m/%d/%Y %H:%M:%S"))