import xlrd as rd
import csv
import os
from difflib import SequenceMatcher
import jellyfish
import time

from django.http import HttpResponseRedirect
from django.contrib import messages

from .models import product

def saveModel(valueList): #!TODO Redo SaveModel
    form = product.objects.get_or_create( amendedPN=valueList[0], gaiaPN=valueList[1],
            SgPN=valueList[2], supplementaryPN=valueList[5], description=valueList[4], productCategory=valueList[6],
            isManual=valueList[7], filmTThickness=valueList[8], status=valueList[9], cylinderSequence=valueList[29],
            sealingSequence=valueList[30], USDCostPrice=float(valueList[10]), deliveredDutyGBP=float(valueList[11]), gaiaSellPrice=float(valueList[12]),
            samuelGrantPurchasePrice=float(valueList[13]), samuelGrantBuyback=float(valueList[14]), PCSPerObject=int(valueList[15]), amountPerPallet=int(valueList[16]),
            minimumOrderQuantity=int(valueList[17]), deflatedWidth=int(valueList[18]), deflatedLength=int(valueList[19]), deflatedHeight=int(valueList[20]), inflatedWidth=int(valueList[21]),
            inflatedLength=int(valueList[22]), inflatedHeight=int(valueList[23]), CTNAmountPerPallet=int(valueList[24]), CTNWidth=int(valueList[25]), CTNLength=int(valueList[26]), CTNHeight=int(valueList[27]),
            netWeight=valueList[28], grossWeight=valueList[29], 
        )
    if form.is_valid():
        form.save()
        print(valueList[0], "Form Saved")
    else:
        print("Form is not")
    pass

def handleFile(request, spreadsheetUrl):
    path = os.path.abspath('projectRoot/media/'+str(spreadsheetUrl))
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
    'productCategory':'str', 'isManual':'bool', 'filmThickness':'str', 'STATUS':'str', 'cylinderSequence':'str', 
    'sealingSequence':'str', 'CP':'float', 'DDP':'float', 'GAIASP':'float', 'SGPP':'float', 'SGBB':'float', 'PCSPerRoll':'int', 
    'PCSPerPallet':'int', 'MOQ':'int', 'deflatedWidth':'int', 'deflatedLength':'int', 'deflatedHeight':'int', 
    'inflatedWidth':'int', 'inflatedLength':'int', 'inflatedHeight':'int', 'CTNAmountPerPallet':'int', 'CTNWidth':'int', 
    'CTNLength':'int', 'CTNHeight':'int', 'nettWeight':'int', 'grossWeight':'int'}
    
    # Work Out which column index is associated with each entry
    colindex = 0 # Keeping Track of which column indicates which database object
    continueAppend = False # ContinueAppend, tempCounter and tempString are used to make the phonetic algorithm more accurate by changeing strings.
    tempCounter = 0
    tempString = ""

    listOfColumIndexesAndAssociatedFields = {}

    for i in tailheaders:
        checkString = i.value
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
            
            listOfColumIndexesAndAssociatedFields[listOfEntriesAndTypes.get(string)+","+string] = colindex
    print(listOfColumIndexesAndAssociatedFields)
    # Loop Ends
    for rowIndex in (2, sheet.nrows):
        tempList = []
        colcount = 0
        for cell in sheet.row(rowIndex):
            print(cell)
            try:
                dataType = list(listOfColumIndexesAndAssociatedFields.keys())[list(listOfColumIndexesAndAssociatedFields.values()).index(colcount)].split(",")[0]
            except:
                dataType = "null"
            var = cell.value
            if var == "": # Lookup what column the cell is currently under and compare it to listOfColumIndexes....
                print(dataType)
                if dataType == "int":
                    var = -1
                elif dataType == "float":
                    var = -1.0
                # pass               
            tempList.append(var)
            colcount += 1

        print(tempList)
        
        # Save Model
        pass

    print("Time Taken: ", time.time() - t1)



def parseCSV(path):
    pass    