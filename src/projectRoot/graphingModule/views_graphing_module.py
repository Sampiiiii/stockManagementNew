from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect

from .forms import facilityForm, productHistoryForm;
from .models import facilities, productHistory;

# Create your views here.
def productHistoryList(request):
    productHistories = productHistoryForm.objects.all()
    return render(request, 'document')

def addProductHistory(request):
    form = productHistoryForm(request.POST)
    if form.is_valid():
        form.save()
        