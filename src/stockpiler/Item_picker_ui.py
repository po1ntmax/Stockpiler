from tkinter import ttk
from tkinter import *
import os
import re
import logging
import datetime
from PIL import ImageTk,Image
import cv2

from stockpiler.tooltip import CreateToolTip
from stockpiler.items import ButtonState, category_mapping

class ItemPicker():		
	def __init__(self,main_obj,image):
		main_obj.learning.set(False)
		self.main_obj = main_obj
		root_x = main_obj.main_widget.winfo_rootx()
		root_y = main_obj.main_widget.winfo_rooty()
		if main_obj.PickerX != -1:
			win_x = main_obj.PickerX
			win_y = main_obj.PickerY
		elif root_x == root_y == -32000:
			win_x = 20
			win_y = 20
		elif root_x < 20:
			win_x = 20
			win_y = 20
		else:
			# This window is so big in its current form that it just needs to be further in the corner
			win_x = root_x - 20
			win_y = root_y - 20

		location = "+" + str(win_x) + "+" + str(win_y)
		window = Toplevel(main_obj.main_widget)
		self.window = window
		window.geometry("537x600"+location)
		canvas = Canvas(window)


		def _on_mousewheel(event):
			canvas.yview_scroll(int(-1*(event.delta/120)), "units")

		canvas.bind_all("<MouseWheel>", _on_mousewheel)

		scrollbar = ttk.Scrollbar(window, orient=VERTICAL, command=canvas.yview)
		scrollbar.pack(side="right", fill="y")

		canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scrollbar.set)
		canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

		canvas.pack(side=LEFT, fill=BOTH, expand=1)
		frame = ttk.Frame(canvas)
		canvas.create_window((0, 0), window=frame, anchor="nw", height="3800p", width="567p")
		window.resizable(False, False)

		iconrow = iconcolumn = 0

		NewIconLabel = ttk.Label(frame, text="What item is this?")
		NewIconLabel.grid(row=iconrow, column=0, columnspan=8)
		iconrow += 1
		self.image = image
		im = Image.fromarray(image)
		# tkimage = ImageTk.PhotoImage(im)
		# NewIconImage = ttk.Label(frame, image=tkimage)
		# NewIconImage.image = image
		# NewIconImage.grid(row=iconrow, column=0)
		
		bigim = im.resize(size=(200, 200), resample=Image.NEAREST)
		tkimagebig = ImageTk.PhotoImage(bigim)
		
		BigIconImage = ttk.Label(frame, image=tkimagebig)
		BigIconImage.image = tkimagebig
		BigIconImage.grid(row=iconrow, column=1, columnspan=4)
		
		iconrow += 1
		crate_or_ind = IntVar()
		crate_or_ind.set(1)
		crate = ttk.Radiobutton(frame,text="Crate",variable=crate_or_ind,value=1)
		individual = ttk.Radiobutton(frame,text="Individual",variable=crate_or_ind,value=2)
		self.crate_or_ind = crate_or_ind
		crate.grid(row = iconrow, column=0)
		individual.grid(row = iconrow, column=4)
		iconrow += 1

		self.item_list = main_obj.master_list

		file_dir = os.path.dirname(os.path.abspath(__file__))
		root_dir = os.path.dirname(os.path.dirname(file_dir))

		column = 0
		for i,(category,custom_categories) in enumerate(category_mapping.items()):

			catimg = PhotoImage(file=os.path.join(root_dir,"UI","cat" + str(i+1) + ".png"))
			cat_label = ttk.Label(frame, image=catimg)
			cat_label.grid(row=iconrow, column=column, sticky="NSEW", columnspan=8)
			cat_label.image = catimg

			iconrow+=1
			
			for custom_category in custom_categories:

				cc_text = ttk.Label(master=frame,text=custom_category)
				cc_text.grid(row=iconrow, columnspan=8, sticky="ew")
				iconrow+=1

				items_i = self.item_list.filter({"custom_category":custom_category,"stockpile_category":category})

				for item in items_i:
					if hasattr(item,"img"):
						if column >= 8:
							iconrow += 1
							column = 0
						item_btn = item.make_btn(frame)

						if item_btn:
							item_btn.grid(row=iconrow, column=column, sticky="W", padx=2, pady=2)
							item_btn["command"] = lambda id=item.id: self.item_selected(id)
						column += 1
				iconrow+=1
				column = 0

			catsep = ttk.Separator(frame, orient=HORIZONTAL)
			catsep.grid(row=iconrow, columnspan=8, sticky="ew", pady=10)
			iconrow+=1

	def item_selected(self,id):
		if self.crate_or_ind.get() == 1:
			name = str(id) + "C.png"
		elif self.crate_or_ind.get() == 2:
			name = str(id) + ".png"
		else:
			print("no radio button selected")
		if self.main_obj.Set.get() == 0:
			save = 'CheckImages//Default//' + name
		else:
			save = 'CheckImages//Modded//' + name
		print("save:", save)
		cv2.imwrite(save, self.image)
		self.window.destroy()
		self.main_obj.learning.set(True)
