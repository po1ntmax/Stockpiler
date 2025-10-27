import csv
import os
from tkinter import *
from tkinter import ttk 
import enum
import re
import copy
import cv2
import numpy as np

from stockpiler.tooltip import CreateToolTip

class ButtonState(enum.Enum):
    ENABLED = 0
    MANUAL_DISABLED = 1
    DISABLED = 2
    FACTION_DISABLED = 3

class Item(object):
    
    numbers = {
        "0":cv2.imread('CheckImages//num0.png', cv2.IMREAD_GRAYSCALE), 
        "1":cv2.imread('CheckImages//num1.png', cv2.IMREAD_GRAYSCALE), 
        "2":cv2.imread('CheckImages//num2.png', cv2.IMREAD_GRAYSCALE),
        "3":cv2.imread('CheckImages//num3.png', cv2.IMREAD_GRAYSCALE), 
        "4":cv2.imread('CheckImages//num4.png', cv2.IMREAD_GRAYSCALE), 
        "5":cv2.imread('CheckImages//num5.png', cv2.IMREAD_GRAYSCALE),
		"6":cv2.imread('CheckImages//num6.png', cv2.IMREAD_GRAYSCALE),
        "7":cv2.imread('CheckImages//num7.png', cv2.IMREAD_GRAYSCALE), 
        "8":cv2.imread('CheckImages//num8.png', cv2.IMREAD_GRAYSCALE),
		"9":cv2.imread('CheckImages//num9.png', cv2.IMREAD_GRAYSCALE), 
        "k+":cv2.imread('CheckImages//numk.png', cv2.IMREAD_GRAYSCALE)
    }
    
    headers = [
        "id",
        "i",
        "c",
        "name",
        "nickname",
        "subType",
        "ammo",
        "faction",
        "stockpile_category",
        "custom_category",
        "category_sort",
        "in_category_sort",
        "ind_exists",
        "crate_exists",
        "per_crate",
        "bmats",
        "emats",
        "rmats",
        "hemats",
        "relicmats"
    ]

    def __init__(self,row_data):
        for i,h in enumerate(self.headers):
            self.__setattr__(h,row_data[i])

        file_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(os.path.dirname(file_dir))
        self.img_paths = {
            "modded": os.path.join(root_dir,"CheckImages","Modded",self.id+".png"),
            "default":os.path.join(root_dir,"CheckImages","Default",self.id+".png"),
            "modded_c":os.path.join(root_dir,"CheckImages","Modded",self.id+"C.png"),
            "default_c":os.path.join(root_dir,"CheckImages","Default",self.id+"C.png")
        }
        self.icon = os.path.join(root_dir,"UI",str(self.id)+".png")
        self.quantity = 0
        self.c_quantity = 0
        self.icon_scale=1
        self.text_scale=1
 
        self.enabled = ButtonState.ENABLED
        if os.path.exists(self.icon):
            self.img = PhotoImage(file = os.path.abspath(self.icon))

    def make_btn(self,frame):
        if os.path.exists(self.icon):
            self.btn = ttk.Button(
                frame, 
                image=self.img, 
                style="EnabledButton.TButton",
                command=lambda: self.toggle()
            )
        else:
            return
        self.btn.image = self.img
        self.ttp = CreateToolTip(self.btn,re.sub('\'', '', self.name))
        return self.btn
            

    def toggle(self):
        # toggle is designed to work only if the category and faction are turned on

        if self.enabled == ButtonState.ENABLED:

            self.enabled = ButtonState.MANUAL_DISABLED
            self.btn.config(style="ManualDisabledButton.TButton")
        elif self.enabled == ButtonState.MANUAL_DISABLED:
            self.enabled = ButtonState.ENABLED
            self.btn.config(style="EnabledButton.TButton")

    def set_check_img(self,stockpile_type,tag):
        self.tag = tag
        self.search_crates=False
        self.search_normal=False
            
        if stockpile_type in [0,1]:
            if self.crate_exists:
                self.search_crates=True
            if self.stockpile_category=="Vehicle"or self.stockpile_category=="Shippable":
                self.search_normal= True
        else:
            self.search_normal=True

    def set_scales(self,icon_scale,text_scale):
        self.icon_scale=icon_scale
        self.text_scale = text_scale
        new_numbers = {}
        for number,image in Item.numbers.items():
            new_numbers[number]=cv2.resize(
                    image, 
                    (int(image.shape[1] * icon_scale), int(image.shape[0] * icon_scale))
                )
            
        self.numbers=new_numbers

    def get_qnty(self,stockpile,threshold):
        if self.search_normal:
            img_path = self.img_paths[self.tag]
            if not os.path.exists(img_path):
                self.quantity=0
            else:
                findimage = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if self.icon_scale != 1.0: 
                    findimage = cv2.resize(
                        findimage, 
                        (int(findimage.shape[1] * self.icon_scale), int(findimage.shape[0] * self.icon_scale)), 
                        interpolation=cv2.INTER_LANCZOS4
                    )
                self.quantity=self.__get_qnty(findimage,stockpile,threshold)

        if self.search_crates:
            img_path = self.img_paths[self.tag+"_c"]
            if not os.path.exists(img_path):
                self.c_quantity=0
            else:
                findimage = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if self.icon_scale != 1.0: 
                    findimage = cv2.resize(
                        findimage, 
                        (int(findimage.shape[1] * self.icon_scale), int(findimage.shape[0] * self.icon_scale)), 
                        interpolation=cv2.INTER_LANCZOS4
                    )
                self.c_quantity = self.__get_qnty(findimage,stockpile,threshold)

    def __get_qnty(self,icon,stockpile,threshold):
        
        res = cv2.matchTemplate(stockpile, icon, cv2.TM_CCOEFF_NORMED)
					
        if np.amax(res) > threshold:
						
            y, x = np.unravel_index(res.argmax(), res.shape)
						# Found a thing, now find amount

            numberarea = stockpile[
                int(y+8*self.text_scale):int(y+28*self.text_scale), 
                int(x+45*self.text_scale ):int(x+87*self.text_scale)
            ]

            numberlist = []
            for number in range(10):
                number_name = str(number)
                number_img = self.numbers[number_name]
                
                resnum = cv2.matchTemplate(numberarea, number_img, cv2.TM_CCOEFF_NORMED)

                threshold = .9
                x_pos = np.where(resnum >= threshold)[1]
                # It only looks for up to 3 of each number for each item, since after that it would be a "k+" scenario, which never happens in stockpiles
                # This will need to be changed to allow for more digits whenever it does in-person looks at BB stockpiles and such, where it will show up to 5 digits

                numberlist+=[(x,number_name) for x in x_pos]

            numberlist.sort(key=lambda y: y[0])

            number_string = "".join([nl[1] for nl in numberlist])
            quantity = int(number_string)						

            k_res = cv2.matchTemplate(numberarea, self.numbers["k+"] , cv2.TM_CCOEFF_NORMED)
            if np.amax(k_res) > threshold:
                quantity=quantity*1000
            return quantity
        else:
            return 0
        
    def get_contents(self):
        contents = []
        if self.quantity!=0:
            contents.append([self.id, self.name, self.quantity,self.category_sort, self.in_category_sort,0])
        if self.c_quantity!=0:
            contents.append([self.id, self.name+" Crate", self.c_quantity, self.category_sort, self.in_category_sort,1])
        
        return contents





class ItemList():

    stockpilecontents = []
    sortedcontents = []
    slimcontents = []
    ThisStockpileName = ""
    FoundStockpileTypeName = ""
    UIimages = []
    master_data = []
    
	
    def __init__(self):
        self.data = []
        with open('ItemNumberingnew.csv', 'rt') as f_input:
            csv_input = csv.reader(f_input, delimiter=',')
            # Skips first line
            header = next(csv_input)
            # Skips reserved line
            reserved = next(csv_input)
            for rowdata in csv_input:
                item_i = Item(rowdata)
                self.data.append(item_i)


        with open('Filter.csv', 'rt') as f_input:
            csv_input = csv.reader(f_input, delimiter=',')
            # Skips first line
            header = next(csv_input)
            for rowdata in csv_input:
                print(rowdata)
                try:
                    item_id = int(rowdata[0])
                    print(item_id)
                except:
                    continue
                try:
                    enable_status = int(rowdata[1])
                    self.data[item_id].enabled = ButtonState(enable_status)
                except ValueError:
                    print("valueError",item_id)
                    self.data[item_id].enabled = ButtonState.DISABLED


    def filter(self,filter_dict):

        out_data = []
        for d in self.data:
            matched = True
            for k,v in filter_dict.items():
                if getattr(d,k)!=v:
                    matched = False
                    break
            if matched:
                out_data.append(d)
        return out_data
    
    def factionToggle(self,faction,state):
        for item in self.data:
            if item.faction == faction:
                item.enabled = state

    def categoryToggle(self,category,state):
        for item in self.data:
            if item.stockpile_category == category:
                item.enabled = state

    def thread_copy(self):
        new_list = copy.copy(self)
    
        for i in range(len(self.data)):
            new_list.data[i]=copy.copy(self.data[i])
        
        return new_list

category_mapping = {
    "Small Arms":[
        "Rifle",
        "Automatic Rifle",
        "Machine Gun",
        "Misc. Small Arms",
        "Light Kinetic Ammo",
        "Heavy Kinetic Ammo",
        "Light Grenade"
    ],
    "Heavy Arms":[
        "20mm Weaponry",
        "AT Weaponry",
        "Mortar Weaponry",
        "30mm Weaponry",
        "Heavy Grenade",
        "Incindiary"
    ],
    "Heavy Ammunition":[
        "Artillery Shells",
        "Tank Munitions",
        "Anti Ship",
        "Rocket Ammunition"
    ],
    "Utility":[
        "Engineering",
        "Intelligence",
        "Demolition",
        "Misc. Equipment",
        "Incindiary"
    ],
    "Medical":[
        "Medical",
    ],
    "Resource":[
        "Materials",
        "Raw Materials",
        "Tech Mats",
        "Fuel",
        "Assembly Materials",
        "Construction Materials",
    ],
    "Uniforms":[
        "Assault Uniforms",
        "Engineering Uniforms",
        "Recon Uniforms",
    ],
    "Vehicle":[
        "Utility",
        "Armor",
        "Light Armor",
        "Heavy Armor",
        "Field Gun",
        "Scout",
        "Rocket",
        "Aquatic",
    ],
    "Shippables":[
        "Logistics",
        "Emplacement",
        "Naval",
        "Large Structure",
        "Ballistic",
    ],
}