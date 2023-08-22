from FISQueue import FISQueue
import pandas as pd 

df = pd.read_excel("FIS FINAL ARRIVALS WEAPONS SHEET 01AUG23.xlsx", header=2).iloc[:, :8]

fqm = FISQueue(df, 1, 1, 4, 4)

that = fqm.get_wait_times_fis()



that = fqm.apply_recheck_time(that)

that = fqm.apply_tsa(that)

that.to_csv("fis_enter.csv")
