from .maintance_date import *

def process_excel_file_place(facilityNum, place, dateList):
    processType=2
    
    result = ""
    for date in dateList:
        isLast = False
        if (date == dateList[-1]):
            isLast = True
        result = process_excel_file(processType, facilityNum, place, date, isLast=isLast)
        
    return result