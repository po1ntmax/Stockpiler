import numpy as np
import cv2
import os

from stockpiler.Item_picker_ui import ItemPicker
def Learn(config, screen):

	numbox = cv2.imread('CheckImages//NumBox.png', cv2.IMREAD_GRAYSCALE)
	res = cv2.matchTemplate(screen, numbox, cv2.TM_CCOEFF_NORMED)
	threshold = .99
	config.learning.set(True)
	if np.amax(res) > threshold:
		numloc = np.where(res >= threshold)
		print("found them here:", numloc)
		print(len(numloc[0]))
		for spot in range(len(numloc[0])):
			# Stockpiles never displayed in upper left under State of the War area
			# State of the War area throws false positives for icons
			if numloc[1][spot] < (1920 * .25) and numloc[0][spot] < (1080 * .24):
				pass

			else:
				print("x:", numloc[1][spot], " y:",numloc[0][spot])

				# cv2.imshow('icon', screen[int(numloc[0][spot]+2):int(numloc[0][spot]+36), int(numloc[1][spot]-38):numloc[1][spot]-4])
				# cv2.waitKey(0)

				currenticon = screen[int(numloc[0][spot]+2):int(numloc[0][spot]+36), int(numloc[1][spot]-38):numloc[1][spot]-4]
				print("currenticon:", currenticon.shape)
				if config.Set.get() == 0:
					folder = "CheckImages//Default//"
				else:
					folder = "CheckImages//Modded//"
				Found = False
				for imagefile in os.listdir(folder):

					checkimage = cv2.imread(folder + imagefile, cv2.IMREAD_GRAYSCALE)
					print("Checking for ", str(imagefile))
					result = cv2.matchTemplate(currenticon, checkimage, cv2.TM_CCOEFF_NORMED)
					threshold = .99
					if np.amax(result) > threshold:
						#print("Found:", imagefile)
						Found = True
						break
				if not Found:
					print("Not found, should launch IconPicker")
					picker = ItemPicker(config,currenticon)
					config.main_widget.wait_window(picker.window)
					# config.main_widget.wait_variable(config.learning)


	else:
		print("Found no numboxes, which is very strange")
		if config.debug.get() == 1:
			cv2.imshow("No numboxes?", screen)
			cv2.waitKey(0)