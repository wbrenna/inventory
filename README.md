Inventory
=========

This set of Python scripts will allow you to interface a barcode reader such as [zbarcam](http://zbar.sourceforge.net/) with a UPC database to keep track of foods as you buy them.


Install
=======

Download the set of scripts, ensure you have a working Python installation (I use Python>=2.6), and run 

```bash
python inventory --help
```

for information. 


Run
======

There are a number of features and options. Most of them are self-described. You can run

```bash
python inventory add
```

to begin adding items to your database. It is important to note that some of the commands require
input prefixed by the barcode type (only EAN-13 is fully supported at the moment), while others require
just the barcode iteself. This is because some commands are designed to receive input piped from zbarcam,
while others are designed to receive manual input. For example

	./inventory add

requires input such as

	0068100084245

The "modifyexpiry" allows you to enter a specific product EAN-13 manually and customize its expiry date.
The expiry dates persist through deletion of stock, so you will never need to enter expiry lengths for that particular product again.
The "remove" option allows you to scan barcodes on the way out, removing that product from your inventory.
The "printout" option will print the database out for you, neatly.
Finally, the "daily" option allows for cron or some other scheduling tool to check daily for products nearing expiry.
This is best used with a line in crontab that runs inventory with the daily option.
You will need to enter your email in inventory_daily.py in order for this to properly work,
as well as ensure that your system is a working mailserver.


Interfacing with Cronometer
--------------------------

Inventory also checks your [Cronometer](http://sourceforge.net/projects/cronometer/) database for UPC codes.
First, ensure you have the Cronometer foods folder specified in inventory_grabcronometer.py (it is a global variable).
Then, when you add custom items into Cronometer, just put the UPC in the Comments section. Inventory will automatically scan for Cronometer UPCs before turning to the web.


TODO
=========

Integrate with webserver to display printout status
