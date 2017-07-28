#!/usr/bin/env python

import pickle
import sys
from xmlrpclib import ServerProxy, Error
import datetime
import urllib2
import simplejson
import inventory_grabcronometer

DEFAULT_EXPIRY_TIME = 600
#The default expiry time for items, in days.

def main():
	try:
		with open('inventory.inv', 'r') as filename:
			inventoryarr = pickle.load(filename)
			filename.close()
	except IOError:
		inventoryarr = {}


	while True:
		linetmp = sys.stdin.readline()
		if not linetmp:
			break
		line = linetmp.rstrip()
		#upc = line[7:]
		upc = line
		itemdata = datetime.date.today()
		if inventoryarr.has_key(upc):
			inventoryarr[upc].append(itemdata)
		else:
			print "UPC" + upc + " is a brand new item. Searching Cronometer..." 
			arr = inventory_grabcronometer.cronometer(upc)
			if arr != 0:
				print "Found in Cronometer! Item successfully entered."
                                specified_expiry_time = int(arr[0])
                                if specified_expiry_time < 600 and specified_expiry_time > 0:
                                    arr2 = [specified_expiry_time,arr[1],arr[2]]
                                else:
                                    arr2 = [DEFAULT_EXPIRY_TIME,arr[1],arr[2]]
				inventoryarr[upc] = [arr2]
				inventoryarr[upc].append(itemdata)
				continue
                        #print "Not found in Cronometer. Searching UPC Database."
                        print "UPC " + upc + " was not found in Cronometer. Please enter it."
                        continue

		print "Successfully entered upc " + upc

	print "Your current inventory contains:"
	print inventoryarr

	file = open('inventory.inv', 'w')
	pickle.dump(inventoryarr,file)
	file.close()

if __name__ == "__main__":
	main()
