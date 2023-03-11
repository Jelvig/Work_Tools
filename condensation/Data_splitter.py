import pandas as pd
class CoolerRaw():
    
    def __init__(self, df, destination):

        self.destination = destination
        self.df = df
        self.special = df['type'].unique()

    def RP_split(self):
        #  Creating RP human and mouse split
        if '2' in self.special:
            RP = self.df[self.df['type'] == '2']
            self.RPHs = RP[RP['Description 2'] == 'Hs']
            self.RPMm = RP[RP['Description 2'] == 'Mm']
            self.RPHs = self.RPHs.sort_values(by="Bin Code")
            self.RPMm = self.RPMm.sort_values(by="Bin Code")

            #  Creating RP split for nonhuman
            self.RPnonHs = RP[RP['Description 2'] != 'Hs']
            self.RPnonHs = self.RPnonHs[self.RPnonHs['Description 2'] != 'Mm']
            self.RPnonHs = self.RPnonHs.sort_values(by='Bin Code')
            return self.RPHs, self.RPMm, self.RPnonHs
        else:
            print("No RP's to split")
            self.RPHs = self.RPMm = self.RPnonHs = pd.DataFrame()
            return self.RPHs, self.RPMm, self.RPnonHs
        
            
    def GP_split(self):
        #  Creating GP human/mouse split
        if '3' in self.special:
            GP = self.df[self.df['type'] == '3']
            self.GPHs = GP[GP['Description 2'] == 'Hs']
            self.GPMm = GP[GP['Description 2'] == 'Mm']
            self.GPHs = self.GPHs.sort_values(by="Bin Code")
            self.GPMm = self.GPMm.sort_values(by="Bin Code")

            #  Creating RP split for nonhuman
            self.GPnonHs = GP[GP['Description 2'] != 'Hs']
            self.GPnonHs = self.GPnonHs[self.GPnonHs['Description 2'] != 'Mm']
            self.GPnonHs = self.GPnonHs.sort_values(by='Bin Code')
            return self.GPHs, self.GPMm, self.GPnonHs
        else:
            print("No GP's to split")
            self.GPHs = self.GPMm = self.GPnonHs = pd.DataFrame()
            return self.GPHs, self.GPMm, self.GPnonHs

    def TP_split(self):
        #  Creating TP split to be written
        if '4' in self.special:
            TP = self.df[self.df['type'] == '4']
            self.TP = TP.sort_values(by="Bin Code")
            return self.TP
        else:
            print("No TP's to split")
            self.TP = pd.DataFrame()
            return self.TP
    
    def Micro_split(self):
        # Creating Micro split to be written
        if '5' in self.special:
            Micro = self.df[self.df['type'] == '5']
            self.Micro = Micro.sort_values(by="Bin Code")
            return self.Micro
        else:
            print("No Micro's to split")
            self.Micro = pd.DataFrame()
            return self.Micro
    
    def cooler_split(self):
        self.RPHs, self.RPMm, self.RPnonHs = self.RP_split()
        self.GPHs, self.GPMm, self.GPnonHs = self.GP_split()
        self.TP = self.TP_split()
        self.Micro = self.Micro_split()
        return self.RPHs, self.RPMm, self.RPnonHs, self.GPHs, self.GPMm, self.GPnonHs, self.TP, self.Micro

    def df_writer(self):
        import pandas as pd
        # Writing data frames to seperate sheets in original file, if the dataframe exists
        with pd.ExcelWriter(f"{self.destination}/Raw data.xlsx", engine='xlsxwriter') as writer:
            self.df.to_excel(writer, sheet_name = 'Raw', index=False)
            if "2" in self.special:
                self.RPHs.to_excel(writer, sheet_name='RPHs', index=False)
                self.RPMm.to_excel(writer, sheet_name='RPMm', index=False)
                self.RPnonHs.to_excel(writer, sheet_name='RPnon', index=False)
            if "3" in self.special:
                self.GPHs.to_excel(writer, sheet_name='GPHs', index=False)
                self.GPMm.to_excel(writer, sheet_name='GPMm', index=False)
                self.GPnonHs.to_excel(writer, sheet_name='GPnon', index=False)
            if "4" in self.special:
                self.TP.to_excel(writer, sheet_name='TP', index=False)
            if "5" in self.special:
                self.Micro.to_excel(writer, sheet_name='Micro', index=False)
    
