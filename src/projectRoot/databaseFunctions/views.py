from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import documentForm, productForm
from .models import document, product

from .uploadhandler import handleFile

# Documents
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
        d = document.objects.get(pk=pk)
        handleFile(request, d.document)
        return HttpResponseRedirect('/documents')

# Products

def product_list(request):
    products = product.objects.all()
    return render(request, 'products.html', {'products' : products})

#FIXME FIX THIS
def modify_product(request, pk):
    product_instance = product.objects.get(id=pk)
    print(product_instance)
    form = productForm(request.POST or None, instance=product_instance)
    print(form)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/products')
    return render(request, 'modify_product.html', {
        'form': form
    })
            
def product_add(request):
    form = productForm(request.POST)
    if form.is_valid(): 
        form.save()
        return HttpResponseRedirect('/products')
    return render(request, 'add_product.html', {'form' : form})

def delete_product(request, pk):
    if request.method == 'POST':
        print(pk)
        p = product.objects.get(pk=pk)
        p.delete()
        return HttpResponseRedirect('/products')

def delete_all_products(request):
    if request.method == 'POST':
        products = product.objects.all()
        for p in products:
            p.delete()
    return HttpResponseRedirect('/products')


