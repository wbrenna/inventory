#!/usr/bin/python

import pickle
import datetime
import smtplib
import string

def main():
	file = open('inventory.inv', 'r')
	inventoryarr = pickle.load(file)
	file.close()

#We just check each of the elements
	for upc in inventoryarr.keys():
		itemname = upc + ": " + inventoryarr[upc][0][1] 
		length = inventoryarr[upc][0][0]
		for key in inventoryarr[upc][1:]:
			buydate = key
			newdate = buydate + datetime.timedelta(days=length)
			print itemname
			print "Expiring on " + newdate.strftime("%A, %d %B %Y")
			print "\n"


	file = open('inventory.inv', 'w')
	pickle.dump(inventoryarr,file)
	file.close()

if __name__ == "__main__":
	main()
