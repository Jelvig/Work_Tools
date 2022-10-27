def main():
    decision = inout()

    if decision == 1:
        opf = upload()
        upgrade2(opf)
    elif decision == 2:
        opf = upload()
        upgrade(opf)
    print('Exported JA')

def inout():
    while True:
        try:
            decision = int(input('1. Positive Adj.\n2. Negative adj.\nchoose number for adjustment:'))
        except (ValueError, TypeError) as error:
                print('sorry thats not a valid chose, try again.')
                continue
        if decision == 1:
            break
        elif decision == 2:
            break
    return decision

def upload():
    from tkinter import filedialog
    import pandas as pd

    path = filedialog.askopenfilename(initialdir=r'W:\Production\Probe Oligos\REMP Files\_Re-Rack Files', title='Choose upload file')
    opf = pd.read_csv(path,usecols=[0,1,3,4], names=['A','B','C','D'])

    return opf

def upgrade(opf):
    import pandas as pd
    reasoncode = reason_check()
    
    
    df = pd.DataFrame()
    df['A'] = opf['A']
    df['B'] = opf['C']
    df['C'] = ''
    df['D'] = opf['B']
    df['E'], df['F'] = '', ''
    df['G'] = opf['D']
    df['H'] = ''
    df['I'] = 0
    df['J'] = opf['D']
    df['K'] = reasoncode

    df.to_csv("W:/Production/Probe Oligos/Oligo Management/Journal Adjustments/JA_number_reason_JE_OUT.csv", header=False, index = False)

def upgrade2(opf):
    import pandas as pd
    reasoncode = reason_check()
    
    
    df = pd.DataFrame()
    df['A'] = opf['A']
    df['B'] = opf['C']
    df['C'] = ''
    df['D'] = opf['B']
    df['E'], df['F'] = '', ''
    df['G'] = 0
    df['H'] = ''
    df['I'] = opf['D']
    df['J'] = 0
    df['K'] = reasoncode

    df.to_csv("W:/Production/Probe Oligos/Oligo Management/Journal Adjustments/JA_number_reason_JE_IN.csv", header=False, index = False)

def reason_check():
    while True:
        try:
            reasonselect = int(input('what is your reason code? \n1. CYCLE CNT\n2. EXPIRED\n3. LOW VOL\n4. SCRAP\n5. YIELD ADJ\n6. other\nchoosen number:'))
        except (ValueError, TypeError) as error:
            print('sorry thats not a valid chose, try again.')
            continue
        if reasonselect == 1:
            reasoncode = 'CYCLE CNT'
            break
        elif reasonselect == 2:
            reasoncode = 'EXPIRED'
            break
        elif reasonselect == 3:
            reasoncode = 'LOW VOL'
            break
        elif reasonselect == 4:
            reasoncode = 'SCRAP'
            break
        elif reasonselect == 5:
            reasoncode = 'YIELD ADJ'
            break
        elif reasonselect == 6:
            reasoncode = input('input reason code:')
            break
    return reasoncode

main()