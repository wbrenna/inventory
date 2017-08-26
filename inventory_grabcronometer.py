#!/usr/bin/python

import sys
import os
from xml.etree import ElementTree
import glob
import re
import datetime

CRONOMETER_FOLDER = "../CRONOMETER-data/foods/"

def cronometer_recipes(inventoryarr):
	#execute concatenate_cronometer.sh
	foodlist = {}
	food = ''
	foodroot = ElementTree.parse('complete_cronometer_data.xml').getroot()
	foods = foodroot.findall('food')
	recipes = foodroot.findall('recipe')
        validrecipelist = []
#the CRONOMETER item is either a recipe or an item with a UPC
#check to make sure it's a recipe; should start with <recipe uid="####" ...
#from ####.xml
	print "Collecting foods in inventory..."
        for inventoryarritems in inventoryarr:
                expiryindex = 0
                #print inventoryarr[inventoryarritems]
                expirylength = inventoryarr[inventoryarritems][0][0]
                #print expirylength
                for inventoryarritem in inventoryarr[inventoryarritems][1:]:
                        #print inventoryarritem
                        daydiff = datetime.date.today() - inventoryarritem
                        expiryindextmp = float((daydiff.days))/expirylength #numdays in cupboard
			#print daydiff
			#print float(daydiff.days)
                        if expiryindextmp > 1:
                                expiryindextmp = 1
                        if expiryindextmp > expiryindex:
                                expiryindex = expiryindextmp
                #print expiryindex
                foodlist[inventoryarr[inventoryarritems][0][2]] = expiryindex
	print "Gathering and sorting matching recipes..."
	for recipe in recipes:
                ingredients = recipe.iter('serving')
		ingmatch = 0
		expirymetric = 0
                ingcounter = 0
		for ingredient in ingredients:
                        #print ingredient.attrib
                        ingcounter = ingcounter + 1
                        if ingredient.attrib['food'] in foodlist.keys():
				ingmatch = ingmatch + 1
				expirymetric = expirymetric + foodlist[ingredient.attrib['food']]
				#print(foodlist[ingredient.attrib['food']])
		if ingmatch > 0:
#add the recipe to our list, and determine whether any of the <serving ... food="######" source="My Foods"
#exist in the recipe, if so, add them as an element of the recipe-indexed list.
			expirymetric = float(expirymetric)/ingmatch
			validrecipelist.append((recipe, float(float(1-float(1/float(ingmatch+0.3))+float(1/float(ingcounter+0.3)))*(float(expirymetric+2)/3.0))))
			#print('Recipe found, with metric ' + str(expirymetric) + '; ingmatch is ' + str(ingmatch))
        return(sorted(validrecipelist, key = lambda recipedata: recipedata[1], reverse=True))



def cronometer(upc):
	foodxml = ''
	food = ''
	foodroot = ''
	for filename in glob.glob(CRONOMETER_FOLDER + '/*.xml'):
		foodroot = ElementTree.parse(filename).getroot()

		food =  foodroot.findall('comments')[0].text

		if food is not None:
			#print "Found a UPC in the comment."
                        foodarr = re.split('\r|\t|\n',food)
			if upc in foodarr:
				print foodroot.attrib['name'] + ", UID = " +  foodroot.attrib['uid']
				return([foodarr[foodarr.index(upc)+1],foodroot.attrib['name'],foodroot.attrib['uid']])
	
	return(0)

def main():
        x = cronometer("0066800000152")
	if x == 0:
		print "No result."
	else:
		print "Match found!"

if __name__ == "__main__":
        main()
