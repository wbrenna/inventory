#!/usr/bin/env python

import pickle
import sys
from xmlrpclib import ServerProxy, Error
import datetime
import urllib2
import simplejson
import select
import inventory_grabcronometer

DEFAULT_EXPIRY_TIME = 100
INPUT_TIMEOUT = 100

#This will add an item if it is scanned once,
#and remove it if scanned twice consecutively.
def main():
	try:
		with open('inventory.inv', 'r') as filename:
			inventoryarr = pickle.load(filename)
			filename.close()
	except IOError:
		inventoryarr = {}


        lineprev = ""
	while True:
                lastRun = False
                if select.select([sys.stdin], [], [], INPUT_TIMEOUT)[0]:
                        linetmp = sys.stdin.readline() 
                        if lineprev == "":
                                lineprev = linetmp
                                if select.select([sys.stdin], [], [], INPUT_TIMEOUT)[0]:
                                        linetmp = sys.stdin.readline() 
                                        if linetmp == lineprev:
                                                removeItem = True
                                        else:
                                                removeItem = False
                                else:
                                        lineprev = linetmp
                                        linetmp = ""
                                        removeItem = False
                                        lastRun = True
                        else:
                                if linetmp == lineprev:
                                        removeItem = True
                                else:
                                        removeItem = False
                else:
                        lineprev = linetmp
                        linetmp = ""
                        removeItem = False
                        lastRun = True


		line = lineprev.rstrip()
		upc = line
		itemdata = datetime.date.today()
                if removeItem == False:
                        if inventoryarr.has_key(upc):
                                inventoryarr[upc].append(itemdata)
                        else:
                                print "UPC" + upc + " is a brand new item. Searching Cronometer..." 
                                arr = inventory_grabcronometer.cronometer(upc)
                                if arr != 0:
                                        print "Found in Cronometer! Item successfully entered."
                                        #inventoryarr[upc] = [arr] 
                                        specified_expiry_time = int(arr[0])
                                        if specified_expiry_time < 100 and specified_expiry_time > 0:
                                            arr2 = [specified_expiry_time,arr[1],arr[2]]
                                        else:
                                            arr2 = [DEFAULT_EXPIRY_TIME,arr[1],arr[2]]
                                        inventoryarr[upc] = [arr2]
                                        inventoryarr[upc].append(itemdata)
                                        continue
                                print "Not found in Cronometer. Please add there."
                                continue
                else:
                        try:
                            tmp = inventoryarr[upc]
                            print "Item added on " + tmp.pop(1).strftime("%A, %d %B %Y") + " was successfully deleted."
                        except:
                            print "Item to be removed did not exist in the database."

                        linetmp = ""

		print "Successfully entered upc " + upc
                if lastRun = True:
                        print "Saving entries..."
                        file = open('inventory.inv', 'w')
                        pickle.dump(inventoryarr,file)
                        file.close()
                        lineprev = ""
                        linetmp = ""
                else:
                        lineprev = linetmp


	print "Your current inventory contains:"
	print inventoryarr

	file = open('inventory.inv', 'w')
	pickle.dump(inventoryarr,file)
	file.close()

if __name__ == "__main__":
	main()
