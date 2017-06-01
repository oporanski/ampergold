#!/usr/bin/env python
import datetime
import dateutil.parser
import requests
import MySQLdb
import smtplib
import os.path

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#from datetime import datetime
from datetime import datetime, timedelta
from lxml import html

#######GLOBALS##########
ROOT_URL = 'https://poloniex.com'
INDEX_URL = ROOT_URL + '/exchange#btc_eth'

FROM = "ampergold@starelamy.org"
TO = ("oporanski@gmail.com", "marcin.opinc@gmail.com")
SUBJECT = "Poloniex number of users change significantly last 1h"
SUBJECT_DAY = "Poloniex number of users change significantly last 24h"
SERVER = "localhost"
CONN = MySQLdb.connect(host="localhost",user="root",passwd="PKjsizw02k",db="poloniex")
DEBUG = True
RE_NOTYFICATION_PERIOD = 1
MAX_CHANGE_HOUR = 0.1
MAX_CHANGE_DAY = 0.1

#######FUNCTIONS##########
def get_web_page_urls():
    response = requests.get(INDEX_URL)
    tree = html.fromstring(response.content)
    usersOnline = tree.xpath('//span[@id="usersOnline"]/text()')
    return usersOnline

def write_users_to_db(usersOnline):
    x = CONN.cursor()
    try:
	x.execute("""INSERT INTO `Users_Online`(`Number_Of_Users`) VALUES (%s)""",(usersOnline))
	CONN.commit()
    except:
	CONN.rollback()

def get_average_last_hour(sqlq):
    #log(sqlq)
    x = CONN.cursor()
    try:
	x.execute(sqlq)
	rows = x.fetchall()
    except:
	CONN.rollback()
    avgUsers = 0
    for row in rows:
	#log("Value:" + row[0])
	avgUsers += int(row[0])
    avgUsers = avgUsers/NumberOfRecords
    return avgUsers

def write_date_of_last_notyfication(fileName):
    f = open(fileName, "w")
    f.write(str(datetime.now()))
    f.close()

def check_last_notyfication(fileName):
    if (not os.path.isfile(fileName)):
	return True
    f = open(fileName, "r")
    line = f.readline()
    f.close()
    lastNotyficatioin = getDateTimeFromISO8601String(line)
    now = datetime.now()
    if abs(now - lastNotyficatioin) > timedelta(hours=RE_NOTYFICATION_PERIOD):
	return True
    return False

#######HELPERS##########
def sendMail(FROM,TO,SUBJECT,TEXT,HTML,SERVER,notyfiType):
    """Function sending email Input: FROM,TO,SUBJECT,TEXT,HTML,SERVER"""
    write_date_of_last_notyfication(notyfiType)

    COMMASPACE = ', '
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = COMMASPACE.join(TO)
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(TEXT, 'plain')
    part2 = MIMEText(HTML, 'html')
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
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
#get number of users online 
usersOnline = get_web_page_urls()[0]
log('Users Online: ' + str(usersOnline))
write_users_to_db(usersOnline)


#get number of users avarage last hour 
#Get last 12 records we are checking every 5 min so 5x12=60min
NumberOfRecords = 12
#sqlquery = """SELECT `Number_Of_Users` FROM `Users_Online` WHERE `Id` > (SELECT MAX(`Id`) - %s FROM `Users_Online`)""",NumberOfRecords
sqlquery = "SELECT `Number_Of_Users` FROM `Users_Online` WHERE `Id` > (SELECT MAX(`Id`) - " + str(NumberOfRecords) + " FROM `Users_Online`)"
avgHourUsers = get_average_last_hour(sqlquery)
log('Average last hour: '+ str(avgHourUsers))
#% changed last hour 
#change = float(usersOnline)/float(avgHourUsers)
change = abs(1-(float(avgHourUsers)/float(usersOnline)))
log("Change last hour: " + str("%.2f" % round(change,2)))

send = check_last_notyfication("last_notyfication_uah")
if send and change > MAX_CHANGE_HOUR: 
    # Create the body of the message (a plain-text and an HTML version).
    TEXT = "Achtung!\nA significant change in number of users on Poloniex\nChange: " + str("%.2f" % round(change,2)) + "%"
    HTML = "<html><head></head><body><p>Achtung!!!<br>A significant change in number of users on Poloniex<br>Change:"+ str("%.2f" % round(change,2)) + "%</p></body></html>"
    sendMail(FROM,TO,SUBJECT,TEXT,HTML,SERVER,"last_notyfication_uah")
    log("Email Sent To: " + ", ".join(TO))

#Send if 24h change is > then 85%
#get number of users avarage last 24 hours
#Get last 12 records we are checking every 5 min so 5x228=1440min (24h)
NumberOfRecords = 228
sqlquery = "SELECT `Number_Of_Users` FROM `Users_Online` WHERE `Id` > (SELECT MAX(`Id`) - " + str(NumberOfRecords) + " FROM `Users_Online`)"
avgDayUsers = get_average_last_hour(sqlquery)
log('Average last 24 hours: '+ str(avgDayUsers))
#% changed last hour 
#changeDay = float(usersOnline)/float(avgDayUsers)
changeDay = abs(1-(float(avgDayUsers)/float(usersOnline)))
log("Change last 24 hour: " + str("%.2f" % round(changeDay,2)))

send = check_last_notyfication("last_notyfication_day")
if send and change > MAX_CHANGE_DAY: 
    # Create the body of the message (a plain-text and an HTML version).
    TEXT = "Achtung!\nA significant change in number of users on Poloniex last 24h \nChange: " + str("%.2f" % round(changeDay,2)) + "%"
    HTML = "<html><head></head><body><p>Achtung!!!<br>A significant change in number of users on Poloniex<br>Change:"+ str("%.2f" % round(change,2)) + "%</p></body></html>"
    sendMail(FROM,TO,SUBJECT_DAY,TEXT,HTML,SERVER,"last_notyfication_day")
    log("Email Sent To: " + ", ".join(TO))


CONN.close()
