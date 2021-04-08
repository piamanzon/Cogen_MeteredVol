'''
Created on Jan 7, 2021

@author: pia.manzon
'''
import csv
import pandas as pd 
from itertools import islice
import File
from datetime import time, datetime

def processData(assetIDList, fileName, reportDate):
    resultList = []
    assetCounter = 0
    try:
        with open(fileName, "r") as infile:
            reader = csv.reader(infile)
            
            for line in islice(reader, 12, None):
                
                #If all assets have been found, exit
                foundValue = [dictionary for dictionary in assetIDList if dictionary["AssetID"] == line[2]]
                if (assetCounter == 19):
                    break
                if foundValue:
                    assetCounter = assetCounter + 1
                    for hourIndex in range(len(line[3:])):
                        #if(float(line[3:][hourIndex]) == 0): #If value is not 0, store it to the list
                        tm = time(hourIndex)
                        combined = datetime.combine(reportDate, tm)
                        tempList = [foundValue[0]['Asset'], combined, float(line[3:][hourIndex])]
                        resultList.append(tempList)
                     
            return resultList 
    except Exception  as e:
        File.deleteFile(fileName)
        raise e

def convertToDF(dataList):
    df = pd.DataFrame(dataList, columns = ['Asset', 'TimeStamp', 'Volume' ]) 
    if((df['Volume'] == 0).all()):
        print("true")
    else:
        print ("false")
    print(df.info())
    return df
    