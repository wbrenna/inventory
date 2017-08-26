#!/usr/bin/env python

import pickle
#import sys
import os.path
from subprocess import call
from xmlrpclib import ServerProxy, Error
import datetime
import urllib2
import simplejson
from xml.etree import ElementTree
import inventory_grabcronometer


def main():
	try:
		with open('inventory.inv', 'r') as filename:
			inventoryarr = pickle.load(filename)
			filename.close()
	except IOError:
		inventoryarr = {}

	call("./concatenate_cronometer.sh", shell=True)
        recipearr = inventory_grabcronometer.cronometer_recipes(inventoryarr) #construct recipes with at least one item from inventoryarr
        #print out the details of the top few recipes
        if recipearr != []:
                print "The top ranked recipe is called " + recipearr[0][0].attrib['name'] + " with ranking " + str(recipearr[0][1]) + "."
                print "Other top recipes:"
                for el in recipearr[1:8]:
                        print el[0].attrib['name'] + " with ranking " + str(el[1]) + "."

        else:
                print "No matching recipes found."

if __name__ == "__main__":
	main()
