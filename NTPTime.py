import time

class NTPTime(object):

	def getTime(self):
		return time.strftime('%H:%M')