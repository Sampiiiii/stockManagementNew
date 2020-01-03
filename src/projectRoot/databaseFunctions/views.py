from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import documentForm, productForm
from .models import document, product

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
        #print(pk)
        d = document.objects.get(pk=pk)
        handleFile(request, d.document)
        return HttpResponseRedirect('/documents')

def product_list(request):
    products = product.objects.all()
    return render(request, 'products.html', {'products' : products})

def modify_product(request, pk):
    if request.method =='POST':
        print(pk)
        p = product.objects.get(pk=pk)
        form = productForm(instance=p)
    return render(request, 'modify_product.html', {
        'form': form
    })

def product_add(request):
    form = productForm()
    return render(request, 'modify_product.html', {'form' : form})

def delete_product(request, pk):
    if request.method == 'POST':
        print(pk)
        p = product.objects.get(pk=pk)
        p.delete()
        return HttpResponseRedirect('/products')
