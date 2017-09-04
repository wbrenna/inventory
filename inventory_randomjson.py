#!/usr/bin/env python

import pickle
import os.path
from subprocess import call
from xmlrpclib import ServerProxy, Error
import datetime
import urllib2
import json
import re
import random
import qrcode
from pprint import pprint
from PIL import Image

def main():
	try:
		with open('inventory.inv', 'r') as filename:
			inventoryarr = pickle.load(filename)
			filename.close()
	except IOError:
		inventoryarr = {}

        with open('../CRONOMETER-data/bbcrecipes/bbccouk-recipes.json', 'r') as jsonfile:
            jsondata = json.load(jsonfile)
            jsonfile.close()

        #Generate a random number between 0 and 105 to narrow down the BBC recipes
        bbcchunk = int(105*random.random())
        bbcindex = int(99*random.random())

        bestrecipe = 0
        ingmatches = 0
        bestscore = 0

        
        searchinventoryarr = []
        for value in inventoryarr.values():
            try:
                searchinventoryarr.append(value[0][1])
            except IndexError:
                print "Index err."

        searchinventoryarr = [re.split(', |,| ', value) for value in searchinventoryarr] #split on comma or spaces
        searchinventoryarr = [item for items in searchinventoryarr for item in items] #flatten
        searchinventoryarr = [re.sub('[^A-Za-z]+', '', value) for value in searchinventoryarr] #only keep ascii letters
        searchinventoryarr = [item.lower() for item in searchinventoryarr]

        for searchcounter in range(0,30):
            recipeindex = (bbcindex + searchcounter) % 100
            jsonrecipe = jsondata[bbcchunk*100 + recipeindex]
            jsonings = [item.encode('ascii', 'xmlcharrefreplace') for item in jsonrecipe["ingredients"]]
            jsonings = [re.split(', |,| ', value) for value in jsonings] #split on comma or spaces
            jsonings = [item for items in jsonings for item in items] #flatten
            jsonings = [re.sub('[^A-Za-z]+', '', value) for value in jsonings] #only keep ascii letters
            jsonings = [item.lower() for item in jsonings]
            recipeingmatches = len(set(searchinventoryarr)&set(jsonings))
            recipenumingredients = len(set(jsonings))
            recipescore = float(float(recipeingmatches)/float(recipenumingredients))
            recipetitle = jsonrecipe["title"].encode('ascii', 'xmlcharrefreplace')
            if recipescore > bestscore:
                bestrecipe = recipetitle
                ingmatches = recipeingmatches
                bestscore = recipescore
            
        recipetitlestripped = re.sub('[^A-Za-z]+', '', bestrecipe)
	url = 'https://wbrenna.ca/wilson/recipes/bbcrecipesxml-' + str(bbcchunk) + '.xml#' + recipetitlestripped
        print "Here is a semi-random recipe you can try to make: it has a score of " + str(bestscore) + ". It's called \"" + bestrecipe + "\". See it at " + url + "."
        img = qrcode.make(url)
        img.show()
	img.save('qrcode.png')

if __name__ == "__main__":
	main()
