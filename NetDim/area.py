# NetDim
# Copyright (C) 2016 Antoine Fourmy (antoine.fourmy@gmail.com)
# Released under the GNU General Public License GPLv3

from miscellaneous import CustomTopLevel

class Area(object):
    
    class_type = "area"
    
    def __init__(self, name, AS, trunks, nodes):
        self.name = name
        self.AS = AS
        if not trunks:
            trunks = set()
        if not nodes:
            nodes = set()
        self.pa = {"node": nodes, "trunk": trunks}
        # update the AS dict for all objects, so that they are aware they
        # belong to this new area
        for obj in nodes | trunks:
            obj.AS[self.AS].add(self)
        # update the area dict of the AS with the new area
        self.AS.areas[name] = self
        # add the area to the AS management panel area listbox
        self.AS.management.create_area(name)
        
    def add_to_area(self, *objects):
        for obj in objects:
            self.pa[obj.network_type].add(obj)
            obj.AS[self.AS].add(self)
            
    def remove_from_area(self, *objects):
        for obj in objects:
            self.pa[obj.network_type].discard(obj)
            obj.AS[self.AS].discard(self)
            
class CreateArea(CustomTopLevel):
    def __init__(self, asm):
        super().__init__()
        self.geometry("30x65")        
        self.title("Create area")   
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.entry_name = ttk.Entry(self, width=9)
        self.entry_name.grid(row=0, column=0, pady=5, padx=5)
        
        self.button_OK = ttk.Button(self, text="OK", command=lambda: self.create_area(asm))
        self.button_OK.grid(row=1, column=0, pady=5, padx=5, sticky="nsew")
        
    def create_area(self, asm):
        asm.create_area(self.entry_name.get())
        self.destroy()