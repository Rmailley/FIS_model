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
    global number_entries, df, fqm, flights, flight_menu, curr_flight
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
    flights=list(fqm.fltnum_eta.keys())
    flight_menu.destroy()

    flight_menu = tk.OptionMenu(
        app,
        curr_flight,

        *flights,
        command=edit_flt,

    )

    flight_menu.grid(row=3, column=1, padx=5, pady=5)

         


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

l =  ["Global Entry", "MPC", "US Citz", "Intl Visitors"]

number_entries = []
for i in range(4):
    label = tk.Label(app, text=l[i])
    label.grid(column = i, row= 1, padx=5, pady=5)
    number_entry = tk.Entry(app, width=10)
    number_entries.append(number_entry)
    number_entry.grid(column=i, row=2, padx=5, pady=5)


edit_flights_label = tk.Label(app, text="Edit Flight ETA's:")
edit_flights_label.grid(row=3, column=0, pady=10)


def edit_flt(slatt):
    global curr_flight

    print(curr_flight.get())
    


if "flights" not in globals():

    flights = [None]

curr_flight = tk.StringVar(app)
curr_flight.set('No Flight Selected')
flight_menu = tk.OptionMenu(
    app,
    curr_flight,

    *flights,
    command=edit_flt,

)

flight_menu.grid(row=3, column=1, padx=5, pady=5)

fltentry = tk.Entry(app)
fltentry.grid(column=2, row=3)
def submitf():

    global fqm, curr_flight
    newentry = fltentry.get()
    
    if (int(newentry) < 1300) | (int(newentry) > 2300):
        messagebox.showerror("Error", "Please submit valid time ")
        fltentry.delete(0,'end')
        return
    flightnum = int(curr_flight.get())
    try:
        fqm.fltnum_eta[flightnum] = pd.Timestamp(year=1900, month=1, day=1, hour=int(newentry[:2]), minute=int(newentry[2:]))
    except KeyError:
        print("bad flight")

    
    fltentry.delete(0,'end')
    

submitbutton = tk.Button(
    app,
    text="Submit change",
    command=submitf
)
submitbutton.grid(column=3, row=3, padx=5)

def get_connection_data():
    pass

get_connect_data_button = tk.Button(app, text="Get connection data", command=get_connection_data)
get_connect_data_button.grid(column=5, row=, sticky="se")

app.mainloop()