import logging
import cv2
import datetime
import numpy as np
import glob
import os
import requests
import xlsxwriter

from stockpiler.match_template_best_scale import matchTemplateBestScale
from stockpiler.popup import popup
from stockpiler.items import ButtonState

def ItemScan(screen,config,items):

	resC = None
	res = None
	if config.Set.get() == 0:
		findshirtC = cv2.imread('CheckImages//Default//86C.png', cv2.IMREAD_GRAYSCALE)
		findshirt = cv2.imread('CheckImages//Default//86.png', cv2.IMREAD_GRAYSCALE)

		if (config.experimentalResizing.get() == 1):
			if (config.bestIconScale == None):
				if (config.foxhole_height == 1080):
					config.bestIconScale = 1.0
					print("Best scale for ITEM ICONS is: " + str(config.bestIconScale))
				else:
					best_score, config.bestIconScale, resC = matchTemplateBestScale(screen, findshirtC, numtimes=20)
					print("Best scale for ITEM ICONS is: " + str(config.bestIconScale) + " with a score of: " + str(best_score))
			else:
				print("Best scale for ITEM ICONS is: " + str(config.bestIconScale))
			findshirtC = cv2.resize(findshirtC, (int(findshirtC.shape[1]*config.bestIconScale), int(findshirtC.shape[0]*config.bestIconScale)))
			findshirt = cv2.resize(findshirt, (int(findshirt.shape[1]*config.bestIconScale), int(findshirt.shape[0]*config.bestIconScale)))

			
	else:
		try:
			findshirtC = cv2.imread('CheckImages//Modded//86C.png', cv2.IMREAD_GRAYSCALE)
		except Exception as e:
			print("Exception: ", e)
			print("You don't have the Shirt crate yet in ItemScan")
			logging.info(str(datetime.datetime.now()) + " Failed loading modded shirt crate icon in ItemScan " + str(e))
		try:
			findshirt = cv2.imread('CheckImages//Modded//86.png', cv2.IMREAD_GRAYSCALE)
		except Exception as e:
			print("Exception: ", e)
			print("You don't have the individual Shirt yet in ItemScan")
			logging.info(str(datetime.datetime.now()) + " Failed loading modded individual shirt icon in ItemScan " + str(e))
	
	
	
	try:
		if (resC == None): resC = cv2.matchTemplate(screen, findshirtC, cv2.TM_CCOEFF_NORMED)
	except Exception as e:
		print("Exception: ", e)
		print("Looks like you're missing the shirt crate in ItemScan")
		logging.info(str(datetime.datetime.now()) + " Maybe missing shirt crate icon in ItemScan " + str(e))
	try:
		res = cv2.matchTemplate(screen, findshirt, cv2.TM_CCOEFF_NORMED)
	except Exception as e:
		print("Exception: ", e)
		print("Looks like you're missing the individual shirts in ItemScan")
		logging.info(str(datetime.datetime.now()) + " Maybe missing individual shirt icon in ItemScan " + str(e))


	threshold = .9
	FoundShirt = False

	try:
		if np.amax(res) > threshold:
			print("Found Shirts")
			y, x = np.unravel_index(res.argmax(), res.shape)
			FoundShirt = True
	except Exception as e:
		print("Exception: ", e)
		print("Don't have the individual shirts icon or not looking at a stockpile in ItemScan")
		logging.info(str(datetime.datetime.now()) + " Don't have the individual shirts icon or not looking at a stockpile in ItemScan " + str(e))
	
	try:
		if np.amax(resC) > threshold:
			print("Found Shirt Crate")
			y, x = np.unravel_index(resC.argmax(), resC.shape)
			FoundShirt = True
	except Exception as e:
		print("Exception: ", e)
		print("Don't have the shirt crate icon or not looking at a stockpile in ItemScan")
		logging.info(str(datetime.datetime.now()) + " Don't have the shirt crate icon or not looking at a stockpile in ItemScan " + str(e))
	
	if not FoundShirt:
		print("Found nothing.  Either don't have shirt icon(s) or not looking at a stockpile in ItemScan")
		y = 0
		x = 0

	# COMMENT OUT IF TESTING A SPECIFIC IMAGE
	if y == x == 0:
		stockpile = screen
	else:
		stockpile = screen[y - 32:1080, x - 11:x + 589]

	if config.debug.get() == 1:
		cv2.imshow('Stockpile in this image in ItemScan?', stockpile)
		cv2.waitKey(0)
	# UNCOMMENT IF TESTING A SPECIFIC IMAGE
	# stockpile = screen


	# Image clips for each type of stockpile should be in this array below
	StockpileTypes = (
		('CheckImages//Seaport.png', 'Seaport', 0), 
		('Checkimages//StorageDepot.png', 'Storage Depot', 1),
		('Checkimages//Outpost.png', 'Outpost', 2), 
		('Checkimages//Townbase.png', 'Town Base', 3),
		('Checkimages//RelicBase.png', 'Relic Base', 4),
		('Checkimages//BunkerBase.png', 'Bunker Base', 5),
		('Checkimages//Encampment.png', 'Encampment', 6),
		('Checkimages//SafeHouse.png', 'Safe House', 7)
	)


	# Check cropped stockpile image for each location type image
	FoundStockpileType = None
	FoundStockpileTypeName = None
	highestScore = 0
	y = 0
	x = 0
	for image in StockpileTypes:
		try:
			findtype = cv2.imread(image[0], cv2.IMREAD_GRAYSCALE)
			if config.debug.get() == 1:
				cv2.imshow("Looking for this", findtype)
				cv2.waitKey(0)
			if (config.experimentalResizing.get() == 1): 
				findtype = cv2.resize(findtype, (int(findtype.shape[1]*config.best_text_scale), int(findtype.shape[0]*config.best_text_scale)))
			res = cv2.matchTemplate(stockpile, findtype, cv2.TM_CCOEFF_NORMED)
			# Threshold is a bit lower for types as they are slightly see-thru
			typethreshold = .65
			score = np.amax(res)
			if (score > typethreshold and score > highestScore):
				highestScore = score
				y, x = np.unravel_index(res.argmax(), res.shape)
				FoundStockpileType = image[2]
				FoundStockpileTypeName = image[1]
			
		except Exception as e:
			print("Exception: ", e)
			print("Probably not looking at a stockpile or don't have the game open.  Looked for: ", str(image))
			FoundStockpileType = None
			ThisStockpileName = None
			logging.info(str(datetime.datetime.now()) + " Probably not looking at a stockpile or don't have the game open.")
			logging.info(str(datetime.datetime.now()) + " Looked for: ", str(image) + str(e))
			pass
	
	if (FoundStockpileType != None):
		if FoundStockpileTypeName == "Seaport" or FoundStockpileTypeName == "Storage Depot":
			findtab = cv2.imread('CheckImages//Tab.png', cv2.IMREAD_GRAYSCALE)
			if (config.experimentalResizing.get() == 1): 
				findtab = cv2.resize(findtab, (int(findtab.shape[1]*config.best_text_scale), int(findtab.shape[0]*config.best_text_scale)))
			res = cv2.matchTemplate(stockpile, findtab, cv2.TM_CCOEFF_NORMED)
			tabthreshold = .6
			cv2.imwrite('stockpile.jpg', stockpile)
			if np.amax(res) > tabthreshold:
				print("Found the Tab")
				y, x = np.unravel_index(res.argmax(), res.shape)
				# Seaports and Storage Depots have the potential to have named stockpiles, so grab the name
				#print("config.bestTextScale:" + str(config.bestTextScale))
				stockpilename = stockpile[int(y - 5*config.best_text_scale):int(y + 17*config.best_text_scale), int(x - 150*config.best_text_scale):int(x - 8*config.best_text_scale)]
				# Make a list of all current stockpile name images
				currentstockpiles = glob.glob("Stockpiles/*.png")
				# print(currentstockpiles)
				found = 0
				for image in currentstockpiles:
					stockpilelabel = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
					if not image.endswith("image.png"):
						res = cv2.matchTemplate(stockpilename, stockpilelabel, cv2.TM_CCOEFF_NORMED)
						threshold = .97
						flag = False
						if np.amax(res) > threshold:
							# Named stockpile is one already seen
							found = 1
							ThisStockpileName = (image[11:(len(image) - 4)])
				
				if found != 1:
					p = popup(config,"new_stock")
					p.add_stockpile(stockpilename)
					p.popup_window.wait_window()
					new_stockpile_name = config.new_stockpile_name
					if new_stockpile_name == "" or new_stockpile_name.lower() == "public":
						popup("BlankName")
						ThisStockpileName = "TheyLeftTheStockpileNameBlank"
					else:
						# NewStockpileFilename = 'Stockpiles//' + new_stockpile_name + '.png'
						# It's a new stockpile, so save an images of the name as well as the cropped stockpile itself
						cv2.imwrite('Stockpiles//' + new_stockpile_name + '.png', stockpilename)
						if config.ImgExport.get() == 1:
							cv2.imwrite('Stockpiles//' + new_stockpile_name + ' image.png', stockpile)
						ThisStockpileName = new_stockpile_name
			else:
				# It's not a named stockpile, so just call it by the type of location (Bunker Base, Encampment, etc)
				print("Didn't find the Tab, so it looks like it's not a named stockpile")
				ThisStockpileName = FoundStockpileTypeName
		else:
			# It's not a named stockpile, so just call it by the type of location (Bunker Base, Encampment, etc)
			print("Not a named stockpile, it's a Bunker Base, Encampment, something like that")
			ThisStockpileName = FoundStockpileTypeName
		# StockpileName = StockpileNameEntry.get()
		# cv2.imwrite('Stockpiles//' + StockpileName + '.png', stockpilename)
	else:
		# print("Didn't find",image[1])
		print("Doesn't look like any known stockpile type")
		FoundStockpileType = "None"
		ThisStockpileName = "None"
		pass

	# These stockpile types allow for crates (ie: Seaport)
	CrateList = [0, 1]
	# These stockpile types only allow individual items (ie: Bunker Base)
	SingleList = [2, 3, 4, 5, 6, 7]

	start = datetime.datetime.now()

	print(ThisStockpileName)
	if ThisStockpileName == "TheyLeftTheStockpileNameBlank":
		pass
	else:
		if config.Set.get() == 0:
			folder = "default"
		else:
			folder = "modded"
		if ThisStockpileName != "None":
			if config.ImgExport.get() == 1:
				cv2.imwrite('Stockpiles//' + ThisStockpileName + ' image.png', stockpile)
							
			threshold = .98 if (config.experimentalResizing.get() == 1 and config.foxhole_height != 1080) else .96 
			contents = []
			for item in items.data:
				if item.enabled != ButtonState.ENABLED:
	
					continue
				if item.ind_exists!="1":
					if config.debug.get() == 1:
						print("Skipping icon: ", item.name, "because ItemNumbering.csv lists it as impossible/never displayed in stockpile images (like pistol ammo and crates of warheads)")
					continue

				item.set_check_img(FoundStockpileType,folder)

				if config.experimentalResizing.get() == 1:
					item.set_scale(config.bestIconScale,config.bestTextScale)
				try:
					item.get_qnty(stockpile,threshold)
					contents += item.get_contents()

				except Exception as e:
					print("Exception: ", e)
					if config.debug.get() == 1:
						print("Failed while looking for: ", item.name)
						logging.info(str(datetime.datetime.now()) + "Failed while looking for (missing?): ", item.name + str(e))
					pass
			
			# sort by category, then incategory, then by crated, then by quantity
			sortedcontents = list(sorted(contents, key=lambda x: (x[3], x[4], x[5], -x[2])))
			# Here's where we sort stockpilecontents by category, then number, so they spit out the same as screenshot
			# Everything but vehicles and shippables first, then single vehicle, then crates of vehicles, then single shippables, then crates of shippables
			if ThisStockpileName in ("Seaport","Storage Depot","Outpost","Town Base","Relic Base","Bunker Base","Encampment","Safe House"):
				ThisStockpileName = "Public"

			if config.CSVExport.get() == 1:

				stockpilefile = open("Stockpiles//" + ThisStockpileName + ".csv", 'w')
				stockpilefile.write(ThisStockpileName + ",\n")
				stockpilefile.write(FoundStockpileTypeName + ",\n")
				stockpilefile.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ",\n")
				stockpilefile.close()

				# Writing to both csv and xlsx, only the quantity and name is written
				# If more elements from items.data are added to stockpilecontents, they could be added to these exports as fields
				with open("Stockpiles//" + ThisStockpileName + ".csv", 'a') as fp:
					# fp.write('\n'.join('{},{},{}'.format(x[0],x[1],x[2]) for x in stockpilecontents))
					############### THIS ONE DOES IN REGULAR ORDER ############
					# fp.write('\n'.join('{},{}'.format(x[1],x[2]) for x in stockpilecontents))
					############### THIS ONE DOES IN SORTED ORDER #############
					fp.write('\n'.join('{},{}'.format(x[1], x[2]) for x in sortedcontents))
				fp.close()


			if config.updateBot.get() == 1 and ThisStockpileName != "Public":
				requestObj = {
					"password": config.BotPassword.get(),
					"name": ThisStockpileName,
					"guildID": config.BotGuildID.get()
				}
				data = []
				for x in sortedcontents:
					data.append([x[1], x[2]])
				requestObj["data"] = data
				print("Bot Data", data)

				try:
					r = requests.post(config.BotHost.get(), json=requestObj, timeout=10)
					response = r.json()
					
					print("=============== [Storeman Bot Link: Sending to Server] ===============")
					storemanBotPrefix = "[Storeman Bot Link]: "
					if (response["success"]): print(storemanBotPrefix + "Scan of " + ThisStockpileName + " has been received by the server successfully. Your logisitics channel will be updated shortly if you have set one (you can use /spstatus on your server for instant updates")
					elif (response["error"] == "empty-stockpile-name"): print(storemanBotPrefix + "Stockpile name is invalid. Perhaps the stockpile name was not detected or empty.")
					elif (response["error"] == "invalid-password"): print(storemanBotPrefix + "Invalid password, check that the Bot Password is correct.")
					elif (response["error"] == "invalid-guild-id"): print(storemanBotPrefix + "The Guild ID entered was not found on the Storeman Bot server. Please check that it is correct.")
					else: print(storemanBotPrefix + "An unhandled error occured: " + response["error"])

					print("=============== [Storeman Bot Link: End of Request] ===============")
				except Exception as e:
					print("There was an error connecting to the Bot")
					print("Exception: ", e)


			if config.XLSXExport.get() == 1:
				workbook = xlsxwriter.Workbook("Stockpiles//" + ThisStockpileName + ".xlsx")
				worksheet = workbook.add_worksheet()
				worksheet.write(0, 0, ThisStockpileName)
				worksheet.write(1, 0, FoundStockpileTypeName)
				worksheet.write(2, 0, str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
				row = 3
				for col, data in enumerate(items.sortedcontents):
					# print("col", col, " data", data)
					worksheet.write(row + col, 0, data[1])
					worksheet.write(row + col, 1, data[2])
				workbook.close()
				
			print(datetime.datetime.now()-start)

		else:
			popup("NoStockpile")