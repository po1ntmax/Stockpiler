from tkinter import *
from tkinter import ttk
import logging
import datetime
import os
from pynput.mouse import Controller
import threading
import copy

from stockpiler.items import ItemList
from stockpiler.filter_ui import FilterTab
from stockpiler.settings_ui import SettingsTab
from stockpiler.table_ui import TableTab
from stockpiler.order_ui import OrderTab
from stockpiler.search_image import SearchImage
from stockpiler.learn import Learn
from stockpiler.itemscan import ItemScan
# from stockpiler.table_ui import TableTab


class Stockpiler():
	Version = "0.0.1"

	def __init__(self):
		StockpilerWindow = Tk()
		self.main_widget = StockpilerWindow
		StockpilerWindow.title('Stockpiler ' + self.Version)

		# Window width is based on generated UI.  If buttons change, width should change here.
		StockpilerWindow.geometry("537x600")

		# Width locked since button array doesn't adjust dynamically
		StockpilerWindow.resizable(width=False, height=False)
		StockpilerWindow.iconbitmap(default='Bmat.ico')

		self.master_list = ItemList()
		ItemList.master_data = self.master_list.data

		self.experimentalResizing = IntVar()
		self.category = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0]]
		self.faction = [0, 0]
		self.topscroll = 0
		self.learning = BooleanVar(value=False)
		self.BotHost = StringVar()
		self.BotPassword = StringVar()
		self.BotGuildID = StringVar()
		self.CSVExport = IntVar()
		self.updateBot = IntVar()
		self.XLSXExport = IntVar()
		self.ImgExport = IntVar()
		self.debug = IntVar()
		self.Set = IntVar()
		self.Learning = IntVar()
		self.PickerX = -1
		self.PickerY = -1
		self.bindings = list()
		self.grabshift = IntVar()
		self.grabctrl = IntVar()
		self.grabalt = IntVar()
		self.grabhotkey = StringVar()
		self.scanshift = IntVar()
		self.scanctrl = IntVar()
		self.scanalt = IntVar()
		self.scanhotkey = StringVar()
		self.grabhotkeystring = "f2"
		self.scanhotkeystring = "f3"
		self.grabmods = "000"
		self.scanmods = "000"

		self.grabshift.set(0)
		self.grabctrl.set(0)
		self.grabalt.set(0)
		self.scanshift.set(0)
		self.scanctrl.set(0)
		self.scanalt.set(0)
		self.debug.set(0)
		self.experimentalResizing.set(0)

		s = ttk.Style()
		s.theme_use('alt')
		s.configure("EnabledButton.TButton", background="gray")
		s.configure("DisabledButton.TButton", background="red2")
		# Manually disabled button is different color because it is retained regardless of category/faction disable/enable
		s.configure("ManualDisabledButton.TButton", background="red4")
		s.configure("EnabledCategory.TButton", background="gray")
		s.configure("DisabledCategory.TButton", background="red2")
		s.configure("EnabledFaction.TButton", background="gray")
		s.configure("DisabledFaction.TButton", background="red2")
		s.configure("TScrollbar", troughcolor="grey20", arrowcolor="grey20", background="gray", bordercolor="grey15")
		s.configure("TFrame", background="black")
		s.configure("TCanvas", background="black")
		s.configure("TCheckbutton", background="black", foreground="grey75")
		s.configure("TWindow", background="black")
		s.map("TCheckbutton", foreground=[('!active', 'grey75'),('pressed', 'black'),
										('active', 'black'), ('selected', 'green'), ('alternate', 'purple')],
			background=[ ('!active','black'),('pressed', 'grey75'), ('active', 'white'),
						('selected', 'cyan'), ('alternate', 'pink')],
			indicatorcolor=[('!active', 'black'),('pressed', 'black'), ('selected','grey75')],
			indicatorbackground=[('!active', 'green'),('pressed', 'pink'), ('selected','red')])
		s.configure('TNotebook', background="grey25", foreground="grey15", borderwidth=0)
		s.map('TNotebook.Tab', foreground=[('active', 'black'), ('selected', 'black')],
					background=[('active', 'grey80'), ('selected', 'grey65')])
		s.configure("TNotebook.Tab", background="grey40", foreground="black", borderwidth=0)
		s.configure('TRadiobutton', background='black', indicatorbackground='blue',
					indicatorcolor='grey20', foreground='grey75', focuscolor='grey20')
		s.map("TRadiobutton", foreground=[('!active', 'grey75'),('pressed', 'black'), ('active', 'black'),
										('selected', 'green'), ('alternate', 'purple')],
			background=[ ('!active','black'),('pressed', 'grey15'), ('active', 'white'),
						('selected', 'cyan'), ('alternate', 'pink')])
		s.configure("TLabel", background="black", foreground="grey75")

		self.style = s

		self.threads = []
		self.thread_count = 0

		if os.path.exists("Config.txt"):
			with open("Config.txt") as file:
				content = file.readlines()
			content = [x.strip() for x in content]
			try:
				print("Attempting to load from Config.txt")
				logging.info(str(datetime.datetime.now()) + ' Attempting to load from config.txt')
				self.CSVExport.set(int(content[0]))
				self.XLSXExport.set(int(content[1]))
				self.ImgExport.set(int(content[2]))
				self.Set.set(int(content[3]))
				self.Learning.set(int(content[4]))
				self.updateBot.set(int(content[5]))
				self.BotHost.set(content[6])
				self.BotPassword.set(content[7])
				self.BotGuildID.set(content[8])
				if (len(content) >= 13): self.experimentalResizing.set(content[13])
			except Exception as e:
				print("Exception: ", e)
				logging.info(str(datetime.datetime.now()) + ' Loading from config.txt failed, setting defaults')
				self.CSVExport.set(0)
				self.XLSXExport.set(0)
				self.ImgExport.set(1)
				self.Set.set(0)
				self.Learning.set(0)
			try:
				print("Attempting to load hotkeys from config.txt")
				logging.info(str(datetime.datetime.now()) + ' Attempting to load from hotkeys from config.txt')
				self.grabhotkey.set(content[9])
				self.scanhotkey.set(content[10])
				self.grabhotkeystring = self.grabhotkey.get()
				self.scanhotkeystring = self.scanhotkey.get()
				self.grabshift.set(content[11][0])
				self.grabctrl.set(content[11][1])
				self.grabalt.set(content[11][2])
				self.grabmods = str(self.grabshift.get()) + str(self.grabctrl.get()) + str(self.grabalt.get())
				self.scanshift.set(content[12][0])
				self.scanctrl.set(content[12][1])
				self.scanalt.set(content[12][2])
				self.scanmods = str(self.scanshift.get()) + str(self.scanctrl.get()) + str(self.scanalt.get())
			except Exception as e:
				print("Exception: ", e)
				print("Failed to load hotkeys from config.txt, setting them to defaults of f2, f3")
				logging.info(str(datetime.datetime.now()) + ' No custom hotkeys in config.txt, setting defaults of f2, f3')
				self.grabhotkey.set("f2")
				self.scanhotkey.set("f3")
				self.grabhotkeystring = self.grabhotkey.get()
				self.scanhotkeystring = self.scanhotkey.get()
				self.grabshift.set(0)
				self.grabctrl.set(0)
				self.grabalt.set(0)
				self.grabmods = "000"
				self.scanshift.set(0)
				self.scanctrl.set(0)
				self.scanalt.set(0)
				self.scanmods = "000"
		else:
			self.CSVExport.set(0)
			self.XLSXExport.set(0)
			self.ImgExport.set(1)
			self.Set.set(0)
			self.Learning.set(0)

		OuterFrame = ttk.Frame(StockpilerWindow)
		OuterFrame.pack(fill=BOTH, expand=1)
		TabControl = ttk.Notebook(OuterFrame)
		self.notebook = TabControl
		TabControl.pack(expand=1, fill=BOTH)

		filter_ui = FilterTab(self)
		# table_ui = TableTab(self)
		settings_ui = SettingsTab(self)
		settings_ui.set_hotkeys()

		self.table_ui = TableTab(self)
		self.order_ui = OrderTab(self)
	
	def update_results(self,data):
		new_results = ItemList()

		for item in new_results.data:
			qnt = data[item.name]
			item.quantity = qnt

		self.table_ui.results = new_results

		self.table_ui.print_table()

	def run(self):
		self.main_widget.mainloop()

	def scan(self):
		print("scanning")
		screen = SearchImage(self, "", "")
		if self.Learning.get() == 1:
			Learn(self, screen)

		filtered_items = self.master_list.thread_copy()
		args = (screen, self, filtered_items)
		logging.info(str(datetime.datetime.now()) + " Starting scan thread: " + str(self.thread_count))

		thread = threading.Thread(target=ItemScan, args=args)
		thread.daemon=True
		thread.start()
		self.thread_count+=1
		self.threads.append(thread)
		
		thread.join()
		self.table_ui.results = filtered_items
		self.table_ui.print_table()