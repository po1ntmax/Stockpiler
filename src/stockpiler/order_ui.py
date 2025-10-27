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

class OrderTab():
    def __init__(self,main_widget):
        parent_notebook = main_widget.notebook
        self.parent_widget = main_widget
        self.tab = ttk.Frame(parent_notebook)
        parent_notebook.add(self.tab, text="Logistics Order")
        
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
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw", height="7000p", width="390p")
        self.results = ItemList()

        self.print_table()

    def print_table(self):
        data = self.results
        file_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(os.path.dirname(file_dir))
        row = 0
        column = 0

        self.stockpile_var = StringVar()

        choose_stockpile_label = ttk.Label(self.frame,text="Destination Stockpile")
        choose_stockpile_label.grid(column=0,row=row)
        row+=1

        choose_stockpile = ttk.Combobox(self.frame,textvariable=self.stockpile_var)
        choose_stockpile.grid(column=0,row=row)
        row+=1
        
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
                    print_items.append(item)
                if len(print_items)==0:
                    continue

                height = 25*len(print_items)+25
                cc_text = ttk.Label(master=self.frame,text=custom_category,width=402)
                cc_text.grid(row=row, column=0, sticky="ew")
                row+=1
                table = [[print_item.name, 0] for print_item in print_items]
                ResultSheet = Sheet(
                    self.frame, 
                    data=(table),
                    height=height,
                    headers=["Item","Amount"],
                    total_rows=len(table)
                )
                ResultSheet.enable_bindings()
                ResultSheet.set_column_widths([200,75])
                
                ResultSheet.grid(row=row, sticky="nsew")
                ResultSheet.set_options(table_bg="grey75", header_bg="grey55", index_bg="grey55", top_left_bg="grey15", frame_bg="grey15")
                row+=1
				

            catsep = ttk.Separator(self.frame, orient=HORIZONTAL)
            catsep.grid(row=row, columnspan=8, sticky="ew", pady=10)
            row+=1

        submit_but = ttk.Button(self.frame,text="Submit",command=lambda : self.submit_order())
        submit_but.grid(row=row, columnspan=8, sticky="ew", pady=10)
        row+=1

    def submit_order(self):
        pass