#!/usr/bin/python

import pickle
import sys
import datetime


def main():
	file = open('inventory.inv', 'r')
	inventoryarr = pickle.load(file)
	file.close()

	shoppinglistfile = open('shoppinglist.txt', 'a')
	while True: 
		print "Scan the UPC of the item you'd like to remove."
		linetmp = sys.stdin.readline()
		if not linetmp:
			break
		line = linetmp.rstrip()
		#upc = line[7:]
                upc = line
		try:
			tmp = inventoryarr[upc]
		except:
			print "The item " + upc + " does not yet exist in this database."
			continue

		try:
			print upc + ": \"" + inventoryarr[upc][0][1] + "\", added on " + inventoryarr[upc].pop(1).strftime("%A, %d %B %Y") + " was successfully deleted."
			shoppinglistfile.write(inventoryarr[upc][0][1] + ", " + upc + "\n")
		except:
			print "The item exists, but you currently have zero stock. Removing record from inventory entirely."
                        #inventoryarr[upc].pop(0)
                        inventoryarr.pop(upc,None)

	shoppinglistfile.close()

	print "Remaining items:"
	print inventoryarr


	file = open('inventory.inv', 'w')
	pickle.dump(inventoryarr,file)
	file.close()

if __name__ == "__main__":
	main()
