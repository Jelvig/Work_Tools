from .Query import Query
from .Data_splitter import CoolerRaw

class Operator:

    def basic_info(self):
        from tkinter import filedialog

        self.destination = filedialog.askdirectory(title="Choose Working Folder", initialdir=r'W:\Production\Probe Oligos\REMP Files\_Re-Rack Files')
        while True:
            probe = str(input("1. RP\n2. GP\n3. TP\n4. CoolerCleanUp\n->"))
            if str.isdigit(probe) == True:
                if int(probe) in [1, 2, 3, 4]:
                    self.probe = int(probe)
                    break
                else:
                    print('Please choose 1, 2, 3 or 4')
            else:
                print('That is not a number, try again')

        if self.probe in [1,2]:
            while True:
                species = str(input("1. Hs\n2. Mm\n3. Other\n4. All\n->"))
                if str.isdigit(species) == True:
                    if int(species) in [1, 2, 3, 4]:
                        self.species = int(species)
                        break
                    else:
                        print('Please choose 1, 2, or 3')
                else:
                    print('That is not a number, try again')
        if self.probe in [1,2,3]:    
            while True:
                target = str(input('How many targets:'))
                if str.isdigit(target) == True:
                    if int(target) > 30:
                        print("Sorry, but I can't allow anything over 30")
                    else:
                        self.target = int(target)
                        break
                else:
                    print('That is not a number, try again')
    
    def stream(self):
        import pandas as pd
        if self.probe == 1:
            class_query = Query(self.species, self.target)
            self.df = class_query.rp()
            binto_drop = self.df['shelfcode'].iloc[-1]
            self.df = self.df[self.df.shelfcode != binto_drop]
            class_splitter = CoolerRaw(self.df, self.destination)
            self.RPHs, self.RPMm, self.RPnon =  class_splitter.RP_split()
            class_splitter.df_writer()
        if self.probe == 2:
            class_query = Query(self.species, self.target)
            self.df = class_query.gp()
            binto_drop = self.df['shelfcode'].iloc[-1]
            self.df = self.df[self.df.shelfcode != binto_drop]
            class_splitter = CoolerRaw(self.df, self.destination)
            self.GPHs, self.GPMm, self.GPnon =  class_splitter.GP_split()
            class_splitter.df_writer()
        if self.probe == 3:
            self.species = 3
            class_query = Query(self.species, self.target)
            self.df = class_query.tp()
            binto_drop = self.df['shelfcode'].iloc[-1]
            self.df = self.df[self.df.shelfcode != binto_drop]
            class_splitter = CoolerRaw(self.df, self.destination)
            self.TP =  class_splitter.TP_split()
            class_splitter.df_writer()
        if self.probe == 4:
            class_query = Query()
            self.df = class_query.coolercleanup()  
            class_splitter = CoolerRaw(self.df, self.destination)
            self.RPHs, self.RPMm, self.RPnonHs, self.GPHs, self.GPMm, self.GPnonHs, self.TP, self.Micro =  class_splitter.cooler_split()
            class_splitter.df_writer()

    def insert_bins(self):
        from math import ceil
        species_list = ['Human','Mouse','Nonspecies']
        species_count = 0
        if self.probe == 1:
            rp_list = [self.RPHs, self.RPMm, self.RPnon]
            for i in rp_list:
                if i.empty == False:
                    count = 0
                    num_bins = ceil(len(i.index)/96)
                    print(f'Enter {num_bins} {species_list[species_count]} Bin Codes')
                    species_count += 1
                    bin_codes = []
                    while count != num_bins:
                        bin = str(input('->'))
                        if len(bin) == 9:
                            bin_codes.append(bin)
                            count += 1
                        else:
                            print('Try again')
                    i.toBinCode = self.serialize(i, bin_codes)
                else:
                    species_count += 1
        if self.probe == 2:
            gp_list = [self.GPHs, self.GPMm, self.GPnon]
            for i in gp_list:
                if i.empty == False:
                    count = 0
                    num_bins = ceil(len(i.index)/96)
                    print(f'Enter {num_bins} {species_list[species_count]} Bin Codes\n')
                    species_count += 1
                    bin_codes = []
                    while count != num_bins:
                        bin = str(input('->'))
                        if len(bin) == 9:
                            bin_codes.append(bin)
                            count += 1
                        else:
                            print('Try again')
                    i.toBinCode = self.serialize(i, bin_codes)
                else:
                    species_count += 1
        if self.probe == 3:
            if self.TP.empty == False:
                count = 0
                num_bins = ceil(len(self.TP.index)/96)
                print(f'Enter {num_bins} TP Bin Codes\n')
                bin_codes = []
                while count != num_bins:
                    bin = str(input('->'))
                    if len(bin) == 9:
                        bin_codes.append(bin)
                        count += 1
                    else:
                        print('Try again')
                self.TP.toBinCode = self.serialize(self.TP, bin_codes)
            else:
                print('TP dataframe appears to be empty')
        if self.probe == 4:
            coolerspecies_list = ['RP Human','RP Mouse','RP Nonspecies', 'GP Human','GP Mouse','GP Nonspecies', 'TP','Micro']
            cooler_list = [self.RPHs, self.RPMm, self.RPnonHs, self.GPHs, self.GPMm, self.GPnonHs, self.TP, self.Micro]
            for i in cooler_list:
                if i.empty == False:
                    count = 0
                    num_bins = ceil(len(i.index)/96)
                    print(f'Enter {num_bins} {coolerspecies_list[species_count]} Bin Codes\n')
                    species_count += 1
                    bin_codes = []
                    while count != num_bins:
                        bin = str(input('->'))
                        if len(bin) == 9:
                            bin_codes.append(bin)
                            count += 1
                        else:
                            print('Try again')
                    i.toBinCode = self.serialize(i, bin_codes)
                else:
                    species_count += 1

    def serialize(self, df, bin_codes):
        """creates 'tobincode' location for the same amount of lines as the dataframe"""
        letters = ['A','B','C','D','E','F','G','H']
        data = []
        i=0

        for bin in bin_codes:
            for num in range(1,13):
                for let in letters:
                    data.append(f"{bin}-{let}{str(num).zfill(2)}")
                    if len(data) == len(df.index):
                        return data
                    else:    
                        i+=1
        
    def export_ranges(self):
        import pandas as pd
        header = ['Item', 'Lot', 'Bin Code', 'toBinCode', 'Qty', 'UMOC']
        if self.probe == 1:
            rp_list = [self.RPHs, self.RPMm, self.RPnon]
            df_upload = pd.concat(rp_list)
            df_upload.to_csv(f"{self.destination}/upload.csv", index=False, columns=header, header=False)
            for i in rp_list:
                row = 0
                row2 = 95
                if i.empty == False:
                    while True:
                        if row2 > len(i.index):
                            row2 = len(i.index) - 1
                            print(f"{i.iat[row,0]}...{i.iat[row2,0]}")
                            break
                        else:
                            print(f"{i.iat[row,0]}...{i.iat[row2,0]}")
                            row = row2 + 1
                            row2 += 96
        if self.probe == 2:
            gp_list = [self.GPHs, self.GPMm, self.GPnon]
            df_upload = pd.concat(gp_list)
            df_upload.to_csv(f"{self.destination}/upload.csv", index=False, columns=header, header=False)
            for i in gp_list:
                row = 0
                row2 = 95
                if i.empty == False:
                    while True:
                        if row2 > len(i.index):
                            row2 = len(i.index) - 1
                            print(f"{i.iat[row,0]}...{i.iat[row2,0]}")
                            break
                        else:
                            print(f"{i.iat[row,0]}...{i.iat[row2,0]}")
                            row = row2 + 1
                            row2 += 96
                else:
                    continue
        if self.probe == 3:
            self.TP.sort_values(by=['toBinCode'])
            self.TP.to_csv(f"{self.destination}/upload.csv", index=False, columns=header, header=False)
            row = 0
            row2 = 95
            while True:
                if row2 > len(self.TP.index):
                    row2 = len(self.TP.index) - 1
                    print(f"{self.TP.iat[row,0]}...{self.TP.iat[row2,0]}")
                    break
                else:
                    print(f"{self.TP.iat[row,0]}...{self.TP.iat[row2,0]}")
                row = row2 + 1
                row2 += 96
        if self.probe == 4:
            cooler_list = [self.RPHs, self.RPMm, self.RPnonHs, self.GPHs, self.GPMm, self.GPnonHs, self.TP, self.Micro]
            df_upload = pd.concat(cooler_list)
            df_upload.to_csv(f"{self.destination}/upload.csv", index=False, columns=header, header=False)
            for i in cooler_list:
                row = 0
                row2 = 95
                if i.empty == False:
                    while True:
                        if row2 > len(i.index):
                            row2 = len(i.index) - 1
                            print(f"{i.iat[row,0]}...{i.iat[row2,0]}")
                            break
                        else:
                            print(f"{i.iat[row,0]}...{i.iat[row2,0]}")
                            row = row2 + 1
                            row2 += 96
                else:
                    continue



                    

