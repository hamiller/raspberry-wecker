#!/usr/bin/python
# -*- coding: utf-8 -*-
# Raspberry Pi Wecker Class
# $Id: Clock.py, 2014/09/19
#
# Author : Florian Miess
#
# Main Class with all clock funcionality
# 
#
import time
import RPi.GPIO as GPIO
from Display import Display
from NTPTime import NTPTime
from Properties import Properties 
from rotary_class import RotaryEncoder
from Alarm import Alarm

class Clock():
	# Setup der Tasten
	wheelButton = 21
	pauseButton = 20
	stopButton = 16
	schalter = 25
	scrollUp = 6
	scrollDown = 5

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pauseButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(stopButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(schalter, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	# Klassen laden
	ntpTime = NTPTime()
	display = Display()
	prop = Properties()
	alarm = Alarm()

	# ausgewaehltes Menue
	menuItem = 0
	# Menü aktiv
	menuActive = False
	menuMinuten = False

	waittime = 2

	# Einstellungen einlesen
	wakeHour = int(prop.getProperty("Weckzeit").split(":")[0])
	wakeMinute = int(prop.getProperty("Weckzeit").split(":")[1])
	volume = int(prop.getProperty("Lautstaerke"))
	alarmActive = (prop.getProperty("Alarm") == "True")
	

	# Konstruktor
	def __init__(self):
		RotaryEncoder(self.scrollUp, self.scrollDown, self.wheelButton, callback=self.changeEvent)
		GPIO.add_event_detect(self.schalter, GPIO.BOTH, callback=self.changeAlarm)
		GPIO.add_event_detect(self.pauseButton, GPIO.BOTH, callback=self.pauseAlarm)
		GPIO.add_event_detect(self.stopButton, GPIO.BOTH, callback=self.stopAlarm)


	# verschiedene Menueeinträge durchschalten
	def changeEvent(self, event):
		# ein Menü ist aktiviert, also Funktion des aktiven Menüpunktes ausführen
		if self.menuActive:
			if event == RotaryEncoder.CLOCKWISE:
				self.menuUp()
			elif event == RotaryEncoder.ANTICLOCKWISE:
				self.menuDown()
			elif event == RotaryEncoder.BUTTONDOWN:
				# falls wir uns im Weckzeitmenü befinden, durch Stunden und Minuten schalten
				if self.menuItem == 1 and not self.menuMinuten:
					print "aktiviert"
					self.menuMinuten = True	
				else:
					print "deaktiviert"
					self.menuActive = False
					self.menuMinuten = False
					self.prop.setProperty("Weckzeit", str(self.wakeHour) + ":" + str(self.wakeMinute))
					self.prop.setProperty("Lautstaerke", self.volume)


		# kein Menü aktiv, also durch die Menüs navigieren
		else:
			if event == RotaryEncoder.CLOCKWISE:
				self.menuItem += 1
			elif event == RotaryEncoder.ANTICLOCKWISE:
				self.menuItem -= 1
			elif event == RotaryEncoder.BUTTONDOWN:
				self.menuActive = True

			self.display.showMenu(self.menuItem)
			if self.menuItem == 0:
				pass
			elif self.menuItem == 1:
				# Weckzeit einstellen
				self.display.showTime(self.wakeHour, self.wakeMinute, self.alarmActive, self.menuItem)
			elif self.menuItem == 2:
				# Lautstärke einstellen
				self.display.showNumber(self.volume, self.menuItem)
			elif self.menuItem >= 3:
				self.menuItem = -1
			elif self.menuItem <= -1:
				self.menuItem = 3
	

	# Alarm de-/aktivieren
	def changeAlarm(self, event):
		self.alarmActive = not self.alarmActive
		self.display.showAlarm(self.alarmActive)
		self.prop.setProperty("Alarm", self.alarmActive)

	def pauseAlarm(self, event):
		self.alarm.pauseAlarm(self.waittime)
		if self.waittime > 1:
			self.waittime -= 1

	def stopAlarm(self, event):
		self.alarm.stopAlarm()
		waittime = 10

	# Eintrag erhöhen
	def menuUp(self):
		if self.menuItem == 1:
			# Stunden
			if not self.menuMinuten:
				self.wakeHour += 1
				self.wakeHour %= 24
			# Minuten
			else:
				self.wakeMinute += 1
				self.wakeMinute %= 60
			self.display.showTime(self.wakeHour, self.wakeMinute, self.alarmActive, self.menuItem)

		elif self.menuItem == 2:
			self.volume += 1
			self.display.showNumber(self.volume, self.menuItem)
	
	# Eintrag erniedrigen
	def menuDown(self):
		if self.menuItem == 1:
			# Stunden
			if not self.menuMinuten:
				self.wakeHour -= 1
				self.wakeHour %= 24
			# Minuten
			else:
				self.wakeMinute -= 1
				self.wakeMinute %= 60
			self.display.showTime(self.wakeHour, self.wakeMinute, self.alarmActive, self.menuItem)

		elif self.menuItem == 2:
			self.volume -= 1
			self.display.showNumber(self.volume, self.menuItem)


	def main(self):
		try:
			lastminute = 0
			while True:
				# normale Zeit anzeigen
				currentTime = self.ntpTime.getTime()
				hour = currentTime.hour
				minute = currentTime.minute
				second = currentTime.second
				if self.menuItem == 0:
					# blinken
					self.display.showTime(hour, minute, self.alarmActive, self.menuItem)
					self.display.blink(second)
			
				# Alarm 1x pro Minute prüfen
				if not minute == lastminute:
					if self.alarm.isAlarm(currentTime, self.wakeHour, self.wakeMinute, self.alarmActive, self.menuItem):
						self.alarm.startAlarm()
				lastminute = minute
				time.sleep(0.5)


		except KeyboardInterrupt:
			print "Programm abgebrochen"
		finally:
			GPIO.cleanup()

if __name__ == '__main__':
	objName = Clock()
	objName.main()

