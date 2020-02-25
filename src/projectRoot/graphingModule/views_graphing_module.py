from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect

from .forms import facilityForm, productHistoryForm
from .models import facilities, productHistory

from projectRoot.databaseFunctions.models import product

# Product History Views
def view_product(request, pk):
    if request.method == 'POST':
        p = product.objects.get(pk=pk)
        pH = productHistory.objects.get(productID=p.pk)
        f = facilities.objects.get(pk=pH.facilityID)
        return render(request, 'viewProduct.html', 
        {'product' : p, 'productHistory' : pH, 'facility': f})
    pass

# Facility Views
def facilityList(request):
    pass

def addFacility(request):
    pass

def modifyFacility(request, pk):
    pass

def deleteFacility(request, pk):
    pass

def deleteAllFacilities(request):
    pass

