import xlrd
import os
from django.http import HttpResponseRedirect
from django.contrib import messages

def parsespreadsheet(request, spreadsheetUrl):
    path = os.path.abspath('projectRoot/media/'+str(spreadsheetUrl))
    if path.endswith('.xlsx'):
        workbook = xlrd.open_workbook(filename=path)
        sheet_names = workbook.sheet_names()
        print(sheet_names)
        messages.info(request, "The sewected spweadsheet has been pawsed UwU")
    else:
        messages.warning(request, "OwO The sewected fiwe is not a spweadsheet")
        HttpResponseRedirect('/documents')
    pass
