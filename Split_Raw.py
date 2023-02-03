"""Script made to split Raw data Via cooler clean up into seperate sheets.
This process is generally time consuming and could save use several minutes.
This script also works for Condensations, currently splits human, mouse and other"""
class CoolerRaw():
    def file_path(self):
        from tkinter import filedialog
        import pandas as pd
        # Get the raw file
        self.file = filedialog.askopenfilename(initialdir=r"W:/Production/Probe Oligos/REMP Files/_Rerack Files", title="Choose Raw Cooler Data")
        self.df = pd.read_excel(self.file)
        self.species = self.df['Description 2'] == 'Hs'
        self.mouse = self.df['Description 2'] == 'Mm'

    def unique_types(self):
        # Get the unique values in type column to avoid errors
        self.special = self.df['type'].unique()
    
    def RP_split(self):
        #  Creating RP human and mouse split
        if 2 in self.special:
            RP = self.df['type'] == 2
            RP = self.df.loc[RP]
            self.RPHs = RP.loc[self.species]
            self.RPMm = RP.loc[self.mouse]
            self.RPHs = self.RPHs.sort_values(by="Bin Code")
            self.RPMm = self.RPMm.sort_values(by="Bin Code")

            #  Creating RP split for nonhuman/mouse
            self.RPnew = RP.drop(RP[RP['Description 2'] == 'Hs'].index)
            self.RPnonHs = self.RPnew.drop(self.RPnew[self.RPnew['Description 2'] == 'Mm'].index)
            self.RPnonHs = self.RPnonHs.sort_values(by='Bin Code')
        else:
            print("No RP's to split")
            
    def GP_split(self):
        #  Creating GP human/mouse split
        if 3 in self.special:
            GP = self.df['type'] == 3
            GP = self.df.loc[GP]
            self.GPHs = GP.loc[self.species]
            self.GPMm = GP.loc[self.mouse]
            self.GPHs = self.GPHs.sort_values(by="Bin Code")
            self.GPMm = self.GPMm.sort_values(by="Bin Code")

            #  Creating GP nonhuman split
            self.GPnew = GP.drop(GP[GP['Description 2'] == 'Hs'].index)
            self.GPnonHs = self.GPnew.drop(self.GPnew[self.GPnew['Description 2'] == 'Mm'].index)
            self.GPnonHs = self.GPnonHs.sort_values(by='Bin Code')
        else:
            print("No GP's to split")

    def TP_split(self):
        #  Creating TP split to be written
        if 4 in self.special:
            TP = self.df['type'] == 4
            TP = self.df.loc[TP]
            self.TP = TP.sort_values(by="Bin Code")
        else:
            print("No TP's to split")
    
    def Micro_split(self):
        # Creating Micro split to be written
        if 5 in self.special:
            Micro = self.df['type'] == 5
            Micro = self.df.loc[Micro]
            self.Micro = Micro.sort_values(by="Bin Code")
        else:
            print("No Micro's to split")

    def df_writer(self):
        import pandas as pd

        # Writing data frames to seperate sheets in original file, if the dataframe exists
        with pd.ExcelWriter(self.file, engine='xlsxwriter') as writer:
            self.df.to_excel(writer, sheet_name = 'Raw', index=False)
            if 2 in self.special:
                self.RPHs.to_excel(writer, sheet_name='RPHs', index=False)
                self.RPMm.to_excel(writer, sheet_name='RPMm', index=False)
                self.RPnonHs.to_excel(writer, sheet_name='RPnon', index=False)
            if 3 in self.special:
                self.GPHs.to_excel(writer, sheet_name='GPHs', index=False)
                self.GPMm.to_excel(writer, sheet_name='GPMm', index=False)
                self.GPnonHs.to_excel(writer, sheet_name='GPnon', index=False)
            if 4 in self.special:
                self.TP.to_excel(writer, sheet_name='TP', index=False)
            if 5 in self.special:
                self.Micro.to_excel(writer, sheet_name='Micro', index=False)
    
def main():
    splitter = CoolerRaw()
    splitter.file_path()
    splitter.unique_types()
    splitter.RP_split()
    splitter.GP_split()
    splitter.TP_split()
    splitter.Micro_split()
    splitter.df_writer()

    print('items and species are split')

if '__name__' == main():
    main()
