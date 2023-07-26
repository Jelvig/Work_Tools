"""This is to create uploads and put them on the desktop for evaluation,
    any codeset with subfolders will not work, e.g., panels or whales"""

class Upload:
    def __init__(self):
        self.codesets = []

    def menu(self):
        """create a list of CodeSets that will run through the program for needed information"""
        self.codesets = []
        while True:
            codeset = input("Enter CodeSet name:\n").strip()
            if codeset != '':
                self.codesets.append(codeset)
            else:
                break

    def item_getter(self):
        """indexes for codeset names within item card tracking, records it and uses its (max) location to find the up-to-date
        item number for the production orders"""
        import pandas as pd
        master = pd.read_excel(r"W:\Production\Probe Oligos\Oligo Tools\Item Card Tracking.xlsx", sheet_name ='Custom CodeSets', usecols=[0,3])
        for codeset in self.codesets:    
            try:
                lst = master.index[master['CodeSet Name'] == codeset].tolist()
                point = max(lst)
            except Exception:
                print(f'Something went wrong with {codeset}')
            else:
                num = master.iloc[point, 1]
                print(f'''name: {codeset}\nItem number: {num}\n____________________________''')

    def make_folder(self):
        """Makes a new folder on desktop to relocate needed folders"""
        import os
        from datetime import datetime

        #make folder on desktop with name and date
        today = datetime.today()
        folder = 'uploads_' + today.strftime('%Y%m%d')
        destination = os.path.join('C:/Users/jelvig/Desktop/' + folder)
        if os.path.isdir(destination) == True:
            print('upload file exists')
        else:
            os.makedirs(destination)
            print(destination + ' has been created')
        return destination

    def get_comp(self, codeset):
        """this function finds the comparison files in proper folder,
            if a there is a panel, it takes a different route to get both
            comparison files"""
        import glob as glob
        try:
            comp = glob.glob("W:\Production\Probe Oligos\REMP Files\_Re-Rack Files\*" + codeset + "*\*_comparison.txt")
        except IndexError:
                print(f"can't find {codeset} comparison file")
        return comp
    
    def get_opf(self, codeset):
        """this function finds the path to the codeset folder to find each opf, and then
            moves it to the new folder on your desktop"""
        import glob as glob
        try:
            files = glob.glob("Z:/" + codeset + "/production/" + codeset + "_rp_opf.csv")
            files2 = glob.glob("Z:/" + codeset + "/production/" + codeset + "_gp_opf.csv")
            files.extend(files2)
        except:
            print(f"something went wrong with {codeset}")

        else:
            return files

    def folder_check(self, codeset):
        """ Checking to see if folders exist in this path
            if it does, it creates new folder with the date, if not the path is created"""
        import os
        from datetime import datetime
        now = datetime.now()
        date = "%04d_%02d%02d" % (now.year,now.month,now.day)
        path = "W:/Production/ERP/CodeSet OPFs with lot numbers/" + codeset +"/"
        if os.path.isdir(path) == True:
            folder = codeset +' ('+date+')'
            newpath = os.path.join(path + folder)
            if os.path.isdir(newpath) == False:
                os.mkdir(newpath)
                print(codeset + ' had a folder')
            else:
                print(f"{codeset} has a subfolder")
        elif os.path.isdir(path) == False:
            os.mkdir(path)

    def create(self, codeset, comp, opfs, destination):
        import pandas as pd
        import shutil
        try:
            comp_list = pd.read_csv(comp[0],header=None, index_col=None)
        except:
            print(f'{codeset} comparison or file not found')
        else:
            comp_list = comp_list[2].tolist()
            middle_index = len(comp_list)//2
            rp = pd.read_csv(opfs[0], header=None, index_col=None)
            gp = pd.read_csv(opfs[1], header=None, index_col=None)
        try:
            rp['blank'], rp['lots'] = ' ', comp_list[:middle_index]
            gp['blank'], gp['lots'] = ' ', comp_list[middle_index:]
        except:
            print(f'Index out of range for {codeset}, copied folder')
            if comp[0]:
                shutil.copy(comp[0], destination) # if you see this line in an error, the comparison wasnt found
            shutil.copy(opfs[0], destination)
            shutil.copy(opfs[1], destination)
        else:
            rp.to_csv(f"{destination}/{codeset}_rp_opf.csv",  index=False, header = False)
            gp.to_csv(f"{destination}/{codeset}_gp_opf.csv",  index=False, header = False)

    def export(self, destination):
        for codeset in self.codesets:
            upload = Upload()
            upload.folder_check(codeset)
            comp = upload.get_comp(codeset)
            opfs = upload.get_opf(codeset)
            upload.create(codeset, comp, opfs, destination)


def main():
    upload = Upload()
    upload.menu()
    upload.item_getter()
    destination = upload.make_folder()
    upload.export(destination=destination)


if __name__ == '__main__':
    main()
