#!/usr/bin/python

import pickle
import datetime
import smtplib
import string

def main():
	try:
		file = open('inventory.inv', 'r')
	except:
		print "Issue opening inventory.inv. Make sure this file is in the current directory. If it is not, add an item to create it."
		return
	inventoryarr = pickle.load(file)
	file.close()

#We just check each of the elements
	for upc in inventoryarr.keys():
		if inventoryarr[upc][0][1] is not None:
			itemname = upc + ": " + inventoryarr[upc][0][1] 
		else:
			itemname = upc + "Unknown"
		length = inventoryarr[upc][0][0]
		for key in inventoryarr[upc][1:]:
			buydate = key
			newdate = buydate + datetime.timedelta(days=length)
			print itemname + ", expiring on " +  newdate.strftime("%Y-%m-%d, a %A")

	file = open('inventory.inv', 'w')
	pickle.dump(inventoryarr,file)
	file.close()

if __name__ == "__main__":
	main()
