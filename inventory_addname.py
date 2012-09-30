#!/usr/bin/python

import pickle
import sys

def grabessentials():
	itemname = ''
	expiry = ''
	print "Please enter the descriptive name for this item:"
	length = sys.stdin.readline()
	if length:
		itemname = length
	else:
		print "You didn't enter a valid name. Try again."
		return([])

	print "Please enter the approximate amount of shelf-life for this item (in days):"
	length = sys.stdin.readline()
	if length:
		expiry = int(length)
	else:
		print "You didn't enter a valid shelf-life. Enter the item again."
		return([])
	return([expiry,itemname])


def main():
	file = open('inventory.inv', 'r')
	inventoryarr = pickle.load(file)
	file.close()

	while True:
		print "Enter the EAN code of an item you wish to modify."
		linetmp = sys.stdin.readline()
		if not linetmp:
			break
		#line = linetmp.rstrip()[7:]
		upc = linetmp.rstrip()
		arr = grabessentials()
		try:
			tmp = inventoryarr[upc]
			print "The item is already in the database. Unless you quit now I'll overwrite its name..."
			inventoryarr[upc][0] = arr
		except:
			inventoryarr[upc] = [arr]
		print "Added item " + upc +  "."


	file = open('inventory.inv', 'w')
	pickle.dump(inventoryarr,file)
	file.close()

if __name__ == "__main__":
	main()
