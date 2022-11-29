"""Script that checks text file of REMP scans one at a time,
to gaurentee that each lot is unique in inventory,
if not print the findings"""



def file_gather():
	"""Will gather all scan files"""
	import glob
	files = glob.glob(r"W:\Production\Probe Oligos\REMP Files\In-process\REMP Rack 2D Scans\Unused\Test For Duplicates\REMP*.txt")
	return files

def extract(file):
	"""Reads in the text file to dataframe,
		and extract the lots that will be searched"""
	import pandas as pd
	remp = pd.read_csv(file, names=['REMP','Well','Lot'], header=None, skiprows=2, index_col=None)
	lots = remp['Lot'].values.tolist()

	return remp, lots

def test(lots):
	"""Query for all lots on a single plate, if theres any return, add to list"""

	import pyodbc
	import pandas as pd

	conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\jelvig\Desktop\Poseidon_Test.accdb;')
	cursor = conn.cursor()
	placeholder = '?'
	placeholder = ', '.join(placeholder for unused in lots)
	data = """SELECT qy_oligos_containers.[Item No_], qy_oligos_containers.[Lot No_]
			FROM (qy_oligos_containers)
			WHERE (qy_oligos_containers.[Lot No_] IN (%s))
			ORDER BY qy_oligos_containers.[Lot No_];""" % placeholder

	cursor.execute(data, lots)
	items = cursor.fetchall()
	if items:
		info = {'Item': [i[0] for i in items], 'Lot': [i[1] for i in items]}  # fix bug: was reading data as 96 col, not rows
		df = pd.DataFrame(info, index=None)
		dup_lst = df['Lot'].values.tolist()
		
	else:
		dup_lst = None
	return dup_lst

def duplicate(dup_lst, remp):
	"""Found duplicates will be searched and print there location
	on the REMP plate"""
	dup_lst = list(map(lambda x: int(x), dup_lst))
	location = remp[remp['Lot'].isin(dup_lst)]
	print("--Check These Lots--")
	print(location)

def main():
	files = file_gather()
	for file in files:
		remp, lots = extract(file)
		dup_lst = test(lots)
		if dup_lst:
			duplicate(dup_lst, remp)
		else:
			print(f"No Duplicates on {remp.at[0, 'REMP']}")  # verbose if no duplicates on a plate
	print("Taste Test Complete")
			
if "__name__" == main():
	main()
