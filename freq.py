#!/usr/local/bin/python3

from bs4 import BeautifulSoup
import urllib.request
import datetime
import collections
from tabulate import tabulate
from terminaltables import AsciiTable

def read_natstate_month(month, year):
    url = "http://myarkansaslottery.com/games/natural-state-jackpot/did-i-win-date?date[value][year]=" + str(year) + "&date[value][month]=" + str(month)
    content=urllib.request.urlopen(url).read()
    soup = BeautifulSoup(content, "html.parser")
    table = soup.find("table", attrs={ "class" : "views-table sticky-enabled"})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')

    drawings = {}

    for row in rows:
        numbers = []
        data = row.find_all('td')
        date = data[0].get_text().strip()
#        date = datetime.strptime(data[0].get_text().strip(), '%m/%d/%Y')
#        print(date)
        divs = data[1].find_all('div')
        for div in divs:
            numbers.append(div.get_text())
        drawings[date] = numbers

    return(drawings)

def read_lucky_month(month,year):
    url = "http://myarkansaslottery.com/games/luckyforlife/did-i-win-by-date?date[value][year]=" + str(year) + "&date[value][month]=" + str(month)
    content=urllib.request.urlopen(url).read()
    soup = BeautifulSoup(content, "html.parser")
    table = soup.find("table", attrs={ "class" : "views-table"})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')

    drawings = {}

    for row in rows:
        numbers = []
        data = row.find_all('td')
        date = data[0].get_text().strip()
        spans = data[1].find_all('span')
        for span in spans:
            numbers.append(span.get_text())
        numbers.append(data[2].get_text().strip())
        drawings[date] = numbers
#    print(drawings)
    return(drawings)

def read_natstate():
    start_year = 2012
    this_year = datetime.datetime.today().year
    all_natstate_drawings = {}
    for year in range(this_year, start_year - 1, -1):
        for month in range(12, 0, -1):
#            print('{0}/{1}'.format(month,year))
            try:
                drawings = read_natstate_month(month, year)
                all_natstate_drawings.update(drawings)
            except:
                pass
    return(all_natstate_drawings)

def read_lucky():
    start_year = 2015
    this_year = datetime.datetime.today().year
    all_lucky_drawings = {}
    for year in range(this_year, start_year - 1, -1):
        for month in range(12, 0, -1):
#            print('{0}/{1}'.format(month,year))
            try:
                drawings = read_lucky_month(month, year)
                all_lucky_drawings.update(drawings)
            except:
                pass
#    print(all_lucky_drawings)
    return(all_lucky_drawings)

def natstate_freq(drawings):
    all_values = [] # all numbers drawn in a list
    indiv_values = [ [], [], [], [], [] ] # list of lists with numbers drawn by place (1st, 2nd, etc.)
    indiv_counter_tuples = []
    for key, values in drawings.items():
        incr = 0
        for value in values:
            indiv_values[incr].append(value)
            incr += 1
    for list in indiv_values:
        indiv_counter = collections.Counter(list)
        indiv_counter_tuples.append(indiv_counter.most_common(5))
        all_values += list
    whole_counter = collections.Counter(all_values)
    whole_counter_tuples = whole_counter.most_common(10)
    return(whole_counter_tuples, indiv_counter_tuples)

def lucky_freq(drawings):
    all_values = [] # all numbers drawn in a list
    indiv_values = [ [], [], [], [], [], [] ] # list of lists with numbers drawn by place (1st, 2nd, etc.)
    indiv_counter_tuples = []
    for key, values in drawings.items():
        incr = 0
        for value in values:
            indiv_values[incr].append(value)
            incr += 1
    for list in indiv_values:
        indiv_counter = collections.Counter(list)
        indiv_counter_tuples.append(indiv_counter.most_common(5))
        all_values += list
    whole_counter = collections.Counter(all_values)
    whole_counter_tuples = whole_counter.most_common(10)
    return(whole_counter_tuples, indiv_counter_tuples)

def print_natstate(whole, indiv):
    print ("\nNatural State Lottery\n")
    print ("Top 10 Overall Values by Frequency")
    whole_with_headers = [('Number','Frequency')] + whole
    # AsciiTable has no problem with the list of tuples
    overall_table = AsciiTable(whole_with_headers)
    print(overall_table.table)
    print ("\nTop 5 Overall Place Values by Frequency")
    indiv_transposed = [['1st Num','Freq','2nd Num','Freq','3rd Num','Freq','4th Num','Freq','5th Num','Freq']]
    # Transpose the list of list of tuples to something printable by AsciiTable
    for i in range(0,5):
        temp_list = []
        for j in range(0,5):
            temp_list.append(indiv[j][i][0])
            temp_list.append(indiv[j][i][1])
        indiv_transposed.append(temp_list)
    indiv_transposed_table = AsciiTable(indiv_transposed)
    print(indiv_transposed_table.table)

def print_lucky(whole, indiv):
    print ("\nLucky for Life\n")
    print ("Top 10 Overall Values by Frequency")
    whole_with_headers = [('Number','Frequency')] + whole
    # AsciiTable has no problem with the list of tuples
    overall_table = AsciiTable(whole_with_headers)
    print(overall_table.table)
    print ("\nTop 5 Overall Place Values by Frequency")
    indiv_transposed = [['1st Num','Freq','2nd Num','Freq','3rd Num','Freq','4th Num','Freq','5th Num','Freq','Lucky','Freq']]
    # Transpose the list of list of tuples to something printable by AsciiTable
    for i in range(0,5):
        temp_list = []
        for j in range(0,6):
            temp_list.append(indiv[j][i][0])
            temp_list.append(indiv[j][i][1])
        indiv_transposed.append(temp_list)
    indiv_transposed_table = AsciiTable(indiv_transposed)
    print(indiv_transposed_table.table)

def main():
    nat_state_drawings = read_natstate()
    natwhole, natindiv = natstate_freq(nat_state_drawings)
    print_natstate(natwhole, natindiv)
    lucky_drawings = read_lucky()
    luckywhole, luckyindiv = lucky_freq(lucky_drawings)
    print_lucky(luckywhole, luckyindiv)

main()
