'''
Created on Nov 19, 2020

@author: pia.manzon
'''
import os
import time

def isDownloaded (filePath):
    waitTime = 5 #5 sec
    timeCounter = 0
    while (not os.path.exists(filePath)) :
        time.sleep(1)
        timeCounter += 1
        if timeCounter > waitTime:
            return False
    return True
    
def deleteFile(filePath):
    try:
        os.remove(filePath)
        print ("File deleted!")
    except IOError:
        print("Error in deleting the file!")
        raise
    return