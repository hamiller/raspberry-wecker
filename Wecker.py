#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO
from Display import Display
from NTPTime import NTPTime
from Properties import Properties 

# Setup
menu = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(menu, GPIO.IN, pull_up_down=GPIO.PUD_UP)

ntpTime = NTPTime()
display = Display()
prop = Properties()

# ausgewaehltes Menue
menuItem = 0
weckzeit = int(prop.getProperty("Weckzeit"))
lautstaerke = int(prop.getProperty("Lautstaerke"))

# verschiedene Menueeinträge durchschalten
def changeMenu(channel):
	global menuItem
	menuItem += 1
	
	display.showMenu(menuItem)
	if menuItem == 1:
		# Weckzeit einstellen
		global weckzeit
		display.show(weckzeit)
	elif menuItem == 2:
		prop.setProperty("Weckzeit", weckzeit)
		# Lautstärke einstellen
		global lautstaerke
		display.show(lautstaerke)
	elif menuItem == 3:
		prop.setProperty("Lautstaerke", lautstaerke)
		menuItem = 0
	

# Eintrag erhöhen
def menuUp(channel):
	if menuItem == 1:
		global weckzeit
		weckzeit += 1
		display.show(weckzeit)
	elif menuItem == 2:
		global lautstaerke
		lautstaerke += 1
		display.show(lautstaerke)

# Eintrag erniedrigen
def menuDown(channel):
	if menuItem == 1:
		global weckzeit
		weckzeit -= 1
		display.show(weckzeit)
	elif menuItem == 2:
		global lautstaerke
		lautstaerke -= 1
		display.show(lautstaerke)


GPIO.add_event_detect(menu, GPIO.RISING, callback=changeMenu)
GPIO.add_event_detect(scrollUp, GPIO.RISING, callback=menuUp)
GPIO.add_event_detect(scrollDown, GPIO.RISING, callback=menuDown)

#Test
menuUp(1)
menuUp(1)
menuDown(1)
changeMenu(1)
menuUp(1)
menuUp(1)
menuDown(1)
changeMenu(1)
menuUp(1)
menuUp(1)
menuDown(1)
changeMenu(1)
changeMenu(1)

while True:
	currentTime = ntpTime.getTime()
	display.show(currentTime)
	time.sleep(1)