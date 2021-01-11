'''
Created on Dec 23, 2020

@author: pia.manzon
'''
#Selenium Imports
from selenium import webdriver
from selenium.webdriver.support.ui import Select
#Date and Time Imports
import time
from datetime import date, timedelta
from selenium.webdriver.common.by import By


class WebPage ():
    def __init__(self, reportDate):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {
                                        "download.default_directory": r"C:\Users\pia.manzon\AppData\Local\Temp", #Change default directory for downloads
                                        "download.prompt_for_download": False, #To auto download the file
                                        "download.directory_upgrade": True,
                                        "plugins.always_open_pdf_externally": True #It will not show PDFtoDF directly in chrome
                                        })
        
        chromedriver_path = r'C:\Users\pia.manzon\Downloads\chromedriver_win32/chromedriver.exe'
        self.driver = webdriver.Chrome(executable_path=chromedriver_path, options=options) # This will open the Chrome window
        enbridgeLoginURL= "http://ets.aeso.ca/ets_web/docroot/Market/Reports/HistoricalReportsStart.html"
        self.driver.get(enbridgeLoginURL) #Open website
        self.reportDate = reportDate
        
    def downloadReport(self):
        time.sleep(3)
        select = Select(self.driver.find_element_by_name("SelectReport"))
        select.select_by_value("Market/Reports/PublicSummaryAllReportServlet")

        #CSV Format
        Select(self.driver.find_element_by_name("SelectFormat")).select_by_value("csv")  
        
        #Begin Date
        Select(self.driver.find_element_by_name("BeginMonth")).select_by_value(self.reportDate.strftime("%m"))        
        Select(self.driver.find_element_by_name("BeginDay")).select_by_value(self.reportDate.strftime("%d"))     
        Select(self.driver.find_element_by_name("BeginYear")).select_by_value(self.reportDate.strftime("%Y"))
       
        #End Date
        Select(self.driver.find_element_by_name("EndMonth")).select_by_value(self.reportDate.strftime("%m"))        
        Select(self.driver.find_element_by_name("EndDay")).select_by_value(self.reportDate.strftime("%d"))     
        Select(self.driver.find_element_by_name("EndYear")).select_by_value(self.reportDate.strftime("%Y"))
        
        #OK
        self.driver.find_element_by_css_selector('[alt="OK"]').click()
        
    
    def frame_switch(self, name):
        self.driver.switch_to.frame(self.driver.find_element_by_name(name))


    def getReportHTML(self, assetIDList):
        trs = self.driver.find_elements(By.TAG_NAME, "tr")
        
        if (len(trs) == 1):
            print("No update yet!")
            return 
       
        try:
            
            colNum = 2
            
            for rowNum in range(6,len(trs)):
                # Get the columns (all the column 2)        
                col = trs[rowNum].find_elements(By.TAG_NAME, "td")[colNum] 
                assetID = col.text
                foundValue = [dictionary for dictionary in assetIDList if dictionary["AssetID"] == assetID] #compare assetID to the list
                if foundValue:
                    print(trs[rowNum].text)
        
        except Exception as e:
            raise e

    
        
    def closeBrowser(self):
        time.sleep(1)
        self.driver.quit()   