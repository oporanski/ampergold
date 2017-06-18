#!/usr/bin/env python
import datetime
import MySQLdb
#import json
from datetime import datetime
from poloniex import Poloniex, Coach
import sys

#######GLOBALS##########
DEBUG = True
markets = ["USDT_REP", "BTC_XVC", "BTC_PINK", "BTC_SYS", "BTC_EMC2", "BTC_RADS", "BTC_SC", "BTC_MAID", \
        "BTC_GNT", "BTC_BCN", "BTC_REP", "BTC_BCY", "BTC_GNO", "XMR_NXT", "USDT_ZEC", "BTC_FCT", "USDT_ETH", \
        "USDT_BTC", "BTC_LBC", "BTC_DCR", "USDT_ETC", "BTC_AMP", "BTC_XPM", "BTC_NXT", "BTC_VTC", "ETH_STEEM", \
        "XMR_BLK", "BTC_PASC", "XMR_ZEC", "BTC_GRC", "BTC_NXC", "BTC_BTCD", "BTC_LTC", "BTC_DASH", "BTC_NAUT", \
        "ETH_ZEC", "BTC_ZEC", "BTC_BURST", "BTC_BELA", "BTC_STEEM", "BTC_ETC", "BTC_ETH", "BTC_HUC", "BTC_STRAT", \
        "BTC_LSK", "BTC_EXP", "BTC_CLAM", "ETH_REP", "XMR_DASH", "USDT_DASH", "BTC_BLK", "BTC_XRP", "USDT_NXT", \
        "BTC_NEOS", "BTC_BTS", "BTC_DOGE", "ETH_GNT", "BTC_SBD", "ETH_GNO", "BTC_XCP", "USDT_LTC", "BTC_BTM", \
        "USDT_XMR", "ETH_LSK", "BTC_OMNI", "BTC_NAV", "BTC_FLDC", "BTC_XBC", "BTC_DGB", "BTC_NOTE", "XMR_BTCD", \
        "BTC_VRC", "BTC_RIC", "XMR_MAID", "BTC_STR", "BTC_POT", "BTC_XMR", "BTC_SJCX", "BTC_VIA", "BTC_XEM", \
        "BTC_NMC", "ETH_ETC", "XMR_LTC", "BTC_ARDR", "BTC_FLO", "USDT_XRP", "BTC_GAME", "BTC_PPC", "XMR_BCN", "USDT_STR"]

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
log("Start")
polo = Coach()

public = Poloniex(coach=polo)
private = Poloniex("NQVE5PYF-CPG3TGTY-E21OLYUG-9YT229HG", \
          "0cda3c2e4ca65a1a5ca9969e887d10d3605ab5f9544ce308145d47d701e49dfb616fa7a67e6b98bc1f30ef83b45e8978f5e2ba13d213002d8e067fded940cd38", \
          coach=polo)
ticker = public.returnTicker()
m = ticker.keys()

#for i in m:
#    sys.stdout.write('"')
#    sys.stdout.write(str(i))
#    sys.stdout.write('", ')

for market in markets: 
    data = ticker[market]
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
    #log(+ ": " + ','.join(insert))
    write_ticker_data_to_db(str(market), insert)

log("End")
