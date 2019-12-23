import xlrd as rd
import csv
import os

from django.http import HttpResponseRedirect
from django.contrib import messages

from .models import product

def saveModel(valueList):
    valueList.insert(0, genPrimaryKey())
    form = product.objects.get_or_create( amendedPN=valueList[0], gaiaPN=valueList[1],
            SgPN=valueList[2], supplementaryPN=valueList[5], description=valueList[4], productCategory=valueList[6],
            isManual=valueList[7], filmTThickness=valueList[8], status=valueList[9], cylinderSequence=valueList[29],
            sealingSequence=valueList[30], USDCostPrice=valueList[10], deliveredDutyGBP=valueList[11], gaiaSellPrice=valueList[12],
            samuelGrantPurchasePrice=valueList[13], samuelGrantBuyback=valueList[14], PCSPerObject=valueList[15], amountPerPallet=valueList[16],
            minimumOrderQuantity=valueList[17], deflatedWidth=valueList[18], deflatedLength=valueList[19], deflatedHeight=valueList[20], inflatedWidth=valueList[21],
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