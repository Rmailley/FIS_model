import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

class Selector:
    def __init__(self, win) -> None:
        self.filename = tk.StringVar(win)
        self.filename.set('No File Selected')
        self.filename.trace_add("write")
        self.str_fn = None

    def selectworker(self):
        filepath = askopenfilename(
            filetypes=[("Excel Files", "*.xlsx")]
        )
        if not filepath:
            return
        
        self.filename.set(filepath)
        self.str_fn=filepath

window = tk.Tk()
window.geometry("1000x600")
window.title("FISConnects")


window.rowconfigure(0, minsize=5)
window.columnconfigure([0,1,2], minsize=5)

select = Selector(window)




    

fileselect = tk.Button(
    master= window,
    text= "Select File",
    width=10,
    height=2,
    command=select.selectworker
)

run = tk.Button(
    master= window,
    text= "Run Analysis",
    width=10,
    height=2

)

currfile = tk.Label(
    master=window,
    textvariable= select.filename
)

fileselect.grid(sticky='nw')
run.grid(column=1, row = 0, sticky='nw')
currfile.grid(row=0, column=2, sticky='nw')
print(select.str_fn)

window.mainloop()