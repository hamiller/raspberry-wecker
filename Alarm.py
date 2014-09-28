# -*- coding: utf-8 -*-
# Raspberry Pi Alarm Class
# $Id: Alarm.py, 2014/09/25
#
# Author : Florian Miess
#
# Alarm class to do an alarm - sound or something else
# 
#
import time

class Alarm(object):

	alarming = False
	paused = False
	waitminute = 0

	def startAlarm(self):
		if not self.alarming:
			print "Aufwachen!!!"
			self.alarming = True

	def pauseAlarm(self, _waitminute):
		if self.alarming:
			self.alarming = False
			self.waitminute += _waitminute
			print "Alarm pausiert für",_waitminute,"Minuten"

	def stopAlarm(self):
		if self.alarming:
			self.alarming = False
			self.waitminute = 0
			print "Alarm gestopped"

	def isAlarm(self, currentTime, wakehour, wakeminute, alarmActive, menu):
		hour = currentTime.hour
		minute = currentTime.minute
		
		# no alarm during setup
		if not menu == 1:
			if alarmActive and hour == wakehour and minute == (wakeminute + self.waitminute):
				return True

		return False

