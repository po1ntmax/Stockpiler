from tkinter import ttk
from tkinter import *
import os
import re
import logging
import datetime
from tksheet import Sheet

from stockpiler.items import ButtonState, category_mapping
from stockpiler.tooltip import CreateToolTip
from stockpiler.items import ItemList

class TableTab():
    def __init__(self,main_widget):
        parent_notebook = main_widget.notebook
        self.parent_widget = main_widget
        self.tab = ttk.Frame(parent_notebook)
        parent_notebook.add(self.tab, text="Results")
        
        self.canvas = Canvas(self.tab)
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

        scrollbar = ttk.Scrollbar(self.tab, orient=VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(scrollregion=self.canvas.bbox('all'), yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.pack(side=TOP, fill=BOTH, expand=1)
        
        self.frame = ttk.Frame(self.canvas)
        self.frame.grid_columnconfigure(0,weight=1)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw", height="1000p", width="402p")
        self.results = ItemList()

        self.print_table()

    def print_table(self):
        data = self.results
        file_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(os.path.dirname(file_dir))
        row = 0
        column = 0
        for i,(category,custom_categories) in enumerate(category_mapping.items()):

            catimg = PhotoImage(file=os.path.join(root_dir,"UI","cat" + str(i+1) + ".png"))
            cat_label = ttk.Label(self.frame, image=catimg,text=category,width=402)
            cat_label.grid(row=row, column=column, sticky="NSEW")
            cat_label.image = catimg
            row+=1
			
            for custom_category in custom_categories:
                items_i = data.filter({"custom_category":custom_category,"stockpile_category":category})
                print_items = []
                for item in items_i:
                    if item.quantity!=0:
                        print_items.append(item)
                if len(print_items)==0:
                    continue
                height = 45*len(print_items)
                cc_text = ttk.Label(master=self.frame,text=custom_category,width=402)
                cc_text.grid(row=row, column=0, sticky="ew")
                row+=1
                ResultSheet = Sheet(self.frame, data=(data),height=height)
                ResultSheet.enable_bindings()
                ResultSheet.grid(row=row, sticky="nsew")
                ResultSheet.set_options(table_bg="grey75", header_bg="grey55", index_bg="grey55", top_left_bg="grey15", frame_bg="grey15")
                row+=1
				

            catsep = ttk.Separator(self.frame, orient=HORIZONTAL)
            catsep.grid(row=row, columnspan=8, sticky="ew", pady=10)
            row+=1



