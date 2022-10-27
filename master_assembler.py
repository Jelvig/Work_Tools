def codeRP():  # Gather of RP names
    RPonly = []
    while True:
        codeset = input('input RP only:').strip()
        if codeset != '':
            RPonly.append(codeset)
        else:
            break
    return RPonly

def codeGP():  # Gathering of GP names
    GPonly = []
    while True:
        codeset = input('input GP only:').strip()
        if codeset != '':
            GPonly.append(codeset)
        else:
            break
    return GPonly

def codeC():  # Gathering of both RP and GP names to search
    C = []
    while True:
        codeset = input('input for RP&GP:').strip()
        if codeset != '':
            C.append(codeset)
        else:
            break
    return C

def get_df(codeset, pathnum):  # Simple function to get the dataframe for each name or not find it
    import pandas as pd
    import os
    path = (f"Z:/{codeset}/production/{codeset}_rp_opf.csv", f"Z:/{codeset}/production/{codeset}_gp_opf.csv")
    if os.path.isfile(path[pathnum]) == True:
        df = pd.read_csv(path[pathnum], header=None, index_col=None)
        return df
    else:
        print(f"{codeset} was not found")

def get_RPOPF(RPlist):  # Gathering of opfs via list, concatenate and export
    import pandas as pd 
    import os
    from datetime import datetime
    now = datetime.now()
    date = "%04d_%02d_%02d" % (now.year,now.month,now.day)  # Creating date/time format for opf file
    masterfile = date + '_rp_opf.csv'
    masterpath = os.path.join('W:/Production/Probe Oligos/Oligo Tools/Low Volume/Master opf files/'+ masterfile)
    all_files = [get_df(codeset, pathnum=0) for codeset in RPlist]  # List comprehension to retrieve dataframe based on codeset name

    frame = pd.concat(all_files, axis = 0, ignore_index=True)  # Concatenation of opf files and export to file path
    frame = frame.drop_duplicates(subset=1)
    file_check(masterpath, frame)  # Check of files existence, and export

def get_GPOPF(GPlist):  # Gathering of GP opfs via list, concatenate and export
    import pandas as pd 
    import os
    from datetime import datetime
    now = datetime.now()
    date = "%04d_%02d_%02d" % (now.year,now.month,now.day)  # create date format
    masterfile = date + '_gp_opf.csv'
    masterpath = os.path.join('W:/Production/Probe Oligos/Oligo Tools/Low Volume/Master opf files/'+ masterfile)
    all_files = [get_df(codeset, pathnum=1) for codeset in GPlist]  # List comprehension to retrieve dataframe based on codeset name

    frame = pd.concat(all_files, axis = 0, ignore_index=True)  # Concatenate
    frame = frame.drop_duplicates(subset=1)
    file_check(masterpath,frame)  # Export to file path

def file_check(masterpath, frame):  # checks files existence, if one exists its removed
    import os
    if os.path.isfile(masterpath) == False:
        frame.to_csv(masterpath, index=False, header = False)
    else:
        os.remove(masterpath)
        frame.to_csv(masterpath, index=False, header = False)

def main():
    RPonly = codeRP()
    GPonly = codeGP()
    C = codeC()
    RPlist = C + RPonly  # Combine RP&GP list to RP only/GP only list
    GPlist = C + GPonly
    if len(RPlist) != 0 and len(GPlist) != 0:  # avoid errors if no RP or GP are inputed
        get_RPOPF(RPlist)
        get_GPOPF(GPlist)
    elif len(GPlist) == 0:
        get_RPOPF(RPlist)
    elif len(RPlist) == 0:
        get_GPOPF(GPlist)
    else:
        print('Nothing to condense')  # If nothing is inputed
    report(RPlist,GPlist)    
    print('Exported to Master OPF files')

def report(opflistRP,opflistGP):  # simple function that writes the CodeSets that were searched to to text files
    with open(r"C:\Users\jelvig\Desktop\searchedRP.txt", 'w') as file:
        for codeset in opflistRP:
            file.write(codeset+"\n")
    with open(r"C:\Users\jelvig\Desktop\searchedGP.txt", 'w') as file:
        for codeset in opflistGP:
            file.write(codeset+"\n")
    
            

if '__name__' == main():
    main()
