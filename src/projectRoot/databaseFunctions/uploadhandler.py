import xlrd as rd
import csv
import os
import jellyfish
import time
import re

from django.http import HttpResponseRedirect
from django.contrib import messages

from .models import product

def saveModel(valueList):
    # Logic to determine status and product category
    s = valueList[8]
    pC = valueList[5]
    category_choices = [
        ('aaa', 'null'),
        ('ASH', 'AIR|SHIELD™'),
        ('AMA', 'AIR|MAT™'),
        ('APA', 'AIR|PAKK™'),
        ('CCA', 'Corr Case '),
        ('TCO', 'TRANS|COVER'),
        ('TCA', 'TRANS|CASE '),
    ]
    statuses_choices = [
        ('A', 'Active'),
    ]
    for category in category_choices:
        if pC in category[1]:
            valueList[5] = category[0]
            break
    else:
        valueList[6] == 'aaa' # If category does not match fill it with the null value.
    for status in statuses_choices:
        if s in status[1]:
            valueList[8] = status[0]
            break
    else:
        valueList[8] = 'A'
    if valueList[6].lower() == "manual":
        valueList[6] = True
    else:
        valueList[6] = False
    # Generating Form with inputs from the fed list
    p = product(amendedPN=valueList[0], GAIAPN=valueList[1],
            SgPN=valueList[2], description=valueList[3], supplementaryPN=valueList[4], productCategory=valueList[5],
            isManual=valueList[6], filmThickness=valueList[7], STATUS=valueList[8], CP=float(valueList[9]), DDP=float(valueList[10]), 
            GAIASP=float(valueList[11]),
            SGPP=float(valueList[12]), SGBB=float(valueList[13]), PCSPerRoll=int(valueList[14]), PCSPerPallet=int(valueList[15]),
            MOQ=int(valueList[16]), deflatedWidth=int(valueList[17]), deflatedLength=int(valueList[18]), 
            deflatedHeight=int(valueList[19]), inflatedWidth=int(valueList[20]), inflatedLength=int(valueList[21]), 
            inflatedHeight=int(valueList[22]), CTNAmountPerPallet=int(valueList[23]), CTNWidth=int(valueList[24]), 
            CTNLength=int(valueList[25]), CTNHeight=int(valueList[26]), nettWeight=valueList[27], grossWeight=valueList[28], 
            cylinderSequence=valueList[29],
            sealingSequence=valueList[30],
        )
    p.save()

def handleFile(request, spreadsheetUrl):
    path = os.path.abspath('projectRoot/media/'+str(spreadsheetUrl)) # Getting the path of the file from its url
    if path.endswith('.xlsx'):
        intelligentSpreadsheetParser(path)
        messages.info(request, "Parsing spreadsheet...")
    elif path.endswith('.csv'):
        parseCSV(path)
        messages.info(request, "Parsing CSV...")
    else:
        messages.warning(request, "The selected file is not parsable.")
        HttpResponseRedirect('/documents')
    pass

def parseSpreadsheet(path):
    workbook = rd.open_workbook(filename=path)
    sheet_names = workbook.sheet_names()
    sheet = workbook.sheet_by_name(sheet_names[0])
    Headers = sheet.row(1)
    print(Headers) # Headers encompass rows 0 and 1
    print(sheet.nrows) # Amount of rows
    for i in range(2, sheet.nrows): # Each row is a product entry from 2 - 172
        tempList = []
        for j in sheet.row(i):
            var = j.value
            if var == "":
                if j.ctype == 2: # Cell would contain a float
                    var == -1 # Treat -1 as a null value
                elif j.ctype == 1: # Cell would contain a string
                    var == "Null"
            tempList.append(j.value)
        saveModel(tempList)
    pass

def intelligentSpreadsheetParser(path):
    t1 = time.time()
    # Open Spreadsheet
    workbook = rd.open_workbook(filename=path)
    sheet_names = workbook.sheet_names()
    sheet = workbook.sheet_by_name(sheet_names[0]) # Product data is on the first sheet
    head, tailheaders = sheet.row(0), sheet.row(1) 
    del tailheaders[32]
    # The below dictionary is a lookup table of what each field in the database should store, this is used to deal with the issue of empty cells
    listOfEntriesAndTypes = {'amendedPN':'str', 'GAIAPN':'str', 'SgPN':'str', 'supplementaryPN':'str', 'description':'str', 
    'productCategory':'str', 'isManual':'bool', 'filmThickness':'int', 'STATUS':'str', 'cylinderSequence':'str', 
    'sealingSequence':'str', 'CP':'float', 'DDP':'float', 'GAIASP':'float', 'SGPP':'float', 'SGBB':'float', 'PCSPerRoll':'int', 
    'PCSPerPallet':'int', 'MOQ':'int', 'deflatedWidth':'int', 'deflatedLength':'int', 'deflatedHeight':'int', 
    'inflatedWidth':'int', 'inflatedLength':'int', 'inflatedHeight':'int', 'CTNAmountPerPallet':'int', 'CTNWidth':'int', 
    'CTNLength':'int', 'CTNHeight':'int', 'nettWeight':'int', 'grossWeight':'int'}
    
    # Work Out which column index is associated with each entry
    colindex = -1 # Keeping Track of which column indicates which database object
    continueAppend = False # ContinueAppend, tempCounter and tempString are used to make the phonetic algorithm more accurate by changeing strings.
    tempCounter = 0
    tempString = ""

    listOfColumIndexesAndAssociatedFields = []

    for columnHeader in tailheaders:
        checkString = columnHeader.value
        appendString = head[colindex].value
        if checkString =="Short Description": # Short Description will never be added to database in lieu of "Description"
            colindex += 1
        else:
            if "(Kg) / CTN/ROLL" in checkString: # Trimming Unnecessary SubStrings
                checkString = checkString.replace("(Kg) / CTN/ROLL", "").lower()
            elif " / CTN / Rolls " in checkString:
                checkString = checkString.replace(" / CTN / Rolls ", "")
            colindex += 1
            if appendString == "Dimension Deflated" or appendString == "Dimension Inflated / Outer" or continueAppend == True: # This is to increase phonetic algorithm accuracy
                tempCounter += 1                
                if tempCounter == 1:
                    tempString = appendString
                if "Deflated" in tempString:
                    tempString = "deflated"
                elif "Inflated" in tempString:
                    tempString = "inflated"
                continueAppend = True
                checkString = tempString + " " + checkString
                if tempCounter == 3:
                    continueAppend = False
                    tempString = ""
                    tempCounter = 0

            # Determining String Similarity inside a smaller for loop which will check it against the keys of the above dictionary
            max = 0
            string = ""
            for key in listOfEntriesAndTypes.keys():
                similarity = jellyfish.jaro_distance(checkString, key)
                if similarity > max:
                    max = similarity
                    string = key
            
            listOfColumIndexesAndAssociatedFields.append((listOfEntriesAndTypes.get(string), string, colindex))
    # Loop Ends
    for rowIndex in range(2, sheet.nrows):
        tempList = []
        colcount = 0
        col = ""
        for cell in sheet.row(rowIndex):
            dataType = "null"
            for t in listOfColumIndexesAndAssociatedFields: # T is the tuple inside the list
                if colcount == int(t[2]):
                    dataType = str(t[0])
                    col = str(t[1])
                    break
            else:
                dataType =="null"
                col = ""
            var = cell.value # Lookup what column the cell is currently under and compare it to listOfColumIndexes....
            if dataType == "int":
                var = re.sub(r"\D","",str(var))
                if var == "":
                    var = -1
                tempList.append(var)
            elif dataType == "float":
                if var == "":
                    var = -1.0
                tempList.append(var)
            elif dataType == "str":
                if var == "":
                    var = ""
                tempList.append(var)
            elif dataType == "bool":
                if var == "":
                    var == "Manual"
                tempList.append(var)
            elif dataType == "null":
                pass
            colcount += 1
        # Save Model
        saveModel(tempList)
        pass

    print("Time Taken: ", time.time() - t1)
    print("Done!")


def parseCSV(path):
    pass    