def main():
    comp,calc,workingfolder = get_files()
    probe, probe_dec = probe_type()
    if probe_dec == 1:
        creat_comparatorsRPGP(comp, calc, workingfolder,probe)

    else:
        creat_comparators(comp,calc,workingfolder,probe)

def probe_type():
    while True:
        probe_dec = input('What probe are we doing?\n1. RP and GP\n2. RP\n3. GP\n4. Other\n->')
        if probe_dec.isnumeric():
            probe_dec = int(probe_dec)
            if probe_dec == 1:
                probe = ('RP','GP')
                break
            if probe_dec == 2:
                probe = 'RP'
                break
            if probe_dec == 3:
                probe = 'GP'
                break
            if probe_dec == 4:
                    probe = input('please enter the probe type:')
                    break
            else:
                print('Error: Please enter 1, 2, 3, or 4')
    return probe, probe_dec
                    
def get_files():
    '''intakes all file inputs from user to be used in the process'''
    from tkinter import filedialog
    comp = filedialog.askopenfilename(title="Choose Comparison file", initialdir=r'W:\Production\Probe Oligos\REMP Files\_Re-Rack Files')
    calc = filedialog.askopenfilename(title="Choose Calculator")
    workingfolder = filedialog.askdirectory(title="Choose Workingfolder")

    return comp, calc, workingfolder

def creat_comparators(comp, calc, workingfolder,probe):
    import pandas as pd
    from pandas import ExcelWriter
    import openpyxl
    import shutil
    #import time
    #comparator is read in as a dataframe
    df = pd.read_csv(comp, index_col=False, header=None)
    #list of remp numbers is created by searching the column for all unique items 
    REMP = tuple(df[0].unique())
    plate_num=0
    codeset, date = codeset_date()
    #loop is created to calcs for each remp number
    for i in REMP: #calls for each remp name in the list one by one
        plate_num += 1
        file = workingfolder+"\CAL-M0064_Simple Comparator_"+i[4:]+".xlsx"
        shutil.copyfile(calc,file)
        title_df = pd.DataFrame([date,codeset+" "+probe+str(plate_num)])
        with pd.ExcelWriter(file,engine='openpyxl',mode='a',
                if_sheet_exists='overlay') as writer: #excel writer is created automatically for each calc file
            #temperary dataframe is created for the remp number location in comparision file, and name and date
            temp_df = df.loc[df[0] == i] 
            title_df.to_excel(writer,sheet_name='Comparator', header=False,index=False, engine='openpyxl',startrow=0,startcol=1)
            temp_df.to_excel(writer,sheet_name='Comparator', header=False,index=False, engine='openpyxl',startrow=5) #writes to file
            #time.sleep(15)
    print(f'Total comparators:{plate_num}')

def creat_comparatorsRPGP(comp, calc, workingfolder,probe):
    '''Where the magic happens, this function copies the calculator to the working folder under
    new name of remp number, and adds only that remp number info to comparator.
    biggest difference is that is seperates the plate list into two for RPs and GPs.'''
    import pandas as pd
    from pandas import ExcelWriter
    import openpyxl
    import shutil
    #comparator is read in as a dataframe
    df = pd.read_csv(comp, index_col=False, header=None)
    #list of remp numbers is created by searching the column for all unique items 
    REMP = tuple(df[0].unique())
    RempRP =REMP[:len(REMP)//2]
    RempGP =REMP[len(REMP)//2:]
    plate_num=0
    codeset, date = codeset_date()
    #loop is created to calcs for each remp number
    for i in RempRP: #calls for each remp name in the list one by one
        plate_num = plate_num + 1
        file = workingfolder+"\CAL-M0064_Simple Comparator_"+i[4:]+".xlsx"
        shutil.copyfile(calc,file)
        title_df = pd.DataFrame([date,codeset+" "+probe[0]+str(plate_num)])
        with pd.ExcelWriter(file,engine='openpyxl',mode='a',
                if_sheet_exists='overlay') as writer: #excel writer is created automatically for each calc file

            temp_df = df.loc[df[0] == i] #temperary dataframe is created for the remp number location in comparision file
            title_df.to_excel(writer,sheet_name='Comparator', header=False,index=False, engine='openpyxl',startrow=0,startcol=1)
            temp_df.to_excel(writer,sheet_name='Comparator', header=False,index=False, engine='openpyxl',startrow=5) #writes to file
        continue

    plate_num = 0
    for i in RempGP: 
        plate_num = plate_num + 1
        file = workingfolder+"\CAL-M0064_Simple Comparator_"+i[4:]+".xlsx"
        shutil.copyfile(calc,file)
        title_df = pd.DataFrame([date,codeset+" "+probe[1]+str(plate_num)])
        with pd.ExcelWriter(file,engine='openpyxl',mode='a',
                if_sheet_exists='overlay') as writer: 
            temp_df = df.loc[df[0] == i] 
            title_df.to_excel(writer,sheet_name='Comparator', header=False,index=False, engine='openpyxl',startrow=0,startcol=1)
            temp_df.to_excel(writer,sheet_name='Comparator', header=False,index=False, engine='openpyxl',startrow=5) #writes to file  
        continue
    print(f'Total comparators:{plate_num*2}')

def codeset_date():
    from datetime import datetime
    today = datetime.today()
    date = today.strftime("%d%b%Y")
    codeset = input('Enter CodeSet name:')
    codeset = codeset.strip()     
    return codeset, date


main()




