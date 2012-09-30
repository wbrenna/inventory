#!/usr/bin/python

import sys
import os
from xml.etree import ElementTree
import glob

CRONOMETER_FOLDER = "/home/wilson/.cronometer/foods/"

def cronometer(upc):
	foodxml = ''
	food = ''
	foodroot = ''
	for filename in glob.glob(CRONOMETER_FOLDER + '/*.xml'):
		foodroot = ElementTree.parse(filename).getroot()

		food =  foodroot.findall('comments')[0].text

		if food is not None:
			print "Found a UPC in the comment."
			if upc == foodroot.findall('comments')[0].text:
				print foodroot.attrib['name'] + ", UID = " +  foodroot.attrib['uid']
				return([foodroot.attrib['name'],foodroot.attrib['uid']])
	
	return(0)





if __name__ == "__main__":
	x = cronometer("0066800000152")
	if x == 0:
		print "No result."
	else:
		print "Match found!"
