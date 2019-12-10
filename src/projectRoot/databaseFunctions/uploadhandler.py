import xlrd as rd
import csv
import os

from django.http import HttpResponseRedirect
from django.contrib import messages

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
    print(Headers)
    pass

def parseCSV(path):
    pass