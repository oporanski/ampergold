#!/usr/bin/env python
import datetime
import requests
import MySQLdb
import smtplib
import operator

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

#######GLOBALS########################################################################
FROM = "ampergold@starelamy.org"
TO = ["oporanski@gmail.com", "marcin.opinc@gmail.com"]
#TO = ["oporanski@gmail.com"]
SUBJECT = "Average number of users Poloniex"
SERVER = "localhost"
DEBUG = True

######################################################################################

#######FUNCTIONS##########
def get_market(sqlq):
    conn = MySQLdb.connect(host="localhost",user="root",passwd="PKjsizw02k",db="poloniex")
    #log(sqlq)
    x = conn.cursor()
    try:
	x.execute(sqlq)
	rows = x.fetchall()
    except:
	conn.rollback()
    #log("Number of records: " + str(len(rows)))
    ret = []
    for row in rows:
	ret = row
    conn.close()
    return ret


def get_average_users(sqlq):
    conn = MySQLdb.connect(host="localhost",user="root",passwd="PKjsizw02k",db="poloniex")
    #log(sqlq)
    x = conn.cursor()
    try:
	x.execute(sqlq)
	rows = x.fetchall()
    except:
	conn.rollback()
    #log("Number of records: " + str(len(rows)))
    avg_users = 0
    for row in rows:
	#log("Value:" + row[0])
	avg_users += int(row[0])
    avg_users = avg_users/len(rows)
    #log ("AVG:" + str(avg_users))
    conn.close()
    return avg_users

#def get_average_last_hour(sqlq):
#    conn = MySQLdb.connect(host="localhost",user="root",passwd="PKjsizw02k",db="poloniex")
#    #log(sqlq)
#    x = conn.cursor()
#    try:
#	x.execute(sqlq)
#	rows = x.fetchall()
#    except:
#	conn.rollback()
#    #log("Number of records: " + str(len(rows)))
#    avg_users = 0
#    for row in rows:
#	#log("Value:" + row[0])
#	avg_users += int(row[0])
#    avg_users = avg_users/len(rows)
#    #log ("AVG:" + str(avg_users))
#    conn.close()
#    return avg_users


#######HELPERS##########
def sendMail(FROM,TO,SUBJECT,HTML,SERVER):
    """Function sending email Input: FROM,TO,SUBJECT,TEXT,HTML,SERVER"""
    #write_date_of_last_notyfication(notyfiType)
    COMMASPACE = ', '
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = COMMASPACE.join(TO)
    part1 = MIMEText(HTML, 'html')
    msg.attach(part1)
    # Send the email via our own SMTP server.
    s = smtplib.SMTP(SERVER)
    s.sendmail(FROM, TO, msg.as_string())
    s.quit()

def getDateTimeFromISO8601String(s):
    d = dateutil.parser.parse(s)
    return d

def log(s):
    if DEBUG:
        print datetime.now(), s

#######MAIN##########
log("**********************************************************")
#get number of users avarage last hour 
sql_query = "SELECT `Number_Of_Users` FROM `Users_Online` WHERE `Time_Stamp` >= NOW() - INTERVAL 1 HOUR"
avg_hour_users = get_average_users(sql_query)
#log('Average last hour: '+ str(avg_hour_users))

#get number of users avarage last 24 hour 
sql_query = "SELECT `Number_Of_Users` FROM `Users_Online` WHERE `Time_Stamp` >= NOW() - INTERVAL 1 DAY"
avg_day_users = get_average_users(sql_query)
#log('Average last 24 hour: '+ str(avg_day_users))

#get number of users avarage 2 days ago hour 
sql_query = "SELECT `Number_Of_Users` FROM `Users_Online` WHERE `Time_Stamp` >= NOW() - INTERVAL 2 DAY AND `Time_Stamp` <= NOW() - INTERVAL 1 DAY"
avg_2day_users = get_average_users(sql_query)
#log('Average 2 days ago: '+ str(avg_day_users))

#get number of users avarage last week 
sql_query = "SELECT `Number_Of_Users` FROM `Users_Online` WHERE `Time_Stamp` >= NOW() - INTERVAL 1 WEEK"
avg_week_users = get_average_users(sql_query)
#log('Average last week: '+ str(avg_day_users))

#get number of users avarage 2 weeks ago hour 
sql_query = "SELECT `Number_Of_Users` FROM `Users_Online` WHERE `Time_Stamp` >= NOW() - INTERVAL 2 WEEK AND `Time_Stamp` <= NOW() - INTERVAL 1 WEEK"
avg_2week_users = get_average_users(sql_query)
#log('Average 2 weeks ago: '+ str(avg_day_users))

#count average Houerly and Daily
h_c = float(avg_hour_users)/float(avg_day_users)*100
d_c = float(avg_day_users)/float(avg_2day_users)*100
w_c = float(avg_week_users)/float(avg_2week_users)*100

#convert to strings for mail 
ahu = str("%.0f" % round(avg_hour_users,0))
adu = str("%.0f" % round(avg_day_users,0))
a2du = str("%.0f" % round(avg_2day_users,0))
h_cs = str("%.2f" % round(h_c,2))
d_cs = str("%.2f" % round(d_c,2))
w_cs = str("%.2f" % round(w_c,2))
log("Houerly[%]: " + h_cs)
log("Daily[%]: " + d_cs)
log("Weekly[%]: " + w_cs)


#Create the body of the message (a plain-text and an HTML version).
HTML = "<html><head><style>table {border-collapse: collapse;} table, th, td {border: 1px solid black;}</style></head><body>" + \
       "<p>Changes in number of users on Poloniex:<br><ul>" + \
       "<li>Houerly[%]: " + h_cs + "</li><li> Daily[%]: " + d_cs + \
       "</li><li> Weekly[%]: " + w_cs + "</li></ul></p>"

###############################################################
#TOP RISE and DROPS
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

res = {}
for market in markets: 
    sql_query = "SELECT Last, BaseVolume, QuoteVolume FROM " + market + " ORDER BY id DESC LIMIT 1"
    data_now = get_market(sql_query)
    sql_query = "SELECT Last, BaseVolume, QuoteVolume FROM " + market + " WHERE TimeStamp >= NOW() - INTERVAL 1 DAY ORDER BY id ASC LIMIT 1"
    data_24h = get_market(sql_query)
    #print(market)
    #print(data_now)
    #print(data_24h)
    #if any 0 value then skip othervise we will get division by 0
    if(0 in data_now):
        continue
    delta_price = (data_now[0] - data_24h[0])/data_now[0]*100
    delta_base_volume = (data_now[1] - data_24h[1])/data_now[1]*100
    delta_quote_volume = (data_now[2] - data_24h[2])/data_now[0]*100
    #res[market] = [delta_price, delta_base_volume, delta_quote_volume]
    res[market] = delta_price

tops = dict(sorted(res.iteritems(), key=operator.itemgetter(1), reverse=True)[:5])
drops = dict(sorted(res.iteritems(), key=operator.itemgetter(1), reverse=False)[:5])

HTML += "<p>Poloniex TOP 5 Markets:<br><ul>"
#for m in sorted(tops, key=tops.get, reverse=True):
#    print m + ": " + str(tops[m])

for m in sorted(tops, key=tops.get, reverse=True):
    HTML += "<li>" + m + ": " + '{0:.2f}'.format(tops[m]) + "</li>"

HTML += "</ul></p><p>Poloniex TOP 5 Drops:<br><ul>"

for m in sorted(drops, key=drops.get, reverse=True):
    HTML += "<li>" + m + ": " + '{0:.2f}'.format(drops[m]) + "</li>"

HTML +="</ul></p>"
#log('Delta last 24 hour '+ market + ": "+ str(delta_price))
#print(tops)
#print(drops)

###############################################################
#MARKETS
HTML += """<p>Poloniex Markets:<br>
            <table border="1" cellpadding="4"><tr>
            <td>Market</td>
            <td>Last Price</td>
            <td>Percent Change</td>
            <td>Base Volume</td>
            <td>Quote Volume</td>"""

markets = ["USDT_BTC", "BTC_PASC", "BTC_XMR", "BTC_ETH", "BTC_ETC", "BTC_VTC", "BTC_LTC", "BTC_DASH"]
for market in markets: 
    sql_query = "SELECT Last, PercentChange, BaseVolume, QuoteVolume FROM " + market + " ORDER BY id DESC LIMIT 1"
    res = get_market(sql_query)
    HTML += "<tr><td>" + market + "</td><td>" + '{0:.6f}'.format(res[0]) + "</td><td>" + '{0:.2f}'.format(res[1]) \
         + "</td><td>" + '{0:.2f}'.format(res[2]) + "</td><td>" + '{0:.2f}'.format(res[3]) + "</td></tr>"

HTML += "</table>"
HTML += "</p></body></html>"

#log(HTML)
sendMail(FROM,TO,SUBJECT,HTML,SERVER)
log("Email Sent To: " + ", ".join(TO))
