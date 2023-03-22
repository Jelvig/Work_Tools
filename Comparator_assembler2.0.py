class Comparator:
    def probe_type(self):
        """Function that gathers what probe will be used or other,
        which will accept any input.
        """
        while True:
            self.probe_dec = input(
                "What probe are we doing?\n1. RP and GP\n2. RP\n3. GP\n4. Other\n->"
            )
            if self.probe_dec.isnumeric():
                self.probe_dec = int(self.probe_dec)
                if self.probe_dec == 1:
                    self.probe = ("RP", "GP")
                    break
                if self.probe_dec == 2:
                    self.probe = "RP"
                    break
                if self.probe_dec == 3:
                    self.probe = "GP"
                    break
                if self.probe_dec == 4:
                    self.probe = input("please enter the probe type:")
                    break
                else:
                    print("Error: Please enter 1, 2, 3, or 4")

    def get_files(self):
        """function that uses tkinter to obtain file paths
        or directories to use
        """
        from tkinter import filedialog

        self.comp = filedialog.askopenfilename(
            title="Choose Comparison file",
            initialdir=r"W:\Production\Probe Oligos\REMP Files\_Re-Rack Files",
        )
        self.calc = filedialog.askopenfilename(
            title="Choose Calculator", initialdir=r"C:\Users\jelvig\Downloads"
        )
        self.workingfolder = filedialog.askdirectory(
            title="Choose Workingfolder",
            initialdir=r"W:\Production\Probe Oligos\REMP Files\_Re-Rack Files",
        )

    def codeset_date(self):
        """Function that creates the proper data format to paste,
        and asks for the name of the codeset
        """
        from datetime import datetime

        today = datetime.today()
        self.date = today.strftime("%d%b%Y")
        codeset = input("Enter CodeSet name:")
        self.codeset = codeset.strip()

    def create_Comparator(self):
        """coming together of attributes to begin comparator assembler,
        differentiating between RP and GP vs just one probe.
        """
        import pandas as pd
        import time

        self.df = pd.read_csv(self.comp, index_col=False, header=None)
        self.REMP = tuple(self.df[0].unique())
        if self.probe_dec == 1:
            RempRP = self.REMP[: len(self.REMP) // 2]
            RempGP = self.REMP[len(self.REMP) // 2 :]
            REMPS = [RempRP, RempGP]
            count = 0
            for lst in REMPS:
                plate_num = 1
                for comp in lst:
                    self.writer(comp, count, plate_num)
                    plate_num += 1
                    time.sleep(10)  # Don't want to create comparators too fast;)
                count += 1
        else:
            plate_num = 1
            for comp in self.REMP:
                self.writer(comp=comp, plate_num=plate_num)
                plate_num += 1

    def writer(self, comp, count=None, plate_num=0):
        """Function that writes to the comparator template, copying in one
        template at a time.

        Args:
            comp (DataFrame): unique remp number found in comparator, in its own df
            count (int, optional): used to differ between RP and GP. Defaults to None when single probe.
            plate_num (int, optional): the number of plates for this probe. Defaults to 0.
        """
        import shutil
        import pandas as pd

        file = self.workingfolder + "\CAL-M0064_Simple Comparator_" + comp[4:] + ".xlsx"
        shutil.copyfile(self.calc, file)
        if self.probe_dec == 1:
            if len(self.REMP) == 2:
                plate_num = ""
            title_df = pd.DataFrame(
                [self.date, self.codeset + " " + self.probe[count] + str(plate_num)]
            )
        else:
            title_df = pd.DataFrame(
                [self.date, self.codeset + " " + self.probe + str(plate_num)]
            )
        with pd.ExcelWriter(
            file, engine="openpyxl", mode="a", if_sheet_exists="overlay"
        ) as writer:  # excel writer is created automatically for each calc file
            temp_df = self.df.loc[
                self.df[0] == comp
            ]  # temperary dataframe is created for the remp number location in comparision file
            title_df.to_excel(
                writer,
                sheet_name="Comparator",
                header=False,
                index=False,
                engine="openpyxl",
                startrow=0,
                startcol=1,
            )
            temp_df.to_excel(
                writer,
                sheet_name="Comparator",
                header=False,
                index=False,
                engine="openpyxl",
                startrow=5,
            )  # writes to file


def main():
    comp = Comparator()
    comp.get_files()
    comp.probe_type()
    comp.codeset_date()
    comp.create_Comparator()


if "__name__" == main():
    main()
