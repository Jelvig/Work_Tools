
class JumboCheck():
    def __init__(self):  # two lists for names and items will be spawn at beginning of program
        self.codeitems = []
        self.codenames = []
        self.probe = 0

    def get_nameitem(self):  # Ugly attribute that gathers names, items and what probe
        while True:
            name = input('Enter CodeSet name:').strip()
            if name == '':
                break
            else:
                self.codenames.append(name)  # Creating codeset name list 
                
        while True:
            num = input('Enter items to be cross checked:')
            if num.isdigit() and (len(num) == 6 or len(num) == 9):
                num = int(num)
                self.codeitems.append(num)  # Creating item number list
            elif num == '':
                break
            else:
                print('please enter a valid number')
        while True:
            temp = input('Enter 0 for RP or 1 for GP:')
            if temp.isdigit():
                temp = int(temp)
                if temp == 0 or temp == 1:
                    self.probe = temp  # Choosing what probe we are comparing
                    break
                else:
                    print('That is not a 1 or 0, try again')
            else:
                print('That is not a number, try again')
    
    def opf_set(self):  # Gathering of OPF item numbers
        import pandas as pd
        for name in self.codenames:
            try:
                path = (f"Z:\\"+name+"\\production\\"+name+"_rp_opf.csv", "Z:\\"+name+"\\production\\"+name+"_gp_opf.csv")
                codeitem = pd.read_csv(path[self.probe], usecols=[1], header=None, index_col=None)  # Only reads column with item numbers
            except FileNotFoundError:
                print(f"{name} was not found and will be deleted from comparison")
                self.codenames.remove(name)
            else:
                self.codeitems.append(set(codeitem[1]))  # identifying series to be turned in to set
    
    def report(self):
        for first in range(len(self.codenames)):  # Not very pythonic but simple code of comparing each item list to each other
            item1 = set(self.codeitems[first])
            for all in range(first + 1, len(self.codenames)):
                item2 = set(self.codeitems[all])
                cross = item1.intersection(item2)  # Checking if any items are the same
                if len(cross) != 0:
                    print(f"{self.codenames[first]:>15} : {self.codenames[all]:>15}{len(cross):_>8}\n")  # If there is overlap, it will print the name and the number of items
                else:
                    continue  # Ignores any comparisons with no overlap
            continue

    def item_report(self):  # Same function as report, but it prints the item numbers that are overlapping
            for first in range(len(self.codenames)):
                item1 = set(self.codeitems[first])
                for all in range(first + 1, len(self.codenames)):
                    item2 = set(self.codeitems[all])
                    cross = item1.intersection(item2)
                    if len(cross) != 0:
                        print(f"{self.codenames[first]:>15} : {self.codenames[all]:>15}:{cross}\n")  # cross is not turned into number, so it prints a set
                        
                    else:
                        continue
                continue

def main():
    checker = JumboCheck()
    checker.get_nameitem()
    checker.opf_set()
    checker.report()
    while True:
        itemview = input('Need items printed? (y/n):').lower()
        if itemview == 'y':
            checker.item_report()  # If you need item numbers, it will give you an option, otherwise exit the program
            exit()
        elif itemview != 'y' and itemview != 'n':
            print('Invalid type y or n')
        else:
            exit()

if '__name__' == main():
    main()