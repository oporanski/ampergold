#!/usr/bin/env python
import datetime
#import MySQLdb
import json
import urllib2
from datetime import datetime

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
        print (str(datetime.now()) + " - " +  s)

#######MAIN##########
log("**********************************************************")

url = "https://api.coinmarketcap.com/v1/ticker/"
data = json.load(urllib2.urlopen(url))
print(str(data[0]["id"]))
print("\n")
print("one entry:" + str(data[0]))

#for market in markets: 
#    data = ticker[market]
#    last = data["last"]
#    lowest_ask = data["lowestAsk"]
#    highest_bid = data["highestBid"]
#    percentchange = data["percentChange"]
#    base_volume = data["baseVolume"]
#    quote_volume = data["quoteVolume"]
#    is_frozen = data["isFrozen"]
#    high24hr = data["high24hr"]
#    low24hr = data["low24hr"]
#    insert = last, lowest_ask, highest_bid, percentchange, base_volume, quote_volume, is_frozen, high24hr, low24hr
#    log(str(market)+ ": " + ','.join(insert))
#write_ticker_data_to_db("BTC_PASC", insert)

