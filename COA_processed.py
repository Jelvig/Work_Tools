class COA():
    def find_files(self):
        import glob
        self.coa = glob.glob(r"C:/Users/jelvig/Desktop/Processed/*CofA.xls")  # using glob to find all PO files

    def move_files(self):
        import shutil
        for file in self.coa:
            shutil.move(file, self.path)  # Move the files to required destination
        print("Files Moved")
        

    def check_dir(self):
        from datetime import datetime
        import os
        now = datetime.now()
        date = "%04d_%02d%02d" % (now.year,now.month,now.day)  # creation of date format for files
        year = "%04d" % (now.year)
        self.path = f"W:/Production/Probe Oligos/Oligo Stock COA/_processedCOA/{year}_processedCOA/{date}_processedCOA" 
        if os.path.isdir(self.path) == True:  # Check to see if file exists
            print("These files have already been moved")
        else:
            os.mkdir(self.path)
            print(f"{date}_processedCOA file has been made")
    
    def rm_exta(self):
        import glob
        import os
        files = glob.glob(r"C:/Users/jelvig/Desktop/Processed/*")
        if files:
            for file in files:
                os.remove(file)
        print("Extra Files Removed")

def main():
    beta = COA()
    beta.find_files()
    beta.check_dir()
    beta.move_files()
    beta.rm_exta()

if "__name__" == main():
    main()