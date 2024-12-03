from .maintance_date import *

def process_excel_file_facility(facilityNum, maintenanceList):
    processType=3
    
    result = ""
    for m in maintenanceList:
        isLast = False
        if (m == maintenanceList[-1]):
            isLast = True
        place = m.place
        date = m.date
        result = process_excel_file(processType, facilityNum, place, date, isLast = isLast)
        
    return result