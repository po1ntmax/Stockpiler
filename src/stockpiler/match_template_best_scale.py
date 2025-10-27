import cv2
import numpy as np
def matchTemplateBestScale(screen, icon, foxhole_height, method=cv2.TM_CCOEFF_NORMED, numtimes=10):

	print("Finding best scale to resize icons, this may take a while...")
	best_score = -np.inf
	best_scale = None
	final_res = None

	scales=None
	if (foxhole_height < 1080):
		scales = np.linspace(0.5, 1.0, numtimes)[::-1]
	else:
		scales = np.linspace(1.0, 2.0, numtimes)[::-1]

	for scale in scales:
        # resize the icon according to the scale
		icon_resized = cv2.resize(icon, (int(icon.shape[1]*scale), int(icon.shape[0]*scale)))

        # if the resized icon is larger than the screen, skip this scale
		if icon_resized.shape[0] > screen.shape[0] or icon_resized.shape[1] > screen.shape[1]:
			continue
	
		res = cv2.matchTemplate(screen, icon_resized, method)
		score = np.amax(res)
        
		if score > best_score:
			best_score = score
			best_scale = scale
			final_res = res

	return best_score, best_scale, final_res