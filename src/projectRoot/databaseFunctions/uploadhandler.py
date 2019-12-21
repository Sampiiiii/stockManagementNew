import xlrd as rd
import csv
import os

from django.http import HttpResponseRedirect
from django.contrib import messages

from .models import product

def genPrimaryKey():
    pass

def saveModel(valueList):
    valueList.insert(0, genPrimaryKey())
    form = product.objects.get_or_create(
            primaryKey=valueList[0], amendedPN=valueList[1], gaiaPN=valueList[2],
            SgPN=valueList[3], supplementaryPN=valueList[6], description=valueList[5], productCategory=valueList[7],
            isManual=valueList[8], filmTThickness=valueList[9], status=valueList[10], cylinderSequence=valueList[30],
            sealingSequence=valueList[31], USDCostPrice=valueList[11], deliveredDutyGBP=valueList[12], gaiaSellPrice=valueList[13],
            samuelGrantPurchasePrice=valueList[14], samuelGrantBuyback=valueList[15], PCSPerObject=valueList[16], amountPerPallet=valueList[17],
            minimumOrderQuantity=valueList[18], deflatedWidth=valueList[19], deflatedLength=valueList[20], deflatedHeight=valueList[21], inflatedWidth=valueList[22],
            inflatedLength=valueList[22], inflatedHeight=valueList[23], CTNAmountPerPallet=valueList[24], CTNWidth=valueList[25], CTNLength=valueList[26], CTNHeight=valueList[27],
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
        parseSpreadsheet(path)
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
            tempList.append(j.value)
        saveModel(tempList)
    pass
# Test Commit

def parseCSV(path):
    pass    