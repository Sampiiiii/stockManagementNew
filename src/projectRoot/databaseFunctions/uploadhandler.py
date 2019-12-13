import xlrd as rd
import csv
import os

from django.http import HttpResponseRedirect
from django.contrib import messages

from .forms import productForm

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
        form = productForm(tempList[0],tempList[1], tempList[2], tempList[3], tempList[4], tempList[5], tempList[6], tempList[7],
         tempList[8], tempList[9], tempList[10], tempList[11], tempList[12], tempList[13], tempList[14], tempList[15], tempList[16],
         tempList[17], tempList[18], tempList[19], tempList[20], tempList[21], tempList[22], tempList[23], tempList[24], tempList[25],
         tempList[26], tempList[27], tempList[28], tempList[29], tempList[30], tempList[31], tempList[32])
        if form.is_valid():
            form.save()
            print(i, "Form Saved")
        else:
            print("Form is not")
    pass

def parseCSV(path):
    pass