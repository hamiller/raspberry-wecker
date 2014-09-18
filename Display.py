# -*- coding: utf-8 -*-
class Display(object):

	def show(self, number):
		print "number {}".format(number)

	def showMenu(self, number):
		if number == 0:
			print "Uhrzeit"
		elif number == 1:
			print "Weckzeit"
		elif number == 2:
			print "Lautstärke"
		