#!/usr/local/bin/python3

from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime
#import collections
#from tabulate import tabulate
#from terminaltables import AsciiTable
import sqlite3

def read_natstate_month(month, year, db):
    url = "http://myarkansaslottery.com/games/natural-state-jackpot/did-i-win-date?date[value][year]=" + str(year) + "&date[value][month]=" + str(month)
    content=urllib.request.urlopen(url).read()
    soup = BeautifulSoup(content, "html.parser")
    table = soup.find("table", attrs={ "class" : "views-table sticky-enabled"})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')

    for row in rows:
        drawing = []
        data = row.find_all('td')
        drawing.append(datetime.strptime(data[0].get_text().strip(), '%m/%d/%Y').date())
        divs = data[1].find_all('div')
        for div in divs:
            drawing.append(int(div.get_text()))
        print(drawing)
        db.execute('''INSERT INTO natstate (date, ball1, ball2, ball3, ball4, ball5)
                   VALUES(drawing[0], drawing[1], drawing[2], drawing[3], drawing[4], drawing[5])''')

def read_natstate(db):
    start_year = 2017
    this_year = datetime.today().year
    all_natstate_drawings = {}
    for year in range(this_year, start_year - 1, -1):
        for month in range(12, 0, -1):
#            print('{0}/{1}'.format(month,year))
            try:
                drawings = read_natstate_month(month, year, db)
                all_natstate_drawings.update(drawings)
            except:
                pass

def main():
    conn = sqlite3.connect('drawings.sqlite')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS natstate (date date PRIMARY KEY UNIQUE NOT NULL,
              ball1 integer NOT NULL, ball2 integer NOT NULL, ball3 integer NOT NULL,
              ball4 integer NOT NULL, ball5 integer NOT NULL)''')

    read_natstate(c)

main()
