import xlrd as rd
import csv
import os
from difflib import SequenceMatcher
import nltk

from django.http import HttpResponseRedirect
from django.contrib import messages

from .models import product

def saveModel(valueList):
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
    workbook = rd.open_workbook(filename=path)
    sheet_names = workbook.sheet_names()
    sheet = workbook.sheet_by_name(sheet_names[0])
    headers = sheet.row(1)
    del headers[32]
    listOfEntriesAndTypes = {'amendedPN':'str', 'gaiaPN':'str', 'SgPN':'str', 'supplementaryPN':'str', 'description':'str', 'productCategory':'str', 'isManual':'bool', 'filmThickness':'str', 'status':'str', 'cylinderSequence':'str', 'sealingSequence':'str', 'USDCostPrice':'float', 'deliveredDutyGBP':'float', 'gaiaSellPrice':'float', 'samuelGrantPurchasePrice':'float', 'samuelGrantBuyBack':'float', 'PCSPerObject':'int', 'amountPerPallet':'int', 'minimumOrderQuantity':'int', 'deflatedWidth':'int', 'deflatedLength':'int', 'deflatedHeight':'int', 'inflatedWidth':'int', 'inflatedLength':'int', 'inflatedHeight':'int', 'CTNAmountPerPallet':'int', 'CTNWidth':'int', 'CTNLength':'int', 'CTNHeight':'int', 'netWeight':'int', 'grossWeight':'int'}
    # Work Out which column index is associated with each entry
    colindex = 0
    for i in headers:
        #print(i.value, colindex)
        colindex += 1
        max = 0
        string = ""
        for j in listOfEntriesAndTypes.values():
            similarity = nltk.metrics.distance.jaro_winkler_similarity(i.value, j.value, p=0.1)
            if similarity > max:
                max = similarity
                string = j
        print(i,max,  string)





    print(len(listOfEntriesAndTypes))


def parseCSV(path):
    pass    