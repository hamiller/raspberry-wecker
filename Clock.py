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

class Clock():
	# Setup der Tasten
	wheelButton = 21
	taster2 = 20
	taster3 = 16
	schalter = 25
	scrollUp = 6
	scrollDown = 5

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(taster2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(taster3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(schalter, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	# Klassen laden
	ntpTime = NTPTime()
	display = Display()
	prop = Properties()

	# ausgewaehltes Menue
	menuItem = 0
	# Menü aktiv
	menuActive = False
	menuMinuten = False

	# Einstellungen einlesen
	weckzeitStunden = int(prop.getProperty("Weckzeit").split(":")[0])
	weckzeitMinuten = int(prop.getProperty("Weckzeit").split(":")[1])
	lautstaerke = int(prop.getProperty("Lautstaerke"))
	alarm = bool(prop.getProperty("Alarm"))
	

	# Konstruktor
	def __init__(self):
		RotaryEncoder(self.scrollUp, self.scrollDown, self.wheelButton, callback=self.changeEvent)
		GPIO.add_event_detect(self.schalter, GPIO.BOTH, callback=self.changeAlarm)


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
					self.prop.setProperty("Weckzeit", str(self.weckzeitStunden) + ":" + str(self.weckzeitMinuten))
					self.prop.setProperty("Lautstaerke", self.lautstaerke)


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
				self.display.show((self.weckzeitStunden, self.weckzeitMinuten))
			elif self.menuItem == 2:
				# Lautstärke einstellen
				self.display.show(self.lautstaerke)
			elif self.menuItem >= 3:
				self.menuItem = -1
			elif self.menuItem <= -1:
				self.menuItem = 3
	

	# Alarm de-/aktivieren
	def changeAlarm(self, event):
		self.alarm = not self.alarm
		self.display.showAlarm(self.alarm)
		self.prop.setProperty("Alarm", self.alarm)

	# Eintrag erhöhen
	def menuUp(self):
		if self.menuItem == 1:
			# Stunden
			if not self.menuMinuten:
				self.weckzeitStunden += 1
				self.weckzeitStunden %= 24
			# Minuten
			else:
				self.weckzeitMinuten += 1
				self.weckzeitMinuten %= 60
			self.display.show((self.weckzeitStunden, self.weckzeitMinuten))

		elif self.menuItem == 2:
			self.lautstaerke += 1
			self.display.show(self.lautstaerke)
	
	# Eintrag erniedrigen
	def menuDown(self):
		if self.menuItem == 1:
			# Stunden
			if not self.menuMinuten:
				self.weckzeitStunden -= 1
				self.weckzeitStunden %= 24
			# Minuten
			else:
				self.weckzeitMinuten -= 1
				self.weckzeitMinuten %= 60
			self.display.show((self.weckzeitStunden, self.weckzeitMinuten))

		elif self.menuItem == 2:
			self.lautstaerke -= 1
			self.display.show(self.lautstaerke)


	def main(self):
		try:
			while True:
#				currentTime = self.ntpTime.getTime()
#				self.display.show(currentTime)
				time.sleep(0.5)

		except KeyboardInterrupt:
			print "Programm abgebrochen"
		finally:
			GPIO.cleanup()

if __name__ == '__main__':
	objName = Wecker()
	objName.main()

