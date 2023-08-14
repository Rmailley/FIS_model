import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

class Selector:
    def __init__(self, win) -> None:
        self.filename = tk.StringVar(win, "No File Selected")

    def selectworker(self):
        filepath = askopenfilename(
            filetypes=[("Excel Files", "*.xlsx")]
        )
        if not filepath:
            return
        
        self.filename.set(filepath)

window = tk.Tk()
window.geometry("500x300")
window.title("FISConnects")


window.rowconfigure(0, minsize=5)
window.columnconfigure([0,1,2], minsize=5)

select = Selector(window)

print(select.filename)


    

fileselect = tk.Button(
    master= window,
    text= "Select File",
    width=5,
    height=2,
    command=select.selectworker
)

run = tk.Button(
    master= window,
    text= "Run Analysis",
    width=6,
    height=2

)

currfile = tk.Label(
    master=window,
    textvariable= select.filename
)

fileselect.grid(sticky='nw')
run.grid(column=1, row = 0, sticky='nw')
currfile.grid(row=0, column=2, sticky='nw')


window.mainloop()