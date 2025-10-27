from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image
class popup():

    messages = {
        "NoFox":"Foxhole isn't running.\nLaunch Foxhole and retry.",
        "NoStockpile": "Didn't detect stockpile.\nHover over a stockpile on the map and retry.",
        "blank_name": "You must type in the name (which cannot be Public).\nThis field cannot be left blank.\nYou'll need to rescan it.",
        "duplicate_hotkeys": "Warning: If your hotkeys are identical or overlap (ie: F2 and Shift + F2)\nthen it\'s possible that the hotkey will only grab a stockpile image and will not scan.",
        "new_stock":"Looks like a new stockpile."
    }
    def __init__(self,main_obj,message_type):
        self.main = main_obj
        parent = main_obj.main_widget
        root_x = parent.winfo_rootx()
        root_y = parent.winfo_rooty() 
        if root_x == root_y == -32000:
            win_x = 100
            win_y = 100
        else:
            win_x = root_x - 20
            win_y = root_y + 125

        location = "+" + str(win_x) + "+" + str(win_y)

        PopupWindow = Toplevel(parent)
        PopupWindow.geometry(location)
        PopupWindow.resizable(False, False)
        PopupWindow.grab_set()
        PopupWindow.focus_force()

        self.popup_window = PopupWindow

        PopupWindow.bind('<Return>',lambda :self.destroy())

        PopupFrame = ttk.Frame(PopupWindow)
        PopupFrame.pack()
        self.frame = PopupFrame

        label = ttk.Label(PopupFrame, text=self.messages[message_type], style="TLabel")
        label.grid(row=2, column=0)

        OKButton = ttk.Button(PopupFrame, text="OK", command=lambda: self.destroy())
        OKButton.grid(row=10, column=0, sticky="NSEW")
        self.ok = OKButton

    def destroy(self):
        self.popup_window.destroy()

    def name_and_destroy(self):
        self.main.new_stockpile_name = self.stockpile_name_entry.get()
        self.popup_window.destroy()

    def add_stockpile(self,image):
        im = Image.fromarray(image)
        tkimage = ImageTk.PhotoImage(im)

        StockpileNameImage = ttk.Label(self.frame, image=tkimage, style="TLabel")
        StockpileNameImage.image = tkimage
        StockpileNameImage.grid(row=5, column=0)

        StockpileNameLabel = ttk.Label(self.frame, text="What is the name of the stockpile?", style="TLabel")
        StockpileNameLabel.grid(row=7, column=0)

        StockpileNameEntry = ttk.Entry(self.frame)
        StockpileNameEntry.grid(row=8, column=0)
        self.stockpile_name_entry = StockpileNameEntry

        self.popup_window.bind('<Return>',lambda x:self.name_and_destroy())
        self.ok["command"] = lambda:self.name_and_destroy()

