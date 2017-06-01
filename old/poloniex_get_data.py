#!/usr/bin/env python
import datetime
import dateutil.parser
import requests
import MySQLdb
from datetime import datetime, timedelta
from lxml import html
#from poloniex import Poloniex
from poloniex import Poloniex, Coach
#######GLOBALS##########
ROOT_URL = 'https://poloniex.com'
INDEX_URL = ROOT_URL + '/exchange#btc_eth'
CONN = MySQLdb.connect(host="localhost",user="root",passwd="PKjsizw02k",db="poloniex")
DEBUG = True

#######FUNCTIONS##########
def get_web_page_data():
    response = requests.get(INDEX_URL)
    tree = html.fromstring(response.content)
    users_online = tree.xpath('//span[@id="usersOnline"]/text()')[0]
    server_time = tree.xpath('//span[@id="serverTime"]/text()')[0]
    return (users_online, server_time)

def write_users_to_db(usersOnline):
    x = CONN.cursor()
    try:
	x.execute("""INSERT INTO `Users_Online`(`Number_Of_Users`) VALUES (%s)""",(usersOnline))
	CONN.commit()
    except:
	CONN.rollback()


#######HELPERS##########
def get_date_time(s):
    d = dateutil.parser.parse(s)
    return d

def log(s):
    if DEBUG:
        print datetime.now(), s

#######MAIN##########
polo = Coach()

public = Poloniex(coach=polo)
private = Poloniex("NQVE5PYF-CPG3TGTY-E21OLYUG-9YT229HG", \
		  "0cda3c2e4ca65a1a5ca9969e887d10d3605ab5f9544ce308145d47d701e49dfb616fa7a67e6b98bc1f30ef83b45e8978f5e2ba13d213002d8e067fded940cd38", \
		  coach=polo)

balance = private('returnBalances')
print("I have %s BTC!" % balance['BTC'])

print(public.returnTicker()['BTC_ETH'])
print(public.returnTicker()['USDT_BTC'])
print(public.return24Volume()['BTC'])

log("**********************************************************")
#get number of users online 
users_online, server_time = get_web_page_data()
log('Users Online: ' + str(users_online))
log('Server Time: ' + str(server_time))
server_time = get_date_time(server_time)
print (type(server_time))

#write_users_to_db(usersOnline)


CONN.close()
