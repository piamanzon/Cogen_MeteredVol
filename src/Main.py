from WebPage import WebPage

import Data
from datetime import date, timedelta,datetime
import Database

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
    lastDBDate = db.getLatestDate()
    
    #If Monday, get report from friday to sunday
    if date.today().weekday() == 0:
        for day in range(1,4):
            dateYesterday = date.today() - timedelta(day)
            print (dateYesterday)
            wb = WebPage(dateYesterday)
            wb.frame_switch("report_nav")
            wb.downloadReport()
            wb.closeBrowser()
            rawDataList = Data.processData(assetIDList, fileName, dateYesterday)
            if(rawDataList):
                resultList = resultList + rawDataList
                totalData = totalData + len(resultList)
            print("Length of list:" + str(len(resultList)))
            Data.deleteFile(fileName)
  
    #Else just download yesterday's report
    else:
        dateYesterday = date.today() - timedelta(1)
        wb = WebPage(dateYesterday)
        wb.frame_switch("report_nav")
        wb.downloadReport()
        wb.closeBrowser()
        rawDataList = Data.processData(assetIDList, fileName, dateYesterday)
        if(rawDataList):
            resultList = resultList + rawDataList
            totalData = totalData + len(resultList)
        print("Length of list:" + str(len(resultList)))
        Data.deleteFile(fileName)
    
    if(resultList):
        resultDF = Data.convertToDF(resultList)
        print(resultDF.info())
        #db.updateDatabase(resultDF)
    else:
        print("list is empty")
    
   
    print("done")
  
Main ()