#!/usr/bin/python

import pickle
import datetime
import smtplib
import string

MYEMAIL = "test@test.com"
MYFROM = "test@inventory.com"
HOST = "localhost"

def main():
	file = open('inventory.inv', 'r')
	inventoryarr = pickle.load(file)
	file.close()

#We just check for expiry of the elements
	for upc in inventoryarr.keys():
		length = inventoryarr[upc][0][0]
		item = inventoryarr[upc][0][1]
		for key in inventoryarr[upc][1:]:
			#buydate = key
			newdate = key + datetime.timedelta(days=length)
			if newdate < datetime.date.today() + datetime.timedelta(days=2):
				subj = "Items about to expire!"
				text = "Your item " + item + " is expiring in under 2 days. Please finish it!"
				BODY = string.join((
					"From: %s" % MYFROM,
					"To: %s" % MYEMAIL,
					"Subject: %s" % subj ,
					"",
					text
					), "\r\n")
				server = smtplib.SMTP(HOST)
				server.sendmail(FROM, [TO], BODY)
				server.quit()



	file = open('inventory.inv', 'w')
	pickle.dump(inventoryarr,file)
	file.close()

if __name__ == "__main__":
	main()
