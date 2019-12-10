from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import documentForm
from .models import document

from .uploadhandler import handleFile


def document_list(request):
    documents = document.objects.all()
    return render(request, 'documents.html', {
        'Documents' : documents
    })


def upload_document(request):
    if request.method == 'POST':
        form = documentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/documents')
    else:
        form = documentForm()
    return render(request, 'upload_document.html', {
        'form': form
    })


def delete_document(request, pk):
    if request.method =='POST':
        d = document.objects.get(pk=pk)
        d.delete()
        return HttpResponseRedirect('/documents')


def process_document(request, pk):
    if request.method =='POST':
        print(pk)
        d = document.objects.get(pk=pk)
        handleFile(request, d.document)
        return HttpResponseRedirect('/documents')
