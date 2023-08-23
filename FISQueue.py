import pandas as pd
import numpy as np
import datetime as dt
from datetime import datetime
import math


class FISQueue():

    DEPLANEMENT_PER_MIN = 20


    def __init__(self, df, GE, MPC, INTL, CITZ) -> None:
        #self.df = dataframe
        self.GE = GE
        self.MPC = MPC
        self.INTL = INTL
        self.CITZ = CITZ
        self.df = df
        self.DEPLANEMENT_PER_MIN = 20

        

        #df = pd.read_excel("FIS FINAL ARRIVALS WEAPONS SHEET 01AUG23.xlsx", header=2).iloc[:, :8]
        
        # Chop Input excel file 

        def chop_endrow(df):
            df = df.iloc[2:]
            endrow = list(df['GATE*']).index("TOTAL=")
            return df.iloc[:endrow]

        # Drop Precleared and sole iab
        def drop_precleared(df):
            df = df.drop(df.loc[df["FIS PAX*"] == "PRECLEAR"].index) # type: ignore
            return df[df["FIS PAX*"] > 0] # changed from IAB
        
        def manipulate_times(df):
        # apply some transformations 
            df["ETA*"] = df["ETA*"].apply(lambda x: str(x)[:4])
            df['ETA*'] = df["ETA*"].apply(lambda x: datetime.strptime(x, "%H%M"))
            return df
       
        def build_dicts(df):

            # TODO: Flight to gate then apply walk time to eta, also build in capability to change etas
            df['deplane time'] = (df['IAB PAX*']+df["FIS PAX*"])/17
            df["fisratio"] = df['FIS PAX*']/(df['IAB PAX*']+df["FIS PAX*"])

            flt_ratio = dict(zip(df['FLIGHT*'], df['fisratio']))

            planecap = dict(zip(df['FLIGHT*'], df['FIS PAX*'].add(df["IAB PAX*"])))

            fltnum_deplane_time = dict(zip(df["FLIGHT*"], df["deplane time"]))
            fltnum_eta = dict(zip(df["FLIGHT*"], df["ETA*"]))

            return df, flt_ratio, planecap, fltnum_deplane_time, fltnum_eta

        def get_dt_indices():
            timelist = pd.date_range(start='1900-01-01 13:00', end='1900-01-01 21:00', freq='1min').to_list()
            indices = list(range(len(timelist)))
            return dict(zip(timelist, indices))
        
        self.dt_to_inx = get_dt_indices()

        def get_start_time_inx(fltnum):
            ts = self.fltnum_eta[fltnum]
            return self.dt_to_inx[ts]
        
        self.df = chop_endrow(self.df)
        self.df = drop_precleared(self.df)
        self.df = manipulate_times(self.df)
        self.df, self.flt_ratio, self.planecap, self.fltnum_deplane_time, self.fltnum_eta = build_dicts(self.df)


        def edit_fltnum_eta(self, flt, eta):
            if type(eta) != int:
                return

            if flt in self.fltnum_eta:
                self.fltnum_eta[flt] = eta
            else:
                return
            
        def get_eta(self, flt):
            return self.fltnum_eta[flt]
            


        def get_list_deplanement(flt):
            
            cap = self.planecap[flt]
            tlist = [self.DEPLANEMENT_PER_MIN for i in range(math.floor(cap/self.DEPLANEMENT_PER_MIN))]
            remainder = cap - sum(tlist)
            tlist.append(remainder)
            return tlist
        
        # define a function that pads a list with zeros
        def pad_list(lst, k, n):
            # convert the list to a numpy array
            arr = np.array(lst)
            # calculate the number of zeros to add before and after the array
            before = k
            after = n - k - len(arr)
            # check if the padding is valid
            if before < 0 or after < 0:
                return "Invalid padding"
            # pad the array with zeros using np.pad()
            padded_arr = np.pad(arr, (before, after), mode="constant", constant_values=0)
            # convert the padded array back to a list
            padded_lst = padded_arr.tolist()
            # return the padded list
            return padded_lst
        
        def get_lists(flights):
            deplanement_matrix = []
            for flightnum in flights:
                flt_deplanements = get_list_deplanement(flightnum)
                
                
                fisratio = self.flt_ratio[flightnum]
                
                
                
                padded_list = pad_list(flt_deplanements, get_start_time_inx(flightnum),len(self.dt_to_inx.keys()))

                nppad = np.array(padded_list)*fisratio
                
                padded_list = list(np.ceil(nppad))
                deplanement_matrix.append(padded_list)
            
            return deplanement_matrix
        
        def final_step(df):
            lists = get_lists(df['FLIGHT*'])

            ndf = pd.DataFrame(pd.date_range(start='1900-01-01 13:00', end='1900-01-01 21:00', freq='1min'))
            pmin = list(pd.DataFrame(lists).sum())
            ndf["pax/min"] = pmin

            # ndf.to_excel("permin.xlsx")


            return ndf

        self.ndf = final_step(self.df)

    def get_wait_times_fis(self):

        df = self.ndf

        breakdown = {
            "MPC" : .0463,
            "GE" : 0.1636,
            "US" : 0.5528,
            "NONUS" : 0.2373
        }

        processing_time = { # minutes/pax
            "MPC" : .462,
            "GE" : 0.34,
            "US" : 0.403,
            "NONUS" : 1.3
        }

        throughput = {
            "MPC" : 1/.462,
            "GE" : 1/.34,
            "US" : 1/.403,
            "NONUS" : 1/1.3
        }

        pax_entering = pd.DataFrame(df[0])

        pax_entering['MPC'] = df['pax/min'] * breakdown['MPC']
        pax_entering['GE'] = df['pax/min'] * breakdown['GE']
        pax_entering['US'] = df['pax/min'] * breakdown['US']
        pax_entering['NONUS'] = df['pax/min'] * breakdown['NONUS']

        pax_exiting = pd.DataFrame(df[0])

        

        pax_exiting['MPC'] = pd.Series([throughput['MPC'] for i in range(len(df[0]))])
        pax_exiting['GE'] = pd.Series([throughput['GE'] for i in range(len(df[0]))])
        pax_exiting['US'] = pd.Series([throughput['US'] for i in range(len(df[0]))])
        pax_exiting['NONUS'] = pd.Series([throughput['NONUS'] for i in range(len(df[0]))])

        paxinqueue = pd.DataFrame(df[0])

        mpc = [0 for i in range(len(df[0]))]
        ge = [0 for i in range(len(df[0]))]
        us = [0 for i in range(len(df[0]))]
        nonus =  [0 for i in range(len(df[0]))]

        for i in range(1, len(df[0])):
            
            if mpc[i-1] + pax_entering['MPC'][i] <=0:
                 mpc[i] = max(0, mpc[i-1] + pax_entering['MPC'][i] - pax_exiting['MPC'][i] * (self.MPC -1))
                 us[i] = max(0, us[i-1] + pax_entering['US'][i] - pax_exiting ['US'][i] * (self.CITZ+1)) 
        
        
            
            else:
                mpc[i] = max(0, mpc[i-1] + pax_entering['MPC'][i] - pax_exiting['MPC'][i] * self.MPC)
                us[i] = max(0, us[i-1] + pax_entering['US'][i] - pax_exiting ['US'][i] * self.CITZ) 

            if us[i-1] + pax_entering['US'][i] <=0:
                us[i] = max(0, us[i-1] + pax_entering['US'][i] - pax_exiting ['US'][i]*(self.CITZ-2)) 
                nonus[i] = max(0, nonus[i-1] + pax_entering['NONUS'][i] - pax_exiting ['NONUS'][i] * (self.INTL+2))
            else:
                us[i] = max(0, us[i-1] + pax_entering['US'][i] - pax_exiting ['US'][i]*self.CITZ) 
                nonus[i] = max(0, nonus[i-1] + pax_entering['NONUS'][i] - pax_exiting ['NONUS'][i]*self.INTL)

            ge[i] = max(0, ge[i-1] + pax_entering['GE'][i] - pax_exiting ['GE'][i] * self.GE) 
            
            

       

        paxinqueue['MPC'] = mpc
        paxinqueue['GE'] = ge
        paxinqueue['US'] = us
        paxinqueue['NONUS'] = nonus



        waittime = paxinqueue.copy()

        waittime["GE"] = np.ceil(paxinqueue["GE"] * processing_time['GE'] / self.GE)            
        waittime["MPC"] = np.ceil(paxinqueue["MPC"] * processing_time['MPC'] / self.MPC)
        waittime["US"] = np.ceil(paxinqueue["US"] * processing_time['US'] / self.CITZ)
        waittime["NONUS"] = np.ceil(paxinqueue["NONUS"] * processing_time['NONUS'] / self.INTL)


        return waittime
    

    def apply_recheck_time(self, df):
        df = df.set_index(df.columns[0])
        for col in df.columns:
            df[col] = df[col] + 3

        return df

    def apply_tsa(self, df):
        
        for col in df.columns:
            df[col] = df[col] + 12

        return df
    
    def apply_wtg(self, gate):
        pass





        
if __name__ == '__main__':
    pass
        
