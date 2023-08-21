from FISQueue import FISQueue
import pandas as pd 

df = pd.read_excel("FIS FINAL ARRIVALS WEAPONS SHEET 01AUG23.xlsx", header=2).iloc[:, :8]

fqm = FISQueue(df, 1, 1, 4, 4)

fqm.get_wait_times_fis().to_csv("fis_enter.csv")
