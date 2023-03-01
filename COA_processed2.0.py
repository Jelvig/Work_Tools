"""COA_processed.py grabbed pre-split COA and moved all of them to
    a Target directory.
    2.0 now splits the raw COA data and exports to new directory"""
def folders(now, year_month, date_string, date_COA):
    """Checks if source file exists and if target
        directory exists"""
    import os
    archived = f"W:/Production/Probe Oligos/Oligo Stock COA/Archived Duplicates/{now.year}/{year_month}/{date_string}_NanoString Technologies Plate COA.csv"
    processed_folder = f'W:/Production/Probe Oligos/Oligo Stock COA/_processedCOA/{date_COA[:4]}_processedCOA/{date_COA}_processedCOA'
    if os.path.isfile(archived) == True:
        print('Archived COA is splitting')
    else:
        print('Please save the Archived COA first')
        exit()
    if os.path.isdir(processed_folder) == True:
        print('The COA might already be split, exiting program')
        exit()
    else:
        os.mkdir(processed_folder)
        print(f'{date_COA}_processedCOA folder has been made')

def date_format():
    """Compiles all the date formats that will be used throught program"""
    from datetime import datetime
    import calendar
    now = datetime.now()  #yyyy_mmdd and yyyy_mm
    month_abbre = calendar.month_abbr[now.month].upper()
    date_string = "%04d%02d%02d" % (now.year,now.month,now.day)
    year_month = "%04d_%02d_%s" % (now.year, now.month, month_abbre)
    date_COA = "%04d_%02d%02d" % (now.year,now.month,now.day)
    return now, date_string, date_COA, year_month

def main():
    import pandas as pd
    pd.io.formats.excel.ExcelFormatter.header_style = None
    now, date_string, date_COA, year_month = date_format()
    folders(now, year_month, date_string, date_COA)
    df = pd.read_csv(f"W:\Production\Probe Oligos\Oligo Stock COA\Archived Duplicates\{now.year}\{year_month}\{date_string}_NanoString Technologies Plate COA.csv", usecols=[*range(0,20)])
    unique_remps = df['Plate_Name'].unique()
    proce_path = f'W:/Production/Probe Oligos/Oligo Stock COA/_processedCOA/{now.year}_processedCOA/{date_COA}_processedCOA'
    for po in unique_remps:
        temp_COA = df['Plate_Name'] == po
        temp_COA = df.loc[temp_COA]
        with pd.ExcelWriter(f'{proce_path}/{po}_CofA.xls') as writer:
            temp_COA.to_excel(writer, engine='openpyxl', index=False)
            print(f'{po} file made')




if '__name__' == main():
    main()
