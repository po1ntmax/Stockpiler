import pygetwindow as gw
import cv2
import numpy as np
from PIL import ImageTk, ImageGrab, Image
import datetime
import logging

from stockpiler.match_template_best_scale import matchTemplateBestScale

def SearchImage(config, Pass, LearnImage):
	screen = None

	if Pass != "":
		screen = LearnImage
	else:
		try:

			if (config.experimentalResizing.get() == 1):
				print("==============EXPERIMENTAL RESIZING==============")
				window = gw.getWindowsWithTitle("War")
				if (len(window) > 0):
					foxhole_height = window[0].height - 39
					foxhole_width = window[0].width - 16
					config.foxhole_height = foxhole_height
				else:
					print("[Warning: !!!] Foxhole window not detected")
				print(f"Foxhole screen size is: {foxhole_width}x{foxhole_height}")
				width_ratio = foxhole_width / 1920 
				height_ratio = foxhole_height / 1080
				print(f"Screen Ratio to original 1920x1080: {width_ratio}x{height_ratio}")
				
			# OKAY, so you'll have to grab the whole screen, detect that thing in the upper left, then use that as a basis
			# for cropping that full screenshot down to just the foxhole window
			screen = np.array(ImageGrab.grab(bbox=None, include_layered_windows=False, all_screens=True))
			screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

			numbox = cv2.imread('CheckImages//StateOf.png', cv2.IMREAD_GRAYSCALE)
			

			best_score = None
			res = None
			if (config.experimentalResizing.get() == 1):
				if (foxhole_height == 1080): bestTextScale = 1.0
				elif (not bestTextScale):
					best_score, bestTextScale, res = matchTemplateBestScale(screen, numbox, foxhole_height, numtimes=20)
			else:
				bestTextScale = 1.0
			
			config.best_text_scale = bestTextScale
			if (not best_score):
				if (config.experimentalResizing.get() == 1): 
					numbox = cv2.resize(
						numbox, 
						(int(numbox.shape[1]*bestTextScale), int(numbox.shape[0]*bestTextScale))
					)
				
				res = cv2.matchTemplate(screen, numbox, cv2.TM_CCOEFF_NORMED)
				best_score = np.amax(res)
			
			print("Best scale for TEXT is: " + str(bestTextScale) + " with a score of: " + str(best_score))
			

			threshold = .7
			if best_score > threshold:
				min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
				statex, statey = max_loc
				margin_y_ratioed = 35 * height_ratio
				margin_x_ratioed = 244 * height_ratio
				if statey - margin_y_ratioed >= 0:
					statey = statey - margin_y_ratioed
				else:
					statey = 0
				if statex - margin_x_ratioed >= 0:
					statex = statex - margin_x_ratioed
				else:
					statex = 0
				
				screen = screen[int(statey):int(statey + (1079 * height_ratio)), int(statex):int(statex + (1919 * width_ratio))]

				print("It thinks it found the window position in SearchImage and is grabbing location: X:", str(statex),
					  " Y:", str(statey))
				if config.debug.get() == 1:
					cv2.imshow('Grabbed in SearchImage', screen)
					cv2.waitKey(0)
			else:
				print("State of the War not found in SearchImage.  It may be covered up or you're not on the map.")
				if config.debug.get() == 1:
					cv2.imshow('Grabbed in SearchImage, did NOT find State of War', screen)
					cv2.waitKey(0)


		except Exception as e:
			print("Exception: ", e)
			print("Failed to grab the screen in SearchImage")
			logging.info(str(datetime.datetime.now()) + " Failed Grabbing the screen in SearchImage " + str(e))
	return screen

