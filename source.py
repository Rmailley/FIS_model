import tkinter as tk
from tkinter import filedialog, messagebox
from FISQueue import FISQueue
import pandas as pd
import tksheet
import openpyxl

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        filename_var.set(file_path)
        global saved_filename, df
        saved_filename = file_path

        if saved_filename:
            df = pd.read_excel(saved_filename, )
            new_header = list(df.iloc[1].fillna(0))
            df = df.iloc[2:]
            df.columns = new_header
            


def run_analysis():
    global number_entries, df
    numbers = []
    for resp in number_entries:
        try:
            numbers.append(int(resp.get()))
        except:
            messagebox.showerror("Error", "Please enter positive numbers")
            return


    if df is None:
        messagebox.showerror("Error", "Please Select a file")
        return 
    
    fqm = FISQueue(df, *numbers)

    

    print(numbers)

    
    


app = tk.Tk()
app.geometry("1000x600")
app.title('FISConnects')

app.rowconfigure(0, minsize=10)
app.columnconfigure([0,1,2,3,4], minsize=5)


filename_var = tk.StringVar()
saved_filename = ""

open_button = tk.Button(app, width=10, text="Open File", command=open_file)


filename_label = tk.Label(app, textvariable=filename_var)

open_button.grid(sticky="nw")
filename_label.grid(row=0, column=4)

run = tk.Button(app, text="Run Analysis", width=10, command=run_analysis)
run.grid(row=0, column=1)

df = None

ge, mpc, us, intl = 0,0,0,0

l =  ["ge", "mpc", "us", "intl"]

number_entries = []
for i in range(4):
    label = tk.Label(app, text=l[i])
    label.grid(column = i, row= 1, padx=5, pady=5)
    number_entry = tk.Entry(app, width=10)
    number_entries.append(number_entry)
    number_entry.grid(column=i, row=2, padx=5, pady=5)


fltdata = 
    

    




app.mainloop()