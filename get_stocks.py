#!/usr/bin/env/ python3

import re
from robobrowser import RoboBrowser
import argparse
from terminaltables import AsciiTable
import datetime
import re
import sys

global USER_AGENT
global URL
global ALL
global NSE
global BSE
global SYMBOL

def set_url():
    global URL
    URL = 'https://in.finance.yahoo.com/'

def set_user_agent():
    global USER_AGENT
    USER_AGENT='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2783.2 Safari/537.36'

def parse_args():
    global ALL
    global NSE
    global BSE
    global SYMBOL
    
    ALL=False
    NSE=False
    BSE=False
    SYMBOL=''

    search_term=''

    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--searchterm', help='Search term')
    parser.add_argument('-a', '--all', help='Get all indices',  action="store_true", default=False)
    parser.add_argument('-n', '--nse', help='Get only NSE indices',  action="store_true", default=False)
    parser.add_argument('-b', '--bse', help='Get only BSE indices',  action="store_true", default=False)
    parser.add_argument('-s', '--symbol', help='Download csv file with specified symbol')

    args = parser.parse_args()

    if args.all:
        ALL=True
    if args.nse:
        NSE=True
    if args.bse:
        BSE=True
    if args.symbol:
        SYMBOL=args.symbol.upper()
    if args.searchterm:
        search_term = args.searchterm.upper()

    return search_term

def tabulate_results(browser, results_arr):
    s_results = browser.select('table.yui-dt tbody tr')
    for row in s_results:
       cols=row.select('td')
       if cols[2].text != 'NaN':
           if NSE:
               if cols[4].text == 'NSI':
                   results_arr.append ([len(results_arr), cols[0].text, cols[1].text, cols[2].text, cols[3].text, cols[4].text])
           if BSE:
               if cols[4].text == 'BSE':
                   results_arr.append ([len(results_arr), cols[0].text, cols[1].text, cols[2].text, cols[3].text, cols[4].text])
           if not BSE and not NSE:
               results_arr.append ([len(results_arr), cols[0].text, cols[1].text, cols[2].text, cols[3].text, cols[4].text])
    return results_arr 

def maybe_get_nextpage(browser):
    next_res = browser.select('div#pagination a')
    if next_res:
        if(len(next_res)==2):
            if next_res[0].text=='Next':
                return URL+next_res[0].get('href')
            else:
                return None
        elif(len(next_res)==4):
           if next_res[2].text=='Next':
                return URL+next_res[2].get('href')
           else:
                return None
    else:
        return None

def search_stock(browser, stock_name):
    if ALL:
        browser.open(URL+'lookup?s='+stock_name)
    else:
        browser.open(URL+'lookup?s='+stock_name)
        selection_types = browser.select('ul.yui-nav li a')
        all_link=URL+selection_types[0].get('href')
        stocks_link=URL+selection_types[1].get('href')
        mutual_funds_link=URL+selection_types[2].get('href')
        etfs_link=URL+selection_types[3].get('href')
        indices_link=URL+selection_types[4].get('href')
        futures_funds_link=URL+selection_types[5].get('href')
        currencies_link=URL+selection_types[6].get('href')
        browser.open(stocks_link)
    return browser

def pretty_print(data):
    table = AsciiTable(data)
    table.inner_heading_row_border = True
    table.inner_row_border = False
    print (table.table)

def prompt_for_input(results_arr):
    sno = int(input('Select serial number: '))
    stock_symbol=results_arr[sno][1]
    return stock_symbol
    
def download_data(stock_symbol):
    global SYMBOL
    browser = RoboBrowser(history=True,
                          parser='lxml',
                          user_agent=USER_AGENT)
    now = datetime.datetime.now()
    current_year = now.year
    old_year = current_year - 20
    current_year = str(current_year)
    old_year = str(old_year)
    csv_url='http://real-chart.finance.yahoo.com/table.csv?s='+stock_symbol+'&d=6&e=2&f='+current_year+'&g=d&a=0&b=1&c='+old_year+'&ignore=.csv'
    file_name=stock_symbol+'.csv'
    request = browser.session.get(csv_url, stream=True)
    if re.search('.*csv.*',request.headers['Content-Type']):
        print ('Downloading %s.csv' % stock_symbol)
        with open(file_name, "wb") as csv_file:
            csv_file.write(request.content)
        return stock_symbol
    elif SYMBOL:
       SYMBOL=''
       print ('CSV file for %s not found' % stock_symbol)
       get_table(stock_symbol)
    else:
       print ('CSV file for %s not found' % stock_symbol)

def get_table(search_term):
    print('Searching for %s' % search_term)
    set_url()

    browser = RoboBrowser(history=True,
                          parser='lxml',
                          user_agent=USER_AGENT)


    browser = search_stock(browser, search_term)

    results_arr = [['S.No.', 'Symbol','Name','Last Trade','Type','Exchange']]
    results_arr = tabulate_results(browser, results_arr)
    next_page=maybe_get_nextpage(browser)

    while next_page is not None:
        browser.open(next_page)
        results_arr=tabulate_results(browser, results_arr)
        next_page=maybe_get_nextpage(browser)

    if (len(results_arr)>1):
        pretty_print (results_arr)
        stock_symbol = prompt_for_input(results_arr)
        download_data(stock_symbol)
    else:
        print ('Data for %s not found' % search_term)
        sys.exit()
    return stock_symbol

if __name__=='__main__':
    set_user_agent()
    search_term=parse_args()
    if SYMBOL:
        download_data(SYMBOL)
    else:
        get_table(search_term)
