__author__ = 'KevinGee'

import facebook
import json
import urllib2
import ast
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def writeJsontoFile(o, f):
    f.write(json.dumps(o, indent=1).encode('utf8'))

# !!!
# PUT YOUR ACCESS TOKEN IN THE FILE BELOW!!!
# !!!
f = open('access_token.txt', 'r')
ACCESS_TOKEN = f.read()
f.close()

# !!!
# Create credentials.txt with username and pass separated by comma
# email;pass
f = open('credentials.txt', 'r')
CREDENTIALS = f.read().strip().split(';')
f.close()

# Download http://chromedriver.storage.googleapis.com/index.html?path=2.9/
# This is chrome driver

# Documentation about Selenium
# http://selenium-python.readthedocs.org/en/latest/installation.html

# Initialise Chrome and connect to fb
driver = webdriver.Chrome()
# Must be with http:// on Chrome
driver.get("http://www.facebook.com")
email = driver.find_element_by_id("email")
password = driver.find_element_by_id("pass")
email.send_keys(CREDENTIALS[0])
password.send_keys(CREDENTIALS[1])
password.submit()

test = open('user_locations/scrapped.txt', 'w')


g = facebook.GraphAPI(ACCESS_TOKEN)

clubList = []

# Read club list and put it in an array
clubFile = open('clubs.txt', 'r')
for line in clubFile:
	if (line.startswith('#')):
		continue
	array = line.split(';')
	clubList.append((array[0], array[1].strip()))
clubFile.close()

# Output page info and info about events
for club in clubList:
	clubName = club[0].strip()
	clubId = club[1].strip()
	pageJson = g.get_object(clubId)

	# Get event list of concrete club
	eventList = g.get_connections(clubId, 'events')

	counter = 0

	# Update event list with info about event under name "eventdata" : {concrete data}
	for event in eventList['data']:
		eventId = event['id']
		# insert data about people attending event
		attending = g.get_connections(eventId, 'attending')
		# Scrap nationalities from fb
	   	for person in attending['data']:
			personId = person['id']
			driver.get("http://www.facebook.com/" + str(personId))
			lives_in = driver.find_elements_by_class_name("_4_ug")
			for info in lives_in:
				if info.text.startswith('Lives'):
					test.write(info.text.encode('utf8') + '\n')
					test.flush()
					continue
		counter+=1

	   	for event in eventList['data']:
	   		eventId = event['id']
	   		attending = g.get_connections(eventId, 'attending')
	   		for person in attending['data']:
	   			personId = person['id']
	   			driver.get("http://www.facebook.com/" + str(personId))
	   			lives_in = driver.find_elements_by_class_name("_4_ug")
	   			test.write(unicode(personId).encode('utf8') + ';')
	   			for info in lives_in:
	   				if info.text.startswith('Lives'):
	   					test.write(info.text.encode('utf8') + ';')
	   				if info.text.startswith('From'):
	   					test.write(info.text.encode('utf8') + ';')
	   			test.write('\n')
	   			test.flush()

test.close()
