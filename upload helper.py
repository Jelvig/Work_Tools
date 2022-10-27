def main():
    
    code = menu()
    
    destination = make_folder()
    item_getter(code)
    get_comp(code,destination)
    get_opf(destination, code)
    folder_check(code)

def menu():
    """create a list of CodeSets that will run through the program for needed information"""
    code = []
    loop = True
    while loop == True:
        CodeSet = input("Enter CodeSet name:\n")
        if CodeSet != '':
            CodeSet = CodeSet.strip()
            code.append(CodeSet)
            loop == True
            
        elif CodeSet == '':
            loop == False
            break
                
    return code  

def item_getter(code):
    """indexes for codeset names within item card tracking, records it and uses its (max) location to find the up-to-date
    item number for the production orders"""
    import pandas as pd
    master = pd.read_excel(r"W:\Production\Probe Oligos\Oligo Tools\Item Card Tracking.xlsx", sheet_name ='Custom CodeSets', usecols=[0,3])
    for codeset in code:
        lst = master.index[master['CodeSet Name'] == codeset].tolist()
        point = max(lst)
        num = master.iloc[point, 1]
        print(f'''name: {codeset}\nItem number: {num}\n____________________________''')

def make_folder():
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

def get_comp(code, destination):
    """this function finds the comparison files in proper folder,
        if a there is a panel, it takes a different route to get both
        comparison files"""
    import glob as glob
    import shutil
    try:
        for CodeSet in code:  # if panel, get both comparisons
            if CodeSet.startswith('NS_') == True:
                files1 = glob.glob("W:\Production\Probe Oligos\REMP Files\_Re-Rack Files\*" + CodeSet + "*\GP\*_comparison.txt")
                files2 = glob.glob("W:\Production\Probe Oligos\REMP Files\_Re-Rack Files\*" + CodeSet + "*\RP\*_comparison.txt")
                source1 = files1[0]
                source2 = files2[0]
                shutil.copy(source1, destination)
                shutil.copy(source2, destination)

            else:  # get just the one comparison
                files = glob.glob("W:\Production\Probe Oligos\REMP Files\_Re-Rack Files\*" + CodeSet + "*\*_comparison.txt")
                source = files[0]
                shutil.copy(source, destination)
    except IndexError:
            print(f"can't find {CodeSet} comparison file")

    return destination

def get_opf(destination, code):
    """this function finds the path to the codeset folder to find each opf, and then
        moves it to the new folder on your desktop"""
    import os
    import glob as glob
    import shutil
    for CodeSet in code: #get RP opf's
        files = glob.glob("Z:/" + CodeSet + "/production/" + CodeSet + "_rp_opf.csv")
        source = files[0]
        shutil.copy(source, destination)

    for CodeSet in code: #get GP opf's
        files = glob.glob("Z:/" + CodeSet + "/production/" + CodeSet + "_gp_opf.csv")
        source = files[0]
        shutil.copy(source, destination)

def folder_check(code):
    """ this function is to check to see if folders exist in this path
        if it does, it creates new folder with the date, if not the path is created"""

    import os
    from datetime import datetime
    now = datetime.now()
    date = "%04d_%02d%02d" % (now.year,now.month,now.day)
    for CodeSet in code:
        path = "W:/Production/ERP/CodeSet OPFs with lot numbers/" + CodeSet +"/"
        if os.path.isdir(path) == True:
            folder = CodeSet +' ('+date+')'
            newpath = os.path.join(path + folder)
            os.mkdir(newpath)
            print(CodeSet + ' had a folder')
        elif os.path.isdir(path) == False:
            os.mkdir(path)
            

if "__name__" == main():
    main()
