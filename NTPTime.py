# Raspberry Pi Time class
# $Id: NTPTime.py, 2014/09/19
#
# Author : Florian Miess
#
# This class just returns the system time
# 
#

import time

class NTPTime(object):

	def getTime(self):
		return time.strftime('%H:%M')
