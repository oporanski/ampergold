#!/usr/bin/env python
import datetime
import dateutil.parser
import requests
import MySQLdb
from datetime import datetime, timedelta
from lxml import html

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

def write_users_to_db(usersOnline, server_time):
    x = CONN.cursor()
    try:
	x.execute("""INSERT INTO `Users_Online`(`Number_Of_Users`,`Server_Time`) VALUES (%s, %s)""",(usersOnline,server_time))
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
log("**********************************************************")
#get number of users online 
users_online, server_time = get_web_page_data()
log('Users Online: ' + str(users_online))
log('Server Time: ' + str(server_time))
server_time = get_date_time(server_time)
#print (type(server_time))

write_users_to_db(users_online,server_time)


CONN.close()
