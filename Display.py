# -*- coding: utf-8 -*-
# Raspberry Pi Display Class
# $Id: Display.py, 2014/09/28
#
# Author : Florian Miess
#
# Display Class to display time etc. later will be replace by one which controls a 7 segment display
# 
#
from Adafruit_7Segment import SevenSegment

class Display(object):

	segment = SevenSegment(address=0x70)

	def showNumber(self, number, menu):
		print number, " menu: " , menu
		fourth = int(number % 1000) / 1000
		third = int(number % 1000) / 100
		second = int(number % 100) / 10
		first = number % 10
		self.segment.writeDigit(0, fourth)
		self.segment.writeDigit(1, third, menu == 2)
		self.segment.writeDigit(3, second)
		self.segment.writeDigit(4, first) 

	def showTime(self, hour, minute, alarm, menu):
		self.segment.writeDigit(0, int(hour / 10), menu == 1)
		self.segment.writeDigit(1, hour % 10)
		self.segment.writeDigit(3, int(minute / 10))
		self.segment.writeDigit(4, minute % 10, alarm)

	def blink(self, second):
		self.segment.setColon(second % 2)


	def showMenu(self, number):
		if number == 0:
			print "0 Uhrzeit"
		elif number == 1:
			print "1 Weckzeit"
		elif number == 2:
			print "2 Lautstärke"

	def showAlarm(self, alarm):
		print "Alarm:",alarm
		self.segment.writeDot(4, alarm)
