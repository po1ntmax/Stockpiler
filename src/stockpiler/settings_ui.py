
from tkinter import ttk
from tkinter import *
from global_hotkeys import *

from stockpiler.tooltip import CreateToolTip
from stockpiler.popup import popup

class SettingsTab():
	def __init__(self,main_widget):
		parent_notebook = main_widget.notebook
		self.parent_widget = main_widget
		self.tab = ttk.Frame(parent_notebook)
		parent_notebook.add(self.tab, text="Settings")
		self.canvas = Canvas(self.tab)
		self.canvas.pack(side=TOP, fill=BOTH, expand=1)


		self.frame = ttk.Frame(self.canvas)
		self.canvas.create_window((0, 0), window=self.frame, anchor="nw", height="500p", width="402p")
		self.frame.columnconfigure(0, weight=1)
		self.frame.columnconfigure(7, weight=1)

		row = 0
		GrabImageEntryLabel = ttk.Label(self.frame, text="Grab Stockpile Image:")
		GrabImageEntryLabel.grid(row=row, column=0)

		GrabImageEntry = ttk.Entry(self.frame, textvariable=main_widget.grabhotkey, width=10)
		GrabImageEntry.grid(row=row, column=1)
		GrabImageEntry.delete(0, 'end')
		GrabImageEntry.insert(0, main_widget.grabhotkeystring)
		GrabImageEntry_ttp = CreateToolTip(GrabImageEntry, 'Available hotkeys are: all letters, numbers, function keys (as f#)'
														', backspace, tab, clear, enter, pause, caps_lock, escape, space, '
														'page_up, page_down, end, home, up, down, left, right, select, print, '
														'print_screen, insert, delete, help, numpad numbers (as numpad_#), '
														'separator_key (pipe key), multiply_key, add_key, subtract_key, '
														'decimal_key, divide_key, num_lock, scroll_lock, and symbols '
														'(+ - ` , . / ; [ ] \')')
		
		GrabShiftCheck = ttk.Checkbutton(self.frame, text="Shift?", variable=main_widget.grabshift)
		GrabShiftCheck.grid(row=row, column=2)

		GrabCtrlCheck = ttk.Checkbutton(self.frame, text="Ctrl?", variable=main_widget.grabctrl)
		GrabCtrlCheck.grid(row=row, column=3)

		GrabAltCheck = ttk.Checkbutton(self.frame, text="Alt?", variable=main_widget.grabalt)
		GrabAltCheck.grid(row=row, column=4)


		row += 1
		ScanEntryLabel = ttk.Label(self.frame, text="Scan Stockpile:")
		ScanEntryLabel.grid(row=row, column=0)

		ScanEntry = ttk.Entry(self.frame, textvariable=main_widget.scanhotkey, width=10)
		ScanEntry.grid(row=row, column=1)
		ScanEntry.delete(0, 'end')
		ScanEntry.insert(0, main_widget.scanhotkeystring)
		ScanEntry_ttp = CreateToolTip(ScanEntry, 'Available hotkeys are: all letters, numbers, function keys (as f#)'
														', backspace, tab, clear, enter, pause, caps_lock, escape, space, '
														'page_up, page_down, end, home, up, down, left, right, select, print, '
														'print_screen, insert, delete, help, numpad numbers (as numpad_#), '
														'separator_key (pipe key), multiply_key, add_key, subtract_key, '
														'decimal_key, divide_key, num_lock, scroll_lock, and symbols '
														'(+ - ` , . / ; [ ] \')')
		
		ScanShiftCheck = ttk.Checkbutton(self.frame, text="Shift?", variable=main_widget.scanshift)
		ScanShiftCheck.grid(row=row, column=2)

		ScanCtrlCheck = ttk.Checkbutton(self.frame, text="Ctrl?", variable=main_widget.scanctrl)
		ScanCtrlCheck.grid(row=row, column=3)

		ScanAltCheck = ttk.Checkbutton(self.frame, text="Alt?", variable=main_widget.scanalt)
		ScanAltCheck.grid(row=row, column=4)

		row += 1
		ResetHotkeysButton = ttk.Button(self.frame, text="Reset Hotkeys", command=self.reset_hotkeys)
		ResetHotkeysButton.grid(row=row, column=0, columnspan=8, pady=1)
		ResetHotkeys_ttp = CreateToolTip(ResetHotkeysButton, 'Some combinations may not work, like Ctrl + Shift + F-keys.\n'
															'This button will reset the hotkeys to default.  Remember to '
															'save your settings.')
		row += 1
		self.separator(row)

		row += 1
		SetLabel = ttk.Label(self.frame, text="Icon set?", style="TLabel")
		SetLabel.grid(row=row, column=0)
		DefaultRadio = ttk.Radiobutton(self.frame, text="Default", variable=main_widget.Set, value=0)
		DefaultRadio.grid(row=row, column=1)
		ModdedRadio = ttk.Radiobutton(self.frame, text="Modded", variable=main_widget.Set, value=1)
		ModdedRadio.grid(row=row, column=2)

		row += 1
		self.separator(row)

		row += 1
		LearningCheck = ttk.Checkbutton(self.frame, text="Learning Mode?", variable=main_widget.Learning)
		LearningCheck.grid(row=row, column=0, columnspan=2)
		
		row += 1
		self.separator(row)

		row += 1
		CSVCheck = ttk.Checkbutton(self.frame, text="CSV?", variable=main_widget.CSVExport)
		CSVCheck.grid(row=row, column=0)
		XLSXCheck = ttk.Checkbutton(self.frame, text="XLSX?", variable=main_widget.XLSXExport)
		XLSXCheck.grid(row=row, column=1)
		ImgCheck = ttk.Checkbutton(self.frame, text="Image?", variable=main_widget.ImgExport)
		ImgCheck.grid(row=row, column=2)

		row += 1
		self.separator(row)

		row += 1
		SendBotCheck = ttk.Checkbutton(self.frame, text="Send To Bot?", variable=main_widget.updateBot)
		SendBotCheck.grid(row=row, column=0, rowspan=2, padx=5)
		SendBotCheck_ttp = CreateToolTip(SendBotCheck, 'Send results to Storeman-Bot Discord Bot?')
		BotHostLabel = ttk.Label(self.frame, text="Bot Host:")
		BotHostLabel.grid(row=row, column=2)
		BotHost = ttk.Entry(self.frame, textvariable=main_widget.BotHost)
		BotHost.grid(row=row, column=3, columnspan=2)
		BotHost_ttp = CreateToolTip(BotHost, 'Host is http://<your Storeman-Bot server IP>:8090')

		row += 1
		BotPasswordLabel = ttk.Label(self.frame, text="Password:")
		BotPasswordLabel.grid(row=row, column=2)
		BotPassword = ttk.Entry(self.frame, textvariable=main_widget.BotPassword)
		BotPassword.grid(row=row, column=3, columnspan=2)
		BotPassword.config(show="*")
		BotPassword_ttp = CreateToolTip(BotPassword, 'Password is set with bot using /spsetpassword command in Discord')

		row += 1
		BotGuildIDLabel = ttk.Label(self.frame, text="GuildID:")
		BotGuildIDLabel.grid(row=row, column=2)
		BotGuildIDLabel_ttp = CreateToolTip(BotGuildIDLabel, 'Only use if you are using a multi-server instance.  If you are using a public instance of Storeman Bot, this is your Discord\'s "Guild ID"')
		BotGuildID = ttk.Entry(self.frame, textvariable=main_widget.BotGuildID)
		BotGuildID.grid(row=row, column=3, columnspan=2)
		BotGuildID_ttp = CreateToolTip(BotGuildID, 'Only use if you are using a multi-server instance.  If you are using a public instance of Storeman Bot, this is your Discord\'s "Guild ID"')

		row += 1
		self.separator(row)

		row += 1
		ObnoxiousCheck = ttk.Checkbutton(self.frame, text="  Obnoxious\ndebug mode?", variable=main_widget.debug)
		ObnoxiousCheck.grid(row=row, column=0, rowspan=2, padx=5)
		ObnoxiousCheck = ttk.Checkbutton(self.frame, text="  Experimental Resizing", variable=main_widget.experimentalResizing)
		ObnoxiousCheck.grid(row=row, column=1, rowspan=2, padx=5)

		row +=1
		row +=1
		save_img = PhotoImage(file="UI/Save.png")
		save_btn = ttk.Button(self.frame, image=save_img, command=self.get_save_settings_func())

		save_btn.image = save_img
		save_btn.grid(row=row, column=0, columnspan=8, pady=5)
		SaveButton_ttp2 = CreateToolTip(save_btn, 'Save Current Filter and Export Settings')


	def separator(self,row):
		setsep = ttk.Separator(self.frame, orient=HORIZONTAL)
		setsep.grid(row=row, columnspan=8, sticky="ew", pady=10)

	def reset_hotkeys(self):
		self.parent_widget.grabshift.set(0)
		self.parent_widget.grabctrl.set(0)
		self.parent_widget.grabalt.set(0)
		self.parent_widget.grabmods = "000"
		self.parent_widget.grabhotkey.set("f2")
		self.parent_widget.grabhotkeystring = "f2"
		self.parent_widget.scanshift.set(0)
		self.parent_widget.scanctrl.set(0)
		self.parent_widget.scanalt.set(0)
		self.parent_widget.scanmods = "000"
		self.parent_widget.scanhotkey.set("f3")
		self.parent_widget.scanhotkeystring = "f3"

	def set_hotkeys(self):
		clear_hotkeys()
		keys = []
		if self.parent_widget.scanmods[0] == "1":
			keys.append("shift")
		if self.parent_widget.scanmods[1] == "1":
			keys.append("control")
		if self.parent_widget.scanmods[2] == "1":
			keys.append("alt")
		keys.append(self.parent_widget.scanhotkeystring)
		
		
		bindings = [
			[keys,None,lambda :self.parent_widget.scan()]
		]
		register_hotkeys(bindings)
		start_checking_hotkeys()


	def get_save_settings_func(self):
		def out_func():
			with open("Config.txt", "w") as exportfile:
				exportfile.write(str(self.parent_widget.CSVExport.get()) + "\n")
				exportfile.write(str(self.parent_widget.XLSXExport.get()) + "\n")
				exportfile.write(str(self.parent_widget.ImgExport.get()) + "\n")
				exportfile.write(str(self.parent_widget.Set.get()) + "\n")
				exportfile.write(str(self.parent_widget.Learning.get()) + "\n")
				exportfile.write(str(self.parent_widget.updateBot.get()) + "\n")
				exportfile.write(str(self.parent_widget.BotHost.get()) + "\n")
				exportfile.write(str(self.parent_widget.BotPassword.get()) + "\n")
				exportfile.write(str(self.parent_widget.BotGuildID.get()) + "\n")
				exportfile.write(str(self.parent_widget.grabhotkey.get()) + "\n")
				exportfile.write(str(self.parent_widget.scanhotkey.get()) + "\n")
				self.parent_widget.grabhotkeystring = self.parent_widget.grabhotkey.get()
				self.parent_widget.scanhotkeystring = self.parent_widget.scanhotkey.get()
				exportfile.write(str(self.parent_widget.grabshift.get()) + str(self.parent_widget.grabctrl.get()) + str(self.parent_widget.grabalt.get()) + "\n")
				exportfile.write(str(self.parent_widget.scanshift.get()) + str(self.parent_widget.scanctrl.get()) + str(self.parent_widget.scanalt.get()) + "\n")
				exportfile.write(str(self.parent_widget.experimentalResizing.get()) + "\n")
			self.parent_widget.grabmods = str(self.parent_widget.grabshift.get()) + str(self.parent_widget.grabctrl.get()) + str(self.parent_widget.grabalt.get())
			self.parent_widget.scanmods = str(self.parent_widget.scanshift.get()) + str(self.parent_widget.scanctrl.get()) + str(self.parent_widget.scanalt.get())
			self.set_hotkeys()
		return out_func