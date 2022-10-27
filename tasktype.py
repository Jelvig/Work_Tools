def main():
        
    from tkinter import filedialog

    workingfolder = filedialog.askdirectory(initialdir = "W:\Production\Probe Oligos\REMP Files\_Re-Rack Files")
    
    REMP = Remp_check()
    comp_find(REMP, workingfolder)
    rerack_find(REMP, workingfolder)
    print('complete')
    
def Remp_check():  # double checks the given remp is valid
    loop = True    
    while loop == True:
        REMP = str(input('please type in the first REMP number:'))  #left off here, it accepts letters and numbers as long as its length is 8...
        if str.isdigit(REMP) == True and len(REMP)== 8:
            loop = False
        else:
            print('sorry, input was incorrect, please try the 8 remp numbers')
            loop = True
        return REMP

def comp_find(REMP, workingfolder):  # re-writes file with only needed info
    import os
    import glob
    file = glob.glob(workingfolder + '/*_comparison.txt')  # finds text file
    alwayswrite = False
    if file:
        with open(file[0], "r") as f:
            lines = f.readlines()
        with open(file[0], mode='w') as writer:     
            for line in lines:
                if alwayswrite or str(REMP) in line:  # re-writes file with needed info for rerack
                    writer.writelines(line)
                    alwayswrite = True
    elif not file:
        print("cant find comparison file")
            
def rerack_find(REMP, workingfolder):  # finds rerack file and rewrites with needed info
    import glob
    task = "TASKTYPE=TFix-PFix"
    rack = "RACKTYPE=STBR96_300"
    file = glob.glob(workingfolder + "/*_rerack.txt")
    alwayswrite = False
    if file:    
        with open(file[0], "r") as f:
            lines = f.readlines()
        with open(file[0], mode='w') as writer: 
            writer.write(task + '\n' + rack + "\n")    
            for line in lines:
                if str(REMP) in line or alwayswrite:      
                    writer.writelines(line)
                    alwayswrite = True
    if not file:
        print("can't find rerack file")
                                
                         

if "__name__" == main():
    main()
