import tkinter as tk
from tkinter import filedialog, messagebox
from FISQueue import FISQueue
import pandas as pd
import numpy as np
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
    global number_entries, df, fqm, flights, flight_menu, curr_flight, flight_menu_select
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

    flight_menu_select = tk.OptionMenu(
        app,
        flight_for_data,

        *flights,
        command=edit_flt,

    )

    flight_menu_select.grid(row=6, column=0,)

         


app = tk.Tk()
app.geometry("700x350")
app.title('FISConnects')

app.rowconfigure(list(range(25)), minsize=25)
app.columnconfigure([0,1,2,3,4], minsize=5)


filename_var = tk.StringVar()
saved_filename = ""

open_button = tk.Button(app, width=10, text="Open File", command=open_file)


filename_label = tk.Label(app, textvariable=filename_var)

open_button.grid(row=0, column=0)
filename_label.grid(row=0, column=24)

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

    curr_flight.set(str(slatt))

    print(curr_flight)
    


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

flight_for_data = tk.StringVar(app, "No Flight Selected")
def get_connection_data():
    global fqm, cnx_gate, gates, pax_status
    thisf = int(flight_for_data.get())
    print("hello")
    arrival_time = fqm.fltnum_eta[thisf]

    waittimes = fqm.get_wait_times_fis()

    waittimes = fqm.apply_recheck_time(waittimes)

    waittimes = fqm.apply_tsa(waittimes)

    waittimes = fqm.apply_wtg(waittimes, cnx_gate, gates)

    slc = list(waittimes.loc[arrival_time])

    weights = [.04,.16,.55,.23]
    wavg = np.dot(weights, slc)/np.sum(weights)

    nt = arrival_time + pd.Timedelta(minutes=wavg)

    nts = str(nt.hour) + ":" + str(nt.minute)


    statement = f"The anticipated through time for passengers by type is as follows: \n MPC:{slc[0]} Global Entry: {slc[1]}, US Citizens: {slc[2]}, Intl Visitors: {slc[3]} \n The weighted average through time for all pax types is {int(wavg)} minutes. \n Anticipated time at gate: {nts} "

    pax_status.set(statement)

    tk.Label(app, text=pax_status.get()).grid(column=3,row=6)
    
    




get_connect_data_button = tk.Button(app, text="Get connection data", command=get_connection_data)
get_connect_data_button.grid(column=2, row=6, sticky="se")

if 'cnx_gate' not in globals():
    cnx_gate = None

def gateselector_help(arg):
    global cnx_gate
    cnx_gate = arg

gates = {
    "A Gates": 15,
    "Low C Gates": 2,
    "High C Gates": 4,
    "Low D Gates" : 8,
    "Middle D Gates": 10,
    "High D Gates" : 15,
    "Z Gates" : 15

}

gatevar = tk.StringVar(app, "A Gates")

gateselect = tk.OptionMenu(
    app,
    gatevar,
    *list(gates.keys()),
    command=gateselector_help

)
gateselect.grid(column=1, row=6)

pax_status = tk.StringVar(app)

    

app.mainloop()