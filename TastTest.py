"""Script that checks text file of REMP scans one at a time,
to gaurentee that each lot is unique in inventory,
if not print the findings"""



def file_gather():
	import glob
	files = glob.glob("path to duplicates/REMP*.txt")
	return files

def extract(file):
	import pandas as pd
	remp = pd.read_csv(file, header=["REMP", "Well", "Lot"])
	lots = remp.values.tolist()
	return remp, lots

def test(lots):
	import pyodbc
	from pandas import DataFrame

	conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\jelvig\Desktop\Poseidon_Test.accdb;')
	cursor = conn.cursor()
	placeholder = '?'
	placeholder = ', '.join(placeholder for unused in lots)
	data = """
		SELECT qy_oligos_containers.[Item No_], qy_oligos_containers.[Lot No_], qy_oligos_containers.[Bin Code], '' AS toBinCode, qy_oligos_containers.lotQty AS Qty, 'UL' AS UOMC, qy_oligos_containers.type
		FROM ((qy_oligos_containers INNER JOIN [dbo_NanoString$Bin Content] ON qy_oligos_containers.[Bin Code] = [dbo_NanoString$Bin Content].[Bin Code]) INNER JOIN qy_rack_contents ON qy_oligos_containers.shelfCode = qy_rack_contents.shelfCode) INNER JOIN [dbo_NanoString$Item] ON [dbo_NanoString$Bin Content].[Item No_] = [dbo_NanoString$Item].No_
		WHERE (qy_oligos_containers.[Lot No_] IN (%s))
		ORDER BY qy_oligos_containers.[Lot No_];""" % placeholder

	cursor.execute(data, lots)
	items = cursor.fetchall()
	if items:
		df = DataFrame(items, columns=['Item', 'Lot', 'Bin code', 'Qty', 'UL'])
		dup_lst = df["Lot"].values.tolist()
	else:
		dup_lst = None
	return dup_lst

def duplicate(dup, remp):
	location = remp[remp["Lot"].isin(dup)]
	print("--Check These Lots--")
	for loc in location:
		print(loc)

def main():
	files = file_gather()
	for file in files:
		remp, lots = extract(file)
		dup_lst = test(lots, remp)
		if dup_lst:
			duplicate(dup_lst)
			
if "__name__" == main():
	main()
