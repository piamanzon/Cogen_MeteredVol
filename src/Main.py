from WebPage import WebPage

import Data
from datetime import date, timedelta
import Database
import time 
import File
def Main ():
    #Asset list
    assetIDList = [{'AssetID': 'APS1' , 'Asset': 'ATCO Scotford Upgrader (APS1)'}, {'AssetID': 'SCR1', 'Asset': 'Base Plant (SCR1)'}, {'AssetID': 'CNR5', 'Asset': 'CNRL Horizon (CNR5)' },
                   {'AssetID': 'SCR6', 'Asset': 'Firebag (SCR6)'}, {'AssetID': 'FH1', 'Asset': 'Fort Hills (FH1)'}, {'AssetID': 'EC04', 'Asset': 'Foster Creek (EC04)'},
                   {'AssetID': 'IOR3', 'Asset': 'Kearl (IOR3)'}, {'AssetID': 'PEC1', 'Asset': 'Lindbergh (PEC1)'}, {'AssetID': 'MEG1', 'Asset': 'MEG1 Christina Lake (MEG1)'}, 
                   {'AssetID': 'MKRC', 'Asset': 'MacKay River (MKRC)'}, {'AssetID': 'IOR1', 'Asset': 'Mahkeses (IOR1)'}, {'AssetID': 'MKR1', 'Asset': 'Muskeg River (MKR1)'}, 
                   {'AssetID': 'IOR2', 'Asset': 'Nabiye (IOR2)'}, {'AssetID': 'NX02', 'Asset': 'Nexen Inc #2 (NX02)'}, {'AssetID': 'SCR5', 'Asset': 'Poplar Creek (SCR5)'}, 
                   {'AssetID': 'PR1', 'Asset': 'Primrose #1 (PR1)'}, {'AssetID': 'TC02', 'Asset': 'Redwater Cogen (TC02)'}, {'AssetID': 'SCL1', 'Asset': 'Syncrude #1 (SCL1)'},
                   {'AssetID': 'CL01', 'Asset':'Christina Lake (CL01)'}]
    
    db = Database.Database()
    
    #Download location
    fileName = r"C:\Users\pia.manzon\AppData\Local\Temp\PublicSummaryAllReportServlet.csv"
    resultList = []
    totalData = 0
    #Database last date
    lastDBDate = db.getLatestDate().date()
    #lastDBDate = date(2021,12,1) Uncomment if you want to download reports from specific date range
    print(lastDBDate)
    dateYesterday = date.today() - timedelta(1)
   
    while(dateYesterday != lastDBDate):
        print(dateYesterday)
        wb = WebPage(dateYesterday)
        wb.frame_switch("report_nav")
        wb.downloadReport()
        wb.closeBrowser()
        time.sleep(1)
        
        if (File.isDownloaded(fileName) == False):
            print("Error downloading the file! Check your temp folder.")
            exit
            
        rawDataList = Data.processData(assetIDList, fileName, dateYesterday)
        
        if(rawDataList):
            resultList = resultList + rawDataList
            totalData = totalData + len(resultList)
        print("Length of list:" + str(len(resultList)))
        
        File.deleteFile(fileName)
        time.sleep(1)
        dateYesterday = dateYesterday - timedelta(1)
    
    if(resultList):
        resultDF = Data.convertToDF(resultList)
        print(resultDF.info())
        #db.updateDatabase(resultDF)
    else:
        print("No update yet. Try again later!")
    
    time.sleep(1)
    print("Done")
    
  
Main ()