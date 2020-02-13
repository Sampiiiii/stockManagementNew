from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect

from .forms import facilityForm, productHistoryForm
from .models import facilities, productHistory

# Product History Views
def productHistoryList(request):
    productHistories = productHistoryForm.objects.all()
    return render(request, 'document')

def addProductHistory(request):
    form = productHistoryForm(request.POST)
    if form.is_valid():
        form.save()

def modifyProductHistory(request, pk):
    pass

def deleteProductHistory(request, pk):
    pass

def deleteAllProductHistories(request):
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

