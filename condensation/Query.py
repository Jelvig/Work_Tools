class Query:
    """
    A class to represent all probe queries that are ran for RP GP and TP

    Attributes
    ----------
    species : int
      an integer representing a selected species of Hs, Mm, none or all

    target : int
      an integer that represents the number of plates user wishes to use, that translates to number of rows to return

    Methods
    -------
    rp(), gp() and tp()
      each query does the same thing but grabs specific information for  the chosen probe and species, then places it into
      a dataframe for manipulation
    """
    def __init__(self, species=None, target=1):
        import pyodbc
        self.species = species
        self.target = target * 96
        self.conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\jelvig\Desktop\Poseidon_Test.accdb;')
        self.cursor = self.conn.cursor()

    def rp(self):
        import pandas as pd
        if self.species == 1:
            query = ("""SELECT TOP %s qy_Oligoinv_All.[Item No_], qy_Oligoinv_All.[Lot No_], qy_Oligoinv_All.[Bin Code], '' AS toBinCode, qy_Oligoinv_All.Quantity AS Qty,
            'UL' AS UOMC, qy_Oligoinv_All.shelfNo, itemcount.itemCount, qy_Oligoinv_All.type, qy_Oligoinv_All.[Description 2], qy_Oligoinv_All.caneNo
        
            FROM (qy_Oligoinv_All INNER JOIN itemcount ON qy_Oligoinv_All.shelfNo = itemcount.shelfNo)
        
            WHERE ((qy_Oligoinv_All.type)='2') And (Left(qy_Oligoinv_All.[Bin Code],3)='F02') And (((qy_Oligoinv_All.[Description 2] = 'Hs') AND (qy_Oligoinv_All.caneNo) Between '14' And '26')
              OR  (((itemcount.itemCount)<80) And (qy_Oligoinv_All.caneNo) Between '06' And '13'))
        
            ORDER BY itemcount.itemCount, qy_Oligoinv_All.[Bin Code];""" % self.target)
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            info = {'Item': [i[0] for i in results], 'Lot': [i[1] for i in results], 'Bin Code': [i[2] for i in results],
                         'toBinCode':  [i[3] for i in results],'Qty': [i[4] for i in results], 'UMOC': [i[5] for i in results], 'shelfcode': [i[6] for i in results],
                         'itemcount': [i[7] for i in results],'type': [i[8] for i in results], 'Description 2': [i[9] for i in results]}
            df = pd.DataFrame(info, index=None)
            self.conn.close()
            return df

        elif self.species == 2:
            query = ("""SELECT TOP %s qy_Oligoinv_All.[Item No_], qy_Oligoinv_All.[Lot No_], qy_Oligoinv_All.[Bin Code], '' AS toBinCode, qy_Oligoinv_All.Quantity AS Qty,
            'UL' AS UOMC, qy_Oligoinv_All.shelfNo, itemcount.itemCount, qy_Oligoinv_All.type, qy_Oligoinv_All.[Description 2], qy_Oligoinv_All.caneNo
            
            FROM (qy_Oligoinv_All INNER JOIN itemcount ON qy_Oligoinv_All.shelfNo = itemcount.shelfNo)
            
            WHERE ((((qy_Oligoinv_All.[Description 2]='Mm') AND (qy_Oligoinv_All.caneNo) Between '18' And '26')) OR (((itemcount.itemCount)<80)
              AND ((qy_Oligoinv_All.caneNo) Between '14' And '17'))) AND ((Left([qy_Oligoinv_All].[Bin Code],3)='F02') AND ((qy_Oligoinv_All.type)='2'))
            
            ORDER BY (itemcount.itemCount), (qy_Oligoinv_All.[Bin Code]);""" % self.target)
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            info = {'Item': [i[0] for i in results], 'Lot': [i[1] for i in results], 'Bin Code': [i[2] for i in results],
                         'toBinCode':  [i[3] for i in results],'Qty': [i[4] for i in results], 'UMOC': [i[5] for i in results], 'shelfcode': [i[6] for i in results],
                         'itemcount': [i[7] for i in results],'type': [i[8] for i in results], 'Description 2': [i[9] for i in results]}
            df = pd.DataFrame(info, index=None)
            self.conn.close()
            return df

        elif self.species == 3:
            query = ("""SELECT TOP %s qy_Oligoinv_All.[Item No_], qy_Oligoinv_All.[Lot No_], qy_Oligoinv_All.[Bin Code], '' AS toBinCode, qy_Oligoinv_All.Quantity AS Qty,
              'UL' AS UOMC, qy_Oligoinv_All.shelfNo, itemcount.itemCount, qy_Oligoinv_All.type, qy_Oligoinv_All.[Description 2], qy_Oligoinv_All.caneNo
            
            FROM (qy_Oligoinv_All INNER JOIN itemcount ON qy_Oligoinv_All.shelfNo = itemcount.shelfNo)
            
            WHERE (((itemcount.itemCount)<80) And ((qy_Oligoinv_All.type)='2') And ((Left(qy_Oligoinv_All.[Bin Code],3))='F02') And ((qy_Oligoinv_All.caneNo) Between '18' And '26'))
            
            ORDER BY (itemcount.itemCount), (qy_Oligoinv_All.[Bin Code]), 'Update 09FEB2023: Mines all nonspecies specific RP canes and orders return by item count and bincode to ensure lowest item counts are condensed'<>'';
            """ % self.target)
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            info = {'Item': [i[0] for i in results], 'Lot': [i[1] for i in results], 'Bin Code': [i[2] for i in results],
                         'toBinCode':  [i[3] for i in results],'Qty': [i[4] for i in results], 'UMOC': [i[5] for i in results], 'shelfcode': [i[6] for i in results],
                         'itemcount': [i[7] for i in results],'type': [i[8] for i in results], 'Description 2': [i[9] for i in results]}
            df = pd.DataFrame(info, index=None)
            self.conn.close()
            return df

        elif self.species == 4:
            query = ("""SELECT TOP %s qy_Oligoinv_All.[Item No_], qy_Oligoinv_All.[Lot No_], qy_Oligoinv_All.[Bin Code], '' AS toBinCode, qy_Oligoinv_All.Quantity AS Qty,
              'UL' AS UOMC, qy_Oligoinv_All.shelfNo, itemcount.itemCount, qy_Oligoinv_All.type, qy_Oligoinv_All.[Description 2], qy_Oligoinv_All.caneNo
            
            FROM (qy_Oligoinv_All INNER JOIN itemcount ON qy_Oligoinv_All.shelfNo = itemcount.shelfNo)
           
            WHERE (((itemcount.itemCount)<80) And ((qy_Oligoinv_All.type)='2') And ((Left(qy_Oligoinv_All.[Bin Code],3))='F02') And ((qy_Oligoinv_All.caneNo) Between '06' And '26'))
            
            ORDER BY (itemcount.itemCount), (qy_Oligoinv_All.[Bin Code]), 'Update 27Jan2023: Mines all RP canes and orders return by item count and bincode to ensure lowest item counts are condensed'<>'';
            """ % self.target)
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            info = {'Item': [i[0] for i in results], 'Lot': [i[1] for i in results], 'Bin Code': [i[2] for i in results],
                         'toBinCode':  [i[3] for i in results],'Qty': [i[4] for i in results], 'UMOC': [i[5] for i in results], 'shelfcode': [i[6] for i in results],
                         'itemcount': [i[7] for i in results],'type': [i[8] for i in results], 'Description 2': [i[9] for i in results]}
            df = pd.DataFrame(info, index=None)
            self.conn.close()
            return df

    def gp(self):
        import pandas as pd
        if self.species == 1:
            query = ("""SELECT TOP %s qy_Oligoinv_All.[Item No_], qy_Oligoinv_All.[Lot No_], qy_Oligoinv_All.[Bin Code],
              '' AS toBinCode, qy_Oligoinv_All.Quantity AS Qty, 'UL' AS UOMC, qy_Oligoinv_All.shelfNo, itemcount.itemCount, qy_Oligoinv_All.type, qy_Oligoinv_All.[Description 2], qy_Oligoinv_All.caneNo
            
            FROM (qy_Oligoinv_All INNER JOIN itemcount ON qy_Oligoinv_All.shelfNo = itemcount.shelfNo)
            
            WHERE ((((qy_Oligoinv_All.[Description 2]='Hs') AND (qy_Oligoinv_All.caneNo) Between '48' And '60')) OR (((itemcount.itemCount)<80)  AND 
            ((qy_Oligoinv_All.caneNo) Between '27' And '47') and (qy_Oligoinv_All.caneNo) not Between '28' And '40')) AND ((Left([qy_Oligoinv_All].[Bin Code],3)='F02') AND ((qy_Oligoinv_All.type)='3'))
            
            ORDER BY (itemcount.itemCount), (qy_Oligoinv_All.[Bin Code]), 'Update 09FEB2023: Mines all Human GP canes, seaches for human items in other and orders return by item count and bincode to ensure lowest item counts are condensed'<>'';
            """ % self.target)
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            info = {'Item': [i[0] for i in results], 'Lot': [i[1] for i in results], 'Bin Code': [i[2] for i in results],
                         'toBinCode':  [i[3] for i in results],'Qty': [i[4] for i in results], 'UMOC': [i[5] for i in results], 'shelfcode': [i[6] for i in results],
                         'itemcount': [i[7] for i in results],'type': [i[8] for i in results], 'Description 2': [i[9] for i in results]}
            df = pd.DataFrame(info, index=None)
            self.conn.close()
            return df

        elif self.species == 2:
            query = ("""SELECT TOP %s qy_Oligoinv_All.[Item No_], qy_Oligoinv_All.[Lot No_], qy_Oligoinv_All.[Bin Code], '' AS toBinCode, qy_Oligoinv_All.Quantity AS Qty,
              'UL' AS UOMC, qy_Oligoinv_All.shelfNo, itemcount.itemCount, qy_Oligoinv_All.type, qy_Oligoinv_All.[Description 2], qy_Oligoinv_All.caneNo
            
            FROM (qy_Oligoinv_All INNER JOIN itemcount ON qy_Oligoinv_All.shelfNo = itemcount.shelfNo)
            
            WHERE ((((qy_Oligoinv_All.[Description 2]='Mm') AND (qy_Oligoinv_All.caneNo) Between '52' And '60')) OR (((itemcount.itemCount)<80)  AND 
            ((qy_Oligoinv_All.caneNo) Between '48' And '51'))) AND ((Left([qy_Oligoinv_All].[Bin Code],3)='F02') AND ((qy_Oligoinv_All.type)='3'))
            
            ORDER BY (itemcount.itemCount), (qy_Oligoinv_All.[Bin Code]);
            """ % self.target)
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            info = {'Item': [i[0] for i in results], 'Lot': [i[1] for i in results], 'Bin Code': [i[2] for i in results],
                         'toBinCode':  [i[3] for i in results],'Qty': [i[4] for i in results], 'UMOC': [i[5] for i in results], 'shelfcode': [i[6] for i in results],
                         'itemcount': [i[7] for i in results],'type': [i[8] for i in results], 'Description 2': [i[9] for i in results]}
            df = pd.DataFrame(info, index=None)
            self.conn.close()
            return df

        elif self.species == 3:
            query = ("""SELECT TOP %s qy_Oligoinv_All.[Item No_], qy_Oligoinv_All.[Lot No_], qy_Oligoinv_All.[Bin Code], '' AS toBinCode, qy_Oligoinv_All.Quantity AS Qty,
              'UL' AS UOMC, qy_Oligoinv_All.shelfNo, itemcount.itemCount, qy_Oligoinv_All.type, qy_Oligoinv_All.[Description 2], qy_Oligoinv_All.caneNo
            
            FROM (qy_Oligoinv_All INNER JOIN itemcount ON qy_Oligoinv_All.shelfNo = itemcount.shelfNo)
            
            WHERE (((itemcount.itemCount)<80) And ((qy_Oligoinv_All.type)='3') And ((Left(qy_Oligoinv_All.[Bin Code],3))='F02') And ((qy_Oligoinv_All.caneNo) Between '52' And '60'))
            
            ORDER BY (itemcount.itemCount), (qy_Oligoinv_All.[Bin Code]), 'Update 09FEB2023: Mines all nonspecies specific GP canes and orders return by item count and bincode to ensure lowest item counts are condensed'<>'';
            """ % self.target)
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            info = {'Item': [i[0] for i in results], 'Lot': [i[1] for i in results], 'Bin Code': [i[2] for i in results],
                         'toBinCode':  [i[3] for i in results],'Qty': [i[4] for i in results], 'UMOC': [i[5] for i in results], 'shelfcode': [i[6] for i in results],
                         'itemcount': [i[7] for i in results],'type': [i[8] for i in results], 'Description 2': [i[9] for i in results]}
            df = pd.DataFrame(info, index=None)
            self.conn.close()
            return df

        elif self.species == 4:
            query = ("""SELECT TOP %s qy_Oligoinv_All.[Item No_], qy_Oligoinv_All.[Lot No_], qy_Oligoinv_All.[Bin Code],
              '' AS toBinCode, qy_Oligoinv_All.Quantity AS Qty, 'UL' AS UOMC, qy_Oligoinv_All.shelfNo, itemcount.itemCount, qy_Oligoinv_All.type, qy_Oligoinv_All.[Description 2], qy_Oligoinv_All.caneNo
            
            FROM (qy_Oligoinv_All INNER JOIN itemcount ON qy_Oligoinv_All.shelfNo = itemcount.shelfNo)
           
             WHERE (((itemcount.itemCount)<80) And ((qy_Oligoinv_All.type)='3') And ((Left(qy_Oligoinv_All.[Bin Code],3))='F02') And 
            ((qy_Oligoinv_All.caneNo) Between '27' And '60' And (qy_Oligoinv_All.caneNo) Not Between '28' And '40'))
            
            ORDER BY (itemcount.itemCount), (qy_Oligoinv_All.[Bin Code]), 'Update 27Jan2023: Mines all GP canes and orders return by item count and bincode to ensure lowest item counts are condensed'<>'';
            """ % self.target)
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            info = {'Item': [i[0] for i in results], 'Lot': [i[1] for i in results], 'Bin Code': [i[2] for i in results],
                         'toBinCode':  [i[3] for i in results],'Qty': [i[4] for i in results], 'UMOC': [i[5] for i in results], 'shelfcode': [i[6] for i in results],
                         'itemcount': [i[7] for i in results],'type': [i[8] for i in results], 'Description 2': [i[9] for i in results]}
            df = pd.DataFrame(info, index=None)
            self.conn.close()
            return df

    def tp(self):
        import pandas as pd
        query = ("""SELECT TOP %s qy_Oligoinv_All.[Item No_], qy_Oligoinv_All.[Lot No_], qy_Oligoinv_All.[Bin Code], '' AS toBinCode, qy_Oligoinv_All.Quantity AS Qty,
          'UL' AS UOMC, qy_Oligoinv_All.shelfNo, itemcount.itemCount, qy_Oligoinv_All.type, qy_Oligoinv_All.[Description 2], qy_Oligoinv_All.caneNo
           
            FROM (qy_Oligoinv_All INNER JOIN itemcount ON qy_Oligoinv_All.shelfNo = itemcount.shelfNo)
            
            WHERE (((itemcount.itemCount)<80) And ((qy_Oligoinv_All.type)='4') And ((Left(qy_Oligoinv_All.[Bin Code],3))='F02') And ((qy_Oligoinv_All.caneNo) Between '28' And '36'))
            
            ORDER BY (itemcount.itemCount), (qy_Oligoinv_All.[Bin Code]) AND 'Update 27Jan2023: Mines all TP canes and orders return by item count and bincode to ensure lowest item counts are condensed'<>'';
            """ % self.target)
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        info = {'Item': [i[0] for i in results], 'Lot': [i[1] for i in results], 'Bin Code': [i[2] for i in results],
                        'toBinCode':  [i[3] for i in results],'Qty': [i[4] for i in results], 'UMOC': [i[5] for i in results], 'shelfcode': [i[6] for i in results],
                        'itemcount': [i[7] for i in results],'type': [i[8] for i in results], 'Description 2': [i[9] for i in results]}
        df = pd.DataFrame(info, index=None)
        self.conn.close()
        return df


    def coolercleanup(self):
        import pandas as pd
        query = """SELECT qy_Oligoinv_All.[Item No_], qy_Oligoinv_All.[Lot No_], qy_Oligoinv_All.[Bin Code], '' AS toBinCode, qy_Oligoinv_All.Quantity AS Qty, 'UL' AS UOMC, qy_Oligoinv_All.shelfNo, itemcount.itemCount,
               qy_Oligoinv_All.type, qy_Oligoinv_All.[Description 2], qy_Oligoinv_All.caneNo
        FROM (qy_Oligoinv_All INNER JOIN itemcount ON qy_Oligoinv_All.shelfNo = itemcount.shelfNo)
        WHERE (((itemcount.itemCount)<97) And ((qy_Oligoinv_All.type) Between '2' And '5') And ((Left(qy_Oligoinv_All.[Bin Code],3))='C02') And ((qy_Oligoinv_All.caneNo) Between '10' And '13'))
        ORDER BY (qy_Oligoinv_All.type), (qy_Oligoinv_All.[Bin Code])"""
        
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        info = {'Item': [i[0] for i in results], 'Lot': [i[1] for i in results], 'Bin Code': [i[2] for i in results],
                        'toBinCode':  [i[3] for i in results],'Qty': [i[4] for i in results], 'UMOC': [i[5] for i in results], 'shelfcode': [i[6] for i in results],
                        'itemcount': [i[7] for i in results],'type': [i[8] for i in results], 'Description 2': [i[9] for i in results]}
        df = pd.DataFrame(info, index=None)
        self.conn.close()
        return df
