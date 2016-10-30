#!/usr/bin/python

import pickle
import datetime
import smtplib
import string

def main():
	file = open('inventory.inv', 'r')
	inventoryarr = pickle.load(file)
	file.close()

        xmlfile = open('inventory.xml', 'w')
#We just check each of the elements
	for upc in inventoryarr.keys():
                xmlfile.write('<item>\n\t<upc>' + upc + '</upc>\n')
		if inventoryarr[upc][0][1] is not None:
                        xmlfile.write('\t<name>' + inventoryarr[upc][0][1] + '</name>\n')
		length = inventoryarr[upc][0][0]
		for key in inventoryarr[upc][1:]:
			buydate = key
			newdate = buydate + datetime.timedelta(days=length)
                        xmlfile.write('\t\t<expiry>' + newdate.strftime("%A, %d %B %Y") + '</expiry>\n')
                xmlfile.write('</item>')

        xmlfile.close()

if __name__ == "__main__":
	main()
