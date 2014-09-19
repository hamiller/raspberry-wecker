# -*- coding: utf-8 -*-
# Raspberry Pi Display Dummy Class
# $Id: Display.py, 2014/09/19
#
# Author : Florian Miess
#
# Dummy Class to display time etc. later will be replace by one which controls a 7 segment display
# 
#
class Display(object):

	def show(self, number):
		print number

	def showMenu(self, number):
		if number == 0:
			print "0 Uhrzeit"
		elif number == 1:
			print "1 Weckzeit"
		elif number == 2:
			print "2 Lautstärke"

	def showAlarm(self, alarm):
		print "Alarm:",alarm
