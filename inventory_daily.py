#!/usr/bin/python

import subprocess
import pickle
import datetime
import smtplib
import string

#MYEMAIL = "test@test.com"

#MYFROM = "test@inventory.com"

def sendmessage(recipient, subject, body):
        try:
                process = subprocess.Popen(['mail', '-s', subject, recipient],
                                                stdin=subprocess.PIPE)
        except Exception, error:
                print error
        process.communicate(body)

def main():
	file = open('inventory.inv', 'r')
	inventoryarr = pickle.load(file)
	file.close()

#We just check for expiry of the elements
	for upc in inventoryarr.keys():
		length = inventoryarr[upc][0][0]
		item = inventoryarr[upc][0][1]
		for key in inventoryarr[upc][1:]:
			newdate = key + datetime.timedelta(days=length)
			print newdate
			if newdate < datetime.date.today() + datetime.timedelta(days=2):
				subj = "[INVENTORY] \"Items about to expire!\""
				text = "\"Item UPC" + upc + ", " + item + " is expiring on " + str(newdate) + ". Consume with expedience!\""
				BODY = string.join((
					"From: %s" % MYFROM,
					"To: %s" % MYEMAIL,
					"Subject: %s" % subj ,
					"",
					text
					), "\r\n")
                                sendmessage(MYEMAIL, subj, text)
                                print(text)

if __name__ == "__main__":
	main()
