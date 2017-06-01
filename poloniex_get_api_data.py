#!/usr/bin/env python
import datetime
import MySQLdb
#import json
from datetime import datetime
from poloniex import Poloniex, Coach

#######GLOBALS##########
DEBUG = True

#######FUNCTIONS##########
def write_ticker_data_to_db(table, insert):
    conn = MySQLdb.connect(host="localhost",user="root",passwd="PKjsizw02k",db="poloniex")
    x = conn.cursor()
    sql = "INSERT INTO " + table + " (`Last`, `LowestAsk`, `HighestBid`, `PercentChange`, `BaseVolume`, " + \
	"`QuoteVolume`, `IsFrozen`, `24hrHigh`, `24hrLow`) VALUES (" + ','.join(insert) + ")"
    #print(sql)
    try:
	x.execute(sql)
	conn.commit()
    except:
	conn.rollback()
    conn.close()


#######HELPERS##########
def get_date_time(s):
    d = dateutil.parser.parse(s)
    return d

def log(s):
    if DEBUG:
        print datetime.now(), s

#######MAIN##########
log("**********************************************************")
polo = Coach()

public = Poloniex(coach=polo)
private = Poloniex("NQVE5PYF-CPG3TGTY-E21OLYUG-9YT229HG", \
		  "0cda3c2e4ca65a1a5ca9969e887d10d3605ab5f9544ce308145d47d701e49dfb616fa7a67e6b98bc1f30ef83b45e8978f5e2ba13d213002d8e067fded940cd38", \
		  coach=polo)
#BTC_PASC
data = public.returnTicker()['BTC_PASC']
last = data["last"]
lowest_ask = data["lowestAsk"]
highest_bid = data["highestBid"]
percentchange = data["percentChange"]
base_volume = data["baseVolume"]
quote_volume = data["quoteVolume"]
is_frozen = data["isFrozen"]
high24hr = data["high24hr"]
low24hr = data["low24hr"]

insert = last, lowest_ask, highest_bid, percentchange, base_volume, quote_volume, is_frozen, high24hr, low24hr
log("BTC_PASC: " + ','.join(insert))
write_ticker_data_to_db("BTC_PASC", insert)

#USDT_BTC
data = public.returnTicker()['USDT_BTC']
last = data["last"]
lowest_ask = data["lowestAsk"]
highest_bid = data["highestBid"]
percentchange = data["percentChange"]
base_volume = data["baseVolume"]
quote_volume = data["quoteVolume"]
is_frozen = data["isFrozen"]
high24hr = data["high24hr"]
low24hr = data["low24hr"]

insert = last, lowest_ask, highest_bid, percentchange, base_volume, quote_volume, is_frozen, high24hr, low24hr
log("USDT_BTC: " + ','.join(insert))
write_ticker_data_to_db("USDT_BTC", insert)
