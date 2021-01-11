
'''
Created on Dec 07, 2021

@author: pia.manzon
'''

from sqlalchemy import create_engine, func
from urllib.parse import quote_plus
import sqlalchemy


class Database():
    def __init__(self):
        try:
            self.conn = "DRIVER={SQL Server Native Client 11.0};SERVER=CA094A;DATABASE=Scipio;Trusted_Connection=yes;"
            quoted = quote_plus(self.conn)
            self.new_con = 'mssql+pyodbc:///?odbc_connect={}'.format(quoted)
            self.engine = create_engine(self.new_con,fast_executemany=True)
        except sqlalchemy.exc.DBAPIError as dbError:
            raise dbError 

    def getLatestDate(self):
        maxDate =  self.engine.execute("SELECT MAX(TimeStamp) FROM Cogen_Metered_Volumes").fetchone()
        return maxDate[0]
    
    
    def updateDatabase (self,df):
        index = df.index
        totalRows = len(index)
        print("Number of data rows to be inserted: " + str(totalRows))
        df.to_sql("Cogen_Metered_Volumes", con = self.engine, if_exists = 'append', index=False)
        print("Inserted " + str(totalRows) + "rows!")
        return
        
   
